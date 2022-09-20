# coding: utf8
LINK_MAIN_FINANCE = 'http://quotes.money.163.com/service/zycwzb_{}.html?type=report'
LINK_ADBSTRACT_FINANCE = 'http://quotes.money.163.com/service/cwbbzy_{}.html'
LINK_PROFIT_FINANCE = 'http://quotes.money.163.com/service/lrb_{}.html'
LINK_CASH_FINANCE = 'http://quotes.money.163.com/service/xjllb_{}.html'
LINK_LOANS_FINANCE = 'http://quotes.money.163.com/service/zcfzb_{}.html'
LINK_STOCK_DAILY_TRADE_SH = 'https://quotes.money.163.com/service/chddata.html?code=0{}&start=19960827&end=20220913&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
LINK_STOCK_DAILY_TRADE_SZ = 'http://quotes.money.163.com/service/chddata.html?code=1{}&start=19910102&end=20220914&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'

# download file name
FILE_MAIN = '{}_main.csv'
FILE_ABSTRACT = '{}_abstract.csv'
FILE_PROFIT = '{}_profit.csv'
FILE_CASH = '{}_cash.csv'
FILE_LOANS = '{}_loans.csv'
FILE_DAILY_TRADE = '{}_daily_trade.csv'

# download finance folder
FOLDER_DATA_DOWNLOAD = 'finance'

# factor folder
FOLDER_FACTOR = 'finance_processed'

# process trade data folder from daily trade data
FOLDER_DAILY_TRADE_PROCESSED = "daily_trade_processed"
FILE_DAILY_TRADE_QUARTER = "{}_daily_trade_quarter.csv"

# json process config
FILE_JSON_PROCESS_RECORD = "process_record.json"

KEY_DOWNLOAD = 'download'
KEY_DOWNLOAD_DAILY_TRADE_DATA_INDEX = 'download_daily_trade_data_index'
KEY_DOWNLOAD_FINANCE_DATA_INDEX = 'download_finance_data_index'
KEY_PROCESS = 'process'
KEY_PROCESS_DAILY_TRADE_QUARTER_INDEX = "daily_trade_quarter_index"
KEY_PROCESS_FINANCE_FACTOR_INDEX = "stock_factor_calc_index"

process_record_dict = {KEY_DOWNLOAD: {}, KEY_PROCESS: {}}

# csv file
CSV_PROCESS_DAILY_TRADE_SKIP_STOCK = "skip_stocks.csv"