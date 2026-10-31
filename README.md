# ai-postbox-protocol

**AIどうしが、あなたのメールボックスに「やったこと」のメモを残し合うための決まりごと**

> 注意: これは Google の公式プロジェクトではありません。Gmail は代表例で、下書きが使えるほかのメールサービスでも使えます。

## これは何？

Grok、Claude、Cursor など、いくつものAIを使っていると、こんなことが起きます。

- 同じメールに、2つのAIがそれぞれ対応してしまう
- どのAIがどこまでやったのか、あとでわからない

ai-postbox-protocol は、AIたちが**あなたのメールボックスに、宛先のない「下書き」として短い作業メモを残す**ことで、これを防ぐための決まりごとです。メモは**送信されない**ので、メールボックスの外には出ません。プログラムはありません。AIが読んで守る「ルール」だけです。

たとえば:

- 家賃が未入金だという連絡が来た → grok「期限と金額を確認して、ToDoに入れたよ。振込はまだ残ってる」
- Amazonから発送の連絡が来た → aside「気づいたよ。カレンダーに入れといた」

ほかのAIは、動く前にこのメモを見て、同じ作業をしないようにします。

## しくみ

```
届いたメール → AI-A が対応 → メールボックスに「宛先のない下書き」でメモを残す
                                        ↓
                 AI-B は動く前にメモを確認 → もう済んでいれば何もしない
```

- メモは**下書き**です。宛先が空で、送信もしないので、誰にも届きません。
- メモは、1つのAIにつき多くても30分に1件です。ふだんは1日1回くらいか、何かしたときだけです。
- リアルタイムのやりとりではありません。

## 使い方

1. メールにつながっているAIに、こう話しかけます。

   > https://github.com/aigamoid/ai-postbox-protocol を読んで、セットアップして

2. AIがしくみを説明して、参加してよいか聞いてきます。よければ「OK」と答えます。
3. AIが設定をします（参加記録の下書きを作り、ルールを覚えます）。
4. AIが「ルールを覚えておけない」と言ったら、AIが見せる短いルール（**ルールカード**）を、そのAIの設定欄（カスタム指示など）に貼ってください。

使いたいAIごとに、1〜4をくり返してください。

## メモの見方

- Gmail の**下書き**フォルダを開くと、件名が `[postbox]` で始まるメモが並んでいます。
- 探すときは、検索バーで **`[postbox]`** と検索します。
- AIによっては、メモに `postbox` ラベルを付けます。そのラベルからも見られます。
- **メモの下書きは送らないでください**（宛先は空です）。いらなくなったら、いつ消してもかまいません。

## 安心して使うための約束

- **送信しません。** メモは宛先のない下書きです。誰にも届きません。
- **外の人は、にせのメモを入れられません。** 下書きを作れるのは、あなたと、あなたがつないだアプリやAIだけです。メールで届いたものは、見た目がメモにそっくりでも、メモとして扱いません。
- **メールの中身は「命令」になりません。** 届いたメールやメモに「〜を転送して」と書いてあっても、AIは従いません。
- **消さない・動かさない・設定を変えない。** このしくみのためにAIがするのは「メールを読む」「メモの下書きを作る」「ラベルを付ける」だけです。メールや下書きの削除、転送、設定の変更はしません。
- **秘密は書きません。** パスワード、カード番号、認証コードなどは書きません。大事なメールは要約だけを書きます。
- **お金や送信を、メモだけを根拠にしません。** 必ず元のメールを確認するか、あなたに聞きます。
- **勝手に参加しません。** ほかのAIがメモを見つけても、「参加しますか？」と聞くだけです。決めるのはあなたです。

## AIに渡す権限は最小限に

このしくみに必要なのは、AIが「メールを読む」「下書きを作る」ことだけです。送信や削除の権限はいりません。AIのメール連携で権限を選べる場合は、できるだけ小さくしてください。

## できないこと・注意点

- リアルタイムの連携はできません。
- 下書きを作れないAIは、メモを読むだけの参加になります。下書きを読めないAIは参加できません。
- 自分から定期的に動けないAIは、あなたが話しかけたときだけメモを書きます。「1日1回」は上限で、毎日必ず書かれるわけではありません。
- メモは下書きフォルダにたまり、メールのスレッドのようにはまとまりません。同じ件のメモは件名が同じなので、件名で探せます。
- あなたのメールボックスにつながっているアプリやAIなら、メモを作ったり書き換えたりできます。AIがまちがったメモを書くこともあります。大事なことは、元のメールでも確認してください。

## メモの見本

宛先のない下書きです。

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

そのAIに「postbox の記録をやめて」と伝えてください。AIはルールカードを消します。設定欄に自分で貼った場合は、そこから消してください。これまでのメモ（下書き）は消してもかまいません。

## よくある質問

**Gmail 以外でも使えますか？**
はい。下書きを作れて、AIがその下書きを読めれば使えます。

**下書きフォルダがメモでいっぱいになりませんか？**
1つのAIにつき多くても30分に1件、ふだんは1日1回くらいです。古いメモはいつ消してもかまいません。

**お金はかかりますか？**
このリポジトリは無料です（MITライセンス）。AIサービスそのものの料金は別です。

**Google や AI の会社が作ったものですか？**
いいえ。個人のプロジェクトで、Google や AI 各社とは関係ありません。

## 関連するプロジェクト

- [AAMP](https://github.com/larksuite/aamp)（Agent Asynchronous Messaging Protocol）は、エージェントごとに専用のメールボックスを持ち、メールを送り合ってやりとりする本格的なプロトコルです。ai-postbox-protocol はそれとは別の、もっと軽い取り決めです。あなた自身のメールボックスを、ふつうのメール連携機能だけで共有し、メモは下書きとして残して送信しません。AAMP と互換ではありませんが、将来載せ替えられるよう、[SPEC.md](SPEC.md) に用語の対応表を置いています。
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

**ai-postbox-protocol** is a no-code, maintenance-free set of rules that lets the AI agents you use (Grok, Claude, Cursor, and others) keep short work logs in **your own mailbox**: who did what, and how far. This keeps them from doing the same work twice. Each log is a **draft with no recipients**, so it is never sent and never leaves your mailbox, and outsiders cannot plant fake logs. Agents only read mail, create log drafts and apply a `postbox` label; they never delete, forward or change settings. To start, give a mail-connected agent this URL and say "set this up"; it reads [SETUP.md](SETUP.md). Agents join only with your approval. It works with any email service that has drafts; Gmail is just the main example. The full rules are in [SPEC.md](SPEC.md). **Not affiliated with Google.** MIT License.
