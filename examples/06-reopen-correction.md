# 06 · closed の訂正と再開

**場面**: grok が書類提出を完了扱いにしましたが、あとから不足書類の通知を確認しました。過去の下書きを編集せず、理由を示すログで状態を訂正・再開します。記録できることと、実際に書類を送る許可は別です。参加・30分間隔などの条件を満たしているものとします。

## 最初の完了記録

```text
Subject: [postbox] 11月の書類提出

grok (done): 提出受付を確認した。必要な書類はそろっていると判断した。

--- postbox ---
postbox-version: 1
case-id: 2026-11-documents
type: done
status: closed
agent: grok
timestamp: 2026-11-03T09:00:00+09:00
remaining: none
--- end ---

--
ai-postbox-protocol v1: https://github.com/aigamoid/ai-postbox-protocol/tree/v1.0.0
```

## 新しい根拠による訂正・再開

```text
Subject: [postbox] 11月の書類提出

grok (todo): 不足書類の通知を確認したので、09:00の完了判断を訂正する。追加提出はまだ行っていない。

--- postbox ---
postbox-version: 1
case-id: 2026-11-documents
type: todo
status: open
agent: grok
timestamp: 2026-11-03T10:00:00+09:00
event: 不足書類の追加提出が必要という通知を確認
action: grok の 2026-11-03T09:00:00+09:00 の完了判断を訂正して再開
remaining: 不足書類の確認と提出（本人）
source: <missing-document@example.test>
--- end ---

--
ai-postbox-protocol v1: https://github.com/aigamoid/ai-postbox-protocol/tree/v1.0.0
```

closedだからという理由で訂正ログを拒否しません。新しい根拠を確認し、同じcase-id・件名で追記します。再開は古いclaimを復活させず、提出や送信の許可にもなりません。新情報がないのに、同じ作業をやり直すためだけに再開してはいけません。
