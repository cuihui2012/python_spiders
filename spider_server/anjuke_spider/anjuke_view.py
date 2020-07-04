# -*- coding: utf-8 -*-

from flask import render_template
from flask import Response
import json
from spider_server import app  # 引入模块中的公共变量-flask对象
from spider_server.anjuke_spider import anjuke_server


# 获取下拉列表数据
@app.route('/get_datas_lists')
def get_datas_lists():
    datas = anjuke_server.AnJuKeServer().get_datas_lists()
    # 返回json格式的数据
    return Response(json.dumps(datas))


# 获取小区列表数据
@app.route('/get_datas_details/<name>')
def get_datas_details(name):
    datas = anjuke_server.AnJuKeServer().get_datas_details(name)
    # 返回json格式的数据
    return Response(json.dumps(datas))


# 获取最新数据
@app.route('/get_new_data')
def get_new_data():
    try:
        anjuke_server.AnJuKeServer().run()
    except Exception as result:
        # 发生错误时回滚
        print("发生错误 %s" % result)
        return "0"
    return "1"
