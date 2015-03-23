import bisect
import collections
from datetime import timedelta

PriceEvent = collections.namedtuple("PriceEvent", ["timestamp", "price"])


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.price_history = []

    @property
    def price(self):
        return self.price_history[-1].price \
            if self.price_history else None

    def update(self, timestamp, price):
        if price < 0:
            raise ValueError("price should not be negative")
        bisect.insort_left(self.price_history, PriceEvent(timestamp, price))

    def is_increasing_trend(self):
        return self.price_history[-3].price < \
            self.price_history[-2].price < self.price_history[-1].price

    def get_crossover_signal(self, on_date):
        closing_price_list = []
        for i in range(11):
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

        # Return NEUTRAL signal
        if len(closing_price_list) < 11:
            return 0

        # BUY signal
        if sum([update.price for update in closing_price_list[-11:-1]])/10 \
                > sum([update.price for update in closing_price_list[-6:-1]])/5 \
            and sum([update.price for update in closing_price_list[-10:]])/10 \
                < sum([update.price for update in closing_price_list[-5:]])/5:
                    return 1

        # BUY signal
        if sum([update.price for update in closing_price_list[-11:-1]])/10 \
                < sum([update.price for update in closing_price_list[-6:-1]])/5 \
            and sum([update.price for update in closing_price_list[-10:]])/10 \
                > sum([update.price for update in closing_price_list[-5:]])/5:
                    return -1

        # NEUTRAL signal
        return 0
