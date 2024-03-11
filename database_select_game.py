import sqlite3

def main(filename):
    # filename = "C:\SeniorProject\Database\makruk.mkdb"
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    cursor.execute('''
        -- First Query
        SELECT 
            Game.Game_ID, 
            Game_Info.Value,
            Tag.Tag_Name
        FROM Game
        JOIN Game_Info ON Game.Game_ID = Game_Info.Game_ID
        JOIN Tag ON Game_Info.Tag_ID = Tag.Tag_ID
        WHERE Tag.Tag_Name IN ('Event', 'Date', 'Result')

        UNION ALL

        -- Second Query
        SELECT 
            Role.Game_ID,
            Role.Color, 
            Player.Player_Name
        FROM Role
        JOIN Player ON Role.Player_ID = Player.Player_ID;
    ''')

    rows_game = cursor.fetchall()
    # print(rows_game)

    conn.commit()
    conn.close()

    all_game = []

    for row in rows_game:
        if row[2] == 'Event' and (row[1] != 'White' or row[1] != 'Black'):
            all_game.append((row[0], row[1], row[2]))
        elif row[2] == 'Date' and (row[1] != 'White' or row[1] != 'Black'):
            all_game.append((row[0], row[1], row[2]))
        elif row[2] == 'Result' and (row[1] != 'White' or row[1] != 'Black'):
            all_game.append((row[0], row[1], row[2]))
        elif row[1] == 'White' and (row[2] != 'Event' or row[2] != 'Date' or row[2] != 'Result'):
            all_game.append((row[0], row[2], row[1]))
        elif row[1] == 'Black' and (row[2] != 'Event' or row[2] != 'Date' or row[2] != 'Result'):
            all_game.append((row[0], row[2], row[1]))

    all_game = [(id, value.replace('"', ''), attr) for id, value, attr in all_game]

    return SelectAllGame(all_game)

def countData(count, data):
    for i in data:
        count.append(i[0])

    count = list(dict.fromkeys(count))
    
    return count

def SortFrom(data, j):
    sorted_data = []
    sorted_data.clear()
    for i in data:
        if i[0] == j:
            sorted_data.append((i[2], i[1]))
    return sorted_data

def SelectAllGame(data):
    count = []
    alldata = []
    count= countData(count, data)
    
    for j in count:
        sort = SortFrom(data, j)
        #print(sort_from(data, j))
        alldata = alldata + [(j,(sort))]

    return alldata

if __name__ == '__main__':
    main()