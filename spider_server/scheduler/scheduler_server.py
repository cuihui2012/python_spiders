# *-* coding:utf8 *-*
import time

from spider_server.logs.logger import Logger
from spider_server.scheduler import scheduler_db, scheduler_util

logger = Logger(__name__).get_log()


class SchedulerServer(object):

    def restart_scheduler(self):
        """重启调度"""
        state = scheduler_util.SchedulerUtil().get_scheduler_status()
        if state == 1:
            # 停止调度
            scheduler_util.SchedulerUtil().shutdown_scheduler()
        # 强制回收对象,使用del删除对象不能立即回收
        scheduler_util.SchedulerUtil.flush()
        # 调度器中添加任务
        jobs = scheduler_db.SchedulerDB().get_job_lists()
        for job in jobs:
            if job["is_flag"] == "1":
                scheduler_util.SchedulerUtil().add_job(job["job_id"], year=job["year"], month=job["month"],
                                                       day=job["day"], hour=job["hour"], minute=job["minute"],
                                                       second=job["second"])
        # 启动调度
        scheduler_util.SchedulerUtil().start_scheduler()

    def get_job_lists(self):
        """返回任务列表"""
        results = scheduler_db.SchedulerDB().get_job_lists()
        return results

    def reverse_job(self, jobid):
        """移除/新增一个任务"""
        # 获取任务详情
        job_detail = scheduler_db.SchedulerDB().get_job_detail(jobid)
        # 获取调度器状态
        status = scheduler_util.SchedulerUtil().get_scheduler_status()
        # 反转job状态
        is_flag = "1" if job_detail["is_flag"] == "0" else "0"
        # 修改job状态
        scheduler_db.SchedulerDB().update_job_flag(jobid, is_flag)
        if status == 1:
            if is_flag == "1":
                # 增加任务
                scheduler_util.SchedulerUtil().add_job(jobid, year=job_detail["year"], month=job_detail["month"],
                                                       day=job_detail["day"], hour=job_detail["hour"],
                                                       minute=job_detail["minute"],
                                                       second=job_detail["second"])
                # 检查状态
                job = scheduler_util.SchedulerUtil().get_scheduler_job(jobid)
                logger.info("任务 %s 开启成功" % jobid if job is not None else "任务 %s 开启失败" % jobid)
            elif is_flag == "0":
                # 移除任务
                scheduler_util.SchedulerUtil().remove_job(jobid)
                # 检查状态
                job = scheduler_util.SchedulerUtil().get_scheduler_job(jobid)
                logger.info("任务 %s 关闭成功" % jobid if job is None else "任务 %s 关闭失败" % jobid)

    def get_scheduler_status(self):
        return scheduler_util.SchedulerUtil().get_scheduler_status()

    def update_job_detail(self, job):
        scheduler_db.SchedulerDB().update_job_detail(job)

    def update_email_notice(self, jobid):
        job_detail = scheduler_db.SchedulerDB().get_job_detail(jobid)
        if job_detail["email_notice"] == "0":
            raise Exception("禁用状态不可修改")
        elif job_detail["email_notice"] == "1":
            scheduler_db.SchedulerDB().update_email_notice(jobid, "2")
        elif job_detail["email_notice"] == "2":
            scheduler_db.SchedulerDB().update_email_notice(jobid, "1")
