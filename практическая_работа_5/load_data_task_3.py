from parser import parse_json_file
from mongo_lib import load_data_to_mongo


data = parse_json_file("task_3_item.json")
load_data_to_mongo('salary_data', data)
print("Данные загружены")
