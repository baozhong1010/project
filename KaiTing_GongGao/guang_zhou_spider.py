# -*- coding: utf-8 -*-
import json
import requests
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import MySQLdb
from SpiderMan import SpiderMan
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#广州法院庭审直播网：http://gz.sifayun.com/review/review?courtId=14&courtParam=true
class Guang_Zhou_Crawler(SpiderMan):
    def __init__(self):
        super(Guang_Zhou_Crawler, self).__init__(keep_session=False)
        self.conn = MySQLdb.connect(host='172.16.0.20', user='zhangxiaogang', passwd='gangxiaozhang',
                           db='court_notice', charset='utf8')
        self.cursor = self.conn.cursor()
    def save_to_sql(self,sql,params=None):
        try:
            self.cursor.execute(sql,params)
            self.conn.commit()
            print 'NEW'
        except:
            print 'OLD'

    def parse(self,areas):
        for area,fayuan in areas.items():
            url = 'http://gz.sifayun.com/review/reviewpage?courtId=14&catalogId=0&day={day}&area={area}&pageNumber={page}'
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.17 Safari/537.36',
                }
            r = self.get(url=url.format(day='99999', area=area, page=1), headers=headers)
            contents = json.loads(r.text)
            pageTotal = contents['data']['page']['pageTotal']
            for page in range(1,int(pageTotal)+1):
                print '************crawler in ', fayuan,'******',page, '**************'
                try_times = 0
                while True:
                    res = self.get(url=url.format(day='99999',area=area,page=page),headers=headers)
                    data = json.loads(res.text)
                    flag = data['data']['reviewListPage']
                    if flag:
                        for info in flag:
                            anyou = info['title']
                            anhao = info['caseNo']
                            dangshiren = []
                            if info['partyList']:
                                for party in info['partyList']:
                                    name = party['name'] + ':'
                                    value = party['value']
                                    dangshiren.append(name + value)
                            dangshiren = ''.join(dangshiren)
                            time = info['startTime']
                            roomName = info['roomName']
                            fating = fayuan + roomName
                            # print anyou,anhao,dangshiren,time,fating
                            # sql = "insert into guang_zhou_new values (%s,%s,%s,%s,%s,now())"
                            # self.save_to_sql(sql,(anyou,anhao,dangshiren,time,fating))
                        if try_times > 10 or flag:
                            break
                    else:
                        try_times += 1
                        continue

    def run(self):
        areas = [{'gz': '广州中院'}, {'gzhlwfy': '广州互联网法院'}, {'yxqfy': '越秀法院'}, {'hzqfy': '海珠法院'},
                 {'lwqfy': '荔湾法院'}, {'thqfy': '天河法院'}, {'byqfy': '白云法院'}, {'hpqfy': '黄埔法院'},
                 {'hdqfy': '花都法院'}, {'pyqfy': '番禺法院'}, {'nsqfy': '南沙法院(自贸区法院)'},
                 {'chqfy':'从化法院'},{'zcqfy':'增城法院'}]
        # areas = [{'gz': '广州中院'}]
        # print areas
        pools = ThreadPoolExecutor(max_workers=13)
        pools.map(self.parse,areas)

        # for area_new in areas:
        #     self.parse(area_new)


if __name__=='__main__':
    crawler = Guang_Zhou_Crawler()
    crawler.run()