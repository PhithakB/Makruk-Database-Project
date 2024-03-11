import sys, os, sqlite3, tempfile
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QFileDialog, QSizePolicy, QAction, QToolBar, QTableView, QHeaderView, QDialog, QLabel, QTextBrowser, QGridLayout, QHBoxLayout, QTableWidget, QToolButton, QAbstractItemView, QMenu, QLineEdit, QComboBox, QPushButton, QProgressDialog, QTextEdit
from PyQt5.QtGui import QColor, QIcon, QStandardItem, QStandardItemModel, QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QTimer, QDate, QThread
from main_window import Ui_MainWindow
from searchByFen import parse
from search import searchbyfen
from searchByFenUI import BoardWindow as SearchByFenWindow
from language import LanguageDialog

db_file_path = []
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.temp_dir = tempfile.gettempdir()
        self.temp_dir = self.temp_dir + '\mkdb'
        try:
            os.makedirs(self.temp_dir)
        except:
            pass
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f"{LanguageDialog().txt_title()}")
        self.setWindowIcon(QIcon("mkdb_icon.ico"))

        self.ui.actionSave_Database_As.setEnabled(False)

        self.ui.actionNew_Database.triggered.connect(self.create_new_database)
        self.ui.actionOpen_Database.triggered.connect(self.open_database)
        self.ui.actionSave_Database_As.triggered.connect(self.save_database_as)
        self.ui.actionExit_Program.triggered.connect(self.exit_program)
        self.ui.actionFullscreen.triggered.connect(self.fullscreen)
        self.ui.actionLanguage.triggered.connect(self.language)
        self.ui.actionFontSizePlus.triggered.connect(self.fontSizePlus)
        self.ui.actionFontSizeMinus.triggered.connect(self.fontSizeMinus)
        self.ui.actionAbout.triggered.connect(self.about)

        self.load_recent_files()
        self.update_recent_files_menu()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(QWidget())
        central_layout = QVBoxLayout(self.ui.centralwidget)
        central_layout.addWidget(self.stacked_widget)

        self.chess_board_windows = []
        self.font_size = self.font().pointSize()

    def fontSizePlus(self):
        font = self.font()
        font.setPointSize(font.pointSize() + 3)
        if font.pointSize()<100:
            self.setFont(font)
            self.ui.menuFile.setFont(font)
            self.ui.menuView.setFont(font)
            self.ui.menuHelp.setFont(font)
            self.ui.menuRecent.setFont(font)
            self.font_size = self.font().pointSize()

    def fontSizeMinus(self):
        font = self.font()
        font.setPointSize(font.pointSize() - 3)
        if font.pointSize()>7:
            self.setFont(font)
            self.ui.menuFile.setFont(font)
            self.ui.menuView.setFont(font)
            self.ui.menuHelp.setFont(font)
            self.ui.menuRecent.setFont(font)
            self.font_size = self.font().pointSize()

    def language(self):
        self.lang_dialog = LanguageDialog()
        self.lang_dialog.change_lang_signal.connect(self.reload_program)
        self.lang_dialog.exec_()
        
    def reload_program(self):
        QApplication.quit()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def createPageNewDatabase(self, file_path):
        filename = os.path.basename(file_path)
        self.setWindowTitle(f"{LanguageDialog().txt_title()}" + " - " + filename)
        from database_select_game import main as db_select_game
        select_game = db_select_game(file_path)
        page = QWidget()
        toolbar = QToolBar()
        table_view = QTableView()

        table_view.setSelectionBehavior(QTableView.SelectRows)
        table_view.setEditTriggers(QTableView.NoEditTriggers)
        model = QStandardItemModel(0, 7)
        table_view.setModel(model)

        headers = ['Database', 'Game', 'White', 'Result', 'Black', 'Date', 'Event']
        model.setHorizontalHeaderLabels(headers)

        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.verticalHeader().setVisible(False)

        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        filter_action = QAction(QIcon("images/util/filter.png"), f"{LanguageDialog().txt_filter()}", self)
        add_game_action = QAction(QIcon("images/util/add.png"), f"{LanguageDialog().txt_addgame()}", self)
        import_pgn_action = QAction(QIcon("images/util/import.png"), f"{LanguageDialog().txt_importpgn()}", self)
        close_action = QAction(QIcon("images/util/close.png"), f"{LanguageDialog().txt_close()}", self)
        toolbar.addAction(filter_action)
        toolbar.addAction(add_game_action)
        toolbar.addAction(import_pgn_action)
        toolbar.addAction(close_action)

        filter_action.triggered.connect(self.open_filter_dialog)
        add_game_action.triggered.connect(self.add_game)
        import_pgn_action.triggered.connect(self.createPageImportPGN)
        close_action.triggered.connect(self.closePage)

        for action in toolbar.actions():
            button = toolbar.widgetForAction(action)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            button.setMinimumSize(70, 70)

        page.setAutoFillBackground(True)
        palette = page.palette()
        palette.setColor(page.backgroundRole(), QColor(200, 200, 200))
        page.setPalette(palette)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.setAlignment(toolbar, Qt.AlignTop)
        layout.addWidget(table_view)
        page.setLayout(layout)

        if table_view.model():
            for ele in select_game:
                if str(ele[0]).isnumeric():
                    self.insert_row_database(table_view, [filename, ele[0], ele[1][3][1], ele[1][2][1], ele[1][4][1], ele[1][1][1], ele[1][0][1]])

        table_view.doubleClicked.connect(self.create_chess_board)

        return page

    def createPageOpenDatabase(self, file_path):
        filename = os.path.basename(file_path)
        self.setWindowTitle(f"{LanguageDialog().txt_title()}" + " - " + filename)
        from database_select_game import main as db_select_game
        select_game = db_select_game(file_path)
        page = QWidget()
        toolbar = QToolBar()
        table_view = QTableView()

        table_view.setSelectionBehavior(QTableView.SelectRows)
        table_view.setEditTriggers(QTableView.NoEditTriggers)
        model = QStandardItemModel(0, 7)
        table_view.setModel(model)

        headers = ['Database', 'Game', 'White', 'Result', 'Black', 'Date', 'Event']
        model.setHorizontalHeaderLabels(headers)

        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.verticalHeader().setVisible(False)

        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        filter_action = QAction(QIcon("images/util/filter.png"), f"{LanguageDialog().txt_filter()}", self)
        add_game_action = QAction(QIcon("images/util/add.png"), f"{LanguageDialog().txt_addgame()}", self)
        import_pgn_action = QAction(QIcon("images/util/import.png"), f"{LanguageDialog().txt_importpgn()}", self)
        close_action = QAction(QIcon("images/util/close.png"), f"{LanguageDialog().txt_close()}", self)
        toolbar.addAction(filter_action)
        toolbar.addAction(add_game_action)
        toolbar.addAction(import_pgn_action)
        toolbar.addAction(close_action)

        filter_action.triggered.connect(self.open_filter_dialog)
        add_game_action.triggered.connect(self.add_game)
        import_pgn_action.triggered.connect(self.createPageImportPGN)
        close_action.triggered.connect(self.closePage)

        for action in toolbar.actions():
            button = toolbar.widgetForAction(action)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            button.setMinimumSize(70, 70)

        page.setAutoFillBackground(True)
        palette = page.palette()
        palette.setColor(page.backgroundRole(), QColor(200, 200, 200))
        page.setPalette(palette)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.setAlignment(toolbar, Qt.AlignTop)
        layout.addWidget(table_view)
        page.setLayout(layout)

        if table_view.model():
            for ele in select_game:
                if str(ele[0]).isnumeric():
                    self.insert_row_database(table_view, [filename, ele[0], ele[1][3][1], ele[1][2][1], ele[1][4][1], ele[1][1][1], ele[1][0][1]])
        
        table_view.doubleClicked.connect(self.create_chess_board)

        return page
    
    def add_game(self):
        from addGameTag import Form
        self.formDialog = Form(db_file_path[0], self.font_size)
        self.formDialog.reload.connect(self.reload_page)
        self.formDialog.show()

    def open_filter_dialog(self):
        dialog = FilterDialog(self.font_size)
        if dialog.exec_() == QDialog.Accepted:
            game_filter = dialog.game_edit.text()
            player_filter = dialog.player_edit.text().lower()
            Result_filter = dialog.Result_dropdown.currentText()
            day_filter = dialog.day_edit.text()
            month_filter = dialog.month_edit.text()
            year_filter = dialog.year_edit.text()
            Event_filter = dialog.Event_edit.text()
            fen_filter = dialog.fen_edit.text()
            filterfen = parse(fen_filter)
            gamefenid = searchbyfen(filterfen, db_file_path[0])
            boardsearch = dialog.fenboard
        
            if boardsearch:
                boardsearch = [str(id_) for id_ in boardsearch]
                boardsearch = [id_ if id_.isdigit() else '0' for id_ in boardsearch]
                boardsearch = [int(id_) for id_ in boardsearch]
        
            gamefenid = [str(id_) for id_ in searchbyfen(filterfen, db_file_path[0])]
            gamefenid = [id_ for id_ in gamefenid if id_.isdigit()]
            gamefenid = [int(id_) for id_ in gamefenid]
            self.filter_table(player_filter, game_filter, Result_filter, Event_filter, day_filter, month_filter, year_filter, gamefenid,boardsearch)
            
    def filter_table(self, player_filter, game_filter, Result_filter, Event_filter, day_filter, month_filter=None, year_filter=None, gamefenid=None,boardsearch=None):
        table_view = self.stacked_widget.currentWidget().findChild(QTableView)
        model = table_view.model()
        if model is None or model.rowCount() == 0:
            return
        game_filter = game_filter.lower()
        player_filter = player_filter.lower()
        Result_filter = Result_filter.lower()
        year_filter = year_filter.lower()
        Event_filter = Event_filter.lower()

        for row in range(model.rowCount()):
            game_item = model.index(row, 1).data()
            WhitePlayer_item = model.index(row, 2).data()
            BlackPlayer_item = model.index(row, 4).data()
            Result_item = model.index(row, 3).data()
            date_item = model.index(row, 5).data()
            Event_item = model.index(row, 6).data()

            game_matches = game_filter in str(game_item).lower()
            player_matches = player_filter in str(WhitePlayer_item).lower() or player_filter in str(BlackPlayer_item).lower()
            Result_matches = Result_filter in str(Result_item).lower()
            Event_matches = Event_filter in str(Event_item).lower()

            if day_filter:
                date_obj = QDate.fromString(date_item, "yyyy.M.d")
                day_matches = day_filter == str(date_obj.day()).lower()
            else:
                day_matches = True

            if month_filter:
                date_obj = QDate.fromString(date_item, "yyyy.M.d")
                month_matches = month_filter == str(date_obj.month()).lower()
            else:
                month_matches = True

            if year_filter:
                date_obj = QDate.fromString(date_item, "yyyy.M.d")
                year_matches = year_filter == str(date_obj.year()).lower()
            else:
                year_matches = True

            if player_matches and game_matches and Result_matches and Event_matches and month_matches and day_matches:
                if year_filter.isdigit():
                    if year_filter in str(date_obj.year()):
                        table_view.setRowHidden(row, False)
                    else:
                        table_view.setRowHidden(row, True)
                else:
                    table_view.setRowHidden(row, False)
            else:
                table_view.setRowHidden(row, True)

            if gamefenid and int(game_item) not in gamefenid:  
                table_view.setRowHidden(row, True)

            if boardsearch and int(game_item) not in boardsearch:  
                table_view.setRowHidden(row, True)

    def create_chess_board(self, val):
        column_two_index = val.sibling(val.row(), 1)
        game_id_in_table = column_two_index.data()
        chess_board_window = BoardWindow(game_id_in_table, self.font_size)
        self.chess_board_windows.append(chess_board_window)
        chess_board_window.show()

    def reload_page(self, filename):
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
        updated_page = self.createPageOpenDatabase(filename)
        self.stacked_widget.addWidget(updated_page)
        self.stacked_widget.setCurrentWidget(updated_page)

    def closePage(self):
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
        self.setWindowTitle(f"{LanguageDialog().txt_title()}")
        self.ui.actionSave_Database_As.setEnabled(False)
    
    def handle_import_pgn_dialog_on_click(self):
        filename = db_file_path[0]
        self.ui.actionSave_Database_As.setEnabled(True)
        self.reload_page(filename)
      
    def insert_row_database(self, table_view, database_data):
        model = table_view.model()
        if model:
            row_count = model.rowCount()
            model.insertRow(row_count)
            for column, value in enumerate(database_data):
                item = QStandardItem(str(value))
                model.setItem(row_count, column, item)

    def createPageImportPGN(self):
        filename, _ = QFileDialog.getOpenFileName(self, f"{LanguageDialog().txt_importpgn()}" + ' - Import PGN', '', 'Portable Game Notation (*.pgn);;All Files (*)')
        if filename:
            dialog = ImportPGNDialog(self.font_size)
            dialog.onClicked.connect(self.handle_import_pgn_dialog_on_click)
            dialog.load_pgn_file(filename)
            dialog.exec_()

    def create_new_database(self):
        filename, _ = QFileDialog.getSaveFileName(self, f"{LanguageDialog().txt_newdb()}" + ' - New Database', '', 'Makruk Database (*.mkdb);;All Files (*)')
        if filename:
            from database_create import main as Database
            Database(filename)
            self.add_page_new_database(filename)
            self.save_recent_files(filename)
            self.update_recent_files_menu()

    def open_database(self):
        filename, _ = QFileDialog.getOpenFileName(self, f"{LanguageDialog().txt_opendb()}" + ' - Open Database', '', 'Makruk Database (*.mkdb);;All Files (*)')
        if filename:
            self.add_page_open_database(filename)
            self.save_recent_files(filename)
            self.update_recent_files_menu()
            
    def save_database_as(self):
        filename, _ = QFileDialog.getSaveFileName(self, f"{LanguageDialog().txt_savedbas()}" + ' - Save Database As', '', 'Makruk Database (*.mkdb);;All Files (*)')
        if filename:
            if db_file_path[0] == filename:
                dialog = SaveAsDialogFailed(self.font_size + 4)
                dialog.exec_()
            else:
                conn = sqlite3.connect(db_file_path[0])
                backup_conn = sqlite3.connect(filename)
                cursor = conn.cursor()
                cursor.execute("PRAGMA wal_checkpoint(FULL)")
                conn.backup(backup_conn)
                conn.close()
                backup_conn.close()
                self.setWindowTitle(f"{LanguageDialog().txt_title()}" + " - " + os.path.basename(filename))
                self.ui.actionSave_Database_As.setEnabled(False)
                self.save_recent_files(filename)
                self.update_recent_files_menu()
                db_file_path.clear()
                db_file_path.append(filename)
                dialog = SaveAsDialog(self.font_size + 4)
                dialog.exec_()

    def show_recent_files(self, filename):
        filename = filename.replace('\n', '')
        try:
            with open(filename, 'r') as db_file:
                if db_file:
                    self.add_page_open_database(filename)
        except:
            self.update_recent_files(filename)
            self.update_recent_files_menu()
            dialog = RecentErrorDialog(self.font_size + 4)
            dialog.exec_()

    def update_recent_files(self, filename):
        with open(self.temp_dir+'\mkdb_recent_files.tmp', "r") as file:
            lines = []
            for line in file:
                if filename not in line:
                    lines.append(line)

        with open(self.temp_dir+'\mkdb_recent_files.tmp', "w") as file:
            for line in lines:
                file.write(line)
                    
    def update_recent_files_menu(self):
        self.ui.menuRecent.clear()
        recent_files = self.load_recent_files()
        font = QFont()
        font.setPointSize(20)
        for file in recent_files:
            self.actionRecent = QAction(file, self.ui.centralwidget)
            self.actionRecent.triggered.connect(lambda checked, file=file: self.show_recent_files(file))
            self.ui.menuRecent.addAction(self.actionRecent)
        self.ui.menuRecent.addSeparator()
        self.actionClearRecent = QAction(f"{LanguageDialog().txt_clearrecent()}", self.ui.centralwidget)
        self.ui.menuRecent.addAction(self.actionClearRecent)
        self.actionClearRecent.triggered.connect(self.clear_recent)

    def load_recent_files(self):
        try:
            with open(self.temp_dir+'\mkdb_recent_files.tmp', 'r') as file:
                lines = file.readlines()
                lines.reverse()
                return lines
        except:
            open(self.temp_dir+'\mkdb_recent_files.tmp', 'w')

    def save_recent_files(self, filename):
        file_exists = 0
        data_len = 0
        with open(self.temp_dir+'\mkdb_recent_files.tmp', 'r') as file_read:
            for data in file_read:
                if (filename+'\n') == data:
                    file_exists += 1
                data_len += 1
            if file_exists > 0:
                pass
            else:
                with open(self.temp_dir+'\mkdb_recent_files.tmp', 'a') as file_write:
                    file_write.write(filename+'\n')
                    data_len += 1

        if data_len > 5:
            with open(self.temp_dir+'\mkdb_recent_files.tmp', 'r') as file_read:
                data = file_read.read().splitlines(True)
            with open(self.temp_dir+'\mkdb_recent_files.tmp', 'w') as file_write:
                file_write.writelines(data[1:])

    def clear_recent(self):
        with open(self.temp_dir+'\mkdb_recent_files.tmp', 'w') as file_write:
            file_write.writelines
        self.update_recent_files_menu()

    def exit_program(self):
        sys.exit(app.exec_())
    
    def fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def about(self):
        dialog = AboutDialog(self.font_size + 4)
        dialog.exec_()

    def add_page_new_database(self, filename):
        db_file_path.clear()
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
        page = self.createPageNewDatabase(filename)
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)
        self.ui.actionSave_Database_As.setEnabled(True)
        db_file_path.append(filename)

    def add_page_open_database(self, filename):
        db_file_path.clear()
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
        page = self.createPageOpenDatabase(filename)
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)
        self.ui.actionSave_Database_As.setEnabled(True)
        db_file_path.append(filename)

