# 02 · fyi: Amazon の発送連絡に気づいた

**場面**: Amazon から発送の連絡が届きました。aside が気づいて、配達予定日をカレンダーに入れました。ほかにやることはありません。

```
From: you@gmail.com
To: you+postbox@gmail.com
Subject: [postbox] Amazonの荷物（11/3着予定）

aside (fyi): Amazonの発送連絡に気づいた。11/3の配達予定をカレンダーに入れた。

--- postbox ---
postbox-version: 1
case-id: 2026-11-amazon-delivery
type: fyi
status: closed
agent: aside
timestamp: 2026-11-01T14:05:00+09:00
event: Amazonから発送の連絡（11/3 配達予定）
action: カレンダーに「Amazonの荷物を受け取る」（11/3）を追加
remaining: none
source: <0100018f2c4e.a91b@email.example.com>
--- end ---

-- 
ai-postbox-protocol v1: https://github.com/aigamoid/ai-postbox-protocol/tree/v1.0.0
```

## ポイント

- お知らせなので `type: fyi`、やることが残っていないので `status: closed` です。
- あとで claude が同じ発送メールを見つけても、このメモを見れば「もうカレンダーに入っている」とわかるので、予定を二重に入れません。
- 住所や注文の細かい内容は書きません。
