# *-* coding:utf8 *-*

# 需要安装,发送请求用
import requests
# 需要安装,解析数据用
from lxml import etree
# 正则
import re
from spider_server.zhilian_spider import zhilian_db

"""
1 准备URL列表
2 遍历URL,发送请求,获取响应数据
3 解析数据
4 保存数据
"""


class ZhiLianServer(object):
    def __init__(self):
        """初始化数据"""
        # 准备url模板
        self.url_pattern = "https://sou.zhaopin.com/?p={}&jl=864&kw=java"
        # 指定请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }

    def run(self):
        """程序入口,核心入口"""
        # 0 如果重复运行,先清空数据
        # self.clear_data()
        # 1 准备URL列表
        url_list = self.get_url_list()
        # 2 遍历URL,发送请求,获取响应数据
        for url in url_list:
            # 发送请求,获取响应数据
            page = self.get_page_from_url(url)
            # 3 解析数据
            print(url)
            datas = self.get_datas_from_page(page)
            # 4 保存数据
            # self.save_data(datas)

    def get_url_list(self):
        """获取url列表(前20个页面的url)"""
        url_list = []
        # for i in range(1, 2):
        url = self.url_pattern.format(1)
        url_list.append(url)
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
        test = element.xpath("//*[@class='contentpile']/div[@id='listContent']/div[1]/div/a/div[1]/div[1]/span//text()")
        print("开始")
        print(test)
        print("结束")
        divs = element.xpath("/html/body/div[1]/div[1]/div[4]/div[3]/div[3]/div/div")
        # 遍历列表,提取需要的数据
        data_list = []
        print(len(divs))
        for div in divs:
            print("遍历")
            item = {}
            # ./ 表示当前路径之下,// 表示获取该节点及其之下所有的文本
            # 提取招聘职位
            item["zpzw"] = div.xpath("./div/a/div[1]/div[1]/span//text()")[0]
            # 提取招聘企业
            item["zpqy"] = div.xpath("./div/a/div[1]/div[2]/a//text()")[0]
            # 提取招聘地点
            zpdd = div.xpath("./div/a/div[2]/div[1]/ul/li[1]//text()")[0]
            zpdds = str.split("-")
            if len(zpdds) > 1:
                item["zpdd"] = zpdds[1]
            else:
                item["zpdd"] = "未明确定义"
            # 招聘年限
            item["zpnx"] = div.xpath("./div/a/div[2]/div[1]/ul/li[2]//text()")[0]
            print(item)
            data_list.append(item)
        return data_list

    # def save_data(self, datas):
    #     """保存数据"""
    #     mafengwo_db.MaFengWoDB().save_mafengwo_jingdian_data(datas)
    #
    # def get_count(self):
    #     """查看数据是否存在"""
    #     return mafengwo_db.MaFengWoDB().get_mafengwo_count(self.city)
    #
    # def get_data(self):
    #     """查看数据是否存在"""
    #     return mafengwo_db.MaFengWoDB().get_mafengwo_data(self.city)
    #
    # def clear_data(self):
    #     """清空数据"""
    #     mafengwo_db.MaFengWoDB().clear_mafengwo_data(self.city)


if __name__ == '__main__':
    zhilianserver = ZhiLianServer()
    zhilianserver.run()
    pass
