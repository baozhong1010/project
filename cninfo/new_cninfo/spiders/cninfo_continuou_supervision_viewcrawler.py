#!/usr/bin/python
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 20180828
# @Author  : dujianye

import requests
import re
import os
import scrapy
from scrapy import Request
from new_cninfo.items import *
from new_cninfo.spiders import stock_code

class Cninfo_continuou_Spider(scrapy.Spider):
    '''
    持续督导意见
    '''
    name = 'cninfo_continuou'

    def start_requests(self):
        #http://www.cninfo.com.cn//disclosure/cxdd/stocks/cwgw/002002.js?ver=201809111612
        #http://www.cninfo.com.cn//disclosure/cxdd/stocks/bjjg/002002.js?ver=201809111612
        code_list = stock_code.StockCode().stock_code_fetchall()  # 数据库入口:股票代码:元组
        tag_dict = ['cwgw','bjjg']
        for code in code_list:  #遍历股票代码
            for tag in tag_dict:   #遍历字典
                # base_url = f'http://www.cninfo.com.cn//disclosure/{tag_key}/stocks/{tag_value}/cninfo/{code[0]}.js?ver=201809111413'
                base_url = f'http://www.cninfo.com.cn//disclosure/cxdd/stocks/{tag}/{code[0]}.js?ver=201809111612'
                yield Request(base_url,callback=self.parse,meta={'abb_name':code[2],'stock_code':code[0],'part':code[1]},encoding='gbk')


    def parse(self, response):
        res = requests.get(response.url)  #重新请求，解决乱码问题
        print(response.url)
        item = cninfo_continuou_supervision_view()
        item['stock_code'] = response.meta['stock_code']
        item['stock_abb_name'] = response.meta['abb_name']
        res.encoding = 'gbk'
        js_text = res.text
        text = re.findall(r'var szzbAffiches=\[(.*)\]', js_text)
        eval_text = eval(text[0])
        if type(eval_text) == list:
            tuple_text = eval(text[0])
            print(tuple_text)
            if 'cwgw' in response.url:
                item['type'] = '财务顾问持续督导意见'
            elif 'bjjg' in response.url:
                item['type'] = '保荐机构持续督导意见'
            item['title'] = tuple_text[2]
            item['publish_time'] = tuple_text[5]
            item['adjunct_url'] = 'http://www.cninfo.com.cn/' + tuple_text[1]
            download_base_url = 'http://www.cninfo.com.cn/' + tuple_text[1]
            part = response.meta['part']
            File_Path = rf'E:\cninfo\市场资讯\上市公司\{part}\持续督导意见\{tuple_text[5]}/'  #生产环境
            # File_Path = rf'Z:\cninfo\市场资讯\上市公司\{part}\持续督导意见\{tuple_text[5]}/'  # 本地测试
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
                if 'cwgw' in response.url:
                    item['type'] = '财务顾问持续督导意见'
                elif 'bjjg' in response.url:
                    item['type'] = '保荐机构持续督导意见'
                item['title'] = tuple_text[2]
                item['publish_time'] = tuple_text[5]
                item['adjunct_url'] = 'http://www.cninfo.com.cn/'+tuple_text[1]
                download_base_url = 'http://www.cninfo.com.cn/' + tuple_text[1]
                part = response.meta['part']
                File_Path = rf'E:\cninfo\市场资讯\上市公司\{part}\持续督导意见\{tuple_text[5]}/'  #生产环境
                # File_Path = rf'Z:\cninfo\市场资讯\上市公司\{part}\持续督导意见\{tuple_text[5]}/'   #本地测试
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