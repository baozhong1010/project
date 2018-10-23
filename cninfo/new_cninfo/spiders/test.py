#!/usr/bin/python
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 20180828
# @Author  : dujianye
#test

from new_cninfo.spiders import stock_code
import time
import re
from lxml import etree
import requests
from bs4 import BeautifulSoup
import os
import itertools
# File_Path = rf'Z:\cninfo\信息披露\两网公司及退市公司\20180201/'   #本地测试
# adjunctUrl = 'http://www.cninfo.com.cn/finalpage/2018-08-29/1205410886.PDF'
# file_name = adjunctUrl.split('/')[-1]
# r = requests.get(adjunctUrl, stream=True)
# if not os.path.exists(File_Path):
#     os.makedirs(File_Path)
# with open(File_Path + file_name, 'wb') as f:  # 写入本地文件
#     for chunk in r.iter_content(chunk_size=1024):
#         if chunk:  # filter out keep-alive new chunks
#             f.write(chunk)
#             f.flush()
# print(file_name)
# headers = {
#     'Referer': 'http://www.cninfo.com.cn/cninfo-new/announcement/show',
#     'Origin': 'http://www.cninfo.com.cn',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept':'application/json, text/javascript, */*; q=0.01',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'no-cache',
#     'Connection': 'keep-alive',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Host': 'www.cninfo.com.cn',
#     'Pragma': 'no-cache',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest',
# }
# industry = ['农、林、牧、渔业;', '采矿业;', '制造业;', '电力、热力、燃气及水生产和供应业;', '建筑业;', '批发和零售业;'
#     , '交通运输、仓储和邮政业;', '住宿和餐饮业;', '信息传输、软件和信息技术服务业;', '金融业;', '房地产业;'
#     , '租赁和商务服务业;', '租赁和商务服务业;科学研究和技术服务业;', '水利、环境和公共设施管理业;', '居民服务、修理和其他服务业;'
#     , '教育;', '卫生和社会工作;', '文化、体育和娱乐业;', '综合;']
# category = ['category_lsgg_lwts;', 'category_dqgg_lwts;', 'category_zjjg_lwts;', 'category_cxpl_lwts;',
#             'category_scpl_lwts;']
# category1 = ['category_lsgg_gfzr;', 'category_dqgg_gfzr;', 'category_zjjg_gfzr;', 'category_cxpl_gfzr;',
#             'category_scpl_gfzr;']
#
# url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
# for x in itertools.product(industry,category1):
#     data = {
#         'stock': '',
#         'searchkey': '',
#         'plate': '',
#         'category':x[1],
#         'trade': x[0],
#         'column': 'neeq_company',   #区分类型  :2市 或股份转让 #staq_net_delisted  neeq_company
#         'columnTitle': '历史公告查询',
#         'pageNum': '1',
#         'pageSize': '30',
#         'tabName': 'fulltext',
#         'sortName': '',
#         'sortType': '',
#         'limit': '',
#         'showTitle': '',
#         'seDate': ''
#     }
#     res = requests.post(url=url,data=data,headers=headers)
#     print(x)
#     print(res.text)
#     time.sleep(4)

# res = requests.get('http://www.cninfo.com.cn//disclosure/1qreport/stocks/1qr1y/cninfo/000001.js?ver=201809111410')
# res.encoding = 'gbk'
# print(res.text)
# tim = '2018-04-20'
# a = 'http://www.cninfo.com.cn/finalpage/2018-04-20/1204666091.PDF'
# r = requests.get('http://www.cninfo.com.cn/finalpage/2018-04-20/1204666091.PDF',stream=True)
# file_name = a.split('/')[-1]
# File_Path = rf'C:\Users\DJY\PycharmProjects\new_cninfo\new_cninfo\spiders\定期报告\{tim}/'
# if not os.path.exists(File_Path):
#     os.makedirs(File_Path)
# with open(File_Path + file_name, 'wb') as f:
#     for chunk in r.iter_content(chunk_size=1024):
#         if chunk:  # filter out keep-alive new chunks
#             f.write(chunk)
#             f.flush()
# current_dir = os.getcwd()
# path = File_Path + file_name
# print(path)
# soup = BeautifulSoup(res.text,'lxml')
# for i in soup.select('td'):
#     date = i
#
#     print(date)
#     time.sleep(2)
#每次取一个都将拿到的日期作为日期, 如果有新日期,则覆盖旧日期
# data = ''
# sele = etree.HTML(res.text)
# for i in sele.xpath('/html/body/div/div[1]/div/table/tr'):
#     if i.xpath('./td/text()')[0].strip().isdigit():
#         x1 = i.xpath('./td/text()')[1].strip()
#         x2 = i.xpath('./td/text()')[2].strip()
#         x3 = i.xpath('./td/text()')[3].strip()
#         x4 = i.xpath('./td/text()')[4].strip()
#         data = i.xpath('./td/text()')[0].strip()
#         print('yes')
#     else:
#         x1 = i.xpath('./td/text()')[0].strip()
#         x2 = i.xpath('./td/text()')[1].strip()
#         x3 = i.xpath('./td/text()')[2].strip()
#         x4 = i.xpath('./td/text()')[3].strip()
#
#         print('不是')
#     if '截止时间' in i.xpath('./td/text()')[0].strip():
#         continue
#     print(x1, x2, x3, x4,data)
#     time.sleep(1)
#
# if __name__ == '__main__':


# a = 'var szzbAffiches=[["000004","finalpage/2017-04-22/1203359765.PDF","国农科技：广州证券股份有限公司关于公司重大资产出售之2016年度持续督导意见","PDF","253","2017-04-22","2017-04-22 00:00"]];'
# b = 'var szzbAffiches=[["002002","finalpage/2018-03-31/1204557444.PDF","鸿达兴业：华泰联合证券有限责任公司关于公司2017年度保荐工作报告","PDF","309","2018-03-31","2018-03-31 00:00"],["002002","finalpage/2017-12-26/1204254045.PDF","鸿达兴业：华泰联合证券有限责任公司关于公司持续督导期2017年培训情况报告","PDF","229","2017-12-26","2017-12-26 00:00"],["002002","finalpage/2017-12-26/1204254044.PDF","鸿达兴业：华泰联合证券有限责任公司关于公司2017年现场检查报告","PDF","213","2017-12-26","2017-12-26 00:00"],["002002","finalpage/2017-04-28/1203415443.PDF","鸿达兴业：华泰联合证券有限责任公司关于公司2014年非公开发行股票之保荐总结报告书","PDF","200","2017-04-28","2017-04-28 00:00"],["002002","finalpage/2017-04-25/1203378507.PDF","鸿达兴业：华泰联合证券有限责任公司关于公司发行股份购买资产并募集配套资金暨关联交易之2016年度持续督导工作报告暨持续督导总结报告","PDF","597","2017-04-25","2017-04-25 00:00"]];'
# text = re.findall(r'var szzbAffiches=\[(.*)\]',a)
#
# x = eval(text[0])
#
# if type(x) ==list:
#     tuple_text = text
#
# else:
#     tuple_text = eval(text[0])
#
#
# print(eval(tuple_text[0])[1])


