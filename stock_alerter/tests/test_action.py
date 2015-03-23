import smtplib
import unittest
from unittest import mock

from ..action import PrintAction, EmailAction


@mock.patch("builtins.print")
class PrintActionTest(unittest.TestCase):
    def test_executing_action_prints_message(self, mock_print):
        action = PrintAction()
        action.execute("GOOG > $10")
        mock_print.assert_called_with("GOOG > $10")


@mock.patch("smtplib.SMTP")
class EmailActionTest(unittest.TestCase):
    def setUp(self):
        self.action = EmailAction(to="siddharta@silverstripesoftware.com")

    def test_email_is_sent_to_the_right_server(self, mock_smtp_class):
        self.action.execute("MSFT has crossed $10 price level")
        mock_smtp_class.assert_called_with("email.stocks.com")
