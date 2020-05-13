# Cryptocurrency Alerts

import os
import json
import time
from datetime import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# from say import *
# import subprocess

# def say(text):
#     subprocess.call(['say', text])


convert = 'USD'

listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'convert':convert
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '13d954ac-c414-4533-8cfe-29627626b66e',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(listings_url, params=parameters)
  results = json.loads(response.text)
  # print(results)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

data = results['data']

ticker_url_pairs = {}
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    ticker_url_pairs[symbol] = url

print()
print('ALERTS TRACKING...')
print()

already_hit_symbols = []

while True:
    with open('alerts.txt') as inp:
        for line in inp:
            ticker, amount = line.split()
            ticker = ticker.upper()

            ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
            parameters = {
              'id':str(ticker_url_pairs[ticker])
            }
            headers = {
              'Accepts': 'application/json',
              'X-CMC_PRO_API_KEY': '13d954ac-c414-4533-8cfe-29627626b66e',
            }

            session = Session()
            session.headers.update(headers)

            try:
              response = session.get(ticker_url, params=parameters)
              results = json.loads(response.text)
              # print(results)
            except (ConnectionError, Timeout, TooManyRedirects) as e:
              print(e)

            currency = results['data'][str(ticker_url_pairs[ticker])]
            name = currency['name']
            last_updated_string = currency['last_updated']
            symbol = currency['symbol']
            quotes = currency['quote'][convert]
            price = quotes['price']

            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                # os.system('say ' + name + ' hit ' + amount)
                # say(name + ' hit ' + amount)
                last_updated = datetime.strptime(last_updated_string, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%B %d, %Y at %I:%M%p')
                print(name + ' hit ' + amount + ' on ' + last_updated)
                already_hit_symbols.append(symbol)

    print('...')
    time.sleep(300)
