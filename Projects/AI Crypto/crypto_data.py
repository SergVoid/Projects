class CryptoCurrencyData:
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        # Словарь для хранения цен и объёмов по источникам
        self.prices = {}  

    def add_price(self, source, price, volume=None):
        # Сохраняем и цену, и объём в словарь для данного источника
        self.prices[source] = {"price": price, "volume": volume}

    def get_price_and_volume(self, source):
        # Возвращает кортеж (цена, объём) для данного источника
        if source in self.prices:
            price_info = self.prices[source]
            return price_info["price"], price_info["volume"]
        else:
            return None, None
