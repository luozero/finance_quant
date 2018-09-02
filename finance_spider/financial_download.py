#-*- coding:UTF-8 -*-
from urllib import request
import os
import tushare as ts

MAIN_FINANCE = 'http://quotes.money.163.com/service/zycwzb_{}.html?type=report'
ADBSTRACT_FINANCE = 'http://quotes.money.163.com/service/cwbbzy_{}.html'
PROFIT_FINANCE = 'http://quotes.money.163.com/service/lrb_{}.html'
CASH_FINANCE = 'http://quotes.money.163.com/service/xjllb_{}.html'
LOANS_FINANCE = 'http://quotes.money.163.com/service/zcfzb_{}.html'

def Schedule(a,b,c):
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' % per)

def fetch_stock_finance_data(path,stock):
  #main finance
  url = MAIN_FINANCE.format(stock)
  local = os.path.join(path,'{}_main.csv'.format(stock))
  request.urlretrieve(url,local,Schedule)
  #abstract
  url = ADBSTRACT_FINANCE.format(stock)
  local = os.path.join(path,'{}_abstract.csv'.format(stock))
  request.urlretrieve(url,local,Schedule)
  #profit
  url = PROFIT_FINANCE.format(stock)
  local = os.path.join(path,'{}_profit.csv'.format(stock))
  request.urlretrieve(url,local,Schedule)
  #cash
  url = CASH_FINANCE.format(stock)
  local = os.path.join(path,'{}_cash.csv'.format(stock))
  request.urlretrieve(url,local,Schedule)
  #loans
  url = LOANS_FINANCE.format(stock)
  local = os.path.join(path,'{}_loans.csv'.format(stock))
  request.urlretrieve(url,local,Schedule)

def ts_stock_codes():
  basic_data = ts.get_stock_basics()
  stockcode = list(basic_data.index)
  stockcode.remove('603657')
  stockcode.remove('300724')
  stockcode.remove('603192')
  stockcode.remove('601068')
  stockcode.remove('601069')
  stockcode.remove('601606')
  stockcode.sort()
  return stockcode

if __name__ == '__main__':
  stock_codes=ts_stock_codes()
  
  path = '../../data/finance'
  if not os.path.exists(path):
            os.makedirs(path)
  
  for stock in (stock_codes):
    print("fetching stock",stock)
    fetch_stock_finance_data(path,stock)
    print("fetched stock",stock)
  


