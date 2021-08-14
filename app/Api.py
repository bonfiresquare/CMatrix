from abc import ABC
import requests


class Api (ABC):
    _base_url = None

    @staticmethod
    def review(response):
        status = {
            400: Exception('invalid parameters'),
            404: Exception('not found'),
            429: Exception('too many requests')
        }
        if response.status_code in status.keys():
            raise status[response.status_code]
        else:
            return response.json()

    @staticmethod
    def init(url):
        Api._base_url = url
        return

    @staticmethod
    def get_coins():
        response = requests.get(Api._base_url + 'coins')
        return Api.review(response)

    @staticmethod
    def get_exchanges():
        response = requests.get(Api._base_url + 'exchanges')
        return Api.review(response)

    @staticmethod
    def get_coin(coin_id):
        response = requests.get(Api._base_url + 'coins/' + coin_id)
        return Api.review(response)

    @staticmethod
    def get_coin_markets(coin_id, params):
        response = requests.get(Api._base_url + 'coins/' + coin_id + '/markets', params=params)
        return Api.review(response)

    @staticmethod
    def get_exchange_markets(exchange_id, params):
        response = requests.get(Api._base_url + 'exchanges/' + exchange_id + '/markets', params=params)
        return Api.review(response)

    @staticmethod
    def convert(coin_id, quote, amount):
        params = {
            'base_currency_id': coin_id,
            'quote_currency_id': quote,
            'amount': amount
        }
        response = requests.get(Api._base_url + 'price-converter', params=params)
        return Api.review(response)
