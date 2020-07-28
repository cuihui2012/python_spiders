# *-* coding:utf8 *-*

import datetime, time
# 阻塞调度
from apscheduler.schedulers.blocking import BlockingScheduler
# 非阻塞调度
from apscheduler.schedulers.background import BackgroundScheduler

from spider_server.anjuke_spider import anjuke_server
from spider_server.exam_spider import exam_server
from spider_server.logs.logger import Logger
from spider_server.mafengwo_spider import mafengwo_server
from spider_server.zhaopin_spider import zhaopin_server

logger = Logger(__name__).get_log()


class SchedulerUtil(object):
    # 类属性：记录实例是否存在
    instance = None

    # 初始化执行标志
    init_flag = False

    # 创建对象,首先会为对象分配空间
    def __new__(cls, *args, **kwargs):
        # 判断类属性是否为空对象
        if cls.instance is None:
            # 调用父类方法,为对象分配空间
            logger.info("SchedulerUtil-->分配空间")
            cls.instance = super().__new__(cls)
        # 返回对象的引用
        return cls.instance

    # 分配空间后,对象属性初始化
    def __init__(self):
        # 判断是否执行过初始化动作
        if SchedulerUtil.init_flag:
            return
        logger.info("SchedulerUtil-->对象属性初始化")
        self.scheduler = BackgroundScheduler()
        SchedulerUtil.init_flag = True

    def __del__(self):
        logger.info("del done!")

    @classmethod
    def flush(cls):
        """强制回收对象"""
        cls.instance = None
        SchedulerUtil.init_flag = False

    def add_job(self, jobid, **kwargs):
        logger.info("添加job----> %s" % jobid)
        self.scheduler.add_job(eval("self.%s" % jobid), 'cron', **kwargs, id=jobid)

    def remove_job(self, jobid):
        logger.info("删除job----> %s" % jobid)
        self.scheduler.remove_job(jobid)

    def start_scheduler(self):
        """启动调度器

        :return:
        """
        logger.info("启动调度器")
        self.scheduler.start()
        logger.info("调度器状态：%s" % self.scheduler.state)

    def shutdown_scheduler(self):
        """停止调度器

        :return:
        """
        logger.info("停止调度器")
        self.scheduler.shutdown(wait=False)

    def get_scheduler_status(self):
        """获取调度器状态

        :return:
        """
        logger.info("获取调度器状态：%s" % self.scheduler.state)
        return self.scheduler.state

    def get_scheduler_job(self, jobid):
        """获取调度中的任务

        :return:
        """
        return self.scheduler.get_job(jobid)

    def get_scheduler_jobs(self):
        """获取调度中的任务列表

        :return:
        """
        return self.scheduler.get_jobs()

    def exam_job(self):
        """考试信息任务

        :return:
        """
        logger.info("exam_job正在执行中...")
        exam_server.ExamServer().run()

    def employ_job(self):
        """招聘信息任务

        :return:
        """
        logger.info("employ_job正在执行中...")
        zhaopin_server.ZhaopinServer().run()

    def anjuke_job(self):
        """安居客数据任务

        :return:
        """
        logger.info("anjuke_job正在执行中...")
        anjuke_server.AnJuKeServer().run()

    def mafengwo_job(self):
        """马蜂窝数据任务（测试任务）

        :return:
        """
        logger.info("mafengwo_job正在执行中...")
        mafengwo_server.MaFengWoServer("西安").run()


if __name__ == '__main__':
    # logger.info("添加一个任务")
    # SchedulerUtil().add_job("job1")
    logger.info("启动调度器")
    SchedulerUtil().start_scheduler()
    # logger.info("删除一个任务")
    # time.sleep(15)
    # SchedulerUtil().remove_job()
