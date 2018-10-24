#!/usr/bin/python
# _*_ coding:utf-8 _*_
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

class Cninfo_hk_information_bulletin(scrapy.Spider):

    '''
    信息公告
    '''

    name = 'cninfo_hk_infomation'
    def start_requests(self):
        #http://www.cninfo.com.cn//disclosure/fulltext/stocks/hkmblatest/00003.js?ver=201809111755
        code_list = stock_code.StockCode().stock_code_fetchall()  # 数据库入口:股票代码:元组
        tag_list = ['hkmblatest']
        for code in code_list:
            if code[1] == '香港主板' or code[1] == '香港创业板':
                for tag in tag_list:
                    base_url = f'http://www.cninfo.com.cn//disclosure/fulltext/stocks/{tag}/{code[0]}.js?ver=201809111755'
                    yield Request(base_url,callback=self.parse,meta={'abb_name':code[2],'stock_code':code[0],'part':code[1]})


    def parse(self, response):
        res = requests.get(response.url)  #重新请求，解决乱码问题
        item = cninfo_hk_information_bulletin()
        res.encoding = 'gbk'
        js_text = res.text
        text = re.findall(r'var szzbAffiches=\[(.*)\]', js_text)
        eval_text = eval(text[0])
        if type(eval_text) == list:
            tuple_text = eval(text[0])
            item['stock_code'] = response.meta['stock_code']
            item['stock_abb_name'] = response.meta['abb_name']
            item['title'] = tuple_text[2]
            item['publish_time'] = tuple_text[5]
            item['adjunct_url'] = 'http://www.cninfo.com.cn/' + tuple_text[1]
            download_base_url = 'http://www.cninfo.com.cn/' + tuple_text[1]
            part = response.meta['part']
            File_Path = rf'E:\cninfo\市场资讯\上市公司\{part}\信息概况\{tuple_text[5]}/'  # 生产环境
            # File_Path = rf'Z:\cninfo\市场资讯\上市公司\{part}\信息概况\{tuple_text[5]}/'   #本地测试
            file_name = download_base_url.split('/')[-1]
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
                item['title'] = tuple_text[2]
                item['publish_time'] = tuple_text[5]
                item['adjunct_url'] = 'http://www.cninfo.com.cn/'+tuple_text[1]
                download_base_url = 'http://www.cninfo.com.cn/' + tuple_text[1]
                part = response.meta['part']
                File_Path = rf'E:\cninfo\市场资讯\上市公司\{part}\信息概况\{tuple_text[5]}/'  #生产环境
                # File_Path = rf'Z:\cninfo\市场资讯\上市公司\{part}\信息概况\{tuple_text[5]}/'   #本地测试
                file_name = download_base_url.split('/')[-1]
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