class AddGamesThread(QThread):
    updateProgress = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        from game_check import game
        for pgn_num in range(len(game)):
            self.updateProgress.emit(pgn_num + 1)
            from pgn_parser import main as Parser
            Parser(game[pgn_num][1], db_file_path[0])

class ImportPGNDialog(QDialog):
    onClicked = pyqtSignal()
    def __init__(self, font_size):
        super().__init__()
        self.setWindowTitle(f"{LanguageDialog().txt_importpgn()}")
        self.setWindowIcon(QIcon("images/util/import.png"))
        self.setModal(True)
        self.setMinimumSize(800, 600)
        self.font_size = font_size
        table_view = QTableView()
        toolbar = QToolBar()
        toolbar.setStyleSheet("QToolBar { border: 1px solid black; }")
        toolbar.setToolButtonStyle(Qt.ToolButtonTextOnly)

        add_all_games = QAction(f"{LanguageDialog().txt_addallgames()}", self)
        toolbar.addAction(add_all_games)

        for action in toolbar.actions():
            button = toolbar.widgetForAction(action)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            button.setMinimumSize(100, 40)
            button.setStyleSheet("QToolButton { font-weight: bold; }")
            font = QFont()
            font.setPointSize(self.font_size)
            button.setFont(font)

        add_all_games.triggered.connect(self.add_all_games_triggered)

        table_view.setSelectionBehavior(QTableView.SelectRows)
        table_view.setEditTriggers(QTableView.NoEditTriggers)
        model = QStandardItemModel(0, 6)
        table_view.setModel(model)

        headers = ['Game', 'White', 'Result', 'Black', 'Date', 'Event']
        model.setHorizontalHeaderLabels(headers)

        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.verticalHeader().setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.setAlignment(toolbar, Qt.AlignRight)
        layout.addWidget(table_view)
        self.setLayout(layout)
        table_view.doubleClicked.connect(self.getValue)

        app_font = self.font()
        app_font.setPointSize(self.font_size)
        self.setFont(app_font)

    def load_pgn_file(self, filenamePGN):
        from game_check import main as GameCheck
        filename = os.path.basename(filenamePGN)
        GameCheck(filenamePGN)
        from game_check import real_game_tag as GameTag

        for ele in GameTag:
            if str(ele[0]).isnumeric():
                self.insert_row_pgn([filename, ele[1][0][1], ele[1][1][1], ele[1][2][1], ele[1][3][1], ele[1][4][1]])

    def add_all_games_triggered(self):
        from game_check import game
        self.thread = AddGamesThread(self)
        self.progress_dialog = QProgressDialog(f"{LanguageDialog().txt_importinggames()}", "", 0, len(game), self)
        self.progress_dialog.setFixedSize(400, 100)
        self.progress_dialog.setWindowTitle(f"{LanguageDialog().txt_importgames()}")
        self.progress_dialog.setWindowIcon(QIcon("images/util/import.png"))
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setCancelButton(None)
        self.thread.updateProgress.connect(self.update_progress)
        QTimer.singleShot(100, self.start_tread)

    def update_progress(self, value):
        from game_check import game
        self.progress_dialog.setValue(value)

        if value >= len(game):
            self.progress_dialog.close()
            self.onClicked.emit()
            dialog = AddAllGamesDialog(self.font_size)
            dialog.exec_()

    def start_tread(self):
        self.thread.start()

    def getValue(self, val):
        from game_check import game
        row_clicked = val.row()+1
        for pgn in game:
            if pgn[0] == row_clicked:
                pgn_selected = pgn[1]
                dialog = PGNCheckDialog(pgn_selected, self.font_size)
                dialog.exec_()

    def insert_row_pgn(self, database_data):
        model = self.findChild(QTableView).model()
        row_count = model.rowCount()
        model.insertRow(row_count)
        for column, value in enumerate(database_data):
            item = QStandardItem(str(value))
            model.setItem(row_count, column, item)

