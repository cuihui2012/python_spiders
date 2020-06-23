# *-* coding:utf8 *-*

import pymysql

from spider_server.conf import config


class DBMysql(object):
    def __init__(self, host=config.DB_HOST, port=config.DB_PORT, db=config.DB, user=config.USER, passwd=config.PASSWD,
                 charset=config.CHARSET):
        # 建立连接
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建游标，操作设置为字典类型
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        """with语法,返回的值赋值给as后变量"""
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        """with语法,内容执行完毕后,会执行该方法"""
        # 提交数据库并执行
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()
