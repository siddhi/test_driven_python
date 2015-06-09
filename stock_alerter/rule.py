class PriceRule:
    """PriceRule is a rule that triggers when a stock price satisfies a
    condition (usually greater, equal or lesser than a given value)"""

    def __init__(self, symbol, condition):
        self.symbol = symbol
        self.condition = condition

    def matches(self, exchange):
        try:
            stock = exchange[self.symbol]
        except KeyError:
            return False
        return self.condition(stock) if stock.price else False

    def depends_on(self):
        return set([self.symbol])


class TrendRule:
    """TrendRule is a rule that triggers when a stock price satisfies a
    trend (for now the only trend supported is 3 increasing updates)"""

    def __init__(self, symbol):
        self.symbol = symbol

    def matches(self, exchange):
        try:
            stock = exchange[self.symbol]
        except KeyError:
            return False
        return stock.is_increasing_trend()

    def depends_on(self):
        return set([self.symbol])


class AndRule:
    """AndRule triggers when all its component rules are true"""

    def __init__(self, *args):
        self.rules = args

    def matches(self, exchange):
        return all([rule.matches(exchange) for rule in self.rules])

    def depends_on(self):
        depends = set()
        for rule in self.rules:
            depends = depends.union(rule.depends_on())
        return depends
