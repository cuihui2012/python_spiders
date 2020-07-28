# -*- coding: utf-8 -*-

from flask import Response, request
import json
from spider_server import app  # 引入模块中的公共变量-flask对象
from spider_server.exam_spider import exam_server
from spider_server.logs.logger import Logger

logger = Logger(__name__).get_log()


# 考试信息列表接口
@app.route('/get_exam_lists', methods=['GET'])
def get_exam_lists():
    name = request.args.get("name")
    logger.info(name)
    results = exam_server.ExamServer().get_exam_lists(name)
    # 返回json格式的数据
    return Response(json.dumps(results))
