import json
import msgpack
import os
from itertools import groupby


def calculate_average(price_list: list):
    avg_price = sum(price_list) / len(price_list)
    min_price = min(price_list)
    max_price = max(price_list)
    return {'avg': avg_price, 'min': min_price, 'max': max_price}


def handle_group(tpl: tuple):
    name = tpl[0]
    prices = list(map(lambda item: item['price'], tpl[1]))
    averaged_price_data = calculate_average(prices)
    return {'name': name, 'average_data': averaged_price_data}


with open("products_51.json") as file:
    data = json.load(file)

grouped_data = groupby(data, key=lambda item: item['name'])
averaged_data = list(map(handle_group, grouped_data))

with open('answer.json', 'w') as f:
    json.dump(averaged_data, f)

with open("answer.msgpack", "wb") as f:
    msgpack.dump(averaged_data, f)

answer_json_size = os.path.getsize('answer.json')
answer_msgpack_size = os.path.getsize('answer.msgpack')
print('json: ' + str(answer_json_size))
print('msgpack: ' + str(answer_msgpack_size))