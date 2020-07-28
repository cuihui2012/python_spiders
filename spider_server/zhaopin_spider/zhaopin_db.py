# *-* coding:utf8 *-*

import pymysql
from spider_server.db import db_mysql
from spider_server.logs.logger import Logger

logger = Logger(__name__).get_log()


class ZhaopinDB(db_mysql.DBMysql):
    """继承DBMysql类,可直接使用with语法"""

    def save_zhaopin_lanzhou_data(self, data):
        """保存招聘数据

        :param datas:
        :return:
        """
        with ZhaopinDB() as db:
            # SQL 插入语句
            sql = """
                    INSERT INTO `tb_zhaopin_lanzhou` (
                      `zpzw`,
                      `zpqy`,
                      `zpdd`,
                      `zpnx`,
                      `zpxl`,
                      `qyxz`,
                      `qygm`,
                      `zpxz`,
                      `zw_url`,
                      `qy_url`
                    ) 
                    VALUES
                      (
                        '{}',
                        '{}',
                        '{}',
                        '{}',
                        '{}',
                        '{}',
                        '{}',
                        '{}',
                        '{}',
                        '{}'
                      )
                    """.format(data["zpzw"], data["zpqy"], data["zpdd"], data["zpnx"],
                               data["zpxl"], data["qyxz"], data["qygm"], data["zpxz"],
                               data["zw_url"], data["qy_url"])
            try:
                # 执行sql语句
                db.execute(sql)
            except Exception as result:
                # 发生错误时回滚
                logger.error("发生错误 %s" % result)
                logger.error(sql)
                # 数据库自动提交需要设置为off
                # SHOW VARIABLES LIKE 'autocommit';
                # SET autocommit = 0;
                self.conn.rollback()

    def get_employ_lists(self, param):
        with ZhaopinDB() as db:
            zpzw_param = "" if param["zpzw"] == "" else " and zpzw like '%%%s%%'" % param["zpzw"]
            zpqy_param = "" if param["zpqy"] == "" else " and zpqy like '%%%s%%'" % param["zpqy"]
            page = "1" if param["page"] == "" else param["page"]
            size = "10" if param["size"] == "" else param["size"]
            start_int = int(size) * (int(page) - 1)
            size_int = int(size)
            sql = """
                    SELECT 
                      `tid`,
                      `zpzw`,
                      `zpqy`,
                      `zpdd`,
                      `zpnx`,
                      `zpxl`,
                      `qyxz`,
                      `qygm`,
                      `zpxz`,
                      `zw_url`,
                      `qy_url`,
                      DATE_FORMAT(create_time, '%Y-%m-%d %T') `create_time` 
                    FROM
                      tb_zhaopin_lanzhou where 1 = 1 {} {} order by {} limit {},{}
                  """.format(zpzw_param, zpqy_param, param["order"], start_int, size_int)
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 获取所有记录列表
            results = db.fetchall()
            return results

    def get_employ_count(self, param):
        with ZhaopinDB() as db:
            zpzw_param = "" if param["zpzw"] == "" else " and zpzw like '%%%s%%'" % param["zpzw"]
            zpqy_param = "" if param["zpqy"] == "" else " and zpqy like '%%%s%%'" % param["zpqy"]
            sql = """
                    SELECT 
                      count(1) count
                    FROM
                      tb_zhaopin_lanzhou where 1 = 1 {} {}
                  """.format(zpzw_param, zpqy_param)
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 获取首行记录
            result = db.fetchone()
            return result["count"]

    def get_zhaopin_count(self, data):
        """查询招聘数据是否存在

        :param data:
        :return:
        """
        with ZhaopinDB() as db:
            sql = """
                    SELECT 
                      COUNT(1) count
                    FROM
                      tb_zhaopin_lanzhou 
                    WHERE zpzw = '{}' 
                      AND zpqy = '{}' 
                      AND zpdd = '{}' 
                      AND zpnx = '{}' 
                      AND zpxl = '{}' 
                      AND qyxz = '{}' 
                      AND qygm = '{}' 
                      AND zpxz = '{}' 
                      AND zw_url = '{}' 
                      AND qy_url = '{}' 
                  """.format(data["zpzw"],
                             data["zpqy"],
                             data["zpdd"],
                             data["zpnx"],
                             data["zpxl"],
                             data["qyxz"],
                             data["qygm"],
                             data["zpxz"],
                             data["zw_url"],
                             data["qy_url"])
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            result = db.fetchone()
            return result["count"]
