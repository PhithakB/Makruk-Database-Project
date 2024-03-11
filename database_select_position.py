import sqlite3

position = []
def get_position(filename, game_id):
    position.clear()
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Game WHERE Game_ID = {game_id}")
    data = cursor.fetchall()
    position.append(data[0][1])
    cursor.execute(f"SELECT * FROM Move WHERE Game_ID = {game_id}")
    move_data = cursor.fetchall()
    for data in move_data:
        position_id = f"{data[4]}"
        cursor.execute("SELECT * FROM Position WHERE Position_ID = ?", (position_id,))
        position_data = cursor.fetchall()
        pos = position_data[0][1]
        position.append(pos)
    conn.commit()
    conn.close()
    return position