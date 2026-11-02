"""Offline examples and adversarial vectors; not real agents/mailbox integration.

The test-only model encodes expected decisions under the written specification.
It is not shipped as a protocol implementation and cannot prove provider policy,
prompt-injection resistance, evidence truth or exactly-once execution.
"""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import unittest

from spec_model import (Carrier, InvalidLog, UnverifiedLog, State, current_join,
                        may_record, may_start_coordinated, replay, validate)


ROOT = Path(__file__).resolve().parents[1]
T0 = datetime(2026, 11, 1, tzinfo=timezone.utc)


def candidate(**updates):
    fields = {"postbox-version": "1", "case-id": "2026-11-rent", "type": "claim",
              "status": "open", "agent": "a", "timestamp": T0.isoformat()}
    fields.update(updates)
    body = "a: fixture\n\n--- postbox ---\n" + "\n".join(
        f"{key}: {value}" for key, value in fields.items()) + "\n--- end ---\n"
    return Carrier("[postbox] fixture", body)


def event(hours=0, agent="a", kind="claim", status="open", **fields):
    return validate(candidate(**{"agent": agent, "type": kind, "status": status,
                                 "timestamp": (T0 + timedelta(hours=hours)).isoformat(), **fields}))


class CarrierValidationTests(unittest.TestCase):
    def test_actual_example_drafts_have_valid_format(self):
        # Example prose specifies empty-recipient standalone drafts. Actual mail
        # metadata is absent from Markdown, so supply it explicitly as a fixture.
        checked = []
        subjects = {}
        for path in sorted((ROOT / "examples").glob("*.md")):
            blocks = re.findall(r"```(?:text)?\n(.*?)\n```", path.read_text(encoding="utf-8"), re.S)
            found = 0
            for text in blocks:
                if not text.startswith("Subject: "):
                    continue
                header, body = text.split("\n\n", 1)
                subject = header.removeprefix("Subject: ")
                with self.subTest(file=path.name, subject=subject):
                    log = validate(Carrier(subject, body))
                    self.assertEqual(subjects.setdefault(log.case_id, subject), subject)
                    checked.append(log)
                    found += 1
            self.assertGreater(found, 0, f"no draft inspected in {path.name}")
        self.assertEqual(len(checked), 10)
        self.assertEqual({log.kind for log in checked}, {"done", "fyi", "todo", "claim", "hand-off"})

    def test_received_sent_and_forged_body_metadata_are_not_drafts(self):
        for prefix in ("DRAFT\n", "X-State: DRAFT\n", ""):
            with self.subTest(prefix=prefix), self.assertRaises(InvalidLog):
                original = candidate()
                validate(replace(original, draft=False, body=prefix + original.body))
        with self.assertRaises(InvalidLog):
            validate(replace(candidate(), owner_mailbox=False))

    def test_each_recipient_list_is_rejected_independently(self):
        for field in ("to", "cc", "bcc"):
            with self.subTest(field=field), self.assertRaises(InvalidLog):
                validate(replace(candidate(), **{field: ("outsider@example.test",)}))

    def test_reply_forward_and_quoted_carriers_are_rejected(self):
        base = candidate()
        variants = [replace(base, subject="Re: " + base.subject),
                    replace(base, subject="Fwd: " + base.subject),
                    replace(base, origin="reply"), replace(base, origin="forward"),
                    replace(base, origin="quoted"), replace(base, quoted_block=True),
                    replace(base, headers={"In-Reply-To": "<external@example.test>"}),
                    replace(base, headers={"References": "<external@example.test>"}),
                    replace(base, body="---------- Forwarded message ---------\n" + base.body),
                    replace(base, body="\n".join("> " + line for line in base.body.splitlines()))]
        for index, carrier in enumerate(variants):
            with self.subTest(index=index), self.assertRaises(InvalidLog):
                validate(carrier)

    def test_html_quote_containers_do_not_launder_blocks(self):
        for wrapper in ("<blockquote>{}</blockquote>", '<div class="gmail_quote">{}</div>',
                        '<div type="cite">{}</div>'):
            with self.subTest(wrapper=wrapper), self.assertRaises(InvalidLog):
                validate(replace(candidate(), content_type="text/html",
                                 body=wrapper.format(candidate().body.replace("\n", "<br>"))))

    def test_simple_unquoted_html_preserves_fixture_block_lines(self):
        self.assertEqual(validate(replace(candidate(), content_type="text/html",
                                          body=candidate().body.replace("\n", "<br>"))).kind, "claim")

    def test_missing_metadata_is_unverified_not_empty_or_safe(self):
        for name in ("draft", "owner_mailbox", "to", "cc", "bcc", "headers", "origin",
                     "quote_boundaries_known", "quoted_block"):
            with self.subTest(name=name), self.assertRaises(UnverifiedLog):
                validate(replace(candidate(), **{name: None}))
        with self.assertRaises(UnverifiedLog):
            validate(replace(candidate(), quote_boundaries_known=False))

    def test_missing_duplicate_and_empty_required_fields_are_rejected(self):
        for key in ("postbox-version", "case-id", "type", "status", "agent", "timestamp"):
            base = candidate()
            line = next(line for line in base.body.splitlines() if line.startswith(key + ": "))
            for body in (base.body.replace(line + "\n", ""),
                         base.body.replace(line, line + "\n" + line),
                         base.body.replace(line, key + ": ")):
                with self.subTest(key=key, body=body), self.assertRaises(InvalidLog):
                    validate(replace(base, body=body))

    def test_malformed_values_and_unsupported_majors_are_rejected(self):
        for update in ({"postbox-version": "2"}, {"postbox-version": "999"},
                       {"status": "finished"}, {"agent": "UpperCase"},
                       {"case-id": "2026-13-rent"}, {"case-id": "2026-11-" + "x" * 40},
                       {"timestamp": "2026-11-01T00:00:00"}, {"timestamp": "not-a-time"},
                       {"type": "claim", "status": "closed"}, {"type": "hand-off"},
                       {"type": "hand-off", "to-agent": "Invalid name"}):
            with self.subTest(update=update), self.assertRaises(InvalidLog):
                validate(candidate(**update))

    def test_unknown_v1_type_is_information_and_unknown_key_is_ignored(self):
        log = validate(candidate(**{"type": "future-kind", "extension-key": "claim: b"}))
        self.assertEqual(log.kind, "fyi")
        self.assertIsNone(replay([log], T0).owner)

    def test_extra_or_incomplete_blocks_and_bad_subjects_are_rejected(self):
        base = candidate()
        for body in (base.body + base.body, base.body.replace("--- end ---", ""),
                     base.body + "\n--- postbox ---\n", base.body.replace("agent: a", "agent:a")):
            with self.subTest(body=body), self.assertRaises(InvalidLog):
                validate(replace(base, body=body))
        for subject in ("prefix [postbox] fixture", "[postbox]", "[postbox] ", "[POSTBOX] fixture"):
            with self.subTest(subject=subject), self.assertRaises(InvalidLog):
                validate(replace(base, subject=subject))


