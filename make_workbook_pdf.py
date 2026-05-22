"""
自分らしい発信をAIと作るワークブック PDF生成スクリプト
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos

FONT_REG  = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
FONT_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
OUTPUT    = '/Users/naitoisao/ClaudeCode/tokuten/workbook.pdf'

# カラー定義
BG           = (250, 247, 243)
WHITE        = (255, 255, 255)
ACCENT       = (200, 121, 65)      # #C87941
ACCENT_L     = (237, 213, 190)     # #EDD5BE
ACCENT_TEXT  = (160, 96, 40)       # 文字用の濃いアクセント
PRIMARY      = (46, 61, 69)        # #2E3D45
TEXT         = (58, 53, 48)        # #3A3530
TEXT_L       = (122, 111, 102)     # #7A6F66
BORDER       = (220, 210, 202)
STEP1_C      = (91, 143, 168)
STEP2_C      = (122, 158, 126)
STEP3_C      = (200, 121, 65)
BLUE_BG      = (234, 242, 248)
BLUE_BD      = (160, 196, 220)

W = 210   # A4 幅 mm
H = 297   # A4 高さ mm
ML = 18   # 左右マージン
MT = 18   # 上マージン
CW = W - 2 * ML  # コンテンツ幅


class PDF(FPDF):
    def __init__(self):
        super().__init__(unit='mm', format='A4')
        # Arial Unicode を通常・太字両方に使う（日本語対応のため）
        self.add_font('JP',  fname=FONT_REG)
        self.add_font('JP-B', fname=FONT_REG)   # 太字は大きめサイズ・色で代替
        self.set_margins(ML, MT, ML)
        self.set_auto_page_break(auto=True, margin=22)

    # ── 便利メソッド ──────────────────────────────
    def fc(self, color):
        self.set_fill_color(*color)

    def dc(self, color):
        self.set_draw_color(*color)

    def tc(self, color):
        self.set_text_color(*color)

    def sp(self, h=5):
        self.ln(h)

    def text_block(self, txt, font='JP', size=10, color=TEXT, line_h=6, w=None):
        self.set_font(font, size=size)
        self.tc(color)
        self.multi_cell(w or CW, line_h, txt,
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def write_box(self, height=26, label=''):
        """記入欄（罫線ボックス）"""
        if label:
            self.set_font('JP', size=8)
            self.tc(TEXT_L)
            self.cell(CW, 5, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        x, y = self.get_x(), self.get_y()
        self.fc(WHITE); self.dc(BORDER)
        self.set_line_width(0.3)
        self.rect(x, y, CW, height, style='FD')
        # 薄い罫線（書きやすくするため）
        self.set_line_width(0.15)
        self.dc((230, 222, 215))
        line_gap = 8
        for i in range(1, int(height // line_gap)):
            ly = y + i * line_gap
            self.line(x + 3, ly, x + CW - 3, ly)
        self.ln(height + 3)

    def q_block(self, num, question, hint='', box_h=26, color=ACCENT):
        """設問ブロック"""
        x, y = self.get_x(), self.get_y()
        # Q番号バッジ
        self.fc(color); self.dc(color)
        self.set_line_width(0)
        self.rect(x, y, 9, 9, style='F')
        self.set_font('JP-B', size=9)
        self.tc(WHITE)
        self.set_xy(x, y + 0.5)
        self.cell(9, 8, f'Q{num}', align='C')
        # 質問文
        self.set_font('JP-B', size=12)
        self.tc(PRIMARY)
        self.set_xy(x + 11, y)
        self.multi_cell(CW - 11, 7, question,
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        # ヒント
        if hint:
            self.set_font('JP', size=8.5)
            self.tc(TEXT_L)
            self.multi_cell(CW, 5, f'>> {hint}',
                            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.sp(2)
        self.write_box(height=box_h)
        self.sp(2)

    def step_banner(self, num, title, sub, color):
        """STEPヘッダーバナー"""
        x, y = ML, self.get_y()
        self.fc(color); self.dc(color)
        self.set_line_width(0)
        self.rect(x, y, CW, 15, style='F')
        # STEP番号
        self.fc((*[max(0, c - 30) for c in color],))
        self.rect(x + 3, y + 2.5, 20, 10, style='F')
        self.set_font('JP-B', size=8)
        self.tc(WHITE)
        self.set_xy(x + 3, y + 3)
        self.cell(20, 9, f'STEP  {num}', align='C')
        # タイトル
        self.set_font('JP-B', size=13)
        self.tc(WHITE)
        self.set_xy(x + 26, y + 2)
        self.cell(CW - 28, 11, title)
        self.set_xy(ML, y + 15)
        self.sp(4)
        # サブタイトル
        self.text_block(sub, size=9.5, color=TEXT_L)
        self.sp(5)


# ═══════════════════════════════════════════
# 各ページ生成関数
# ═══════════════════════════════════════════

def page_cover(pdf):
    pdf.add_page()
    # 背景
    pdf.fc(BG); pdf.dc(BG)
    pdf.rect(0, 0, W, H, style='F')
    # 上部バー
    pdf.fc(ACCENT)
    pdf.rect(0, 0, W, 10, style='F')
    # 右上の装飾円
    pdf.fc(ACCENT_L)
    pdf.ellipse(W - 50, 20, 70, 70, style='F')
    pdf.fc((*[int(c * 1.04) for c in ACCENT_L],))
    pdf.ellipse(W - 35, 60, 40, 40, style='F')

    # バッジ
    pdf.fc(ACCENT_L)
    pdf.rect(ML, 26, 70, 8, style='F')
    pdf.set_font('JP', size=9)
    pdf.tc(ACCENT_TEXT)
    pdf.set_xy(ML, 27.5)
    pdf.cell(70, 5, '起業家のための発信ワークブック', align='C')

    # メインタイトル
    pdf.set_xy(ML, 46)
    pdf.set_font('JP-B', size=30)
    pdf.tc(PRIMARY)
    pdf.multi_cell(CW - 20, 14, '自分らしい発信を\nAIと作る\nワークブック',
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # サブ
    pdf.sp(4)
    pdf.set_font('JP', size=11)
    pdf.tc(TEXT_L)
    pdf.multi_cell(CW, 7, '3ステップで「発信コンセプト」が決まる\nAIへのプロフィールシートつき',
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # 区切り線
    pdf.sp(10)
    pdf.dc(ACCENT_L); pdf.set_line_width(0.6)
    pdf.line(ML, pdf.get_y(), ML + 40, pdf.get_y())
    pdf.sp(10)

    # ステップ一覧
    steps = [
        ('STEP 1', '発信コンセプトを見つける', '4問'),
        ('STEP 2', '自分らしさを言語化する', '3問'),
        ('STEP 3', 'AIプロフィールシートを完成させる', ''),
    ]
    colors = [STEP1_C, STEP2_C, STEP3_C]
    for (label, title, sub), col in zip(steps, colors):
        y = pdf.get_y()
        pdf.fc(col)
        pdf.rect(ML, y, 18, 7, style='F')
        pdf.set_font('JP-B', size=8)
        pdf.tc(WHITE)
        pdf.set_xy(ML, y + 0.5)
        pdf.cell(18, 6, label, align='C')
        pdf.set_font('JP-B', size=11)
        pdf.tc(PRIMARY)
        pdf.set_xy(ML + 21, y)
        pdf.cell(80, 7, title)
        if sub:
            pdf.set_font('JP', size=9)
            pdf.tc(TEXT_L)
            pdf.cell(30, 7, f'（{sub}）')
        pdf.set_xy(ML, y + 8)
        pdf.sp(3)

    # 著者
    pdf.set_xy(ML, H - 22)
    pdf.set_font('JP', size=10)
    pdf.tc(TEXT_L)
    pdf.cell(CW, 7, '内藤いさお', align='R')

    # 下部バー
    pdf.fc(ACCENT)
    pdf.rect(0, H - 9, W, 9, style='F')


def page_intro(pdf):
    pdf.add_page()
    pdf.fc(WHITE); pdf.rect(0, 0, W, H, style='F')

    pdf.sp(5)
    pdf.set_font('JP-B', size=18)
    pdf.tc(PRIMARY)
    pdf.multi_cell(CW, 10, 'このワークブックについて',
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    # アクセントライン
    pdf.dc(ACCENT); pdf.set_line_width(0.6)
    pdf.line(ML, pdf.get_y(), ML + 35, pdf.get_y())
    pdf.sp(7)

    pdf.text_block('「何を発信すればいいかわからない」「AIを使っても自分らしい文章にならない」——そんな声をよく聞きます。', size=11, line_h=7)
    pdf.sp(3)
    pdf.text_block('このワークブックは、7つの問いに答えるだけで発信コンセプトが明確になり、その答えをそのままAIに渡せる形に整えられるよう設計しています。', size=11, line_h=7)
    pdf.sp(3)
    pdf.text_block('正解はありません。思ったことをそのまま書いてください。', size=11, line_h=7)
    pdf.sp(8)

    # 「このワークが終わると」ボックス
    y = pdf.get_y()
    pdf.fc(ACCENT_L); pdf.dc(ACCENT_L)
    pdf.set_line_width(0)
    pdf.rect(ML, y, CW, 42, style='F')
    pdf.set_xy(ML + 5, y + 5)
    pdf.set_font('JP-B', size=10)
    pdf.tc(ACCENT_TEXT)
    pdf.cell(CW - 10, 6, 'このワークが終わると…')
    pdf.set_xy(ML + 5, y + 13)
    items = [
        '✓  自分が何を発信すればいいかが1行で言える',
        '✓  AIにコピペするだけで"自分っぽい文章"が出るようになる',
        '✓  発信に迷ったとき、ここに戻れば軸を取り戻せる',
    ]
    for item in items:
        pdf.set_font('JP', size=10)
        pdf.tc(PRIMARY)
        pdf.set_x(ML + 5)
        pdf.cell(CW - 10, 8, item, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.sp(8)

    # 使い方
    pdf.set_font('JP-B', size=12)
    pdf.tc(PRIMARY)
    pdf.multi_cell(CW, 7, '使い方', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.sp(3)

    howtos = [
        ('1', 'STEP 1〜2の問いに、直感で答えてください。'),
        ('2', 'STEP 3のシートにSTEP 1・2の答えを書き写します。'),
        ('3', 'シートをAI（ChatGPT・Claude・Geminiなど）にコピペして使います。'),
    ]
    for num, txt in howtos:
        y = pdf.get_y()
        pdf.fc(ACCENT); pdf.dc(ACCENT)
        pdf.set_line_width(0)
        pdf.ellipse(ML, y + 0.5, 7, 7, style='F')
        pdf.set_font('JP-B', size=9)
        pdf.tc(WHITE)
        pdf.set_xy(ML, y + 0.5)
        pdf.cell(7, 7, num, align='C')
        pdf.set_font('JP', size=10)
        pdf.tc(TEXT)
        pdf.set_xy(ML + 9, y)
        pdf.multi_cell(CW - 9, 7, txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.sp(2)


def page_step1(pdf):
    pdf.add_page()
    pdf.fc(WHITE); pdf.rect(0, 0, W, H, style='F')
    pdf.step_banner(1, '発信コンセプトを見つける',
        '次の4問に答えてください。「完璧な答え」でなくて大丈夫です。直感で書いてみましょう。',
        STEP1_C)

    pdf.q_block(1, 'あなたが一番助けたいのは、どんな人ですか？',
        '年齢・職業・状況など、具体的に想像してみましょう', box_h=24, color=STEP1_C)
    pdf.q_block(2, 'その人が今、一番困っていることは何ですか？',
        '悩み・不安・うまくいかないこと…どんなことで詰まっているか', box_h=24, color=STEP1_C)
    pdf.q_block(3, '「これは自分だから言える」と思うことは何ですか？',
        '経験・失敗・気づき・価値観など', box_h=24, color=STEP1_C)
    pdf.q_block(4, '発信を通じて、どんな人だと知られたいですか？',
        '「〇〇といえば自分」という〇〇に入る言葉を探すイメージで', box_h=24, color=STEP1_C)

    # まとめ欄
    y = pdf.get_y()
    pdf.fc(ACCENT_L); pdf.dc(ACCENT_L)
    pdf.set_line_width(0)
    pdf.rect(ML, y, CW, 8, style='F')
    pdf.set_xy(ML + 4, y + 1)
    pdf.set_font('JP-B', size=9)
    pdf.tc(ACCENT_TEXT)
    pdf.cell(CW - 8, 6, '▼  STEP 1 まとめ：私の「発信の軸」を1行で書いてみましょう')
    pdf.set_xy(ML, y + 8)
    pdf.sp(1)
    pdf.write_box(height=16)


def page_step2(pdf):
    pdf.add_page()
    pdf.fc(WHITE); pdf.rect(0, 0, W, H, style='F')
    pdf.step_banner(2, '自分らしさを言語化する',
        'AIに「あなたらしさ」を伝えるための言葉を整理します。',
        STEP2_C)

    pdf.q_block(5, 'あなたがよく使う言葉・口癖を教えてください',
        '「〜なんですよね」「〜な感じで」など、話し言葉でもOK', box_h=25, color=STEP2_C)
    pdf.q_block(6, '絶対に使いたくない言葉・表現はありますか？',
        '堅すぎる言葉、よそよそしい敬語、AIっぽいフレーズなど', box_h=25, color=STEP2_C)

    # Q7: トーン（チェック式）
    x, y = pdf.get_x(), pdf.get_y()
    pdf.fc(STEP2_C); pdf.dc(STEP2_C)
    pdf.set_line_width(0)
    pdf.rect(x, y, 9, 9, style='F')
    pdf.set_font('JP-B', size=9)
    pdf.tc(WHITE)
    pdf.set_xy(x, y + 0.5)
    pdf.cell(9, 8, 'Q7', align='C')
    pdf.set_font('JP-B', size=12)
    pdf.tc(PRIMARY)
    pdf.set_xy(x + 11, y)
    pdf.cell(CW - 11, 9, 'あなたの発信のトーンは？（近いものに○をつける）')
    pdf.set_xy(ML, y + 10)
    pdf.sp(3)

    tones = [
        ('親しみやすい',   'フォーマル・きちんとした'),
        ('やわらかい',     'キリッとしている'),
        ('話しかけるような', '読み物として完結している'),
        ('感情豊か',       '論理的・整理されている'),
        ('ユーモアがある',  'まじめ・誠実な'),
    ]
    col_w = (CW - 14) / 2
    for left, right in tones:
        y = pdf.get_y()
        # 左
        pdf.fc(WHITE); pdf.dc(BORDER); pdf.set_line_width(0.3)
        pdf.rect(ML, y, col_w, 8, style='FD')
        pdf.set_font('JP', size=9); pdf.tc(TEXT)
        pdf.set_xy(ML + 3, y + 1)
        pdf.cell(col_w - 6, 6, f'○  {left}')
        # vs
        pdf.set_font('JP', size=8); pdf.tc(TEXT_L)
        pdf.set_xy(ML + col_w + 1, y + 1)
        pdf.cell(12, 6, 'vs', align='C')
        # 右
        pdf.fc(WHITE); pdf.dc(BORDER)
        pdf.rect(ML + col_w + 14, y, col_w, 8, style='FD')
        pdf.set_font('JP', size=9); pdf.tc(TEXT)
        pdf.set_xy(ML + col_w + 17, y + 1)
        pdf.cell(col_w - 6, 6, f'○  {right}')
        pdf.set_xy(ML, y + 9)
        pdf.sp(1)

    pdf.sp(5)

    # まとめ欄
    y = pdf.get_y()
    pdf.fc((*[int(c * 0.9) for c in (200, 230, 200)],))
    pdf.fc(ACCENT_L); pdf.dc(ACCENT_L)
    pdf.set_line_width(0)
    pdf.rect(ML, y, CW, 8, style='F')
    pdf.set_xy(ML + 4, y + 1)
    pdf.set_font('JP-B', size=9)
    pdf.tc(ACCENT_TEXT)
    pdf.cell(CW - 8, 6, '▼  STEP 2 まとめ：私のトーンを一言で表すと（自由に書いてください）')
    pdf.set_xy(ML, y + 8)
    pdf.sp(1)
    pdf.write_box(height=15)


def page_step3(pdf):
    pdf.add_page()
    pdf.fc(WHITE); pdf.rect(0, 0, W, H, style='F')
    pdf.step_banner(3, 'AIプロフィールシートを完成させる',
        'STEP 1・2の答えをここに書き写してください。このシートをそのままAIにコピペして使います。',
        STEP3_C)

    # シートの枠
    y = pdf.get_y()
    sheet_h = 115
    pdf.fc((252, 248, 244)); pdf.dc(ACCENT)
    pdf.set_line_width(0.6)
    pdf.rect(ML, y, CW, sheet_h, style='FD')

    pdf.set_xy(ML + 5, y + 5)
    pdf.set_font('JP-B', size=10)
    pdf.tc(ACCENT_TEXT)
    pdf.cell(CW - 10, 6, '【AIへのコピペ用プロフィールシート】')
    pdf.sp(1)

    fields = [
        ('私は',               'Q1・Q3 の答えをもとに「〇〇のための〇〇」の形で'),
        ('発信テーマは',         'Q3・Q4 の答えをもとに'),
        ('読者は',             'Q1・Q2 の答えをもとに「〇〇に困っている〇〇な人」の形で'),
        ('私の口調・言い回しは', 'Q5 の答えをそのまま'),
        ('使いたくない言葉は',   'Q6 の答えをそのまま'),
        ('目指すトーンは',       'Q7 で○をつけたものを'),
    ]

    for label, hint_text in fields:
        yn = pdf.get_y()
        pdf.set_font('JP-B', size=9); pdf.tc(PRIMARY)
        pdf.set_xy(ML + 5, yn)
        pdf.cell(36, 5, label)
        # 下線
        pdf.dc(BORDER); pdf.set_line_width(0.25)
        pdf.line(ML + 44, yn + 4, ML + CW - 5, yn + 4)
        pdf.set_xy(ML + 5, yn + 6)
        pdf.set_font('JP', size=7.5); pdf.tc(TEXT_L)
        pdf.cell(CW - 10, 4, f'← {hint_text}')
        pdf.set_xy(ML, yn + 11)
        pdf.sp(2)

    # コピペテンプレート
    pdf.sp(6)
    pdf.set_font('JP-B', size=11)
    pdf.tc(PRIMARY)
    pdf.multi_cell(CW, 7, 'AIに渡すときのテンプレート（上のシートを埋めたらここにコピー）',
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.sp(2)

    ty = pdf.get_y()
    tbox_h = 72
    pdf.fc(BLUE_BG); pdf.dc(BLUE_BD)
    pdf.set_line_width(0.4)
    pdf.rect(ML, ty, CW, tbox_h, style='FD')

    pdf.set_xy(ML + 5, ty + 5)
    pdf.set_font('JP', size=9.5)
    pdf.tc((46, 80, 110))
    lines = [
        '以下の情報をふまえて、文章を書いてください。',
        '',
        '私は [「私は」欄の内容] です。',
        '発信テーマは「[発信テーマ欄の内容]」です。',
        '読者は「[読者欄の内容]」です。',
        '私の口調は [口調欄の内容] で、',
        '[使いたくない言葉欄の内容] は使わないでください。',
        'トーンは [トーン欄の内容] でお願いします。',
        '',
        '---',
        '[ここに今日お願いしたいことを書く]',
    ]
    for ln in lines:
        pdf.set_xy(ML + 5, pdf.get_y())
        if not ln:
            pdf.ln(3)
        else:
            pdf.multi_cell(CW - 10, 5.5, ln,
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def page_closing(pdf):
    pdf.add_page()
    pdf.fc(BG); pdf.rect(0, 0, W, H, style='F')
    pdf.fc(ACCENT); pdf.rect(0, 0, W, 10, style='F')

    pdf.sp(10)
    pdf.set_font('JP-B', size=18)
    pdf.tc(PRIMARY)
    pdf.multi_cell(CW, 10, 'おわりに',
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.dc(ACCENT); pdf.set_line_width(0.6)
    pdf.line(ML, pdf.get_y(), ML + 28, pdf.get_y())
    pdf.sp(8)

    closing = (
        'このワークブックをやり終えた時点で、あなたはもう「AIを使いこなせない人」ではありません。\n\n'
        'AIに自分のことを教えられる人は、AIから「自分らしい文章」を引き出せます。\n\n'
        'ぜひ、今日から一度試してみてください。\n'
        '「なんか違う」から「これ、私っぽい」に変わる瞬間が必ずあります。'
    )
    pdf.text_block(closing, size=11, line_h=7.5)

    pdf.sp(12)
    pdf.set_font('JP', size=10)
    pdf.tc(TEXT_L)
    pdf.multi_cell(CW, 7, '内藤いさお\nnaitostyle.com',
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.fc(ACCENT)
    pdf.rect(0, H - 9, W, 9, style='F')


# ═══════════════════════════════════════════
# フッター（2ページ目以降）
# ═══════════════════════════════════════════

class WorkbookPDF(PDF):
    def footer(self):
        if self.page_no() > 1:
            self.set_y(-14)
            self.set_font('JP', size=7.5)
            self.tc(TEXT_L)
            self.cell(0, 5,
                f'自分らしい発信をAIと作るワークブック  ©内藤いさお  |  {self.page_no()}',
                align='C')


# ═══════════════════════════════════════════
# メイン
# ═══════════════════════════════════════════

def build():
    pdf = WorkbookPDF()
    page_cover(pdf)
    page_intro(pdf)
    page_step1(pdf)
    page_step2(pdf)
    page_step3(pdf)
    page_closing(pdf)
    pdf.output(OUTPUT)
    print(f'✅ 完了: {OUTPUT}')


if __name__ == '__main__':
    build()
