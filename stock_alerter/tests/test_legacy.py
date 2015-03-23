import unittest
from unittest import mock
from datetime import datetime

from ..legacy import AlertProcessor


class TestAlertProcessor(AlertProcessor):
    def __init__(self, exchange):
        AlertProcessor.__init__(self, autorun=False)
        self.exchange = exchange


class AlertProcessorTest(unittest.TestCase):
    @mock.patch("builtins.print")
    def test_processor_characterization_1(self, mock_print):
        AlertProcessor()
        mock_print.assert_has_calls([mock.call("AAPL", 8),
                                     mock.call("GOOG", 15),
                                     mock.call("AAPL", 10),
                                     mock.call("GOOG", 21)])

    def test_processor_characterization_2(self):
        processor = AlertProcessor(autorun=False)
        with mock.patch("builtins.print") as mock_print:
            processor.run()
        mock_print.assert_has_calls([mock.call("AAPL", 8),
                                     mock.call("GOOG", 15),
                                     mock.call("AAPL", 10),
                                     mock.call("GOOG", 21)])

    def test_processor_characterization_3(self):
        processor = AlertProcessor(autorun=False)
        mock_goog = mock.Mock()
        processor.exchange = {"GOOG": mock_goog}
        updates = [("GOOG", datetime(2014, 12, 8), 5)]
        processor.do_updates(updates)
        mock_goog.update.assert_called_with(datetime(2014, 12, 8), 5)

    def test_processor_characterization_4(self):
        mock_goog = mock.Mock()
        mock_aapl = mock.Mock()
        exchange = {"GOOG": mock_goog, "AAPL": mock_aapl}
        processor = AlertProcessor(autorun=False, exchange=exchange)
        updates = [("GOOG", datetime(2014, 12, 8), 5)]
        processor.do_updates(updates)
        mock_goog.update.assert_called_with(datetime(2014, 12, 8), 5)

    def test_processor_characterization_5(self):
        mock_goog = mock.Mock()
        mock_aapl = mock.Mock()
        exchange = {"GOOG": mock_goog, "AAPL": mock_aapl}
        processor = TestAlertProcessor(exchange)
        updates = [("GOOG", datetime(2014, 12, 8), 5)]
        processor.do_updates(updates)
        mock_goog.update.assert_called_with(datetime(2014, 12, 8), 5)

    def test_processor_characterization_6(self):
        processor = AlertProcessor(autorun=False)
        processor.do_updates = mock.Mock()
        processor.run()
        processor.do_updates.assert_called_with([
            ('GOOG', datetime(2014, 2, 11, 14, 10, 22, 130000), 5),
            ('AAPL', datetime(2014, 2, 11, 0, 0), 8),
            ('GOOG', datetime(2014, 2, 11, 14, 11, 22, 130000), 3),
            ('GOOG', datetime(2014, 2, 11, 14, 12, 22, 130000), 15),
            ('AAPL', datetime(2014, 2, 11, 0, 0), 10),
            ('GOOG', datetime(2014, 2, 11, 14, 15, 22, 130000), 21)])

    def test_processor_characterization_7(self):
        processor = AlertProcessor(autorun=False)
        processor.parse_file = mock.Mock()
        processor.parse_file.return_value = [
            ('GOOG', datetime(2014, 2, 11, 14, 12, 22, 130000), 15)]
        with mock.patch("builtins.print") as mock_print:
            processor.run()
        mock_print.assert_called_with("GOOG", 15)
