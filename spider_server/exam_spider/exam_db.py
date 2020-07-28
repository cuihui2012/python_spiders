# -*- coding: utf-8 -*-

import pymysql
from spider_server.db import db_mysql
from spider_server.logs.logger import Logger

logger = Logger(__name__).get_log()


class ExamDB(db_mysql.DBMysql):
    """继承DBMysql类,可直接使用with语法"""

    def save_exam_data(self, data):
        """保存考试通知数据

        :param data:
        :return:
        """
        with ExamDB() as db:
            # SQL 插入语句
            sql = """
                    INSERT INTO `tb_rensheting_exam` (
                          `notice_name`,
                          `notice_time`,
                          `notice_url`
                        ) 
                        VALUES
                          (
                            '{}',
                            '{}',
                            '{}'
                          )
                    """.format(data["notice_name"], data["notice_time"], data["notice_url"])
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

    def get_exam_count(self, notice_name):
        """查询考试数据是否存在

        :param notice_name:
        :return:
        """
        with ExamDB() as db:
            sql = "SELECT COUNT(1) count FROM tb_rensheting_exam WHERE notice_name = '{}'".format(notice_name)
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            result = db.fetchone()
            return result["count"]

    def get_exam_lists(self, name):
        with ExamDB() as db:
            name_param = "" if name == "" else " and notice_name like '%%%s%%'" % name
            sql = """
                  SELECT 
                      notice_name,
                      notice_time,
                      notice_url
                    FROM
                      tb_rensheting_exam 
                    WHERE 1 = 1 {}
                    ORDER BY notice_time DESC
                  """.format(name_param)
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 获取所有记录列表
            results = db.fetchall()
            return results
