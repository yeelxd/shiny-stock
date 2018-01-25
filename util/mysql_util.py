# -*- coding: utf-8 -*-
# Python 3.6.3
# MySQL 数据库CRUD的工具类

import pymysql
from config import config


# MySQL操作类，使用ini的配置文件
class MysqlUtil(object):

    # 初始化方法
    # 创建完对象后会自动被调用
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
            print("MySQL connect success.")
        except Exception as e:
            print("MySQL connect Err.", e)

    # 关闭连接
    def close(self):
        try:
            self.conn.close()
            print("MySQL close success.")
        except Exception as e:
            print("MySQL close Err.", e)

    # 获取游标
    def get_cur(self):
        return self.conn.cursor()

    # 关闭游标
    def close_cur(self):
        self.get_cur().close()

    # 新增一条记录
    def add(self, stock_info):
        sql = "insert into stock_info(stock_type, stock_code, stock_name, \
                today_open, today_low, today_high, turn_rate, swing_rate, \
                today_price, today_rose, last_price, limit_up, limit_down, trade_date, \
                trade_num, trade_amount, in_trade, out_trade, trade_scale, \
                volume_scale, market_value, total_value, pe, pb, eps, bps, roe, \
                market_equity, total_equity, industry_part, attention_rate, \
                create_date) values('%s', '%s', '%s', \
                %f, %f, %f, '%s', '%s', \
                %f, '%s', %f, %f, %f, '%s', \
                '%s', '%s', '%s', '%s', '%s', \
                '%s', '%s', '%s', %f, %f, %f, %f, %f, \
                '%s', '%s', '%s', %d, \
                NOW())" % \
                (stock_info['stock_type'], stock_info['stock_code'], stock_info['stock_name'],
                 stock_info['today_open'], stock_info['today_low'], stock_info['today_high'],
                 stock_info['turn_rate'], stock_info['swing_rate'], stock_info['today_price'],
                 stock_info['today_rose'],
                 stock_info['last_price'], stock_info['limit_up'], stock_info['limit_down'],
                 stock_info['trade_date'], stock_info['trade_num'], stock_info['trade_amount'],
                 stock_info['in_trade'], stock_info['out_trade'], stock_info['trade_scale'],
                 stock_info['volume_scale'], stock_info['market_value'], stock_info['total_value'],
                 stock_info['pe'], stock_info['pb'], stock_info['eps'], stock_info['bps'], stock_info['roe'],
                 stock_info['market_equity'], stock_info['total_equity'],
                 stock_info['industry_part'], stock_info['attention_rate'])
        try:
            self.get_cur().execute(sql)
            self.conn.commit()
        except Exception as e:
            print("add Err.", e)
            self.conn.rollback()
        finally:
            self.close_cur()

    # 新增多条记录
    def add_many(self, stock_info_list):
        # 不管什么类型，统一使用%s/?作为占位符
        sql = "insert into stock_info(stock_type, stock_code, stock_name, \
                today_open, today_low, today_high, turn_rate, swing_rate, \
                today_price, today_rose, last_price, limit_up, limit_down, trade_date, \
                trade_num, trade_amount, in_trade, out_trade, trade_scale, \
                volume_scale, market_value, total_value, pe, pb, eps, bps, roe, \
                market_equity, total_equity, industry_part, attention_rate, \
                create_date) values(%s, %s, %s, \
                %s, %s, %s, %s, %s, \
                %s, %s, %s, %s, %s, %s, \
                %s, %s, %s, %s, %s, \
                %s, %s, %s, %s, %s, %s, %s, %s, \
                %s, %s, %s, %s, \
                NOW())"
        params = []
        for stock_info in stock_info_list:
            params.append((stock_info['stock_type'], stock_info['stock_code'], stock_info['stock_name'],
                          stock_info['today_open'], stock_info['today_low'], stock_info['today_high'],
                          stock_info['turn_rate'], stock_info['swing_rate'],
                          stock_info['today_price'], stock_info['today_rose'], stock_info['last_price'],
                          stock_info['limit_up'], stock_info['limit_down'], stock_info['trade_date'],
                          stock_info['trade_num'], stock_info['trade_amount'], stock_info['in_trade'],
                          stock_info['out_trade'], stock_info['trade_scale'],
                          stock_info['volume_scale'], stock_info['market_value'], stock_info['total_value'],
                          stock_info['pe'], stock_info['pb'], stock_info['eps'], stock_info['bps'],
                          stock_info['roe'],
                          stock_info['market_equity'], stock_info['total_equity'],
                          stock_info['industry_part'], stock_info['attention_rate']))
        try:
            self.get_cur().executemany(sql, args=params)
            self.conn.commit()
            print("saved success. count={}".format(len(stock_info_list)))
        except Exception as e:
            print("add_many Err.", e)
            self.conn.rollback()
        finally:
            self.close_cur()

    # 根据主键删除一条记录
    def remove_by_id(self, sid):
        sql = "delete from stock_info where id='%d'" % sid
        try:
            self.get_cur().execute(sql)
            self.conn.commit()
        except Exception as e:
            print("remove Err.", e)
            self.conn.rollback()
        finally:
            self.close_cur()

    # 根据交易日期删除记录
    def remove_by_trade_date(self, trade_date):
        sql = "delete from stock_info where trade_date='%s'" % trade_date
        try:
            self.get_cur().execute(sql)
            self.conn.commit()
        except Exception as e:
            print("remove Err.", e)
            self.conn.rollback()
        finally:
            self.close_cur()

    # 根据主键查询一条记录
    def query_by_sid(self, sid):
        sql = "select * from stock_info where id=%d" % sid
        try:
            cursor = self.get_cur()
            cursor.execute(sql)
            res = cursor.fetchone()
            return res
        except Exception as e:
            print("query_by_sid Err.", e)
            self.conn.rollback()
        finally:
            self.close_cur()

    '''使用谁调用谁关闭的原则
    # 析构方法
    # 当对象被删除时，会自动被调用
    def __del__(self):
        self.close()
    '''


if __name__ == "__main__":
    MysqlUtil = MysqlUtil()
    print(MysqlUtil.query_by_sid(1))
    MysqlUtil.close()
