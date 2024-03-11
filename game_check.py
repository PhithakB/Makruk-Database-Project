import re

game = []
game_tag = []
filtered_list = []
real_game_tag = []
def game_split(file_path):
    with open(file_path, encoding="utf-8") as pgn_file:
        pgn_data = pgn_file.read()

    games = re.split(r'\n\n(?=\[Event)', pgn_data.strip())
    
    for game_number, game_data in enumerate(games, start=1):
        game.append((game_number, game_data))
        game_tags = re.compile(r'\[([^"]+)"([^"]+)"\]')
        game_tags_matches = game_tags.findall(game_data)
        game_tag.append((game_number,game_tags_matches))

def main(file_path):
    game.clear()
    game_tag.clear()
    filtered_list.clear()
    real_game_tag.clear()
    
    game_split(file_path)
    key_name = ['White', 'Result', 'Black', 'Date', 'Event']
    for game_number, game_data in game_tag:
        for key in range(len(key_name)):
            for info in range(len(game_data)):
                if key_name[key] in game_data[info][0]:
                    filtered_list.append((game_number, game_data[info]))

    merged_data = {}

    for item in filtered_list:
        number, info = item
        if number not in merged_data:
            merged_data[number] = []
        merged_data[number].append( info)

    result = list(merged_data.values())

    for game_number, game_data in enumerate(result, start=1):
        real_game_tag.append((game_number, game_data))

if __name__ == '__main__':
    main()