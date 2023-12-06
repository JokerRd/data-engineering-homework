from parser import parse_pkl_file
from mongo_lib import load_data_to_mongo


data = parse_pkl_file("task_1_item.pkl")
load_data_to_mongo('salary_data', data)
print("Данные загружены")