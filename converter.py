import re
from itertools import chain

move = []
tag_n = []
tag_v = []
comm = []

def parse(fen_str):
    ranks = fen_str.split(" ")[0].split("/")
    pieces_on_all_ranks = [parse_rank(rank) for rank in ranks]
    return pieces_on_all_ranks

def parse_rank(rank):
    rank_re = re.compile("(\d|[kmsnrpKMSNRP])")
    piece_tokens = rank_re.findall(rank)
    pieces = flatten(map(expand_or_noop, piece_tokens))
    return pieces

def flatten(lst):
    return list(chain(*lst))

def expand_or_noop(piece_str):
    piece_re = re.compile("([kmsnrpKMSNRP])")
    retval = ""
    if piece_re.match(piece_str):
      retval = piece_str
    else:
      retval = expand(piece_str)
    return retval

def expand(num_str):
    return int(num_str)*"-"

def replace_moves(moves, tag_name, tag_value, exact_real_comment):
    for m in range(len(moves)):
        if "B" in moves[m]:
            v = moves[m].replace("B", "S")
            move.append(v)
        elif "Q" in moves[m]:
            v = moves[m].replace("Q", "M")
            move.append(v)
        else:
            move.append(moves[m])
    for i in tag_name:
        tag_n.append(i)
    for j in tag_value:
        tag_v.append(j)
    for k in exact_real_comment:
        comm.append(k)

endPosition = []
startPosition = []
start_pos = []
fen_result = []
fen_start = []

def draw_board(tag_name, tag_value):
    algebragic_pattern = re.compile(r'[a-h][1-8]')
    skip_pattern = re.compile(r'[skip]')
    matches_list = []
    for algebragic in move:
        match = re.search(algebragic_pattern, algebragic)
        skip_match = re.search(skip_pattern, algebragic)
        if match:
            matches_list.append(match.group())
        elif skip_match:
            matches_list.append("skip")

    if matches_list:
        for i in matches_list:
            endPosition.append(i)
        
    BOARD_SIZE = 8

    for i in range(len(tag_name)):
        if tag_name[i] == 'FEN':
            value = tag_value[i]

    if "FEN" in tag_name:
        board = parse(value)
    else:
        board = [
                    ["r", "n", "s", "m", "k", "s", "n", "r"],
                    ["-", "-", "-", "-", "-", "-", "-", "-"],
                    ["p", "p", "p", "p", "p", "p", "p", "p"],
                    ["-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-"],
                    ["P", "P", "P", "P", "P", "P", "P", "P"],
                    ["-", "-", "-", "-", "-", "-", "-", "-"],
                    ["R", "N", "S", "K", "M", "S", "N", "R"],
                ]
    
    return BOARD_SIZE, board

def get_piece(move):
    pieces = []
    pieces_pattern = re.compile(r'[RNKMS]')
    promote_pattern = re.compile(r'[P][a-h]')
    skip_pattern = re.compile(r'[skip]')
    matches_list = []

    for piece in move:
        match = re.search(pieces_pattern, piece)
        promote_match = re.search(promote_pattern, piece)
        skip_match = re.search(skip_pattern, piece)
        if match:
            matches_list.append(match.group())
        elif promote_match:
            matches_list.append("F")
        elif skip_match:
            matches_list.append("skip")
        else:
            matches_list.append("P")
    
    if matches_list:
        pieces = matches_list

    return pieces

def convert_position(endPosition):
    ends = []
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    
    for i in range(len(endPosition)):
        if endPosition[i] == "skip":
            ends.append("skip")
        else:
            x = ranksToRows[endPosition[i][1]] 
            y = filesToCols[endPosition[i][0]]
            ends.append((x, y))
        
    return ends

def convert_alge(start_pos):
    rowsToRanks = { 7: "1", 6: "2", 5: "3", 4: "4",
                    3: "5", 2: "6", 1: "7", 0: "8"}

    colsToFiles = { 0: "a", 1: "b", 2: "c", 3: "d",
                    4: "e", 5: "f", 6: "g", 7: "h"}

    for i in range(len(start_pos)):
        if start_pos[i] == "skip":
            startPosition.append("skip")
        else:
            start = colsToFiles[start_pos[i][1]] + rowsToRanks[start_pos[i][0]] 
            startPosition.append(start)

def check_move(i, pre_start, pieces):
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    s = move[i]
    s1 = s.replace(pieces[i], '')
    s2 = s1.replace(endPosition[i], '')
    locate = s2[:1]
    col, row = 0, 0
    
    if locate.isnumeric():
        rows = ranksToRows[locate]
        for v in pre_start:
            if v[0] == rows:
                col, row = v[1], v[0]
    elif locate.isalpha():
        cols = filesToCols[locate]
        for v in pre_start:
            if v[1] == cols:
                col, row = v[1], v[0]
    return (row, col)

