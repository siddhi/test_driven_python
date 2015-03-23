from datetime import datetime

from .stock import Stock
from .rule import PriceRule


class AlertProcessor:
    def __init__(self, autorun=True, exchange=None):
        if exchange is None:
            self.exchange = {"GOOG": Stock("GOOG"), "AAPL": Stock("AAPL")}
        else:
            self.exchange = exchange
        rule_1 = PriceRule("GOOG", lambda stock: stock.price > 10)
        rule_2 = PriceRule("AAPL", lambda stock: stock.price > 5)
        self.exchange["GOOG"].updated.connect(
            lambda stock: print(stock.symbol, stock.price) \
                          if rule_1.matches(self.exchange) else None)
        self.exchange["AAPL"].updated.connect(
            lambda stock: print(stock.symbol, stock.price) \
                          if rule_2.matches(self.exchange) else None)
        if autorun:
            self.run()

    def do_updates(self, updates):
        for symbol, timestamp, price in updates:
            stock = self.exchange[symbol]
            stock.update(timestamp, price)

    def parse_file(self):
        updates = []
        with open("updates.csv", "r") as fp:
            for line in fp.readlines():
                symbol, timestamp, price = line.split(",")
                updates.append((symbol,
                       datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f"),
                       int(price)))
        return updates

    def run(self):
        updates = self.parse_file()
        self.do_updates(updates)
