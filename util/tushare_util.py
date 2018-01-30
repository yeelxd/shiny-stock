# Crawler Test For tushare API util
# Dependency tushare Modules
# Python 3.6.3

import tushare as ts
import json
from util import mongo_util


class TushareUtil(object):

    # 根据20MA平均线，评估买卖
    # 即设定一个策略：以20日线为标准，当前股价低于20日线的时候就卖出，高于20日线的时候就买入。
    @staticmethod
    def buy_sell(stock_code, is_print):
        is_buy = 0
        buy_val = []
        buy_date = []
        sell_val = []
        sell_date = []
        df = ts.get_hist_data(stock_code)
        # 20日平均价
        ma20 = df[u'ma20']
        # 当日的收盘价
        close = df[u'close']
        rate = 1.0
        # 数据量Index
        idx = len(ma20)

        while idx > 0:
            idx -= 1
            close_val = close[idx]
            ma20_val = ma20[idx]
            if close_val > ma20_val:
                if is_buy == 0:
                    is_buy = 1
                    buy_val.append(close_val)
                    buy_date.append(close.keys()[idx])
            elif close_val < ma20_val:
                if is_buy == 1:
                    is_buy = 0
                    sell_val.append(close_val)
                    sell_date.append(close.keys()[idx])
        if is_print:
            print("stock number : %s" % stock_code)
            print("buy count    : %d" % len(buy_val))
            print("sell count   : %d" % len(sell_val))

        for i in range(len(sell_val)):
            rate = rate * (sell_val[i] * (1 - 0.002) / buy_val[i])
            if is_print:
                print("buy date : %s, buy price : %.2f" % (buy_date[i], buy_val[i]))
                print("sell date: %s, sell price: %.2f" % (sell_date[i], sell_val[i]))
        rate = round(rate, 2) * 100
        print("The [%s] final rate of return: %d%%" % (stock_code, rate))
        return rate

    # 获取近五年股票的业绩报告（主表）情况
    # 保存到MongolianDB中
    """
    code,代码
    name,名称
    esp,每股收益
    eps_yoy,每股收益同比(%)
    bvps,每股净资产
    roe,净资产收益率(%)
    epcf,每股现金流量(元)
    net_profits,净利润(万元)
    profits_yoy,净利润同比(%)
    distrib,分配方案
    report_date,发布日期
    """
    @staticmethod
    def obtain_5y_report():
        judge_repeat = []
        stat_years = [2012, 2013, 2014, 2015, 2016, 2017]
        report_data = []
        for stat_year in stat_years:
            for q in range(1, 5):
                df = ts.get_report_data(stat_year, q)
                if df is not None:
                    json_dfs = json.loads(df.to_json(orient='records'))
                    for json_df in json_dfs:
                        period = str(stat_year) + "Q" + str(q)
                        code = str(json_df['code'])
                        # 判重
                        if judge_repeat.count(period+code) > 0:
                            continue
                        new_data = {"period": period}
                        new_data.update(json_df)
                        report_data.append(new_data)
                        # 添加到重复判断的列表
                        judge_repeat.append(period+code)
        # MongoDB
        mongo_util_instance = mongo_util.MongoUtil()
        mongo_util_instance.add_many(collection='stock_report', data_json_list=report_data)
        mongo_util_instance.close()
        print("获取近五年业绩报告（主表）数据成功. count=[{}]".format(len(report_data)))

    # 获取近五年股票的盈利能力情况
    # 保存到MongolianDB中
    """
    code,代码
    name,名称
    roe,净资产收益率(%)
    net_profit_ratio,净利率(%)
    gross_profit_rate,毛利率(%)
    net_profits,净利润(万元)
    esp,每股收益
    business_income,营业收入(百万元)
    bips,每股主营业务收入(元)
    """
    @staticmethod
    def obtain_5y_profit():
        judge_repeat = []
        stat_years = [2012, 2013, 2014, 2015, 2016, 2017]
        profit_data = []
        for stat_year in stat_years:
            for q in range(1, 5):
                df = ts.get_profit_data(stat_year, q)
                if df is not None:
                    json_dfs = json.loads(df.to_json(orient='records'))
                    for json_df in json_dfs:
                        period = str(stat_year) + "Q" + str(q)
                        code = str(json_df['code'])
                        # 判重
                        if judge_repeat.count(period + code) > 0:
                            continue
                        new_data = {"period": period}
                        new_data.update(json_df)
                        profit_data.append(new_data)
                        # 添加到重复判断的列表
                        judge_repeat.append(period + code)
        # MongoDB
        mongo_util_instance = mongo_util.MongoUtil()
        mongo_util_instance.add_many(collection='stock_profit', data_json_list=profit_data)
        mongo_util_instance.close()
        print("获取近五年的盈利能力数据成功. count=[{}]".format(len(profit_data)))

    # 获取近五年股票的成长能力情况
    # 保存到MongolianDB中
    """
    code,代码
    name,名称
    mbrg,主营业务收入增长率(%)
    nprg,净利润增长率(%)
    nav,净资产增长率
    targ,总资产增长率
    epsg,每股收益增长率
    seg,股东权益增长率
    """
    @staticmethod
    def obtain_5y_growth():
        judge_repeat = []
        stat_years = [2012, 2013, 2014, 2015, 2016, 2017]
        growth_data = []
        for stat_year in stat_years:
            for q in range(1, 5):
                df = ts.get_growth_data(stat_year, q)
                if df is not None:
                    json_dfs = json.loads(df.to_json(orient='records'))
                    for json_df in json_dfs:
                        period = str(stat_year) + "Q" + str(q)
                        code = str(json_df['code'])
                        # 判重
                        if judge_repeat.count(period + code) > 0:
                            continue
                        new_data = {"period": period}
                        new_data.update(json_df)
                        growth_data.append(new_data)
                        # 添加到重复判断的列表
                        judge_repeat.append(period + code)
        # MongoDB
        mongo_util_instance = mongo_util.MongoUtil()
        mongo_util_instance.add_many(collection='stock_growth', data_json_list=growth_data)
        mongo_util_instance.close()
        print("获取近五年成长能力数据成功. count=[{}]".format(len(growth_data)))

    # 基金持股
    # 获取每个季度基金持有上市公司股票的数据
    # 保存到MongolianDB中
    """
    code：股票代码
    name：股票名称
    date:报告日期
    nums:基金家数
    nlast:与上期相比（增加或减少了）
    count:基金持股数（万股）
    clast:与上期相比
    amount:基金持股市值
    ratio:占流通盘比率
    """
    @staticmethod
    def obtain_5y_fund():
        judge_repeat = []
        stat_years = [2012, 2013, 2014, 2015, 2016, 2017]
        fund_data = []
        for stat_year in stat_years:
            for q in range(1, 5):
                df = ts.fund_holdings(stat_year, q)
                if df is not None:
                    json_dfs = json.loads(df.to_json(orient='records'))
                    for json_df in json_dfs:
                        period = str(stat_year) + "Q" + str(q)
                        code = str(json_df['code'])
                        # 判重
                        if judge_repeat.count(period + code) > 0:
                            continue
                        new_data = {"period": period}
                        new_data.update(json_df)
                        fund_data.append(new_data)
                        # 添加到重复判断的列表
                        judge_repeat.append(period + code)
        # MongoDB
        mongo_util_instance = mongo_util.MongoUtil()
        mongo_util_instance.add_many(collection='stock_fund', data_json_list=fund_data)
        mongo_util_instance.close()
        print("获取近五年基金持股数据成功. count=[{}]".format(len(fund_data)))


if __name__ == "__main__":
    tushare_util = TushareUtil()
    # 中国卫星
    # tushare_util.buy_sell('600118', True)
    # 飞乐音响
    # tushare_util.buy_sell('600651', True)
    # 获取近五年的业绩报告（主表）数据
    tushare_util.obtain_5y_report()
    # 获取近五年的盈利能力的数据
    tushare_util.obtain_5y_profit()
    # 获取近五年成长能力数据
    tushare_util.obtain_5y_growth()
    # 获取近五年基金持股数据
    tushare_util.obtain_5y_fund()
