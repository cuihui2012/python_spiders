#!/bin/bash
## 测试代码
##部署项目
cp -rf $PROJ_PATH/python_spiders/* /root/python_spiders/

##重启服务
/root/restart-server.sh -s