# Crawler Test For tushare API util
# Dependency tushare Modules
# Python 3.6.3

import tushare as ts
import json
from util import mongo_util
from util.os_util import OsUtil
import time


class TushareUtil(object):

    # 大单交易数据
    # 默认400手
    def big_order(self, stock_code_list):
        # MongoDB
        mongo_util_instance = mongo_util.MongoUtil()
        # 首先删除今日的数据
        today = time.strftime("%Y-%m-%d", time.localtime())
        filter_param = {"trade_date": today}
        mongo_util_instance.del_many(collection='big_order', filter_param=filter_param)
        mongo_util_instance.del_many(collection='big_order_stat', filter_param=filter_param)
        print("删除今日大单统计数据成功")
        # 循环处理股票列表
        for stock_code in stock_code_list:
            try:
                df = ts.get_sina_dd(stock_code, date=today)
                print(df)
                if df is not None:
                    json_list = json.loads(df.to_json(orient='records'))
                    new_json_list = []
                    for json_data in json_list:
                        new_json_data = {'trade_date': today}
                        new_json_data.update(json_data)
                        new_json_list.append(new_json_data)
                    # 保存到MongoDB
                    mongo_util_instance.add_many(collection='big_order', data_json_list=new_json_data)
                    # 统计当天的大单净量并插入到Mongo中
                    net_json = self.trade_net_stat_func(json_list)
                    mongo_util_instance.add_one(collection='big_order_stat', data_json=net_json)
            except Exception as e:
                print("大单数据统计异常", e)
        print("新增今日大单统计数据成功")
        # 关闭Mongo连接
        mongo_util_instance.close()

    # 统计当天的交易净量
    @staticmethod
    def trade_net_stat_func(df_json_list):
        net_stat = 0
        for df_json in df_json_list:
            # 买卖类型【买盘、卖盘、中性盘】
            trade_type = df_json['type']
            trade_volume = int(df_json['volume'])
            if trade_type == "中性盘":
                continue
            if trade_type == "卖盘":
                trade_volume = trade_volume * (-1)
            net_stat += trade_volume
        # 更新列表信息
        big_order_stat = {"trade_date": df_json_list[0]['trade_date']}
        big_order_stat.update({"code": df_json_list[0]['code']})
        big_order_stat.update({"name": df_json_list[0]['name']})
        net_type = "买入"
        if net_stat < 0:
            net_type = "卖出"
        big_order_stat.update({"type": net_type})
        big_order_stat.update({"volume": net_stat})
        return big_order_stat

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
        # 四舍五入到个位
        rate = round(rate * 100)
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

    # 沪深300的成分股及其权重
    # 日期转换https://www.epochconverter.com/
    # 默认`epoch` = epoch milliseconds - 毫秒数
    """
    code :股票代码
    name :股票名称
    date :日期
    weight:权重
    """
    @staticmethod
    def obtain_hs300_weight():
        df = ts.get_hs300s()
        if df is not None:
            json_dfs = json.loads(df.to_json(orient='records'))
            # 对筛选结果根据weight排序--降序
            json_dfs.sort(key=lambda obj: obj.get('weight'), reverse=True)
            for json_df in json_dfs:
                # 转换日期
                date_stamp = json_df['date'] / 1000
                date_str = time.strftime("%Y-%m-%d", time.localtime(date_stamp))
                json_df['date'] = date_str
            # MongoDB
            mongo_util_instance = mongo_util.MongoUtil()
            mongo_util_instance.add_many(collection='stock_hs300', data_json_list=json_dfs)
            mongo_util_instance.close()
            print("获取沪深300的成分股及其权重. count=[{}]".format(len(json_dfs)))

    # 统计近三个月的历史分笔交易的数据，大致判断资金的进出情况
    # stock_info_list : [{'code':'600118', 'name':'中国卫星'}]
    def history_trade_stat(self, stock_info_list):
        # MongoDB
        mongo_util_instance = mongo_util.MongoUtil()
        try:
            # 循环处理股票列表
            for stock_info in stock_info_list:
                # 首先删除该股票的历史统计数据
                mongo_util_instance.del_many(collection='stock_hisorder', filter_param=stock_info)
                print("删除已存的统计数据成功:", stock_info)
                # 循环调用历史分笔数据接口
                code = stock_info['code']
                # 每天交易净量的集合
                net_list = []
                for i in range(1, 91):
                    try:
                        p_date = OsUtil.get_day_of_day(-i)
                        trade_date = p_date.strftime("%Y-%m-%d")
                        df = ts.get_tick_data(code=code, date=trade_date)
                        if df is not None:
                            json_list = json.loads(df.to_json(orient='records'))
                            # 当天无数据
                            if json_list[0]['price'] is None:
                                continue
                            for json_data in json_list:
                                json_data.update(stock_info)
                                json_data.update({'trade_date': trade_date})
                            # 统计当天的交易净量
                            net_json = self.trade_net_stat_func(json_list)
                            net_list.append(net_json)
                    except Exception as e:
                        print("获取指定日期的分笔数据Err.", e)
                    finally:
                        time.sleep(2)
                if len(net_list) > 0:
                    # 汇总所有净量数据
                    net_stat_json = self.trade_net_stat_func(net_list)
                    net_stat_json.update({'trade_date': '0000-00-00'})
                    # 交易净量插入到Mongo中
                    mongo_util_instance.add_one(collection='stock_hisorder', data_json=net_stat_json)
                    mongo_util_instance.add_many(collection='stock_hisorder', data_json_list=net_list)
                print("历史分笔交易统计成功:", stock_info)
        except Exception as e:
            print(e)
        finally:
            # 最后关闭Mongo的连接
            mongo_util_instance.close()

    # 一次性获取当前交易所有股票的行情数据(如果是节假日，即为上一交易日)
    """
    code：代码
    name:名称
    changepercent:涨跌幅
    trade:现价
    open:开盘价
    high:最高价
    low:最低价
    settlement:昨日收盘价
    volume:成交量
    turnoverratio:换手率
    amount:成交量
    per:市盈率
    pb:市净率
    mktcap:总市值
    nmc:流通市值
    """
    @staticmethod
    def obtain_today_all():
        # MongoDB
        mongo_util_instance = mongo_util.MongoUtil()
        try:
            # 首先删除今日的数据
            today = time.strftime("%Y-%m-%d", time.localtime())
            filter_param = {"trade_date": today}
            mongo_util_instance.del_many(collection='stock_today', filter_param=filter_param)
            print("删除今日行情交易数据成功")
            df = ts.get_today_all()
            if df is not None:
                json_list = json.loads(df.to_json(orient='records'))
                new_json_list = []
                for json_data in json_list:
                    new_json_data = {'trade_date': today}
                    new_json_data.update(json_data)
                    new_json_list.append(new_json_data)
                # 今日所有交易行情数据存入Mongo
                mongo_util_instance.add_many(collection='stock_today', data_json_list=new_json_list)
                print("\n获取今日行情交易数据成功, len={}".format(len(new_json_list)))
        except Exception as e:
            print(e)
        finally:
            # 最后关闭Mongo的连接
            mongo_util_instance.close()

    # 获取实时分笔数据，可以实时取得股票当前报价和成交信息
    """
    symbols：6位数字股票代码，
    或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
    可输入的类型：str、list、set或者pandas的Series对象
    """
    @staticmethod
    def obtain_realtime(stock_code_list):
        # MongoDB
        mongo_util_instance = mongo_util.MongoUtil()
        try:
            # 首先删除今日的数据
            today = time.strftime("%Y-%m-%d", time.localtime())
            filter_param = {"trade_date": today}
            mongo_util_instance.del_many(collection='stock_realtime', filter_param=filter_param)
            print("删除实时行情交易数据成功")
            df = ts.get_realtime_quotes(stock_code_list)
            if df is not None:
                new_df = df[['code', 'name', 'open', 'pre_close', 'price', 'low', 'high', 'volume', 'amount', 'time']]
                json_list = json.loads(new_df.to_json(orient='records'))
                new_json_list = []
                for json_data in json_list:
                    new_json_data = {'trade_date': today}
                    new_json_data.update(json_data)
                    new_json_list.append(new_json_data)
                # 今日所有交易行情数据存入Mongo
                mongo_util_instance.add_many(collection='stock_realtime', data_json_list=new_json_list)
                print("获取实时行情交易数据成功, len={}".format(len(new_json_list)))
        except Exception as e:
            print(e)
        finally:
            # 最后关闭Mongo的连接
            mongo_util_instance.close()


if __name__ == "__main__":
    tushare_util = TushareUtil()
    # 中国卫星
    # tushare_util.buy_sell('600118', True)
    # 飞乐音响
    # tushare_util.buy_sell('600651', True)
