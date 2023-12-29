import csv
import json
import os
import pickle

import msgpack


def load_file_as_str(file_path) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return str(f.read())


def get_all_files_in_dir(dir_path: str) -> list[str]:
    return os.listdir(dir_path)


def load_files(dir_path: str) -> list[str]:
    files = get_all_files_in_dir(dir_path)
    return list(map(lambda file_name: load_file_as_str(os.path.join(dir_path, file_name)), files))


def save_to_json_file(data, encoder, file_name):
    with open(file_name, 'w', encoding='utf8') as f:
        json.dump(data, f, cls=encoder, indent=4, ensure_ascii=False)


def parse_pkl_file(name_file: str):
    with open(name_file, 'rb') as file:
        data_from_pkl = pickle.load(file)
    return data_from_pkl


def parse_msgpack_file(name_file: str):
    with open(name_file, 'rb') as file:
        data_from_pkl = msgpack.load(file)
    return data_from_pkl


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


def parse_json_file(name_file: str):
    with open(name_file, 'r', encoding='utf-8') as file:
        data_from_json = json.load(file)
    return data_from_json