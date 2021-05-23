import requests

BITTREX = {'url': 'https://api.bittrex.com/v3/markets', 'separator': '-', 'suffix': '/tickers'}
BITTREX_SUMMARY = {'url': 'https://api.bittrex.com/v3/markets/', 'separator': '-', 'suffix': '/summary'}
CURRENCIES = ('BTC', 'ETH', 'USDT', 'EOS', 'LTC', 'USD', 'EUR', 'DOGE', 'ADA', 'DGB', 'CGT', 'BCH', 'QNT', 'USDC',
              'VET', 'BSV')


def get_current_rate(base_curr_list, target_curr):
    url = BITTREX['url'] + BITTREX['suffix']
    data = data_request(url)
    if data is None:
        return None
    result = {}
    markets = []
    for base_curr in base_curr_list:
        markets.append(f'{base_curr}-{target_curr}')
    for market in data:
        if market['symbol'] in markets:
            currency = market['symbol'].split('-')[0]
            rate = float(market['lastTradeRate'])
            result[currency] = rate
    return result


def get_average_rate(base_curr, target_curr):
    url = BITTREX_SUMMARY['url'] + base_curr + \
          BITTREX_SUMMARY['separator'] + target_curr + BITTREX_SUMMARY['suffix']
    data = data_request(url)
    if data is None:
        return None
    lowest = float(data['low'])
    highest = float(data['high'])
    rate = (lowest + highest)/2
    return rate


def data_request(url):
    respond = requests.get(url)
    if respond.status_code != 200:
        return None
    else:
        return respond.json()
