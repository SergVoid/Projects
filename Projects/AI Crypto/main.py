   # -*- coding: utf-8 -*-
from datetime import datetime
import database_manager
import schedule
import time
from data_collector import CryptoDataCollector

def fetch_prices():
    start_time = datetime.now()
    session_timestamp = datetime.now()
    print(f"\nFetching prices started at {start_time}\n")

    collector = CryptoDataCollector()

    # Получение списка активных символов и источников
    symbols = database_manager.get_active_symbols()
    sources = database_manager.get_active_sources()

    for symbol in symbols:
        collector.add_currency(symbol)

    for source_name in sources:
        for symbol in symbols:
            # Получаем ID для символа и источника
            symbol_id = database_manager.get_symbol_id(symbol)
            source_id = database_manager.get_source_id(source_name)

            # Проверяем, откуда получать данные
            if source_name == 'Binance':
                collector.fetch_price_usdt_binance(symbol)          
            # Получаем цену и объем из данных, собранных collector'ом
            # Убедитесь, что метод add_price возвращает также объем, если это необходимо
            price, volume = collector.currencies_data[symbol.upper()].get_price_and_volume(source_name)
            
            if symbol_id and source_id and price is not None:
                database_manager.add_price_data(symbol_id, source_id, price, volume, session_timestamp)
                print(f"Данные для {symbol} от {source_name} успешно добавлены.")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"Fetching prices finished at {end_time}, duration: {duration} seconds\n")

def display_prices_table():
    data = database_manager.get_price_data()
    print(f"{'Currency':<8} {'Source':<15} {'Price':>10} {'Volume 24H in token':>25} {'Timestamp'}")
    print("-" * 85)

    for row in data:
        ticker, source_name, price, volume_24_token, timestamp = row 
        print(f"{ticker:<8} {source_name:<15} {price:>10.2f} {volume_24_token:>25.2f} {timestamp}")

# Пример логирования длительности запроса (не включено в таблицу)
def log_request_duration(source_name, duration):
    print(f"Request to {source_name} took {duration:.2f} seconds.")


if __name__ == "__main__":
    fetch_prices()
    display_prices_table()
    # Здесь может быть ваше расписание для регулярного выполнения fetch_prices
    # Например, запускать fetch_prices каждую минуту
    schedule.every(1).minutes.do(fetch_prices)
    schedule.every(1).minutes.do(display_prices_table)
    print("Script is set up to fetch cryptocurrency prices every 1 minutes.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script stopped by user.")
