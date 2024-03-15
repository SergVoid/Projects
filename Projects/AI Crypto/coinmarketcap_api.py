import requests

def get_price_usdt_coinmarketcap(symbol, api_key):
    headers = {'X-CMC_PRO_API_KEY': api_key}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {'symbol': symbol, 'convert': 'USDT'}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        price_info = data['data'][symbol.upper()]
        price = price_info['quote']['USDT']['price']
        return price
    else:
        print(f"Error fetching {symbol} price from CoinMarketCap: {response.status_code}")
        return None