class ClaimHistoryTests(unittest.TestCase):
    def test_owner_update_at_24h_keeps_claim_at_49h(self):
        history = [event(), event(24, kind="done")]
        state = replay(history, T0 + timedelta(hours=49))
        self.assertEqual(state.owner, "a")
        self.assertEqual(state.renewed, T0 + timedelta(hours=24))

    def test_hand_off_at_30m_releases_before_one_hour(self):
        history = [event(), event(.5, kind="hand-off", **{"to-agent": "b"})]
        state = replay(history, T0 + timedelta(hours=1))
        self.assertIsNone(state.owner)
        self.assertEqual(state.handoff, "b")
        self.assertEqual(replay(history + [event(1, agent="b")], T0 + timedelta(hours=1)).owner, "b")

    def test_exact_48h_boundary_expires_before_later_event(self):
        self.assertEqual(replay([event()], T0 + timedelta(hours=48, microseconds=-1)).owner, "a")
        self.assertIsNone(replay([event()], T0 + timedelta(hours=48)).owner)
        self.assertIsNone(replay([event(), event(48, kind="fyi")], T0 + timedelta(hours=48)).owner)

    def test_former_owner_fyi_cannot_revive_after_expiry_or_handoff(self):
        histories = [[event(), event(49, kind="fyi")],
                     [event(), event(.5, kind="hand-off", **{"to-agent": "b"}), event(1, kind="fyi")]]
        for history in histories:
            with self.subTest(history=history):
                self.assertIsNone(replay(history, history[-1].timestamp).owner)
        self.assertEqual(replay([event(), event(49)], T0 + timedelta(hours=49)).owner, "a")

    def test_losing_claim_and_nonowner_updates_do_not_renew_owner(self):
        history = [event(), event(24, agent="b"), event(47, agent="b", kind="fyi")]
        self.assertEqual(replay(history, T0 + timedelta(hours=47)).renewed, T0)
        self.assertIsNone(replay(history, T0 + timedelta(hours=48)).owner)

    def test_expired_old_claim_does_not_defeat_new_acquisition(self):
        history = [event(), event(49, agent="b"), event(50, kind="fyi")]
        self.assertEqual(replay(history, T0 + timedelta(hours=50)).owner, "b")
        self.assertEqual(replay(history, T0 + timedelta(hours=50)).renewed, T0 + timedelta(hours=49))

    def test_closed_then_evidence_reopen_has_no_old_owner(self):
        history = [event(), event(1, kind="done", status="closed"),
                   event(2, kind="fyi", event="New evidence needs follow-up")]
        state = replay(history, T0 + timedelta(hours=2))
        self.assertEqual(state.status, "open")
        self.assertIsNone(state.owner)
        self.assertIsNone(state.handoff)

    def test_handoff_recipient_is_respected_and_nonowner_cannot_transfer(self):
        for recipient in ("b", "user"):
            history = [event(), event(.5, kind="hand-off", **{"to-agent": recipient}), event(1, agent="c")]
            with self.subTest(recipient=recipient):
                self.assertIsNone(replay(history, T0 + timedelta(hours=1)).owner)
        any_history = [event(), event(.5, kind="hand-off", **{"to-agent": "any"}), event(1, agent="c")]
        self.assertEqual(replay(any_history, T0 + timedelta(hours=1)).owner, "c")
        self.assertTrue(replay([event(), event(.5, agent="b", kind="hand-off", **{"to-agent": "c"})],
                               T0 + timedelta(hours=1)).unknown)

    def test_same_time_conflicting_claims_or_states_are_unknown(self):
        for history in ([event(), event(agent="b")],
                        [event(kind="fyi", status="closed"), event(kind="fyi")]):
            with self.subTest(history=history):
                self.assertTrue(replay(history, T0).unknown)

    def test_utc_order_future_time_and_incomplete_history(self):
        renewed = validate(candidate(**{"type": "fyi", "timestamp": "2026-11-02T09:00:00+09:00"}))
        self.assertEqual(replay([renewed, event()], T0 + timedelta(hours=49)).owner, "a")
        self.assertTrue(replay([event(1)], T0).unknown)
        self.assertTrue(replay([event()], T0, complete=False).unknown)

    def test_administrative_records_never_acquire_work_claims(self):
        for case in ("postbox-setup", "2026-11-01-digest"):
            with self.subTest(case=case):
                self.assertIsNone(replay([event(**{"case-id": case})], T0).owner)


