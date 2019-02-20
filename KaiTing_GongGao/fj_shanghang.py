# -*- coding: utf-8 -*-
import re
import time
import MySQLdb
import requests
from bs4 import BeautifulSoup
from SpiderMan import SpiderMan
from concurrent.futures import ThreadPoolExecutor, wait


class Crawler_ShangHang(SpiderMan):
    conn = MySQLdb.connect(host='172.16.0.20', user='zhangxiaogang', passwd='gangxiaozhang',
                       db='court_notice', charset='utf8')
    cursor = conn.cursor()

    def get_html(self,url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.17 Safari/537.36',
        }
        try:
            response = self.get(url=url,headers=headers)
            return response.text
        except Exception,e:
            print e

    def save_to_sql(self,sql,params=None):
        try:
            self.cursor.execute(sql,params)
            self.conn.commit()
            print 'NEW'
        except:
            print 'OLD'

    def get_total_number(self):
        url = 'http://lyshfy.chinacourt.org/article/index/id/MzRLNjBINDAwNCACAAA/page/1.shtml'
        html = self.get_html(url=url)
        soup = BeautifulSoup(html,'html5lib')
        info = soup.find_all('div',class_='paginationControl')[0]
        for number in info.find_all('a'):
            if u'尾页' in number.text:
                num_href = number['href']
                total_num = re.search('/(\d+).',num_href).group(1)
                return int(total_num)

    def parse(self,start_page,end_page):
        url = 'http://lyshfy.chinacourt.org/article/index/id/MzRLNjBINDAwNCACAAA/page/{page}.shtml'
        base_url = 'http://lyshfy.chinacourt.org'
        for page in range(start_page,end_page+1):
            try_times = 0
            while True:
                try:
                    html = self.get_html(url=url.format(page=page))
                    soup = BeautifulSoup(html,'html5lib')
                    info = soup.find_all('div',class_='font14 dian_a')[0]
                    try_times += 1
                    if len(info) < 1 and try_times < 10:
                        continue
                    if len(info) < 1 or try_times >= 10:
                        break
                    print 'crawler is in page',page,'****************'
                    for contents in info.ul.find_all('li'):
                        link = contents.a['href']
                        link = base_url + link
                        detail_html = self.get_html(url=link)
                        detail_soup = BeautifulSoup(detail_html,'html5lib')
                        flag = detail_soup.find_all('div',class_='title')
                        if flag:
                            title = detail_soup.find_all('div',class_='b_title')[0].text.strip()
                            content = detail_soup.find_all('div',class_='text')[0].text.strip()
                            fb_time = detail_soup.find_all('div',class_='sth_a')[0].span.text.strip()
                            fb_time = re.sub(u'发布时间：','',fb_time)
                            sql = "insert into fj_shanghang values (%s,%s,%s,now())"
                            # self.save_to_sql(sql,(title,content,fb_time))
                            # print title,content,fb_time
                            try_times = 0
                        else:
                            continue
                    break
                except Exception as e:
                    print e
                    time.sleep(10)
                    continue

    def run(self):
        start = time.time()
        total_number = self.get_total_number()
        # self.parse(25,total_number)
        pools = ThreadPoolExecutor(max_workers=2)
        futures = []
        futures.append(pools.submit(self.parse,1,2))
        futures.append(pools.submit(self.parse,2,3))
        wait(futures)
        print(time.time()-start)


        # pools.submit(self.parse,40,60)
        # pools.submit(self.parse,60,80)
        # pools.submit(self.parse,80,total_number)


if __name__ == '__main__':
    crawler = Crawler_ShangHang()
    crawler.run()