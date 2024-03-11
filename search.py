import sqlite3

def searchbyfen(fen, db_file_path):
    game_id = []
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    fen_to_search = fen.replace('-','_')
    cursor.execute("SELECT * FROM Game WHERE Start_Position LIKE ?", (fen_to_search,))
    result1 = cursor.fetchall()
    if result1:
        for i in range(len(result1)):
            game_id.append(result1[i][0])
        
    cursor.execute("SELECT * FROM Position WHERE Position LIKE ?", (fen_to_search,))
    result2 = cursor.fetchall()
    if result2:
        for i in range(len(result2)):
            pos_id = result2[i][0]
            cursor.execute("SELECT * FROM Move WHERE Position_ID = ?", (pos_id,))
            result3 = cursor.fetchall()
            
            for j in range(len(result3)):
                gid = result3[j][2]
                if gid not in game_id:
                    game_id.append(gid)
                else:
                    pass
    cursor.close()
    conn.close()
    if game_id:
        return game_id
    else:
        return "Not Found"
