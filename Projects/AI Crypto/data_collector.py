from crypto_data import CryptoCurrencyData
from binance_api import get_price_usdt_binance
from coingecko_api import get_price_usd_coingecko
from coinmarketcap_api import get_price_usdt_coinmarketcap
from utils import format_price_and_volume

class CryptoDataCollector:
    def __init__(self):
        self.currencies_data = {}

    def add_currency(self, symbol):
        if symbol.upper() not in self.currencies_data:
            self.currencies_data[symbol.upper()] = CryptoCurrencyData(symbol)

    def fetch_price_usdt_binance(self, symbol):
        price, volume = get_price_usdt_binance(symbol)
        if price is not None:
            print(f"Received Binance price for {symbol}: {format_price_and_volume(price, volume)}")
            self.currencies_data[symbol.upper()].add_price('Binance', price, volume)

    def fetch_price_usd_coingecko(self, symbol):
        price, volume = get_price_usd_coingecko(symbol)
        if price is not None:
            formatted_price, formatted_volume = format_price_and_volume(price, volume)
            print(f"Received CoinGecko price for {symbol}: {formatted_price}, Volume: {formatted_volume}")
            self.currencies_data[symbol.upper()].add_price('CoinGecko', price, volume)

    def fetch_price_usdt_coinmarketcap(self, symbol, api_key):
        price, volume = get_price_usdt_coinmarketcap(symbol, api_key)
        if price is not None:
            formatted_price, formatted_volume = format_price_and_volume(price, volume)
            print(f"Received CoinMarketCap price for {symbol}: {formatted_price}, Volume: {formatted_volume}")
            self.currencies_data[symbol.upper()].add_price('CoinMarketCap', price, volume)
