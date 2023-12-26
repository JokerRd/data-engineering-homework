from collections import Counter

from file_utils import load_files, save_to_json_file
from html_utils import SoupHelper
from model import ChessInformation, StatInformation, FrequencyInformation, DataInformation, DataEncoder, \
    PhoneInformation
from cast_utils import cast_int, cast_float
from практическая_работа_3.text_utils import substring_with_regex, exclude_substring


def parse_html_with_chess_information(html: str):
    helper = SoupHelper(html)
    chess_info = ChessInformation()
    chess_info.type = helper.get_substring_value_by_selector("div.chess-wrapper div span")
    chess_info.tournament = helper.get_substring_value_by_selector("h1.title")
    chess_info.city = helper.get_value_by_selector_and_exclude_substring("p.address-p",
                                                                         "Город", "Начало")
    chess_info.date = helper.get_value_by_selector_and_name("p.address-p", "Начало")
    chess_info.round_count = cast_int(helper.get_substring_value_by_selector("span.count"))
    chess_info.time_control = helper.get_substring_value_by_selector("span.year")
    chess_info.min_rating = cast_int(helper.get_substring_value_by_selector("span.year + span"))
    chess_info.url_img = helper.get_value_attr_by_selector("img", "src")
    chess_info.rating = cast_float(
        helper.get_substring_value_by_selector("div.chess-wrapper div:last-child span:first-child"))
    chess_info.count_view = cast_int(
        helper.get_substring_value_by_selector("div.chess-wrapper div:last-child span:last-child"))
    return chess_info


def parse_html_with_phone_information(html: str):
    helper = SoupHelper(html)
    phone_info = PhoneInformation()
    phone_info.id = cast_int(helper.get_value_attr_by_selector("a[data-id]", "data-id"))
    phone_info.model = helper.get_value_by_selector("div.product-item span")
    phone_info.screen_size_inch = cast_float(substring_with_regex(phone_info.model, r'^.*"', '"'))
    phone_info.memory_storage_gb = cast_int(substring_with_regex(phone_info.model, r'\d*GB', 'GB'))
    phone_info.price_rub = cast_int(helper.parse_value_by_selector("price",
                                                                   lambda raw: exclude_substring("₽", raw)))
    phone_info.bonus = cast_int(helper.get_number_value_by_selector("strong"))
    phone_info.processor = helper.get_value_by_selector('li[type="processor"]')
    phone_info.ram_gb = cast_int(helper.get_number_value_by_selector('li[type="ram"]'))
    phone_info.count_sim = cast_int(helper.get_number_value_by_selector('li[type="sim"]'))
    phone_info.matrix = helper.get_value_by_selector('li[type="matrix"]')
    phone_info.resolution = helper.get_value_by_selector('li[type="resolution"]')
    phone_info.size_camera_mp = cast_int(helper.get_number_value_by_selector('li[type="camera"]'))
    phone_info.acc_mah = cast_int(helper.get_number_value_by_selector('li[type="acc"]'))
    return phone_info


def parse_html_with_phone_information_list(html: str) -> list:
    helper = SoupHelper(html)
    elements = helper.get_elements_html_by_selector("div.pad")
    return list(map(lambda item: parse_html_with_phone_information(str(item)), elements))


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


def parse_html_task2():
    files_as_str = load_files('2_zip_var_51')
    phone_information_list = map(lambda html: parse_html_with_phone_information_list(html), files_as_str)
    phone_information_flat_list = sum(phone_information_list, [])
    sorted_data = sorted(phone_information_flat_list, key=lambda item: item.price_rub, reverse=True)
    filtered_data = list(filter(lambda item: (item.count_sim is not None and item.count_sim == 2) and
                                             (item.ram_gb is not None and item.ram_gb > 8),
                                phone_information_flat_list))
    stat = calculate_stat("price_rub", lambda item: item.price_rub, phone_information_flat_list)
    frequency = calculate_frequency("matrix", lambda item: item.matrix, phone_information_flat_list)
    result = DataInformation(phone_information_flat_list, sorted_data, filtered_data, stat, frequency)
    save_to_json_file(result, DataEncoder, "task_2_answer.json")


parse_html_task1()
parse_html_task2()
