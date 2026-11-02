# 04 · claim → hand-off → done: 1つの案件を引き受けて、引き継ぐ

**場面**: [03](03-todo-open.md) の「自動車保険の更新」の続きです。grok が引き受け（claim）、見積もりを比べてから、申し込みをあなたに引き継ぎます（hand-off）。最後に aside が完了を確認します。どのメモも、03 と同じ件名・同じ case-id の**新しい下書き**です（宛先なし）。

## 1. grok が引き受ける（claim）

```
Subject: [postbox] 自動車保険の更新（11/20まで）

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

## 2. aside は手を出さない（下書きは作らない）

grok はclaim下書きの作成を確認してから再検索し、競合した担当がないことを確認して作業します。これは最善努力の確認で、原子的な排他保証ではありません。二重実行が困る操作には、別途単独担当の指定などが必要です。

その日の夕方、aside も同じ更新案内に気づきました。ログを検索すると、grok が48時間以内に引き受けているので、aside は何もしません。「読んだよ」というだけのメモも作りません。

## 3. grok があなたに引き継ぐ（hand-off）

```
Subject: [postbox] 自動車保険の更新（11/20まで）

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
Subject: [postbox] 自動車保険の更新（11/20まで）

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

- 件名は最初のメモのままです（`Re:` も付けません）。下書きフォルダで件名を検索すれば、この件のメモが全部見つかります。
- 前のメモを書き換えずに、毎回新しい下書きを作ります。まちがいを直すときも、新しい下書きを作ります。
- 引き受け（claim）は、現在の担当者が有効期間内に書いた最新ログから48時間未満だけ有効です。hand-offやclosedで即解放し、正確に48時間で失効します。期限切れ後の通常ログでは復活しません。新しく引き受けるときは、指定された引継ぎ先も確認します。
- `to-agent: user` は「あなた（持ち主）に引き継ぐ」という意味です。AIの名前や `any`（誰でも）も使えます。
- 最後に `status: closed` のメモが作られたので、ほかのAIはこの件にもう手を出しません。
- 完了を確認するログの記録は、本人に引き継いだ手続きを代行することとは別です。新たな事実による再開や訂正は、closedの後も許されます（[06](06-reopen-correction.md)）。
