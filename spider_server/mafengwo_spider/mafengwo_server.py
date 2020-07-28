# *-* coding:utf8 *-*

# 需要安装,发送请求用
import requests
# 需要安装,解析数据用
from lxml import etree
# 正则
import re

from spider_server.conf.config_util import ConfigUtil
from spider_server.logs.logger import Logger
from spider_server.mafengwo_spider import mafengwo_db

"""
1 准备URL列表
2 遍历URL,发送请求,获取响应数据
3 解析数据
4 保存数据
"""

logger = Logger(__name__).get_log()


class MaFengWoServer(object):
    def __init__(self, city):
        """初始化数据"""
        self.city = city
        # 准备url模板
        self.url_pattern = ConfigUtil().get("URL", "URL_MFW")
        # 指定请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }

    def run(self):
        """程序入口,核心入口"""
        # 0 如果重复运行,先清空数据
        self.clear_data()
        # 1 准备URL列表
        url_list = self.get_url_list()
        # 2 遍历URL,发送请求,获取响应数据
        for url in url_list:
            # 发送请求,获取响应数据
            page = self.get_page_from_url(url)
            # 3 解析数据
            datas = self.get_datas_from_page(page)
            # 4 保存数据
            self.save_data(datas)

    def get_url_list(self):
        """获取url列表(前20个页面的url)"""
        url_list = []
        for i in range(1, 21):
            url = self.url_pattern.format(self.city, i)
            url_list.append(url)
        logger.info(url_list)
        return url_list

    def get_page_from_url(self, url):
        """根据url,发送请求,获取页面数据"""
        response = requests.get(url, headers=self.headers)
        # 返回响应的字符串数据,二进制需要转为字符串
        return response.content.decode()

    def get_datas_from_page(self, page):
        """解析页面数据"""
        # 页面转换为Element,就可以使用Xpath提取数据了
        element = etree.HTML(page)
        # 获取标签列表
        # xpath返回的是一个列表
        lis = element.xpath("//*[@id='_j_search_result_left']/div/div/ul/li")
        # 遍历列表,提取需要的数据
        data_list = []
        for li in lis:
            item = {}
            # ./ 表示当前路径之下,// 表示获取该节点及其之下所有的文本
            name = "".join(li.xpath("./div/div[2]/h3/a//text()"))
            # 如果标题中没有景点,则过滤
            if name.find("景点") == -1:
                continue
            # 去掉标题中的景点,数据库中插入'进行转义
            item["name"] = name.replace("景点 - ", "").replace("'", "\\'")
            # 提取地址
            item["address"] = li.xpath("./div/div[2]/ul/li[1]/a//text()")[0] if len(
                li.xpath("./div/div[2]/ul/li[1]/a//text()")) > 0 else ""
            # 点评数量
            comments_num = li.xpath("./div/div[2]/ul/li[2]/a//text()")[0]
            # 正则提取数字,蜂评(23)--蜂评\((\d+)\)
            item["comments_num"] = int(re.findall("蜂评\((\d+)\)", comments_num)[0])
            # 游记数量
            travel_notes_num = li.xpath("./div/div[2]/ul/li[3]/a//text()")[0]
            item["travel_notes_num"] = int(re.findall("游记\((\d+)\)", travel_notes_num)[0])
            # 记录当前景点的城市
            item["city"] = self.city
            data_list.append(item)
        return data_list

    def save_data(self, datas):
        """保存数据"""
        mafengwo_db.MaFengWoDB().save_mafengwo_jingdian_data(datas)

    def get_count(self):
        """查看数据是否存在"""
        return mafengwo_db.MaFengWoDB().get_mafengwo_count(self.city)

    def get_data(self):
        """查看数据是否存在"""
        return mafengwo_db.MaFengWoDB().get_mafengwo_data(self.city)

    def clear_data(self):
        """清空数据"""
        mafengwo_db.MaFengWoDB().clear_mafengwo_data(self.city)


if __name__ == '__main__':
    pass
