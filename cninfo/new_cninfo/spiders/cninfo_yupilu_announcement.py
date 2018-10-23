import datetime
import json
import os
import re
import requests
import scrapy
from new_cninfo.items import *

class YupiluAnnouncement(scrapy.Spider):
    name = "cninfo_yupilu_announcement"
    start_urls = [
        'http://www.cninfo.com.cn/cninfo-new/announcement/query'
    ]
    def start_requests(self):
        for page in range(80):
            data = {
                'column': 'pre_disclosure',
                'columnTitle': '历史公告查询',
                'pageNum': page,
                'pageSize': 30,
                'tabName': 'fulltext',
            }
            for start_url in self.start_urls:
                yield scrapy.FormRequest(url=start_url,formdata=data,callback=self.parse)

    def parse(self,response):
        item = Yupilu_AnnouncementItem()
        contents = json.loads(response.text)
        for content in contents['announcements']:
            title = content['announcementTitle']
            announcementId = content['announcementId']
            timeStamp = content['announcementTime']
            timeStamp = re.search('\d{10}', str(timeStamp)).group()
            publish_time = datetime.datetime.utcfromtimestamp(int(timeStamp)).strftime('%Y-%m-%d')
            detail_url = content['adjunctUrl']
            adjunct_url = 'http://www.cninfo.com.cn/' + detail_url
            File_Path = rf'E:\cninfo\信息披露\预披露公告\{publish_time}/'
            file_name = title + '.PDF'
            r1 = requests.get(adjunct_url)
            if not os.path.exists(File_Path):
                os.makedirs(File_Path)
            with open(File_Path + file_name, 'wb') as f:  # 写入本地文件
                for chunk in r1.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
            item['announcement_title'] = title
            item['announcementId'] = announcementId
            item['publish_time'] = publish_time
            item['adjunct_url'] = adjunct_url
            item['file_path'] = File_Path + file_name
            yield item