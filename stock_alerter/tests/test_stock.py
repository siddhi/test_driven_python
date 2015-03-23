import unittest
from datetime import datetime

from ..stock import Stock


class StockTest(unittest.TestCase):
    def test_price_of_a_new_stock_class_should_be_None(self):
        stock = Stock("GOOG")
        self.assertIsNone(stock.price)

    def test_stock_update(self):
        """An update should set the price on the stock object

        We will be  using the `datetime` module for the timestamp
        """
        goog = Stock("GOOG")
        goog.update(datetime(2014, 2, 12), price=10)
        self.assertEqual(10, goog.price)

    def test_negative_price_should_throw_ValueError(self):
        goog = Stock("GOOG")
        with self.assertRaises(ValueError):
            goog.update(datetime(2014, 2, 13), -1)

    def test_stock_price_should_give_the_latest_price(self):
        goog = Stock("GOOG")
        goog.update(datetime(2014, 2, 12), price=10)
        goog.update(datetime(2014, 2, 13), price=8.4)
        self.assertAlmostEqual(8.4, goog.price, delta=0.0001)
