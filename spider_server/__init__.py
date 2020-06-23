# -*- coding: utf-8 -*-

from flask import Flask

from .conf import config

# 创建Flask对象
app = Flask(__name__)

# 需要导入路由模块,否则路由不生效
from spider_server.mafengwo_spider import mafengwo_view
