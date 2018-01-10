-- --------------------------------------------------------
-- 主机:                              127.0.0.1
-- 服务器版本:                        5.7.17-log - MySQL Community Server (GPL)
-- 服务器操作系统:                    Win64
-- HeidiSQL 版本:                     9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 shinycenter 的数据库结构
CREATE DATABASE IF NOT EXISTS `shinycenter` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `shinycenter`;

-- 导出  表 shinycenter.stock_info 结构
CREATE TABLE IF NOT EXISTS `stock_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键PK',
  `stock_type` varchar(8) DEFAULT NULL COMMENT '股票类型(SH-上海交易所，SZ-深圳交易所)',
  `stock_code` varchar(20) DEFAULT NULL COMMENT '股票代码',
  `stock_name` varchar(50) DEFAULT NULL COMMENT '股票名称',
  `today_open` float(10,2) DEFAULT NULL COMMENT '今开价',
  `today_low` float(10,2) DEFAULT NULL COMMENT '今天最低价',
  `today_high` float(10,2) DEFAULT NULL COMMENT '今天最高价',
  `turn_rate` varchar(20) DEFAULT NULL COMMENT '换手率(在一定时间内市场中股票转手买卖的频率)',
  `swing_rate` varchar(20) DEFAULT NULL COMMENT '振幅(股票开盘后的当日最高价和最低价之间的差的绝对值与前日收盘价的百分比)',
  `today_price` float(10,2) DEFAULT NULL COMMENT '今天收盘价',
  `last_price` float(10,2) DEFAULT NULL COMMENT '昨天收盘价',
  `limit_up` float(10,2) DEFAULT NULL COMMENT '涨停价',
  `limit_down` float(10,2) DEFAULT NULL COMMENT '跌停价',
  `trade_date` char(10) DEFAULT NULL COMMENT '交易日期(yyyy-MM-dd)',
  `trade_num` varchar(50) DEFAULT NULL COMMENT '成交量',
  `trade_amount` varchar(50) DEFAULT NULL COMMENT '成交额',
  `in_trade` varchar(50) DEFAULT NULL COMMENT '内盘(卖家以买家的买入价而卖出成交，成交价为申买价，说明抛盘比较踊跃)',
  `out_trade` varchar(50) DEFAULT NULL COMMENT '外盘(买家以卖家的卖出价而买入成交，成交价为申卖价，说明买盘比较积极)',
  `trade_scale` varchar(20) DEFAULT NULL COMMENT '委比(委比=（委买手数－委卖手数）／（委买手数＋委卖手数）×100％，委比同股票价格正相关)',
  `volume_scale` varchar(20) DEFAULT NULL COMMENT '量比(量比=现成交总手/((过去5个交易日平均每分钟成交量)×当日累计开市时间(分)))',
  `market_value` varchar(50) DEFAULT NULL COMMENT '流通市值',
  `total_value` varchar(50) DEFAULT NULL COMMENT '总市值',
  `pe` double(10,2) DEFAULT NULL COMMENT '市盈率MRQ(每股市价除以每股盈利(Earnings Per Share,EPS))',
  `pb` float(10,2) DEFAULT NULL COMMENT '市净率(每股股价与每股净资产的比率)',
  `eps` double(10,2) DEFAULT NULL COMMENT '每股收益(又称每股税后利润、每股盈余，指税后利润与股本总数的比率)',
  `bps` float(10,2) DEFAULT NULL COMMENT '每股净资产(每股帐面价值，股东权益 / 总股数)',
  `market_equity` varchar(50) DEFAULT NULL COMMENT '流通股本',
  `total_equity` varchar(50) DEFAULT NULL COMMENT '总股票',
  `industry_part` varchar(100) DEFAULT NULL COMMENT '所属行业',
  `attention_rate` int(11) DEFAULT NULL COMMENT '关注度(多少人关注该股票)',
  `create_date` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `IDX_SC` (`stock_type`,`stock_code`,`today_price`,`pe`,`industry_part`,`attention_rate`,`trade_date`,`create_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='股票日数据记录表';

-- 正在导出表  shinycenter.stock_info 的数据：~0 rows (大约)
DELETE FROM `stock_info`;
/*!40000 ALTER TABLE `stock_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `stock_info` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
