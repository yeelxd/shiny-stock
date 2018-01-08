# -*- coding: utf-8 -*-
# Python 3.6.3

import requests
from bs4 import BeautifulSoup
import re


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except (IOError, RuntimeError, BaseException):
        return ""


def getStockList(slist, stock_list_url):
    html = getHTMLText(stock_list_url)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            slist.append(re.findall(r"[s][hz][6|3|0][0][0|1|2]\d{3}", href)[0])
        except (IOError, RuntimeError, BaseException):
            continue


def getStockInfo(slist, stock_info_url, output_file):
    count = 0
    for stock in slist:
        url = stock_info_url + stock + ".html"
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')

            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})

            name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
            infoDict.update({'股票名称': name.text.split()[0]})
            infoDict.update({'股票代码': name.select("span")[0].text})

            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val

            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(str(infoDict) + '\n\n')
                count = count + 1
                print("\r当前进度: {:.2f}%".format(
                    count * 100 / len(slist)), end="")
        except (IOError, RuntimeError, BaseException):
            count = count + 1
            print("\r出错进度: {:.2f}%".format(count * 100 / len(slist)), end="")
            continue


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_file = 'C:/WorkCenter/_Temp/PyDownload/StockInfoList.txt'
    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)


# Call Running Center
main()
