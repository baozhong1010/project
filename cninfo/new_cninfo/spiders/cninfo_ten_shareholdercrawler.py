#!/usr/bin/python
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 20180828
# @Author  : dujianye
import scrapy
from scrapy import Request
from new_cninfo.items import *
from new_cninfo.spiders import stock_code
class Cninfo_shareholders_Spider(scrapy.Spider):
    '''
    十大股东
    '''
    name = 'cninfo_shareholders'

    def start_requests(self):
        code_list = stock_code.StockCode().stock_code_fetchall()  # 数据库入口:股票代码:元组
        tag_list = ['shareholders','circulateshareholders']
        for code in code_list:
            for tag in tag_list:
                base_url = f'http://www.cninfo.com.cn/information/{tag}/{code[0]}.html'
                yield Request(base_url,callback=self.parse,meta={'abb_name':code[2],'stock_code':code[0]})
    def parse(self, response):
        items = cninfo_ten_shareholder()
        items['stock_code'] = response.meta['stock_code']
        items['stock_abb_name'] = response.meta['abb_name']
        deadline_data = ''
        for i in response.xpath('/html/body/div/div[1]/div/table/tr'):
            if i.xpath('./td/text()').extract()[0].strip().isdigit():
                items['shareholder_name'] = i.xpath('./td/text()').extract()[1].strip()
                items['number_of_share_held'] = i.xpath('./td/text()').extract()[2].strip()
                items['shareholding_ratio'] = i.xpath('./td/text()').extract()[3].strip()
                items['nature_of_share'] = i.xpath('./td/text()').extract()[4].strip()
                deadline_data = i.xpath('./td/text()').extract()[0].strip()
                items['deadline'] = deadline_data
            else:
                items['shareholder_name'] = i.xpath('./td/text()').extract()[0].strip()
                items['number_of_share_held'] = i.xpath('./td/text()').extract()[1].strip()
                items['shareholding_ratio'] = i.xpath('./td/text()').extract()[2].strip()
                items['nature_of_share'] = i.xpath('./td/text()').extract()[3].strip()
            if '截止时间' in i.xpath('./td/text()').extract()[0].strip():
                continue
            yield items