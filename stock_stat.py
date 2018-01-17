# -*- coding: utf-8 -*-
# Python 3.6.3

import requests
from bs4 import BeautifulSoup
import re
import time
from util import mysql_util
import json
import os
from multiprocessing.dummy import Pool


# 股票详情URL列表
STOCK_URL_LIST = []
# 股票信息对象列表
STOCK_INFO_LIST = []


# 获取HTML页面内容
def get_html_text(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
    header = {'User-Agent': user_agent, 'Accept': '*/*'}
    try:
        # 不设置超时时间, 一直等待中..
        r = requests.get(url, headers=header, timeout=None)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        print("获取HTML页面内容Err.", e)
        return ""


# 获取股票列表
def get_stock_list(stock_list_url, stock_info_url):
    html = get_html_text(stock_list_url)
    # Page Html
    html_soup = BeautifulSoup(html, 'html.parser')
    # Html Body
    quote_body = html_soup.find('div', attrs={'class': 'quotebody'})
    all_a = quote_body.find_all('a', attrs={'target': '_blank'})
    for a in all_a:
        try:
            href = a.attrs['href']
            stock_code = re.findall(r"[s][hz][60][0][012]\d{3}", href)
            if len(stock_code) > 0:
                stock_url = stock_info_url + stock_code[0] + ".html"
                # 谨防重复处理
                if STOCK_URL_LIST.count(stock_url) == 0:
                    STOCK_URL_LIST.append(stock_url)
        except Exception as e:
            print("获取股票列表Err.", e)
            continue


# 获取股票详情信息
def package_stock_info(stock_info_url):
    # Debugger URL
    # stock_info_url = "https://gupiao.baidu.com/stock/sh600359.html"
    # 关注度获取API
    stock_attention_url = 'https://gupiao.baidu.com/stock/api/rails/stockfollownum?stock_code='
    # 获取股票信息
    start_rot = stock_info_url.rfind("/")+1
    stock = stock_info_url[start_rot:start_rot+8]
    html = get_html_text(stock_info_url)
    # Http出错再获取一次
    if html == "" or html.count('class="error-page-bg"') > 0:
        html = get_html_text(stock_info_url)
    try:
        if html == "" or html.count('class="error-page-bg"') > 0:
            return None
        soup = BeautifulSoup(html, 'html.parser')
        stock_info_div = soup.find('div', attrs={'class': 'stock-bets'})
        industry_div = soup.find('div', attrs={'class': 'industry'})
        if stock_info_div is None or industry_div is None:
            print("获取股票信息{%s} is None. html={%s}" % (stock, html))
            return None

        # 是否是已收盘
        trade_status = stock_info_div.find_all('span')[1].text.strip()
        # 状态: 停牌/未开盘/交易中/午间休市/已收盘/已休市/已退市
        if trade_status[0:3] not in ("交易中", "已收盘"):
            return None

        stock_info = {}
        name = stock_info_div.find_all(attrs={'class': 'bets-name'})[0]
        stock_info.update({'stock_type': stock[0:2].upper()})
        stock_info.update({'stock_code': name.select("span")[0].text.strip()})
        name_text_str = name.text.strip()
        stock_name = name_text_str[0:name_text_str.index("(")].strip()
        if stock_name[0:1] == "N" or stock_name.count("ST") > 0:
            return None
        stock_info.update({'stock_name': stock_name})

        dd_list = stock_info_div.find_all('dd')
        pe_str = dd_list[8].text.strip()
        pb_str = dd_list[19].text.strip()
        eps_str = dd_list[9].text.strip()
        bps_str = dd_list[20].text.strip()
        if pe_str == "--" or pb_str == "--" or eps_str == "--" or bps_str == "--":
            return None
        # 严格控制系数
        # 一般市盈率{pe=股价/每股收益}合理区间[10-20]
        # 一般市净率{pb=股价/每股净资产}合理区间[3-10]
        # 一般每股收益{eps=税后利润与股本总数的比率}合理区间[>0.3]
        pe = float(pe_str)
        pb = float(pb_str)
        eps = float(eps_str)
        # 每股净资产{bps=股东权益 / 总股数}
        bps = float(bps_str)
        # 一般净资产收益率{roe=每股收益eps/每股净资产bps}合理区间[>15%]
        roe = eps * 100 / bps
        if pe > 20 or pb > 10 or eps < 0.3 or roe < 15:
            return None
        stock_info.update({'today_open': float(dd_list[0].text.strip())})
        stock_info.update({'today_low': float(dd_list[13].text.strip())})
        stock_info.update({'today_high': float(dd_list[2].text.strip())})
        stock_info.update({'turn_rate': dd_list[12].text.strip()})
        stock_info.update({'swing_rate': dd_list[16].text.strip()})
        # 今日价格
        today_price = stock_info_div.find('strong', attrs={'class': '_close'}).text.strip()
        if today_price == "--":
            return None
        stock_info.update({'today_price': float(today_price)})
        # 今日涨幅
        today_rose = stock_info_div.find_all('span')[3].text.strip()
        stock_info.update({'today_rose': today_rose})
        stock_info.update({'last_price': float(dd_list[11].text.strip())})
        stock_info.update({'limit_up': float(dd_list[3].text.strip())})
        stock_info.update({'limit_down': float(dd_list[14].text.strip())})
        stock_info.update({'trade_date': time.strftime("%Y-%m-%d", time.localtime())})
        stock_info.update({'trade_num': dd_list[1].text.strip()})
        stock_info.update({'trade_amount': dd_list[5].text.strip()})
        stock_info.update({'in_trade': dd_list[4].text.strip()})
        stock_info.update({'out_trade': dd_list[15].text.strip()})
        stock_info.update({'trade_scale': dd_list[6].text.strip()})
        stock_info.update({'volume_scale': dd_list[17].text.strip()})
        stock_info.update({'market_value': dd_list[7].text.strip()})
        stock_info.update({'total_value': dd_list[18].text.strip()})
        stock_info.update({'pe': pe})
        stock_info.update({'pb': pb})
        stock_info.update({'eps': eps})
        stock_info.update({'bps': bps})
        stock_info.update({'roe': round(roe, 2)})
        stock_info.update({'market_equity': dd_list[21].text.strip()})
        stock_info.update({'total_equity': dd_list[10].text.strip()})

        # 所属行业
        industry_part = industry_div.find('p').text.strip()
        stock_info.update({'industry_part': industry_part})
        # 关注度
        attention_rate = 0
        attention_url = stock_attention_url + stock
        attention_html = get_html_text(attention_url)
        if attention_html != "":
            attention_json = json.loads(attention_html)
            if attention_json['errorMsg'] == "success":
                attention_rate = attention_json['data']
        stock_info.update({'attention_rate': int(attention_rate)})
        # 封装好的信息添加到待处理列表
        STOCK_INFO_LIST.append(stock_info)
        print("获取成功: pid={}, url={}".format(os.getpid(), stock_info_url))
        print("所在列表位置: {}/{}".format(STOCK_URL_LIST.index(stock_info_url), len(STOCK_URL_LIST)))
    except Exception as e:
        print("获取股票信息{%s}Err." % stock, e)


# 执行主方法
def main_center():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    get_stock_list(stock_list_url, stock_info_url)
    # 筛选股票信息保存到数据库中
    print("待筛选的股票数量={}".format(len(STOCK_URL_LIST)))
    # 记录开始时间
    start_time = time.time()
    # 使用四个进程处理任务
    pool = Pool(4)
    pool.map(package_stock_info, STOCK_URL_LIST)
    pool.close()
    pool.join()
    # 列表去重
    new_stock_info_list = []
    for stock_info in STOCK_INFO_LIST:
        if stock_info not in new_stock_info_list:
            new_stock_info_list.append(stock_info)
    # 保存到DB
    # 实例化MySQL工具类并保存
    mysql_util_instance = mysql_util.MysqlUtil()
    mysql_util_instance.add_many(new_stock_info_list)
    mysql_util_instance.close()
    end_time = time.time()
    # 计算程序执行耗时
    total_time = end_time - start_time
    print("筛选股票信息完毕，共获取[{0}]只，耗时：{1:.2f}秒".format(len(new_stock_info_list), total_time))


# Call Running Center
main_center()
