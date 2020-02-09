import pandas as pd
import os

proc_days = 5

class stock_loader:
  def _init_(self, stock_code = "000001.XSHE", path="../../../data", t_vs_t = 0.1, train_day = "5day"):
    factor_csv = os.path.join(path, stock_code + ".csv")
    self.data = pd.read_csv(factor_csv)
    self.train_day = train_day
    row, col = self.data.shape
    self.train_num = int(row * t_vs_t)
    self.test_num = row - self.train_num - proc_days
    self.train_index = 1
    self.test_index = self.train_num + 1
    self.proc_num = row

  def train_loader(self):
    if self.train_index > self.train_num:
      return
    train_output = self.data.ix[self.train_index:self.train_num, self.train_day]
    train_input = self.data.ix[self.train_index:self.train_num, 1:-proc_days]
    self.train_index += 1
    return train_input, train_output

  def test_loader(self):
    if self.test_index > self.test_num:
      return
    test_output = self.data.ix[self.test_index:self.test_num , self.train_day]
    test_input = self.data.ix[self.test_index:self.test_num , 1:-proc_days]
    self.test_index +=1
    return test_input, test_output

