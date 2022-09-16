# coding: utf8
LINK_MAIN_FINANCE = 'http://quotes.money.163.com/service/zycwzb_{}.html?type=report'
LINK_ADBSTRACT_FINANCE = 'http://quotes.money.163.com/service/cwbbzy_{}.html'
LINK_PROFIT_FINANCE = 'http://quotes.money.163.com/service/lrb_{}.html'
LINK_CASH_FINANCE = 'http://quotes.money.163.com/service/xjllb_{}.html'
LINK_LOANS_FINANCE = 'http://quotes.money.163.com/service/zcfzb_{}.html'
LINK_STOCK_DAILY_TRADE_SH = 'https://quotes.money.163.com/service/chddata.html?code=0{}&start=19960827&end=20220913&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
LINK_STOCK_DAILY_TRADE_SZ = 'http://quotes.money.163.com/service/chddata.html?code=1{}&start=19910102&end=20220914&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'

FILE_MAIN = '{}_main.csv'
FILE_ABSTRACT = '{}_abstract.csv'
FILE_PROFIT = '{}_profit.csv'
FILE_CASH = '{}_cash.csv'
FILE_LOANS = '{}_loans.csv'
FILE_DAILY_TRADE = '{}_daily_trade.csv'


DATA_DOWNLOAD_FOLDER = 'finance'
FACTOR_FOLDER = 'finance_processed'