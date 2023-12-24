from parser import parse_json_file
from parser import parse_csv_file
from mongo_lib import load_data_to_mongo


def cast_str_to_int(value: str):
    if value is None or value == '':
        return None
    return int(value)


def cast_str_number_to_bool(value: str):
    return bool(int(value))


data = parse_json_file("task4_clubs.json")
load_data_to_mongo('club', data)

field_names = ['game_id', "club_id", "own_goals", "own_position", "own_manager_name", "opponent_id",
               "opponent_goals", "opponent_position", 'opponent_manager_name', "hosting", "is_win"]
cast_type_by_name = {"game_id": cast_str_to_int,
                     "club_id": cast_str_to_int,
                     "own_goals": cast_str_to_int,
                     "own_position": cast_str_to_int,
                     "opponent_id": cast_str_to_int,
                     "opponent_goals": cast_str_to_int,
                     "opponent_position": cast_str_to_int,
                     "is_win": cast_str_number_to_bool}

data = parse_csv_file("task4_club_games.csv", field_names, cast_type_by_name, delimiter=',')
load_data_to_mongo('club_games', data)

print("Данные загружены")

