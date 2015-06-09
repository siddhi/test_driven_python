import unittest
from datetime import datetime

from ..stock import Stock
from ..rule import PriceRule, TrendRule, AndRule


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
        self.assertEqual(set(["MSFT"]), rule.depends_on())


class TrendRuleTest(unittest.TestCase):
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
        cls.exchange = {"GOOG": goog, "MSFT": msft}

    def test_a_TrendRule_matches_if_the_stock_increased_last_3_updates(self):
        rule = TrendRule("GOOG")
        self.assertTrue(rule.matches(self.exchange))

    def test_a_TrendRule_is_False_if_stock_doesnt_increasing_trend(self):
        rule = TrendRule("MSFT")
        self.assertFalse(rule.matches(self.exchange))

    def test_a_TrendRule_is_False_if_stock_is_not_in_the_exchange(self):
        rule = TrendRule("APPL")
        self.assertFalse(rule.matches(self.exchange))

    def test_a_TrendRule_is_False_if_the_stock_hasnt_got_an_update_yet(self):
        self.exchange["AAPL"] = Stock("AAPL")
        rule = PriceRule("AAPL", lambda price: price > 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_TrendRule_only_depends_on_its_stock(self):
        rule = TrendRule("AAPL")
        self.assertEqual(set(["AAPL"]), rule.depends_on())


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

    def test_an_AndRule_is_False_if_any_component_is_false(self):
        rule = AndRule(PriceRule("GOOG", lambda stock: stock.price > 15),
                       PriceRule("MSFT", lambda stock: stock.price > 10))
        self.assertFalse(rule.matches(self.exchange))

    def test_an_AndRule_should_support_any_number_of_subrules(self):
        rule = AndRule(PriceRule("RHT", lambda stock: stock.price < 10),
                       PriceRule("GOOG", lambda stock: stock.price > 8),
                       PriceRule("MSFT", lambda stock: stock.price > 10))
        self.assertTrue(rule.matches(self.exchange))

    def test_an_empty_AndRule_is_true(self):
        rule = AndRule()
        self.assertTrue(rule.matches(self.exchange))

    def test_an_AndRule_can_be_nested(self):
        rule = AndRule(PriceRule("RHT", lambda stock: stock.price < 10),
                       AndRule(PriceRule("GOOG", lambda stock: stock.price > 8),
                               PriceRule("MSFT", lambda stock: stock.price > 10)))
        self.assertTrue(rule.matches(self.exchange))

    def test_an_AndRule_depends_on_what_the_component_rules_depend_on(self):
        rule = AndRule(PriceRule("AAPL", lambda stock: stock.price < 10),
                       PriceRule("GOOG", lambda stock: stock.price > 8))
        self.assertEqual(set(["AAPL", "GOOG"]), rule.depends_on())

    def test_depends_on_should_not_have_duplicates(self):
        rule = AndRule(PriceRule("AAPL", lambda stock: stock.price < 10),
                       PriceRule("AAPL", lambda stock: stock.price > 5))
        self.assertEqual(set(["AAPL"]), rule.depends_on())
