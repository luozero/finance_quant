# coding: utf8
import os

import pandas as pd
from datetime import datetime
from datetime import date

from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.data.instrument_mixin import InstrumentMixin

class ohlcvt_data:
  def __init__(self, path = '~/'):
    data_path = os.path.join(path, ".rqalpha")
    data_bundle_path = os.path.join(os.path.expanduser(data_path), "bundle")
    if not os.path.isdir(data_bundle_path ):
      print("not exist this file", data_bundle_path)
      exit(-1)
    data_source = BaseDataSource(data_bundle_path)
    self.data_source_ = data_source

    Instru = InstrumentMixin(data_source._instruments._instruments)
    self.sym_inst_ = Instru
    self.insts_ = data_source._instruments._instruments


  #data_type = [close     high     low     open         total_turnover     volume]
  def load_data(self, data_type = "close",
                date_time = date(2019, 9, 5), bar_count=100):
    data = self.data_source_.history_bars(instrument=self.sym_inst_.instruments(inst_sym), bar_count=100,
                                    frequency='1d', fields=data_type, dt=date_time,
                                    skip_suspended=False, adjust_orig=date_time)
    return data

  #data_type = [close     high     low     open         total_turnover     volume]
  def load_all_data(self, inst_sym = '603032.XSHG',
                date_time = date(2019, 9, 5), bar_count=100):
    data = self.data_source_.history_bars(instrument=self.sym_inst_.instruments(inst_sym), bar_count = bar_count,
                                                frequency='1d', fields=["datetime", "close", "high", "low", "open", "total_turnover", "volume"], dt=date_time,
                                                skip_suspended=False, adjust_orig=date_time)
    #data = pd.DataFrame(data)
    #data.columns = ["close", "high", "low", "open", "turnover", "volume"]
    return data