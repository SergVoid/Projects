# -*- coding: utf-8 -*-
from datetime import datetime
from data_collector import CryptoDataCollector
from utils import format_price

def main():
    collector = CryptoDataCollector()
    symbols = ['BTC', 'ETH', 'BNB']
    sources = ['Binance', 'CoinGecko']

    # Фиксация времени начала запросов
    start_time = datetime.now()
    # Добавляем криптовалюты в коллектор
    for symbol in symbols:
        collector.add_currency(symbol)

    # Внешний цикл по источникам данных
    for source in sources:
        print(f"Fetching prices from {source}...")
        for symbol in symbols:
            if source == 'Binance':
                collector.fetch_price_usdt_binance(symbol)
            elif source == 'CoinGecko':
                collector.fetch_price_usd_coingecko(symbol)

    # Фиксация времени окончания запросов и расчёт затраченного времени
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    
    print(f"\nTotal time for API requests: {total_time} seconds\n")
    
    # Вывод данных в виде таблицы
    header = "Currency\t" + "\t".join(sources)
    print(header)
    print("-" * len(header))

    for symbol in symbols:
        row = [symbol]
        for source in sources:
            price = collector.currencies_data[symbol.upper()].get_price(source)
            row.append(format_price(price) if price else "N/A")
        print("\t".join(row))

if __name__ == "__main__":
    main()