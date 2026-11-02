"""Small offline test oracles for SPEC §§4, 6 and 7, not a runtime engine.

This no-code project does not implement an agent, mailbox connector, MIME trust
detector, authorization gateway or distributed lock. Carrier metadata and facts
such as standalone origin/evidence are explicit test fixtures, not assertions
in an email body. These models check examples and expected specification cases;
passing them does not establish real AI, provider or concurrency compliance.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from itertools import groupby
import re


LEASE = timedelta(hours=48)
FREQUENCY = timedelta(minutes=30)
REQUIRED = {"postbox-version", "case-id", "type", "status", "agent", "timestamp"}
KNOWN_TYPES = {"done", "todo", "fyi", "claim", "hand-off"}
NAME = re.compile(r"[a-z0-9-]+\Z")


class InvalidLog(ValueError):
    """Known-invalid carrier or syntax; never use it as protocol state."""


class UnverifiedLog(ValueError):
    """Required information is missing; never assume empty/safe metadata."""


@dataclass(frozen=True)
class Carrier:
    subject: str
    body: str
    draft: bool | None = True
    owner_mailbox: bool | None = True
    to: tuple[str, ...] | None = ()
    cc: tuple[str, ...] | None = ()
    bcc: tuple[str, ...] | None = ()
    headers: dict[str, str] | None = field(default_factory=dict)
    origin: str | None = "standalone"
    quote_boundaries_known: bool | None = True
    quoted_block: bool | None = False
    content_type: str = "text/plain"


@dataclass(frozen=True)
class Log:
    case_id: str
    kind: str
    status: str
    agent: str
    timestamp: datetime
    fields: dict[str, str]


class _FixtureHTML(HTMLParser):
    """Normalize simple fixture HTML, not arbitrary provider MIME output."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.has_quote_container = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "blockquote" or "gmail_quote" in classes or attrs.get("type") == "cite":
            self.has_quote_container = True
        if tag in {"br", "div", "p", "blockquote", "pre"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"div", "p", "blockquote", "pre"}:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)


def _case_id(value):
    if value == "postbox-setup":
        return True
    if len(value) > 40 or not re.fullmatch(r"\d{4}-(?:0[1-9]|1[0-2])-[a-z0-9-]+", value):
        return False
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}-digest", value):
        try:
            date.fromisoformat(value[:10])
        except ValueError:
            return False
    return True


def administrative(case_id):
    return case_id == "postbox-setup" or bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}-digest", case_id))


def validate(carrier):
    """Validate the deliberately small fixture representation of a candidate."""
    metadata = (carrier.draft, carrier.owner_mailbox, carrier.to, carrier.cc,
                carrier.bcc, carrier.headers, carrier.origin,
                carrier.quote_boundaries_known, carrier.quoted_block)
    if any(value is None for value in metadata) or not carrier.quote_boundaries_known:
        raise UnverifiedLog("required service metadata or quote boundaries missing")
    if not carrier.draft or not carrier.owner_mailbox:
        raise InvalidLog("not an owner-mailbox draft")
    if carrier.to or carrier.cc or carrier.bcc:
        raise InvalidLog("recipients present")
    if not carrier.subject.startswith("[postbox] ") or not carrier.subject[10:].strip():
        raise InvalidLog("subject is not the exact log prefix and a summary")
    headers = {key.lower(): value for key, value in carrier.headers.items()}
    if "in-reply-to" in headers or "references" in headers:
        raise InvalidLog("reply/reference headers present")
    if carrier.origin != "standalone" or carrier.quoted_block:
        raise InvalidLog("reply, forward or quoted carrier")
    body = carrier.body
    if carrier.content_type == "text/html":
        parser = _FixtureHTML()
        parser.feed(body)
        body = "".join(parser.parts)
        if parser.has_quote_container and "--- postbox ---" in body:
            raise InvalidLog("HTML quote carrier")
    elif carrier.content_type != "text/plain":
        raise UnverifiedLog("fixture model cannot inspect this body format")
    if re.search(r"(?m)^\s*>.*--- postbox ---", body):
        raise InvalidLog("quoted text block")
    if re.search(r"(?im)^\s*-+\s*forwarded message\s*-+", body):
        raise InvalidLog("forwarded-message wrapper")
    lines = body.splitlines()
    if lines.count("--- postbox ---") != 1 or lines.count("--- end ---") != 1:
        raise InvalidLog("need exactly one complete block")
    start, end = lines.index("--- postbox ---"), lines.index("--- end ---")
    if end <= start:
        raise InvalidLog("block delimiter order")
    fields = {}
    for line in lines[start + 1:end]:
        if ": " not in line:
            raise InvalidLog("key/value delimiter")
        key, value = line.split(": ", 1)
        if not NAME.fullmatch(key) or key in fields:
            raise InvalidLog("invalid or duplicate key")
        fields[key] = value
    if not REQUIRED <= fields.keys() or any(not fields[key].strip() for key in REQUIRED):
        raise InvalidLog("missing or empty required field")
    if fields["postbox-version"] != "1":
        raise InvalidLog("unsupported major version")
    if fields["status"] not in {"open", "closed"}:
        raise InvalidLog("invalid status")
    if not NAME.fullmatch(fields["agent"]) or not _case_id(fields["case-id"]):
        raise InvalidLog("invalid agent or case-id")
    try:
        stamp = datetime.fromisoformat(fields["timestamp"])
        if "T" not in fields["timestamp"] or stamp.utcoffset() is None:
            raise ValueError("timezone required")
        stamp = stamp.astimezone(timezone.utc)
    except ValueError as error:
        raise InvalidLog("invalid timezone-bearing timestamp") from error
    kind = fields["type"] if fields["type"] in KNOWN_TYPES else "fyi"
    if kind in {"claim", "hand-off"} and fields["status"] != "open":
        raise InvalidLog("claim and hand-off must be open")
    if kind == "hand-off" and not NAME.fullmatch(fields.get("to-agent", "")):
        raise InvalidLog("hand-off needs a valid recipient")
    if "due" in fields:
        try:
            date.fromisoformat(fields["due"])
        except ValueError as error:
            raise InvalidLog("invalid due date") from error
    return Log(fields["case-id"], kind, fields["status"], fields["agent"], stamp, fields)


