#encoding=utf8
import itertools
import re
import requests
from bs4 import BeautifulSoup
from tudi.get_cookie import Get_Cookie
from data_info import *
import MySQLdb


class Result_Announcement(object):

    url = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default'
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

    def post_html(self,url,headers):
        html = self.get_html(url=url, headers=headers)
        soup = BeautifulSoup(html, 'lxml')
        __VIEWSTATE = soup.find('input', id='__VIEWSTATE')["value"]
        __EVENTVALIDATION = soup.find('input', id='__EVENTVALIDATION')["value"]
        for name,id in get_info_xing_zheng_qu():
            print name,id
            data = {
                '__VIEWSTATE': __VIEWSTATE,
                '__EVENTVALIDATION': __EVENTVALIDATION,
                'hidComName': 'default',
                'TAB_QueryConditionItem': '42ad98ae-c46a-40aa-aacc-c0884036eeaf',
                'TAB_QuerySortItemList': '282:False',
                'TAB_QuerySubmitConditionData': u'42ad98ae-c46a-40aa-aacc-c0884036eeaf:{id}▓~{name}'.format(id=id,name=name).encode('gbk'),
                'TAB_QuerySubmitOrderData': '282:False',
                'TAB_RowButtonActionControl': '',
                'TAB_QuerySubmitPagerData': '1',
                'TAB_QuerySubmitSortData': ''
            }
            r1 = requests.post(url=url, headers=headers, data=data)
            if u'没有检索到相关数据' in r1.text:
                print 'no data'
                continue
            page_total = int(re.search(u'共(\d+)页', r1.text).group(1))
            if page_total <= 200:
                for page in range(1,page_total+1):
                    print 'crawler is in page:', page
                    data['TAB_QuerySubmitPagerData'] = page
                    r11 = requests.post(url=url, headers=headers, data=data)
                    r11.encoding = 'gbk'
                    yield r11.text
            else:
                for name2, id2 in get_info_gong_ying_way():
                    print name, id, name2, id2
                    data2 = {
                        '__VIEWSTATE': __VIEWSTATE,
                        '__EVENTVALIDATION': __EVENTVALIDATION,
                        'hidComName': 'default',
                        'TAB_QueryConditionItem': '42ad98ae-c46a-40aa-aacc-c0884036eeaf',
                        'TAB_QueryConditionItem': '8fd0232c-aff0-45d1-a726-63fc4c3d8ea9',
                        'TAB_QuerySortItemList': '282:False',
                        'TAB_QuerySubmitConditionData':
                            u'42ad98ae-c46a-40aa-aacc-c0884036eeaf:{id}▓~{name}|8fd0232c-aff0-45d1-a726-63fc4c3d8ea9:{id2}▓~{name2}'
                                .format(id=id, name=name, id2=id2, name2=name2).encode('gbk'),
                        'TAB_QuerySubmitOrderData': '282:False',
                        'TAB_RowButtonActionControl': '',
                        'TAB_QuerySubmitPagerData': '1',
                        'TAB_QuerySubmitSortData': ''
                    }
                    r2 = requests.post(url=url, headers=headers, data=data2)
                    page_total = int(re.search(u'共(\d+)页', r2.text).group(1))
                    print 'page_total',page_total
                    for page in range(1, page_total + 1):
                        print 'crawler is in page:', page
                        data2['TAB_QuerySubmitPagerData'] = page
                        r22 = requests.post(url=url, headers=headers, data=data2)
                        r22.encoding = 'gbk'
                        yield r22.text

    def parse(self,html,headers):
        try:
            soup = BeautifulSoup(html,'lxml')
            contents = soup.find_all('table',id='TAB_contentTable')[0]
            for content in contents.find_all('tr')[1:]:
                xing_zheng_qu = content.find_all('td')[1].text.strip()
                if '..' in xing_zheng_qu:
                    xing_zheng_qu = content.find_all('td')[1].span['title']
                tudi_location = content.find_all('td')[2].a.text.strip()
                if '..' in tudi_location:
                    tudi_location = content.find_all('td')[2].a.span['title']
                detail_link = content.find_all('td')[2].a['href']
                detail_link = 'http://www.landchina.com/' + detail_link
                detail_content = self.get_html(url=detail_link, headers=headers)
                detail_text = self.parse_detail(detail_content)
                all_mianji = content.find_all('td')[3].text.strip()
                tudi_use = content.find_all('td')[4].text.strip()
                gong_ying_method = content.find_all('td')[5].text.strip()
                qian_ding_riqi = content.find_all('td')[6].text.strip()
                print xing_zheng_qu,tudi_location,all_mianji,tudi_use,gong_ying_method,qian_ding_riqi
                # print detail_text
                # sql = "replace into Result_Announcement values (%s,%s,%s,%s,%s,%s,%s,now())"
                # self.save_to_sql(sql,(xing_zheng_qu,tudi_location,all_mianji,tudi_use,
                #                       gong_ying_method,qian_ding_riqi,detail_text))
        except:
            self.parse(html,headers)

    def parse_detail(self,html):
        soup = BeautifulSoup(html,'lxml')
        contents = soup.find_all('div',id='p1')[0]
        return contents

    def save_to_sql(self,sql, params=None):
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            print 'NEW'
        except:
            print 'OLD'

    def run(self):
        headers = self.update_headers()
        contents = self.post_html(url=self.url,headers=headers)
        for content in contents:
            self.parse(content,headers)



if __name__ == '__main__':
    crawler = Result_Announcement()
    # url = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default'
    # headers = crawler.update_headers()
    # r = requests.get(url=url, headers=headers)
    # print r.text
    crawler.run()