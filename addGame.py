from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTableWidget, QVBoxLayout, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QDialog
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from addGameFormat import format, generate_fen
from standardFEN import parse
from notation import piece_th, rank_th, piece_en, rank_en
from language import LanguageDialog

class BoardWindow(QWidget):
    reload = pyqtSignal(str)
    def __init__(self, turn_board, tag_name, tag_value, db_file_path, font_size):
        super().__init__()
        self.setWindowTitle(f"{LanguageDialog().txt_addgame()}")
        self.setWindowIcon(QIcon("images/util/board.png"))
        self.setFixedSize(1200, 860)
        self.layout = QGridLayout(self)
        self.font_size = font_size
        self.board = turn_board[1]
        self.tag_name = tag_name
        self.tag_value = tag_value
        self.db_file_path = db_file_path
        self.turn = turn_board[0]
        self.all_pos = []
        self.start_end = []
        self.create_chess_board()
        self.create_movelog()
        self.create_submit_button()
        self.result = self.chess_board.result
        self.chess_board.turn.connect(self.color_turn)
        self.chess_board.log.connect(self.move_log.update_movelog)
        self.chess_board.position.connect(self.position_table)
        self.chess_board.log.connect(self.startend_pos)
        self.chess_board.send_result.connect(self.receive_result)
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
        
    def create_chess_board(self):
        if hasattr(self, 'chess_board'):
            self.chess_board.deleteLater()
        self.chess_board = Board(self.board, self.turn)
        self.result = self.chess_board.result
        self.layout.addWidget(self.chess_board, 0, 0)
        
    def create_movelog(self):
        if hasattr(self, 'move_log'):
            self.move_log.deleteLater()
        self.move_log = MoveLog(self.turn, self.font_size)
        self.layout.addWidget(self.move_log, 0, 1)
    
    def create_submit_button(self):
        button_layout = QHBoxLayout()
        self.draw_button = QPushButton(f"{LanguageDialog().txt_draw()}", self)
        self.draw_button.clicked.connect(self.draw_clicked)
        button_layout.addWidget(self.draw_button)
        self.draw_button.setEnabled(False)
        
        self.resign_button = QPushButton(f"{LanguageDialog().txt_resign()}", self)
        self.resign_button.clicked.connect(self.resign_clicked)
        button_layout.addWidget(self.resign_button)
        self.resign_button.setEnabled(False)
        
        self.submit_button = QPushButton(f"{LanguageDialog().txt_apply()}", self)
        self.submit_button.clicked.connect(self.submit_clicked)
        button_layout.addWidget(self.submit_button) 
        self.submit_button.setEnabled(False)
       
        self.generate_button = QPushButton(f"{LanguageDialog().txt_fengen()}", self)
        self.generate_button.clicked.connect(self.generate_clicked)
        button_layout.addWidget(self.generate_button)
        
        lineEdit = QLineEdit()
        lineEdit.setReadOnly(True)
        
        self.layout.addWidget(lineEdit, 1, 1)
        self.layout.addLayout(button_layout, 1, 0)
        
    def submit_clicked(self):
        all_fen = []
        if self.all_pos:
            for i in self.all_pos:
                fen = format(i)
                all_fen.append(fen)
            self.start_pos = []
            self.end_pos = []
            for i in self.start_end:
                self.start_pos.append(i[0])
                self.end_pos.append(i[1])
            
            self.tag_name.append('Result')
            self.tag_value.append(self.result)
            self.comment = []
            fen_start = [generate_fen(format(self.board))]
            from database_insert import main as DatabaseInsert
            DatabaseInsert(self.tag_name, self.tag_value, self.comment, fen_start, self.start_pos, self.end_pos, all_fen, self.db_file_path)
            dialog = ApplySuccess()
            dialog.exec_()
            self.reload.emit(self.db_file_path)
            self.close()

    def draw_clicked(self):
        self.result = "1/2-1/2"
        self.chess_board.checkmate = True
        self.draw_button.setEnabled(False)
        self.resign_button.setEnabled(False)
    
    def resign_clicked(self):
        if self.turn == "w":
            self.result = "0-1"
        elif self.turn == "b":
            self.result = "1-0"
        self.chess_board.checkmate = True
        self.draw_button.setEnabled(False)
        self.resign_button.setEnabled(False)

    def color_turn(self, white_turn):
        if white_turn == True:
            self.turn = "w"
        else:
            self.turn = "b"

    def generate_clicked(self):
        if self.all_pos:
            fen = format(self.all_pos[-1])
            fen_str = parse(fen)
            lineEdit = self.layout.itemAtPosition(1, 1).widget()
            lineEdit.setText(fen_str+" "+self.turn)
        else:
            fen_str = 'rnsmksnr/8/pppppppp/8/8/PPPPPPPP/8/RNSKMSNR'
            lineEdit = self.layout.itemAtPosition(1, 1).widget()
            lineEdit.setText(fen_str+" "+"w")
    
    def position_table(self,current_board):
        self.all_pos = current_board
        if self.all_pos:
            self.submit_button.setEnabled(True)
            if self.chess_board.checkmate:
                self.draw_button.setEnabled(False)
                self.resign_button.setEnabled(False)
            else:
                self.draw_button.setEnabled(True)
                self.resign_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)
            self.draw_button.setEnabled(False)
            self.resign_button.setEnabled(False)
        
    def startend_pos(self, start_end_piece):
        pos = []
        for move in start_end_piece:
            pos.append((move[1],move[2]))
        self.start_end  = pos
    
    def receive_result(self, result):
        self.result = result
        
