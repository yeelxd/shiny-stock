# Crawler Test For tushare api
# Dependency tushare Modules
# Python 3.6.3
import time
import json
import tushare as ts
from util import mongo_util


class TushareST(object):

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
                    for json_data in json_list:
                        json_data.update({'trade_date': today})
                    # 保存到MongoDB
                    mongo_util_instance.add_many(collection='big_order', data_json_list=json_list)
                    # 统计当天的大单净量并插入到Mongo中
                    net_json = self.big_order_stat_func(json_list)
                    mongo_util_instance.add_one(collection='big_order_stat', data_json=net_json)
            except Exception as e:
                print("大单数据统计异常", e)
        print("新增今日大单统计数据成功")
        # 关闭Mongo连接
        mongo_util_instance.close()

    # 统计当天的大单净量
    @staticmethod
    def big_order_stat_func(df_json_list):
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
        big_order_stat.update({"net_type": net_type})
        big_order_stat.update({"net_volume": net_stat})
        return big_order_stat


if __name__ == "__main__":
    tushare_st = TushareST()
    # 大单交易 600118 600651
    stock_code_post = ["600118", "600651", "600038"]
    tushare_st.big_order(stock_code_post)
