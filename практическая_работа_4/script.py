from file_utils import parse_pkl_file, save_to_json_file, parse_csv_file, parse_json_file, parse_msgpack_file
from sqlalchemy import create_engine
from db_model import Base, House, ReviewHouse, Song, Phone, Club, ClubGame, Player
from repository import HouseRepository, ReviewHouseRepository, SongRepository, PhoneRepository, ClubRepository, \
    ClubGameRepository, PlayerRepository
from model import StatInformation, FrequencyInformation, DataInformation, DataEncoder, OnlyStatInformation
from utils import get_name_column, build_stat_information, cast_str_to_int, cast_str_to_float, \
    delete_key_value_by_key_list, cast_str_number_to_bool, cast_str_to_date


def init_db():
    engine = create_engine('sqlite:///db.sqlite', echo=True)
    Base.metadata.create_all(engine)
    return (HouseRepository(engine), ReviewHouseRepository(engine),
            SongRepository(engine), PhoneRepository(engine),
            ClubRepository(engine), ClubGameRepository(engine), PlayerRepository(engine))


def load_data_task_1(repository: HouseRepository):
    data = parse_pkl_file("task_1_var_51_item.pkl")
    house_list = list(map(lambda item: House.create_from_dict(item), data))
    repository.save_all(house_list)


def query_task_1(repository: HouseRepository):
    sorted_data = repository.get_sorted(House.year.desc(), 25)
    stat_information = build_stat_information(repository.get_sum, repository.get_min,
                                              repository.get_max, repository.get_avg,
                                              House.prob_price)
    freq_dict = dict(repository.get_frequency(House.city))
    freq_information = FrequencyInformation(get_name_column(House.city), freq_dict)
    filtered_data = repository.get_by_great_than_floor_and_between_year(3, 1850, 1950,
                                                                        House.prob_price.desc(), 25)
    result = DataInformation(sorted_data, filtered_data, stat_information, freq_information)
    save_to_json_file(result, DataEncoder, "answer/task_1_answer.json")


def load_data_task_2(repository: ReviewHouseRepository):
    data = parse_pkl_file("task_2_var_51_subitem.pkl")
    review_house_list = list(map(lambda item: ReviewHouse.create_from_dict(item), data))
    repository.save_all(review_house_list)


def map_house_with_rating(tup: (House, int)):
    dict_house = tup[0].to_dict()
    dict_house['rating'] = tup[1]
    return dict_house


def query_task_2(repository: HouseRepository):
    review_by_city = repository.get_review_by_in_city(['Минск', 'Белград', 'Гранада'], ReviewHouse.rating.desc())
    house_with_max_rating = list(
        map(lambda item: map_house_with_rating(item), repository.get_house_with_max_rating(20)))
    review_by_year = repository.get_review_by_year_house_between(1900, 2000, ReviewHouse.security, 10)
    result = {'review_by_city': review_by_city,
              'house_with_max_rating': house_with_max_rating,
              'review_by_year': review_by_year}
    save_to_json_file(result, DataEncoder, "answer/task_2_answer.json")


def load_data_task_3(repository: SongRepository):
    columns = ['artist', 'song', 'duration_ms', 'year', 'tempo', 'genre']
    cast_type_by_name = {'duration_ms': cast_str_to_int, 'year': cast_str_to_int, 'tempo': cast_str_to_float}
    csv_data = parse_csv_file("task_3_var_51_part_1.csv", columns, cast_type_by_name)
    delete_columns = ['explicit', 'popularity', 'danceability']
    json_data = list(map(lambda item: delete_key_value_by_key_list(item, delete_columns),
                         parse_json_file("task_3_var_51_part_2.json")))
    all_data = csv_data + json_data
    save_data = list(map(lambda item: Song.create_from_dict(item), all_data))
    repository.save_all(save_data)
    # song_repository.save_all(csv_data)


def query_task_3(repository: SongRepository):
    sorted_data = repository.get_sorted(Song.duration_ms, 61)
    stat_information = build_stat_information(repository.get_sum, repository.get_min,
                                              repository.get_max, repository.get_avg,
                                              Song.duration_ms)
    freq_dict = dict(repository.get_frequency(Song.genre))
    freq_information = FrequencyInformation(get_name_column(Song.genre), freq_dict)
    filtered_data = repository.get_by_genre_and_between_year("pop", 2000, 2015,
                                                             Song.tempo.desc(), 66)
    result = DataInformation(sorted_data, filtered_data, stat_information, freq_information)
    save_to_json_file(result, DataEncoder, "answer/task_3_answer.json")


def load_data_task_4(repository: PhoneRepository):
    data = parse_pkl_file("task_4_var_51_product_data.pkl")
    phone_list = list(map(lambda item: Phone.create_from_dict(item), data))
    repository.save_all(phone_list)
    print(data)


def update_data_task_4(repository: PhoneRepository):
    update_data = parse_msgpack_file("task_4_var_51_update_data.msgpack")
    for update in update_data:
        repository.update_data(update)


def map_stat_phone_to_dict(tup):
    phone_dict = {}
    stat_information = OnlyStatInformation(count=tup[1], sum=tup[2], min=tup[3], max=tup[4], mean=tup[5])
    phone_dict[tup[0]] = stat_information
    return phone_dict


