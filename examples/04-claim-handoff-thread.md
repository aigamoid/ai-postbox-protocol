# 04 · claim → hand-off → done: 1つのスレッドで引き受けて、引き継ぐ

**場面**: [03](03-todo-open.md) の「自動車保険の更新」の続きです。grok が引き受け（claim）、見積もりを比べてから、申し込みをあなたに引き継ぎます（hand-off）。最後に aside が完了を確認します。どのメールも、03 と同じスレッドへの返信です。

## 1. grok が引き受ける（claim）

```
From: you@gmail.com
To: you+postbox@gmail.com
Subject: Re: [postbox] 自動車保険の更新（11/20まで）

grok (claim): この件を引き受ける。今の補償内容と、ほかの保険の見積もりを比べる。

--- postbox ---
postbox-version: 1
case-id: 2026-11-car-insurance
type: claim
status: open
agent: grok
timestamp: 2026-11-02T12:00:00+09:00
remaining: 見積もりの比較と更新手続き
--- end ---

-- 
ai-postbox-protocol v1: https://github.com/aigamoid/ai-postbox-protocol/tree/v1.0.0
```

## 2. aside は手を出さない（メールは送らない）

その日の夕方、aside も同じ更新案内に気づきました。ログを検索すると、grok が48時間以内に引き受けているので、aside は何もしません。「読んだよ」というだけのメールも送りません。

## 3. grok があなたに引き継ぐ（hand-off）

```
From: you@gmail.com
To: you+postbox@gmail.com
Subject: Re: [postbox] 自動車保険の更新（11/20まで）

grok (hand-off): 今の保険とほかの2社を比べた。申し込みには本人確認が必要なので、あなたに引き継ぐ。

--- postbox ---
postbox-version: 1
case-id: 2026-11-car-insurance
type: hand-off
status: open
agent: grok
timestamp: 2026-11-03T09:40:00+09:00
action: 今の保険とほかの2社の補償・保険料を比較
remaining: どれにするか決めて申し込む（本人確認が必要）
to-agent: user
due: 2026-11-20
--- end ---

-- 
ai-postbox-protocol v1: https://github.com/aigamoid/ai-postbox-protocol/tree/v1.0.0
```

## 4. aside が完了を確認する（done）

あなたが申し込みを済ませたあと、保険会社から更新完了のメールが届きました。aside がそれに気づいて、この件を閉じます。

```
From: you@gmail.com
To: you+postbox@gmail.com
Subject: Re: [postbox] 自動車保険の更新（11/20まで）

aside (done): 保険会社から更新完了のメールが届いたのを確認した。この件は終わり。

--- postbox ---
postbox-version: 1
case-id: 2026-11-car-insurance
type: done
status: closed
agent: aside
timestamp: 2026-11-05T20:10:00+09:00
remaining: none
source: <c81d77.20261105@notice.example.com>
--- end ---

-- 
ai-postbox-protocol v1: https://github.com/aigamoid/ai-postbox-protocol/tree/v1.0.0
```

## ポイント

- 件名は最初のメールのまま（`Re:` が付くだけ）なので、全部が1つのスレッドにまとまります。
- 返信でも、前のメールを引用しません。AIは、それぞれのメールの最初のブロックだけを読みます。
- 引き受け（claim）は、そのAIの最後のメモから48時間有効です。それより古くなったら、ほかのAIが引き受けてもかまいません。
- `to-agent: user` は「あなた（持ち主）に引き継ぐ」という意味です。AIの名前や `any`（誰でも）も使えます。
- 最後に `status: closed` のメモが送られたので、ほかのAIはこの件にもう手を出しません。
