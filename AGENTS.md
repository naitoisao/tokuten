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
4. ChatGPT・Gemini・Codex 比較表（Google Drive）

### メルマガ限定特典（?unlocked=true のときのみ表示）
1. AI時代の自分らしい発信の仕方（Google Drive）

### 設定済みURL
- `MAIL_CTA_URL`: https://naitostyle.com/p/r/9npkWrWG
- メルマガ限定特典URL: https://drive.google.com/file/d/1nIsbyUZbAc88ePWOQWavlmNBFKIle494/view?usp=sharing

### ロック解除のしくみ
- `?unlocked=true` パラメータがあるとメルマガ限定特典カードが表示される
- `?unlocked=true` のときはメルマガ登録CTAが非表示になる
- MyASPのステップメール1通目に `?unlocked=true` 付きURLを入れて運用

---

## 今後やること（TODO）

- [ ] AIプロンプト帳PDF（make_pdf.pyで生成済み）を特典ページに掲載する
- [ ] メルマガ限定特典を増やす（内容が決まり次第 tokutenList に追加）
- [ ] MyASPのステップメールに `?unlocked=true` 付きURLを設定する

---

## ファイル構成

```
tokuten/
├── index.html        # 特典まとめページ（単一HTML、JS/CSS内包）
├── style-generator.html  # 自分らしい文章プロンプトジェネレーター
├── AI_prompt_book.pdf    # AIプロンプト帳（未掲載）
├── make_pdf.py       # PDF生成スクリプト（再生成時に使用）
├── HANDOFF.md        # プロジェクト設計書
└── AGENTS.md         # このファイル
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
