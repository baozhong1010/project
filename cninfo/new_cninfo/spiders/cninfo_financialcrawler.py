#!/usr/bin/python
# _*_ coding:utf-8 _*_
#
# @Version : 1.0.0
# @Time    : 201800901
# @Author  : dujianye
import scrapy
from scrapy import FormRequest
from new_cninfo.items import *
from new_cninfo.spiders import stock_code
class Cninfo_financial_Spider(scrapy.Spider):
    '''
    财务指标
    '''

    name = 'cninfo_financial'

    def start_requests(self):
        code_list = stock_code.StockCode().stock_code_fetchall()  # 数据库   stock_code,part
        post_data = stock_code.StockCode().post_data()  # post参数   list:元素为data字典
        tag_list = [
            'financialreport',
           'incomestatements',
            'balancesheet',
            'cashflow',
            ]
        for code in code_list:   #000001
            for tag in tag_list:  #balancesheet
                for data in post_data:
                    data['cwzb'] = tag
                    post_base_url = f'http://www.cninfo.com.cn/information/stock/{tag}_.jsp?stockCode={code[0]}'
                    if 'balancesheet' in post_base_url:
                        yield FormRequest(url=post_base_url, formdata=data, callback=self.parse_balancesheet, meta={'data':data,'abb_name':code[2],'stock_code':code[0]})
                    elif 'incomestatements' in post_base_url:
                        yield FormRequest(url=post_base_url, formdata=data, callback=self.parse_incomestatements, meta={'data':data,'abb_name':code[2],'stock_code':code[0]})
                    elif 'cashflow' in post_base_url:
                        yield FormRequest(url=post_base_url, formdata=data, callback=self.parse_cashflow, meta={'data':data,'abb_name':code[2],'stock_code':code[0]})
                    elif 'financialreport' in post_base_url:
                        yield FormRequest(url=post_base_url, formdata=data,callback=self.parse_financialreport, meta={'data':data,'abb_name':code[2],'stock_code':code[0]})

    def parse_balancesheet(self, response):  # 资产负债表
        items = balancesheet()
        items['stock_code'] = response.meta['stock_code']
        items['stock_abb_name'] = response.meta['abb_name']
        items['year'] = response.meta['data']['yyyy']  # 年份
        items['reporting_period'] = response.meta['data']['mm']   # 报告期
        try:
            items['table_content'] = response.xpath(
                '//div[@class="clear"]').extract()[0]
        except:
            items['table_content'] = '<div class="clear">  </div>'
        yield items

    def parse_incomestatements(self, response):  # 利润表

        items = incomestatements()
        items['stock_code'] = response.meta['stock_code']
        items['stock_abb_name'] = response.meta['abb_name']
        items['year'] = response.meta['data']['yyyy']  # 年份
        items['reporting_period'] = response.meta['data']['mm']   # 报告期
        try:
            items['table_content'] = response.xpath(
                '//div[@class="clear"]').extract()[0]
        except:
            items['table_content'] = '<div class="clear">  </div>'
        yield items

    def parse_cashflow(self, response):  # 现金流量表

        items = cashflow()
        items['stock_code'] = response.meta['stock_code']
        items['stock_abb_name'] = response.meta['abb_name']
        items['year'] = response.meta['data']['yyyy']  # 年份
        items['reporting_period'] = response.meta['data']['mm']   # 报告期
        try:
            items['table_content'] = response.xpath(
                '//div[@class="clear"]').extract()[0]
        except:
            items['table_content'] = '<div class="clear">  </div>'
        yield items

    def parse_financialreport(self, response):  # 公司综合能力指标

        items = financialreport()
        items['stock_code'] = response.meta['stock_code']
        items['stock_abb_name'] = response.meta['abb_name']
        items['year'] = response.meta['data']['yyyy']  # 年份
        items['reporting_period'] = response.meta['data']['mm']   # 报告期
        try:
            items['table_content'] = response.xpath(
                '//div[@class="clear"]').extract()[0]
        except:
            items['table_content'] = '<div class="clear">  </div>'
        yield items
