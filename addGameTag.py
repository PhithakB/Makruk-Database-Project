from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from addGameFormat import parse, start_board, color_turn
from language import LanguageDialog

class Form(QWidget):
    tag_signal = pyqtSignal()
    reload = pyqtSignal(str)
    def __init__(self, db_file_path, font_size):
        super().__init__()
        self.setWindowTitle(f"{LanguageDialog().txt_addgame()}")
        self.setWindowIcon(QIcon("images/util/add.png"))
        self.setFixedWidth(400)
        self.layout = QVBoxLayout(self)
        self.font_size = font_size
        self.db_file_path = db_file_path
        self.create_seven_tag()
        self.create_new_window_button()
        self.create_submit_button()
        
        self.tag_signal.connect(self.seven_tag.tag_values)
        self.seven_tag.next_signal.connect(self.close_panel)
        self.seven_tag.reload_page.connect(self.reload_page)

        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)

    def reload_page(self):
        self.reload.emit(self.db_file_path)
    
    def close_panel(self):
        self.close()
        
    def create_new_window_button(self):
        button = QPushButton(f"{LanguageDialog().txt_addsuptag()}")
        button.clicked.connect(self.open_new_window)
        self.layout.addWidget(button)
        
    def create_submit_button(self):
        button = QPushButton(f"{LanguageDialog().txt_next()}")
        button.clicked.connect(self.submit_button)
        self.layout.addWidget(button)
        
    def submit_button(self):
        self.tag_signal.emit()
        
    def open_new_window(self):
        dialog = SupTagDialog(self.font_size)
        dialog.sup_tag.add_sup_tag.connect(self.seven_tag.suptag_rev)
        dialog.exec_()

    def create_seven_tag(self):
        self.seven_tag = SevenTagRoster(self.db_file_path, self.font_size)
        self.layout.addWidget(self.seven_tag)
        
    def get_tag_names(self, tag_names):
        self.tag_names = tag_names

class SevenTagRoster(QWidget):
    next_signal = pyqtSignal()
    reload_page = pyqtSignal(str)
    def __init__(self, db_file_path, font_size):
        super().__init__()
        self.grid_layout = QGridLayout(self)
        self.tag_name()
        self.font_size = font_size
        self.db_file_path = db_file_path

    def tag_name(self):
        self.tags = ['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'FEN']
        for self.tag_row, tag_name in enumerate(self.tags):
            label = QLabel(f'{tag_name} :')
            lineEdit = QLineEdit()
            setattr(self, tag_name.replace(" ", "_"), lineEdit)
            self.grid_layout.addWidget(label, self.tag_row, 0)
            self.grid_layout.addWidget(lineEdit, self.tag_row, 1)

    def tag_values(self):
        self.values = []
        for tag in self.tags:
            value = getattr(self, tag.replace(" ", "_"), None)
            if value:
                self.values.append(value.text())
                
        if self.values[6] == '':
            fen = "rnsmksnr/8/pppppppp/8/8/PPPPPPPP/8/RNSKMSNR w - - 0 1"
            self.values[6] = fen
            
        else:
            fen = self.values[6]
            
        try:
            turn = color_turn(fen)
            board = start_board(parse(fen))
            turn_board = [turn,board]
            from addGame import BoardWindow
            self.formDialog = BoardWindow(turn_board, self.tags, self.values, self.db_file_path, self.font_size)
            self.formDialog.reload.connect(self.reload)
            self.formDialog.show()
            self.next_signal.emit()
        except:
            dialog = FENErrorDialog()
            dialog.exec_()
    
    def reload(self):
        self.reload_page.emit(self.db_file_path)
        
    def suptag_rev(self, tag_name):
        self.tags.append(tag_name)
        label = QLabel(f'{tag_name} :')
        lineEdit = QLineEdit()
        setattr(self, tag_name.replace(" ", "_"), lineEdit)
        self.grid_layout.addWidget(label, self.tag_row+1, 0)
        self.grid_layout.addWidget(lineEdit, self.tag_row+1, 1)
        self.tag_row += 1

class SupTag(QWidget):
    add_sup_tag = pyqtSignal(str)
    def __init__(self, font_size):
        super().__init__()
        self.setFixedWidth(300)
        self.layout = QVBoxLayout(self)
        self.add_tag()
        self.submit_button = QPushButton(f"{LanguageDialog().txt_apply()}")  
        self.submit_button.clicked.connect(self.tag_values)
        self.layout.addWidget(self.submit_button)

        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)

    def add_tag(self):
        grid_layout = QGridLayout()
        self.tag_name_fill = QLineEdit()
        grid_layout.addWidget(self.tag_name_fill, 0, 0)
        self.layout.addLayout(grid_layout)

    def tag_values(self):
        tag_names = self.tag_name_fill.text()
        self.add_sup_tag.emit(tag_names)

class SupTagDialog(QDialog):  
    def __init__(self, font_size):
        super().__init__()
        self.setWindowTitle(f"{LanguageDialog().txt_addsuptag()}")
        self.setWindowIcon(QIcon("images/util/add.png"))
        self.font_size = font_size
        self.sup_tag = SupTag(self.font_size)
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.sup_tag)

class FENErrorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{LanguageDialog().txt_error()}")
        self.setWindowIcon(QIcon("images/util/error.png"))
        self.setModal(True)
        self.setMinimumSize(400, 200)
        self.setMaximumSize(400, 200)

        about_label = QLabel(f"{LanguageDialog().txt_fenerror()}")
        about_label.setAlignment(Qt.AlignCenter)
        
        font = QFont()
        font.setPointSize(12)
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

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     form = Form()
#     form.show()
#     sys.exit(app.exec_())
