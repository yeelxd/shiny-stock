# Crawler Test For tushare api
# Dependency tushare Modules
# Python 3.6.3
import time
import json
import tushare as ts
from pymongo import MongoClient
from config import config


class TushareST(object):

    # 大单交易数据
    # 默认400手
    def big_order(self):
        today = time.strftime("%Y-%m-%d", time.localtime())
        df_600118 = ts.get_sina_dd('600118', date=today)
        print(df_600118)
        df_600651 = ts.get_sina_dd('600651', date=today, vol=1000)
        print(df_600651)

        # 存储到MongoDB中
        # uri = "mongodb://user:password@example.com/the_database?authMechanism=MONGODB-CR"
        mongo_client = MongoClient(host=config.mogo_host, port=config.mogo_port,
                                   username=config.mogo_user, password=config.mogo_pass,
                                   authMechanism=config.mogo_auth)
        db = mongo_client[config.mogo_db]
        # 首先删除今日的数据
        filter_param = {"trade_date": today}
        delete_result = db["big_order"].delete_many(filter_param)
        print("删除今日统计数据，Result=", delete_result.raw_result)
        delete_stat_result = db["big_order_stat"].delete_many(filter_param)
        print("删除今日汇总数据，Result=", delete_stat_result.raw_result)
        # 600118
        if df_600118 is not None:
            json_list_600118 = json.loads(df_600118.to_json(orient='records'))
            for json_600118 in json_list_600118:
                json_600118.update({'trade_date': today})
            result_600118 = db["big_order"].insert_many(json_list_600118)
            print("{600118}插入记录数=", len(result_600118.inserted_ids))
            # 统计当天的大单净量并插入到Mongo中
            net_json_600118 = self.big_order_stat_func(json_list_600118)
            net_result_600118 = db["big_order_stat"].insert_one(net_json_600118)
            print("{600118}插入大单净量结果=", net_result_600118.inserted_id)
        # 600651
        if df_600651 is not None:
            json_list_600651 = json.loads(df_600651.to_json(orient='records'))
            for json_600651 in json_list_600651:
                json_600651.update({'trade_date': today})
            result_600651 = db["big_order"].insert_many(json_list_600651)
            print("{600118}插入记录数=", len(result_600651.inserted_ids))
            # 统计当天的大单净量并插入到Mongo中
            net_json_600651 = self.big_order_stat_func(json_list_600651)
            net_result_600651 = db["big_order_stat"].insert_one(net_json_600651)
            print("{600651}插入大单净量结果=", net_result_600651.inserted_id)

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
    # 大单交易
    # tushare_st.big_order()
