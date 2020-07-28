# *-* coding:utf8 *-*

# 需要安装,发送请求用
import time
import urllib.parse

import requests
# 需要安装,解析数据用
import requests_html
from lxml import etree

from selenium import webdriver

# 正则
import re

from spider_server.conf.config_util import ConfigUtil
from spider_server.email_smtp.email_util import EmailSMTP
from spider_server.logs.logger import Logger
from spider_server.scheduler.scheduler_db import SchedulerDB
from spider_server.zhaopin_spider import zhaopin_db

"""
1 准备URL列表
2 遍历URL,发送请求,获取响应数据
3 解析数据
4 保存数据
"""
logger = Logger(__name__).get_log()


class ZhaopinServer(object):
    def __init__(self):
        """初始化数据"""
        # 准备url模板
        self.url_pattern = ConfigUtil().get("URL", "URL_EMPLOY")
        # 指定请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }

    def run(self):
        """程序入口,核心入口"""
        # 1 准备URL列表
        url_list = self.get_url_list()
        # 2 遍历URL,发送请求,获取响应数据
        for url in url_list:
            logger.info(url)
            # 防止封ip
            time.sleep(30)
            # 3 发送请求,获取响应数据
            page = self.get_page_from_url(url)
            # 4 解析数据
            datas = self.get_datas_from_page(page)
            # 5 保存数据
            self.save_data(datas)

    def get_url_list(self):
        """获取url列表(前20个页面的url)"""
        url_list = []
        # for i in range(1, 20):
        #     url = self.url_pattern.format(i)
        #     url_list.append(url)
        # 测试用
        url = self.url_pattern.format(1)
        url_list.append(url)
        return url_list

    def get_page_from_url(self, url):
        """根据url,发送请求,获取页面数据"""
        # request抓取页面不全,此处用了chromedriver.exe,需要下载,并放置python根目录
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get(url)
        # 获取源码，解析
        html = driver.page_source
        return html

    def get_datas_from_page(self, page):
        """解析页面数据"""
        # 页面转换为Element,就可以使用Xpath提取数据了
        element = etree.HTML(page)
        # 获取标签列表
        # xpath返回的是一个列表
        lis = element.xpath("//*[@id='main']/div/div[2]/ul/li")
        # 遍历列表,提取需要的数据
        data_list = []
        logger.info(len(lis))
        for li in lis:
            item = {}
            # ./ 表示当前路径之下,// 表示获取该节点及其之下所有的文本
            # 提取招聘职位
            item["zpzw"] = li.xpath("./div/div[1]/div[1]/div/div[1]/span[1]/a//text()")[0]
            # 职位url
            item["zw_url"] = urllib.parse.urljoin(self.url_pattern,
                                                  li.xpath("./div/div[1]/div[1]/div/div[1]/span[1]/a/@href")[0])
            # 提取招聘企业
            item["zpqy"] = li.xpath("./div/div[1]/div[2]/div/h3/a//text()")[0]
            # 企业url
            item["qy_url"] = urllib.parse.urljoin(self.url_pattern,
                                                  li.xpath("./div/div[1]/div[2]/div/h3/a/@href")[0])
            # 提取招聘地点
            item["zpdd"] = li.xpath("./div/div[1]/div[1]/div/div[1]/span[2]/span//text()")[0]
            # 招聘年限
            item["zpnx"] = li.xpath("./div/div[1]/div[1]/div/div[2]/p/text()[1]")[0]
            # 招聘薪资
            item["zpxz"] = li.xpath("./div/div[1]/div[1]/div/div[2]/span/text()")[0]

            # 招聘学历
            item["zpxl"] = li.xpath("./div/div[1]/div[1]/div/div[2]/p/text()[2]")[0]

            if len(li.xpath("./div/div[1]/div[2]/div/p/text()")) == 2:
                # 招聘企业性质
                item["qyxz"] = li.xpath("./div/div[1]/div[2]/div/p/text()[1]")[0]
                # 招聘企业规模
                item["qygm"] = li.xpath("./div/div[1]/div[2]/div/p/text()[2]")[0]
            if len(li.xpath("./div/div[1]/div[2]/div/p/text()")) == 1:
                # 招聘企业性质
                item["qyxz"] = ""
                # 招聘企业规模
                item["qygm"] = li.xpath("./div/div[1]/div[2]/div/p/text()[1]")[0]
            data_list.append(item)
        return data_list

    def save_data(self, datas):
        """保存数据"""
        for data in datas:
            # 查看数据是否已经入库
            count = zhaopin_db.ZhaopinDB().get_zhaopin_count(data)
            if count == 0:
                # 新通知处理
                logger.info("BOSS直聘新发布职位通知--->%s" % data["zpzw"])
                # 邮件通知
                job_detail = SchedulerDB().get_job_detail("employ_job")
                if job_detail["email_notice"] == "1":
                    EmailSMTP().send_email("BOSS直聘新发布职位通知",
                                           "招聘职位：%s \n 招聘年限：%s \n 招聘薪资：%s \n 招聘企业：%s \n 职位链接：%s \n 企业链接：%s" % (
                                               data["zpzw"], data["zpnx"], data["zpxz"],
                                               data["zpqy"], data["zw_url"], data["qy_url"]))
                # 数据入库
                zhaopin_db.ZhaopinDB().save_zhaopin_lanzhou_data(data)

    def get_employ_lists(self, param):
        results = {
            "data": zhaopin_db.ZhaopinDB().get_employ_lists(param),
            "total": zhaopin_db.ZhaopinDB().get_employ_count(param)
        }
        return results


if __name__ == '__main__':
    zhaopinserver = ZhaopinServer()
    zhaopinserver.run()
