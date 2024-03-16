import requests
from datetime import datetime

# Маппинг тикеров к идентификаторам CoinGecko
TICKER_TO_COINGECKO_ID = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "BNB": "binancecoin",
    # Добавьте другие валюты по необходимости
}

def get_price_usd_coingecko(ticker):
    symbol_id = TICKER_TO_COINGECKO_ID.get(ticker.upper(), None)
    if not symbol_id:
        print(f"CoinGecko does not support the ticker: {ticker}")
        return None, None

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': symbol_id,
        'vs_currencies': 'usd',
        'include_market_cap': 'true',  # Для получения объёма торгов
    }
    start_time = datetime.now()
    response = requests.get(url, params=params)
    end_time = datetime.now()
    print(f"Request to CoinGecko for {ticker} ({symbol_id}) took {(end_time - start_time).total_seconds()} seconds.")

    if response.status_code == 200:
        data = response.json()
        price = data[symbol_id]['usd']
        volume = data[symbol_id].get('usd_market_cap', None)  # Объём торгов может быть не доступен
        print(f"CoinGecko price for {ticker} ({symbol_id}): {price} USD, Volume: {volume}")
        return price, volume
    else:
        print(f"Error fetching {ticker} ({symbol_id}) price from CoinGecko: {response.status_code}")
        return None, None