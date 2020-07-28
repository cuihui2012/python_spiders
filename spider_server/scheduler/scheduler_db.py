# *-* coding:utf8 *-*

import pymysql
from spider_server.db import db_mysql
from spider_server.logs.logger import Logger

logger = Logger(__name__).get_log()


class SchedulerDB(db_mysql.DBMysql):
    """继承DBMysql类,可直接使用with语法"""

    def get_job_lists(self):
        with SchedulerDB() as db:
            sql = """
                  SELECT 
                      `job_id`,
                      `job_name`,
                      `year`,
                      `month`,
                      `day`,
                      `hour`,
                      `minute`,
                      `second`,
                      `is_flag`,
                      `email_notice`,
                      `email_notice_desc`,
                      DATE_FORMAT(create_time, '%Y-%m-%d %T') create_time 
                    FROM
                      tb_scheduler_job
                  """
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 获取所有记录列表
            results = db.fetchall()
            return results

    def get_job_detail(self, jobid):
        """获取任务详情

        :param city:
        :return:
        """
        with SchedulerDB() as db:
            sql = """
                  SELECT 
                      `job_id`,
                      `job_name`,
                      `year`,
                      `month`,
                      `day`,
                      `hour`,
                      `minute`,
                      `second`,
                      `is_flag`,
                      `email_notice`,
                      DATE_FORMAT(create_time, '%Y-%m-%d %T') create_time 
                    FROM
                      tb_scheduler_job
                    WHERE job_id = '{}'
                  """.format(jobid)
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            result = db.fetchone()
            return result

    def update_job_flag(self, jobid, is_flag):
        """修改任务标识

        :param jobid:
        :param is_flag:
        :return:
        """
        with SchedulerDB() as db:
            sql = """
                  UPDATE 
                      tb_scheduler_job 
                    SET
                      is_flag = '{0}' 
                    WHERE job_id = '{1}'
                  """.format(is_flag, jobid)
            try:
                # 执行sql语句
                db.execute(sql)
            except Exception as e:
                # 发生错误时回滚
                logger.error(e)
                self.conn.rollback()

    def update_job_detail(self, job):
        """修改任务明细

        :param job:
        :return:
        """
        with SchedulerDB() as db:
            sql = """
                  UPDATE 
                      tb_scheduler_job 
                    SET
                      job_name = '{}',
                      year = '{}',
                      month = '{}',
                      day = '{}',
                      hour = '{}',
                      minute = '{}',
                      second = '{}',
                      create_time = CURRENT_TIMESTAMP 
                    WHERE job_id = '{}'
                  """.format(job["job_name"], job["year"], job["month"], job["day"], job["hour"], job["minute"],
                             job["second"], job["job_id"])
            try:
                # 执行sql语句
                db.execute(sql)
            except Exception as e:
                # 发生错误时回滚
                logger.error(e)
                self.conn.rollback()

    def update_email_notice(self, jobid, email_notice):
        """修改邮件通知

        :param jobid:
        :param email_notice:
        :return:
        """
        with SchedulerDB() as db:
            sql = """
                  UPDATE 
                      tb_scheduler_job 
                    SET
                      email_notice = '{0}' 
                    WHERE job_id = '{1}'
                  """.format(email_notice, jobid)
            try:
                # 执行sql语句
                db.execute(sql)
            except Exception as e:
                # 发生错误时回滚
                logger.error(e)
                self.conn.rollback()
