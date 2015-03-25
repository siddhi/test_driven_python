class Processor:
    def __init__(self, reader, exchange):
        self.reader = reader
        self.exchange = exchange

    def process(self):
        for symbol, timestamp, price in self.reader.get_updates():
            stock = self.exchange[symbol]
            stock.update(timestamp, price)
