import time
import json
import tushare as ts
from pymongo import MongoClient
from config import config

# 大单交易数据
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
result_600118 = db["big_order"].insert_many(json.loads(df_600118.to_json(orient='records')))
for ids in result_600118.inserted_ids:
    print(ids)
result_600651 = db["big_order"].insert_many(json.loads(df_600651.to_json(orient='records')))
print(result_600651)
