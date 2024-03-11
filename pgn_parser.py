from antlr4 import *
from PGNLexer import PGNLexer
from PGNParser import PGNParser

tag_name = []
tag_value = []
moves = []
gameEnd = []
comment = []
move_number = []
real_comment = []
exact_real_comment = []

def process_move(ctx):
    rule_index = PGNParser.ruleNames[ctx.getRuleIndex()]

    if rule_index == "tag_name":
        tag_name.append(ctx.getText())
    elif rule_index == "tag_value":
        tag_value.append(ctx.getText())
    elif rule_index == "san_move":
        moves.append(ctx.getText())
    elif rule_index == "move_number_indication":
        move_number.append(ctx.getText())
    elif rule_index == "comment":
        comment.append((move_number[-1], ctx.getText()))
    elif rule_index == "game_termination":
        gameEnd.append(ctx.getText())

def traverse_tree(ctx, func):
    func(ctx)
    for child in ctx.children:
        if isinstance(child, RuleContext):
            traverse_tree(child, func)

def find_move():
    for i in comment:
        if "..." in i[0]:
            move_id = i[0].replace(".", "")
            move_id = int(move_id) * 2
            real_comment.append((move_id, i[1]))
        else:
            move_id = i[0].replace(".", "")
            move_id = (int(move_id) * 2) - 1
            real_comment.append((move_id, i[1]))

def del_bracket(og_string):
    return og_string.replace('\n', '')

def main(pgn_selected, db_file_path):
    input_stream = InputStream(pgn_selected)
    lexer = PGNLexer(input_stream)
    token_stream = CommonTokenStream(lexer)

    parser = PGNParser(token_stream)
    tree = parser.pgn_game()

    traverse_tree(tree, process_move)

    find_move()

    for index, element in real_comment:
        exact_real_comment.append((index, del_bracket(element)))
    
    if move_number[0] == "1...":
        moves.insert(0, "skip")
        
    import converter
    converter.main(moves, tag_name, tag_value, exact_real_comment, db_file_path)
    tag_name.clear()
    tag_value.clear()
    moves.clear()
    gameEnd.clear()
    comment.clear()
    move_number.clear()
    real_comment.clear()
    exact_real_comment.clear()

if __name__ == '__main__':
    main()