import unittest
from datetime import datetime

from ..timeseries import TimeSeries


class TimeSeriesTest(unittest.TestCase):
    def test_closing_price_list_before_series_start_date(self):
        """Empty list is returned if on_date is before the start of the series

        The moving average calculation might be done before any data has been
        added to the stock. We return an empty list so that the calculation can
        still proceed as usual.
        """
        series = TimeSeries()
        series.update(datetime(2014, 3, 10), 5)
        on_date = datetime(2014, 3, 9)
        self.assertEqual([],
                         series.get_closing_price_list(on_date, 1))


class TimeSeriesTestCase(unittest.TestCase):
    def assert_has_price_history(self, price_list, series):
        for index, expected_price in enumerate(price_list):
            actual_price = series[index].value
            if actual_price != expected_price:
                raise self.failureException("Price index %d: %d != %d".format(
                    index, expected_price, actual_price))


class TimeSeriesEqualityTest(unittest.TestCase):
    def test_timeseries_price_history(self):
        series = TimeSeries()
        series.update(datetime(2014, 3, 10), 5)
        series.update(datetime(2014, 3, 11), 15)
        self.assertEqual(5, series[0].value)
        self.assertEqual(15, series[1].value)
