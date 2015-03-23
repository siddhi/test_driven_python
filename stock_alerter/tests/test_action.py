import unittest
from unittest import mock

from ..action import PrintAction


class PrintActionTest(unittest.TestCase):
    @mock.patch("builtins.print")
    def test_executing_action_prints_message(self, mock_print):
        action = PrintAction()
        action.execute("GOOG > $10")
        mock_print.assert_called_with("GOOG > $10")
