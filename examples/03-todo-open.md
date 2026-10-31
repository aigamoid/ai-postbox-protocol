# 03 · todo: やることがあるが、まだ誰も対応していない

**場面**: 自動車保険の更新案内が届いています。claude は気づきましたが、手続きはしていません。「やることがある」とだけ記録しておきます。

claude が作る下書き（宛先なし）:

```
Subject: [postbox] 自動車保険の更新（11/20まで）

claude (todo): 自動車保険の更新案内が届いている。11/20までに手続きが必要。まだ誰も対応していない。

--- postbox ---
postbox-version: 1
case-id: 2026-11-car-insurance
type: todo
status: open
agent: claude
timestamp: 2026-11-02T08:15:00+09:00
event: 保険会社から更新案内（期限 11/20）
remaining: 補償内容の確認と更新手続き
due: 2026-11-20
source: <a3f9e1.20261102@notice.example.com>
--- end ---

-- 
ai-postbox-protocol v1: https://github.com/aigamoid/ai-postbox-protocol/tree/v1.0.0
```

## ポイント

- `todo` は「やることがある。でも自分はやっていない」という意味です。
- どのAIでも、この件を引き受けられます（`claim`）。続きは [04-claim-handoff-thread.md](04-claim-handoff-thread.md) にあります。
- `due` に期限を書いておくと、ほかのAIが優先順位を決めやすくなります。
