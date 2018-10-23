# -*- coding: utf-8 -*-
import datetime
from importlib import reload

import pymysql
from bs4 import BeautifulSoup
from new_cninfo.items import *
import sys
reload(sys)

conn = pymysql.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                       db='cninfo', charset='utf8')
cursor = conn.cursor()
time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

class ZhaiQuan_Spider(scrapy.Spider):
    name = 'cninfo_zhaiquan'
    start_urls = ['http://www.cninfo.com.cn/information/bond/brief/{code}.html',
                  'http://www.cninfo.com.cn/information/bond/memo/{code}.html',
                  ]

    def start_requests(self):
        info_part = ['深市企业债','深市可转债','深市公司债','沪市企业债','沪市可转债','沪市公司债']
        sql = "select * from cninfo_bond_list"
        cursor.execute(sql)
        for table in cursor.fetchall():
            data_part = table[4]
            code = table[3]
            for num, start_url in enumerate(self.start_urls):
                for part in info_part:
                    if part == data_part:
                        if num == 0:
                            yield scrapy.Request(start_url.format(code=code),
                                                 meta={'part': part, 'url': start_url.format(code=code)},
                                                 callback=self.parse_ziliao)
                            yield scrapy.Request(start_url.format(code=code),
                                                 meta={'code': code, 'url': start_url.format(code=code)},
                                                 callback=self.parse_fx_situation)
                        if num == 1:
                            yield scrapy.Request(start_url.format(code=code),
                                                 meta={'code': code, 'url': start_url.format(code=code)},
                                                 callback=self.parse_beiwang)
    def parse_ziliao(self,response):
        item = ZiliaoItem()
        response.coding = 'gbk'
        part = response.meta['part']
        html = BeautifulSoup(response.text,'lxml')
        info_all = html.find_all('div',class_='zx_left')[0]
        nei_rongs = info_all.find_all('div', class_='clear')[0]

        code = nei_rongs.find_all('tr')[0].find_all('td')[1].text.strip()     #债券代码
        bond_abb_name = nei_rongs.find_all('tr')[1].find_all('td')[1].text.strip()    #债券简称
        bond_name = nei_rongs.find_all('tr')[2].find_all('td')[1].text.strip()    #债券全称
        bond_english_name = nei_rongs.find_all('tr')[3].find_all('td')[1].text.strip()   #债券英文全称
        type_of_bond = nei_rongs.find_all('tr')[4].find_all('td')[1].text.strip()    #债券种类
        bond_form = nei_rongs.find_all('tr')[5].find_all('td')[1].text.strip()    #债券形式
        interest_payment_method = nei_rongs.find_all('tr')[6].find_all('td')[1].text.strip()   #付息方式
        value_date = nei_rongs.find_all('tr')[7].find_all('td')[1].text.strip()   #起息日
        expiry_date = nei_rongs.find_all('tr')[8].find_all('td')[1].text.strip()   #到期日
        redemption_date = nei_rongs.find_all('tr')[9].find_all('td')[1].text.strip()   #兑付日
        repayment_period = nei_rongs.find_all('tr')[10].find_all('td')[1].text.strip()  #偿还期限（月）
        interest_date_description = nei_rongs.find_all('tr')[11].find_all('td')[1].text.strip()   #付息日期说明
        date_of_listing = nei_rongs.find_all('tr')[12].find_all('td')[1].text.strip()   #上市日期
        termination_of_listing_date = nei_rongs.find_all('tr')[13].find_all('td')[1].text.strip()   #终止上市日期
        unit_denomination = nei_rongs.find_all('tr')[14].find_all('td')[1].text.strip()    #单位面值（元）
        interest_rate_type = nei_rongs.find_all('tr')[15].find_all('td')[1].text.strip()   #利率类型
        coupon_rate = nei_rongs.find_all('tr')[16].find_all('td')[1].text.strip()   #票面利率（%）
        applicable_date_of_interest_rate_start = nei_rongs.find_all('tr')[17].find_all('td')[1].text.strip()    #利率起始适用日期
        interest_rate_termination_date = nei_rongs.find_all('tr')[18].find_all('td')[1].text.strip()   #利率终止适用日期

        item['code'] = code
        item['bond_abb_name'] = bond_abb_name
        item['part'] = part
        item['bond_name'] = bond_name
        item['bond_english_name'] = bond_english_name
        item['type_of_bond'] = type_of_bond
        item['bond_form'] = bond_form
        item['interest_payment_method'] = interest_payment_method
        item['value_date'] = value_date
        item['expiry_date'] = expiry_date
        item['redemption_date'] = redemption_date
        item['repayment_period'] = repayment_period
        item['interest_date_description'] = interest_date_description
        item['date_of_listing'] = date_of_listing
        item['termination_of_listing_date'] = termination_of_listing_date
        item['unit_denomination'] = unit_denomination
        item['interest_rate_type'] = interest_rate_type
        item['coupon_rate'] = coupon_rate
        item['applicable_date_of_interest_rate_start'] = applicable_date_of_interest_rate_start
        item['interest_rate_termination_date'] = interest_rate_termination_date
        yield item
    def parse_fx_situation(self, response):
        #发行情况部分
        item = FxsituationItem()
        response.coding = 'gbk'
        code = response.meta['code']
        html = BeautifulSoup(response.text, 'lxml')
        info_all = html.find_all('div', class_='zx_left')[0]
        fx_nei_rongs = info_all.find_all('div', class_='clear')[1]
        issue_object = fx_nei_rongs.find_all('tr')[0].find_all('td')[1].text.strip()    #发行对象
        issue_price = fx_nei_rongs.find_all('tr')[1].find_all('td')[1].text.strip()     #发行价格（元）
        exchange_online_issuance_start_date = fx_nei_rongs.find_all('tr')[2].find_all('td')[1].text.strip()     #发行起始日
        exchange_online_end_date = fx_nei_rongs.find_all('tr')[3].find_all('td')[1].text.strip()    #发行终止日
        actual_circulation = fx_nei_rongs.find_all('tr')[4].find_all('td')[1].text.strip()      #实际发行量（万元）
        issuance_method = fx_nei_rongs.find_all('tr')[5].find_all('td')[1].text.strip()      #发行方式

        item['code'] = code
        item['issue_object'] = issue_object
        item['issue_price'] = issue_price
        item['exchange_online_issuance_start_date'] = exchange_online_issuance_start_date
        item['exchange_online_end_date'] = exchange_online_end_date
        item['actual_circulation'] = actual_circulation
        item['issuance_method'] = issuance_method
        yield item

    def parse_beiwang(self,response):
        item = BeiwangItem()
        response.coding = 'gbk'
        code = response.meta['code']
        html = BeautifulSoup(response.text, 'lxml')
        contents = html.find_all('div', class_='zx_list')[0]
        contents = contents.find_all('tr')[1:]
        for content in contents:
            bond_event = content.find_all('td')[0].text.strip()
            bond_time = content.find_all('td')[1].text.strip()
            # print(code, bond_event, bond_time)
            item['code'] = code
            item['bond_event'] = bond_event
            item['bond_time'] = bond_time
            yield item

