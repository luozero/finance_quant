# coding: utf8
import os
import sys
from datetime import date
from stock_deeplearning.ultility.stock_codes_utility import stock_codes_utility as SCU
from stock_deeplearning.rqalpha.rqalpha.data.base_data_source import BaseDataSource
from stock_deeplearning.rqalpha.rqalpha.data.instrument_mixin import InstrumentMixin
from stock_deeplearning.rqalpha.rqalpha.core.bar_dict_price_board import BarDictPriceBoard
from stock_deeplearning.rqalpha.rqalpha.data.data_proxy import DataProxy
from stock_deeplearning.data_set.rqalpha_data.ohlcvt_data import ohlcvt_data
import numpy as np
import pandas as pd

#from rqalpha.data.instrument_store import instrument_store

class ohlcvt_factor:
  def __init__(self, path_data='~/', path_factor='../../../data/',
               date_time = date(2019, 9, 5), count=100):
    path_factor = os.path.join(path_factor, 'ohlcvt_factor')
    if not os.path.exists(path_factor):
      os.makedirs(path_factor)
    self.path_factor_ = path_factor

    self.date_ = date_time
    self.count_ = count
    self.ohlcvt_data_ = ohlcvt_data(path_data)

  def mean_factor(self, ohlcv_data, data_type = "close", windows = 5):
    price = ohlcv_data[data_type]
    data = pd.DataFrame(price)
    data = data.pct_change()
    mean = data.rolling(windows=windows, min_periods=1).mean()
    mean.column = "mean"
    return mean

  def var_factor(self, ohlcv_data, data_type = "close", windows = 5):
    price = ohlcv_data[data_type]
    data = pd.DataFrame(price)
    data = data.pct_change()
    var = data.rolling(windows=windows, min_periods=1).var()
    var.column = "var"
    return var

  def price_ratio(self, ohlcv_data, data_type = "close", freq = "5D"):
    price = ohlcv_data[data_type]
    data = pd.DataFrame(price)
    data = data.resample(freq).asfreq()
    data = data.pct_change()
    return data

  def proc_factor(self, windows = 5, inst_sym = '603032.XSHG',
                date_time = date(2019, 9, 5), bar_count=100):
    ohlcv_data = self.ohlcvt_data_.load_all_data(inst_sym, date_time, bar_count)

    factor = self.mean_factor(ohlcv_data, "close", windows)
    data = self.var_factor(ohlcv_data, "close", windows)
    factor = pd.concat([factor, data], axis=1)

if __name__ == '__main__':
  ohlcvt = ohlcvt_factor('~/', '../../../data/', date(2019, 9, 5), 100)