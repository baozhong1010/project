#encoding=utf8
import requests
from bs4 import BeautifulSoup
from tudi.get_cookie import Get_Cookie
import MySQLdb


class Tu_Di_Big_Company(object):

    url = 'http://www.landchina.com/default.aspx?tabid=347&ComName=default'
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

    def post_html(self,url,headers,page):
        html = self.get_html(url=url,headers=headers)
        soup = BeautifulSoup(html,'lxml')
        __VIEWSTATE = soup.find('input', id='__VIEWSTATE')["value"]
        __EVENTVALIDATION = soup.find('input', id='__EVENTVALIDATION')["value"]
        data = {
            '__VIEWSTATE':__VIEWSTATE,
            '__EVENTVALIDATION': __EVENTVALIDATION,
           'hidComName': 'default',
           'TAB_QuerySubmitConditionData': '',
           'TAB_QuerySubmitOrderData': '',
           'TAB_RowButtonActionControl': '',
           'TAB_QuerySubmitPagerData': str(page),
           'TAB_QuerySubmitSortData': '',
        }
        r = requests.post(url=url,headers=headers,data=data)
        r.encoding = 'gbk'
        return r.text

    def parse(self,html,headers):
        soup = BeautifulSoup(html,'lxml')
        contents = soup.find_all('table',id='TAB_contentTable')[0]
        for content in contents.find_all('tr')[1:]:
            xing_zheng_qu = content.find_all('td')[1].text.strip()
            if '..' in xing_zheng_qu:
                xing_zheng_qu = content.find_all('td')[1].span['title']
            dian_zi_jg_number = content.find_all('td')[2].text.strip()
            qian_ding_riqi = content.find_all('td')[3].text.strip()
            shou_rang_ren = content.find_all('td')[4].a.text.strip()
            detail_link = content.find_all('td')[4].a['href']
            detail_link = 'http://www.landchina.com/' + detail_link
            detail_content = self.get_html(url=detail_link,headers=headers)
            detail_text = self.parse_detail(detail_content)
            gong_di_zong_mian_ji = content.find_all('td')[5].text.strip()
            yue_ding_dong_gong_time = content.find_all('td')[6].text.strip()
            print xing_zheng_qu,dian_zi_jg_number,qian_ding_riqi,shou_rang_ren,gong_di_zong_mian_ji,yue_ding_dong_gong_time
            # print detail_text
            # sql = "replace into Big_Company_Buy_Tudi_situation values (%s,%s,%s,%s,%s,%s,%s,now())"
            # self.save_to_sql(sql,(xing_zheng_qu,dian_zi_jg_number,qian_ding_riqi,shou_rang_ren,
            #                       gong_di_zong_mian_ji,yue_ding_dong_gong_time,detail_text))

    def parse_detail(self,html):
        soup = BeautifulSoup(html,'lxml')
        contents = soup.find_all('div',id='p1')[0]
        return contents

    def save_to_sql(self,sql, params=None):
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            print('NEW')
        except:
            print('OLD')

    def run(self):
        headers = self.update_headers()
        for page in range(1,50):
            try:
                print 'crawler is in page:',page
                contents = self.post_html(url=self.url,headers=headers,page=page)
                self.parse(contents,headers)
            except:
                headers = self.update_headers()
                continue


if __name__ == '__main__':
    crawler = Tu_Di_Big_Company()
    crawler.run()
