# -*- coding: utf-8 -*-

from spider_server import app, config

if __name__ == '__main__':
    # 启动服务
    app.run(host=config.SERVER_HOST, port=config.SERVER_PORT, debug=config.SERVER_DEBUG)
