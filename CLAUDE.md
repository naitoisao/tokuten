# tokuten プロジェクト メモ

## 概要
LINE登録者向けの特典まとめページ。静的HTML1ファイル構成。

- **本番URL**: https://tokuten.vercel.app/
- **メルマガ登録者URL**: https://tokuten.vercel.app/?unlocked=true
- **GitHub**: https://github.com/naitoisao/tokuten
- **Vercel**: GitHubにpushすると自動デプロイ

---

## 現在の状態（完了済み）

### LINE特典（誰でも見られる）
1. 自分らしい文章プロンプトジェネレーター（style-generator.html）
2. 自己紹介文メーカー（https://jikoshokai-maker.vercel.app/）
3. 天命ナビLITE（https://tenmei-navi-ai.vercel.app/quiz）
4. ChatGPT・Gemini・Claude 比較表（Google Drive）

### メルマガ限定特典（?unlocked=true のときのみ表示）
1. AI時代の自分らしい発信の仕方【PDF資料】（Google Drive）
   - URL: https://drive.google.com/file/d/1nIsbyUZbAc88ePWOQWavlmNBFKIle494/view?usp=sharing

### シェアキャンペーン（ページ最下部・全員に表示）
- シェアしてほしい投稿: https://www.threads.com/@naitoisao/post/DYljv9PDqPS?xmt=AQG001I7yHvMeeeeeRTudjOsNqKfadY23srx90VoFYjHvA
- 特典①: 自分らしい発信をAIと作るワークブック
  - https://drive.google.com/file/d/1w7O-D0Uh5AizRh0_QXdCA3x64a5Ua6Q1/view?usp=drive_link
- 特典②: X・Threadsで読まれる投稿の型
  - https://drive.google.com/file/d/1tsMHrXtIfcE7XA6As8iYFuIey4HPgSnU/view?usp=drive_link
- LINE OA キーワード自動応答: 「シェアしました」→ PDF2冊のURL送信（設定済み）

### 設定済みURL（index.html JS変数）
- `MAIL_CTA_URL`: https://naitostyle.com/p/r/9npkWrWG
- `LINE_URL`: https://lin.ee/zEeMd0H
- `SHARE_THREADS_URL`: 上記Threads投稿URL
- `GIFT_WORKBOOK_URL`: ワークブックGoogle Drive URL
- `GIFT_TEMPLATES_URL`: 投稿の型Google Drive URL

### ロック解除のしくみ
- `?unlocked=true` パラメータがあるとメルマガ限定特典カードが表示される
- `?unlocked=true` のときはメルマガ登録CTAが非表示になる
- MyASPのステップメール1通目に `?unlocked=true` 付きURLを入れて運用

---

## 今後やること（TODO）

- [ ] MyASPのステップメールに `?unlocked=true` 付きURLを設定する
- [ ] メルマガ限定特典を増やす（内容が決まり次第 tokutenList に追加）

---

## ファイル構成

```
tokuten/
├── index.html              # 特典まとめページ（単一HTML、JS/CSS内包）
├── style-generator.html    # 自分らしい文章プロンプトジェネレーター
├── make_workbook_pdf.py    # ワークブックPDF生成スクリプト
├── make_threads_pdf.py     # Threads投稿テンプレートPDF生成スクリプト
├── workbook.pdf            # 自分らしい発信をAIと作るワークブック
├── threads_templates.pdf   # Threads投稿テンプレート（旧版）
├── HANDOFF.md              # プロジェクト設計書
└── CLAUDE.md               # このファイル
```

---

## 特典の追加方法

`index.html` 内の `tokutenList` 配列にオブジェクトを追加するだけ。

```javascript
{
  area: 'open',     // 'open' = LINE特典 / 'locked' = メルマガ限定
  emoji: '📋',
  tag: 'pdf',       // tool / pdf / video / checklist
  tagLabel: 'PDF',
  title: '特典タイトル',
  desc: '説明文',
  url: 'https://...',
  isNew: true,
},
```
