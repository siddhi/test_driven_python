import unittest
from unittest import mock

from ..action import PrintAction


class PrintActionTest(unittest.TestCase):
    def test_executing_action_prints_message(self):
        with mock.patch('builtins.print') as mock_print:
            action = PrintAction()
            action.execute("GOOG > $10")
            mock_print.assert_called_with("GOOG > $10")
