import csv
import json
import pickle


def parse_csv_file(name_file: str, field_names: list[str], cast_type_by_name, skip_header: bool = True,
                   delimiter: str = ';'):
    data_from_csv = []
    with open(name_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, field_names, delimiter=delimiter)
        if skip_header:
            csv_reader.__next__()
        for row in csv_reader:
            item = {}
            for field_name in field_names:
                cast_func = cast_type_by_name.get(field_name)
                raw_value = row[field_name]
                if cast_func is None:
                    item[field_name] = raw_value
                else:
                    item[field_name] = cast_func(raw_value)
            data_from_csv.append(item)
    return data_from_csv


def parse_pkl_file(name_file: str):
    with open(name_file, 'rb') as file:
        data_from_pkl = pickle.load(file)
    return data_from_pkl


def parse_json_file(name_file: str):
    with open(name_file, 'r', encoding='utf-8') as file:
        data_from_json = json.load(file)
    return data_from_json
