import unittest
from unittest import mock

from ..action import PrintAction


class PrintActionTest(unittest.TestCase):
    def test_executing_action_prints_message(self):
        mock_print = mock.Mock()
        old_print = __builtins__["print"]
        __builtins__["print"] = mock_print
        try:
            action = PrintAction()
            action.execute("GOOG > $10")
            mock_print.assert_called_with("GOOG > $10")
        finally:
            __builtins__["print"] = old_print
