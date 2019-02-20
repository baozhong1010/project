import json
import random
import threading

import requests
from SpiderMan import SpiderMan
import pymysql


#浙江法院公开网
# url = 'http://www.zjsfgkw.cn/TrialProcess/TrialProcessSearch'

order_nbr = '5fe6cf97-5592-11e7-be16-f45c89a63279'
crawler = SpiderMan(order_nbr, keep_session=True)

conn = pymysql.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                       db='court_notice', charset='utf8')
cursor = conn.cursor()
def get_html(url,data):
    headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
           {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
    try:
        response = crawler.post(url=url,data=data,headers=headers[random.randint(0,2)])
        return response.text
    except Exception,e:
        print e


def get_detail(page,sql1,sql2):
    url = 'http://www.zjsfgkw.cn/TrialProcess/TrialProcessSearchList'
    data = {
        'PageNo': page,
        'PageSize': 5,
        'AH_NH': 2018,
    }
    html = get_html(url=url, data=data)
    j = json.loads(html)
    flag = j['informationmodels']
    if flag:
        for info in flag:
            AnHao = info['AH']
            FaYuan = info['CourtName']
            LiAn_RQ = info['LARQ']
            AnJian_ZT = info['AJZT']
            DangShiRen_contents = info['DSRModels']
            DangShiRen = []
            for content in DangShiRen_contents:
                DangShiRen.append(content['SSDW'] + ':')    #身份
                DangShiRen.append(content['MC'] + ' ')      #名字
                save_to_sql(sql1, (AnHao,content['MC'],content['SSDW']))
            DangShiRen = ''.join(DangShiRen)
            print AnHao,FaYuan,LiAn_RQ,DangShiRen,AnJian_ZT
            save_to_sql(sql2,(AnHao,FaYuan,LiAn_RQ,DangShiRen,AnJian_ZT))

        return flag
    else:
        print 'The url is no contents'
        return flag

def save_to_sql(sql, params=None):
    try:
        cursor.execute(sql, params)
        conn.commit()
        print 'NEW'
    except:
        print 'OLD'

def do_spider():
    page = 1
    sql1 = "insert ignore into ZJ_fayuan_dangshiren values(%s,%s,%s,now())"
    sql2 = "repalce into ZJ_fayuan values(%s,%s,%s,%s,%s,now())"
    while True:
        print '******* crawler is in page',page,'********'
        flag = get_detail(page,sql1,sql2)
        page += 1
        if not flag:
            break


if __name__ == '__main__':
    do_spider()

