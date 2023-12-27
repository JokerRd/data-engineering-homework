from collections import Counter

from model import StatInformation, FrequencyInformation


def calculate_stat(name_field: str, get_field_func, item_list: list):
    sum_value = sum(map(get_field_func, item_list))
    mean = round(sum_value / len(item_list), 2)
    min_value = min(map(get_field_func, item_list))
    max_value = max(map(get_field_func, item_list))
    return StatInformation(name_field, sum_value, mean, min_value, max_value)


def calculate_frequency(name_field, get_field_func, item_list: list):
    field_value_list = list(filter(lambda item: item is not None, map(get_field_func, item_list)))
    frequency_by_name = dict(Counter(field_value_list))
    return FrequencyInformation(name_field, frequency_by_name)