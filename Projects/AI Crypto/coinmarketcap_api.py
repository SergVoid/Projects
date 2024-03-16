import requests
from datetime import datetime

def get_price_usdt_coinmarketcap(symbol, api_key):
    headers = {'X-CMC_PRO_API_KEY': api_key}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {'symbol': symbol, 'convert': 'USDT'}
    start_time = datetime.now()
    response = requests.get(url, headers=headers, params=params)
    end_time = datetime.now()
    print(f"Request to CoinMarketCap for {symbol} took {(end_time - start_time).total_seconds()} seconds.")

    if response.status_code == 200:
        data = response.json()
        price_info = data['data'][symbol.upper()]
        price = price_info['quote']['USDT']['price']
        # Добавим поддержку объёма, если он доступен
        volume = price_info['quote']['USDT'].get('volume_24h', None)
        print(f"CoinMarketCap price for {symbol}: {price}")
        return price, volume
    else:
        print(f"Error fetching {symbol} price from CoinMarketCap: {response.status_code}")
        return None, None
