# -*- coding: utf-8 -*-

from flask import Response, request
import json
from spider_server import app  # 引入模块中的公共变量-flask对象
from spider_server.logs.logger import Logger
from spider_server.scheduler import scheduler_util, scheduler_server

logger = Logger(__name__).get_log()


# 重启调度器
@app.route('/restart_scheduler')
def restart_scheduler():
    try:
        scheduler_server.SchedulerServer().restart_scheduler()
    except Exception as result:
        # 发生错误时回滚
        logger.error("发生错误 %s" % result)
        return "0"
    return "1"


# 任务列表接口
@app.route('/get_job_lists')
def get_job_lists():
    results = scheduler_server.SchedulerServer().get_job_lists()
    # 返回json格式的数据
    return Response(json.dumps(results))


# 移除/增加一个任务
@app.route('/reverse_job/<jobid>')
def reverse_job(jobid):
    try:
        scheduler_server.SchedulerServer().reverse_job(jobid)
    except Exception as result:
        # 发生错误时回滚
        logger.error("发生错误 %s" % result)
        return "0"
    return "1"


@app.route('/get_scheduler_status')
def get_scheduler_status():
    return str(scheduler_server.SchedulerServer().get_scheduler_status())


@app.route('/update_job_detail', methods=['GET', 'POST'])
def update_job_detail():
    if request.method == 'POST':
        logger.info("post")
        # logger.info(request.form.get("job_id"))
        logger.info(request.json)
        logger.info(type(request.json))
    else:
        logger.info("get")
        logger.info(request.form.get("job_id"))
    try:
        scheduler_server.SchedulerServer().update_job_detail(request.json)
    except Exception as result:
        # 发生错误时回滚
        logger.error("发生错误 %s" % result)
        return "0"
    return "1"


@app.route('/update_email_notice/<jobid>')
def update_email_notice(jobid):
    try:
        scheduler_server.SchedulerServer().update_email_notice(jobid)
    except Exception as result:
        # 发生错误时回滚
        logger.error("发生错误 %s" % result)
        return "0"
    return "1"
