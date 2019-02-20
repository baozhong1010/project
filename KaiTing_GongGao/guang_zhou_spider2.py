#encoding=utf-8
import requests
from bs4 import BeautifulSoup
import MySQLdb
import datetime

conn = MySQLdb.connect(host='172.16.0.20',user='zhangxiaogang',passwd='gangxiaozhang',
                       db='court_notice',charset='utf8')
cursor = conn.cursor()
update_time = datetime.datetime.now().strftime('%Y-%m-%d')

def parse(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.17 Safari/537.36',
    }
    try:
        r = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(r.text,'html5lib')
        contents = soup.find_all('div',class_='hot_case_list2_main')
        judge = soup.find_all('div',id='refreshQuery')[0].ul.li.text.strip()
        for content in contents:
            try:
                an_you = content.find('div',class_='content_right_case_title2').text.strip()
                info = content.find_all('div',class_='index_broadcast_address OverFlow')
                an_hao = info[0].text.strip()
                people = info[1].find_all('div',class_='index_broadcast_address OverFlow')
                dang_shi_ren = ''
                for i in range(len(people)):
                    dang_shi_ren += people[int(i)].text.strip()
                time = info[len(people)+2].text.strip()
                fa_ting = info[len(people)+3].text.strip()
                sql = "insert into guang_zhou_new values (%s,%s,%s,%s,%s,%s)"
                save_to_sql(sql,(an_you,an_hao,dang_shi_ren,time,fa_ting,update_time))
                # print an_you,'\n',an_hao,'\n',dang_shi_ren,'\n',time,'\n',fa_ting
                # print sql
            except Exception, e:
                print e
        return judge
    except Exception,e:
        print e

def save_to_sql(sql,params=None):
    try:
        cursor.execute(sql,params)
        conn.commit()
        print 'NEW'
    except:
        print 'OLD'


def run(day):
    url = 'http://gz.sifayun.com/review/review?courtId=14&catalogId=0&day={_day}&area=null&pageNumber={page}'
    page = 1
    while True:
        print '************crawler in ', page, '**************'
        judge = parse(url.format(page=page,_day=day))
        page += 1
        if judge == u'暂无案件信息':
            break


def main():
    run('99999')#全量
    # run('1')#昨天
    # run('0')#今天

if __name__=='__main__':
    main()