# *-* coding:utf8 *-*

import pymysql
from spider_server.db import db_mysql


class ZhiLianDB(db_mysql.DBMysql):
    """继承DBMysql类,可直接使用with语法"""

    def save_zhilian_lanzhou_data(self, datas):
        """保存智联数据

        :param datas:
        :return:
        """
        with ZhiLianDB() as db:
            for data in datas:
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
                          `xzmin`,
                          `xzmax`
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
                            {},
                            {}
                          )
                        """.format(data["zpzw"], data["zpqy"], data["zpdd"], data["zpnx"],
                                   data["zpxl"], data["qyxz"], data["qygm"], data["xzmin"], data["xzmax"])
                try:
                    # 执行sql语句
                    db.execute(sql)
                except Exception as result:
                    # 发生错误时回滚
                    print("发生错误 %s" % result)
                    print(sql)
                    # 数据库自动提交需要设置为off
                    # SHOW VARIABLES LIKE 'autocommit';
                    # SET autocommit = 0;
                    self.conn.rollback()

    def get_datas_lists(self):
        with ZhiLianDB() as db:
            sql = "SELECT DISTINCT ZPDD FROM TB_ZHAOPIN_LANZHOU"
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 获取所有记录列表
            results = db.fetchall()
            list = []
            for result in results:
                list.append(result["ZPDD"])
            print(list)
            return list

    def get_datas_details(self, zpdd):
        with ZhiLianDB() as db:
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
                      `xzmin`,
                      `xzmax`,
                      DATE_FORMAT(create_time, '%Y-%m-%d %T') `create_time` 
                    FROM
                      tb_zhaopin_lanzhou 
                    WHERE zpdd = '{}' 
                  """.format(zpdd)
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 获取所有记录列表
            results = db.fetchall()
            print(results)
            return results
