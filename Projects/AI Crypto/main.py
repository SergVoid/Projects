# -*- coding: utf-8 -*-
from datetime import datetime
import schedule
import time
from data_collector import CryptoDataCollector
from utils import format_price

COINMARKETCAP_API_KEY = '7943aa0d-539f-4907-8f75-97aea4834a25'

def fetch_prices():
    start_time = datetime.now()
    print(f"\nFetching prices started at {start_time}\n")

    collector = CryptoDataCollector()
    symbols = ['BTC', 'ETH', 'BNB']
    sources = ['Binance', 'CoinMarketCap', 'CoinGecko']

    for symbol in symbols:
        collector.add_currency(symbol)

    for source in sources:
        print(f"Fetching prices from {source}...")
        for symbol in symbols:
            if source == 'Binance':
                collector.fetch_price_usdt_binance(symbol)
            elif source == 'CoinGecko':
                collector.fetch_price_usd_coingecko(symbol)
            elif source == 'CoinMarketCap':
                collector.fetch_price_usdt_coinmarketcap(symbol, COINMARKETCAP_API_KEY)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"Fetching prices finished at {end_time}, duration: {duration} seconds\n")

    return collector, sources, start_time, end_time, duration

def display_prices_table(collector, sources, start_time, end_time, duration):
    # Форматируем время начала и окончания с целыми секундами
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Выводим информацию о времени сбора данных и его продолжительности
    print(f"Data collection started at {start_time_str} and finished at {end_time_str}, duration: {int(duration)} seconds\n")
    
    # Текущее время для отметки времени данных
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Current data timestamp: {current_time_str}\n")
    
    header = "Currency\t" + "\t".join(sources)
    print(header)
    print("-" * len(header))

    symbols = collector.currencies_data.keys()
    for symbol in symbols:
        row = [symbol]
        for source in sources:
            price = collector.currencies_data[symbol].get_price(source)
            row.append(format_price(price) if price else "N/A")
        print("\t".join(row))

if __name__ == "__main__":
    # Сначала выполняем задачу немедленно
    collector, sources, start_time, end_time, duration = fetch_prices()
    display_prices_table(collector, sources, start_time, end_time, duration)

    # Настройка расписания для её периодического выполнения каждую 5 минуту
    def scheduled_job():
        collector, sources, start_time, end_time, duration = fetch_prices()
        display_prices_table(collector, sources, start_time, end_time, duration)

    schedule.every(5).minutes.do(scheduled_job)
    
    print("The script is set up to fetch cryptocurrency prices every minute.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script stopped by user.")
