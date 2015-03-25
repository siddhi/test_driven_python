import unittest
from datetime import datetime

from ..timeseries import TimeSeries


class TimeSeriesTestCase(unittest.TestCase):
    def assert_has_price_history(self, price_list, series):
        for index, expected_price in enumerate(price_list):
            actual_price = series[index].value
            if actual_price != expected_price:
                raise self.failureException("Price index {0}: {1} != {2}".format(
                    index, expected_price, actual_price))


class TimeSeriesEqualityTest(TimeSeriesTestCase):
    def test_timeseries_price_history(self):
        series = TimeSeries()
        series.update(datetime(2014, 3, 10), 5)
        series.update(datetime(2014, 3, 11), 15)
        self.assert_has_price_history([5, 15], series)
