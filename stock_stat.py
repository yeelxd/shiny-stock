# -*- coding: utf-8 -*-
# Python 3.6.3

import requests
from bs4 import BeautifulSoup
import re
import time
import mysql_util


# 获取HTML页面内容
def get_html_text(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except (IOError, RuntimeError, BaseException):
        return ""


# 获取股票列表
def get_stock_list(stock_list, stock_list_url):
    html = get_html_text(stock_list_url)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            stock_list.append(re.findall(r"[s][hz][630][0][012]\d{3}", href)[0])
        except (IOError, RuntimeError, BaseException):
            continue


# 获取股票信息并存入本地文件
def get_stock_info_to_file(stock_list, stock_info_url, output_file):
    count = 0
    for stock in stock_list:
        url = stock_info_url + stock + ".html"
        html = get_html_text(url)
        try:
            if html == "":
                continue
            stock_dict = {}
            soup = BeautifulSoup(html, 'html.parser')

            stock_info = soup.find('div', attrs={'class': 'stock-bets'})

            name = stock_info.find_all(attrs={'class': 'bets-name'})[0]
            stock_dict.update({'股票名称': name.text.split()[0]})
            stock_dict.update({'股票代码': name.select("span")[0].text})

            key_list = stock_info.find_all('dt')
            value_list = stock_info.find_all('dd')
            for i in range(len(key_list)):
                key = key_list[i].text
                val = value_list[i].text
                stock_dict[key] = val

            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(str(stock_dict) + '\n\n')
                count = count + 1
                print("\r当前进度: {:.2f}%".format(
                    count * 100 / len(stock_list)), end="")
        except (IOError, RuntimeError, BaseException):
            count = count + 1
            print("\r出错进度: {:.2f}%".format(count * 100 / len(stock_list)), end="")
            continue


# 获取股票信息并存入数据库
def get_stock_info_to_db(stock_list, stock_info_url):
    count = 0
    for stock in stock_list:
        url = stock_info_url + stock + ".html"
        html = get_html_text(url)
        try:
            if html == "":
                continue
            stock_info = {}
            soup = BeautifulSoup(html, 'html.parser')
            stock_info_div = soup.find('div', attrs={'class': 'stock-bets'})

            name = stock_info_div.find_all(attrs={'class': 'bets-name'})[0]
            stock_info.update({'stock_type': stock[0:2].upper()})
            stock_info.update({'stock_code': name.text.split()[0].strip()})
            stock_info.update({'stock_name': name.select("span")[0].text.strip()})

            dd_list = stock_info_div.find_all('dd')
            pe = float(dd_list[8].text.strip())
            # 根据市盈率筛选优质股票
            if pe > 100:
                continue
            stock_info.update({'today_open': float(dd_list[0].text.strip())})
            stock_info.update({'today_low': float(dd_list[13].text.strip())})
            stock_info.update({'today_high': float(dd_list[2].text.strip())})
            stock_info.update({'turn_rate': dd_list[12].text.strip()})
            stock_info.update({'swing_rate': dd_list[16].text.strip()})
            # 今日价格
            today_price = stock_info_div.find('strong', attrs={'class': '_close'}).text.strip()
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
            stock_info.update({'pb': float(dd_list[19].text.strip())})
            stock_info.update({'eps': float(dd_list[9].text.strip())})
            stock_info.update({'bps': float(dd_list[20].text.strip())})
            stock_info.update({'market_equity': dd_list[21].text.strip()})
            stock_info.update({'total_equity': dd_list[10].text.strip()})

            # 所属行业
            industry_part = soup.find('div', attrs={'class': 'industry'}).find_all('p')[0].text.strip()
            stock_info.update({'industry_part': industry_part})
            # 关注度
            attention_rate = soup.find('span', attrs={'class': 'add-stock-count'}).text.strip()
            stock_info.update({'attention_rate': int(attention_rate)})

            # 保存到MySQL数据库中
            mysql_util.MysqlUtil.add(mysql_util.MysqlUtil(), stock_info=stock_info)

            # 打印进度
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(stock_list)), end="")
        except Exception as e:
            print(e)
            count = count + 1
            continue


# 执行主方法
def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    stock_list = []
    get_stock_list(stock_list, stock_list_url)
    # output_file = 'C:/WorkCenter/_Temp/PyDownload/StockInfoList.txt'
    # get_stock_info_to_file(stock_list, stock_info_url, output_file)
    get_stock_info_to_db(stock_list, stock_info_url)


# Call Running Center
main()
