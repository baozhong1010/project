#encoding=utf8
import json
import re
import time

import requests
from bs4 import BeautifulSoup
from tudi.get_cookie import Get_Cookie
import MySQLdb

class Get_ID(object):

    url = 'http://www.landchina.com/ExtendModule/WorkAction/EnumSelectEx.aspx?group=1&n=TAB_queryTblEnumItem_83'
    conn = MySQLdb.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                           db='China_Tudi', charset='utf8')
    cursor = conn.cursor()

    def update_headers(self):
        Cookie = Get_Cookie()
        cookie = Cookie.cookie(self.url)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.17 Safari/537.36',
            'Cookie': str(cookie)
        }
        return headers

    def get_html(self,url,headers):
        r = requests.get(url=url,headers=headers)
        r.encoding = 'gbk'
        return r.text

    def post_html(self,url,headers,data):
        r = requests.post(url=url,headers=headers,data=data)
        r.encoding = 'gbk'
        return r.text

    def parse_level(self,headers,data):
        url = 'http://www.landchina.com/ExtendModule/WorkAction/EnumHandler.ashx'
        try:
            html = self.post_html(url=url, headers=headers, data=data)
            j = json.loads(html)
            return j
        except:
            time.sleep(5)
            self.parse_level(headers,data)

    def save_to_sql(self,sql, params=None):
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            print 'NEW'
        except:
            print 'OLD'

    def parse_level1(self,headers):
        #省
        html = self.get_html(url=self.url,headers=headers)
        content = re.search('var zNodes = \[(.*)\]', html).group(1)
        contents = re.findall('(\{.*?\})',content)
        true = 'true'
        false = 'false'
        for info in contents[2:]:
            # time.sleep(1)
            info = info.encode('utf-8')
            info = eval(info)
            yield info

    def parse_level2(self,headers):
        #市/辖区
        for info in self.parse_level1(headers):
            # time.sleep(1)
            name = info['name']
            group = info['group']
            id = info['value']
            print name,id
            data = {
                'id': id,
                'group': group
            }
            # sql = "replace into xing_zheng_qu_shengji values(%s,%s,%s)"
            # self.save_to_sql(sql,(name,id,group))
            for nei_rong in self.parse_level(headers,data):
                yield nei_rong

    def parse_level3(self,headers):
        #县/区
        for info in self.parse_level2(headers):
            # time.sleep(1)
            id_next = info['value']
            group_next = info['group']
            name_next = info['name']
            data = {
                'id':id_next,
                'group':group_next
            }
            print name_next,id_next
            # sql = "replace into xing_zheng_qu_shiji values(%s,%s,%s)"
            # self.save_to_sql(sql,(name_next,id_next,group_next))
            for nei_rong in self.parse_level(headers,data):
                yield nei_rong

    def get_value(self,headers):
        for info in self.parse_level3(headers):
            try:
                id_next = info['value']
                group_next = info['group']
                name_next = info['name']
                sql = "replace into xing_zheng_qu values(%s,%s,%s)"
                self.save_to_sql(sql,(name_next,id_next,group_next))
                print name_next,id_next,group_next
            except:
                with open('log.txt') as f:
                    f.write(info + '\n')
                continue



if __name__ == '__main__':
    crawler = Get_ID()
    headers = crawler.update_headers()
    crawler.get_value(headers)

