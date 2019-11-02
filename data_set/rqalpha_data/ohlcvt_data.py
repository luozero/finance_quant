# coding: utf8
import os
import sys
import pandas as pd
from datetime import datetime
from datetime import date

from stock_deeplearning.rqalpha.rqalpha.data.base_data_source import BaseDataSource
from stock_deeplearning.rqalpha.rqalpha.data.instrument_mixin import InstrumentMixin

class ohlcvt_data:
  def __init__(self, path = '~/'):
    data_path = os.path.join(path, ".rqalpha")
    data_bundle_path = os.path.join(os.path.expanduser(data_path), "bundle")
    if not exit(os.path.expanduser(data_bundle_path )):
      print("not exist this file", data_bundle_path)
      exit(-1)
    data_source = BaseDataSource(data_bundle_path)
    self.data_source_ = data_source

    Instru = InstrumentMixin(data_source._instruments._instruments)
    self.instruments_ = Instru

  #data_type = [close     high     low     open         total_turnover     volume]
  def load_data(self, data_type = "close",
                date_time = date(2019, 9, 5), bar_count=100):
    data = self.data_source_.history_bars(instrument=self.instruments_.instruments(inst_sym), bar_count=100,
                                    frequency='1d', fields=data_type, dt=date_time,
                                    skip_suspended=False, adjust_orig=date_time)
    return data

  #data_type = [close     high     low     open         total_turnover     volume]
  def load_all_data(self, inst_sym = '603032.XSHG',
                date_time = date(2019, 9, 5), bar_count=100):
    close = self.data_source_.history_bars(instrument=self.instruments_.instruments(inst_sym), bar_count=100,
                                                frequency='1d', fields="close", dt=date_time,
                                                skip_suspended=False, adjust_orig=date_time)
    data = close
    high = self.data_source_.history_bars(instrument=self.instruments_.instruments(inst_sym), bar_count=100,
                                                frequency='1d', fields="high", dt=date_time,
                                                skip_suspended=False, adjust_orig=date_time)
    data = pd.concat([data, high], axis=1)
    low = self.data_source_.history_bars(instrument=self.instruments_.instruments(inst_sym), bar_count=100,
                                                frequency='1d', fields="low", dt=date_time,
                                                skip_suspended=False, adjust_orig=date_time)
    data = pd.concat([data, low], axis=1)
    open = self.data_source_.history_bars(instrument=self.instruments_.instruments(inst_sym), bar_count=100,
                                                frequency='1d', fields="open", dt=date_time,
                                                skip_suspended=False, adjust_orig=date_time)
    data = pd.concat([data, open], axis=1)
    total_turnover = self.data_source_.history_bars(instrument=self.instruments_.instruments(inst_sym), bar_count=100,
                                                          frequency='1d', fields="total_turnover", dt=date_time,
                                                          skip_suspended=False, adjust_orig=date_time)
    data = pd.concat([data, total_turnover], axis=1)
    volume = self.data_source_.history_bars(instrument=self.instruments_.instruments(inst_sym), bar_count=100,
                                                  frequency='1d', fields="volume", dt=date_time,
                                                  skip_suspended=False, adjust_orig=date_time)
    data = pd.concat([data, volume], axis=1)
    data.column = ["close", "high", "low", "open", "turnover", "volume"]
    return data