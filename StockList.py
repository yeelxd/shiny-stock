# -*- coding: utf-8 -*-
# Python 3.6.3

import requests
from bs4 import BeautifulSoup
import re


def get_html_text(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except (IOError, RuntimeError, BaseException):
        return ""


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


def get_stock_info(stock_list, stock_info_url, output_file):
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


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_file = 'C:/WorkCenter/_Temp/PyDownload/StockInfoList.txt'
    stock_list = []
    get_stock_list(stock_list, stock_list_url)
    get_stock_info(stock_list, stock_info_url, output_file)


# Call Running Center
main()