def promote(i, piece, start_pos ,board):
    if "=P" in move[i] or "=M" in move[i]:
        piece = "F"
    else:
        piece = board[start_pos[i][0]][start_pos[i][1]]
    return piece

def generate_fen(chess_board):
    flatten_board = list(chain.from_iterable(chess_board))
    fen = "".join(flatten_board)
    return fen

def find_start_pos(i, possible_move, x , y , piece, pieces, board):
    pre_start = []
    if i%2 == 0:
        color = "white"
    elif i%2 != 0:
        color = "black"
    if color == "white":
        for k in possible_move:
            b_x = k[0]
            b_y = k[1]
            if piece == "M":
                if board[b_x][b_y] == piece or board[b_x][b_y] == "F" : 
                    pre_start.append((b_x, b_y))
            elif board[b_x][b_y] == piece: 
                pre_start.append((b_x, b_y))
        if len(pre_start) == 1:
            start_pos.append((pre_start[0]))
            board[x][y] = promote(i, piece, start_pos, board)
            board[pre_start[0][0]][pre_start[0][1]] = "-"
        else:
            start_pos.append(check_move(i, pre_start, pieces))
            board[x][y] = promote(i, piece, start_pos, board)
            board[start_pos[i][0]][start_pos[i][1]] = "-"
    elif color == "black":
        for k in possible_move:
            b_x = k[0]
            b_y = k[1]    
            if piece == "M":
                if board[b_x][b_y] == piece.lower() or board[b_x][b_y] == "f": 
                    pre_start.append((b_x, b_y))
            elif board[b_x][b_y] == piece.lower(): 
                pre_start.append((b_x, b_y))
        if len(pre_start) == 1:
            start_pos.append((pre_start[0]))
            board[x][y] = promote(i, piece, start_pos, board).lower()
            board[pre_start[0][0]][pre_start[0][1]] = "-"
        else:
            start_pos.append(check_move(i, pre_start, pieces))
            board[x][y] = promote(i, piece, start_pos, board).lower()
            board[start_pos[i][0]][start_pos[i][1]] = "-"
    pre_start.clear()
    possible_move.clear()   
    fen = generate_fen(board)
    fen_result.append(fen)

