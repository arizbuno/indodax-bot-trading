from indodax.indodax import indodax as indodax_client
from tradingview_ta import TA_Handler
import time
import random

class TradingState:
  def action(self):
    pass

class PreBid(TradingState):
  def __init__(self, symbol, screener, exchange, interval, buy_preference='STRONG_BUY', min_wait=15, max_wait=30):
    self._symbol = symbol
    self._screener = screener
    self._exchange = exchange
    self._interval = interval
    self._buy_preference = buy_preference
    self._min_wait = min_wait
    self._max_wait = max_wait

  def action(self):
    while True:
      try:
        if Utilities.analyze(self._symbol, self._screener, self._exchange, self._interval) == self._buy_preference:
          return True
        Utilities.wait_random(self._min_wait, self._max_wait)
      except Exception as error:
        print(error)

class TradeBuy(TradingState):
  def __init__(self, indodax, coin, amount, idr_or_btc='idr'):
    self._indodax = indodax
    self._coin = coin
    self._amount = amount
    self._with_idr = idr_or_btc

  def action(self):
    market_sell_price = float(indodax_client.get_price(self._coin)['ticker']['sell'])
    market_buy_price = float(indodax_client.get_price(self._coin)['ticker']['buy'])
    print(Utilities.dye_str(f"Buying {self._coin} at: {market_sell_price}", 'GREEN'))
    buy_order_id = self._indodax.trade_buy(self._coin, market_sell_price, self._amount, self._idr_or_btc)['return']['orders'][0]
    
    return True

class Utilities:
  def analyze(symbol, screener, exchange, interval):
    coin = TA_Handler(
      symbol=symbol,
      screener=screener,
      exchange=exchange,
      interval=interval
    )
    coin_summary = coin.get_analysis().summary

    recommendation = coin_summary['RECOMMENDATION']
    coin_recommendation = f"{symbol} {recommendation}"
    coin_buy = str(coin_summary['BUY'])
    coin_sell = str(coin_summary['SELL'])
    coin_neutral = str(coin_summary['NEUTRAL'])

    recommendation_with_color = Utilities.dye_str(coin_recommendation, 'YELLOW')
    if coin_recommendation[-3:len(coin_recommendation)] == 'BUY':
      recommendation_with_color = Utilities.dye_str(coin_recommendation, 'GREEN')
    elif coin_recommendation[-4:len(coin_recommendation)] == 'SELL':
      recommendation_with_color = Utilities.dye_str(coin_recommendation, 'RED')
    
    print(f"{recommendation_with_color} | {Utilities.dye_str('BUY: ' + coin_buy, 'GREEN')} | {Utilities.dye_str('SELL: ' + coin_sell, 'RED')} | {Utilities.dye_str('NEUTRAL: ' + coin_neutral, 'YELLOW')}")
    return recommendation

  def dye_str(string, color):
    color_code = {
      'GREEN': '\033[92m',
      'YELLOW': '\033[93m',
      'RED': '\033[91m',
      'RESET': '\033[0m'
    }
    return f"{color_code[color]}{string}{color_code['RESET']}"

  def wait_random(min_wait, max_wait):
    rand_time_s = random.randint(min_wait, max_wait)
    print(f"Wait: {rand_time_s}s")
    time.sleep(rand_time_s)
