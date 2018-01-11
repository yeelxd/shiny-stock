# -*- coding: utf-8 -*-
# Python 3.6.3
# MySQL 数据库CRUD的工具类

import pymysql
from config import config


# MySQL操作类，使用ini的配置文件
class MysqlUtil(object):

    # 初始化
    def __init__(self):
        # 连接MySQL
        try:
            conn = pymysql.connect(
                host=config.db_host,
                port=config.db_port,
                user=config.db_user,
                passwd=config.db_pass,
                db=config.db_name,
                charset=config.db_charset
            )
            self.conn = conn
            print("MySQL连接成功")
        except Exception as e:
            print("MySQL连接Err.", e)

    # 关闭连接
    def close(self):
        self.conn.close()

    # 新增记录
    def add(self, stock_info):
        sql = "insert into stock_info(stock_type, stock_code, stock_name, \
                today_open, today_low, today_high, turn_rate, swing_rate, \
                today_price, today_rose, last_price, limit_up, limit_down, trade_date, \
                trade_num, trade_amount, in_trade, out_trade, trade_scale, \
                volume_scale, market_value, total_value, pe, pb, eps, bps, \
                market_equity, total_equity, industry_part, attention_rate, \
                create_date) values('%s', '%s', '%s', \
                '%f', '%f', '%f', '%s', '%s', \
                '%f', '%s', '%f', '%f', '%f', '%s', \
                '%s', '%s', '%s', '%s', '%s', \
                '%s', '%s', '%s', '%F', '%f', '%F', '%f', \
                '%s', '%s', '%s', '%d', \
                NOW())" % \
                (stock_info['stock_type'], stock_info['stock_code'], stock_info['stock_name'],
                 stock_info['today_open'], stock_info['today_low'], stock_info['today_high'],
                 stock_info['turn_rate'], stock_info['swing_rate'], stock_info['today_price'],
                 stock_info['today_rose'],
                 stock_info['last_price'], stock_info['limit_up'], stock_info['limit_down'],
                 stock_info['trade_date'], stock_info['trade_num'], stock_info['trade_amount'],
                 stock_info['in_trade'], stock_info['out_trade'], stock_info['trade_scale'],
                 stock_info['volume_scale'], stock_info['market_value'], stock_info['total_value'],
                 stock_info['pe'], stock_info['pb'], stock_info['eps'], stock_info['bps'],
                 stock_info['market_equity'], stock_info['total_equity'],
                 stock_info['industry_part'], stock_info['attention_rate'])
        cursor = self.conn.cursor()
        res = cursor.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        # 关闭指针对象
        cursor.close()

    # 根据主键删除一条记录
    def remove(self, sid):
        sql = "delete from stock_info where id='%d'" % sid
        cursor = self.conn.cursor()
        res = cursor.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        # 关闭指针对象
        cursor.close()

    # 根据主键查询一条记录
    def query_by_sid(self, sid):
        sql = "select * from stock_info where id='%d'" % sid
        cursor = self.conn.cursor()
        self.execute(sql)
        res = self.fetchone()
        # 关闭指针对象
        cursor.close()
        return res
