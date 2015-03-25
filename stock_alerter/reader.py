from datetime import datetime


class ListReader:
    """Reads a series of updates from a list"""
    def __init__(self, updates):
        self.updates = updates

    def get_updates(self):
        for update in self.updates:
            yield update


class FileReader:
    """Reads a series of stock updates from a file"""
    def __init__(self, filename):
        self.filename = filename

    def get_updates(self):
        """Returns the next update everytime the method is called"""
        with open(self.filename, "r") as fp:
            data = fp.read()
            lines = data.split()
            for line in lines:
                symbol, timestamp, price = line.split(",")
                yield (symbol,
                       datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f"),
                       int(price))