class AddAllGamesDialog(QDialog):
    def __init__(self, font_size):
        super().__init__()
        self.setWindowTitle(f"{LanguageDialog().txt_addallgames()}")
        self.setWindowIcon(QIcon("images/util/accept.png"))
        self.setModal(True)
        self.setMinimumSize(400, 200)

        about_label = QLabel(f"{LanguageDialog().txt_addgamesuccess()}")
        about_label.setAlignment(Qt.AlignCenter)
        
        font = QFont()
        font.setPointSize(font_size + 4)
        about_label.setFont(font)

        label_container = QWidget()
        label_layout = QVBoxLayout()
        label_layout.addWidget(about_label)
        label_container.setLayout(label_layout)

        dialog_layout = QVBoxLayout(self)
        dialog_layout.addStretch(1)
        dialog_layout.addWidget(label_container)
        dialog_layout.addStretch(1)

        self.setLayout(dialog_layout)

class PGNCheckDialog(QDialog):
    def __init__(self, pgn_selected, font_size):
        super().__init__()
        self.setWindowTitle(f"{LanguageDialog().txt_gamedetails()}")
        self.setWindowIcon(QIcon("images/util/details.png"))
        self.setModal(True)

        self.text_browser = QTextBrowser()
        self.text_browser.setPlainText(pgn_selected)

        preferred_width = 600
        preferred_height = self.text_browser.sizeHint().height() + 100

        self.setMinimumSize(preferred_width, preferred_height)

        font = QFont()
        font.setPointSize(font_size)
        self.text_browser.setFont(font)

        layout = QVBoxLayout(self)
        layout.addWidget(self.text_browser)
        self.setLayout(layout)

