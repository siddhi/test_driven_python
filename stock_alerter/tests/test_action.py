import smtplib
import unittest
from unittest import mock

from ..action import PrintAction, EmailAction


class MessageMatcher:
    def __init__(self, expected):
        self.expected = expected

    def __eq__(self, other):
        return self.expected["Subject"] == other["Subject"] and \
            self.expected["From"] == other["From"] and \
            self.expected["To"] == other["To"] and \
            self.expected["Message"] == other._payload


@mock.patch("builtins.print")
class PrintActionTest(unittest.TestCase):
    def test_executing_action_prints_message(self, mock_print):
        action = PrintAction()
        action.execute("GOOG > $10")
        mock_print.assert_called_with("GOOG > $10")


class EmailActionTest(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch("smtplib.SMTP")
        self.addCleanup(patcher.stop)
        self.mock_smtp_class = patcher.start()
        self.mock_smtp = self.mock_smtp_class.return_value
        self.action = EmailAction(to="siddharta@silverstripesoftware.com")

    def test_email_is_sent_to_the_right_server(self):
        self.action.execute("MSFT has crossed $10 price level")
        self.mock_smtp_class.assert_called_with("email.stocks.com")

    def test_connection_closed_after_sending_mail(self):
        self.action.execute("MSFT has crossed $10 price level")
        self.mock_smtp.send_message.assert_called_with(mock.ANY)
        self.assertTrue(self.mock_smtp.quit.called)
        self.mock_smtp.assert_has_calls([
            mock.call.send_message(mock.ANY),
            mock.call.quit()])

    def test_connection_closed_if_send_gives_error(self):
        self.mock_smtp.send_message.side_effect = smtplib.SMTPServerDisconnected()
        try:
            self.action.execute("MSFT has crossed $10 price level")
        except Exception:
            pass
        self.assertTrue(self.mock_smtp.quit.called)

    def test_email_is_sent_with_the_right_subject(self):
        self.action.execute("MSFT has crossed $10 price level")
        call_args, _ = self.mock_smtp.send_message.call_args
        sent_message = call_args[0]
        self.assertEqual("New Stock Alert", sent_message["Subject"])

    def test_email_is_sent_when_action_is_executed(self):
        expected_message = {
            "Subject": "New Stock Alert",
            "Message": "MSFT has crossed $10 price level",
            "To": "siddharta@silverstripesoftware.com",
            "From": "alerts@stocks.com"
        }
        self.action.execute("MSFT has crossed $10 price level")
        self.mock_smtp.send_message.assert_called_with(
            MessageMatcher(expected_message))
