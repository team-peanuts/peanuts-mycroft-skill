import json
import uuid

import requests


#def get_shopping_cart(user):
#    url = 'http://peanuts-voice-api.westus.azurecontainer.io:8080/shopping-cart/' + user
#    request_result = requests.get(url)
#
#   return request_result


#def get_nlu_result(s):
#    url = 'http://peanuts-voice-api.westus.azurecontainer.io:8080/nlu'
#    res = requests.post(url, s)
#    return res


def add_to_shopping_cart(user, nlu_result):

    items = []
    for nlu_item in nlu_result:
        item = dict()
        item['itemName'] = nlu_item['itemName']
        item['itemQuantity'] = nlu_item['itemQuantity']
        item['itemId'] = str(uuid.uuid4())
        items.append(item)

    shopping_cart_content = get_shopping_cart(user)
    shopping_cart_content_json = shopping_cart_content.json()

    shopping_cart_content_json['shoppingCartItems'] = shopping_cart_content_json['shoppingCartItems'] + items

    url = 'http://peanuts-voice-api.westus.azurecontainer.io:8080/shopping-cart/' + user
    header = {'Content-type': 'application/json',
              'accept': 'application/json'}
    res = requests.put(url, json.dumps(shopping_cart_content_json), headers=header)

    print(res)
    # 1. get shopping cart content
    # 2. add new order
    # 3. update shopping cart


if __name__ == '__main__':

    nlu_results  = get_nlu_result('toilet paper')
    add_to_shopping_cart('testcaller1', nlu_results.json())

