import unittest

from stock_alerter.tests import test_stock

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(test_stock.suite())
