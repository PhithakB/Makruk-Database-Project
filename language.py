import json, io, os, tempfile
from PyQt5.QtWidgets import QDialog, QPushButton, QGridLayout
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon

class LanguageDialog(QDialog):
    change_lang_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setFixedSize(950, 300)
        self.setWindowTitle("Language")
        self.setWindowIcon(QIcon("images/util/language.png"))
        self.temp_dir = tempfile.gettempdir()
        self.temp_dir = self.temp_dir + '\mkdb'
        try:
            os.makedirs(self.temp_dir)
        except:
            pass
        try:
            with open(self.temp_dir+'\mkdb_language.tmp', "r") as file:
                for line in file.readlines():
                    self.default_lang = line
        except:
            with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
                file.write("en")
            with open(self.temp_dir+'\mkdb_language.tmp', "r") as file:
                for line in file.readlines():
                    self.default_lang = line

        thai = QPushButton("   ไทย (Thai)")
        thai.setIcon(QIcon("images/lang_img/th.png"))
        thai.setIconSize(QSize(20, 20))
        thai.setStyleSheet("text-align: left; padding: 10")

        english = QPushButton("   English")
        english.setIcon(QIcon("images/lang_img/en.png"))
        english.setIconSize(QSize(20, 20))
        english.setStyleSheet("text-align: left; padding: 10")

        chinese = QPushButton("   简体字 (Chinese)")
        chinese.setIcon(QIcon("images/lang_img/cn.png"))
        chinese.setIconSize(QSize(20, 20))
        chinese.setStyleSheet("text-align: left; padding: 10")

        japanese = QPushButton("   日本語 (Japanese)")
        japanese.setIcon(QIcon("images/lang_img/jp.png"))
        japanese.setIconSize(QSize(20, 20))
        japanese.setStyleSheet("text-align: left; padding: 10")

        korean = QPushButton("   한국어 (Korean)")
        korean.setIcon(QIcon("images/lang_img/kr.png"))
        korean.setIconSize(QSize(20, 20))
        korean.setStyleSheet("text-align: left; padding: 10")

        spanish = QPushButton("   español (Spanish)")
        spanish.setIcon(QIcon("images/lang_img/es.png"))
        spanish.setIconSize(QSize(20, 20))
        spanish.setStyleSheet("text-align: left; padding: 10")

        french = QPushButton("   français (French)")
        french.setIcon(QIcon("images/lang_img/fr.png"))
        french.setIconSize(QSize(20, 20))
        french.setStyleSheet("text-align: left; padding: 10")

        portuguese = QPushButton("   português (Portuguese)")
        portuguese.setIcon(QIcon("images/lang_img/pt.png"))
        portuguese.setIconSize(QSize(20, 20))
        portuguese.setStyleSheet("text-align: left; padding: 10")

        german = QPushButton("   Deutsch (German)")
        german.setIcon(QIcon("images/lang_img/de.png"))
        german.setIconSize(QSize(20, 20))
        german.setStyleSheet("text-align: left; padding: 10")

        italian = QPushButton("   italiano (Italian)")
        italian.setIcon(QIcon("images/lang_img/it.png"))
        italian.setIconSize(QSize(20, 20))
        italian.setStyleSheet("text-align: left; padding: 10")

        india = QPushButton("   हिन्दी, हिंदी (Indian)")
        india.setIcon(QIcon("images/lang_img/in.png"))
        india.setIconSize(QSize(20, 20))
        india.setStyleSheet("text-align: left; padding: 10")

        turkish = QPushButton("   Türkçe (Turkish)")
        turkish.setIcon(QIcon("images/lang_img/tr.png"))
        turkish.setIconSize(QSize(20, 20))
        turkish.setStyleSheet("text-align: left; padding: 10")

        indonesian = QPushButton("   Bahasa Indonesia (Indonesian)")
        indonesian.setIcon(QIcon("images/lang_img/id.png"))
        indonesian.setIconSize(QSize(20, 20))
        indonesian.setStyleSheet("text-align: left; padding: 10")

        filipino = QPushButton("   Wikang Filipino (Filipino)")
        filipino.setIcon(QIcon("images/lang_img/ph.png"))
        filipino.setIconSize(QSize(20, 20))
        filipino.setStyleSheet("text-align: left; padding: 10")

        russian = QPushButton("   русский язык (Russian)")
        russian.setIcon(QIcon("images/lang_img/ru.png"))
        russian.setIconSize(QSize(20, 20))
        russian.setStyleSheet("text-align: left; padding: 10")

        swedish = QPushButton("   svenska (Swedish)")
        swedish.setIcon(QIcon("images/lang_img/se.png"))
        swedish.setIconSize(QSize(20, 20))
        swedish.setStyleSheet("text-align: left; padding: 10")

        malaysian = QPushButton("   bahasa Melayu (Malaysian)")
        malaysian.setIcon(QIcon("images/lang_img/my.png"))
        malaysian.setIconSize(QSize(20, 20))
        malaysian.setStyleSheet("text-align: left; padding: 10")

        vietnamese = QPushButton("   Tiếng Việt (Vietnamese)")
        vietnamese.setIcon(QIcon("images/lang_img/vn.png"))
        vietnamese.setIconSize(QSize(20, 20))
        vietnamese.setStyleSheet("text-align: left; padding: 10")

        lao = QPushButton("   ພາສາລາວ (Lao)")
        lao.setIcon(QIcon("images/lang_img/la.png"))
        lao.setIconSize(QSize(20, 20))
        lao.setStyleSheet("text-align: left; padding: 10")

        burmese = QPushButton("   မြန်မာစာ (Burmese)")
        burmese.setIcon(QIcon("images/lang_img/mm.png"))
        burmese.setIconSize(QSize(20, 20))
        burmese.setStyleSheet("text-align: left; padding: 10")

        layout = QGridLayout()
        layout.addWidget(thai, 0, 0)
        layout.addWidget(english, 0, 1)
        layout.addWidget(chinese, 0, 2)
        layout.addWidget(japanese, 0, 3)
        layout.addWidget(korean, 1, 0)
        layout.addWidget(spanish, 1, 1)
        layout.addWidget(french, 1, 2)
        layout.addWidget(portuguese, 1, 3)
        layout.addWidget(german, 2, 0)
        layout.addWidget(italian, 2, 1)
        layout.addWidget(india, 2, 2)
        layout.addWidget(turkish, 2, 3)
        layout.addWidget(indonesian, 3, 0)
        layout.addWidget(filipino, 3, 1)
        layout.addWidget(russian, 3, 2)
        layout.addWidget(swedish, 3, 3)
        layout.addWidget(malaysian, 4, 0)
        layout.addWidget(vietnamese, 4, 1)
        layout.addWidget(lao, 4, 2)
        layout.addWidget(burmese, 4, 3)
        self.setLayout(layout)

        thai.clicked.connect(self.thai_lang)
        english.clicked.connect(self.english_lang)
        chinese.clicked.connect(self.chinese_lang)
        japanese.clicked.connect(self.japanese_lang)
        korean.clicked.connect(self.korean_lang)
        spanish.clicked.connect(self.spanish_lang)
        french.clicked.connect(self.french_lang)
        portuguese.clicked.connect(self.portuguese_lang)
        german.clicked.connect(self.german_lang)
        italian.clicked.connect(self.italian_lang)
        india.clicked.connect(self.india_lang)
        turkish.clicked.connect(self.turkish_lang)
        indonesian.clicked.connect(self.indonesian_lang)
        filipino.clicked.connect(self.filipino_lang)
        russian.clicked.connect(self.russian_lang)
        swedish.clicked.connect(self.swedish_lang)
        malaysian.clicked.connect(self.malaysian_lang)
        vietnamese.clicked.connect(self.vietnamese_lang)
        lao.clicked.connect(self.lao_lang)
        burmese.clicked.connect(self.burmese_lang)

    def thai_lang(self):
        self.default_lang = "th"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines(self.default_lang)
        self.change_lang()

    def english_lang(self):
        self.default_lang = "en"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("en")
        self.change_lang()

    def chinese_lang(self):
        self.default_lang = "cn"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("cn")
        self.change_lang()

    def japanese_lang(self):
        self.default_lang = "jp"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("jp")
        self.change_lang()

    def korean_lang(self):
        self.default_lang = "kr"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("kr")
        self.change_lang()

    def spanish_lang(self):
        self.default_lang = "es"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("es")
        self.change_lang()

    def french_lang(self):
        self.default_lang = "fr"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("fr")
        self.change_lang()

    def portuguese_lang(self):
        self.default_lang = "pt"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("pt")
        self.change_lang()

    def german_lang(self):
        self.default_lang = "de"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("de")
        self.change_lang()

    def italian_lang(self):
        self.default_lang = "it"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("it")
        self.change_lang()

    def india_lang(self):
        self.default_lang = "in"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("in")
        self.change_lang()

    def turkish_lang(self):
        self.default_lang = "tr"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("tr")
        self.change_lang()

    def indonesian_lang(self):
        self.default_lang = "id"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("id")
        self.change_lang()

    def filipino_lang(self):
        self.default_lang = "ph"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("ph")
        self.change_lang()

    def russian_lang(self):
        self.default_lang = "ru"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("ru")
        self.change_lang()

    def swedish_lang(self):
        self.default_lang = "se"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("se")
        self.change_lang()

    def malaysian_lang(self):
        self.default_lang = "my"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("my")
        self.change_lang()

    def vietnamese_lang(self):
        self.default_lang = "vn"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("vn")
        self.change_lang()

    def lao_lang(self):
        self.default_lang = "la"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("la")
        self.change_lang()

    def burmese_lang(self):
        self.default_lang = "mm"
        with open(self.temp_dir+'\mkdb_language.tmp', "w") as file:
            file.writelines("mm")
        self.change_lang()

    def change_lang(self):
        with io.open('lang/'+self.default_lang+'.json', 'r', encoding='utf-8') as json_file:
            self.data = json.load(json_file)
        self.change_lang_signal.emit()

    def txt_title(self):
        self.change_lang()
        txt_title = self.data['Title']
        return txt_title

    def txt_file(self):
        self.change_lang()
        txt_file = self.data['File']
        return txt_file
    
    def txt_view(self):
        self.change_lang()
        txt_view = self.data['View']
        return txt_view
    
    def txt_help(self):
        self.change_lang()
        txt_help = self.data['Help']
        return txt_help
    
    def txt_newdb(self):
        self.change_lang()
        txt_newdb = self.data['NewDB']
        return txt_newdb
    
    def txt_opendb(self):
        self.change_lang()
        txt_opendb = self.data['OpenDB']
        return txt_opendb
    
    def txt_savedbas(self):
        self.change_lang()
        txt_savedbas = self.data['SaveDBAs']
        return txt_savedbas
    
    def txt_recent(self):
        self.change_lang()
        txt_recent = self.data['Recent']
        return txt_recent
    
    def txt_clearrecent(self):
        self.change_lang()
        txt_clearrecent = self.data['ClearRecent']
        return txt_clearrecent
    
    def txt_exit(self):
        self.change_lang()
        txt_exit = self.data['Exit']
        return txt_exit
    
    def txt_fullscreen(self):
        self.change_lang()
        txt_fullscreen = self.data['Fullscreen']
        return txt_fullscreen
    
    def txt_language(self):
        self.change_lang()
        txt_language = self.data['Language']
        return txt_language
    
    def txt_about(self):
        self.change_lang()
        txt_about = self.data['About']
        return txt_about
    
    def txt_filter(self):
        self.change_lang()
        txt_filter = self.data['Filter']
        return txt_filter
    
    def txt_addgame(self):
        self.change_lang()
        txt_addgame = self.data['AddGame']
        return txt_addgame

    def txt_importpgn(self):
        self.change_lang()
        txt_importpgn = self.data['ImportPGN']
        return txt_importpgn
    
    def txt_close(self):
        self.change_lang()
        txt_close = self.data['Close']
        return txt_close
    
    def txt_filterbyfen(self):
        self.change_lang()
        txt_filterbyfen = self.data['FilterByFEN']
        return txt_filterbyfen
    
    def txt_board(self):
        self.change_lang()
        txt_board = self.data['Board']
        return txt_board
    
    def txt_next(self):
        self.change_lang()
        txt_next = self.data['Next']
        return txt_next
    
    def txt_apply(self):
        self.change_lang()
        txt_apply = self.data['Apply']
        return txt_apply
    
    def txt_clear(self):
        self.change_lang()
        txt_clear = self.data['Clear']
        return txt_clear
    
    def txt_ok(self):
        self.change_lang()
        txt_ok = self.data['OK']
        return txt_ok

    def txt_addsuptag(self):
        self.change_lang()
        txt_addsuptag = self.data['AddSupTag']
        return txt_addsuptag
    
    def txt_whitemove(self):
        self.change_lang()
        txt_whitemove = self.data['WhiteMove']
        return txt_whitemove
    
    def txt_blackmove(self):
        self.change_lang()
        txt_blackmove = self.data['BlackMove']
        return txt_blackmove
    
    def txt_addallgames(self):
        self.change_lang()
        txt_addallgames = self.data['AddAllGames']
        return txt_addallgames
    
    def txt_gamedetails(self):
        self.change_lang()
        txt_gamedetails = self.data['GameDetails']
        return txt_gamedetails
    
    def txt_saveassuccess(self):
        self.change_lang()
        txt_saveassuccess = self.data['SaveAsSuccess']
        return txt_saveassuccess
    
    def txt_saveasfailed(self):
        self.change_lang()
        txt_saveasfailed = self.data['SaveAsFailed']
        return txt_saveasfailed
    
    def txt_addgamesuccess(self):
        self.change_lang()
        txt_addgamesuccess = self.data['AddGameSuccess']
        return txt_addgamesuccess
    
    def txt_error(self):
        self.change_lang()
        txt_error = self.data['Error']
        return txt_error
    
    def txt_errorrecent(self):
        self.change_lang()
        txt_errorrecent = self.data['ErrorRecent']
        return txt_errorrecent
    
    def txt_day(self):
        self.change_lang()
        txt_day = self.data['Day']
        return txt_day
    
    def txt_month(self):
        self.change_lang()
        txt_month = self.data['Month']
        return txt_month
    
    def txt_year(self):
        self.change_lang()
        txt_year = self.data['Year']
        return txt_year
    
    def txt_applysuccess(self):
        self.change_lang()
        txt_applysuccess = self.data['ApplySuccess']
        return txt_applysuccess
    
    def txt_draw(self):
        self.change_lang()
        txt_draw = self.data['Draw']
        return txt_draw
    
    def txt_resign(self):
        self.change_lang()
        txt_resign = self.data['Resign']
        return txt_resign
    
    def txt_fengen(self):
        self.change_lang()
        txt_fengen = self.data['FENGen']
        return txt_fengen
    
    def txt_importinggames(self):
        self.change_lang()
        txt_importinggames = self.data['ImportingGames']
        return txt_importinggames
    
    def txt_importgames(self):
        self.change_lang()
        txt_importgames = self.data['ImportGames']
        return txt_importgames
    
    def txt_comment(self):
        self.change_lang()
        txt_comment = self.data['Comment']
        return txt_comment
    
    def txt_addcomment(self):
        self.change_lang()
        txt_addcomment = self.data['AddComment']
        return txt_addcomment
    
    def txt_editcomment(self):
        self.change_lang()
        txt_editcomment = self.data['EditComment']
        return txt_editcomment
    
    def txt_fontsize(self):
        self.change_lang()
        txt_fontsize = self.data['FontSize']
        return txt_fontsize
    
    def txt_fenerror(self):
        self.change_lang()
        txt_fenerror = self.data['FENError']
        return txt_fenerror
    