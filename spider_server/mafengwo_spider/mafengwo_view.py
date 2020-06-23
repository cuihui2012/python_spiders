# -*- coding: utf-8 -*-

from flask import render_template
from flask import Response
import json
from spider_server import app  # 引入模块中的公共变量-flask对象
from spider_server.mafengwo_spider import mafengwo_server


@app.route('/')
def view():
    return render_template('index.html')


# 渲染数据的方法
@app.route('/echarts/<city>')
def chars(city):
    # 获取城市的景点数据量
    count = mafengwo_server.MaFengWoServer(city).get_count()

    print(count)
    # 如果没有查到需要的数据, 就开启一个爬虫, 去采集需要的数据
    if not count:
        # 创建指定城市的爬虫, 抓取需要的数据
        mafengwo_server.MaFengWoServer(city).run()

    # 查询数据
    datas = mafengwo_server.MaFengWoServer(city).get_data()
    # 返回json格式的数据
    return Response(json.dumps(datas))
