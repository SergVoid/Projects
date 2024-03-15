class CryptoCurrencyData:
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.prices = {}  # Изменим на словарь для хранения цен по источникам

    def add_price(self, source, price):
        self.prices[source] = price

    def get_price(self, source):
        return self.prices.get(source)