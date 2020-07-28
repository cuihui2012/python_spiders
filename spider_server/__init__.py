# -*- coding: utf-8 -*-

from flask import Flask

# 创建Flask对象
app = Flask(__name__)

# 需要导入路由模块,否则路由不生效
from spider_server.mafengwo_spider import mafengwo_view
from spider_server.anjuke_spider import anjuke_view
from spider_server.scheduler import scheduler_view
from spider_server.exam_spider import exam_view
from spider_server.zhaopin_spider import zhaopin_view
