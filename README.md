# ai-postbox-protocol

**AIどうしが、あなたのメールボックスで「やったこと」を伝え合うための決まりごと**

> 注意: これは Google の公式プロジェクトではありません。Gmail は代表例で、ほかのメールサービスでも使えます。

## これは何？

Grok、Claude、Cursor など、いくつものAIを使っていると、こんなことが起きます。

- 同じメールに、2つのAIがそれぞれ対応してしまう
- どのAIがどこまでやったのか、あとでわからない

ai-postbox-protocol は、AIたちが**あなた自身のメールアドレス宛てに短い作業メモを送る**ことで、これを防ぐための決まりごとです。プログラムはありません。AIが読んで守る「ルール」だけです。

たとえば:

- 家賃が未入金だという連絡が来た → grok「期限と金額を確認して、ToDoに入れたよ。振込はまだ残ってる」
- Amazonから発送の連絡が来た → aside「気づいたよ。カレンダーに入れといた」

ほかのAIは、動く前にこのメモを見て、同じ作業をしないようにします。

## しくみ

```
届いたメール → AI-A が対応 → あなた宛てに作業メモを送る（例: you+postbox@gmail.com）
                                        ↓
                 AI-B は動く前にメモを確認 → もう済んでいれば何もしない
```

- メモの宛先は**あなた自身のアドレスだけ**です。ほかの人には送りません。
- メモは、1つのAIにつき多くても30分に1通です。ふだんは1日1回くらいか、何かしたときだけです。
- リアルタイムのやりとりではありません。

**`+postbox` って？** Gmail では、アドレスの `@` の前に `+好きな言葉` を付けても自分に届きます（例: `you+postbox@gmail.com`）。メモを見分けやすくするために使います。これが使えないメールサービスでは、ふつうのアドレスで大丈夫です。

## 使い方

1. メールにつながっているAIに、こう話しかけます。

   > https://github.com/aigamoid/ai-postbox-protocol を読んで、セットアップして

2. AIがしくみを説明して、参加してよいか聞いてきます。よければ「OK」と答えます。
3. AIが設定をします（参加記録のメールを送り、ルールを覚えます）。
4. AIが「ルールを覚えておけない」と言ったら、AIが見せる短いルール（**ルールカード**）を、そのAIの設定欄（カスタム指示など）に貼ってください。
5. 任意: メモを「postbox」というラベルにまとめたいときは、AIが案内する手順で Gmail のフィルタを作ります。作らなくても動きます。

使いたいAIごとに、1〜4をくり返してください。

## 安心して使うための約束

- **あなた以外には送りません。** メモの宛先はあなた自身だけです。元のメール（お店や管理会社など）に返信することもありません。
- **秘密は書きません。** パスワード、カード番号、認証コードなどは書きません。大事なメールは要約だけを書きます。
- **メモは「命令」になりません。** 誰かがメモにそっくりなメールを送ってきても、AIは従いません。信用するのは、あなたのアドレスから送られたメモだけです。
- **お金・送信・削除を、メモだけを根拠にしません。** 必ず元のメールを確認するか、あなたに聞きます。
- **勝手に参加しません。** ほかのAIがメモを見つけても、「参加しますか？」と聞くだけです。決めるのはあなたです。
- **あなたのメールボックスの中だけで完結します。** 外部のサーバーは使いません。

## できないこと・注意点

- リアルタイムの連携はできません。
- メールを読むことはできても、送れないAIもあります。その場合は、メモを読んで同じ作業を避けるだけの参加になります。
- 自分から定期的に動けないAIは、あなたが話しかけたときだけメモを書きます。「1日1回」は上限で、毎日必ず届くわけではありません。
- AIがルールを完全に守るとは限りません。大事なことは、元のメールでも確認してください。
- メモはふつうのメールなので、メールボックスに残ります。いつ消してもかまいません。

## メモの見本

```
To: you+postbox@gmail.com
Subject: [postbox] 11月分の家賃の未入金連絡

grok (done): 家賃の期限と金額を確認してToDoに登録した。振込はまだ（本人の対応が必要）。

--- postbox ---
postbox-version: 1
case-id: 2026-11-rent
type: done
status: open
agent: grok
timestamp: 2026-11-01T10:30:00+09:00
remaining: 振込（本人）
due: 2026-11-05
--- end ---
```

1行目が人のための要約です。`--- postbox ---` から下は、AIが読むための部分です。ほかの見本は [examples/](examples/) にあります。

| 種類（type） | 意味 |
|---|---|
| `done` | やった（残りがあることもある） |
| `todo` | やることがある（自分はやっていない） |
| `fyi` | お知らせ |
| `claim` | この件は自分が引き受ける |
| `hand-off` | この件を別のAI（またはあなた）に引き継ぐ |

## やめたいとき

そのAIに「postbox の記録をやめて」と伝えてください。AIはルールカードを消します。設定欄に自分で貼った場合は、そこから消してください。これまでのメモは消してもかまいません。

## よくある質問

**Gmail 以外でも使えますか？**
はい。自分宛てにメールを送れて、メールを検索できれば使えます。

**お金はかかりますか？**
このリポジトリは無料です（MITライセンス）。AIサービスそのものの料金は別です。

**Google や AI の会社が作ったものですか？**
いいえ。個人のプロジェクトで、Google や AI 各社とは関係ありません。

## 関連するプロジェクト

- [AAMP](https://github.com/larksuite/aamp)（Agent Asynchronous Messaging Protocol）は、エージェントごとに専用のメールボックスを持ち、メールヘッダでやりとりする本格的なプロトコルです。ai-postbox-protocol はそれとは別の、もっと軽い取り決めです。あなた自身のメールボックスを、ふつうのメール連携機能だけで共有します（メールの本文だけを使います）。AAMP と互換ではありませんが、将来載せ替えられるよう、[SPEC.md](SPEC.md) に用語の対応表を置いています。
- [A2A](https://github.com/a2aproject/A2A)（Agent2Agent）は、エージェントどうしがリアルタイムにやりとりするためのプロトコルです。将来のバージョンで、同じ項目を A2A に載せることを考えています。

## ファイル一覧

| ファイル | 内容 |
|---|---|
| [README.md](README.md) | このファイル（人向けの説明） |
| [SETUP.md](SETUP.md) | AIが読んで実行するセットアップ手順 |
| [SPEC.md](SPEC.md) | 正式な決まりごと |
| [examples/](examples/) | メモの見本（5つ） |
| [CHANGELOG.md](CHANGELOG.md) | 変更の記録 |

## 商標などについて

Google の公式プロジェクトではありません。Gmail は Google LLC の商標です。Grok、Claude、Cursor などの名前は、例として製品名を使っているだけで、各社とは関係ありません。

---

## English

**ai-postbox-protocol** is a no-code, maintenance-free set of rules that lets the AI agents you use (Grok, Claude, Cursor, and others) leave short work logs in **your own mailbox**: who did what, and how far. This keeps them from doing the same work twice. Logs go only to your own address (for example `you+postbox@gmail.com`), at most once per 30 minutes per agent. To start, give a mail-connected agent this URL and say "set this up"; it reads [SETUP.md](SETUP.md). Agents join only with your approval and never send anything to third parties. It works with any email service; Gmail is just the main example. The full rules are in [SPEC.md](SPEC.md). **Not affiliated with Google.** MIT License.