class Board(QWidget):
    log = pyqtSignal(list)
    position = pyqtSignal(list)
    turn = pyqtSignal(bool)
    send_result = pyqtSignal(str)
    def __init__(self, board, act_turn, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setFocusPolicy(Qt.StrongFocus)
        self.start_board = []
        self.board_start_position(board)
        self.active_turn = act_turn
        self.result = "*"
        self.checkmate = False
        self.stalemate = False
        self.draw_squares()
        self.current_board = []
        self.white = self.turn_check()
        self.selected_piece = None
        self.highlighted_squares = []
        self.start_end_piece = []
        self.move_functions = {'P':self.biamove,  'N':self.mamove, 'R': self.rueamove,
                                'S':self.khonmove, 'M':self.metmove, 'K':self.khunmove, 'F':self.biangaimove}
        self.board = []
        self.setup_board()
        self.wk_location, self.bk_location = self.khunLocation()
        self.isCheckmate()
        
    def turn_check(self):
        if self.active_turn == 'b':
            white = False
        elif self.active_turn == 'w':
            white = True
        return white

    def board_start_position(self, board):
        self.start_board = board

    def draw_squares(self):
        for row, rank in enumerate('87654321'):
            for col, file in enumerate('abcdefgh'):
                square = QLabel(self)
                square.setFixedSize(100, 100)
                square.setObjectName(file + rank)
                if row % 2 == col % 2:
                    square.setStyleSheet('background-color: #F0D9B5')
                else:
                    square.setStyleSheet('background-color: #B58863')
                self.layout.addWidget(square, row, col)

    def setup_board(self):
        if self.board:
            for row in range(8):
                for col in range(8):
                    piece = self.board[row][col]
                    square_name = chr(col + ord('a')) + str(8 - row)
                    square = self.findChild(QLabel, square_name)
                    if piece != "-":
                        square.setProperty("piece", piece)
                        square.setPixmap(QPixmap(f"images/pieces/{piece}.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        self.style().polish(square)
                    else:
                        square.setProperty("piece", None)
                        square.clear() 
        else:
            if self.start_board:
                board = self.start_board
            else:
                board = [
                ["bR","bN","bS","bM","bK","bS","bN","bR"],
                ["-","-","-","-","-","-","-","-"],
                ["bP","bP","bP","bP","bP","bP","bP","bP"],
                ["-","-","-","-","-","-","-","-"],
                ["-","-","-","-","-","-","-","-"],
                ["wP","wP","wP","wP","wP","wP","wP","wP"],
                ["-","-","-","-","-","-","-","-"],
                ["wR","wN","wS","wK","wM","wS","wN","wR"]
            ]
                
            for row in range(8):
                for col in range(8):
                    piece = board[row][col]
                    square_name = chr(col + ord('a')) + str(8 - row)
                    square = self.findChild(QLabel, square_name)
                    if piece != "-":
                        square.setProperty("piece", piece)
                        square.setPixmap(QPixmap(f"images/pieces/{piece}.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        self.style().polish(square)
                    else:
                        square.setProperty("piece", None)
                        square.clear()

    def mousePressEvent(self, event):
        if not self.checkmate and not self.stalemate:
            if event.button() == Qt.LeftButton:
                child = self.childAt(event.pos())
                if isinstance(child, QLabel):
                    piece = child.property("piece")
                    squarename = child.objectName()
                    
                    if self.white:
                        if piece is not None and piece[0] != 'b':
                            self.clearHighlightedSquares()
                            self.possibleMove(child)
                            self.selected_piece = child
                            
                        elif self.highlighted_squares:
                            target_square = self.findChild(QLabel, squarename)
                            if target_square in self.highlighted_squares:
                                self.movePiece(target_square)
                                self.read_position()
                                return
                    else:
                        if piece is not None and piece[0] != 'w':
                            self.clearHighlightedSquares()
                            self.possibleMove(child)
                            self.selected_piece = child
                            
                        elif self.highlighted_squares:
                            target_square = self.findChild(QLabel, squarename)
                            if target_square in self.highlighted_squares:
                                self.movePiece(target_square)
                                self.read_position()
                                return
    
    def isCheckmate(self):
        self.validMove()
        if self.checkmate :          
            if self.white :
                self.result = "0-1"
            elif not self.white:
                self.result = "1-0"
        elif self.stalemate:
            self.result = "1/2-1/2"
        self.send_result.emit(self.result)
        
    def movePiece(self, target_square):
        piece_label = self.selected_piece
        start_name = piece_label.objectName()
        piece = piece_label.property("piece")
        sqrname = target_square.objectName()
        if target_square.property("piece") is not None:
            operation = 'x'
        else:
            operation = '-'
        if (piece == 'bP'and sqrname[1] == '3') or (piece == 'wP'and sqrname[1] == '6') :
            self.check_promote(piece_label, target_square, operation)
        else: 
            if piece == "wK":
                self.wk_location = sqrname
            elif piece == "bK":
                self.bk_location = sqrname
            target_square.setProperty("piece", piece)
            target_square.setPixmap(QPixmap(f"images/pieces/{piece}.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            piece_label.setProperty("piece", None)
            piece_label.clear()
            self.move_log(start_name, target_square, operation)
            self.clearHighlightedSquares()
            self.selected_piece = None                
     
    def isPinAndCheck(self):
        pins = []
        checks = []
        in_check = False
        if self.white:
            enemy_color = "b"
            ally_color = "w"
            k_file = self.wk_location[0]
            k_rank = self.wk_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            k_file = self.bk_location[0]
            k_rank = self.bk_location[1]
        
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, -1),(-1, 1) , (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = () 
            for i in range(1,8):
                end_file = chr(ord(k_file) + direction[0]* i)
                end_rank = int(k_rank) + direction[1] * i
                if "a" <= end_file <= "h" and 1 <= end_rank <= 8:
                    square = self.findChild(QLabel, end_file+str(end_rank))
                    if square and square.property("piece") is not None:
                        piece = square.property("piece")
                        if piece[0] == ally_color and piece[1] != 'K':
                            if possible_pin ==():
                                possible_pin = (end_file, str(end_rank), direction[0], direction[1])
                            else: 
                                break
                        elif piece[0] == enemy_color:
                            enemy_type = piece[1]
                            if (0 <= j <= 3 and enemy_type == "R") or (
                                i == 1 and enemy_type == "P" and ((enemy_color == "b" and 6 <= j <= 7) or (enemy_color == "w" and 4 <= j <= 5))) or (i == 1 and (enemy_type in "MFS") and 4 <= j <= 7) or (
                                i == 1 and enemy_type == "S" and ((enemy_color == "b" and  j == 3) or (enemy_color == "w" and j == 1))) or (i == 1 and enemy_type == "K"):
                                if possible_pin == ():  # no piece blocking, so check
                                    in_check = True
                                    checks.append((end_file, str(end_rank), direction[0], direction[1]))
                                    break
                                else:
                                    pins.append(possible_pin)
                                    break
                            else:
                                break
                else:
                    break
        
        ma_move = [(-1, 2),(2,-1),(1,2),(2,1),(-2,1),(1,-2),(-2,-1),(-1,-2)]
        for x,y in ma_move:
            file = chr(ord(k_file) + y)
            rank = int(k_rank) + x 
            if  "a"  <= file <= "h" and  0 < rank <= 8:
                square = self.findChild(QLabel, file+str(rank))
                if square and square.property("piece") is not None:
                    piece = square.property("piece")
                    if piece[0] == enemy_color and piece[1] =="N":
                        in_check = True
                        checks.append((file, str(rank), x, y))
        return in_check, pins , checks
    
    def validMove(self):
        if self.white:
            k_rank = self.wk_location[1]
            k_file = self.wk_location[0]
        else:
            k_rank = self.bk_location[1]
            k_file = self.bk_location[0]
        self.in_check, self.pins, self.checks = self.isPinAndCheck()

        if self.in_check:
            if len(self.checks) == 1:
                moves = self.allPossibleMoves()
                valid_squares = []
                check = self.checks[0]
                check_file = check[0]
                check_rank = check[1]
                square = self.findChild(QLabel, check_file+check_rank)
                piece = square.property("piece")
                
                if piece[1] in "NPSMF":
                    valid_squares = [check_file+check_rank]
                else:
                    for i in range(1,8):
                        file = chr(ord(k_file) + check[2]* i)
                        rank = int(k_rank) + check[3] * i
                        valid_squares.append(file+str(rank))
                        if file == check_file and str(rank) == check_rank:
                            break
               
                for i in range(len(moves) - 1, -1, -1):  
                    if moves[i][2] != "K":
                        if not (moves[i][1][0]+moves[i][1][1]) in valid_squares:
                            moves.remove(moves[i])
            else:
                self.khunmove(k_rank+k_file, moves)
        else:
            moves = self.allPossibleMoves()
        
        if len(moves) == 0:
            if self.isCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return moves
               
    def allPossibleMoves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                square_name = chr(ord('a') + col) + str(8 - row)
                square = self.findChild(QLabel, square_name)
                if square and square.property("piece") is not None:
                    piece = square.property("piece")
                    if (piece[0] == "w" and self.white) or (piece[0] == "b" and not self.white):
                        self.move_functions[piece[1]](square.objectName(), moves)
        return moves        
    
    def underAttack(self, sqr):
        self.white = not self.white
        opponents_moves = self.allPossibleMoves()
        self.white = not self.white
        for move in opponents_moves:
            if move[1][0] == sqr[0] and move[1][1] == sqr[1]:
                return True
        return False
    
    def khunLocation(self):
        for row in range(8):
            for col in range(8):
                square_name = chr(ord('a') + col) + str(8 - row)
                square = self.findChild(QLabel, square_name)
                if square:
                    piece = square.property("piece")
                    if piece == "wK":
                        wk_location = square_name
                    elif piece == "bK":
                        bk_location = square_name
        return wk_location, bk_location
    
    def isCheck(self):
        if self.white:
            return self.underAttack(self.wk_location)
        else:
            return self.underAttack(self.bk_location)
  
    def highlight(self, targetSqr):
        sqr = self.findChild(QLabel, targetSqr)
        sqr.setStyleSheet('background-color: #e06960;')
        self.highlighted_squares.append(sqr)

    def clearHighlightedSquares(self):
        for sqr in self.highlighted_squares:
            squre_name = sqr.objectName()
            if (squre_name[0] in "aceg" and squre_name[1] in "1357") or (squre_name[0] in "bdfh" and squre_name[1] in "2468"):
                sqr.setStyleSheet('background-color: #B58863')
            else:
                sqr.setStyleSheet('background-color: #F0D9B5')
        self.highlighted_squares = []

    def possibleMove(self, square):
        square_name = square.objectName()
        all_move = self.validMove()
        
        for move in all_move:
            if move[0] == square_name:
                self.highlight(move[1])
        
    def mamove(self, sqr, moves):
        ma_move = [(-1, 2),(2,-1),(1,2),(2,1),(-2,1),(1,-2),(-2,-1),(-1,-2)]
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == sqr[0] and self.pins[i][1] == sqr[1]:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        ally_color = "w" if self.white else "b"
        for x,y in ma_move:
            file = chr(ord(sqr[0]) + y)
            rank = int(sqr[1]) + x
            if "a"  <= file < "i" and 0 < rank <= 8:
                if not piece_pinned:
                    squre = self.findChild(QLabel, file+str(rank))
                    if squre.property("piece") is not None:
                        piece = squre.property("piece")
                        if piece[0] != ally_color:
                                moves.append((sqr,file+str(rank),"N"))
                    else:
                        moves.append((sqr,file+str(rank),"N"))

    def rueamove(self, sqr, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == sqr[0] and self.pins[i][1] == sqr[1]:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = "b" if self.white else "w" 
        for direction in directions:
            for i in range(1,8):
                file = chr(ord(sqr[0]) + direction[0] * i)
                rank = int(sqr[1]) + direction[1] * i
                if  "a"  <= file < "i" and 0 < rank <= 8:
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        squre = self.findChild(QLabel, file+str(rank))
                        if squre.property("piece") is not None:
                            piece = squre.property("piece")
                            if piece[0] == enemy_color:
                                moves.append((sqr,file+str(rank),"R"))
                                break
                            else:
                                break
                        else:
                            moves.append((sqr,file+str(rank),"R"))
                else:
                    break
    
    def biamove(self, sqr , moves):
        move = [-1 , 1]
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == sqr[0] and self.pins[i][1] == sqr[1]:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        
        enemy_color = "b" if self.white else "w"
        y = 1 if enemy_color == 'b' else -1
        for x in move:
            file = chr(ord(sqr[0]) + x)
            rank = int(sqr[1]) + y
            if "a"  <= file < "i" and 0 < rank <= 8:
                if not piece_pinned:
                    target = self.findChild(QLabel, file+str(rank))
                    if target.property("piece") is not None:
                        piece = target.property("piece")
                        if piece[0] == enemy_color:
                            moves.append((sqr,file+str(rank),"P"))
                    else:
                        pass
        if not piece_pinned:      
            target = self.findChild(QLabel, sqr[0]+str(int(sqr[1])+y))
            if target.property("piece") is not None:
                pass
            else:
                moves.append((sqr,sqr[0]+str(int(sqr[1])+y), "P"))
        
    def metmove(self,sqr, moves): 
        move = [(1,1),(1,-1),(-1,1),(-1,-1)]
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == sqr[0] and self.pins[i][1] == sqr[1]:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        
        enemy_color = "b" if self.white else "w"
        for x,y in move:
            file = chr(ord(sqr[0]) + y)
            rank = int(sqr[1]) + x
            if "a"  <= file < "i" and 0 < rank <= 8:
                if not piece_pinned:
                    squre = self.findChild(QLabel, file+str(rank))
                    if squre.property("piece") is not None:
                        piece = squre.property("piece")
                        if piece[0] == enemy_color:
                                moves.append((sqr,file+str(rank), "M"))
                    else:
                        moves.append((sqr,file+str(rank), "M"))
        
    def khunmove(self, sqr, moves):
        move = [(1,1),(1,-1),(-1,1),(-1,-1),(0,1),(0,-1),(-1,0),(1,0)]
        ally_color = "w" if self.white else "b"
        for x,y in move:
            file = chr(ord(sqr[0]) + y)
            rank = int(sqr[1]) + x
            if "a"  <= file < "i" and 0 < rank <= 8:
                squre = self.findChild(QLabel, file+str(rank))
                if squre:
                    if squre.property("piece") is not None:
                        piece = squre.property("piece")
                        if piece[0] != ally_color:
                            if ally_color == 'w':
                                self.wk_location = file+str(rank)
                            else:
                                self.bk_location = file+str(rank)
                            
                            in_check, pins, checks = self.isPinAndCheck()
                            if not in_check:
                                moves.append((sqr,file+str(rank), "K"))
                                
                            if ally_color == 'w':
                                self.wk_location = sqr[0]+sqr[1]
                            else:
                                self.bk_location = sqr[0]+sqr[1]
                            
                    else:
                        if ally_color == 'w':
                            self.wk_location = file+str(rank)
                        else:
                            self.bk_location = file+str(rank)
                            
                        in_check, pins, checks = self.isPinAndCheck()
                        if not in_check:
                            moves.append((sqr,file+str(rank), "K"))
                            
                        if ally_color == 'w':
                            self.wk_location = sqr[0]+sqr[1]
                        else:
                            self.bk_location = sqr[0]+sqr[1]
                    
    def khonmove(self, sqr, moves):
        move = [(1,1),(1,-1),(-1,1),(-1,-1)]
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == sqr[0] and self.pins[i][1] == sqr[1]:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        
        enemy_color = "b" if self.white else "w"
        for x,y in move:
            file = chr(ord(sqr[0]) + y)
            rank = int(sqr[1]) + x
            if "a"  <= file < "i" and 0 < rank <= 8:
                if not piece_pinned:
                    squre = self.findChild(QLabel, file+str(rank))
                    if squre.property("piece") is not None:
                        piece = squre.property("piece")
                        if piece[0] == enemy_color:
                                moves.append((sqr,file+str(rank), "S"))
                    else:
                        moves.append((sqr,file+str(rank), "S"))
        i = 1 if enemy_color == "b" else -1
        if not piece_pinned:
            target = self.findChild(QLabel, sqr[0]+str(int(sqr[1])+i))
            if target.property("piece") is not None:
                piece = target.property("piece")
                if piece[0] == enemy_color:
                    moves.append((sqr,file+str(rank), "S"))
            else:
                moves.append((sqr,sqr[0]+str(int(sqr[1])+i), "S"))
         
    def biangaimove(self, sqr, moves):
        move = [(1,1),(1,-1),(-1,1),(-1,-1)]
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == sqr[0] and self.pins[i][1] == sqr[1]:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        
        enemy_color = "b" if self.white else "w"
        for x,y in move:
            file = chr(ord(sqr[0]) + y)
            rank = int(sqr[1]) + x
            if "a"  <= file < "i" and 0 < rank <= 8:
                if not piece_pinned:
                    squre = self.findChild(QLabel, file+str(rank))
                    if squre.property("piece") is not None:
                        piece = squre.property("piece")
                        if piece[0] == enemy_color:
                                moves.append((sqr,file+str(rank), "F"))
                    else:
                        moves.append((sqr,file+str(rank), "F"))

    def check_promote(self, piece_label, target_square, operation):
        piece = piece_label.property("piece")
        start_name = piece_label.objectName()
        if piece[0] == 'b':
            piece = "bF"
            target_square.setProperty("piece", piece)
            target_square.setPixmap(QPixmap(f"images/pieces/{piece}.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            piece_label.setProperty("piece", None)
            piece_label.clear()  # Clear the original square
            self.move_log(start_name, target_square, operation)
            self.clearHighlightedSquares()  # Clear highlighted squares
            self.selected_piece = None  # Reset selected piece
                
        if piece[0] == 'w':
            piece = "wF"
            target_square.setProperty("piece", piece)
            target_square.setPixmap(QPixmap(f"images/pieces/{piece}.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            piece_label.setProperty("piece", None)
            piece_label.clear()  # Clear the original square
            self.move_log(start_name, target_square, operation)
            self.clearHighlightedSquares()  # Clear highlighted squares
            self.selected_piece = None  # Reset selected piece
    
    def move_log(self,startsqr, endsqr, operation):
        start = startsqr
        end = endsqr.objectName()
        piece = endsqr.property("piece")
        
        self.white = not self.white
        self.isCheckmate()
        if self.checkmate:
            check_symbol = "++"
        else:
            if self.isCheck():
                check_symbol = "+"
            else:
                check_symbol = ""
        self.turn.emit(self.white)
        self.start_end_piece.append((piece,start,end, operation, check_symbol)) 
        self.log.emit(self.start_end_piece)

    def read_position(self):
        position = []
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
            position.append(row_data)
        self.current_board.append(position)
        self.position.emit(self.current_board) 
            
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Z:
            if self.highlighted_squares:
                pass
            else:
                self.undo()
        if key == Qt.Key_R:
            if self.highlighted_squares:
                pass
            else:
                self.reset_game()    
                
    def undo(self):
        if self.current_board:
            self.current_board.pop()
            self.position.emit(self.current_board)
            self.start_end_piece.pop()
            self.log.emit(self.start_end_piece)
            if self.current_board:
                if self.checkmate:
                    self.checkmate = not self.checkmate
                elif self.stalemate:
                    self.stalemate = not self.checkmate
                self.result = "*"
                self.board = self.current_board[-1]
                self.selected_piece = None
                self.white = not self.white
                self.isCheckmate()
                self.turn.emit(self.white)
                self.send_result.emit(self.result)
                self.setup_board()
            else:
                self.reset_game()
  
    def reset_game(self):
        self.current_board = []
        self.board = []
        if self.checkmate:
            self.checkmate = not self.checkmate
        elif self.stalemate:
            self.stalemate = not self.checkmate
        self.result = "*"
        self.white = self.turn_check()
        self.selected_piece = None
        self.highlighted_squares = []
        self.start_end_piece = []
        self.setup_board()
        self.isCheckmate()
        self.turn.emit(self.white)
        self.log.emit(self.start_end_piece)
        self.position.emit(self.current_board)
        self.send_result.emit(self.result)
        
class MoveLog(QWidget):
    def __init__(self, turn, font_size):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.font_size = font_size
        self.log_table()
        self.turn = turn
        self.move_log = []
        font = QFont()
        font.setPointSize(font_size)
        self.setFont(font)
        
    def update_movelog(self,start_end_piece):
        if self.turn == 'b':
            new_log = [('')]
            self.move_log = new_log + start_end_piece
        else:
            self.move_log = start_end_piece
        self.movelog.setRowCount(0)
        self.movelog.setColumnWidth(0, 50)
        self.add_to_table()
        
    def log_table(self):
        self.movelog = QTableWidget(self)
        app_font = self.movelog.font()
        app_font.setPointSize(self.font_size)
        self.movelog.horizontalHeader().setFont(app_font)
        self.movelog.verticalHeader().setVisible(False)
        self.movelog.setColumnCount(3)
        self.movelog.setRowCount(0)
        self.movelog.setColumnWidth(0, 50)
        column_names = ["",f"{LanguageDialog().txt_whitemove()}", f"{LanguageDialog().txt_blackmove()}"]
        self.movelog.setHorizontalHeaderLabels(column_names)
        self.layout.addWidget(self.movelog)

    def add_to_table(self):
        if self.move_log:
            move_number = len(self.move_log)
            if move_number % 2 != 0:
                rowsCount = (move_number + 1) // 2
            else:
                rowsCount = move_number // 2
            self.movelog.setRowCount(rowsCount)
            for move in range(move_number):
                if self.move_log[move] == '':
                    item = ''
                else:
                    piece = self.move_log[move][0][1]
                    start = self.move_log[move][1]
                    end = self.move_log[move][2]
                    operation = self.move_log[move][3]
                    symbol = self.move_log[move][4]

                    if LanguageDialog().default_lang == 'th':
                        item = piece_th[piece]+','+rank_th[start[0]]+start[1]+operation+rank_th[end[0]]+end[1]+symbol
                    else:
                        if piece == "P":
                            item = piece_en[piece]+rank_en[start[0]]+start[1]+operation+rank_en[end[0]]+end[1]+symbol
                        else:
                            item = piece_en[piece]+','+rank_en[start[0]]+start[1]+operation+rank_en[end[0]]+end[1]+symbol
                row = move//2
                col = (move%2)+1
                self.movelog.setItem(row, 0, QTableWidgetItem(str(row+1)))
                self.movelog.setItem(row, col, QTableWidgetItem(str(item)))
               
class ApplySuccess(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{LanguageDialog().txt_applysuccess()}")
        self.setWindowIcon(QIcon("images/util/accept.png"))
        self.setModal(True)
        self.setMinimumSize(400, 200)
        self.setMaximumSize(400, 200)
        about_label = QLabel(f"{LanguageDialog().txt_applysuccess()}")
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
