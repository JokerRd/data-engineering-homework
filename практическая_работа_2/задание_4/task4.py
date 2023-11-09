import json
import pickle


def modify_product(product, price_info):
    copied_product = product.copy()
    if price_info['method'] == 'percent+':
        copied_product['price'] = product['price'] + product['price'] * price_info['param']
    elif price_info['method'] == 'percent-':
        copied_product['price'] = product['price'] - product['price'] * price_info['param']
    elif price_info['method'] == 'add':
        copied_product['price'] = product['price'] + price_info['param']
    elif price_info['method'] == 'sub':
        copied_product['price'] = product['price'] - price_info['param']
    return copied_product


with open("price_info_51.json") as file:
    price_info_list = json.load(file)

with open("products_51.pkl", 'rb') as file:
    products = pickle.load(file)

price_dict = {price_info['name']: {'method': price_info['method'], 'param': price_info['param']}
              for price_info in price_info_list}
modify_products = list(map(lambda product: modify_product(product, price_dict[product['name']]), products))

with open("answer.pkl", "wb") as f:
    pickle.dump(modify_products, f)
