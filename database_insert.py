import sqlite3

def extract_tag_from_pgn_file(tag_name, tag_value):
    tag = []
    for name, value in zip(tag_name, tag_value):
        tag.append((name, value))
    return tag

def extract_comment_from_pgn_file(exact_real_comment):
    comment = []
    for move_id, value in exact_real_comment:
        comment.append((move_id, value))
    return comment

def variant_check(tag):
    variant_name = ''
    for i in range(len(tag)):
        if tag[i][0] == 'Variant':
            variant_name = tag[i][1]
            variant_name = variant_name.replace('\"', '')
            break
        else:
            variant_name = 'Makruk'
    return variant_name

def insert_variant(cursor, variant):
    cursor.execute(f"INSERT OR IGNORE INTO Variant (Variant_Name) VALUES ('{variant}')")

def insert_game(variant, cursor, fen_start, row_variant):
    for i in range(len(row_variant)):
        if row_variant[i][1] == variant:
            cursor.execute(f"INSERT INTO Game (Start_Position, Variant_ID) VALUES ('{fen_start}', {row_variant[i][0]})")

def check_role(tag):
    white = ''
    black = ''
    for i in range(len(tag)):
        if tag[i][0] == 'White':
            white = tag[i][0]
        elif tag[i][0] == 'Black':
            black = tag[i][0]
    return white, black

def insert_tag(cursor, tag):
    for i in range(len(tag)):
        if tag[i][0] == 'White':
            cursor.execute(f"INSERT OR IGNORE INTO Player (Player_Name) VALUES ('{tag[i][1]}')")
        elif tag[i][0] == 'Black':
            cursor.execute(f"INSERT OR IGNORE INTO Player (Player_Name) VALUES ('{tag[i][1]}')")
        else:
            cursor.execute(f"INSERT OR IGNORE INTO Tag (Tag_Name) VALUES ('{tag[i][0]}')")

def tag_check(tag):
    tag_name = []
    for i in range(len(tag)):
        tag_name.append(tag[i][0])
    return tag_name

def insert_game_info(cursor, tag, row_tag, tag_name, id_game):
    tag_id = []
    for i in row_tag:
        for j in tag_name:
            if i[1] == j:
                tag_id.append(i[0])
                for k in tag_id:
                    if i[0] == k:
                        for l in tag:
                            if l[0] == i[1]:
                                cursor.execute(f"INSERT INTO Game_Info (Value, Tag_ID, Game_ID) VALUES ('{l[1]}', {k}, {id_game})")

def insert_role(cursor, tag, row_role, color, id_game):
    tag_id = []
    for i in color:
        for j in tag:
            if j[0] == i:
                for k in row_role:
                    if k[1] == j[1] and k[0] not in tag_id:
                        tag_id.append(k[0])
                    for l in tag_id:
                        if k[1] == j[1] and k[0] == l:
                            cursor.execute(f"INSERT INTO Role (Color, Game_ID, Player_ID) VALUES ('{i}', {id_game}, {l})")

def insert_move(cursor, id_game, start_pos, end_pos, fen_result_old, fen_start):
    fen_result = []
    for i, j in zip(start_pos, end_pos):
        if i == 'skip' and j == 'skip':
            fen_result.append(fen_start)
    for i in fen_result_old:
        fen_result.append(i)

    for i in range(len(start_pos)):
        position = cursor.execute("SELECT * FROM Position")
        pos_list = position.fetchall()
        for j in pos_list:
            if j[1] == fen_result[i]:
                pos_ins = j[0]
                cursor.execute(f"INSERT INTO Move (Start, End, Game_ID, Move_ID, Position_ID) VALUES ('{start_pos[i]}', '{end_pos[i]}', {id_game}, {i+1}, {pos_ins})")

def insert_comment(cursor, comment, id_game):
    for i in range(len(comment)):
        cursor.execute(f"INSERT INTO Comment (Comment, Game_ID, Move_ID) VALUES ('{comment[i][1]}', {id_game}, {comment[i][0]})")

def insert_position(cursor, fen_pos):
    for i in range(len(fen_pos)):
        cursor.execute(f"INSERT OR IGNORE INTO Position (Position) VALUES ('{fen_pos[i]}')")

def main(tag_name, tag_value, exact_real_comment, fen_start, startPosition, endPosition, fen_result, db_file_path):
    try:
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        tag = extract_tag_from_pgn_file(tag_name, tag_value)
        comment = extract_comment_from_pgn_file(exact_real_comment)
        variant = variant_check(tag)

        insert_variant(cursor, variant)

        variant_row = cursor.execute("SELECT * FROM Variant")
        row_variant = variant_row.fetchall()

        insert_game(variant, cursor, fen_start[0], row_variant)
        id_game = ''
        game_id = cursor.execute("SELECT MAX(Game_ID) FROM Game")
        for i in game_id:
            id_game = i[0]

        insert_tag(cursor, tag)

        tag_row = cursor.execute("SELECT * FROM Tag")
        row_tag = tag_row.fetchall()
        tag_name_found = tag_check(tag)

        insert_game_info(cursor, tag, row_tag, tag_name_found, id_game)

        role_row = cursor.execute("SELECT * FROM Player")
        row_role = role_row.fetchall()
        color = check_role(tag)

        insert_role(cursor, tag, row_role, color, id_game)
        fen_pos = fen_result
        insert_position(cursor, fen_pos)

        start_pos = startPosition
        end_pos = endPosition
        insert_move(cursor, id_game, start_pos, end_pos, fen_result, fen_start[0])
        insert_comment(cursor, comment, id_game)
        
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    main()