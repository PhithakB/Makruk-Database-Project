from itertools import chain
import re

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

def format(board):
    flatten_board = list(chain.from_iterable(board))
    for p in range(len(flatten_board)):
        if flatten_board[p] != '-':
            if flatten_board[p][0] == 'b':
                flatten_board[p] = flatten_board[p][1].lower()
            else:
                flatten_board[p] = flatten_board[p][1]
    fen = "".join(flatten_board)
    return fen

def start_board(board):
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value.islower():
                board[i][j] = f"b{value.upper()}"
            elif value.isupper():
                board[i][j] = f"w{value.upper()}"
    return board

def generate_fen(chess_board):
    flatten_board = list(chain.from_iterable(chess_board))
    fen = "".join(flatten_board)
    return fen

def color_turn(fen_str):
    for symbol in fen_str:
        if symbol == 'w' or symbol == 'b':
            color = symbol
    return color
