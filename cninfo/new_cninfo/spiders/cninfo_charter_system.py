#!/usr/bin/python
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 20180828
# @Author  : dujianye

#!/usr/bin/python
#
# @Version : 1.0
# @Time    : 20180828
# @Author  : dujianye

import re
import os
import scrapy
import requests
from scrapy import Request
from new_cninfo.items import *
from new_cninfo.spiders import stock_code


class Cninfo_charter_system_Spider(scrapy.Spider):
    '''
    章程制度
    '''
    name = 'cninfo_charter'

    def start_requests(self):
        #http://www.cninfo.com.cn//disclosure/gzzd/stocks/gzzd1y/000004.js?ver=201809111727
        #http://www.cninfo.com.cn//disclosure/gszc/stocks/gszc1y/cninfo/000004.js?ver=201809111731
        code_list = stock_code.StockCode().stock_code_fetchall()  # 数据库入口:股票代码:元组
        tag_dict = {'gzzd':'gzzd1y','gszc':'gszc1y'}
        for code in code_list:  #遍历股票代码
            for tag_key,tag_value in tag_dict.items():   #遍历字典
                if tag_key == 'gszc':
                    base_url1 = f'http://www.cninfo.com.cn//disclosure/{tag_key}/stocks/{tag_value}/cninfo/{code[0]}.js?ver=201809111727'
                    yield Request(base_url1, callback=self.parse,
                                  meta={'abb_name': code[2], 'stock_code': code[0], 'part': code[1]}, encoding='gbk')
                else:
                    base_url = f'http://www.cninfo.com.cn//disclosure/{tag_key}/stocks/{tag_value}/{code[0]}.js?ver=201809111727'
                    yield Request(base_url,callback=self.parse,meta={'abb_name':code[2],'stock_code':code[0],'part':code[1]},encoding='gbk')

    def parse(self, response):   #解析
        res = requests.get(response.url)  #重新请求，解决乱码问题
        item = cninfo_charter_system()
        res.encoding = 'gbk'
        js_text = res.text
        text = re.findall(r'var szzbAffiches=\[(.*)\]', js_text)
        eval_text = eval(text[0])
        if type(eval_text) == list:
            tuple_text = eval(text[0])
            item['stock_code'] = response.meta['stock_code']
            item['stock_abb_name'] = response.meta['abb_name']
            if 'gszc' in response.url:
                item['type'] = '公司章程'
            elif 'gzzd' in response.url:
                item['type'] = '工作制度'
            item['title'] = tuple_text[2]
            item['publish_time'] = tuple_text[5]
            item['adjunct_url'] = 'http://www.cninfo.com.cn/' + tuple_text[1]
            download_base_url = 'http://www.cninfo.com.cn/' + tuple_text[1]
            part = response.meta['part']
            File_Path = rf'E:\cninfo\市场资讯\上市公司\{part}\章程制度\{tuple_text[5]}/'  # 生产环境
            # File_Path = rf'Z:\cninfo\市场资讯\上市公司\{part}\章程制度\{tuple_text[5]}/'   #本地测试
            file_name = tuple_text[2] + download_base_url.split('/')[-1]
            r = requests.get(download_base_url, stream=True)
            if not os.path.exists(File_Path):
                os.makedirs(File_Path)
            with open(File_Path + file_name, 'wb') as f:  # 写入本地文件
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
            path = File_Path + file_name
            item['path'] = path

            yield item
        else:
            tuple_texts = eval(text[0])
            for tuple_text in tuple_texts:
                item['stock_code'] = response.meta['stock_code']
                item['stock_abb_name'] = response.meta['abb_name']
                if 'gszc' in response.url:
                    item['type'] = '公司章程'
                elif 'gzzd' in response.url:
                    item['type'] = '工作制度'
                item['title'] = tuple_text[2]
                item['publish_time'] = tuple_text[5]
                item['adjunct_url'] = 'http://www.cninfo.com.cn/'+tuple_text[1]
                download_base_url = 'http://www.cninfo.com.cn/' + tuple_text[1]
                part = response.meta['part']
                File_Path = rf'E:\cninfo\市场资讯\上市公司\{part}\章程制度\{tuple_text[5]}/'  #生产环境
                # File_Path = rf'Z:\cninfo\市场资讯\上市公司\{part}\章程制度\{tuple_text[5]}/'   #本地测试
                file_name = tuple_text[2]+download_base_url.split('/')[-1]
                r = requests.get(download_base_url, stream=True)
                if not os.path.exists(File_Path):
                    os.makedirs(File_Path)
                with open(File_Path + file_name, 'wb') as f:  #写入本地文件
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            f.flush()
                path = File_Path+ file_name
                item['path'] = path
                yield item