class AboutDialog(QDialog):
    def __init__(self, font_size):
        super().__init__()
        self.setWindowTitle(f"{LanguageDialog().txt_about()}")
        self.setWindowIcon(QIcon("images/util/about.png"))
        self.setModal(True)
        self.setMinimumSize(400, 200)

        about_label = QLabel("This is Makruk Database application\n"
                             "Version : 1.0\n"
                             "Author : Makruk Database Project Team\n"
                             "Member : Phithak Buathong\n"
                             "               Napat Mueangnakin\n"
                             "               Nattaphong Sakamornchai")
        about_label.setAlignment(Qt.AlignLeft)
        
        font = QFont()
        font.setPointSize(font_size)
        about_label.setFont(font)

        label_container = QWidget()
        label_layout = QVBoxLayout()
        label_layout.addWidget(about_label)
        label_container.setLayout(label_layout)

        dialog_layout = QVBoxLayout(self)
        dialog_layout.addStretch(1)
        dialog_layout.addWidget(label_container)
        dialog_layout.addStretch(1)

        self.setLayout(dialog_layout)

class SaveAsDialog(QDialog):
    def __init__(self, font_size):
        super().__init__()
        self.setWindowTitle(f"{LanguageDialog().txt_savedbas()}")
        self.setWindowIcon(QIcon("images/util/accept.png"))
        self.setModal(True)
        self.setMinimumSize(400, 200)

        about_label = QLabel(f"{LanguageDialog().txt_saveassuccess()}")
        about_label.setAlignment(Qt.AlignCenter)
        
        font = QFont()
        font.setPointSize(font_size)
        about_label.setFont(font)

        label_container = QWidget()
        label_layout = QVBoxLayout()
        label_layout.addWidget(about_label)
        label_container.setLayout(label_layout)

        dialog_layout = QVBoxLayout(self)
        dialog_layout.addStretch(1)
        dialog_layout.addWidget(label_container)
        dialog_layout.addStretch(1)

        self.setLayout(dialog_layout)

