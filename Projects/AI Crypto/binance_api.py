import requests
from datetime import datetime

def get_price_and_volume_usdt_binance(symbol):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    params = {'symbol': symbol.upper() + "USDT"}
    start_time = datetime.now()
    response = requests.get(url, params=params)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"Request to Binance for {symbol} took {duration} seconds.")

    if response.status_code == 200:
        data = response.json()
        price = float(data['lastPrice'])
        volume = float(data['volume'])
        print(f"Binance price for {symbol}: {price}")
        print(f"Binance 24h volume for {symbol}: {volume}")

        return price, volume
    else:
        print(f"Error fetching {symbol} price from Binance: {response.status_code}")
        return None, None
