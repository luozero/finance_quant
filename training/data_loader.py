import pandas as pd
import os
import torch

proc_days = 5

class StockLoader:
  def __init__(self, stock_code = "000001.XSHE", path="../../../data", t_vs_t = 0.1, train_day = "5day", train_opt = ["ADX", "ADXR"]):
    factor_csv = os.path.join(path, stock_code + ".csv")
    self.data = pd.read_csv(factor_csv, index_col=0)
    self.train_day = train_day
    self.train_opt = train_opt
    row, col = self.data.shape
    self.train_num = int(row * t_vs_t)
    self.test_num = row
    self.train_index = 1
    self.test_index = self.train_num + 1
    self.proc_num = row

  def train_loader(self):
    if self.train_index > self.train_num:
      return
    train_output = self.data.loc[:, self.train_day]
    train_output =  train_output.iloc[self.train_index: self.train_num]
    train_input = self.data.loc[:, self.train_opt]
    train_input = train_input.iloc[self.train_index: self.train_num, :]
    train_data = [];
    index = 0
    for label, output in train_output.iterrows():
      input = train_input.iloc[index, :]
      train_data.append(tuple([torch.Tensor(input.values), torch.Tensor(output)]))
      index +=1
    return train_data

  def test_loader(self):
    if self.test_index > self.test_num:
      return
    test_output = self.data.loc[:, self.train_day]
    test_output =  test_output.iloc[self.test_index: self.test_num]
    test_input = self.data.loc[:, self.train_opt]
    test_input = test_input.iloc[self.test_index: self.test_num, :]
    test_data = [];
    index = 0
    for label, output in test_output.iterrows():
      input = test_input.iloc[index, :]
      test_data.append(tuple([torch.Tensor(input.values), torch.Tensor(output)]))
      index +=1
    return test_data

