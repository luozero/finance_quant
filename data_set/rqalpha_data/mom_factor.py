import os
import sys
import talib
from datetime import date
import pandas as pd
import numpy as np
sys.path.append(r'../../../')
sys.path.append(r'../../rqalpha')
from stock_deeplearning.data_set.rqalpha_data.ohlcvt_data import ohlcvt_data
from stock_deeplearning.ultility.stock_codes_utility import stock_codes_utility as SCU



class talib_factor:
  def __init__(self, path_data='~/', path_factor='../../../data/',
               date_time = date(2019, 9, 5), count=100):
    path_factor = os.path.join(path_factor, 'talib_factor')
    if not os.path.exists(path_factor):
      os.makedirs(path_factor)
    self.path_factor_ = path_factor

    self.date_ = date_time
    self.count_ = count
    self.ohlcvt_data_ = ohlcvt_data(path_data)

  def factor_calc(self, inst_sym = '603032.XSHG',
                date_time = date(2019, 9, 5), timeperiod=14,
                  fastperiod=12, slowperiod=26, signalperiod=9):
    factor_csv = os.path.join(self.path_factor_, inst_sym + ".csv")

    ohlcvt = self.ohlcvt_data_.load_all_data(inst_sym, date_time, self.count_)
    try:
        data_len = len(ohlcvt)
    except TypeError:
        return

    if data_len < slowperiod :
      return
    datetime = ohlcvt["datetime"]
    high = ohlcvt["high"]
    close = ohlcvt["close"]
    low = ohlcvt["low"]
    open = ohlcvt["open"]
    volumn = ohlcvt["volume"]

    factor = talib.ADX(high, low, close, timeperiod)
    factor[np.isnan(factor)] = 0
    data =  pd.DataFrame({"ADX": factor})
    #data = pd.concat([data, pd.DataFrame({"ADX": factor})], axis=1)

    factor = talib.ADXR(high, low, close, timeperiod)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"ADXR": factor})], axis=1)

    factor = talib.APO(close, fastperiod, slowperiod, matype=0)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"APO": factor})], axis=1)

    aroondown, aroonup = talib.AROON(high, low, timeperiod)
    aroondown[np.isnan(aroondown)] = 0
    aroonup[np.isnan(aroonup)] = 0
    data = pd.concat([data, pd.DataFrame({"aroondown": aroondown})], axis=1)
    data = pd.concat([data, pd.DataFrame({"aroonup": aroonup})], axis=1)

    factor = talib.AROONOSC(high, low, timeperiod)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"AROONOSC": factor})], axis=1)

    factor = talib.BOP(open, high, low, close)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"BOP": factor})], axis=1)

    factor = talib.CCI(high, low, close, timeperiod)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"CCI": factor})], axis=1)

    factor = talib.CMO (close, timeperiod)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"CMO": factor})], axis=1)

    factor = talib.DX(high, low, close, timeperiod)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"DX": factor})], axis=1)

    [macd, macdsignal, macdhist] = talib.MACD(close, fastperiod, slowperiod, signalperiod)
    macdsignal[np.isnan(macdsignal)] = 0
    data = pd.concat([data, pd.DataFrame({"MACD": macdsignal})], axis=1)

    factor = talib.MFI(high, low, close, volumn, timeperiod)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"MFI": factor})], axis=1)

    factor = talib.PPO(close, fastperiod, slowperiod, matype=0)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"PPO": factor})], axis=1)

    factor = talib.ROCP(close, timeperiod)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"ROCP": factor})], axis=1)

    factor = talib.RSI(close, timeperiod)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"RSI": factor})], axis=1)

    slowk, slowd = talib.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3,
                         slowd_matype=0)
    slowk[np.isnan(slowk)] = 0
    slowd[np.isnan(slowd)] = 0
    data = pd.concat([data, pd.DataFrame({"STOCHslowk": slowk})], axis=1)
    data = pd.concat([data, pd.DataFrame({"STOCHslowd": slowd})], axis=1)

    fastk, fastd = talib.STOCHRSI(close, timeperiod, fastk_period=5, fastd_period=3, fastd_matype=0)
    fastk[np.isnan(fastk)] = 0
    fastd[np.isnan(fastd)] = 0
    data = pd.concat([data, pd.DataFrame({"STOCHRSIfastk": fastk})], axis=1)
    data = pd.concat([data, pd.DataFrame({"STOCHRSIfastd": fastd})], axis=1)

    factor = talib.TRIX(close, timeperiod)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"TRIX": factor})], axis=1)

    factor = talib.ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
    factor[np.isnan(factor)] = 0
    data = pd.concat([data, pd.DataFrame({"TRIX": factor})], axis=1)

    price = pd.DataFrame(close)
    day1 = price.pct_change(periods=1)
    data1 = day1.shift(-1, axis=0)
    day2 = price.pct_change(periods=2)
    day2 = day2.shift(-2, axis=0)
    data1 = pd.concat([data1, day2], axis=1)
    day3 = price.pct_change(periods=3)
    day3 = day3.shift(-3, axis=0)
    data1 = pd.concat([data1, day3], axis=1)
    day4 = price.pct_change(periods=4)
    day4 = day4.shift(-4, axis=0)
    data1 = pd.concat([data1, day4], axis=1)
    day5 = price.pct_change(periods=5)
    day5 = day5.shift(-5, axis=0)
    data1 = pd.concat([data1, day5], axis=1)

    data1.columns = ["1day", "2day", "3day", "4day", "5day"]
    data = pd.concat([data, data1], axis=1)
    data[np.isnan(data)] = 0

    date_index = pd.DataFrame(datetime).applymap(lambda x: pd.to_datetime(str(x), format = "%Y%m%d%H%M%S"))
    date_index.columns = ["datetime"]
    data = pd.concat([date_index, data], axis=1)

    data.to_csv(factor_csv, index = False)

  def is_number(self, s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

if __name__ == '__main__':
  scu = SCU('../../../data/');
  talib_f = talib_factor('~/', '../../../data/', date(2019, 9, 5), 1000)
  stock_codes = scu.stock_codes()
  stock_codes = scu.add_allstock_xshg_xshe(stock_codes)

  # stock_codes= ['002975.XSHE', '000002.XSHE']
  for stock_code in stock_codes:
    print("calculated stock:", stock_code);
    talib_f.factor_calc(stock_code);

