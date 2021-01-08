# python环境基础镜像构建
# Author: cuihui

#alpine-linux版本,主要是小
ARG VERSION=3.7-alpine
FROM python:${VERSION}

# 标签信息
LABEL version="base"
LABEL author="cuihui" email="751670441@qq.com" date="2021-01-08"
LABEL description="python环境基础镜像"

# 修改镜像源,时区设置,删除缓存包
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
   && apk add --no-cache tzdata \
   && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
   && echo 'Asia/Shanghai' > /etc/timezone \
   && rm -rf /var/cache/apk/*.tar.gz

# 拷贝项目代码
COPY python_spiders /home/python_spiders

# 切换工作目录
WORKDIR /home/python_spiders

# python模块lxm需要的基础依赖,安装python模块
RUN apk add --no-cache gcc musl-dev libxslt-dev \
   && rm -rf /var/cache/apk/*.tar.gz \
   && pip3 install --no-cache-dir -r requirements.txt

# 运行项目
CMD [ "python3", "./run.py" ]