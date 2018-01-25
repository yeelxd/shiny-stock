# -*- coding: utf-8 -*-
# Python 3.6.3
# 程序运行中心
from test import tushare_st
import stock_filter
import stock_stat

# 大单统计
tushare_st_instance = tushare_st.TushareST()
tushare_st_instance.big_order()

# 优质股票过滤
stock_filter_instance = stock_filter.StockFilter()
stock_filter_instance.main_center()

# 网页爬虫筛选股票
stock_stat_instance = stock_stat.StockStat()
stock_stat_instance.main_center()
