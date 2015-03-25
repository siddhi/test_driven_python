The stock_alerter module allows you to setup rules and get alerted when
those rules are met.

>>> from datetime import datetime

First, we need to setup an exchange which contains all the stocks that
are going to be processed. A simple dictionary will do.

>>> from stock_alerter.stock import Stock
>>> exchange = {"GOOG": Stock("GOOG"), "AAPL": Stock("AAPL")}
>>> for key in sorted(exchange.keys()):
...    print(key, exchange[key])
...    
AAPL       <stock_alerter.stock.Stock object at 0x0...>
GOOG       <stock_alerter.stock.Stock object at 0x0...>

Next, we configure the reader. The reader is the source from where the
stock updates are coming. The module provides two readers out of the
box: A FileReader for reading updates from a comma separated file,
and a ListReader to get updates from a list. You can create other
readers, such as an HTTPReader to get updates from a remote server.
Here we create a simple ListReader by passing in a list of 3-tuples
containing the stock symbol, timestamp and price.

>>> from stock_alerter.reader import ListReader
>>> reader = ListReader([("GOOG", datetime(2014, 2, 8), 5)])

Next, we setup an Alert. We give it a rule, and an action to be taken
when the rule is fired.

>>> from stock_alerter.alert import Alert
>>> from stock_alerter.rule import PriceRule
>>> from stock_alerter.action import PrintAction
>>> alert = Alert("GOOG > $3", PriceRule("GOOG", lambda s: s.price > 3),\
...               PrintAction())

Connect the alert to the exchange

>>> alert.connect(exchange)

Now that everything is setup, we can start processing the updates

>>> from stock_alerter.processor import Processor
>>> processor = Processor(reader, exchange)
>>> processor.process()
GOOG > $3
