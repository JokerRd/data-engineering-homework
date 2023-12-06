from pymongo import MongoClient
import urllib.parse
import os


def connect_to_mongo():
    return MongoClient("localhost", 27017)


def load_data_to_mongo(name_collection: str, input_data):
    client = connect_to_mongo()
    with client:
        db = client['data']
        salary_data_collection = db[name_collection]
        salary_data_collection.insert_many(input_data)
