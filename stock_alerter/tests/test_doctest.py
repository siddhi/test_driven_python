import doctest
from datetime import datetime

from stock_alerter import stock


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite(stock, globs={
        "datetime": datetime,
        "Stock": stock.Stock
    }))
    tests.addTests(doctest.DocFileSuite("../readme.txt"))
    return tests
