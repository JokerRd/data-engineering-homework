from collections import Counter

from file_utils import load_files, save_to_json_file
from html_utils import SoupHelper
from model import ChessInformation, StatInformation, FrequencyInformation, DataInformation, DataEncoder
from cast_utils import cast_int, cast_float


def parse_html_with_chess_information(html: str):
    helper = SoupHelper(html)
    chess_info = ChessInformation()
    chess_info.type = helper.get_value_by_selector("div.chess-wrapper div span")
    chess_info.tournament = helper.get_value_by_selector("h1.title")
    chess_info.city = helper.get_value_by_selector_and_exclude_substring("p.address-p",
                                                                         "Город", "Начало")
    chess_info.date = helper.get_value_by_selector_and_name("p.address-p", "Начало")
    chess_info.round_count = cast_int(helper.get_value_by_selector("span.count"))
    chess_info.time_control = helper.get_value_by_selector("span.year")
    chess_info.min_rating = cast_int(helper.get_value_by_selector("span.year + span"))
    chess_info.url_img = helper.get_value_attr_by_selector("img", "src")
    chess_info.rating = cast_float(helper.get_value_by_selector("div.chess-wrapper div:last-child span:first-child"))
    chess_info.count_view = cast_int(helper.get_value_by_selector("div.chess-wrapper div:last-child span:last-child"))
    return chess_info


def calculate_stat(name_field: str, get_field_func, item_list: list):
    sum_value = sum(map(get_field_func, item_list))
    mean = round(sum_value / len(item_list), 2)
    min_value = min(map(get_field_func, item_list))
    max_value = max(map(get_field_func, item_list))
    return StatInformation(name_field, sum_value, mean, min_value, max_value)


def calculate_frequency(name_field, get_field_func, item_list: list):
    field_value_list = list(map(get_field_func, item_list))
    frequency_by_name = dict(Counter(field_value_list))
    return FrequencyInformation(name_field, frequency_by_name)


def parse_html_task1():
    files_as_str = load_files('1_zip_var_51')
    chess_information_list = list(map(lambda html: parse_html_with_chess_information(html), files_as_str))
    sorted_chess_information_list = sorted(chess_information_list, key=lambda item: item.rating, reverse=True)
    filtered_chess_information_list = list(filter(lambda item: 2200 < item.min_rating < 2300,
                                                  chess_information_list))
    stat = calculate_stat("count_view", lambda item: item.count_view, chess_information_list)
    frequency = calculate_frequency("type", lambda item: item.type, chess_information_list)
    result = DataInformation(chess_information_list, sorted_chess_information_list,
                             filtered_chess_information_list, stat, frequency)
    save_to_json_file(result, DataEncoder, "task_1_answer.json")


parse_html_task1()
