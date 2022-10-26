# coding: utf8
LINK_MAIN_FINANCE            = 'http://quotes.money.163.com/service/zycwzb_{}.html?type=report'
LINK_EARNING_CAPACITY        = 'http://quotes.money.163.com/service/zycwzb_{}.html?type=report&part=ylnl'
LINK_RETURN_DEBIT_CAPACITY   = 'http://quotes.money.163.com/service/zycwzb_{}.html?type=report&part=chnl'
LINK_GROWTH_CAPACITY         = 'http://quotes.money.163.com/service/zycwzb_{}.html?type=report&part=cznl'
LINK_OPERATION_CAPACITY      = 'http://quotes.money.163.com/service/zycwzb_{}.html?type=report&part=yynl'
LINK_ADBSTRACT_FINANCE       = 'http://quotes.money.163.com/service/cwbbzy_{}.html'
LINK_PROFIT_FINANCE          = 'http://quotes.money.163.com/service/lrb_{}.html'
LINK_CASH_FINANCE            = 'http://quotes.money.163.com/service/xjllb_{}.html'
LINK_LOANS_FINANCE           = 'http://quotes.money.163.com/service/zcfzb_{}.html'
LINK_STOCK_DAILY_TRADE       = 'https://quotes.money.163.com/service/chddata.html?code={}&start=19960827&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
LINK_INDEX_DAILY_TRADE 			 = 'http://quotes.money.163.com/service/chddata.html?code={}&start=19910102&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'

# download file name
FILE_MAIN 						 = 'main.csv'
FILE_EARNING 					 = 'earning.csv'
FILE_RETURN_DEBIT 	   = 'return_debit.csv'
FILE_GROWTH 					 = 'growth.csv'
FILE_OPERATION 				 = 'operation.csv'
FILE_ABSTRACT 				 = 'abstract.csv'
FILE_PROFIT 					 = 'profit.csv'
FILE_CASH 						 = 'cash.csv'
FILE_LOANS 						 = 'loans.csv'
FILE_STOCK_DAILY_TRADE = 'stock_daily_trade.csv'
FILE_INDEX_DAILY_TRADE = 'index_daily_trade.csv'
FILE_INDEX_NORTH_DAILY_TRADE = 'index_north_daily_trade.csv'
FILE_FINANCE_FACTOR     = 'finance_factors.csv'
FILE_STOCK_BILL         = 'trade_bill.csv'
FILE_STOCK_BIG_DEAL         = 'trade_big_deal.csv'
FILE_TRADE_NORTH       = 'trade_north.csv'
FILE_TRADE_NORTH_NEW       = 'trade_north_new.csv'
FILE_TRADE_MAEGIN_SHORT = 'trade_margin_short.csv'

# download data fyle
TYPE_FINANCE_STOCK = 'finance_stock_data'
TYPE_STOCK 				 = 'stock_data'
TYPE_INDEX 				 = 'index_data'

# download finance folder
FOLDER_163_INDEX = '163'

# factor folder
FOLDER_FACTOR                = 'finance_processed'
FOLDER_RANK                  = 'rank'
FOLDER_DAILY_TRADE_PROCESSED = "daily_trade_processed"
FOLDER_NORTH_INDEX_TEMP      = 'north_index_temp'
FOLDER_NORTH_INDEX_CONCEPT_TEMP      = 'north_index_concept_temp'
FOLDER_NORTH_STOCK_TEMP      = 'north_stock_temp'

# process trade data folder from daily trade data
FILE_DAILY_TRADE_QUARTER = "daily_trade_quarter.csv"

# json process config
JSON_FILE_PROCESS_RECORD              = "process_record.json"

KEY_DOWNLOAD                          = 'download'
KEY_DOWNLOAD_DAILY_TRADE_DATA_INDEX   = 'download_daily_trade_data_index'
KEY_DOWNLOAD_FINANCE_DATA_INDEX       = 'download_finance_data_index'
KEY_PROCESS                           = 'process'
KEY_PROCESS_DAILY_TRADE_QUARTER_INDEX = "daily_trade_quarter_index"
KEY_PROCESS_FINANCE_FACTOR_INDEX      = "stock_factor_calc_index"

process_record_dict                   = {KEY_DOWNLOAD: {}, KEY_PROCESS: {}}

# csv file
CSV_SKIP_STOCK                  = "skip_stocks.csv"
CSV_PROCESS_FINANCE_SKIP_STOCK  = "finance_skip_stocks.csv"