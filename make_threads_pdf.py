"""
Threads投稿テンプレート10選 PDF
シェアキャンペーン特典用
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus.flowables import HRFlowable

# フォント
pdfmetrics.registerFont(TTFont('NotoSansJP', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('NotoSansJP-Bold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('NotoSansJP', normal='NotoSansJP', bold='NotoSansJP-Bold', italic='NotoSansJP', boldItalic='NotoSansJP-Bold')

# カラー
C_BG      = colors.HexColor('#F7F4F0')
C_DARK    = colors.HexColor('#2E3D45')
C_ACCENT  = colors.HexColor('#C87941')
C_ACCENT_L = colors.HexColor('#EDD5BE')
C_TEXT    = colors.HexColor('#3A3530')
C_TEXT_L  = colors.HexColor('#7A6F66')
C_WHITE   = colors.white
C_TEMPLATE_BG = colors.HexColor('#F0EBE5')
C_EXAMPLE_BG  = colors.HexColor('#EAF2F8')
C_EXAMPLE_BD  = colors.HexColor('#A8C8DC')

# パターンごとのカラー
PATTERN_COLORS = [
    colors.HexColor('#5B8FA8'),
    colors.HexColor('#7A9E7E'),
    colors.HexColor('#C87941'),
    colors.HexColor('#9B7EC8'),
    colors.HexColor('#C87878'),
    colors.HexColor('#7A9E9A'),
    colors.HexColor('#C4A35A'),
    colors.HexColor('#8FA87A'),
    colors.HexColor('#A87AA8'),
    colors.HexColor('#7A8FA8'),
]

# ===== テンプレートデータ =====
TEMPLATES = [
    {
        'no': 1,
        'pattern': 'PAS型',
        'title': '悩み共感から入る',
        'scene': 'フォロワーの悩みに共感してもらいたいとき',
        'basis': '問題提示→共感→解決策の流れが最もコメントを生みやすい',
        'template': '''「[悩みを一言で]」

これ、すごく聞くんですよね。

[悩みの原因を一言で]
だけなんですよね。

だからこそ [解決策・提供物] を
[形式] にしました。

[CTA または問いかけ]''',
        'example': '''「AIで書いた文章、なんか自分っぽくない」

これ、すごく聞くんですよね。

AIに「あなたのこと」を
伝えられていないだけなんですよね。

だからこそプロンプトジェネレーターを
無料で作りました。

↓ LINE登録でお受け取りください''',
    },
    {
        'no': 2,
        'pattern': '逆説型',
        'title': '常識を覆す意外な真実',
        'scene': '「えっ？」という驚きでリポストを誘いたいとき',
        'basis': '常識と逆のことを言う投稿はリポスト率が高い傾向がある',
        'template': '''[一般的にいいとされていること] すると
[意外なマイナス面] になる。

これ、逆説的なんですけど
あるあるじゃないですか。

本当に大切なのは
[本質的なこと] なんですよね。

[感想または問いかけ]''',
        'example': '''AIを使えば使うほど
自分らしさが薄れていく。

これ、逆説的なんですけど
あるあるじゃないですか。

本当に大切なのは
「AIに自分を教える」ことなんですよね。

同じように感じている人いますか？''',
    },
    {
        'no': 3,
        'pattern': 'ビフォーアフター型',
        'title': '変化・成長のストーリー',
        'scene': '自分やお客様の変化をリアルに伝えたいとき',
        'basis': '具体的な変化は「自分もそうなれる」という希望を生む',
        'template': '''以前は [ビフォーの状態] でした。

[きっかけ・転機] がきっかけで
少しずつ変わって。

今は [アフターの状態] になっています。

[気づきや感想]

あなたはどんな変化がありましたか？''',
        'example': '''以前はAIを使うたびに
「なんか違う」と消していました。

プロンプトの書き方を変えたことで
自分の言葉に近い文章が出てくるように。

ツールより「伝え方」の問題だったんですよね。

何かきっかけになった気づき、ありますか？''',
    },
    {
        'no': 4,
        'pattern': '数字リスト型',
        'title': 'ポイントを番号で整理',
        'scene': 'ノウハウや気づきをまとめて伝えたいとき',
        'basis': '奇数（3・5・7）のリストが最も記憶に残りやすい',
        'template': '''[テーマ] で大切な [数字] つのこと

[番号]. [ポイント1]
[番号]. [ポイント2]
[番号]. [ポイント3]

特に [番号] 番目は
[補足コメント]

保存しておいてください。''',
        'example': '''AI発信で失敗しやすい3つのパターン

1. とりあえず全部AIに任せる
2. 出てきた文章をそのまま使う
3. フィードバックなしで繰り返す

特に3番目は気づきにくいので
じわじわ「自分らしさ」が消えていきます。

保存しておいてください。''',
    },
    {
        'no': 5,
        'pattern': '問いかけ型',
        'title': '質問でコメントを引き出す',
        'scene': 'エンゲージメントを上げてアルゴリズムに乗りたいとき',
        'basis': '最後の問いかけでコメント数が平均2.5倍になるデータがある',
        'template': '''突然ですが、[質問] ですか？

[自分の体験や観察を1〜2行]

意外とみんなそうみたいで。

ちなみに僕は [自分の答え] です。

あなたはどうですか？''',
        'example': '''突然ですが、AIツールを
毎日使えていますか？

「使おうと思って開いたけど
何を頼めばいいかわからない」
という声をよく聞きます。

ちなみに僕は朝の文章下書きに使っています。

あなたはどうですか？''',
    },
    {
        'no': 6,
        'pattern': '対比型',
        'title': 'できる人 vs できない人',
        'scene': '気づきや違いをわかりやすく伝えたいとき',
        'basis': '対比構造は情報が整理されて「保存したい」と思わせる',
        'template': '''[テーマ] がうまい人と下手な人の違い
一言で言うと

うまい人：[特徴]
下手な人：[特徴]

ここだけなんですよね。

[感想または補足]''',
        'example': '''AI活用がうまい人と下手な人の違い
一言で言うと

うまい人：AIに「背景」を伝える
下手な人：「やってください」だけ伝える

ここだけなんですよね。

どれだけ伝えるかで
出てくる文章が全然変わります。''',
    },
    {
        'no': 7,
        'pattern': '気づき型',
        'title': '日常 → ビジネスの本質へ',
        'scene': '人柄を見せながら気づきをシェアしたいとき',
        'basis': '日常エピソードは親近感を生み、フォロー率を高める',
        'template': '''[日常の出来事] をしていて
気づいたことがあって。

[出来事の詳細1〜2行]

これって [ビジネス・発信] にも
そのまま言えますよね。

[本質的な気づきを一言]''',
        'example': '''料理のレシピ通りに作っても
「なんか違う」ってなること、ありますよね。

材料じゃなくて
「火加減と塩加減」が要なんですよね。

AIの文章も同じで
ツールより「伝え方の加減」が全てだと思っています。''',
    },
    {
        'no': 8,
        'pattern': 'ランキング型',
        'title': 'ベスト3でおすすめを伝える',
        'scene': 'おすすめツールや方法を比較しながら紹介したいとき',
        'basis': 'ランキング形式はスクロールを止めて最後まで読ませる効果がある',
        'template': '''私が実際に使ってよかった [テーマ] ベスト3

3位：[アイテム・方法]
→ [一言コメント]

2位：[アイテム・方法]
→ [一言コメント]

1位：[アイテム・方法]
→ [一言コメント]

[対象者] には特に1位を試してほしいです。''',
        'example': '''AIツールを使い始めた人に
試してほしいこと ベスト3

3位：ChatGPTで自己紹介文を作る
→ まず「AIってこういうことか」がわかる

2位：Geminiで投稿アイデアを出す
→ ネタ切れが減ります

1位：自分の文体プロンプトを作る
→ これをやると全部が変わります

ITが苦手な方にこそ1位から試してほしいです。''',
    },
    {
        'no': 9,
        'pattern': '共感収集型',
        'title': '「わかる！」を集める投稿',
        'scene': 'フォロワーと一緒に考えたい・仲間意識を作りたいとき',
        'basis': '「同じように感じている人いますか？」はコメントが集まりやすい',
        'template': '''[テーマ] って、なんでこんなに
[難しい・大変・時間がかかる] んだろう。

[具体的な自分の体験を1〜2行]

同じように感じている人、いますか？

ちなみに僕がやっていること：
[自分の対処法を一言]''',
        'example': '''発信って、なんでこんなに
続けるのが難しいんだろう。

「今日は何を書こう」と考えるだけで
30分経ってることがあります。

同じように感じている人、いますか？

ちなみに僕がやっていること：
朝起きたら気づきを3行だけメモする習慣。''',
    },
    {
        'no': 10,
        'pattern': 'ノウハウ提供型',
        'title': '3ステップで実用情報を届ける',
        'scene': 'すぐ使える情報を提供して保存・シェアを促したいとき',
        'basis': '手順が明確な投稿は「保存」率が高くリーチが伸びやすい',
        'template': '''[テーマ] を簡単にする方法

① [手順1]
② [手順2]
③ [手順3]

これだけで [効果・変化] が変わります。

[補足コメント]
保存しておいてください。''',
        'example': '''AIに「自分らしい文章」を書かせる方法

① 過去に書いた文章を3つ貼り付ける
② 「この文体の特徴を教えて」と聞く
③ その特徴を毎回の指示に加える

これだけで出てくる文章が
ぐっと「自分っぽく」なります。

保存しておいてください。''',
    },
]

# ===== スタイル =====
def make_styles():
    s = {}
    s['pattern_tag'] = ParagraphStyle('pattern_tag',
        fontName='NotoSansJP', fontSize=9, textColor=C_WHITE,
        alignment=TA_CENTER, leading=13)
    s['card_title'] = ParagraphStyle('card_title',
        fontName='NotoSansJP', fontSize=14, textColor=C_DARK,
        alignment=TA_LEFT, leading=21, spaceAfter=1*mm)
    s['scene'] = ParagraphStyle('scene',
        fontName='NotoSansJP', fontSize=9, textColor=C_TEXT_L,
        alignment=TA_LEFT, leading=14, spaceAfter=1*mm)
    s['basis'] = ParagraphStyle('basis',
        fontName='NotoSansJP', fontSize=8.5, textColor=C_ACCENT,
        alignment=TA_LEFT, leading=13, spaceAfter=2*mm)
    s['label'] = ParagraphStyle('label',
        fontName='NotoSansJP', fontSize=8, textColor=C_TEXT_L,
        alignment=TA_LEFT, leading=12, spaceAfter=1*mm)
    s['template_text'] = ParagraphStyle('template_text',
        fontName='NotoSansJP', fontSize=9.5, textColor=C_TEXT,
        alignment=TA_LEFT, leading=16)
    s['example_text'] = ParagraphStyle('example_text',
        fontName='NotoSansJP', fontSize=9, textColor=colors.HexColor('#2E5F7A'),
        alignment=TA_LEFT, leading=15)
    s['cover_main'] = ParagraphStyle('cover_main',
        fontName='NotoSansJP', fontSize=28, textColor=C_DARK,
        alignment=TA_CENTER, leading=42)
    s['cover_sub'] = ParagraphStyle('cover_sub',
        fontName='NotoSansJP', fontSize=12, textColor=C_TEXT_L,
        alignment=TA_CENTER, leading=20)
    s['cover_badge'] = ParagraphStyle('cover_badge',
        fontName='NotoSansJP', fontSize=10, textColor=C_ACCENT,
        alignment=TA_CENTER, leading=16)
    s['cover_note'] = ParagraphStyle('cover_note',
        fontName='NotoSansJP', fontSize=9, textColor=C_TEXT_L,
        alignment=TA_CENTER, leading=15)
    s['footer'] = ParagraphStyle('footer',
        fontName='NotoSansJP', fontSize=8, textColor=C_TEXT_L,
        alignment=TA_CENTER, leading=12)
    return s


# ===== カード =====
def make_card(t, styles, W):
    col = PATTERN_COLORS[t['no'] - 1]
    card_w = W - 30*mm

    # タグ（パターン名）
    tag_cell = Table(
        [[Paragraph(f'{t["pattern"]}', styles['pattern_tag'])]],
        colWidths=[22*mm]
    )
    tag_cell.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), col),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 2*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2*mm),
        ('ROUNDEDCORNERS', [4]),
    ]))

    # タイトル行
    title_row = Table(
        [[tag_cell, Paragraph(f'<b>No.{t["no"]:02d}　{t["title"]}</b>', styles['card_title'])]],
        colWidths=[24*mm, card_w - 28*mm - 6*mm]
    )
    title_row.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('ALIGN', (1,0), (1,0), 'LEFT'),
    ]))

    # 使用場面 + 根拠
    scene = Paragraph(f'📌 {t["scene"]}', styles['scene'])
    basis = Paragraph(f'📊 {t["basis"]}', styles['basis'])

    # テンプレート本文
    tpl_text = t['template'].replace('\n', '<br/>')
    tpl_para = Paragraph(tpl_text, styles['template_text'])
    tpl_inner = Table([[tpl_para]], colWidths=[card_w - 18*mm])
    tpl_inner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_TEMPLATE_BG),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 4*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 4*mm),
        ('ROUNDEDCORNERS', [4]),
    ]))

    # 記入例
    ex_text = t['example'].replace('\n', '<br/>')
    ex_para = Paragraph(ex_text, styles['example_text'])
    ex_inner = Table([[ex_para]], colWidths=[card_w - 18*mm])
    ex_inner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_EXAMPLE_BG),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 4*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 4*mm),
        ('BOX', (0,0), (-1,-1), 0.5, C_EXAMPLE_BD),
        ('ROUNDEDCORNERS', [4]),
    ]))

    inner_rows = [
        [title_row],
        [Spacer(1, 1.5*mm)],
        [scene],
        [basis],
        [Paragraph('▼ テンプレート（[ ] を書き換えて使う）', styles['label'])],
        [tpl_inner],
        [Spacer(1, 1.5*mm)],
        [Paragraph('▼ 記入例（AI × 起業テーマ）', styles['label'])],
        [ex_inner],
    ]
    inner = Table(inner_rows, colWidths=[card_w - 10*mm])
    inner.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0.5*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5*mm),
    ]))

    card = Table(
        [[Table([['']], colWidths=[2*mm]), inner]],
        colWidths=[2*mm, card_w - 4*mm]
    )
    card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), col),
        ('BACKGROUND', (1,0), (1,-1), colors.white),
        ('TOPPADDING', (0,0), (-1,-1), 3.5*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5*mm),
        ('LEFTPADDING', (1,0), (1,-1), 4*mm),
        ('RIGHTPADDING', (1,0), (1,-1), 4*mm),
        ('LEFTPADDING', (0,0), (0,-1), 0),
        ('RIGHTPADDING', (0,0), (0,-1), 0),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E2D9D0')),
        ('ROUNDEDCORNERS', [4]),
    ]))
    return KeepTogether(card)


# ===== 表紙 =====
def draw_cover(canvas, doc):
    canvas.saveState()
    W, H = A4
    M = 18*mm

    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)

    # 上部アクセントバー
    canvas.setFillColor(C_ACCENT)
    canvas.rect(M, H - M - 6*mm, W - 2*M, 6*mm, fill=1, stroke=0)

    # 枠
    canvas.setStrokeColor(C_ACCENT)
    canvas.setLineWidth(1.2)
    canvas.rect(M, M, W - 2*M, H - 2*M, fill=0, stroke=1)

    # 上部タグ
    canvas.setFont('NotoSansJP', 10)
    canvas.setFillColor(C_WHITE)
    canvas.drawCentredString(W/2, H - M - 4*mm, '女性起業家のための シェア特典')

    # メインタイトル
    canvas.setFont('NotoSansJP', 30)
    canvas.setFillColor(C_DARK)
    canvas.drawCentredString(W/2, H*0.70, 'Threads 投稿')
    canvas.drawCentredString(W/2, H*0.63, 'テンプレート')

    # バッジ
    cx = W/2
    canvas.setFillColor(C_ACCENT_L)
    canvas.roundRect(cx-28*mm, H*0.565, 56*mm, 11*mm, 5*mm, fill=1, stroke=0)
    canvas.setFont('NotoSansJP', 11)
    canvas.setFillColor(C_ACCENT)
    canvas.drawCentredString(cx, H*0.575, '厳 選  10 パターン')

    # 区切り線
    canvas.setStrokeColor(C_ACCENT_L)
    canvas.setLineWidth(1)
    canvas.line(W*0.3, H*0.545, W*0.7, H*0.545)

    # サブテキスト
    canvas.setFont('NotoSansJP', 9.5)
    canvas.setFillColor(C_TEXT_L)
    canvas.drawCentredString(W/2, H*0.515, 'バズる投稿の研究をもとに設計した')
    canvas.drawCentredString(W/2, H*0.495, '穴埋め式テンプレート集')

    # パターン一覧
    y = H*0.43
    patterns = [
        ('01 PAS型', '02 逆説型', '03 ビフォーアフター型'),
        ('04 数字リスト型', '05 問いかけ型', '06 対比型'),
        ('07 気づき型', '08 ランキング型', '09 共感収集型'),
        ('10 ノウハウ提供型', '', ''),
    ]
    canvas.setFont('NotoSansJP', 9)
    canvas.setFillColor(C_TEXT_L)
    for row in patterns:
        x_positions = [W*0.18, W*0.46, W*0.72]
        for i, item in enumerate(row):
            if item:
                canvas.drawString(x_positions[i], y, item)
        y -= 6*mm

    # 下部
    canvas.setFillColor(colors.HexColor('#F0EBE5'))
    canvas.rect(M, M, W - 2*M, 18*mm, fill=1, stroke=0)
    canvas.setFont('NotoSansJP', 10)
    canvas.setFillColor(C_TEXT_L)
    canvas.drawCentredString(W/2, M + 6*mm, '内藤いさお')

    canvas.restoreState()


def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('NotoSansJP', 8)
    canvas.setFillColor(C_TEXT_L)
    page = canvas.getPageNumber()
    if page > 1:
        canvas.drawCentredString(A4[0]/2, 8*mm,
            f'Threads投稿テンプレート10選  ©内藤いさお  |  {page}')
    canvas.restoreState()


# ===== 使い方ページ =====
def make_howto(styles, W):
    items = []
    items.append(Paragraph('📖  このテンプレートの使い方', ParagraphStyle('ht',
        fontName='NotoSansJP', fontSize=16, textColor=C_DARK, leading=24)))
    items.append(HRFlowable(width='100%', thickness=1, color=C_ACCENT_L, spaceAfter=4*mm))

    body = ParagraphStyle('b', fontName='NotoSansJP', fontSize=10,
        textColor=C_TEXT, leading=18, spaceAfter=2*mm)
    step = ParagraphStyle('s', fontName='NotoSansJP', fontSize=10,
        textColor=C_TEXT, leading=18, leftIndent=4*mm, spaceAfter=1.5*mm)

    items.append(Paragraph(
        'このテンプレートは、バズった投稿の研究をもとに設計した「型」です。'
        '[ ] の部分を自分の言葉に書き換えるだけで投稿文が完成します。', body))
    items.append(Spacer(1, 3*mm))

    steps = [
        ('STEP 1', '使いたいパターンを選ぶ', '投稿したいテーマに近いパターンを選んでください。'),
        ('STEP 2', '[ ] を自分の言葉に書き換える', '「記入例」を参考に、自分のビジネスや体験に合わせて書き換えます。'),
        ('STEP 3', 'Threadsに投稿する', 'そのまま貼り付けて投稿。改行・絵文字はお好みで調整してください。'),
        ('STEP 4', '反応を見て型を選ぶ', 'いいね・コメント・リポストが多かったパターンを繰り返します。'),
    ]
    for label, title, desc in steps:
        row = Table([[
            Paragraph(f'<font color="#C87941"><b>{label}</b></font>', body),
            Paragraph(f'<b>{title}</b><br/>{desc}', body),
        ]], colWidths=[22*mm, None])
        row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 1*mm),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1*mm),
        ]))
        items.append(row)

    items.append(Spacer(1, 5*mm))

    tips_content = [
        Paragraph('<b>💡  より「自分らしく」するコツ</b>', body),
        Spacer(1, 2*mm),
        Paragraph('・テンプレートはあくまで「骨格」。語尾や言い回しは自分の普段の話し方に変えましょう', body),
        Paragraph('・記入例はAI×起業テーマで書いていますが、どんなテーマにも使えます', body),
        Paragraph('・「なんか違う」と感じたら、自分が実際に使っている言葉に置き換えてみてください', body),
    ]
    tips = Table([[ tips_content ]], colWidths=['100%'])
    tips.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_ACCENT_L),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING', (0,0), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 5*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 5*mm),
    ]))
    items.append(tips)
    return items


# ===== メイン =====
def build(output_path):
    W, H = A4
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        rightMargin=15*mm, leftMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm,
    )
    styles = make_styles()
    story = []

    # 表紙
    story.append(Spacer(1, 1*mm))
    story.append(PageBreak())

    # 使い方
    story += make_howto(styles, W)
    story.append(PageBreak())

    # テンプレートカード
    for i, t in enumerate(TEMPLATES):
        story.append(make_card(t, styles, W))
        story.append(Spacer(1, 4*mm))
        if i % 2 == 1 and i < len(TEMPLATES) - 1:
            story.append(PageBreak())

    doc.build(story, onFirstPage=draw_cover, onLaterPages=add_footer)
    print(f'完了: {output_path}')


if __name__ == '__main__':
    build('/Users/naitoisao/ClaudeCode/tokuten/threads_templates.pdf')
