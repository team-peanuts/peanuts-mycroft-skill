import json
import uuid

import requests
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler


class Peanuts(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.user_name = 'philipp '




    @intent_handler('add.user.intent')
    def add_user(self, message):

        self.add_a_new_customer(self.user_name)
        self.speak("Added new order for you " + self.user_name)

    @intent_handler('order.intent')
    def handle_order(self, message):
        what = message.data.get('type')
        self.log.warning(what)

        nlu_result = self.get_nlu_result(what)

        self.add_to_shopping_cart(self.user_name, nlu_result.json())

        self.speak(what)

    @intent_handler('get.shopping.cart.intent')
    def handle_get_shoping_cart(self, message):
        self.log.warning(self.user_name)
        result_string = self.get_shopping_cart_string_results(self.user_name)

        self.speak(result_string)


    def get_nlu_result(self, s):
        url = 'http://peanuts-voice-api.westus.azurecontainer.io:8080/nlu'
        res = requests.post(url, s)
        return res

    def add_to_shopping_cart(self, user, nlu_result):

        items = []
        for nlu_item in nlu_result:
            item = dict()
            item['itemName'] = nlu_item['itemName']
            item['itemQuantity'] = nlu_item['itemQuantity']
            item['itemId'] = str(uuid.uuid4())
            items.append(item)

        shopping_cart_content = self.get_shopping_cart(user)
        shopping_cart_content_json = shopping_cart_content.json()

        shopping_cart_content_json['shoppingCartItems'] = shopping_cart_content_json['shoppingCartItems'] + items

        url = 'http://peanuts-voice-api.westus.azurecontainer.io:8080/shopping-cart/' + user
        header = {'Content-type': 'application/json',
                  'accept': 'application/json'}
        res = requests.put(url, json.dumps(shopping_cart_content_json), headers=header)

        print(res)

    def add_a_new_customer(self, person):
        customer = dict()
        customer['customerName'] = 'Dummy name'
        customer['callerId'] = person
        customer['customerAddress'] = 'Dummy Address, Zurich, Switzerland'

        obj = dict()
        obj['shoppingCartCustomer'] = customer
        obj['shoppingCartItems'] = []
        obj['orderDate'] = 0
        obj['expectedDeliveryDate'] = 0
        obj['shoppingCartId'] = '732ed14e-b202-43ed-8d3f-c09851fbd8e8'
        obj['orderStatus'] = 'ORDER_CREATED'

        url = 'http://peanuts-voice-api.westus.azurecontainer.io:8080/shopping-cart/'
        header = {'Content-type': 'application/json',
                  'accept': 'application/json'}
        requests.post(url, json.dumps(obj), headers=header)

    def get_shopping_cart_string_results(self, user):
        request_result = self.get_shopping_cart(user)

        result_string = ''
        for item in request_result.json()['shoppingCartItems']:
            result_string = result_string + str(item['itemQuantity']) + ':' + item['itemName'] + ', '

        return result_string

    def get_shopping_cart(self, user):
        url = 'http://peanuts-voice-api.westus.azurecontainer.io:8080/shopping-cart/' + user
        request_result = requests.get(url)

        return request_result

def create_skill():
    return Peanuts()


