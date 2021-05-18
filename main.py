from indodax.indodax import indodax as indodax_client
from tradingview_ta import Interval, Exchange
import Trading

KEY = ''
SECRET = b''

indodax = indodax_client(KEY, SECRET)

analysis = Trading.PreBid('BTCIDR', 'crypto', 'BITFINEX', Interval.INTERVAL_1_MINUTE, buy_preference='BUY')

if analysis.action():
  trade_buy = Trading.TradeBuy(indodax, 'btc', 200000)
  trade_buy.action()

