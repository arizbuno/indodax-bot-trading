from tradingview_ta import Interval, Exchange
import Trading

analysis = Trading.PreBid('BTCIDR', 'crypto', 'BITFINEX', Interval.INTERVAL_1_MINUTE)
analysis.action()
