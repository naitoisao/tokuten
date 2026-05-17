# 特典まとめページ - Claude Code 引き継ぎドキュメント

## プロジェクト概要

LINE登録者向けの特典まとめページ。2段構成で、LINE特典（誰でも使える）とメルマガ限定特典（ロック表示→メルマガ登録で解放）を一覧表示する。

## 背景・目的

- 椎原崇さんのYouTube→LINE→Notion特典モデルを参考に、内藤さん版を構築
- 対象：既にビジネスが回っているがITやAIが苦手な女性起業家（40〜50代）
- Notionは対象者にハードルが高いため、シンプルなWebページで提供
- 特典を増やしていく運用を前提とした設計

## ファイル構成

```
tokuten-page/
├── index.html    ← 特典まとめページ（単一HTML、JS/CSS内包）
└── HANDOFF.md    ← このファイル
```

## デプロイ手順

1. GitHubに新規リポジトリ作成（例：`naitoisao/tokuten`）
2. このディレクトリの中身をpush
3. Vercelにインポート → フレームワーク「Other」を選択 → デプロイ
4. 環境変数は不要（静的ページのためAPIキー不要）

## 特典の追加方法

`index.html` 内の `tokutenList` 配列にオブジェクトを追加するだけ。

```javascript
{
  area: 'open',        // 'open' = LINE特典, 'locked' = メルマガ限定
  emoji: '📋',         // 表示する絵文字
  tag: 'checklist',    // tool / pdf / video / checklist（タグの色分け）
  tagLabel: 'チェックリスト',  // タグの表示テキスト
  title: '特典のタイトル',
  desc: '特典の説明文',
  url: 'https://...',  // リンク先URL
  isNew: true,         // NEWバッジの表示
},
```

### area の値
- `open`：LINE特典エリア（リンクとして動作、誰でもアクセス可能）
- `locked`：メルマガ限定エリア（ロック表示、リンク無効、グレーアウト）

### tag の値と表示色
- `tool`：緑系（AIツール）
- `pdf`：紫系（PDF・テンプレート）
- `video`：青系（動画）
- `checklist`：オレンジ系（チェックリスト）

新しいタグが必要な場合は、CSSに `.tokuten-tag.新タグ名` を追加する。

## 変更が必要なURL（TODO）

以下の `#` を実際のURLに差し替えること：

1. **MAIL_CTA_URL**（冒頭の定数）→ MyASPメルマガ登録フォームのURL
2. **自己紹介文メーカー** の url → Vercelデプロイ済みURL（例：`https://jikoshokai-maker.vercel.app/`）
3. **天命ナビLITE** の url → 天命ナビLITE版のURL
4. **メルマガ限定特典** の url → メルマガ登録後に届くURLまたはそのまま `#`（ロック状態のためリンク不要）

## 関連プロジェクト

- **自己紹介文メーカー**（jikoshokai-maker）：LINE特典の1つ。Vercel + Edge Function + Claude API。GitHubリポジトリ：`naitoisao/jikoshokai-maker`（想定）
- **天命ナビ**：有料サービス。LITE版（5問→5タイプ）をLINE特典として無料提供予定。
- **MyASP**：メルマガ配信。LINE登録→特典ページ→メルマガ登録フォームの導線。

## 全体の導線設計

```
YouTube / Threads / SNS
  ↓
LINE友だち追加
  ↓
あいさつメッセージで特典ページURL送付
  ↓
特典ページ（このページ）
  ├── LINE特典エリア → ツールやPDFをすぐ利用
  └── メルマガ限定エリア → 「メルマガに登録する」ボタン
        ↓
      MyASP登録フォーム（メアド入力）
        ↓
      ステップメールで追加特典配信 → 天命ナビ等の有料サービス案内
```

## デザイン仕様

- **フォント**：Zen Maru Gothic（見出し）/ Noto Sans JP（本文）
- **カラー**：ベージュ系の温かみのある配色（var(--accent): #D4A574）
- **対象者配慮**：大きめの文字、余白多め、シンプルな操作
- **レスポンシブ**：スマホ表示最適化済み（max-width: 480px）
- **自己紹介文メーカーと統一したデザイントーン**

## 今後の拡張予定

- 特典の追加（発信セルフチェックシート、プロンプト集など）
- メルマガ登録後のロック解除機能（URLパラメータやパスワードで制御）
- アクセス解析の導入
