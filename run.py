#!/usr/bin/python3
# -*- coding: utf-8 -*-

from spider_server import app
from spider_server.conf.config_util import ConfigUtil

if __name__ == '__main__':
    # 启动服务
    app.run(host=ConfigUtil().get("SERVER", "SERVER_HOST"), port=int(ConfigUtil().get("SERVER", "SERVER_PORT")),
            debug=bool(ConfigUtil().get("SERVER", "SERVER_DEBUG")))
