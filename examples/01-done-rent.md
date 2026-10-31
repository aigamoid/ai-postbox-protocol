# 01 · done: 家賃の未入金連絡に対応した

**場面**: 管理会社から「11月分の家賃が未入金です」というメールが届きました。grok が期限と金額を確認して、ToDoに登録しました。振込はあなた本人がする必要があるので、まだ残っています。

grok が作る下書き（宛先なし）:

```
Subject: [postbox] 11月分の家賃の未入金連絡

grok (done): 家賃の期限と金額を確認してToDoに登録した。振込はまだ（本人の対応が必要）。

--- postbox ---
postbox-version: 1
case-id: 2026-11-rent
type: done
status: open
agent: grok
timestamp: 2026-11-01T10:30:00+09:00
event: 管理会社から11月分の家賃の未入金連絡（期限 11/5）
action: ToDo「家賃を振り込む（11/5まで）」を作成
remaining: 振込（本人）
due: 2026-11-05
source: <20261101093000.k7x2@mail.example.com>
--- end ---

-- 
ai-postbox-protocol v1: https://github.com/aigamoid/ai-postbox-protocol/tree/v1.0.0
```

## ポイント

- 宛先のない新しい下書きとして残します。送信はしません。
- `type: done`（やった）でも、振込が残っているので `status: open`（未完了）にしています。
- 振込先の口座番号は書きません。必要なときは元のメールを見ます。
- `source` に元のメールの Message-ID を入れておくと、ほかのAIが「同じ件だ」とすぐわかります。
- 同じ件のメモは、ずっと同じ件名にします。件名で探せるようにするためです。
