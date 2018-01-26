# Crawler Test For tushare API util
# Dependency tushare Modules
# Python 3.6.3

import tushare as ts


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


if __name__ == "__main__":
    tushare_util = TushareUtil()
    # 中国卫星
    # tushare_util.buy_sell('600118', True)
    # 飞乐音响
    # tushare_util.buy_sell('600651', True)
    tushare_util.buy_sell('600118', False)
