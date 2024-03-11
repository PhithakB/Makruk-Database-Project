import os, sqlite3

def main(filename):
    if os.path.exists(filename):
        os.remove(filename)

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Variant (
            Variant_ID INTEGER PRIMARY KEY,
            Variant_Name TEXT UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Game (
            Game_ID INTEGER PRIMARY KEY,
            Start_Position TEXT NOT NULL,
            Variant_ID INTEGER,
            FOREIGN KEY (Variant_ID) REFERENCES Variant (Variant_ID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tag (
            Tag_ID INTEGER PRIMARY KEY,
            Tag_Name TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Game_Info (
            Value TEXT NOT NULL,
            Tag_ID INTEGER,
            Game_ID INTEGER,
            FOREIGN KEY (Game_ID) REFERENCES Game (Game_ID),
            FOREIGN KEY (Tag_ID) REFERENCES Tag (Tag_ID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Player (
            Player_ID INTEGER PRIMARY KEY,
            Player_Name TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Role (
            Color TEXT NOT NULL,
            Game_ID INTEGER,
            Player_ID INTEGER,
            FOREIGN KEY (Game_ID) REFERENCES Game (Game_ID),
            FOREIGN KEY (Player_ID) REFERENCES Player (Player_ID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Move (
            Start TEXT NOT NULL,
            End TEXT NOT NULL,
            Game_ID INTEGER,
            Move_ID INTEGER,
            Position_ID INTEGER,
            FOREIGN KEY (Game_ID) REFERENCES Game (Game_ID),
            FOREIGN KEY (Position_ID) REFERENCES Position (Position_ID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Comment (
            Comment TEXT NOT NULL,
            Game_ID INTEGER,
            Move_ID INTEGER,
            FOREIGN KEY (Game_ID) REFERENCES Game (Game_ID)
            FOREIGN KEY (Move_ID) REFERENCES Move (Move_ID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Position (
            Position_ID INTEGER PRIMARY KEY,
            Position TEXT NOT NULL UNIQUE
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()