/*
SQLyog Ultimate v12.08 (64 bit)
MySQL - 8.0.1-dmr : Database - spider_data
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`spider_data` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `spider_data`;

/*Table structure for table `tb_anjuke_xian` */

DROP TABLE IF EXISTS `tb_anjuke_xian`;

CREATE TABLE `tb_anjuke_xian` (
  `tid` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `address_desc` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `area` varchar(100) DEFAULT NULL,
  `price` bigint(20) DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;

/*Table structure for table `tb_mafengwo_jingdian` */

DROP TABLE IF EXISTS `tb_mafengwo_jingdian`;

CREATE TABLE `tb_mafengwo_jingdian` (
  `tid` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `comments_num` bigint(20) DEFAULT NULL,
  `travel_notes_num` bigint(20) DEFAULT NULL,
  `city` varchar(10) DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=381 DEFAULT CHARSET=utf8;

/*Table structure for table `tb_zhaopin_lanzhou` */

DROP TABLE IF EXISTS `tb_zhaopin_lanzhou`;

CREATE TABLE `tb_zhaopin_lanzhou` (
  `tid` bigint(20) NOT NULL AUTO_INCREMENT,
  `zpzw` varchar(100) DEFAULT NULL,
  `zpqy` varchar(100) DEFAULT NULL,
  `zpdd` varchar(100) DEFAULT NULL,
  `zpnx` varchar(100) DEFAULT NULL,
  `zpxl` varchar(100) DEFAULT NULL,
  `qyxz` varchar(100) DEFAULT NULL,
  `qygm` varchar(100) DEFAULT NULL,
  `xzmin` bigint(20) DEFAULT NULL,
  `xzmax` bigint(20) DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=360 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
