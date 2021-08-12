# *-* coding:utf8 *-*

# 需要安装,发送请求用
import urllib.parse

import requests
# 需要安装,解析数据用
from lxml import etree
# 正则
import re

from spider_server.conf.config_util import ConfigUtil
from spider_server.email_smtp.email_util import EmailSMTP
from spider_server.exam_spider import exam_db
from spider_server.logs.logger import Logger
from spider_server.scheduler.scheduler_db import SchedulerDB

"""
1 准备URL列表
2 遍历URL,发送请求,获取响应数据
3 解析数据
4 保存数据
"""
logger = Logger(__name__).get_log()


class ExamServer(object):
    def __init__(self):
        """初始化数据"""
        # 准备url模板
        self.url = ConfigUtil().get("URL", "URL_EXAM")
        # 指定请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }

    def run(self):
        """程序入口,核心入口"""
        # 1 发送请求,获取响应数据
        page = self.get_page_from_url(self.url)
        # 2 解析数据
        datas = self.get_datas_from_page(page)
        # 3 保存数据
        self.save_data(datas)

    def get_page_from_url(self, url):
        """根据url,发送请求,获取页面数据"""
        response = requests.get(url, headers=self.headers, verify=False)
        # 返回响应的字符串数据,二进制需要转为字符串
        return response.content.decode()

    def get_datas_from_page(self, page):
        """解析页面数据"""
        # 页面转换为Element,就可以使用Xpath提取数据了
        element = etree.HTML(page)
        # 获取标签列表
        # xpath返回的是一个列表
        lis = element.xpath("//*[@id='form1']/ul/li")
        # 遍历列表,提取需要的数据
        data_list = []
        for li in lis:
            item = {}
            # ./ 表示当前路径之下,// 表示获取该节点及其之下所有的文本
            # 通知名称
            item["notice_name"] = li.xpath("./a/span//text()")[0].strip()
            # 通知时间
            item["notice_time"] = li.xpath("./span[2]//text()")[0].strip()
            # 通知url
            new_url = li.xpath("./a/@href")[0]
            item["notice_url"] = urllib.parse.urljoin(self.url, new_url)
            data_list.append(item)
        return data_list

    def save_data(self, datas):
        """保存数据"""
        for data in datas:
            # 查看数据是否已经入库
            count = exam_db.ExamDB().get_exam_count(data["notice_name"])
            if count == 0:
                # 新通知处理
                logger.info("考试通知--->%s" % data["notice_name"])
                # 邮件通知
                job_detail = SchedulerDB().get_job_detail("exam_job")
                if job_detail["email_notice"] == "1":
                    EmailSMTP().send_email("人社厅考试通知", "标题：%s \n 时间：%s \n 链接：%s" % (
                        data["notice_name"], data["notice_time"], data["notice_url"]))
                # 数据入库
                exam_db.ExamDB().save_exam_data(data)

    def get_exam_lists(self, name):
        """返回考试信息列表"""
        results = exam_db.ExamDB().get_exam_lists(name)
        return results


if __name__ == '__main__':
    ExamServer().run()
