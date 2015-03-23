import unittest
from datetime import datetime

from ..stock import Stock
from ..rule import PriceRule, AndRule


class PriceRuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        goog = Stock("GOOG")
        goog.update(datetime(2014, 2, 10), 11)
        cls.exchange = {"GOOG": goog}

    def test_a_PriceRule_matches_when_it_meets_the_condition(self):
        rule = PriceRule("GOOG", lambda stock: stock.price > 10)
        self.assertTrue(rule.matches(self.exchange))

    def test_a_PriceRule_is_False_if_the_condition_is_not_met(self):
        rule = PriceRule("GOOG", lambda stock: stock.price < 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_PriceRule_is_False_if_the_stock_is_not_in_the_exchange(self):
        rule = PriceRule("MSFT", lambda stock: stock.price > 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_PriceRule_is_False_if_the_stock_hasnt_got_an_update_yet(self):
        self.exchange["AAPL"] = Stock("AAPL")
        rule = PriceRule("AAPL", lambda stock: stock.price > 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_PriceRule_only_depends_on_its_stock(self):
        rule = PriceRule("MSFT", lambda stock: stock.price > 10)
        self.assertEqual({"MSFT"}, rule.depends_on())


class AndRuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        goog = Stock("GOOG")
        goog.update(datetime(2014, 2, 10), 8)
        goog.update(datetime(2014, 2, 11), 10)
        goog.update(datetime(2014, 2, 12), 12)
        msft = Stock("MSFT")
        msft.update(datetime(2014, 2, 10), 10)
        msft.update(datetime(2014, 2, 11), 10)
        msft.update(datetime(2014, 2, 12), 12)
        redhat = Stock("RHT")
        redhat.update(datetime(2014, 2, 10), 7)
        cls.exchange = {"GOOG": goog, "MSFT": msft, "RHT": redhat}

    def test_an_AndRule_matches_if_all_component_rules_are_true(self):
        rule = AndRule(PriceRule("GOOG", lambda stock: stock.price > 8),
                       PriceRule("MSFT", lambda stock: stock.price > 10))
        self.assertTrue(rule.matches(self.exchange))