class SaveAsDialogFailed(QDialog):
    def __init__(self, font_size):
        super().__init__()
        self.setWindowTitle(f"{LanguageDialog().txt_savedbas()}")
        self.setWindowIcon(QIcon("images/util/error.png"))
        self.setModal(True)
        self.setMinimumSize(400, 200)

        about_label = QLabel(f"{LanguageDialog().txt_saveasfailed()}")
        about_label.setAlignment(Qt.AlignCenter)
        
        font = QFont()
        font.setPointSize(font_size)
        about_label.setFont(font)

        label_container = QWidget()
        label_layout = QVBoxLayout()
        label_layout.addWidget(about_label)
        label_container.setLayout(label_layout)

        dialog_layout = QVBoxLayout(self)
        dialog_layout.addStretch(1)
        dialog_layout.addWidget(label_container)
        dialog_layout.addStretch(1)

        self.setLayout(dialog_layout)

class RecentErrorDialog(QDialog):
    def __init__(self, font_size):
        super().__init__()
        self.setWindowTitle(f"{LanguageDialog().txt_error()}")
        self.setWindowIcon(QIcon("images/util/error.png"))
        self.setModal(True)
        self.setMinimumSize(400, 200)

        about_label = QLabel(f"{LanguageDialog().txt_errorrecent()}")
        about_label.setAlignment(Qt.AlignCenter)
        
        font = QFont()
        font.setPointSize(font_size)
        about_label.setFont(font)

        label_container = QWidget()
        label_layout = QVBoxLayout()
        label_layout.addWidget(about_label)
        label_container.setLayout(label_layout)

        dialog_layout = QVBoxLayout(self)
        dialog_layout.addStretch(1)
        dialog_layout.addWidget(label_container)
        dialog_layout.addStretch(1)

        self.setLayout(dialog_layout)
              
