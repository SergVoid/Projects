import requests

def get_price_usd_coingecko(symbol):
    coingecko_ids = {'BTC': 'bitcoin', 'ETH': 'ethereum', 'BNB': 'binancecoin'}
    symbol_id = coingecko_ids.get(symbol.upper())
    if symbol_id:
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {'ids': symbol_id, 'vs_currencies': 'usd'}  # Используем 'usd'
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'usd' in data[symbol_id]:  # Убедитесь, что используете правильный ключ
                price = data[symbol_id]['usd']
                print(f"CoinGecko price for {symbol}: {price} USD")
                return price
            else:
                print(f"Price in USD for {symbol} is not available from CoinGecko.")
        else:
            print(f"Error fetching {symbol} from CoinGecko: {response.status_code}")
    else:
        print(f"{symbol} is not a supported symbol in CoinGecko")
    return None
