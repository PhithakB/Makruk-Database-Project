from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QDrag, QFont
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from searchByFen import format, start_board
from standardFEN import parse
from language import LanguageDialog

class BoardWindow(QWidget):
    fen_generated = pyqtSignal(str)
    search_button_clicked = pyqtSignal()
    standard_fen = pyqtSignal(str)
    
    def __init__(self, start_fen, font_size):
        super().__init__()
        self.layout = QGridLayout(self)
        self.font_size = font_size
        self.setFixedSize(800, 700)
        self.pos = []
        
        self.start_fen = start_fen
        self.board_position()
        
        self.create_chess_board()
        self.create_info_layout()
        self.create_buttons()

        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
        
    def board_position(self):
        if self.start_fen != '':
            self.pos = start_board(self.start_fen) 
            
    def create_chess_board(self):
        if hasattr(self, 'chess_board'):
            self.chess_board.deleteLater()
        self.chess_board = Board(self.pos, self.font_size)
        self.layout.addWidget(self.chess_board, 0, 0)
        self.chess_board.position_changed.connect(self.update_position)
        
    def create_info_layout(self):
        if hasattr(self, 'info_layout'):
            self.info_layout.deleteLater()
        self.info_layout = Info(self.font_size)
        self.layout.addWidget(self.info_layout, 0, 1)
        
    def create_buttons(self):
        btn_clear = QPushButton(f"{LanguageDialog().txt_clear()}", self)
        btn_clear.setFocusPolicy(Qt.NoFocus)
        btn_clear.clicked.connect(self.clear_board)
        btn_generate = QPushButton(f"{LanguageDialog().txt_ok()}", self)
        btn_generate.setFocusPolicy(Qt.NoFocus)
        btn_generate.clicked.connect(self.on_search_button_clicked)
        
        button_layout = QGridLayout()
        button_layout.addWidget(btn_clear, 0, 0)
        button_layout.addWidget(btn_generate, 1, 0)
        self.layout.addLayout(button_layout, 1, 0)
   
    def on_search_button_clicked(self):
        if self.pos:
            fentosearch = format(self.pos)
            fen_standard = parse(fentosearch)
            
            self.search_button_clicked.emit()
            self.fen_generated.emit(fentosearch)
            self.standard_fen.emit(fen_standard)
        else:
            pass
                
    def clear_board(self):
        self.pos.clear()
        self.start_fen = ''
        self.create_chess_board()
        self.create_info_layout()
            
    def update_position(self, position):
       self.pos = position
              
class Board(QWidget):
    position_changed = pyqtSignal(list)
    
    def __init__(self, start_position, font_size):
        super().__init__()
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setFixedSize(560,560)
        self.position = start_position
        self.draw_squares()
        self.setup()
        self.setAcceptDrops(True)
        self.drag_start_position = None

    def setup(self):
        if self.position :
            for row in range(8):
                for col in range(8):
                    piece = self.position[row][col]
                    square_name = chr(ord('a') + col) + str(8 - row)
                    square = self.findChild(QLabel, square_name)
                    if piece != "-":
                        square.setProperty("piece", piece)
                        square.setPixmap(QPixmap(f"images/pieces/{piece}.png").scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        self.style().polish(square)
                    else:
                        square.setProperty("piece", None)
                        square.clear()
            
    def draw_squares(self):
        for row, rank in enumerate('87654321'):
            for col, file in enumerate('abcdefgh'):
                square = QLabel(self)
                square.setFixedSize(70, 70) 
                square.setObjectName(file + rank)
                square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                if row % 2 == col % 2:
                    square.setStyleSheet('background-color: #F0D9B5')
                else:
                    square.setStyleSheet('background-color: #B58863')
                self.layout.addWidget(square, row, col)
        
    def place_piece(self, row, col, piece):
        square_name = chr(ord('a') + col) + str(8 - row)
        square = self.findChild(QLabel, square_name)
        if square:
            if piece:
                piece_name = piece
                square.setProperty("piece", piece_name)
                square.setPixmap(QPixmap(f"images/pieces/{piece}.png").scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.style().polish(square)
  
    def read_position(self):
        if self.position:
            self.position.clear()
            
        for row in range(8):
            row_data = []
            for col in range(8):
                square_name = chr(ord('a') + col) + str(8 - row)
                square = self.findChild(QLabel, square_name)
                if square:
                    piece = square.property("piece")
                    if piece is not None:
                        row_data.append(piece)
                    else:
                        row_data.append('-')
                else:
                    row_data.append(None)
                    
            self.position.append(row_data)
            
            self.position_changed.emit(self.position)
            
        return self.position
         
    def dragMoveEvent(self, event):
        event.accept()
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        piece_name = event.mimeData().text()
        piece = piece_name 

        drop_position = event.pos()
        child = self.childAt(drop_position)

        if child is not None:
            row, col, _, _ = self.layout.getItemPosition(self.layout.indexOf(child))
            if row != -1 and col != -1:
                
                if hasattr(self, 'current_dragged_piece') and self.current_dragged_piece is not None:
                    old_row, old_col, _, _ = self.layout.getItemPosition(self.layout.indexOf(self.current_dragged_piece))
                    if old_row != -1 and old_col != -1:
                        old_square_name = chr(ord('a') + old_col) + str(8 - old_row)
                        old_square = self.findChild(QLabel, old_square_name)
                        if old_square:
                            old_square.setProperty("piece", None)
                            old_square.clear()

                    self.current_dragged_piece.clear()
                    self.current_dragged_piece = None
                    
                self.place_piece(row, col, piece)
                self.read_position()            
              
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            child = self.childAt(event.pos())
            if child is not None and child.property("piece") is not None:
                self.drag_start_position = event.pos()
                self.current_dragged_piece = child
            else:
                self.drag_start_position = None
                
        if event.button() == Qt.RightButton:
            child = self.childAt(event.pos())
            if child is not None and child.property("piece") is not None:
                row, col, _, _ = self.layout.getItemPosition(self.layout.indexOf(child))
                square_name = chr(ord('a') + col) + str(8 - row)
                square = self.findChild(QLabel, square_name)
                if square:
                    square.setProperty("piece", None)
                    square.clear()
            else:
                self.drag_start_position = None
            
            self.read_position()
                                
    def mouseMoveEvent(self, event):
        if self.drag_start_position is not None and (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.current_dragged_piece.property("piece"))
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)
    
class Info(QWidget):
    def __init__(self, font_size):
        super().__init__()
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.draw_pieces()
        self.setFixedSize(160, 560)

        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
        
    def draw_pieces(self):
        W_pieces = ['wK', 'wM', 'wR', 'wS', 'wN', 'wP', 'wF']
        B_pieces = ['bK', 'bM', 'bR', 'bS', 'bN', 'bP', 'bF']
        for row, piece in enumerate(W_pieces):
            draggable_piece = DraggablePiece(piece)
            self.layout.addWidget(draggable_piece, row, 0)
        for row, piece in enumerate(B_pieces):
            draggable_piece = DraggablePiece(piece)
            self.layout.addWidget(draggable_piece, row, 1)

class DraggablePiece(QLabel):
    def __init__(self, piece, parent=None):
        super().__init__(parent)
        self.piece = piece  
        self.setPixmap(QPixmap(f"images/pieces/{piece}.png").scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(80, 80)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setScaledContents(True)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            self.current_dragged_piece = self
            self.current_dragged_piece_name = self.piece

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.current_dragged_piece_name)
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)