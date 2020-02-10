# stock_deeplearning

this project is developing to used deep-learning to train stock base on tensorflow and pytorch
good material for quant stock study.

env requirements,
1, tushare
2, tensorflow
3, ricequant
4, talib

##################################################

# volme and price trade rule(for learning)
run step,
1) cd stock_process_day_data
2) python getdata.py (get all the A stock day trade data)
3) cd easyvolumeprice
4) python easyvolumeprice (run volum and price trade strategy)

# technical analysis back test

1) cd stock_process_day_data
2) python getdata.py (get all the A stock day trade data)
3) cd easyvolumeprice
4) python trade_ta_back_test (run macd buy and kdj sell strategy)

# deep learning price predict

simple user guide, without any modification, you can training 000001 stock price rate with stock('000001','000002','000018', '600000','600005','600007')
close, open, high, low, volum data.

1) cd stock_process_day_data
2) python getdata.py (get all the A stock day trade data)
3). cd /stock_deeplearning
4). python train.py

##################################################

for momentum investment
# dataset(folder)
used to get finance data and trading data, processing them into different factor

# training
1) use mom_factor.py(data_set/mom_factor) to generate momentum factor
2) use mom_training.py(training) to training and inference stock, you can only modify run folder to test 000002.XSHE.csv


##################################################

financial_stock_basic_proc.py
run this python to generate company finance rank to get the better foundmental company.

