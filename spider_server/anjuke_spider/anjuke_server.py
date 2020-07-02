# *-* coding:utf8 *-*

# 需要安装,发送请求用
import requests
# 需要安装,解析数据用
from lxml import etree
# 正则
import re
from spider_server.anjuke_spider import anjuke_db

"""
1 准备URL
2 发送请求,获取响应数据
3 解析数据
4 保存数据
"""


class AnJuKeServer(object):
    def __init__(self):
        """初始化数据"""
        # 准备url
        self.url = "https://xa.xinfang.anjuke.com/lou/chengnan/a1_w1/"
        # 指定请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }

    def run(self):
        """程序入口,核心入口"""
        # 发送请求,获取响应数据
        page = self.get_page_from_url(self.url)
        # 解析数据
        datas = self.get_datas_from_page(page)
        print(datas)
        # 保存数据
        self.save_data(datas)

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
        divs = element.xpath("//*[@id='container']/div[2]/div[1]/div[3]/div")
        # 遍历列表,提取需要的数据
        data_list = []
        for div in divs:
            item = {}
            # ./ 表示当前路径之下,// 表示获取该节点及其之下所有的文本
            name = "".join(div.xpath("./div/a[1]/span//text()"))
            item["name"] = name
            # 提取地址
            address_full = div.xpath("./div/a[2]/span//text()")[0]
            address_full = "".join(address_full.split())
            item["address"] = re.findall("\[(.*)\]", address_full)[0]
            item["address_desc"] = address_full.split("]")[1]
            # 提取户型、面积
            type_area = "".join(div.xpath("./div/a[3]//text()")).strip().replace(" ", "").replace("\n", "").replace(
                "\r", "").replace("\t", "")
            item["type"] = type_area[:type_area.index("建筑面积：")].replace("户型：", "")
            item["area"] = type_area[type_area.index("建筑面积："):].replace("建筑面积：", "")
            # 提取价格
            item["price"] = int(div.xpath("./a[2]/p/span//text()")[0])
            data_list.append(item)
        return data_list

    def save_data(self, datas):
        """保存数据"""
        anjuke_db.AnJuKeDB().save_anjuke_xian_data(datas)

    def get_datas_lists(self):
        """获取房屋列表"""
        return anjuke_db.AnJuKeDB().get_datas_lists()

    def get_datas_details(self, name):
        """获取指定小区最新十条数据"""
        return anjuke_db.AnJuKeDB().get_datas_details(name)


if __name__ == '__main__':
    ms = AnJuKeServer()
    ms.run()
