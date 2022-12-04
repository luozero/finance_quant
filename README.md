# change this repo from stock_deeplearning to finance_quant.

the aim is to quantative all kinds of finance data, including stock, future, bond, marco, etc.

now it's only can download china A stock finance data and daily trade data, and also calculate some factors.


# how to use this repo.

## git submodule
git submodule init update

## configure
configure your data store folder
 open ./conf/con_release.json
  "path": "../finance_data", 

## run
download all the A stock's finance data and trade data. and generate some factors.
sh run.sh

## result folder
stock:
finance_data/data/stock/000001
abstract.csv
cash.csv
daily_trade.csv
daily_trade_quarter.csv
earning.csv
finance_factors.csv
growth.csv
loans.csv
main.csv
operation.csv
profit.csv
return_debit.csv
trade_big_deal.csv
trade_bill.csv
trade_bill_calc.csv
trade_margin_short.csv
trade_north.csv
trade_north_new.csv
index:
finance_data/data/index/000001
daily_trade.csv
trade_bill.csv
