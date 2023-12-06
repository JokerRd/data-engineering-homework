from parser import parse_csv_file
from mongo_lib import load_data_to_mongo


def cast_str_to_int(value: str):
    return int(value)


field_names = ["job", "salary", "id", "city", "year", "age"]
cast_type_by_name = {"salary": cast_str_to_int, "year": cast_str_to_int, "age": cast_str_to_int}
data = parse_csv_file("task_2_item.csv", field_names, cast_type_by_name)
load_data_to_mongo('salary_data', data)
print("Данные загружены")
