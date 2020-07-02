# *-* coding:utf8 *-*

import pymysql
from spider_server.db import db_mysql


class AnJuKeDB(db_mysql.DBMysql):
    """继承DBMysql类,可直接使用with语法"""

    def save_anjuke_xian_data(self, datas):
        """保存安居客数据

        :param datas:
        :return:
        """
        with AnJuKeDB() as db:
            for data in datas:
                # SQL 插入语句
                sql = """
                        INSERT INTO tb_anjuke_xian (
                          name,
                          address,
                          address_desc,
                          type,
                          area,
                          price
                        ) 
                        VALUES
                          (
                            '{}',
                            '{}',
                            '{}',
                            '{}',
                            '{}',
                            {}
                          )
                        """.format(data["name"], data["address"], data["address_desc"], data["type"],
                                   data["area"], data["price"])
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
        with AnJuKeDB() as db:
            sql = "SELECT DISTINCT NAME FROM tb_anjuke_xian"
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 获取所有记录列表
            results = db.fetchall()
            list = []
            for result in results:
                list.append(result["NAME"])
            print(list)
            return list

    def get_datas_details(self, name):
        with AnJuKeDB() as db:
            sql = """
                    SELECT 
                      tid,
                      name,
                      address,
                      address_desc,
                      type,
                      area,
                      price,
                      DATE_FORMAT(create_time, '%Y-%m-%d %T') create_time 
                    FROM
                      tb_anjuke_xian 
                    WHERE NAME = '{}' 
                      ORDER BY create_time LIMIT 10
                  """.format(name)
            # 使用 execute()  方法执行 SQL 查询
            db.execute(sql)
            # 获取所有记录列表
            results = db.fetchall()
            print(results)
            return results
