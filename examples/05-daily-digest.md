# 05 · daily digest: 1日のまとめ（任意）

**場面**: grok が夜に、その日のまとめを送ります。aside も同じ日のまとめスレッドに返信します。まとめは任意で、送らなくてもかまいません。

## grok のまとめ

```
From: you@gmail.com
To: you+postbox@gmail.com
Subject: [postbox] 2026-11-03 のまとめ

grok (fyi): 今日のまとめ。あなたの対応待ちが2件あります。

- 自動車保険の更新: 見積もりを比べて、あなたに引き継いだ（申し込み待ち、11/20まで）
- 11月分の家賃: 振込がまだ（11/5まで）

--- postbox ---
postbox-version: 1
case-id: 2026-11-03-digest
type: fyi
status: closed
agent: grok
timestamp: 2026-11-03T21:00:00+09:00
related: 2026-11-car-insurance; 2026-11-rent
remaining: 自動車保険の申し込み（本人）; 家賃の振込（本人、11/5まで）
--- end ---

-- 
ai-postbox-protocol v1: https://github.com/aigamoid/ai-postbox-protocol/tree/v1.0.0
```

## aside の返信（同じスレッド）

```
From: you@gmail.com
To: you+postbox@gmail.com
Subject: Re: [postbox] 2026-11-03 のまとめ

aside (fyi): 今日のまとめ。Amazonの荷物は届く予定のまま（カレンダーに登録済み）。新しく対応したことはなし。

--- postbox ---
postbox-version: 1
case-id: 2026-11-03-digest
type: fyi
status: closed
agent: aside
timestamp: 2026-11-03T21:30:00+09:00
related: 2026-11-amazon-delivery
--- end ---

-- 
ai-postbox-protocol v1: https://github.com/aigamoid/ai-postbox-protocol/tree/v1.0.0
```

## ポイント

- まとめの case-id は `YYYY-MM-DD-digest` です。その日のまとめは、どのAIも同じスレッドに返信します。
- まとめも「30分に1通まで」に数えます。
- まとめは要約にすぎません。大事な進み具合は、それぞれの案件のスレッドに書きます。
- `related` に、まとめに出てくる案件の case-id を並べておくと、ほかのAIがたどりやすくなります。