@dataclass
class State:
    status: str | None = None
    owner: str | None = None
    renewed: datetime | None = None
    handoff: str | None = None
    unknown: bool = False


def replay(logs, now, *, complete=True):
    """Replay one case's accepted factual logs; evidence acceptance is external.

    This oracle intentionally cannot establish whether a claimed action occurred,
    a correction's evidence is true, or another agent's write is still invisible.
    """
    if not complete or any(log.timestamp > now for log in logs):
        return State(unknown=True)
    if len({log.case_id for log in logs}) > 1:
        raise ValueError("replay requires one case")
    state = State()
    for stamp, group in groupby(sorted(logs, key=lambda log: log.timestamp), key=lambda log: log.timestamp):
        group = list(group)
        if state.owner and stamp >= state.renewed + LEASE:
            state.owner = state.renewed = None
        effects = {(log.kind, log.status, log.agent, log.fields.get("to-agent")) for log in group}
        if len({log.status for log in group}) > 1 or (
            len(effects) > 1 and any(log.kind in {"claim", "hand-off"} for log in group)
        ):
            return State(unknown=True)
        for log in group:
            state.status = log.status
            if administrative(log.case_id) or log.status == "closed":
                state.owner = state.renewed = state.handoff = None
            elif log.kind == "hand-off":
                if state.owner != log.agent:
                    return State(unknown=True)
                state.owner = state.renewed = None
                state.handoff = log.fields["to-agent"]
            elif log.kind == "claim" and state.owner is None:
                if state.handoff in (None, "any", log.agent):
                    state.owner, state.renewed, state.handoff = log.agent, stamp, None
            elif state.owner == log.agent:
                state.renewed = stamp
    if state.owner and now >= state.renewed + LEASE:
        state.owner = state.renewed = None
    return state


def current_join(logs, agent):
    relevant = [log for log in logs if log.case_id == "postbox-setup" and log.agent == agent
                and log.kind == "fyi" and log.status == "closed"
                and log.fields.get("action") in {"joined", "left"}]
    if not relevant:
        return False
    last = max(log.timestamp for log in relevant)
    return {log.fields["action"] for log in relevant if log.timestamp == last} == {"joined"}


def may_record(*, mode, agent, joined, since_last, state, purpose, evidence=False,
               identifies_original=False, initial_join=False, owner_approved=False):
    """Model recording eligibility, not truth of evidence or permission to act."""
    if mode != "log" or (since_last is not None and since_last < FREQUENCY):
        return False
    if not joined and not (purpose == "setup" and initial_join and owner_approved):
        return False
    if state.unknown:
        return False
    if purpose in {"setup", "digest"}:
        return True
    if purpose == "reopen":
        return evidence
    if purpose == "correction":
        return evidence and identifies_original
    if purpose == "fyi":
        return evidence  # A factual update preserves the accepted status/owner.
    return (purpose == "ordinary" and state.status != "closed"
            and state.owner in (None, agent))


def may_start_coordinated(*, mode, agent, state, write_confirmed, reread_succeeded,
                          duplicate_sensitive=False, independently_serialized=False):
    """Automatic postbox-coordinated work only; direct owner tasks are out of scope."""
    return (mode == "log" and not state.unknown and state.status == "open"
            and state.owner == agent and write_confirmed and reread_succeeded
            and (not duplicate_sensitive or independently_serialized))
