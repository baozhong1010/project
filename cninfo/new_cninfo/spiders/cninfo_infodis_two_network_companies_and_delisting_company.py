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


class Two_Network_Companies(scrapy.Spider):

    '''
    两网公司及退市公司
    '''

    name = 'two_network_companies'

    def start_requests(self):
        category = ['category_lsgg_lwts;', 'category_dqgg_lwts;', 'category_zjjg_lwts;', 'category_cxpl_lwts;',
                    'category_scpl_lwts;']
        announcement_post_data = stock_code.StockCode().announcement_post_data(category)  # post参数   list:元素为data字典
        tag = 'staq_net_delisted'  # 两网公司及退市公司
        base_url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
        i =1
        for data in announcement_post_data:
            data['column'] = tag
            while 1:
                data['pageNum'] = f'{i}'
                yield FormRequest(url=base_url,formdata=data,callback=self.parse,meta={'data':data})
                i += 1
                if i > 50:
                    break


    def parse(self, response):
        items = cninfo_infodis_two_network_companies_and_delisting_company()
        data1 = json.loads(response.text)
        announcements = data1['announcements']
        for i in announcements:
            title = i['secName']+':'+i['announcementTitle']
            announcementTime = i['announcementTime']
            adjunctUrl = 'http://www.cninfo.com.cn/' + i['adjunctUrl']
            announcementTime /= 1000
            ne_time = time.localtime(announcementTime)
            publish_time = time.strftime("%Y-%m-%d", ne_time)
            File_Path = rf'E:\cninfo\信息披露\两网公司及退市公司\{publish_time}/'  # 生产环境
            # File_Path = rf'Z:\cninfo\信息披露\两网公司及退市公司\{publish_time}/'   #本地测试
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
            category = response.meta['data']['category']
            trade = response.meta['data']['trade']
            items['stock_code'] = i['secCode']  # stock_code
            items['announment_id'] = i['announcementId']
            items['announcement_category'] = category
            items['industry_category'] = trade
            items['publish_time'] = publish_time
            items['adjunct_url'] = adjunctUrl
            items['title'] = title
            items['path'] = path
            yield items
