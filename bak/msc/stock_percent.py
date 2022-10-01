import os
import sys
import getopt
sys.path.append(r'../')
sys.path.append(r'../rqalpha')
from datetime import date
from datetime import datetime
import pandas as pd
from data_set.rqalpha_data.ohlcvt_data import ohlcvt_data
from ultility.download_record import download_record as DR
import rqalpha as rqa


class percent_factor:
  def __init__(self, path_data='~/',
               date_time = date(2019, 9, 5), count=30):

    self.date_ = date_time
    self.count_ = count
    self.ohlcvt_data_ = ohlcvt_data(path_data)
    self.insts_ = self.ohlcvt_data_.insts_

  def factor_calc(self, inst_sym = '603032.XSHG', date_time = date(2019, 12, 6),
                day = 5):
    ohlcvt = self.ohlcvt_data_.load_all_data(inst_sym, date_time, self.count_)
    if ohlcvt == None or ohlcvt.size == 0:
      return pd.DataFrame()
    # if inst_sym == '002962.XSHE':
    #   print(inst_sym)
    datetime = ohlcvt["datetime"]
    high = ohlcvt["high"]
    close = ohlcvt["close"]
    low = ohlcvt["low"]
    open = ohlcvt["open"]
    volumn = ohlcvt["volume"]

    price = pd.DataFrame(close)
    day1 = price.pct_change(periods=1)
    day2 = price.pct_change(periods=2)
    day3 = price.pct_change(periods=3)
    day4 = price.pct_change(periods=4)
    day5 = price.pct_change(periods=5)

    data = pd.DataFrame([[inst_sym, day1.iloc[-1,0], day2.iloc[-1,0], day3.iloc[-1,0], day4.iloc[-1,0], day5.iloc[-1,0]]],
                        columns = ["inst", "1day", "2day", "3day", "4day", "5day"])

    date_index = pd.DataFrame([pd.to_datetime(str(datetime[-1]), format = "%Y%m%d%H%M%S")])
    date_index.columns = ["datetime"]
    data = pd.concat([date_index, data], axis=1)

    return data

    # data.to_csv(factor_csv, index = False)

#python stock_percent.py -d 2019-12-4 -p D:\stock\python\quant_stock\data_20191110
if __name__ == '__main__':

  path = 'D:\stock\python\quant_stock\data_20191110'
  date_time_str = '2019-12-6'
  count = 30
  try:
    opts, args = getopt.getopt(sys.argv[1:], "p:d:c:", ["path=", "date=", "count="])
  except getopt.GetoptError:
    print('test.py -o <outputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('test.py -o <outputfile>')
    elif opt in ("-d", "--date"):
      date_time_str = arg
    elif opt in ("-c", "--count"):
      filename = arg
    elif opt in ("-p", "--path"):
      path = arg

  date_time = datetime.strptime(date_time_str, "%Y-%m-%d")
  print("path is:", path)

  dr = DR(path, 'stock_percent_date.json')
  if date_time_str != dr.read_date():
    rqa.update_bundle()
    dr.write_date(date_time_str)

  percent = percent_factor('~/', date_time, count)

  dataRepo = pd.DataFrame()
  for stock in percent.insts_:
    if stock.type == 'CS':
      print("inst:",stock.order_book_id)
      data = percent.factor_calc(inst_sym = stock.order_book_id, date_time = date_time,
                  day = 5);
      if data.empty == False:
        dataRepo = dataRepo.append(data)

  dataRepo.sort_values(by=['5day'], ascending=False)
  path_store = os.path.join(path, "percent_factor.csv")
  dataRepo.to_csv(path_store)