class BoardWindow(QWidget):
    def __init__(self, game_id_in_table, font_size):
        super().__init__()
        self.setMinimumSize(1300, 800)
        self.setWindowTitle(f"{LanguageDialog().txt_board()}")
        self.setWindowIcon(QIcon("images/util/board.png"))
        self.font_size = font_size
        from database_select_position import get_position
        from database_select_move_by_id import main as db_select_move_by_id
        self.game_id = game_id_in_table
        self.select_move_by_id_old = db_select_move_by_id(db_file_path[0], game_id_in_table)
        self.pos_old = get_position(db_file_path[0], game_id_in_table)
        self.select_move_by_id = []
        self.pos = []
        self.flg = 0
        self.row = 0
        self.column = 0
        self.check_black_move_first()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.create_chess_board(self.flg, self.pos)
        self.create_info(self.select_move_by_id)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop_play)
        
    def update_flg(self, new_flg, row, column):
        self.flg = new_flg
        self.row = row
        self.column = column
        self.create_chess_board(self.flg, self.pos)
        self.create_info(self.select_move_by_id)
        self.showComment(self.flg)
        if self.info_layout.tableWidget.item(self.row, self.column) is not None:
            self.info_layout.tableWidget.item(self.row, self.column).setBackground(QColor(Qt.yellow))
        
    def create_chess_board(self, flg, pos):
        if hasattr(self, 'chess_board'):
            self.layout.removeWidget(self.chess_board)
            self.chess_board.deleteLater()
        self.chess_board = Board(flg, pos)
        self.layout.addWidget(self.chess_board, 8)

    def create_info(self, select_move_by_id):
        if hasattr(self, 'info_layout'):
            self.layout.removeWidget(self.info_layout)
            self.info_layout.deleteLater()
        self.info_layout = Info(select_move_by_id, self.game_id, self.font_size)
        app_font = self.info_layout.tableWidget.font()
        app_font.setPointSize(self.font_size)
        self.info_layout.tableWidget.setFont(app_font)
        self.info_layout.tableWidget.horizontalHeader().setFont(app_font)
        self.info_layout.tableWidget.resizeColumnsToContents()
        self.info_layout.tableWidget.resizeRowsToContents()
        self.info_layout.flgChanged.connect(self.update_flg)
        self.info_layout.button_double_left.connect(self.button_d_left)
        self.info_layout.button_double_right.connect(self.button_d_right)
        self.info_layout.button_left_and_right.connect(self.button_left_right)
        self.info_layout.button_play_pause.connect(self.button_play_pause)
        self.layout.addWidget(self.info_layout, 2)

    def showComment(self, move_num):
        try:
            conn = sqlite3.connect(db_file_path[0])
            cursor = conn.cursor()
            cursor.execute(f"SELECT Comment FROM Comment WHERE Game_ID = {self.game_id} AND Move_ID = {move_num}")
            comment_fecth = cursor.fetchall()
            if comment_fecth:
                self.info_layout.comment_detail.setText(comment_fecth[0][0])
            conn.commit()
        finally:
            conn.close()

    def check_black_move_first(self):
        if self.select_move_by_id_old[0][0] == 2:
            self.select_move_by_id.append(('1', ''))
            self.pos.append(self.pos_old[0])
        for i in self.select_move_by_id_old:
            self.select_move_by_id.append(i)
        for i in self.pos_old:
            self.pos.append(i)

    def button_d_left(self):
        self.flg = 0
        self.row_column()

    def button_d_right(self):
        pos_list = self.pos
        length = len(pos_list) - 1
        self.flg = length
        self.row_column()

    def button_left_right(self, side):
        self.move_num(side)

    def button_play_pause(self, stage):
        if stage == "play":
            self.timer.start(800)
        if stage == "pause":
            self.timer.stop()
    
    def loop_play(self):
        if self.flg < len(self.pos) - 1:
            self.flg += 1
            self.row_column()
        else:
            self.timer.stop()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            side = "right"
            self.move_num(side)
        elif event.key() == Qt.Key_Left:
            side = "left"
            self.move_num(side)

    def move_num(self, side):
        pos_list = self.pos
        length = len(pos_list) - 1
        if side == "right" and self.flg == length:
            self.flg = length
        elif side == "right":
            self.flg += 1
        elif side == "left" and self.flg != 0:
            self.flg -= 1
        else:
            self.flg = self.flg
        self.row_column()
    
    def row_column(self):
        row = ((self.flg % 2) + (self.flg // 2)) - 1
        column = 0
        if self.flg%2 == 0:
            column = 2
        if self.flg%2 == 1:
            column = 1
        self.update_flg(self.flg, row, column)

class Piece(QLabel):
    def __init__(self,  piece_name, parent=None):
        super().__init__(parent)
        self.piece_name = piece_name
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(1, 1)
        self.setAlignment(Qt.AlignCenter)
        self.setAttribute(Qt.WA_TranslucentBackground)
        pixmap = QPixmap("images/pieces/"+piece_name+".png").scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.setScaledContents(True)
        
    def resizeEvent(self, event):
        if event.size().width() > event.size().height():
            self.resize(event.size().height(), event.size().height())
        else:
            self.resize(event.size().width(), event.size().width())

class Board(QWidget):
    def __init__(self, flg, pos, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.draw_squares(self.layout)
        self.position = pos
        self.index = flg
        self.sqsize = 100
        
        self.get_board(self.position[self.index],self.layout)
        
        self.setLayout(self.layout)
        
    def draw_squares(self, layout):
        for row, rank in enumerate('87654321'):
            for col, file in enumerate('abcdefgh'):
                square = QWidget(self)
                square.setObjectName(file + rank)
                square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                if row % 2 == col % 2:
                    square.setStyleSheet('background-color: #F0D9B5')
                else:
                    square.setStyleSheet('background-color: #B58863')
                layout.addWidget(square, row, col)
                
    def get_board(self, fen, layout):
        fen_to_board = [fen[i:i+8] for i in range(0, len(fen), 8)]
        board = [list(fen_to_board) for fen_to_board in fen_to_board]
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                
                if piece.islower() and piece != "-":
                    color = "b"
                    piece_name = color+piece.upper()
                    piece = Piece(piece_name)
                    layout.addWidget(piece, row, col)
                    
                elif piece.isupper() and piece != "-":
                    color = "w"
                    piece_name = color+piece.upper()
                    piece = Piece(piece_name)
                    layout.addWidget(piece, row, col)

    def resizeEvent(self, event):
        if event.size().width() > event.size().height():
            self.resize(event.size().height(), event.size().height())
            self.sqr_size = int(event.size().height() / 8)
        else:
            self.resize(event.size().width(), event.size().width())
            self.sqr_size = int(event.size().width() / 8)

class Info(QWidget):
    flgChanged = pyqtSignal(int, int, int)
    button_double_left = pyqtSignal()
    button_left_and_right = pyqtSignal(str)
    button_play_pause = pyqtSignal(str)
    button_double_right = pyqtSignal()
    def __init__(self, select_move_by_id, game_id, font_size):
        super().__init__()
        self.game_id = game_id
        self.initUI(select_move_by_id)
        self.font_size = font_size

    def initUI(self, select_move_by_id):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        column_names = ["    ", f"{LanguageDialog().txt_whitemove()}", f"{LanguageDialog().txt_blackmove()}"]
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionsClickable(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setStyleSheet("QTableWidget::item:selected { background-color: transparent; }")

        all_move = [i for i in select_move_by_id]
        move = self.match_pairs(all_move)
        for index, data in enumerate(move, start=1):
            if str(index).isnumeric():
                self.insert_row_database([index, data[0], data[1]])

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        self.tableWidget.cellClicked.connect(self.cell_clicked)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.showContextMenu)

        button_double_left = QToolButton()
        button_double_left.setIcon(QIcon("images/util/double-left.png"))
        button_double_left.setIconSize(QSize(60, 40))

        button_left = QToolButton()
        button_left.setIcon(QIcon("images/util/left.png"))
        button_left.setIconSize(QSize(60, 40))

        button_pause = QToolButton()
        button_pause.setIcon(QIcon("images/util/pause.png"))
        button_pause.setIconSize(QSize(60, 40))

        button_play = QToolButton()
        button_play.setIcon(QIcon("images/util/play.png"))
        button_play.setIconSize(QSize(60, 40))

        button_right = QToolButton()
        button_right.setIcon(QIcon("images/util/right.png"))
        button_right.setIconSize(QSize(60, 40))

        button_double_right = QToolButton()
        button_double_right.setIcon(QIcon("images/util/double-right.png"))
        button_double_right.setIconSize(QSize(60, 40))

        button_double_left.clicked.connect(self.button_double_left_clicked)
        button_left.clicked.connect(self.button_left_clicked)
        button_pause.clicked.connect(self.button_pause_clicked)
        button_play.clicked.connect(self.button_play_clicked)
        button_right.clicked.connect(self.button_right_clicked)
        button_double_right.clicked.connect(self.button_double_right_clicked)

        button_double_left.setFocusPolicy(Qt.NoFocus)
        button_left.setFocusPolicy(Qt.NoFocus)
        button_pause.setFocusPolicy(Qt.NoFocus)
        button_play.setFocusPolicy(Qt.NoFocus)
        button_right.setFocusPolicy(Qt.NoFocus)
        button_double_right.setFocusPolicy(Qt.NoFocus)

        button_layout = QHBoxLayout()
        button_layout.addWidget(button_double_left)
        button_layout.addWidget(button_left)
        button_layout.addWidget(button_pause)
        button_layout.addWidget(button_play)
        button_layout.addWidget(button_right)
        button_layout.addWidget(button_double_right)
        
        comment_label = QLabel(f"{LanguageDialog().txt_comment()}", self)
        self.comment_detail = QTextBrowser()

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget, 6)
        layout.addWidget(comment_label)
        layout.addWidget(self.comment_detail, 1)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def showContextMenu(self, pos):
        index = self.tableWidget.indexAt(pos)
        if index.isValid():
            self.move_num = self.go_to_moves(index)
            if index.column() != 0 and index.data() is not None:
                menu = QMenu(self)

                add_comment_action = QAction(f"{LanguageDialog().txt_addcomment()}", self)
                add_comment_action.triggered.connect(self.addComment)
                menu.addAction(add_comment_action)
                add_comment_action.setEnabled(False)

                edit_comment_action = QAction(f"{LanguageDialog().txt_editcomment()}", self)
                edit_comment_action.triggered.connect(self.editComment)
                menu.addAction(edit_comment_action)
                edit_comment_action.setEnabled(False)
                
                try:
                    conn = sqlite3.connect(db_file_path[0])
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT Comment FROM Comment WHERE Game_ID = {self.game_id} AND Move_ID = {self.move_num}")
                    comment_fecth = cursor.fetchall()
                    if comment_fecth:
                        edit_comment_action.setEnabled(True)
                    else:
                        add_comment_action.setEnabled(True)
                    conn.commit()
                finally:
                    conn.close()

                menu.exec_(self.mapToGlobal(pos))

    def addComment(self):
        dialog = AddCommentDialog(self.font_size)
        dialog.add_comment.connect(self.insert_comment)
        dialog.exec_()

    def editComment(self):
        dialog = EditCommentDialog(self.game_id, self.move_num, self.font_size)
        dialog.edit_comment.connect(self.edit_comment)
        dialog.exec_()

    def insert_comment(self, comment):
        try:
            conn = sqlite3.connect(db_file_path[0])
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO Comment (Comment, Game_ID, Move_ID) VALUES ('{comment}', {self.game_id}, {self.move_num})")
            self.comment_detail.setText(comment)
            conn.commit()
        finally:
            conn.close()

    def edit_comment(self, comment):
        try:
            conn = sqlite3.connect(db_file_path[0])
            cursor = conn.cursor()
            cursor.execute(f"UPDATE Comment SET Comment = '{comment}' WHERE Game_ID = {self.game_id} AND Move_ID = {self.move_num}")
            self.comment_detail.setText(comment)
            conn.commit()
        finally:
            conn.close()

    def match_pairs(self, input_data):
        result = []
        while input_data:
            first = input_data.pop(0)
            second = input_data.pop(0) if input_data else None
            result.append((first[1], second[1] if second else None))
        return result

    def cell_clicked(self, row, column):
        item = self.tableWidget.item(row, column)
        move_num = self.go_to_moves(item)
        if move_num:
            self.flgChanged.emit(move_num, row, column)
        
    def go_to_moves(self, item):
        if item is not None:
            if item.column() != 0:
                move_num = 0
                if item.column() == 1:
                    move_num = (((item.row()+1)*2)-1)
                elif item.column() == 2:
                    move_num = ((item.row()+1)*2)
                return move_num

    def insert_row_database(self, database_data):
        model = self.tableWidget.model()
        if model:
            row_count = model.rowCount()
            model.insertRow(row_count)
            model.setData(model.index(row_count, 0), database_data[0], Qt.DisplayRole)
            model.setData(model.index(row_count, 1), database_data[1], Qt.DisplayRole)
            model.setData(model.index(row_count, 2), database_data[2], Qt.DisplayRole)

    def button_double_left_clicked(self):
        self.button_double_left.emit()

    def button_left_clicked(self):
        side = "left"
        self.button_left_and_right.emit(side)
        self.button_play_pause.emit("pause")

    def button_pause_clicked(self):
        self.button_play_pause.emit("pause")

    def button_play_clicked(self):
        self.button_play_pause.emit("play")

    def button_right_clicked(self):
        side = "right"
        self.button_left_and_right.emit(side)
        self.button_play_pause.emit("pause")

    def button_double_right_clicked(self):
        self.button_double_right.emit()

class AddCommentDialog(QDialog):
    add_comment = pyqtSignal(str)
    def __init__(self, font_size):
        super().__init__()
        self.setMinimumWidth(300)
        self.setWindowTitle(f"{LanguageDialog().txt_addcomment()}")
        self.setWindowIcon(QIcon("images/util/comment.png"))

        self.layout = QVBoxLayout(self)
        self.apply_button = QPushButton(f"{LanguageDialog().txt_apply()}")  
        self.apply_button.clicked.connect(self.apply)
        
        self.add_comment_fill = QTextEdit()
        self.layout.addWidget(self.add_comment_fill)
        self.layout.addWidget(self.apply_button)

        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)

    def apply(self):
        comment = self.add_comment_fill.toPlainText()
        self.add_comment.emit(comment)
        self.close()

class EditCommentDialog(QDialog):
    edit_comment = pyqtSignal(str)
    def __init__(self, game_id, move_num, font_size):
        super().__init__()
        self.setMinimumWidth(300)
        self.setWindowTitle(f"{LanguageDialog().txt_editcomment()}")
        self.setWindowIcon(QIcon("images/util/comment.png"))
        self.game_id = game_id
        self.move_num = move_num

        self.layout = QVBoxLayout(self)
        self.apply_button = QPushButton(f"{LanguageDialog().txt_apply()}")  
        self.apply_button.clicked.connect(self.apply)
        
        self.add_comment_fill = QTextEdit()
        self.layout.addWidget(self.add_comment_fill)
        self.layout.addWidget(self.apply_button)

        try:
            conn = sqlite3.connect(db_file_path[0])
            cursor = conn.cursor()
            cursor.execute(f"SELECT Comment FROM Comment WHERE Game_ID = {self.game_id} AND Move_ID = {self.move_num}")
            comment_fecth = cursor.fetchall()
            self.add_comment_fill.append(comment_fecth[0][0])
            conn.commit()
        finally:
            conn.close()

        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)

    def apply(self):
        comment = self.add_comment_fill.toPlainText()
        self.edit_comment.emit(comment)
        self.close()