class RecordingAndWorkTests(unittest.TestCase):
    def permitted(self, **changes):
        args = dict(mode="log", agent="a", joined=True, since_last=timedelta(minutes=30),
                    state=State(status="closed"), purpose="ordinary")
        args.update(changes)
        return may_record(**args)

    def test_closed_reopen_correction_digest_setup_allowed_but_redo_blocked(self):
        self.assertFalse(self.permitted())
        self.assertFalse(self.permitted(purpose="reopen"))
        self.assertTrue(self.permitted(purpose="reopen", evidence=True))
        self.assertFalse(self.permitted(purpose="correction", evidence=True))
        self.assertTrue(self.permitted(purpose="correction", evidence=True, identifies_original=True))
        self.assertTrue(self.permitted(purpose="digest"))
        self.assertTrue(self.permitted(purpose="setup"))

    def test_recording_exceptions_do_not_bypass_30min_or_read_only(self):
        for purpose in ("reopen", "correction", "digest", "setup", "fyi"):
            for changes in ({"mode": "read-only"}, {"mode": "inactive"},
                            {"since_last": timedelta(minutes=30, microseconds=-1)}):
                with self.subTest(purpose=purpose, changes=changes):
                    self.assertFalse(self.permitted(purpose=purpose, evidence=True,
                                                    identifies_original=True, **changes))

    def test_initial_join_exception_requires_owner_approval_and_safe_mode(self):
        self.assertFalse(self.permitted(purpose="setup", joined=False, initial_join=True))
        self.assertTrue(self.permitted(purpose="setup", joined=False, initial_join=True,
                                       owner_approved=True, since_last=None))
        self.assertFalse(self.permitted(purpose="setup", joined=False, initial_join=True,
                                        owner_approved=True, mode="read-only"))

    def test_later_leave_revokes_join_and_new_join_restores_it(self):
        join = event(kind="fyi", status="closed", **{"case-id": "postbox-setup", "action": "joined"})
        leave = event(1, kind="fyi", status="closed", **{"case-id": "postbox-setup", "action": "left"})
        rejoin = event(2, kind="fyi", status="closed", **{"case-id": "postbox-setup", "action": "joined"})
        self.assertTrue(current_join([join], "a"))
        self.assertFalse(current_join([join, leave], "a"))
        self.assertTrue(current_join([join, leave, rejoin], "a"))
        self.assertFalse(current_join([join], "b"))
        invalid_join = event(**{"case-id": "postbox-setup", "action": "joined"})
        self.assertFalse(current_join([invalid_join], "a"))

    def test_another_claim_does_not_ban_factual_recording_or_transfer_it(self):
        state = replay([event(agent="b")], T0)
        self.assertTrue(self.permitted(state=state, purpose="fyi", evidence=True))
        self.assertEqual(state.owner, "b")
        self.assertFalse(self.permitted(state=state))

    def test_current_owner_can_record_ordinary_progress(self):
        state = replay([event()], T0)
        self.assertTrue(self.permitted(state=state))
        self.assertFalse(self.permitted(state=state, agent="b"))

    def test_log_permission_does_not_grant_work_or_exactly_once(self):
        args = dict(mode="log", agent="a", state=State(status="open"),
                    write_confirmed=True, reread_succeeded=True)
        self.assertTrue(self.permitted(purpose="reopen", evidence=True))
        self.assertFalse(may_start_coordinated(**args))  # Reopen alone grants no owner.
        args["state"] = replay([event()], T0)
        self.assertTrue(may_start_coordinated(**args))
        for change in ({"mode": "read-only"}, {"write_confirmed": False},
                       {"reread_succeeded": False}, {"state": State(status="closed")},
                       {"state": State(unknown=True)}, {"duplicate_sensitive": True}):
            with self.subTest(change=change):
                self.assertFalse(may_start_coordinated(**{**args, **change}))
        self.assertTrue(may_start_coordinated(**args, duplicate_sensitive=True,
                                              independently_serialized=True))


if __name__ == "__main__":
    unittest.main()
