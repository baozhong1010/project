#!/usr/bin/python
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 20180828
# @Author  : dujianye
#
import datetime
import time

import pymysql
import itertools

class StockCode(object):
    '''
    读取入口数据表
    cninfo_listed_company
    返回
    stock_code,part  字段
    '''
    def __init__(self):
        self.conn = pymysql.connect(
            host='172.16.0.20',
            user='zhangxiaogang',
            passwd='gangxiaozhang',
            db='cninfo',
            charset='utf8')
        self.cor = self.conn.cursor()

    def stock_code_fetchall(self):
        sql = 'select stock_code,part,abb_name from cninfo_listed_company'
        self.cor.execute(sql)
        fetchall = self.cor.fetchall()
        return fetchall

    def post_data(self):  #财务指标 data 数据构造
        data_list = []
        for yyyy in range(2016, 2019):
            for mm in ['-03-31', '-06-30', '-09-30', '-12-31']:

                data = {
                    'yyyy': f'{yyyy}',  # 2016 2017 2018
                    'mm': f'{mm}',  # -03-31, -06-30 -09-30 -12-31
                    'cwzb': '',
                    'button2': '(unable to decode value)'
                }
                data_list.append(data)
        return data_list

    def announcement_post_data(self,category):
        data_list = []
        industry = ['农、林、牧、渔业;','采矿业;','制造业;','电力、热力、燃气及水生产和供应业;','建筑业;','批发和零售业;'
                    ,'交通运输、仓储和邮政业;','住宿和餐饮业;','信息传输、软件和信息技术服务业;','金融业;','房地产业;'
                    ,'租赁和商务服务业;','租赁和商务服务业;科学研究和技术服务业;','水利、环境和公共设施管理业;','居民服务、修理和其他服务业;'
                    ,'教育;','卫生和社会工作;','文化、体育和娱乐业;','综合;']
        t = time.time()
        yesterday_time = int(int(t) - 3600*24)
        yesterday_time_local = time.localtime(yesterday_time)
        # yesterday = time.strftime("%Y-%m-%d", yesterday_time_local)
        yesterday = [str(datetime.date.today() - datetime.timedelta(days=i)) for i in range(1,200)]
        for x in itertools.product(industry, category,yesterday):
            data = {
                'stock': '',
                'searchkey': '',
                'plate': '',
                'category': x[1],
                'trade': x[0],
                'column': '',  # 区分类型  :2市 或股份转让
                'columnTitle': '历史公告查询',
                'pageNum': '',
                'pageSize': '30',
                'tabName': 'fulltext',
                'sortName': '',
                'sortType': '',
                'limit': '',
                'showTitle': '',
                'seDate': x[2]
            }
            data_list.append(data)
        return data_list

    def full_annoucement(self,stock_code1,column):
        data_list = []
        category1 = ['category_ndbg_szsh','category_bndbg_szsh','category_yjdbg_szsh','category_sjdbg_szsh','category_scgkfx_szsh',
                   'category_pg_szsh', 'category_zf_szsh','category_kzhzq_szsh','category_qzxg_szsh','category_qtrz_szsh',
                   'category_qyfpxzcs_szsh', 'category_gqbd_szsh','category_jy_szsh','category_gddh_szsh','category_cqfxyj_szsh',
                   'category_tbclts_szsh', 'category_bcgz_szsh','category_zjjg_szsh','category_ssgszd_szsh','category_zqgg_szsh',
                   'category_qtzdsx_szsh', 'category_tzzgx_szsh','category_dshgg_szsh','category_jshgg_szsh']

        for x in itertools.product(column, category1):
            data = {
                'stock':stock_code1 ,
                'searchkey': '',
                'category': x[1],
                'column': x[0],  # 区分类型  :
                'pageNum': '',
                'pageSize': '30',
                'tabName': 'fulltext',
                'sortName': '',
                'sortType': '',
                'limit': '',
                'seDate': ''
            }

            data_list.append(data)
        return data_list
if __name__ == '__main__':
    # s = StockCode()
    # category = ['category_lsgg_gfzr;', 'category_dqgg_gfzr;', 'category_zjjg_gfzr;', 'category_cxpl_gfzr;',
    #             'category_scpl_gfzr;']  # data内参数
    # s.announcement_post_data(category)
    pass