class FilterDialog(QDialog):
    fen_generated = pyqtSignal(str)
    def __init__(self, font_size):
        super().__init__()
        self.setWindowTitle(f"{LanguageDialog().txt_filter()}")
        self.setWindowIcon(QIcon("images/util/filter.png"))
        self.setMinimumSize(400, 250)
        self.font_size = font_size
        self.game_label = QLabel("Game ID:")
        self.game_edit = QLineEdit()
        self.fenboard = None
        self.player_label = QLabel("Player:")
        self.player_edit = QLineEdit()
        
        
        self.Result_label = QLabel("Result:")
        self.Result_dropdown = QComboBox()
        self.Result_dropdown.addItem("")
        self.Result_dropdown.addItem("1-0")
        self.Result_dropdown.addItem("0-1")
        self.Result_dropdown.addItem("*")
        self.Result_dropdown.addItem("Draw")
        
        self.Date_label = QLabel("Date:  ")
        self.day_edit = QLineEdit()
        self.day_edit.setPlaceholderText(f"{LanguageDialog().txt_day()}")
        self.month_edit = QLineEdit()
        self.month_edit.setPlaceholderText(f"{LanguageDialog().txt_month()}")
        self.year_edit = QLineEdit()
        self.year_edit.setPlaceholderText(f"{LanguageDialog().txt_year()}")
        
        self.Event_label = QLabel("Event:")
        self.Event_edit = QLineEdit()
        
        self.fen_label = QLabel(f"{LanguageDialog().txt_filterbyfen()}")
        self.fen_edit = QLineEdit()
        self.fen_button = QPushButton(f"{LanguageDialog().txt_board()}")
        self.fen_button.clicked.connect(self.open_board_window)
        
        self.filter_button = QPushButton(f"{LanguageDialog().txt_filter()}")
        self.filter_button.clicked.connect(self.accept)
        
        self.board_window = None
        
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.game_label, 0, 0)
        self.grid_layout.addWidget(self.game_edit, 0, 1, 1, 3)
        
        self.grid_layout.addWidget(self.player_label, 1, 0)
        self.grid_layout.addWidget(self.player_edit, 1, 1, 1, 3)
        
        self.grid_layout.addWidget(self.Result_label, 3, 0)
        self.grid_layout.addWidget(self.Result_dropdown, 3, 1, 1, 3)
        
        self.grid_layout.addWidget(self.Date_label, 4, 0)
        self.grid_layout.addWidget(self.day_edit, 4, 1)
        self.grid_layout.addWidget(self.month_edit, 4, 2)
        self.grid_layout.addWidget(self.year_edit, 4, 3)
        
        self.grid_layout.addWidget(self.Event_label, 5, 0)
        self.grid_layout.addWidget(self.Event_edit, 5, 1, 1, 3)
        
        self.grid_layout.addWidget(self.fen_label, 6, 0)
        self.grid_layout.addWidget(self.fen_edit, 6, 1, 1, 2)
        self.grid_layout.addWidget(self.fen_button, 6, 3)
        
        self.grid_layout.addWidget(self.filter_button, 7, 0, 1, 4)
        
        self.setLayout(self.grid_layout)

        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)

    def open_board_window(self):
        start_fen = ''
        if self.fen_edit.text() != '':
            start_fen = self.fen_edit.text()
        new_dialog = QDialog()
        new_dialog.setFixedSize(800, 700)
        board_window = SearchByFenWindow(start_fen, self.font_size)
        board_window.setParent(new_dialog)
        layout = QVBoxLayout(new_dialog)
        layout.addWidget(board_window)
        new_dialog.setWindowTitle(f"{LanguageDialog().txt_board()}")
        new_dialog.setWindowIcon(QIcon("images/util/board.png"))
        board_window.fen_generated.connect(self.fenfil)
        
        board_window.search_button_clicked.connect(new_dialog.accept)
        
        board_window.standard_fen.connect(self.show_fen)
        
        if new_dialog.exec_() == QDialog.Accepted:
            pass 
            
    def fenfil(self, fen):
        self.fenboard = (searchbyfen(fen, db_file_path[0]))

    def show_fen(self, standard_fen):
        lineEdit = self.grid_layout.itemAtPosition(6, 1).widget()
        lineEdit.setText(standard_fen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())