# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import pymysql
from new_cninfo.items import *
import re
import time
from new_cninfo.spiders import stock_code
import json
import requests

class CninfocrawlerSpider(scrapy.Spider):
    name = 'cninfocrawler'

    def __init__(self,crawl_mode):

        """

        :param crawl_mode: 最新资料:lastest  公司简介:brief, 发行筹资:issue, 分红dividend,
                            高管人员:management, 股本结构:stockstructure, 配股:allotment

        """
        super(CninfocrawlerSpider, self).__init__()
        self.crawl_mode = crawl_mode
        
    def request(self,url,tag,abb_name,stock_code):    #构造Request函数

        if 'lastest' in tag:
            return Request(url, callback=self.parse_cn_lastest,meta={'abb_name':abb_name,'stock_code':stock_code})  # 最新资料
        elif 'brief' in tag:
            return Request(url, callback=self.parse_cn_brief,meta={'abb_name':abb_name,'stock_code':stock_code})
        elif 'issue' in tag:
            return Request(url, callback=self.parse_cn_issue,meta={'abb_name':abb_name,'stock_code':stock_code})  # 发行筹资
        elif 'dividend' in tag:
            return Request(url, callback=self.parse_cn_dividend,meta={'abb_name':abb_name,'stock_code':stock_code})  # 分红
        elif 'allotment' in tag:
            return Request(url, callback=self.parse_cn_allotment,meta={'abb_name':abb_name,'stock_code':stock_code})  # 配股
        elif 'management' in tag:
            return Request(url, callback=self.parse_cn_management,meta={'abb_name':abb_name,'stock_code':stock_code})  # 高管人员
        elif 'stockstructure' in tag:
            return Request(url, callback=self.parse_cn_stockstructure,meta={'abb_name':abb_name,'stock_code':stock_code})  # 股本结构

    def start_requests(self):

        hk_detail_base_url = 'http://www.cninfo.com.cn/information/hk/mb/brief'  # 香港主板
        #      http://www.cninfo.com.cn/information/hk/mb/brief00034.html
        hk_gem_url = 'http://www.cninfo.com.cn/information/hk/gem/brief'  # 香港中小板
        tag = self.crawl_mode   #页面标签
        code_list = stock_code.StockCode().stock_code_fetchall()  #数据库入口文件
        base_url = f'http://www.cninfo.com.cn/information/{tag}/'
        for code in code_list:
            if '沪市主板' in code:
                shmb_url = base_url + 'shmb' + code[0] + '.html'
                yield self.request(url=shmb_url,tag=tag,abb_name=code[2],stock_code=code[0])
            elif '深市主板' in code:
                szmb_url = base_url + 'szmb' + code[0] + '.html'
                yield self.request(url=szmb_url,tag=tag,abb_name=code[2],stock_code=code[0])

            elif '中小企业板' in code:
                szsme_url = base_url + 'szsme' + code[0] + '.html'
                yield self.request(url=szsme_url, tag=tag,abb_name=code[2],stock_code=code[0])

            elif '创业板' in code:
                szcn_url = base_url + 'szcn' + code[0] + '.html'
                yield self.request(url=szcn_url, tag=tag,abb_name=code[2],stock_code=code[0])

            elif '香港主板' in code:
                yield Request(hk_detail_base_url + code[0] + '.html', callback=self.parse_cn_hk,meta={'stock_code':code[0],'abb_name':code[2]})

            elif '香港创业板' in code and int(code[0]) > 8000:
                yield Request(hk_gem_url + code[0] + '.html', callback=self.parse_cn_hk,meta={'stock_code':code[0],'abb_name':code[2]})

    def parse_cn_brief(self, response):# 内陆企业概况
        items = NewCninfoItem_cn()
        if 'hk' not in response.url:
                items['stock_code'] = response.meta['stock_code']
                items['stock_abb_name'] = response.meta['abb_name']
                for item in response.xpath('//div[@class="clear"]/table'):
                    items['company_name'] = item.xpath(
                        './tr[1]/td[2]/text()').extract()[0].strip()  # 公司全称
                    items['company_english_name'] = item.xpath(
                        './tr[2]/td[2]/text()').extract()[0].strip()  # 英文名称
                    items['registered_address'] = item.xpath(
                        './tr[3]/td[2]/text()').extract()[0].strip()  # 注册地
                    items['company_abb_name'] = item.xpath(
                        './tr[4]/td[2]/text()').extract()[0].strip()  # 公司简称
                    items['legal_person'] = item.xpath(
                        './tr[5]/td[2]/text()').extract()[0].strip()  # 法定代表人
                    items['company_secretary'] = item.xpath(
                        './tr[6]/td[2]/text()').extract()[0].strip()  # 公司董秘
                    items['registered_capital'] = item.xpath(
                        './tr[7]/td[2]/text()').extract()[0].strip()  # 注册资本
                    items['type_of_industry'] = item.xpath(
                        './tr[8]/td[2]/text()').extract()[0].strip()  # 行业种类
                    items['postal_code'] = item.xpath(
                        './tr[9]/td[2]/text()').extract()[0].strip()  # 邮政编码
                    items['company_phone'] = item.xpath(
                        './tr[10]/td[2]/text()').extract()[0].strip()  # 公司电话
                    items['company_fax'] = item.xpath(
                        './tr[11]/td[2]/text()').extract()[0].strip()  # 公司传真
                    items['company_website'] = item.xpath(
                        './tr[12]/td[2]/text()').extract()[0].strip()  # 公司网址
                    items['time_to_market'] = item.xpath(
                        './tr[13]/td[2]/text()').extract()[0].strip()  # 上市时间
                    items['ipo_time'] = item.xpath(
                        './tr[14]/td[2]/text()').extract()[0].strip()  # 招股时间
                    items['issue_number'] = item.xpath(
                        './tr[15]/td[2]/text()').extract()[0].strip()  # 发行数量(万股)
                    items['issue_price'] = item.xpath(
                        './tr[16]/td[2]/text()').extract()[0].strip()  # 发行价格(元)
                    items['earnings_ratio'] = item.xpath(
                        './tr[17]/td[2]/text()').extract()[0].strip()  # 发行市盈率(倍)
                    items['issuance_method'] = item.xpath(
                        './tr[18]/td[2]/text()').extract()[0].strip()  # 发行方式
                    items['lead_underwriter'] = item.xpath(
                        './tr[19]/td[2]/text()').extract()[0].strip()  # 主承销商
                    items['listed_recommender'] = item.xpath(
                        './tr[20]/td[2]/text()').extract()[0].strip()  # 上市推荐人
                    items['sponsor_institution'] = item.xpath(
                        './tr[21]/td[2]/text()').extract()[0].strip()  # 保荐机构
                yield items


    def parse_cn_hk(self, response):  #   香港企业概况
        items = NewCninfoItem_cn_hk()
        items['stock_code'] = response.meta['stock_code']
        items['stock_abb_name'] = response.meta['abb_name']
        if 'hk' in response.url:  # 香港企业
                items['address'] = response.xpath(
                    '//table/tr[3]/td[4]/text()').extract()[0].strip()  # 公司地址
                items['main_business'] = response.xpath(
                    '//table/tr[4]/td[4]/text()').extract()[0].strip()  # 主营业务
                items['chairman'] = response.xpath(
                    '//table/tr[5]/td[4]/text()').extract()[0].strip()  # 主席
                items['category'] = response.xpath(
                    '//table/tr[6]/td[4]/text()').extract()[0].strip()  # 行业分类
                items['place_of_incorporation'] = response.xpath(
                    '//table/tr[7]/td[4]/text()').extract()[0].strip()  # 注册地点
                items['registrar'] = response.xpath(
                    '//table/tr[8]/td[4]/text()').extract()[0].strip()  # 过户处
                items['board_lot'] = response.xpath(
                    '//table/tr[9]/td[4]/text()').extract()[0].strip()  # 买卖单位
                items['issued_share'] = response.xpath(
                    '//table/tr[10]/td[4]/text()').extract()[0].strip()  # 发行股数
                items['market_capitalisation_currency'] = response.xpath(
                    '//table/tr[11]/td[4]/text()').extract()[0].strip()  # 市值货币
                items['market_capitalisation'] = response.xpath(
                    '//table/tr[12]/td[4]/text()').extract()[0].strip()  # 市值
                items['EPS_currency'] = response.xpath(
                    '//table/tr[13]/td[4]/text()').extract()[0].strip()  # 每股盈利货币
                items['earning_per_share'] = response.xpath(
                    '//table/tr[14]/td[4]/text()').extract()[0].strip()  # 每股盈利
                items['EPS_adjusted_indicator'] = response.xpath(
                    '//table/tr[15]/td[4]/text()').extract()[0].strip()  # 每股盈利经调整指示
                items['trading_currency'] = response.xpath(
                    '//table/tr[16]/td[4]/text()').extract()[0].strip()  # 交易货币
                items['listing_date'] = response.xpath(
                    '//table/tr[17]/td[4]/text()').extract()[0].strip()  # 上市日期
                items['net_profit_currency'] = response.xpath(
                    '//table/tr[18]/td[4]/text()').extract()[0].strip()  # 纯利货币
                items['net_profit'] = response.xpath(
                    '//table/tr[19]/td[4]/text()').extract()[0].strip()  # 纯利
                items['net_asset_value'] = response.xpath(
                    '//table/tr[20]/td[4]/text()').extract()[0].strip()  # 资产净值货币
                items['Net_assetvalue'] = response.xpath(
                    '//table/tr[21]/td[4]/text()').extract()[0].strip()  # 资产净值
                items['indicator'] = response.xpath(
                    '//table/tr[22]/td[4]/text()').extract()[0].strip()  # 指示
                yield items


    def parse_cn_lastest(self,response):   #最新资料
        dict_share_status = {}
        dict_financal_ind = {}
        dict_note = {}
        dict_announcement = {}
        dict_share_status['最新股本状况']=response.xpath('/html/body/div[2]/div[1]/div[2]').extract()[0].strip()
        dict_financal_ind['最新财务指标'] =response.xpath('/html/body/div[2]/div[1]/div[4]').extract()[0].strip()
        items = lastest()
        items['stock_code'] = response.meta['stock_code']
        items['stock_abb_name'] = response.meta['abb_name']
        items['latest_share_statu'] = str(dict_share_status)
        items['latest_financial_indicator'] = str(dict_financal_ind)
        memo_url = response.url.replace(response.url.split('/')[4], 'memo')
        res1 = requests.get(memo_url)
        res1.encoding = 'urf-8'
        dict_note['公司备忘'] = res1.text
        items['company_note'] = str(dict_note)
        announcement_url = re.findall(r'(.*)/', response.url)[0] + '/' + ''.join(re.findall(r'\d', response.url.split('/')[-1])) + '.js'
        res = requests.get(announcement_url)
        res.encoding = 'utf-8'
        dict_announcement['最新公司动态'] = re.findall(r'zxgsdt=\[(.*)\]',res.text)[0]
        items['latest_announcement'] = str(dict_announcement)
        yield items
    def parse_cn_issue(self,response): # 发行筹资
        issuance_financing = {}
        prospectu = {}
        listing_announcement = {}
        share_placement_statement = {}
        issuance_financing['发行筹资']=response.xpath('/html/body/div[2]/div[1]/div[2]/table').extract()[0].strip()
        items = issue()
        items['stock_code'] = response.meta['stock_code']
        items['stock_abb_name'] = response.meta['abb_name']
        items['issuance_financing'] = str(issuance_financing)
        #http://www.cninfo.com.cn/information/issue/szmb000002.html
        #http://www.cninfo.com.cn/information/issue/000002.js
        announcement_url = re.findall(r'(.*)/', response.url)[0] + '/' + ''.join(re.findall(r'\d', response.url.split('/')[-1])) + '.js'
        res = requests.get(announcement_url)
        res.encoding = 'utf-8'
        prospectu['招股说明书'] = re.findall(r'zgsmsData=\[(.*?)\]',res.text)[0]
        listing_announcement['上市公告书'] = re.findall(r'ssggsData=\[(.*?)\]', res.text)[0]
        share_placement_statement['配股说明书'] = re.findall(r'pgsmsData=\[(.*?)\]', res.text)[0]
        items['prospectu'] = str(prospectu)
        items['listing_announcement'] = str(listing_announcement)
        items['share_placement_statement'] = str(share_placement_statement)
        yield items

    def parse_cn_dividend(self,response): # 分红
        items = dividend()
        items['stock_code'] = response.meta['stock_code']
        items['stock_abb_name'] = response.meta['abb_name']
        for i in response.xpath('/html/body/div[3]/div[1]/div[2]/table/tr'):
            items['year'] = i.xpath('./td/text()').extract()[0].strip()
            items['dividend_plan'] = i.xpath('./td/text()').extract()[1].strip()
            items['equity_registration_date'] = i.xpath('./td/text()').extract()[2].strip()
            items['dividend_date'] = i.xpath('./td/text()').extract()[3].strip()
            items['red_stock_listing_day'] = i.xpath('./td/text()').extract()[4].strip()
            if items['year'] == '分红年度':
                continue
            yield items

    def parse_cn_allotment(self,response):  # 配股
        items = allotment()
        items['stock_code'] = response.meta['stock_code']
        items['stock_abb_name'] = response.meta['abb_name']
        for i in response.xpath('/html/body/div[3]/div[1]/div[2]/table/tr'):
            items['year'] = i.xpath('./td/text()').extract()[0].strip()
            items['allotment_plan'] = i.xpath('./td/text()').extract()[1].strip()
            items['allotment_price'] = i.xpath('./td/text()').extract()[2].strip()
            items['equity_registration_date'] = i.xpath('./td/text()').extract()[3].strip()
            items['dividend_date'] = i.xpath('./td/text()').extract()[4].strip()
            items['start_end_date_of_issue'] = i.xpath('./td/text()').extract()[5].strip()
            items['part_of_listing_day'] = i.xpath('./td/text()').extract()[6].strip()
            if items['year'] == '配股年度':
                continue
            yield items

    def parse_cn_management(self,response):  # 高管人员
        items = management()
        items['stock_code'] = response.meta['stock_code']
        items['stock_abb_name'] = response.meta['abb_name']
        for i in response.xpath('/html/body/div[2]/div[1]/div[2]/table/tr'):
            items['name'] = i.xpath('./td/text()').extract()[0].strip()
            items['position'] = i.xpath('./td/text()').extract()[1].strip()
            items['birth'] = i.xpath('./td/text()').extract()[2].strip()
            items['gender'] = i.xpath('./td/text()').extract()[3].strip()
            items['education'] = i.xpath('./td/text()').extract()[4].strip()
            if items['name'] == '姓名':
                continue
            yield items

    def parse_cn_stockstructure(self,response):  # 股本结构
        item = stockstructure()
        item['stock_code'] = response.meta['stock_code']
        item['stock_abb_name'] = response.meta['abb_name']
        for i in response.xpath('//div[@class="clear"]/table'):
            for x in range(2,4):
                item['change_date'] = i.xpath(f'./tr[1]/td[{x}]/text()').extract()[0].strip()
                item['reason_for_change'] = i.xpath(f'./tr[2]/td[{x}]/text()').extract()[0].strip()
                item['circulated_share'] = i.xpath(f'./tr[3]/td[{x}]/text()').extract()[0].strip()
                item['rmb_common_stock'] = i.xpath(f'./tr[4]/td[{x}]/text()').extract()[0].strip()
                item['domestically_listed_foreign_share_B'] = i.xpath(f'./tr[5]/td[{x}]/text()').extract()[0].strip()
                item['domestically_listed_foreign_share'] = i.xpath(f'./tr[6]/td[{x}]/text()').extract()[0].strip()
                item['other_outstanding_share'] = i.xpath(f'./tr[7]/td[{x}]/text()').extract()[0].strip()
                item['restricted_share'] = i.xpath(f'./tr[8]/td[{x}]/text()').extract()[0].strip()
                item['state_owned_share'] = i.xpath(f'./tr[9]/td[{x}]/text()').extract()[0].strip()
                item['domestic_share_other_than_state_owned_share'] = i.xpath(f'./tr[10]/td[{x}]/text()').extract()[0].strip()
                item['foreign_shareholding'] = i.xpath(f'./tr[11]/td[{x}]/text()').extract()[0].strip()
                item['placing_legal_person_share'] = i.xpath(f'./tr[12]/td[{x}]/text()').extract()[0].strip()
                item['uncirculated_share'] = i.xpath(f'./tr[13]/td[{x}]/text()').extract()[0].strip()
                item['state_owned_share_1'] = i.xpath(f'./tr[14]/td[{x}]/text()').extract()[0].strip()
                item['domestic_legal_person_holding'] = i.xpath(f'./tr[15]/td[{x}]/text()').extract()[0].strip()
                item['foreign_legal_person_holding_share'] = i.xpath(f'./tr[16]/td[{x}]/text()').extract()[0].strip()
                item['natural_person_holding'] = i.xpath(f'./tr[17]/td[{x}]/text()').extract()[0].strip()
                item['other_undistributed_share'] = i.xpath(f'./tr[18]/td[{x}]/text()').extract()[0].strip()
                item['total_sharecapital'] = i.xpath(f'./tr[19]/td[{x}]/text()').extract()[0].strip()
                yield item