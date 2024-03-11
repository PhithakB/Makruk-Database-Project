from itertools import chain
import re

def parse(fen_str):
    ranks = fen_str.split(" ")[0].split("/")
    pieces_on_all_ranks = [parse_rank(rank) for rank in ranks]
    fen = generate_fen(pieces_on_all_ranks)
    
    return fen

def parse_rank(rank):
    rank_re = re.compile("(\d|[kmsnrfpKMSNRPF])")
    piece_tokens = rank_re.findall(rank)
    pieces = flatten(map(expand_or_noop, piece_tokens))
    return pieces

def flatten(lst):
    return list(chain(*lst))

def expand_or_noop(piece_str):
    piece_re = re.compile("([kmsfnrpKMSNRPF])")
    retval = ""
    if piece_re.match(piece_str):
      retval = piece_str
    else:
      retval = expand(piece_str)
    return retval

def expand(num_str):
    return int(num_str)*"-"

def generate_fen(chess_board):
    flatten_board = list(chain.from_iterable(chess_board))
         
    fen = "".join(flatten_board)
    
    return fen

def format(board):
    flatten_board = list(chain.from_iterable(board))
    for p in range(len(flatten_board)):
        if flatten_board[p] != '-':
            if flatten_board[p][0] == 'b':
                flatten_board[p] = flatten_board[p][1].lower()
            elif flatten_board[p][0] == 'w':
                flatten_board[p] = flatten_board[p][1].upper()
        fen = "".join(flatten_board)
    
    return fen

def start_board(board):
    ranks = board.split(" ")[0].split("/")
    pieces_on_all_ranks = [parse_rank(rank) for rank in ranks]
    
    for i, row in enumerate(pieces_on_all_ranks):
        for j, value in enumerate(row):
            if value.islower():
                pieces_on_all_ranks[i][j] = f"b{value.upper()}"
            elif value.isupper():
                pieces_on_all_ranks[i][j] = f"w{value.upper()}"
    return pieces_on_all_ranks
