from model import StatInformation


def get_name_column(field):
    return str(field).split('.')[-1]


def build_stat_information(sum_func, min_func, max_func, mean_func, field) -> StatInformation:
    sum_by_field = sum_func(field)
    min_by_field = min_func(field)
    max_by_field = max_func(field)
    mean_by_field = mean_func(field)
    name = str(field).split('.')[-1]
    return StatInformation(name, sum_by_field, mean_by_field, min_by_field, max_by_field)


def cast_str_to_int(value: str):
    if value is None or value == '':
        return None
    return int(value)


def cast_str_to_float(value: str):
    if value is None or value == '':
        return None
    return float(value)


def cast_str_number_to_bool(value: str):
    return bool(int(value))


def delete_key_value_by_key_list(dictionary, key_list):
    for key in key_list:
        del dictionary[key]
    return dictionary
