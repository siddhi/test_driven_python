from datetime import timedelta
from enum import Enum

from .timeseries import TimeSeries, MovingAverage, NotEnoughDataException


class StockSignal(Enum):
    buy = 1
    neutral = 0
    sell = -1


class Stock:
    LONG_TERM_TIMESPAN = 10
    SHORT_TERM_TIMESPAN = 5

    def __init__(self, symbol):
        self.symbol = symbol
        self.history = TimeSeries()

    @property
    def price(self):
        try:
            return self.history[-1].value
        except IndexError:
            return None

    def update(self, timestamp, price):
        if price < 0:
            raise ValueError("price should not be negative")
        self.history.update(timestamp, price)

    def is_increasing_trend(self):
        return self.history[-3].value < self.history[-2].value < self.history[-1].value

    def _get_closing_price_list(self, on_date, num_days):
        closing_price_list = []
        for i in range(num_days):
            chk = on_date.date() - timedelta(i)
            for price_event in reversed(self.price_history):
                if price_event.timestamp.date() > chk:
                    pass
                if price_event.timestamp.date() == chk:
                    closing_price_list.insert(0, price_event)
                    break
                if price_event.timestamp.date() < chk:
                    closing_price_list.insert(0, price_event)
                    break
        return closing_price_list

    def _is_crossover_below_to_above(self, prev_ma, prev_reference_ma,
                                     current_ma, current_reference_ma):
        return prev_ma < prev_reference_ma and current_ma > current_reference_ma

    def get_crossover_signal(self, on_date):
        long_term_ma = MovingAverage(self.history, self.LONG_TERM_TIMESPAN)
        short_term_ma = MovingAverage(self.history, self.SHORT_TERM_TIMESPAN)
        try:
            long_term_ma_value = long_term_ma.value_on(on_date, self.LONG_TERM_TIMESPAN)
            prev_long_term_ma_value = long_term_ma.value_on(on_date-timedelta(1), self.LONG_TERM_TIMESPAN)
            short_term_ma_value = short_term_ma.value_on(on_date, self.SHORT_TERM_TIMESPAN)
            prev_short_term_ma_value = short_term_ma.value_on(on_date-timedelta(1), self.SHORT_TERM_TIMESPAN)
        except NotEnoughDataException:
            return StockSignal.neutral

        if self._is_crossover_below_to_above(prev_short_term_ma_value, prev_long_term_ma_value,
                                             short_term_ma_value, long_term_ma_value):
                return StockSignal.buy

        if self._is_crossover_below_to_above(prev_long_term_ma_value, prev_short_term_ma_value,
                                             long_term_ma_value, short_term_ma_value):
                return StockSignal.sell

        return StockSignal.neutral
