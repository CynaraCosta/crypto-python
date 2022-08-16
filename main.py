from dataclasses import replace
import config
from requests import Request, Session
import json
import pprint

url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"

parameters = {
    'slug': 'polkadot',
    'convert': 'BRL'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config.api_key
}

session = Session()
session.headers.update(headers)

response = session.get(url, params=parameters)
# pprint.pprint(json.loads(response.text)["data"])

first_dict = json.loads(response.text)["data"]
cad_coin = next(iter(first_dict))
price_value = json.loads(response.text)["data"][f"{cad_coin}"]["quote"]["BRL"]["price"]

price_usd_value_string = "R$ {:.2f}".format(price_value)
price_brl_value_string = price_usd_value_string.replace(".", ",")
print(price_brl_value_string)