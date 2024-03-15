# -*- coding: utf-8 -*-
# Не забудьте добавить импорты в начало файла
from datetime import datetime
import schedule
import time
from data_collector import CryptoDataCollector
from utils import format_price

api_key = '7943aa0d-539f-4907-8f75-97aea4834a25' # CoinMarketCap Api-key

def fetch_and_display_prices():
    print(f"\nFetching prices started at {datetime.now()}\n")
    collector = CryptoDataCollector()
    symbols = ['BTC', 'ETH', 'BNB']
    sources = ['Binance', 'CoinMarketCap', 'CoinGecko']

    for symbol in symbols:  # Добавляем криптовалюты в коллектор
        collector.add_currency(symbol)

    for source in sources:  # Внешний цикл по источникам данных
        print(f"Fetching prices from {source}...")
        for symbol in symbols:
            if source == 'Binance':
                collector.fetch_price_usdt_binance(symbol)
            elif source == 'CoinGecko':
                collector.fetch_price_usd_coingecko(symbol)
            elif source == 'CoinMarketCap':
                collector.fetch_price_usdt_coinmarketcap(symbol, api_key)

    header = "Currency\t" + "\t".join(sources)  # Вывод данных в виде таблицы
    print(header)
    print("-" * len(header))

    for symbol in symbols:
        row = [symbol]
        for source in sources:
            price = collector.currencies_data[symbol.upper()].get_price(source)
            row.append(format_price(price) if price else "N/A")
        print("\t".join(row))
    
    print(f"\nFetching prices finished at {datetime.now()}\n")

if __name__ == "__main__":
    fetch_and_display_prices()  # Сначала выполняем задачу немедленно
    schedule.every(1).minutes.do(fetch_and_display_prices)  # Затем настраиваем расписание для её периодического выполнения каждую минуту
    
    print("The script is set up to fetch cryptocurrency prices every minute.")
    print("Press Ctrl+C to stop.")

    try:    # Запуск цикла для выполнения запланированных задач
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script stopped by user.")
