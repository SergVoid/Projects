import requests
from datetime import datetime

def format_price(price):
    return f"${float(price):,.2f}"

def get_price_usdt_binance(currencies=['BTCUSDT', 'ETHUSDT', 'LTCUSDT', 'BNBUSDT']):
    url = "https://api.binance.com/api/v3/ticker/price"
    print("Prices from Binance:")
    for currency in currencies:
        response = requests.get(url, params={'symbol': currency})
        data = response.json()
        if response.status_code == 200:
            # Форматирование названия криптовалюты для единообразия
            formatted_currency = currency[:-4] + " (USDT)"
            print(f"The current price of {formatted_currency} is: {format_price(data['price'])}")
        else:
            print(f"Could not retrieve price for {currency}")

def retrieve_data():
    # Получаем и выводим текущее время
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Data retrieved at: {current_time}\n")
    
    # Получение цен с Binance
    get_price_usdt_binance()

# Запуск функции для вывода цен на экран
retrieve_data()
