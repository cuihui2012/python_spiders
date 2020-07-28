# *-* coding:utf8 *-*

import pymysql
from spider_server.db import db_mysql
from spider_server.logs.logger import Logger

logger = Logger(__name__).get_log()


class MaFengWoDB(db_mysql.DBMysql):
    """继承DBMysql类,可直接使用with语法"""

    def save_mafengwo_jingdian_data(self, datas):
        """保存马蜂窝数据

        :param datas:
        :return:
        """
        with MaFengWoDB() as db:
            for data in datas:
                # SQL 插入语句
                sql = """
                        INSERT INTO tb_mafengwo_jingdian (
                          name,
                          address,
                          comments_num,
                          travel_notes_num,
                          city
                        ) 
                        VALUES
                          (
                            '{}',
                            '{}',
                            {},
                            {},
                            '{}'
                          )
                        """.format(data["name"], data["address"], data["comments_num"], data["travel_notes_num"],
                                   data["city"])
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

    def clear_mafengwo_data(self, city):
        """清空马蜂窝数据

        :param city:
        :return:
        """
        with MaFengWoDB() as db:
            sql = "DELETE FROM tb_mafengwo_jingdian WHERE city = '{}'".format(city)
            db.execute(sql)

    def get_mafengwo_count(self, city):
        """获取马蜂窝数据总数

        :param city:
        :return:
        """
        with MaFengWoDB() as db:
            sql = "SELECT COUNT(1) count FROM tb_mafengwo_jingdian WHERE city = '{}'".format(city)
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            result = db.fetchone()
            return result["count"]

    def get_mafengwo_data(self, city):
        """获取马蜂窝数据

        :param city:
        :return:
        """
        with MaFengWoDB() as db:
            sql = """
                    SELECT 
                      `tid`,
                      `name`,
                      `address`,
                      `comments_num`,
                      `travel_notes_num`,
                      `city`,
                      DATE_FORMAT(
                        `create_time`,
                        '%Y-%m-%d %H:%i:%s'
                      ) create_time 
                    FROM
                      tb_mafengwo_jingdian 
                    WHERE city = '{}'
                    ORDER BY comments_num DESC LIMIT 10
                  """.format(city)
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 获取所有记录列表
            results = db.fetchall()
            logger.info(results)
            return results