def query_task_4(repository: PhoneRepository):
    top_updated = repository.get_top(Phone.count_update.desc(), 10)
    stat_by_price = repository.get_stat(Phone.from_city, Phone.price)
    stat_by_price_dict_list = list(map(lambda item: map_stat_phone_to_dict(item), stat_by_price))
    stat_by_quantity = repository.get_stat(Phone.from_city, Phone.quantity)
    stat_by_quantity_dict_list = list(map(lambda item: map_stat_phone_to_dict(item), stat_by_quantity))
    data_by_cities = repository.get_by_in_city(['Гранада', 'Варшава', 'Алькала-де-Энарес', 'Тбилиси'],
                                               Phone.price.desc(), 10)
    result = {'top_updated': top_updated, 'stat_by_price': stat_by_price_dict_list,
              'stat_by_quantity': stat_by_quantity_dict_list, 'data_by_cities': data_by_cities}
    save_to_json_file(result, DataEncoder, 'answer/task_4_answer.json')
    print(data_by_cities)


def load_club_data_task_5(club_repository: ClubRepository):
    columns_club = ['club_id', 'club_code', 'name', 'squad_size', 'average_age', 'foreigners_number',
                    'national_team_players', 'stadium_name', 'stadium_seats', 'net_transfer_record', 'last_season']
    club_cast_type_by_name = {'club_id': cast_str_to_int, 'squad_size': cast_str_to_int,
                              'average_age': cast_str_to_float,
                              'foreigners_number': cast_str_to_int, 'national_team_players': cast_str_to_int,
                              'stadium_seats': cast_str_to_int, 'last_season': cast_str_to_int}
    club_csv_data = parse_csv_file("task_5_data/clubs.csv", columns_club, club_cast_type_by_name, delimiter=',',
                                   is_all=True)
    club_data = list(map(lambda item: Club.create_from_dict(item), club_csv_data))
    club_repository.save_all(club_data)
    print(club_csv_data)


def load_club_games_data_task_5(club_game_repository: ClubGameRepository):
    columns_club_games = ['game_id', 'club_id', 'own_goals', 'own_position', 'own_manager_name', 'opponent_id',
                          'opponent_goals', 'opponent_position', 'opponent_manager_name', 'hosting', 'is_win']
    club_games_cast_type_by_name = {'game_id': cast_str_to_int, 'club_id': cast_str_to_int,
                                    'own_goals': cast_str_to_int, 'own_position': cast_str_to_int,
                                    'opponent_id': cast_str_to_int, 'opponent_goals': cast_str_to_int,
                                    'opponent_position': cast_str_to_int, 'is_win': cast_str_number_to_bool}
    club_games_csv_data = parse_csv_file("task_5_data/club_games.csv", columns_club_games, club_games_cast_type_by_name,
                                         delimiter=',',
                                         is_all=True)
    club_games_data = list(map(lambda item: ClubGame.create_from_dict(item), club_games_csv_data))
    club_game_repository.save_all(club_games_data)
    print(club_games_data)


def load_player_data_task_5(player_repository: PlayerRepository):
    columns_player_games = ['player_id', 'first_name', 'last_name', 'name', 'last_season', 'current_club_id',
                            'country_of_birth', 'city_of_birth', 'date_of_birth', 'position', 'foot', 'height_in_cm',
                            'market_value_in_eur']
    player_cast_type_by_name = {'player_id': cast_str_to_int, 'last_season': cast_str_to_int,
                                'current_club_id': cast_str_to_int, 'height_in_cm': cast_str_to_int,
                                'market_value_in_eur': cast_str_to_int, 'date_of_birth': cast_str_to_date}
    player_csv_data = parse_csv_file("task_5_data/players.csv", columns_player_games, player_cast_type_by_name,
                                     delimiter=',',
                                     is_all=True)
    player_games_data = list(map(lambda item: Player.create_from_dict(item), player_csv_data))
    player_repository.save_all(player_games_data)
    print(player_games_data)


def map_stat_phone_to_dict(tup):
    club_game_dict = {}
    stat_information = OnlyStatInformation(count=tup[1], sum=tup[2], min=tup[3], max=tup[4], mean=tup[5])
    club_game_dict[tup[0]] = stat_information
    return club_game_dict


def map_freq(tup):
    new_dict = {}
    new_dict[tup[0]] = tup[1]
    return new_dict


def query_task_5(club_repository, club_game_repository, player_repository):
    filtered_club = club_repository.get_by_more_than_squad_size(25, Club.squad_size, 30)
    club_by_player = club_repository.get_club_by_player_name("Rio Ferdinand")
    stat_by_own_manager_name = club_game_repository.get_stat(ClubGame.own_manager_name, ClubGame.own_goals)
    stat_data = list(
        map(lambda item: map_stat_phone_to_dict(item), filter(lambda item: item[0] != '', stat_by_own_manager_name)))
    players_most_goals = list(map(lambda item: item[0],club_game_repository.get_players_for_club_with_most_sum_own_goals()))
    players_by_country = player_repository.get_by_country('England', Player.date_of_birth.desc(), 30)
    freq_by_own_goals = list(map(map_freq,club_game_repository.get_frequency(ClubGame.own_goals)))
    result = {'filtered_clubs': filtered_club, 'club_by_player': club_by_player,
              'stat_by_own_manager_name': stat_data,
              'players_most_goals': players_most_goals, 'players_by_country': players_by_country,
              'freq_by_own_goals': freq_by_own_goals}
    save_to_json_file(result, DataEncoder, 'answer/task_5_answer.json')


(house_repository, review_house_repository, song_repository,
 phone_repository, _club_repository, _club_game_repository, _player_repository) = init_db()

load_data_task_1(house_repository)
query_task_1(house_repository)

load_data_task_2(review_house_repository)
query_task_2(house_repository)

load_data_task_3(song_repository)
query_task_3(song_repository)


load_data_task_4(phone_repository)
update_data_task_4(phone_repository)
query_task_4(phone_repository)


load_club_data_task_5(_club_repository)
load_club_games_data_task_5(_club_game_repository)
load_player_data_task_5(_player_repository)

query_task_5(_club_repository, _club_game_repository, _player_repository)
