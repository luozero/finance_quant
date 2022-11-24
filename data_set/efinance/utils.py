import efinance as ef

class ef_utils:

  def get_north_stock_codes():
    datacenter = ef.stock.datacenter()
    north_stock_status = datacenter.get_north_stock_status()
    stock_codes = sorted(north_stock_status['stock_code'].apply(lambda x: x[:-3]).values)
    return stock_codes
  
  def get_block_codes(block):
    push2_98_getter = ef.stock.push2_98_getter.push2_98()
    code_names = push2_98_getter.get_block_codes(block)
    return code_names.loc[:, 'stock_code'].values

  def get_block_codes_names(block):
    push2_98_getter = ef.stock.push2_98_getter.push2_98()
    code_names = push2_98_getter.get_block_codes(block)
    return code_names

  def get_stock_codes():
    push2_98 = ef.stock.push2_98_getter.push2_98()
    all_stock_status = push2_98.get_all_stock_status()
    stock_codes = all_stock_status['stock_code']
    return sorted(stock_codes.values, reverse=False)

  def get_trading_date():
    stock_code = '1.000001'
    df = ef.stock.get_quote_history(stock_code)
    date = df['日期'].values
    return date