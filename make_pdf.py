"""
AIプロンプト帳 PDF ジェネレーター
女性起業家のための厳選30選
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.flowables import Flowable
import os

# ===== フォント登録 =====
FONT_PATH = '/tmp/NotoSansJP.ttf'
pdfmetrics.registerFont(TTFont('NotoSansJP', FONT_PATH))

# ===== カラー定義 =====
C_BG        = colors.HexColor('#F7F4F0')
C_DARK      = colors.HexColor('#2E3D45')
C_ACCENT    = colors.HexColor('#C87941')
C_ACCENT_L  = colors.HexColor('#EDD5BE')
C_TEXT      = colors.HexColor('#3A3530')
C_TEXT_L    = colors.HexColor('#7A6F66')
C_WHITE     = colors.white
C_CARD_BG   = colors.HexColor('#FDFBF9')
C_PROMPT_BG = colors.HexColor('#F0EBE5')
C_CAT1      = colors.HexColor('#5B8FA8')  # SNS: 青
C_CAT2      = colors.HexColor('#7A9E7E')  # メルマガ: 緑
C_CAT3      = colors.HexColor('#C87941')  # お客様: オレンジ
C_CAT4      = colors.HexColor('#9B7EC8')  # プロフィール: 紫
C_CAT5      = colors.HexColor('#C87878')  # 講座: ピンク
C_CAT6      = colors.HexColor('#7A9E9A')  # 日常: ティール

# ===== スタイル定義 =====
def make_styles():
    styles = {}

    styles['cover_title'] = ParagraphStyle(
        'cover_title',
        fontName='NotoSansJP',
        fontSize=32,
        textColor=C_WHITE,
        alignment=TA_CENTER,
        leading=48,
        spaceAfter=8*mm,
    )
    styles['cover_sub'] = ParagraphStyle(
        'cover_sub',
        fontName='NotoSansJP',
        fontSize=14,
        textColor=colors.HexColor('#EDD5BE'),
        alignment=TA_CENTER,
        leading=22,
        spaceAfter=4*mm,
    )
    styles['cover_body'] = ParagraphStyle(
        'cover_body',
        fontName='NotoSansJP',
        fontSize=11,
        textColor=colors.HexColor('#D0C8BE'),
        alignment=TA_CENTER,
        leading=18,
    )
    styles['section_header'] = ParagraphStyle(
        'section_header',
        fontName='NotoSansJP',
        fontSize=16,
        textColor=C_WHITE,
        alignment=TA_LEFT,
        leading=24,
    )
    styles['prompt_num'] = ParagraphStyle(
        'prompt_num',
        fontName='NotoSansJP',
        fontSize=11,
        textColor=C_ACCENT,
        alignment=TA_LEFT,
        leading=16,
        spaceAfter=1*mm,
    )
    styles['prompt_title'] = ParagraphStyle(
        'prompt_title',
        fontName='NotoSansJP',
        fontSize=13,
        textColor=C_TEXT,
        alignment=TA_LEFT,
        leading=20,
        spaceAfter=2*mm,
    )
    styles['prompt_scene'] = ParagraphStyle(
        'prompt_scene',
        fontName='NotoSansJP',
        fontSize=9,
        textColor=C_TEXT_L,
        alignment=TA_LEFT,
        leading=14,
        spaceAfter=2*mm,
    )
    styles['prompt_text'] = ParagraphStyle(
        'prompt_text',
        fontName='NotoSansJP',
        fontSize=9,
        textColor=C_TEXT,
        alignment=TA_LEFT,
        leading=15,
    )
    styles['prompt_tip'] = ParagraphStyle(
        'prompt_tip',
        fontName='NotoSansJP',
        fontSize=8,
        textColor=C_ACCENT,
        alignment=TA_LEFT,
        leading=13,
        spaceAfter=0,
    )
    styles['intro_title'] = ParagraphStyle(
        'intro_title',
        fontName='NotoSansJP',
        fontSize=18,
        textColor=C_DARK,
        alignment=TA_LEFT,
        leading=28,
        spaceAfter=4*mm,
    )
    styles['intro_body'] = ParagraphStyle(
        'intro_body',
        fontName='NotoSansJP',
        fontSize=10,
        textColor=C_TEXT,
        alignment=TA_LEFT,
        leading=18,
        spaceAfter=2*mm,
    )
    styles['intro_step'] = ParagraphStyle(
        'intro_step',
        fontName='NotoSansJP',
        fontSize=10,
        textColor=C_TEXT,
        alignment=TA_LEFT,
        leading=18,
        leftIndent=4*mm,
        spaceAfter=1.5*mm,
    )
    styles['footer_text'] = ParagraphStyle(
        'footer_text',
        fontName='NotoSansJP',
        fontSize=8,
        textColor=C_TEXT_L,
        alignment=TA_CENTER,
        leading=12,
    )
    return styles


# ===== プロンプトデータ =====
CATEGORIES = [
    {
        'id': 1,
        'name': 'SNS・発信',
        'emoji': '📱',
        'color': C_CAT1,
        'desc': 'Threads・Instagramなどの投稿文を簡単に作成',
    },
    {
        'id': 2,
        'name': 'メルマガ・ブログ',
        'emoji': '✉️',
        'color': C_CAT2,
        'desc': 'メルマガやブログ記事の文章を丁寧に仕上げる',
    },
    {
        'id': 3,
        'name': 'お客様対応',
        'emoji': '💌',
        'color': C_CAT3,
        'desc': 'メールや返信文を誠実で温かみのある表現で',
    },
    {
        'id': 4,
        'name': 'プロフィール・自己紹介',
        'emoji': '✨',
        'color': C_CAT4,
        'desc': '肩書きやプロフィール文を魅力的に表現',
    },
    {
        'id': 5,
        'name': '講座・セミナー',
        'emoji': '🎓',
        'color': C_CAT5,
        'desc': '告知文や案内メールをプロらしく作成',
    },
    {
        'id': 6,
        'name': '日常業務',
        'emoji': '📋',
        'color': C_CAT6,
        'desc': '議事録・提案書など日々の業務を効率化',
    },
]

PROMPTS = [
    # ===== SNS・発信 =====
    {
        'cat': 1, 'no': 1,
        'title': 'Threads投稿文（体験談から作る）',
        'scene': '自分の体験や気づきをThreadsに投稿したいとき',
        'prompt': '''以下の体験をThreads投稿文に変換してください。

【私の体験・気づき】
（ここに体験を書いてください）

【ルール】
・200〜300字以内
・「あるある」と共感される書き出しで始める
・最後は読者への問いかけで終わる
・親しみやすい口語体で書く
・改行を多めにして読みやすくする''',
        'tip': '💡 体験は箇条書きでもOK。AIが文章に整えてくれます',
    },
    {
        'cat': 1, 'no': 2,
        'title': 'お客様の変化を伝える投稿',
        'scene': 'セッションや講座を受けたお客様の変化をシェアしたいとき',
        'prompt': '''以下のお客様の変化をSNS投稿文にしてください。

【変化の前】
（受ける前の状態を書いてください）

【変化の後】
（受けた後の変化を書いてください）

【ルール】
・個人が特定されないよう「あるクライアント様」と表現
・感動・共感が生まれる構成にする
・300字以内
・ハッシュタグを3つ提案してください''',
        'tip': '💡 お客様に掲載許可を取ってから投稿しましょう',
    },
    {
        'cat': 1, 'no': 3,
        'title': 'セミナー・講座の告知投稿',
        'scene': 'イベントや講座の参加者を募集したいとき',
        'prompt': '''以下の情報を元にSNS告知投稿文を作成してください。

【講座名】
【日時】
【内容（箇条書きOK）】
【こんな人に向いている】
【参加費】
【申込方法】

【ルール】
・「こんなお悩みありませんか？」から始める
・読者が「私のことだ」と感じる言葉を入れる
・申込への背中を押す一言で締める
・400字以内''',
        'tip': '💡 「こんな人に向いている」を具体的に書くほど反応が上がります',
    },
    {
        'cat': 1, 'no': 4,
        'title': '「今日の気づき」日常投稿',
        'scene': '日常の小さな気づきを投稿ネタにしたいとき',
        'prompt': '''以下のメモをSNS投稿文に仕上げてください。

【今日の気づきメモ】
（思ったことをそのまま書いてください）

【私のビジネスのテーマ】
（例：女性の自己表現、起業サポートなど）

【ルール】
・日常の話からビジネスの本質につなげる
・「だから私は〇〇と思う」という自分の意見を入れる
・200字以内でサクッと読める長さに
・堅苦しくならないよう会話口調で''',
        'tip': '💡 毎日のメモが投稿ネタになります。まずメモを習慣に',
    },
    {
        'cat': 1, 'no': 5,
        'title': 'フォロワーへの問いかけ投稿',
        'scene': 'コメントやリプライをもらいやすい投稿を作りたいとき',
        'prompt': '''以下のテーマで「問いかけ型」のSNS投稿文を作ってください。

【テーマ】
（例：自己紹介、仕事の悩み、好きなものなど）

【私のビジネスジャンル】

【ルール】
・投稿の最後に答えやすい質問を1つだけ入れる
・「〇〇ですか？コメントで教えてください！」形式
・読者が答えたくなる身近なテーマにする
・200字以内''',
        'tip': '💡 質問は「YES/NOで答えられる」ものが反応しやすいです',
    },
    {
        'cat': 1, 'no': 6,
        'title': '自分の強みを伝える投稿',
        'scene': '自分の専門性や強みをさりげなく発信したいとき',
        'prompt': '''以下の情報を元に、自己PRにならない「強みを伝える投稿文」を作ってください。

【私が得意なこと・専門分野】

【それを活かしてお客様に起きた変化の例】

【ルール】
・「私はすごい」ではなく「こんなことで役に立てます」のトーンで
・具体的なエピソードを1つ入れる
・読んだ人が「相談してみたい」と思える締めにする
・300字以内''',
        'tip': '💡 実績より「どんな変化が起きたか」に焦点を当てましょう',
    },
    {
        'cat': 1, 'no': 7,
        'title': 'Instagram投稿キャプション',
        'scene': '写真に合わせたInstagramのキャプションを作りたいとき',
        'prompt': '''以下の情報でInstagramのキャプションを作ってください。

【投稿する写真の内容】
（例：カフェで作業中、セミナー後、自宅の様子など）

【この投稿で伝えたいこと】

【ルール】
・最初の1〜2行で続きを読みたくなる書き出しを作る
・自分の日常がリアルに伝わる表現にする
・ハッシュタグを5〜8個提案する
・全体で400字以内''',
        'tip': '💡 最初の2行が命。「もっと読みたい」と思わせる言葉を選びましょう',
    },
    {
        'cat': 1, 'no': 8,
        'title': 'お知らせ・リマインド投稿',
        'scene': 'イベント前日や締切前にリマインドを投稿したいとき',
        'prompt': '''以下の情報でリマインド投稿文を作ってください。

【お知らせの内容】

【締切・当日まであと何日か】

【まだ迷っている人へのメッセージ】

【ルール】
・緊急感を出しつつ、プレッシャーを与えすぎない
・「迷っているなら〇〇してみてください」という優しい背中押しを入れる
・200字以内でスッキリまとめる''',
        'tip': '💡 「残り〇席」「明日まで」など数字を入れると反応が上がります',
    },

    # ===== メルマガ・ブログ =====
    {
        'cat': 2, 'no': 9,
        'title': 'メルマガの書き出し文',
        'scene': 'メルマガを書き始める際、つかみの一文に迷ったとき',
        'prompt': '''以下のテーマで「読みたくなるメルマガの書き出し」を3パターン作ってください。

【今日のメルマガのテーマ】

【ルール】
・パターン1：共感から入る（「〜って思ったことありませんか？」）
・パターン2：質問から入る（「突然ですが、〇〇できていますか？」）
・パターン3：エピソードから入る（最近の出来事を入口に）
・各パターン3〜4行で書く
・読んで「続きを読みたい」と思わせる内容に''',
        'tip': '💡 3パターンから1つ選んで、続きを自分で書きましょう',
    },
    {
        'cat': 2, 'no': 10,
        'title': 'ブログ記事の構成案',
        'scene': 'ブログ記事を書く前に構成を考えたいとき',
        'prompt': '''以下のテーマでブログ記事の構成案を作ってください。

【記事のテーマ・タイトル案】

【想定読者】
（例：起業2年目の女性、副業を考えている会社員など）

【この記事で読者に気づいてほしいこと】

【ルール】
・タイトル案を3つ提案する（検索されやすいものを含める）
・見出し（h2）を4〜5個作る
・各見出しに100字程度の説明メモをつける
・最後にCTA（行動を促す一言）の案も提案する''',
        'tip': '💡 構成が決まれば、あとは各見出しを埋めるだけ。一気に書けます',
    },
    {
        'cat': 2, 'no': 11,
        'title': 'メルマガのまとめ・締め文',
        'scene': 'メルマガの締めくくりの言葉に迷ったとき',
        'prompt': '''以下の情報で「メルマガの締め文」を作ってください。

【今日のメルマガで伝えた内容（要点）】

【読者にとってほしい行動（あれば）】
（例：返信してほしい、LINEを見てほしい、申し込んでほしいなど）

【ルール】
・今日のまとめを1〜2行でスッキリまとめる
・温かみのある言葉で締める
・押し売り感のないCTAを自然に入れる
・全体で150字以内''',
        'tip': '💡 「今日も読んでくださってありがとうございます」の一言は必ず入れましょう',
    },
    {
        'cat': 2, 'no': 12,
        'title': '読まれるタイトル案を複数提案',
        'scene': 'メルマガやブログのタイトルを考えたいとき',
        'prompt': '''以下の内容の記事・メルマガのタイトルを10個提案してください。

【内容の要点】

【ターゲット読者】

【ルール】
・「数字入り」「疑問形」「ベネフィット型」「共感型」を各2〜3個含める
・読者が「自分ごと」と感じる言葉を使う
・25字以内を基本に（スマホで途切れない長さ）
・10個のうち、特におすすめの3つに★をつける''',
        'tip': '💡 タイトルで開封率が変わります。「自分ならこれを読みたい」で選びましょう',
    },
    {
        'cat': 2, 'no': 13,
        'title': '長い文章をわかりやすく要約',
        'scene': '書いた文章が長くなりすぎて整理したいとき',
        'prompt': '''以下の文章をわかりやすく整理してください。

【元の文章】
（ここに文章を貼り付けてください）

【ルール】
・伝えたいことを3つの要点に絞る
・各要点を「見出し＋2〜3行の説明」でまとめる
・難しい言葉は使わず、誰でもわかる表現に
・元の文章の「温かみ・口調」は保ったままにする''',
        'tip': '💡 「長すぎて読まれない」より「短くて伝わる」を目指しましょう',
    },
    {
        'cat': 2, 'no': 14,
        'title': 'メルマガ読者へのお礼・ご挨拶文',
        'scene': '読者へ感謝や近況をお伝えするメルマガを書きたいとき',
        'prompt': '''読者への感謝・近況報告のメルマガ文を作ってください。

【伝えたい近況・エピソード】

【読者への感謝の気持ち（自分の言葉で）】

【ルール】
・「いつもありがとうございます」から入らない（ありきたりなので）
・エピソードを通じて人柄が伝わる文章に
・読んだ人が「この人を応援したい」と思えるような温かさを出す
・400字以内''',
        'tip': '💡 近況メルマガは「売り込みゼロ」でOK。信頼関係が深まります',
    },

    # ===== お客様対応 =====
    {
        'cat': 3, 'no': 15,
        'title': 'お問い合わせへの返信メール',
        'scene': 'サービスへの問い合わせに丁寧に返信したいとき',
        'prompt': '''以下の情報でお問い合わせへの返信メールを作成してください。

【お問い合わせ内容（要点）】

【お伝えしたいこと】

【次のステップ（あれば）】
（例：無料相談の案内、資料送付など）

【ルール】
・受け取った喜びと感謝を最初に伝える
・質問にわかりやすく答える
・押しつけがましくなく、でも次のステップへ自然に誘導
・200〜300字以内''',
        'tip': '💡 返信は24時間以内が理想。テンプレを用意しておくと楽です',
    },
    {
        'cat': 3, 'no': 16,
        'title': 'セッション後のお礼メール',
        'scene': 'コンサルやセッション後にお礼を送りたいとき',
        'prompt': '''セッション後のお礼メールを作成してください。

【セッションで話したこと（要点）】

【お客様の変化・気づき（感じたこと）】

【次回への一言（あれば）】

【ルール】
・お客様の名前を冒頭に（○○さん）
・「今日お話しした〇〇について」と具体的に触れる
・温かく、でも簡潔に（長すぎない）
・200字以内''',
        'tip': '💡 具体的な内容に触れることで「ちゃんと聞いてもらえた」と感じてもらえます',
    },
    {
        'cat': 3, 'no': 17,
        'title': '講座申込者への受付完了メール',
        'scene': '講座・セミナーの申し込みを受けたときの案内メール',
        'prompt': '''講座申込者への受付完了メールを作成してください。

【講座名・日時】

【当日の持ち物・準備事項】

【申込者へのメッセージ（自分の言葉で）】

【ルール】
・申し込みへの感謝と「一緒に学べること」への期待を伝える
・当日の案内はわかりやすく箇条書きに
・「楽しみにしています」という温かいひと言で締める
・全体で300字以内''',
        'tip': '💡 受付メールの印象が、当日への期待感を左右します',
    },
    {
        'cat': 3, 'no': 18,
        'title': 'お断りメール（丁寧・誠実に）',
        'scene': 'ご要望に応えられない場合や日程が合わない場合の返信',
        'prompt': '''丁寧なお断りメールを作成してください。

【お断りする理由（正直に）】

【代わりに提案できること（あれば）】

【ルール】
・相手の気持ちを受け止める一言を最初に入れる
・「お断り」という言葉を使わず、自然に伝える
・代替案があれば提案する
・関係が続くように、温かく締める
・200字以内''',
        'tip': '💡 断り方次第で関係は続きます。「また機会があれば」の一言を忘れずに',
    },
    {
        'cat': 3, 'no': 19,
        'title': 'フォローアップメール',
        'scene': '体験セッションや相談後に、その後の状況を確認したいとき',
        'prompt': '''フォローアップメールを作成してください。

【前回の接点（体験セッション・相談など）】

【確認したいこと・伝えたいこと】

【ルール】
・「いかがですか？」だけにならない具体的な一言を入れる
・前回の話題に触れて「覚えていますよ」と伝える
・次のステップへの案内は控えめに、押しつけにならないように
・150字以内''',
        'tip': '💡 1〜2週間後のフォローメールは申込率を大きく上げます',
    },

    # ===== プロフィール・自己紹介 =====
    {
        'cat': 4, 'no': 20,
        'title': 'SNSプロフィール文',
        'scene': 'Instagram・ThreadsのプロフィールのBio欄を整えたいとき',
        'prompt': '''以下の情報でSNSプロフィール文を3パターン作ってください。

【私について（経歴・強み・好きなこと）】

【フォロワーにとってほしい行動】
（例：サイトを見てほしい、LINEに来てほしいなど）

【ルール】
・パターン1：実績・専門性を前面に（信頼感重視）
・パターン2：人柄・ストーリーを前面に（親近感重視）
・パターン3：読者のベネフィットを前面に（有益性重視）
・各パターン100字以内（Instagram Bio文字数制限内）''',
        'tip': '💡 「私が何者か」より「フォローするとどんな得があるか」が大切です',
    },
    {
        'cat': 4, 'no': 21,
        'title': 'セミナー登壇者の紹介文',
        'scene': 'セミナーや勉強会で自己紹介文を求められたとき',
        'prompt': '''セミナー登壇者として使える自己紹介文を作ってください。

【私の経歴・資格・実績】

【今日のセミナーテーマとの関連】

【参加者に伝えたいこと・メッセージ】

【ルール】
・300〜400字の長め版と、100字の短め版の2パターン
・「なぜこのテーマに取り組んでいるか」の動機を入れる
・権威を示しつつも親しみやすいトーンで
・主催者がアナウンスしやすい文体にする''',
        'tip': '💡 主催者が読み上げやすいよう「〇〇さんをご紹介します」の後に続く文体で',
    },
    {
        'cat': 4, 'no': 22,
        'title': '肩書き・キャッチコピー案',
        'scene': '自分のビジネスを一言で表す肩書きに迷ったとき',
        'prompt': '''私のビジネスの肩書き・キャッチコピーを10個提案してください。

【私が提供していること】

【お客様が得られる変化・結果】

【ターゲット（どんな人向けか）】

【ルール】
・「〇〇コーチ」「〇〇コンサルタント」のような職種系も含める
・「〇〇が〇〇になる」という変化を表すものも含める
・ユニークで記憶に残るものも1〜2個入れる
・各20字以内
・10個のうちおすすめ3つに★をつける''',
        'tip': '💡 肩書きは「自分が何者か」より「相手がどうなれるか」で選ぶと刺さります',
    },
    {
        'cat': 4, 'no': 23,
        'title': 'ホームページ「私について」文',
        'scene': 'ホームページのAboutページを充実させたいとき',
        'prompt': '''ホームページの「私について」ページの文章を作成してください。

【私のストーリー（過去の悩み・転機・現在）】

【今提供しているサービス】

【大切にしている価値観・想い】

【理想のお客様像】

【ルール】
・過去の自分の悩みから始める（読者が「この人は私のことをわかってくれる」と感じるように）
・現在に至るまでのストーリーを感情を込めて
・「だからこそ今、〇〇を提供しています」という流れで締める
・全体で600〜800字
・読んだ人が「会いたい」「相談したい」と感じる文章に''',
        'tip': '💡 完璧な実績より「等身大のストーリー」のほうが共感を生みます',
    },

    # ===== 講座・セミナー =====
    {
        'cat': 5, 'no': 24,
        'title': '講座・サービスの概要文',
        'scene': 'サービスページや資料に載せる概要文を作りたいとき',
        'prompt': '''私のサービス・講座の概要文を作成してください。

【サービス名】

【こんな悩みを持つ人向け（3つ）】

【サービスの内容（箇条書きOK）】

【受けると得られる変化・結果】

【ルール】
・「こんなお悩みはありませんか？」から始める
・受講後のビフォーアフターが明確に伝わる構成
・「なぜ私がこれを提供するのか」の想いを1段落入れる
・全体で500字以内
・読んだ人が「私のためのサービスだ」と感じる表現を使う''',
        'tip': '💡 「何をするか」より「どうなれるか」を前面に出しましょう',
    },
    {
        'cat': 5, 'no': 25,
        'title': '受講後アンケートの設問案',
        'scene': '講座・セミナー後にアンケートを取りたいとき',
        'prompt': '''講座・セミナー後のアンケート設問を作ってください。

【講座・セミナーのテーマ】

【アンケートで知りたいこと】
（例：満足度、改善点、次回受けたい内容など）

【ルール】
・設問数は5〜7問（答えやすい量に）
・選択式と自由記述を混ぜる
・最後に「次回受けたいテーマ」を聞く設問を入れる
・回答者への感謝の一言を最初と最後に入れる
・答えるのが楽しくなるような言葉遣いで''',
        'tip': '💡 アンケートは次のコンテンツ作りの最高のヒントになります',
    },
    {
        'cat': 5, 'no': 26,
        'title': 'セミナー前日リマインドメール',
        'scene': '参加者に前日リマインドメールを送りたいとき',
        'prompt': '''セミナー前日のリマインドメールを作成してください。

【セミナー名・日時・場所（またはURL）】

【持ち物・事前準備（あれば）】

【参加者へのメッセージ】

【ルール】
・「明日お会いできることを楽しみにしています」という期待感を伝える
・当日の情報は箇条書きでわかりやすく
・「何か不明点があればいつでもご連絡ください」を入れる
・200字以内でスッキリまとめる''',
        'tip': '💡 前日メールは参加率を上げます。温かい一言で当日が楽しみになる内容に',
    },
    {
        'cat': 5, 'no': 27,
        'title': 'セミナー後のフォローメール',
        'scene': 'セミナー・講座終了後に参加者へお礼を送りたいとき',
        'prompt': '''セミナー・講座後のフォローメールを作成してください。

【セミナー名・実施日】

【今日伝えた内容の要点（3つ）】

【次のステップ（案内したいこと）】

【ルール】
・参加への感謝と「一緒に過ごせた喜び」を伝える
・今日の要点を3点でサッとおさらいする
・「次は〇〇があります」と次回への案内を自然に入れる
・返信しやすい一言（「今日の感想を教えてください」など）で締める
・300字以内''',
        'tip': '💡 「感想を教えてください」の一言がお客様の声収集につながります',
    },

    # ===== 日常業務 =====
    {
        'cat': 6, 'no': 28,
        'title': '会議・打ち合わせの議事録',
        'scene': '打ち合わせの内容をまとめて共有したいとき',
        'prompt': '''以下のメモから議事録を作成してください。

【打ち合わせメモ（箇条書きOK）】
（話し合った内容を思い出して書いてください）

【参加者】

【ルール】
・「決定事項」「確認事項」「次回までのタスク（担当者・期限）」の3つに整理
・5W1Hを意識した明確な表現で
・誰が読んでもわかるよう専門用語は解説を入れる
・最後に「次回の打ち合わせ日程（未定の場合はその旨）」を入れる''',
        'tip': '💡 打ち合わせ直後にメモを貼り付けるだけで議事録が完成します',
    },
    {
        'cat': 6, 'no': 29,
        'title': '提案書・企画書の骨格',
        'scene': 'クライアントへの提案書や企画書の構成を作りたいとき',
        'prompt': '''以下の情報で提案書の骨格を作成してください。

【提案先（どんな方・企業か）】

【提案内容・解決したい課題】

【私が提供できること（強み・実績）】

【ルール】
・構成：①現状の課題 → ②解決策の提案 → ③期待できる効果 → ④具体的な進め方 → ⑤費用・期間
・各項目に100字程度の説明と「ここで書く内容のヒント」をつける
・読んだ人が「この提案は自分たちのためのものだ」と感じる構成に
・専門用語は避け、わかりやすい言葉で''',
        'tip': '💡 骨格が決まれば肉付けは簡単。まず構成から作りましょう',
    },
    {
        'cat': 6, 'no': 30,
        'title': '年間スケジュール・活動計画案',
        'scene': '来年の活動計画やコンテンツカレンダーを考えたいとき',
        'prompt': '''私のビジネスの年間スケジュール案を作成してください。

【私のビジネスの種類・メインサービス】

【今年やったこと（うまくいったこと・課題）】

【来年やりたいこと・目標】

【ルール】
・12ヶ月分の「メインテーマ・重点活動」を表形式で提案
・繁忙期・閑散期を考慮した無理のないスケジュールに
・「新規集客」「既存深化」「コンテンツ作成」「振り返り」のバランスを取る
・実行可能な現実的な計画を立てる''',
        'tip': '💡 年始ではなく年末に来年の計画を立てると動き出しがスムーズです',
    },
]


# ===== PDF生成 =====
def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
    )
    W, H = A4
    styles = make_styles()
    story = []

    # ========== 表紙（キャンバスで描画するので空ページ） ==========
    story += make_cover_story(styles, W, H)
    story.append(PageBreak())

    # ========== 使い方ページ ==========
    story += make_intro_page(styles)
    story.append(PageBreak())

    # ========== 各プロンプト ==========
    current_cat = None
    for prompt in PROMPTS:
        cat_id = prompt['cat']
        cat = next(c for c in CATEGORIES if c['id'] == cat_id)

        # カテゴリ区切り
        if cat_id != current_cat:
            if current_cat is not None:
                story.append(PageBreak())
            story.append(make_category_header(cat, styles, W))
            story.append(Spacer(1, 4*mm))
            current_cat = cat_id

        # プロンプトカード
        story.append(make_prompt_card(prompt, cat, styles, W))
        story.append(Spacer(1, 3*mm))

    doc.build(story, onFirstPage=draw_cover_bg, onLaterPages=add_footer)
    print(f'PDF作成完了: {output_path}')


def draw_cover_bg(canvas, doc):
    """表紙：シンプル白ベースデザイン"""
    canvas.saveState()
    W, H = A4
    M = 18 * mm   # マージン

    # 白背景
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)

    # 外枠（細いアクセントカラー）
    canvas.setStrokeColor(C_ACCENT)
    canvas.setLineWidth(1.2)
    canvas.rect(M, M, W - 2*M, H - 2*M, fill=0, stroke=1)

    # 上部アクセントバー（細め）
    canvas.setFillColor(C_ACCENT)
    canvas.rect(M, H - M - 6*mm, W - 2*M, 6*mm, fill=1, stroke=0)

    # タグ：「女性起業家のための」
    canvas.setFont('NotoSansJP', 10)
    canvas.setFillColor(colors.white)
    canvas.drawCentredString(W / 2, H - M - 4*mm, '女性起業家のための')

    # メインタイトル
    canvas.setFont('NotoSansJP', 42)
    canvas.setFillColor(C_TEXT)
    canvas.drawCentredString(W / 2, H * 0.68, 'AI')

    canvas.setFont('NotoSansJP', 34)
    canvas.drawCentredString(W / 2, H * 0.61, 'プロンプト帳')

    # サブタイトル区切り
    canvas.setStrokeColor(C_ACCENT_L)
    canvas.setLineWidth(1)
    canvas.line(W * 0.3, H * 0.575, W * 0.7, H * 0.575)

    # 「厳選30選」バッジ風
    badge_cx = W / 2
    badge_cy = H * 0.52
    canvas.setFillColor(C_ACCENT_L)
    canvas.roundRect(badge_cx - 28*mm, badge_cy - 5*mm,
                     56*mm, 11*mm, 5*mm, fill=1, stroke=0)
    canvas.setFont('NotoSansJP', 11)
    canvas.setFillColor(C_ACCENT)
    canvas.drawCentredString(badge_cx, badge_cy - 1*mm, '厳 選  30 選')

    # 説明文
    canvas.setFont('NotoSansJP', 9.5)
    canvas.setFillColor(C_TEXT_L)
    canvas.drawCentredString(W / 2, H * 0.46,
        'ChatGPT・Claude・Gemini で今すぐ使える')
    canvas.drawCentredString(W / 2, H * 0.44,
        'コピーして貼るだけ。AI が文章を仕上げてくれます。')

    # カテゴリ一覧（左寄せ・枠内）
    cat_x = W * 0.25
    y = H * 0.385
    canvas.setFont('NotoSansJP', 9.5)
    for cat in CATEGORIES:
        # ドット
        canvas.setFillColor(cat['color'])
        canvas.circle(cat_x - 6*mm, y + 2.5*mm, 2*mm, fill=1, stroke=0)
        # テキスト
        canvas.setFillColor(C_TEXT)
        canvas.drawString(cat_x - 2*mm, y, f'{cat["emoji"]}  {cat["name"]}')
        y -= 6*mm

    # 下部アクセントバー
    canvas.setFillColor(colors.HexColor('#F0EBE5'))
    canvas.rect(M, M, W - 2*M, 18*mm, fill=1, stroke=0)

    # 著者名
    canvas.setFont('NotoSansJP', 10)
    canvas.setFillColor(C_TEXT_L)
    canvas.drawCentredString(W / 2, M + 6*mm, '内藤いさお')

    canvas.restoreState()


def make_cover_story(styles, W, H):
    """表紙ページ用のストーリー（背景はキャンバスで描画済みなので空白のみ）"""
    return [Spacer(1, 1*mm)]


def make_intro_page(styles):
    """使い方ページ"""
    items = []
    items.append(Paragraph('📖  このプロンプト帳の使い方', styles['intro_title']))
    items.append(HRFlowable(width='100%', thickness=1, color=C_ACCENT_L, spaceAfter=4*mm))

    items.append(Paragraph(
        'このプロンプト帳は、ChatGPT・Claude・Gemini などの AI ツールに貼り付けるだけで、'
        '文章をプロらしく仕上げてくれる「呪文集」です。',
        styles['intro_body']
    ))
    items.append(Spacer(1, 4*mm))

    steps = [
        ('STEP 1', '使いたいプロンプトを選ぶ', '場面に合ったプロンプトを見つけてください。'),
        ('STEP 2', 'プロンプトをコピーする', 'グレーのボックス内の文章をまるごとコピー。'),
        ('STEP 3', 'AIに貼り付ける', 'ChatGPT・Claude・Gemini のチャット欄に貼り付けます。'),
        ('STEP 4', '（　）の部分を入力する', '「（ここに〇〇を書いてください）」の箇所を自分の情報に書き換えてEnter。'),
        ('STEP 5', '出力を確認・微調整する', '「もっと短く」「もっと柔らかいトーンで」と追加指示すると精度が上がります。'),
    ]

    for step, title, desc in steps:
        row = Table(
            [[
                Paragraph(f'<font color="#C87941"><b>{step}</b></font>', styles['intro_body']),
                Paragraph(f'<b>{title}</b><br/>{desc}', styles['intro_body']),
            ]],
            colWidths=[22*mm, None],
        )
        row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 1*mm),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1*mm),
        ]))
        items.append(row)
        items.append(Spacer(1, 1*mm))

    items.append(Spacer(1, 6*mm))

    # ポイントボックス
    point_content = [
        Paragraph('<b>💡  うまく使うコツ</b>', styles['intro_body']),
        Spacer(1, 2*mm),
        Paragraph('・出力が自分っぽくないと感じたら「もっと〇〇な感じで」と追加で伝えてみてください', styles['intro_body']),
        Paragraph('・最初から完璧を求めず、3〜5回やり取りして仕上げるのがコツです', styles['intro_body']),
        Paragraph('・よく使うプロンプトはAIの「カスタム指示」や「メモリ」に保存すると便利です', styles['intro_body']),
    ]
    point_table = Table([[point_content]], colWidths=['100%'])
    point_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_ACCENT_L),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING', (0,0), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 5*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 5*mm),
    ]))
    items.append(point_table)
    return items


def make_category_header(cat, styles, W):
    """カテゴリヘッダー"""
    header_text = Paragraph(
        f'{cat["emoji"]}  {cat["name"]}　　{cat["desc"]}',
        styles['section_header']
    )
    table = Table([[header_text]], colWidths=[W - 30*mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), cat['color']),
        ('TOPPADDING', (0,0), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 6*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 6*mm),
        ('ROUNDEDCORNERS', [6]),
    ]))
    return table


def make_prompt_card(prompt, cat, styles, W):
    """プロンプトカード"""
    card_w = W - 30*mm

    # ヘッダー行（番号 + タイトル）
    num_para = Paragraph(f'No.{prompt["no"]:02d}', styles['prompt_num'])
    title_para = Paragraph(prompt['title'], styles['prompt_title'])
    scene_para = Paragraph(f'📌 {prompt["scene"]}', styles['prompt_scene'])

    # プロンプト本文
    prompt_text = prompt['prompt'].replace('\n', '<br/>')
    prompt_para = Paragraph(prompt_text, styles['prompt_text'])
    prompt_box = Table([[prompt_para]], colWidths=[card_w - 14*mm])
    prompt_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_PROMPT_BG),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 4*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 4*mm),
        ('ROUNDEDCORNERS', [4]),
    ]))

    # ヒント
    tip_para = Paragraph(prompt['tip'], styles['prompt_tip'])

    # カード全体
    inner = [
        [num_para],
        [title_para],
        [scene_para],
        [Spacer(1, 1*mm)],
        [prompt_box],
        [Spacer(1, 1.5*mm)],
        [tip_para],
    ]
    inner_table = Table(inner, colWidths=[card_w - 10*mm])
    inner_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0.5*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5*mm),
    ]))

    # 左のカラーバー付きカード
    card = Table(
        [[
            Table([['']], colWidths=[2*mm], rowHeights=[None]),
            inner_table,
        ]],
        colWidths=[2*mm, card_w - 4*mm],
    )
    card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), cat['color']),
        ('BACKGROUND', (1,0), (1,-1), C_CARD_BG),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
        ('LEFTPADDING', (1,0), (1,-1), 4*mm),
        ('RIGHTPADDING', (1,0), (1,-1), 4*mm),
        ('LEFTPADDING', (0,0), (0,-1), 0),
        ('RIGHTPADDING', (0,0), (0,-1), 0),
        ('ROUNDEDCORNERS', [4]),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E2D9D0')),
    ]))
    return KeepTogether(card)


def add_footer(canvas, doc):
    """フッター"""
    canvas.saveState()
    canvas.setFont('NotoSansJP', 8)
    canvas.setFillColor(C_TEXT_L)
    page_num = canvas.getPageNumber()
    if page_num > 1:
        canvas.drawCentredString(A4[0] / 2, 8*mm, f'AIプロンプト帳 厳選30選  ©内藤いさお  |  {page_num}')
    canvas.restoreState()


# ===== 実行 =====
if __name__ == '__main__':
    output = '/Users/naitoisao/ClaudeCode/tokuten/AI_prompt_book.pdf'
    build_pdf(output)
