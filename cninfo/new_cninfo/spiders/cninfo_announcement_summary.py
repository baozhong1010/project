#!/usr/bin/python
# _*_ coding:utf-8 _*_
#

import re
import os
import json
import scrapy
import requests
from scrapy import Request
from new_cninfo.items import *
from new_cninfo.spiders import stock_code


class Cninfo_periodic_Spider(scrapy.Spider):
    '''
    公告摘要
    '''
    name = 'cninfo_announcement_summary'

    def start_requests(self):
        code_list = stock_code.StockCode().stock_code_fetchall()  # 数据库入口:股票代码:元组

        for code in code_list:  #遍历股票代码
            base_url = f'http://www.cninfo.com.cn//disclosure/summary/stocks/summary1y/cninfo/{code[0]}.js?ver=201809291501'
            yield Request(base_url,callback=self.parse,meta={'abb_name':code[2],'stock_code':code[0],'part':code[1]},encoding='gbk')

    def parse(self, response):   #解析
        res = requests.get(response.url)  #重新请求，解决乱码问题
        item = cninfo_announcement_summary()
        res.encoding = 'gbk'
        js_text = res.text
        text = re.findall(r'var szzbAffiches=\[(.*)\]', js_text)
        eval_text = eval(text[0])
        if type(eval_text) == list:
            tuple_text = eval(text[0])
            item['stock_code'] = response.meta['stock_code']
            item['announcement_title'] = tuple_text[2]
            item['publish_time'] = tuple_text[5]
            url = 'http://www.cninfo.com.cn/' + re.findall(r'=(.*)',tuple_text[1])[0].replace('%2F','/')
            js_content = requests.get(url)
            text = re.findall(r'var affiches=\[(.*)\]', js_content.text)
            eval_text = json.loads(text[0])
            item['content'] = f"{eval_text['Zw']}"
            yield item
        else:
            tuple_texts = eval(text[0])
            for tuple_text in tuple_texts:
                item['stock_code'] = response.meta['stock_code']
                item['announcement_title'] = tuple_text[2]
                item['publish_time'] = tuple_text[5]
                url = 'http://www.cninfo.com.cn/' + re.findall(r'=(.*)', tuple_text[1])[0].replace('%2F','/')
                js_content = requests.get(url)
                text = re.findall(r'var affiches=\[(.*)\]', js_content.text)
                eval_text = json.loads(text[0])
                item['content'] = f"{eval_text['Zw']}"
                yield item