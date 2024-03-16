import requests
from datetime import datetime

def get_price_usdt_binance(symbol):
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {'symbol': symbol.upper() + "USDT"}
    start_time = datetime.now()
    response = requests.get(url, params=params)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"Request to Binance for {symbol} took {duration} seconds.")

    if response.status_code == 200:
        data = response.json()
        price = float(data['price'])
        print(f"Binance price for {symbol}: {price}")

        # Пример, где объём не получен напрямую от API в этом запросе.
        # Возвращаем None для объёма, чтобы сохранить согласованность интерфейса функции.
        volume = None  

        return price, volume
    else:
        print(f"Error fetching {symbol} price from Binance: {response.status_code}")
        return None, None
