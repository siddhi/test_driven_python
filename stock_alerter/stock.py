from datetime import timedelta
from enum import Enum

from .event import Event
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
        self.updated = Event()

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
        self.updated.fire(self)

    def is_increasing_trend(self):
        return self.history[-3].value < self.history[-2].value < self.history[-1].value

    def _is_crossover_below_to_above(self, on_date, ma, reference_ma):
        prev_date = on_date - timedelta(1)
        return (ma.value_on(prev_date) < reference_ma.value_on(prev_date)
                and ma.value_on(on_date) > reference_ma.value_on(on_date))

    def get_crossover_signal(self, on_date):
        long_term_ma = MovingAverage(self.history, self.LONG_TERM_TIMESPAN)
        short_term_ma = MovingAverage(self.history, self.SHORT_TERM_TIMESPAN)
        try:
            if self._is_crossover_below_to_above(on_date, short_term_ma, long_term_ma):
                    return StockSignal.buy

            if self._is_crossover_below_to_above(on_date, long_term_ma, short_term_ma):
                    return StockSignal.sell
        except NotEnoughDataException:
            return StockSignal.neutral

        return StockSignal.neutral
