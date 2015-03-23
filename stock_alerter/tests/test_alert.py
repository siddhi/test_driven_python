import unittest
from datetime import datetime

from ..alert import Alert
from ..rule import PriceRule
from ..stock import Stock


class TestAction:
    executed = False

    def execute(self, description):
        self.executed = True


class AlertTest(unittest.TestCase):
    def test_action_is_executed_when_rule_matches(self):
        exchange = {"GOOG": Stock("GOOG")}
        rule = PriceRule("GOOG", lambda stock: stock.price > 10)
        action = TestAction()
        alert = Alert("sample alert", rule, action)
        alert.connect(exchange)
        exchange["GOOG"].update(datetime(2014, 2, 10), 11)
        self.assertTrue(action.executed)
