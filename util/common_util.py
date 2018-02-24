# -*- coding: utf-8 -*-
# Python 3.6.3
# OsUtil 公共操作根据类
from datetime import timedelta, date


class CommonUtil(object):

    # 获取当前日期的前后N天的日期(return date format)
    @staticmethod
    def get_day_of_day(n=0):
        """
        if n>=0,date is larger than today
        if n<0,date is less than today
        date format = "YYYY-MM-DD"
        """
        g_date = date.today()
        if n < 0:
            n = abs(n)
            g_date = g_date - timedelta(days=n)
        else:
            g_date = g_date + timedelta(days=n)
        return g_date