def find_pos(board, end_pos, pieces, BOARD_SIZE):
    fen_start.append(generate_fen(board))
    if pieces[0] == "skip" and end_pos[0] == "skip":
        start_pos.append("skip")
        index = 1
    else:
        index = 0
    for i in range(index, len(pieces)):
        possible_move = []
        if pieces[i] == "skip" and end_pos[i] == "skip":
            color = "black"
            skip_pos = end_pos[i]
            x = skip_pos[0]
            y = skip_pos[1]
        else:
            x = end_pos[i][0]
            y = end_pos[i][1]
        if i%2 == 0:
            color = "white"
        elif i%2 != 0:
            color = "black"
        
        def N_move_check():
            N_move =[(x+2, y-1) ,(x+2, y+1) ,(x-2, y+1) ,(x-2, y-1) ,(x+1, y+2) ,(x+1, y-2) ,(x-1, y+2) ,(x-1, y-2)]
            
            for j in N_move:
                if j[0] > 7 or j[1] > 7:
                    pass
                else:
                    possible_move.append(j)
                    
            find_start_pos(i, possible_move, x, y, "N", pieces, board)
        
        def B_move_check():
            B_move =[(x+1, y+1) ,(x-1, y+1) ,(x-1, y-1) ,(x+1, y-1)]
            if color == "white":
                B_move.append((x+1, y))
            elif color == "black":
                B_move.append((x-1, y))
            
            for j in B_move:
                if j[0] > 7 or j[1] > 7:
                    pass
                else:
                    possible_move.append(j)
                    
            find_start_pos(i, possible_move, x, y, "S", pieces, board)

        def Q_move_check():
            Q_move =[(x+1, y+1) ,(x-1, y+1) ,(x-1, y-1) ,(x+1, y-1) ]
            
            for j in Q_move:
                if j[0] > 7 or j[1] > 7:
                    pass
                else:
                    possible_move.append(j)
            
            find_start_pos(i, possible_move, x, y, "M", pieces, board)
                    
        def K_move_check():
            K_move =[(x, y+1) , (x+1, y+1) , (x-1, y+1) , (x-1, y) , (x+1, y) , (x+1, y-1) , (x-1, y-1) , (x, y-1) ]
            
            for j in K_move:
                if j[0] > 7 or j[1] > 7:
                    pass
                else:
                    possible_move.append(j)
            
            find_start_pos(i, possible_move, x, y, "K", pieces, board)

        def R_move_check():
            R_move = []
            for j in range(1, BOARD_SIZE):
                if color == "white" and (x+j < 8 and y < 8):
                    if board[x+j][y] == '-':
                        R_move.append((x+j, y))
                    elif board[x+j][y].isalpha():
                        R_move.append((x+j, y))
                        break

                elif color == "black" and (x+j < 8 and y < 8):
                    if board[x+j][y] == '-':
                        R_move.append((x+j, y))
                    elif board[x+j][y].isalpha():
                        R_move.append((x+j, y))
                        break

            for j in range(1, BOARD_SIZE):
                if color == "white" and (x-j < 8 and y < 8):
                    if board[x-j][y] == '-':
                        R_move.append((x-j, y))
                    elif board[x-j][y].isalpha():
                        R_move.append((x-j, y))
                        break

                elif color == "black" and (x-j < 8 and y < 8):
                    if board[x-j][y] == '-':
                        R_move.append((x-j, y))
                    elif board[x-j][y].isalpha():
                        R_move.append((x-j, y))
                        break

            for j in range(1, BOARD_SIZE):
                if color == "white" and (x < 8 and y-j < 8):
                    if board[x][y-j] == '-':
                        R_move.append((x, y-j))
                    elif board[x][y-j].isalpha():
                        R_move.append((x, y-j))
                        break
                    
                elif color == "black" and (x < 8 and y-j < 8):
                    if board[x][y-j] == '-':
                        R_move.append((x, y-j))
                    elif board[x][y-j].isalpha():
                        R_move.append((x, y-j))
                        break

            for j in range(1, BOARD_SIZE):
                if color == "white" and (x < 8 and y+j < 8):
                    if board[x][y+j] == '-':
                        R_move.append((x, y+j))
                    elif board[x][y+j].isalpha():
                        R_move.append((x, y+j))
                        break

                elif color == "black" and (x < 8 and y+j < 8):
                    if board[x][y+j] == '-':
                        R_move.append((x, y+j))
                    elif board[x][y+j].isalpha():
                        R_move.append((x, y+j))
                        break  

            for v in R_move:
                if v[0] < 0 or v[1] < 0:
                        pass
                else:
                    possible_move.append(v)
            find_start_pos(i,  possible_move, x, y, "R", pieces, board)

        def P_move_check():
            P_move = []
            if color == 'white':
                if "x" in move[i]:
                    P_move = [(x+1, y+1), (x+1, y-1)]
                else:
                    P_move = [(x+1, y)]
            elif color == 'black':
                if "x" in move[i]:
                    P_move = [(x-1, y+1), (x-1, y-1)]
                else:
                    P_move = [(x-1, y)]

            for j in P_move:
                if j[0] > 7 or j[1] > 7:
                    pass
                else:
                    possible_move.append(j)
            find_start_pos(i, possible_move, x, y, "P", pieces, board)  
       
        def F_move_check():
            F_move =[(x+1, y+1) ,(x-1, y+1) ,(x-1, y-1) ,(x+1, y-1) ]
            
            for j in F_move:
                if j[0] > 7 or j[1] > 7:
                    pass
                else:
                    possible_move.append(j)
            find_start_pos(i, possible_move, x, y, "F", pieces, board)

        if pieces[i] == "N":
            N_move_check()
        elif pieces[i] == "S":
            B_move_check()
        elif pieces[i] == "M":
            Q_move_check()
        elif pieces[i] == "K":
            K_move_check()
        elif pieces[i] == "R":
            R_move_check()
        elif pieces[i] == "P":
            P_move_check()
        elif pieces[i] == "F":
            F_move_check()

def main(moves, tag_name, tag_value, exact_real_comment, db_file_path):
    replace_moves(moves, tag_name, tag_value, exact_real_comment)
    BOARD_SIZE, board = draw_board(tag_name, tag_value)
    pieces = get_piece(move)
    end_pos = convert_position(endPosition)
    find_pos(board, end_pos, pieces, BOARD_SIZE)
    convert_alge(start_pos)
    from database_insert import main as DatabaseInsert
    DatabaseInsert(tag_n, tag_v, comm, fen_start, startPosition, endPosition, fen_result, db_file_path)
    move.clear()
    tag_n.clear()
    tag_v.clear()
    comm.clear()
    endPosition.clear()
    startPosition.clear()
    start_pos.clear()
    fen_result.clear()
    fen_start.clear()

if __name__ == '__main__':
    main()