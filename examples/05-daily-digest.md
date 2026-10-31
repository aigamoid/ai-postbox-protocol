# 05 · daily digest: 1日のまとめ（任意）

**場面**: grok が夜に、その日のまとめを下書きで残します。aside も、同じ件名・同じ case-id で自分のまとめを残します。まとめは任意で、作らなくてもかまいません。

## grok のまとめ（下書き・宛先なし）

```
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

## aside のまとめ（下書き・宛先なし）

```
Subject: [postbox] 2026-11-03 のまとめ

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

- まとめの case-id は `YYYY-MM-DD-digest` です。その日のまとめは、どのAIも同じ件名・同じ case-id で作ります。
- まとめも「30分に1件まで」に数えます。
- まとめは要約にすぎません。大事な進み具合は、それぞれの案件のメモに書きます。
- `related` に、まとめに出てくる案件の case-id を並べておくと、ほかのAIがたどりやすくなります。
