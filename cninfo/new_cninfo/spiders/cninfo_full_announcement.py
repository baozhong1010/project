#!/usr/bin/python
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 20180828
# @Author  : dujianye

import os
import time
import json
import scrapy
import requests
from scrapy import FormRequest
from new_cninfo.items import *
from new_cninfo.spiders import stock_code

class Cninfo_Full_Announcement(scrapy.Spider):

    '''
    公告全文
    '''

    name = 'cninfo_full_announcement'

    def start_requests(self):
        column = ['szse_main', 'szse_sme', 'szse_gem', 'sse']
        code_list = stock_code.StockCode().stock_code_fetchall()  # 数据库入口:股票代码:元组
        for code in code_list:
            stock_code1 = code[0]
            part = code[1]
            if part =='深市主板':
                announcement_post_data = stock_code.StockCode().full_annoucement(stock_code1,list(column[0]))  # post参数   list:元素为data字典
                for data in announcement_post_data:
                    base_url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
                    for i in range(1, 50):
                        try:
                            data['pageNum'] = f'{i}'
                            yield FormRequest(url=base_url, formdata=data, callback=self.parse, meta={'data': data,'part':part})
                        except:
                            time.sleep(0.5)
            elif part =='中小企业板':
                announcement_post_data = stock_code.StockCode().full_annoucement(stock_code1, list(
                    column[1]))  # post参数   list:元素为data字典
                for data in announcement_post_data:
                    base_url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
                    for i in range(1, 50):
                        try:
                            data['pageNum'] = f'{i}'
                            yield FormRequest(url=base_url, formdata=data, callback=self.parse, meta={'data': data,'part':part})
                        except:
                            time.sleep(0.5)
            elif part =='创业板':
                announcement_post_data = stock_code.StockCode().full_annoucement(stock_code1, list(
                    column[2]))  # post参数   list:元素为data字典
                for data in announcement_post_data:
                    base_url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
                    for i in range(1, 50):
                        try:
                            data['pageNum'] = f'{i}'
                            yield FormRequest(url=base_url, formdata=data, callback=self.parse, meta={'data': data,'part':part})
                        except:
                            time.sleep(0.5)
            elif part =='沪市主板':
                announcement_post_data = stock_code.StockCode().full_annoucement(stock_code1, list(
                    column[3]))  # post参数   list:元素为data字典
                for data in announcement_post_data:
                    base_url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
                    for i in range(1, 50):
                        try:
                            data['pageNum'] = f'{i}'
                            yield FormRequest(url=base_url, formdata=data, callback=self.parse, meta={'data': data,'part':part})
                        except:
                            time.sleep(0.5)
    def parse(self, response):
        items = cninfo_full_announcement()
        data1 = json.loads(response.text)
        announcements = data1['announcements']
        for i in announcements:
            part = response.meta['part']
            title = i['secName']+':'+i['announcementTitle']
            announcementTime = i['announcementTime']
            adjunctUrl = 'http://www.cninfo.com.cn/' + i['adjunctUrl']
            announcementTime /= 1000
            ne_time = time.localtime(announcementTime)
            publish_time = time.strftime("%Y-%m-%d", ne_time)
            File_Path = rf'E:\cninfo\市场资讯\上市公司\{part}\公告全文\{publish_time}/'  # 生产环境
            # File_Path = rf'Z:\cninfo\市场资讯\上市公司\深市主板\公告全文\{publish_time}/'   #本地测试
            file_name = adjunctUrl.split('/')[-1]
            r = requests.get(adjunctUrl, stream=True)
            if not os.path.exists(File_Path):
                os.makedirs(File_Path)
            with open(File_Path + file_name, 'wb') as f:  # 写入本地文件
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
            path = File_Path + file_name
            type = response.meta['data']['category']
            items['stock_code'] = i['secCode']  # stock_code
            items['announcement_id'] = i['announcementId']
            items['type'] = type
            items['publish_time'] = publish_time
            items['adjunct_url'] = adjunctUrl
            items['announcement_title'] = title
            items['path'] = path
            yield items


