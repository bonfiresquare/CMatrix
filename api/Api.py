from datetime import datetime as dt
from datetime import timedelta as td
import requests


class Api:
    _base_url = None    # default: https://api.coinpaprika.com/v1/
    _status = {
        400: Exception('invalid parameters'),
        404: Exception('not found'),
        429: Exception('too many requests')
    }

    @staticmethod
    def init(url: str):
        Api._base_url = url
        return

    @staticmethod
    def get(url: str, params: dict = {}):
        response = requests.get(url, params)
        if response.status_code in Api._status.keys():
            raise Api._status[response.status_code]
        else:
            return response.json()

    @staticmethod
    def get_coin(id: str = None):
        return Api.get(Api._base_url + 'coins' + (f'/{id}' if id else ''))

    @staticmethod
    def get_coin_exchanges(id: str):
        return Api.get(Api._base_url + 'coins/' + id + '/exchanges')

    @staticmethod
    def get_coin_markets(id: str, quotes: str = 'USD,BTC'):
        # allowed quote currencies: BTC, ETH, USD, EUR, PLN, KRW, GBP, CAD, JPY, RUB, TRY,
        # NZD, AUD, CHF, UAH, HKD, SGD, NGN, PHP, MXN, BRL, THB, CLP, CNY, CZK, DKK, HUF,
        # IDR, ILS, INR, MYR, NOK, PKR, SEK, TWD, ZAR, VND, BOB, COP, PEN, ARS, ISK
        params = {'quotes': quotes}
        return Api.get(Api._base_url + 'coins/' + id + '/markets', params=params)


    @staticmethod
    def get_coin_ohlc_latest(id: str, quote: str = 'USD'):
        # allowed quote currencies: USD, BTC
        params = {'quote': quote}
        return Api.get(Api._base_url + f'coins/{id}/ohlcv/latest', params=params)

    @staticmethod
    def get_coin_ohlc_range( id: str,
                             start: str = str(int(dt.timestamp(dt.now() - td(days=7)))),
                             end: str = str(int(dt.timestamp(dt.now()))),
                             rows: int = 1,
                             quote:str = 'USD' ):
        # allowed time values:
            # RFC3999 (ISO-8601) eg. 2018-02-15T05:15:00Z
            # Simple date (yyyy-mm-dd) eg. 2018-02-15
            # Unix timestamp (in seconds) eg. 1518671700
        # allowed row limit: 1 - 366
        # allowed quote currencies: USD, BTC
        params = {'start': start, 'end': end, 'limit': rows, 'quote': quote}
        return Api.get(Api._base_url + f'coins/{id}/ohlcv/historical', params=params)

    @staticmethod
    def get_coin_ohlc_today(id: str, quote: str = 'USD'):
        # allowed quote currencies: USD, BTC
        params = {'quote': quote}
        return Api.get(Api._base_url + f'coins/{id}/ohlcv/today', params=params)

    @staticmethod
    def get_exchange(id: str = None):
        return Api.get(Api._base_url + 'exchanges' + (f'/{id}' if id else ''))

    @staticmethod
    def get_exchange_markets(id: str, params: dict = {'quotes':'USD,EUR'}):
        # allowed quote currencies: BTC, ETH, USD, EUR, PLN, KRW, GBP, CAD, JPY, RUB, TRY,
        # NZD, AUD, CHF, UAH, HKD, SGD, NGN, PHP, MXN, BRL, THB, CLP, CNY, CZK, DKK, HUF,
        # IDR, ILS, INR, MYR, NOK, PKR, SEK, TWD, ZAR, VND, BOB, COP, PEN, ARS, ISK
        return Api.get(Api._base_url + 'exchanges/' + id + '/markets', params=params)

    @staticmethod
    def convert(base_id: str, quote_id: str, amount: float = 1):
        params = {
            'base_currency_id': base_id,
            'quote_currency_id': quote_id,
            'amount': amount
        }
        response = requests.get(Api._base_url + 'price-converter', params=params)
        return Api.review(response)
