import pandas as pd
import numpy as np
import os

from ultility.download_record import download_record as DR
from ultility.common_func import * 
from ultility.common_def import * 
from data_set.finance_data.finance_load_store import finance_load_store as FLD
from datetime import datetime

class process_detailed_trade(object):

  def __init__(self, path = "path", path_in = 'path_in', path_out = 'path_out'):

    self.path = path
    if not os.path.exists(path_in):
      print("pls download finance data")
    self.path_in = path_in

    # path_out = os.path.join(path_out, get_today_date())
    if not os.path.exists(path_out):
      os.makedirs(path_out)
    self.path_out = path_out

  def statistic_detailed_bills(self, dates):
    
