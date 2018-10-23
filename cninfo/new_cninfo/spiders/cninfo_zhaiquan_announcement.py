import datetime
import json
import os
import re
import pymysql
import requests
from new_cninfo.items import *

conn = pymysql.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                       db='cninfo', charset='utf8')
cursor = conn.cursor()
time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

class ZhaiQuan_Spider(scrapy.Spider):
    name = 'cninfo_zhaiquan_announcement'
    start_urls = ['http://www.cninfo.com.cn//disclosure/fulltext/stocks/cninfo/bond/bondlatest1y/{code}.js?ver={query}']
    def start_requests(self):
        query_time = datetime.datetime.now().strftime('%Y%m%d')
        info_part = ['深市企业债' ,'深市可转债' ,'深市公司债' ,'沪市企业债' ,'沪市可转债' ,'沪市公司债']
        sql = "select * from cninfo_bond_list"
        cursor.execute(sql)
        for table in cursor.fetchall():
            data_part = table[4]
            code = table[3]
            for start_url in self.start_urls:
                for part in info_part:
                    if part == data_part:
                        yield scrapy.Request(url=start_url.format(code=code,query=query_time),callback=self.parse_announcement,meta={'code':code,'part':part,})

    def parse_announcement(self, response):
        item = AnnouncementItem()
        code = response.meta['code']
        part = response.meta['part']
        r = requests.get(response.url)
        r.encoding = 'gbk'
        contents = re.findall('var szzbAffiches=\[(.*)\]', r.text)[0]
        content = eval(contents)
        for i in content:
            detail_url = i[1]
            gg_title = i[2]
            gg_id = re.search('/(\d+)\.', detail_url).group(1)
            gg_time = i[-2]
            gg_url = 'http://www.cninfo.com.cn/' + detail_url
            File_Path = rf'E:\cninfo\市场资讯\债券\{part}\{gg_time}/'
            file_name = gg_title + '.PDF'
            r1 = requests.get(gg_url)
            if not os.path.exists(File_Path):
                os.makedirs(File_Path)
            with open(File_Path + file_name, 'wb') as f:  # 写入本地文件
                for chunk in r1.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
            path = File_Path + file_name
            download_base_url = ''
            item['code'] = code     #债券代码
            item['gg_title'] = gg_title     #公告标题
            item['gg_id'] = gg_id       #公告ID
            item['gg_time'] = gg_time   #公告发布时间
            item['gg_url'] = gg_url     #公告链接
            item['file_path'] = path    #公告存储路径
            item['download_base_url'] = download_base_url   #公告下载路径
            yield item