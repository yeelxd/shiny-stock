# -*- coding: utf-8 -*-
# Python 3.6.3
# 程序运行中心
from util import tushare_util
# import stock_tushare
# import stock_crawler

# TuShare交易操作工具
tushare_st_instance = tushare_util.TushareUtil()
# 获取近五年的业绩报告（主表）数据
# tushare_st_instance.obtain_5y_report()
# 获取近五年的盈利能力的数据
# tushare_st_instance.obtain_5y_profit()
# 获取近五年成长能力数据
# tushare_st_instance.obtain_5y_growth()
# 获取近五年基金持股数据
# tushare_st_instance.obtain_5y_fund()
# 获取沪深300的成分股及其权重
# tushare_st_instance.obtain_hs300_weight()
# 统计近三个月的历史分笔交易的数据
stock_600118 = {'code': '600118', 'name': '中国卫星'}
stock_600651 = {'code': '600651', 'name': '飞乐音响'}
stock_603160 = {'code': '603160', 'name': '汇顶科技'}
stock_600835 = {'code': '600835', 'name': '上海机电'}
stock_601318 = {'code': '601318', 'name': '中国平安'}
hist_trade_stock_list = [stock_600835, stock_601318]
tushare_st_instance.history_trade_stat(stock_info_list=hist_trade_stock_list)
# 大单交易明细与统计 600118 600651
big_order_stock_code = ["600118", "600651"]
tushare_st_instance.big_order(big_order_stock_code)

# 优质股票过滤
# stock_ts_instance = stock_tushare.StockStat()
# stock_ts_instance.main_center()

# 网页爬虫筛选股票 too slowly
# stock_cl_instance = stock_crawler.StockStat()
# stock_cl_instance.main_center()
