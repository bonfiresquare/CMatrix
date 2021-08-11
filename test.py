import requests
import json
from types import SimpleNamespace

params = {
    'base_currency_id' : 'btc-bitcoin',
    'quote_currency_id' : 'eth-ethereum',
    'amount' : 1
}

#Response = requests.get('https://api.coinpaprika.com/v1/price-converter', params=params)
#Response = requests.get('https://api.coinpaprika.com/v1/coins')
Response = requests.get('https://api.coinpaprika.com/v1/coins/usdt-tether')
Json = Response.json()
print(Json)
#Data = Response.text
#x = json.loads(Data, object_hook=lambda d: SimpleNamespace(**d))

#for i in range(20):
#    print(x[i].rank, x[i].id, x[i].name)
