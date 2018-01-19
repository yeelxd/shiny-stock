# -*- coding: utf-8 -*-
# Python 3.6.3
# MongoDB CRUD的工具类

from config import config
from pymongo import MongoClient


class MongoUtil(object):

    # 初始化方法
    # 创建完对象后会自动被调用
    def __init__(self):
        try:
            mongo_client = MongoClient(host=config.mogo_host, port=config.mogo_port,
                                       username=config.mogo_user, password=config.mogo_pass,
                                       authMechanism=config.mogo_auth)
            self.client = mongo_client
            self.db = mongo_client[config.mogo_db]
            print("Mongo connect success.")
        except Exception as e:
            print("Mongo connect Err.", e)

    def add_one(self, collection, data_json):
        self.db[collection].insert_one(data_json)

    def add_many(self, collection, data_json_list):
        self.db[collection].insert_many(data_json_list)

    def get_one(self, collection, object_id):
        self.db[collection].find_one(object_id)