import requests


def symboltoid(symbol):
    url = "https://api.coingecko.com/api/v3/coins/list"
    base = requests.get(url).json()
    for coin in base:
        if coin['symbol'] == symbol:
            return coin['id']


def price(symbol, currency):
    coin_id = symboltoid(symbol)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
    response = requests.get(url).json()
    return response[coin_id][currency]