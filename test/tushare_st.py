import time
import json
import tushare as ts
from pymongo import MongoClient
from config import config


# 大单交易数据
def big_order():
    # 默认400手
    today = time.strftime("%Y-%m-%d", time.localtime())
    df_600118 = ts.get_sina_dd('600118', date=today)
    print(df_600118)
    df_600651 = ts.get_sina_dd('600651', date=today)
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
    print("删除今日数据，Result=", delete_result.raw_result)
    # 600118
    json_list_600118 = json.loads(df_600118.to_json(orient='records'))
    for json_600118 in json_list_600118:
        json_600118.update({'trade_date': today})
    result_600118 = db["big_order"].insert_many(json_list_600118)
    for ids in result_600118.inserted_ids:
        print(ids)
    # 600651
    json_list_600651 = json.loads(df_600651.to_json(orient='records'))
    for json_600651 in json_list_600651:
        json_600651.update({'trade_date': today})
    result_600651 = db["big_order"].insert_many(json_list_600651)
    print(result_600651)


# 根据20MA平均线，评估买卖
# 即设定一个策略：以20日线为标准，当前股价低于20日线的时候就卖出，高于20日线的时候就买入。
def buy_sell(stock_code):
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
    print("stock number : %s" % stock_code)
    print("buy count    : %d" % len(buy_val))
    print("sell count   : %d" % len(sell_val))

    for i in range(len(sell_val)):
        rate = rate * (sell_val[i] * (1 - 0.002) / buy_val[i])
        print("buy date : %s, buy price : %.2f" % (buy_date[i], buy_val[i]))
        print("sell date: %s, sell price: %.2f" % (sell_date[i], sell_val[i]))
    print("The final rate of return: %.2f" % rate)


if __name__ == "__main__":
    # 大单交易
    big_order()
    # 中国卫星
    # buy_sell('600118')
    # 飞乐音响
    # buy_sell('600651')
