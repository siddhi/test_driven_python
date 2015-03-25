import doctest
from datetime import datetime

from stock_alerter import stock


def setup_stock_doctest(doctest):
    s = stock.Stock("GOOG")
    doctest.globs.update({"stock": s})


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite(stock, globs={
        "datetime": datetime,
        "Stock": stock.Stock
    }, setUp=setup_stock_doctest))
    options = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    tests.addTests(doctest.DocFileSuite("readme.txt", package="stock_alerter", optionflags=options))
    return tests
