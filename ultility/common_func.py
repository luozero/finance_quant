# coding: utf8
import pandas as pd

def nearest_date(items, pivot):
  return min(items, key=lambda x: abs(pd.Timestamp(x) - pd.Timestamp(pivot)))