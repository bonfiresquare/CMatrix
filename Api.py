import requests


class Api:
    def __init__(self, url):
        self._BaseUrl = url

    def get_coins(self):
        response = requests.get(self._BaseUrl + 'coins')
        return response.json()

    def get_coin(self, coin_id):
        response = requests.get(self._BaseUrl + 'coins/' + coin_id)
        return response.json()

    def convert(self, coin_id, quote, amount):
        params = {
            'base_currency_id': coin_id,
            'quote_currency_id': quote,
            'amount': amount
        }
        response = requests.get(self._BaseUrl + 'price-converter', params=params)
        pass
