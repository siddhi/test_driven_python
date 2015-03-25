import doctest
import unittest
from stock_alerter import stock


class PackageDocTest(unittest.TestCase):
    def test_stock_module(self):
        doctest.testmod(stock)

    def test_doc(self):
        doctest.testfile(r"..\readme.txt")
