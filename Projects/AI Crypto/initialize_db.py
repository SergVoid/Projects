import database_manager

def initialize_database():
    # Добавляем валюты
    database_manager.add_symbol('BTC', 'Bitcoin')
    database_manager.add_symbol('ETH', 'Ethereum')
    database_manager.add_symbol('BNB', 'Binance Coin')

    # Добавляем источники
    database_manager.add_source('Binance')
    database_manager.add_source('CoinMarketCap', api_key='7943aa0d-539f-4907-8f75-97aea4834a25')
    database_manager.add_source('CoinGecko')

if __name__ == "__main__":
    initialize_database()
    print("Database initialized with symbols and sources.")
