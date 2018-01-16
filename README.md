shiny-stock
=======================================================================
    Python 3.6.3
    Python Stock Project
    2018.01.08
    本项目基于Python的开发语言的架构优势，以爬虫的的方式获取优质的股票代码。

采集数据来源：
------------------------------------------------------------------------
    股票列表来自：[东方财富](http://quote.eastmoney.com/stocklist.html)
    股票详情信息来自：[百度股票](https://gupiao.baidu.com/stock/SH600118.html)

数据库使用MySQL：
------------------------------------------------------------------------
        参考SQL文件：resources/DB.sql

stock_info      股票日数据记录表
------------------------------------------------------------------------
    id              主键PK
    stock_type      股票类型(SH-上海交易所，SZ-深圳交易所)
    stock_code      股票代码
    stock_name      股票名称
    today_open      今开价
    today_low       今天最低价
    today_high      今天最高价
    turn_rate       换手率(在一定时间内市场中股票转手买卖的频率)
    swing_rate      振幅(股票开盘后的当日最高价和最低价之间的差的绝对值与前日收盘价的百分比)
    today_price     今天收盘价
    today_rose      今日涨幅
    last_price      昨天收盘价
    limit_up        涨停价
    limit_down      跌停价
    trade_date      交易日期(yyyy-MM-dd)   
    trade_num       成交量
    trade_amount    成交额
    in_trade        内盘(卖家以买家的买入价而卖出成交，成交价为申买价，说明抛盘比较踊跃)
    out_trade       外盘(买家以卖家的卖出价而买入成交，成交价为申卖价，说明买盘比较积极)
    trade_scale     委比(委比=（委买手数－委卖手数）／（委买手数＋委卖手数）×100％，委比同股票价格正相关)
    volume_scale    量比(量比=现成交总手/((过去5个交易日平均每分钟成交量)×当日累计开市时间(分)))
    market_value    流通市值
    total_value     总市值
    pe              市盈率MRQ(每股市价除以每股盈利(Earnings Per Share,EPS))
    pb              市净率(每股股价与每股净资产的比率)
    eps             每股收益(又称每股税后利润、每股盈余，指税后利润与股本总数的比率)
    bps             每股净资产(每股帐面价值，股东权益 / 总股数)
    roe             净资产收益率ROE(%)(每股收益eps/每股净资产bps)
    market_equity   流通股本
    total_equity    总股票
    industry_part   所属行业
    attention_rate  关注度(多少人关注该股票)
    create_date     创建时间

####频繁访问出错:
        \<div class="wrap">
            \<div class="error-page">
                \<div class="error-page-bg"></div>
                \<h2>404</h2>
                \<p>雾霾太大，连页面都看不见了</p>
                \<a href="/" target="_parent">去首页看看</a>
            \</div>
        \</div>

