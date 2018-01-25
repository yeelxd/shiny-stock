# -*- coding: utf-8 -*-
# Python 3.6.3
# 使用tushare分析工具
# 保存在MongoDB中
import tushare as ts
from util import mongo_util
import time
import re
import json

'''
code,代码     name,名称     industry,所属行业       area,地区     pe,市盈率
outstanding,流通股本(亿)     totals,总股本(亿)       totalAssets,总资产(万)
liquidAssets,流动资产       fixedAssets,固定资产        reserved,公积金
reservedPerShare,每股公积金      esp,每股收益        bvps,每股净资
pb,市净率      timeToMarket,上市日期       undp,未分利润       perundp, 每股未分配
rev,收入同比(%)     profit,利润同比(%)      gpr,毛利率(%)      npr,净利润率(%)
holders,股东人数
'''


# 获取默认前一天的沪深股票列表
def get_stock_data_list():
    try:
        df = ts.get_stock_basics()
        if df is not None:
            # orient:json格式顺序，包括columns，records，index，split，values，默认为columns
            # index : dict like {index -> {column -> value}}
            return json.loads(df.to_json(orient='index'))
    except Exception as e:
        print(e)
        return None


# 根据市盈率等筛选过滤掉高估的股票
def filter_stock_list(stock_data_list, today):
    new_stock_data_list = []
    for stock_code in stock_data_list.keys():
        try:
            # 过滤只取主板的股票
            match_result = re.match(r"[60][0][0123]\d{3}", stock_code)
            if match_result is None:
                continue
            stock_info = stock_data_list.get(stock_code)
            # 刨除N/ST股
            stock_name = stock_info['name']
            if stock_name[0:1] == "N" or stock_name.count("ST") > 0:
                continue
            # 一般市盈率{pe=股价/每股收益}合理区间[10-20]
            # 一般市净率{pb=股价/每股净资产}合理区间[3-10]
            # 一般每股收益{esp=税后利润与股本总数的比率}合理区间[>0.3]
            pe = stock_info['pe']
            pb = stock_info['pb']
            esp = stock_info['esp']
            if pe > 20 or pb > 10 or esp < 0.3:
                continue
            # 每股净资产{bps=股东权益 / 总股数}
            bvps = stock_info['bvps']
            if bvps == 0:
                continue
            # 一般净资产收益率{roe=每股收益esp/每股净资产bps}合理区间[>15%]
            roe = esp * 100 / bvps
            if roe < 15:
                continue
            # 更新ROE数据
            stock_data = {}
            stock_data.update({'code': stock_code})
            stock_data.update(stock_info)
            stock_data.update({'roe': str(round(roe, 2))+"%"})
            stock_data.update({'createDate': today})
            new_stock_data_list.append(stock_data)
        except Exception as e:
            print("股票{%s}筛选出错" % stock_code, e)
            continue
    return new_stock_data_list


# 处理中心
def main_center():
    init_stock_data_list = get_stock_data_list()
    print("待筛选的股票数量={}".format(len(init_stock_data_list)))
    # 记录开始时间
    start_time = time.time()
    # 当前日期
    today = time.strftime("%Y-%m-%d", time.localtime())
    stock_data_list = filter_stock_list(init_stock_data_list, today)
    # 对筛选结果根据PE排序--升序
    stock_data_list.sort(key=lambda obj: obj.get('pe'), reverse=False)
    # MongoDB
    mongo_util_instance = mongo_util.MongoUtil()
    # 首先删除MongoDB中已存在的当天数据
    filter_param = {"createDate": today}
    mongo_util_instance.del_many(collection='stock_stat', filter_param=filter_param)
    # 保存到MongoDB
    mongo_util_instance.add_many(collection='stock_stat', data_json_list=stock_data_list)
    # 关闭Mongo连接
    mongo_util_instance.close()
    end_time = time.time()
    # 计算程序执行耗时
    total_time = end_time - start_time
    print("筛选股票信息完毕，共获取[{0}]只，耗时：{1:.2f}秒".format(len(stock_data_list), total_time))


# Call Running Center
main_center()
