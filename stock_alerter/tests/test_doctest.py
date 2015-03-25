import doctest
from stock_alerter import stock


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite(stock))
    tests.addTests(doctest.DocFileSuite("../readme.txt"))
    return tests
