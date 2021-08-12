from abc import ABC, abstractmethod
import requests


class Api (ABC):
    _base_url = None

    @staticmethod
    def get_coins():
        response = requests.get(Api._base_url + 'coins')
        return response.json()

    @staticmethod
    def get_coin(coin_id):
        response = requests.get(Api._base_url + 'coins/' + coin_id)
        return response.json()

    @staticmethod
    def convert(coin_id, quote, amount):
        params = {
            'base_currency_id': coin_id,
            'quote_currency_id': quote,
            'amount': amount
        }
        response = requests.get(Api._base_url + 'price-converter', params=params)
        pass

    @staticmethod
    def set_url(url):
        Api._base_url = url
