import sqlite3

def main(filename, game_id):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute(f'''
                SELECT
                    Move.Move_ID,
                    Move.End
                FROM Move WHERE Game_ID = {game_id}''')
                
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data