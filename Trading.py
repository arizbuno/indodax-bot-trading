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


class Utilities:
  def analyze(symbol, screener, exchange, interval):
    coin = TA_Handler(
      symbol=symbol,
      screener=screener,
      exchange=exchange,
      interval=interval
    )
    coin_summary = coin.get_analysis().summary

    recommendation = f"{symbol} {coin_summary['RECOMMENDATION']}"
    coin_buy = str(coin_summary['BUY'])
    coin_sell = str(coin_summary['SELL'])
    coin_neutral = str(coin_summary['NEUTRAL'])

    recommendation_with_color = Utilities.dye_str(recommendation, 'YELLOW')
    if recommendation[-3:len(recommendation)] == 'BUY':
      recommendation_with_color = Utilities.dye_str(recommendation, 'GREEN')
    elif recommendation[-4:len(recommendation)] == 'SELL':
      recommendation_with_color = Utilities.dye_str(recommendation, 'RED')
    
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
