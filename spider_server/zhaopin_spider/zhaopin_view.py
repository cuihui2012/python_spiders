# -*- coding: utf-8 -*-

from flask import Response, request
import json
from spider_server import app  # 引入模块中的公共变量-flask对象
from spider_server.zhaopin_spider import zhaopin_server


# 任务列表接口
@app.route('/get_employ_lists', methods=['GET'])
def get_employ_lists():
    param = {
        "page": request.args.get("page"),
        "size": request.args.get("size"),
        "zpzw": request.args.get("zpzw"),
        "zpqy": request.args.get("zpqy"),
        "order": request.args.get("order")
    }
    results = zhaopin_server.ZhaopinServer().get_employ_lists(param)
    # 返回json格式的数据
    return Response(json.dumps(results))
