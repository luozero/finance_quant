# stock_deeplearning

this project is developing to used deep-learning to train stock base on tensorflow

env requirements,
1, tushare
2, tensorflow

# volme and price trade rule
run step,
1) cd stock_process_day_data
2) python getdata.py (get all the A stock day trade data)
3) cd easyvolumeprice
4) python easyvolumeprice (run volum and price trade strategy)

# deep learning price predict

simple user guide, without any modification, you can training 000001 stock price rate with stock('000001','000002','000018', '600000','600005','600007')
close, open, high, low, volum data.

1) cd stock_process_day_data
2) python getdata.py (get all the A stock day trade data)
3). cd /stock_deeplearning
4). python train.py
