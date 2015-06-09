from __future__ import print_function
from datetime import datetime

from .stock import Stock
from .rule import PriceRule


class FileReader:
    def __init__(self, filename):
        self.filename = filename

    def get_updates(self):
        updates = []
        with open("updates.csv", "r") as fp:
            for line in fp.readlines():
                symbol, timestamp, price = line.split(",")
                updates.append((symbol,
                       datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f"),
                       int(price)))
        return updates


class AlertProcessor:
    def __init__(self, autorun=True, reader=None, exchange=None):
        self.reader = reader if reader else FileReader("updates.csv")
        if exchange is None:
            self.exchange = {"GOOG": Stock("GOOG"), "AAPL": Stock("AAPL")}
        else:
            self.exchange = exchange
        rule_1 = PriceRule("GOOG", lambda stock: stock.price > 10)
        rule_2 = PriceRule("AAPL", lambda stock: stock.price > 5)
        self.exchange["GOOG"].updated.connect(
            lambda stock: self.print_action(stock, rule_1))
        self.exchange["AAPL"].updated.connect(
            lambda stock: self.print_action(stock, rule_2))
        if autorun:
            self.run()

    def print_action(self, stock, rule):
        print(stock.symbol, stock.price) \
            if rule.matches(self.exchange) else None

    def run(self):
        updates = self.parse_file()
        self.do_updates(updates)

    def parse_file(self):
        return self.reader.get_updates()

    def do_updates(self, updates):
        for symbol, timestamp, price in updates:
            stock = self.exchange[symbol]
            stock.update(timestamp, price)
