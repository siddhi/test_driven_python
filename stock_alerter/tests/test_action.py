import unittest
from unittest import mock

from ..action import PrintAction


class PrintActionTest(unittest.TestCase):
    def test_executing_action_prints_message(self):
        patcher = mock.patch('builtins.print')
        mock_print = patcher.start()
        try:
            action = PrintAction()
            action.execute("GOOG > $10")
            mock_print.assert_called_with("GOOG > $10")
        finally:
            patcher.stop()
