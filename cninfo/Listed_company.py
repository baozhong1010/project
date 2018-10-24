import requests
from bs4 import BeautifulSoup
import re
import pymysql
import time
import json
# 公司名称,简称,股票代码,上市板块
#shmb = 沪市主板
#szmb = 深市主板
#szsme = 中小企业板
# szcn = =创业板
# hk mb = 香港主板
# hk gem = 香港创业板
 
 
class JuChao(object):
 
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate'}
        self.conn = pymysql.connect(
            host='172.16.0.20',
            user='zhangxiaogang',
            passwd='gangxiaozhang',
            db='cninfo',
            charset='utf8')
        self.cur = self.conn.cursor()
 
    # def get_proxy(self):  #获取代理
    #     manager_host = '118.190.114.196'
    #     manager_port = 8080
    #     order = '38c7e5f5-59a1-11e7-bda9-f45c89a63279'
    #     while True:
    #         url = 'http://%s:%d/get-proxy-api' % (manager_host, manager_port)
    #         params = {'order': order}
    #         res = requests.get(url, params=params)
    #         if res.status_code == 200 and res.text != '{}':
    #             proxy_config = json.loads(res.text)
    #             proxy_port = proxy_config['proxy']
    #             proxy = {'http': f'{proxy_port}'}
    #             break
    #         else:
    #             time.sleep(1)
    #             print(u'暂无可用代理')
    #     return proxy
 
    def get_urls(self, base_url):  # 获取标签url的end
        urls_end = []
        # proxies = JuChao.get_proxy(self)
        req = self.session.get(base_url, headers=self.headers)
        soup = BeautifulSoup(req.text, 'lxml')
        for i in soup.select('.company-list li a'):
            url = i.get('href')
            result = url.split('?', 2)
            urls_end.append(result[-1])
        return urls_end  # szmb000001   #hk  00001
 
    def get_commany_details(self, detail_url):  # 获取公司详情
        # proxies = JuChao.get_proxy(self)
        detail_msg = self.session.get(detail_url, headers=self.headers)
        detail_msg.encoding = 'gb2312'
        soup = BeautifulSoup(detail_msg.text, 'lxml')
        if 'hk' not in detail_url:  #大陆企业
            total_name = soup.select(
                '.clear table tr td:nth-of-type(2)')[0].text.strip()  # 全称
            abb_name = soup.select(
                '.clear table tr td:nth-of-type(8)')[0].text.strip()  # 简称
            part = detail_url.split('/', 5)[-1].split('.', 1)[0]   # 板块
            code = ''.join(re.findall('\d', part))  # 股票代码
            if 'shmb' in detail_url:
                return total_name, abb_name, code, '沪市主板'
            elif 'szmb' in detail_url:
                return total_name, abb_name, code, '深市主板'
            elif 'szsme' in detail_url:
                return total_name, abb_name, code, '中小企业板'
            elif 'szcn' in detail_url:
                return total_name, abb_name, code, '创业板'
        elif 'hk' in detail_url:  #香港企业
            try:
                total_name = soup.select(
                    '.clear table tr:nth-of-type(2) td:nth-of-type(4)')[0].text.strip()  # 全称
                select_abb = str(soup.select(
                    '.zx_info form table tr td:nth-of-type(1)')[0])[65:]
                abb_name = re.findall(r'</strong>(.*)</td>',str(select_abb))[0]  # 简称
                part = detail_url.split('/', 5)[-1].split('.', 1)[0]   # 板块
                code = ''.join(re.findall('\d', part))  # 股票代码
                if 'mb' in detail_url:
                    return total_name, abb_name, code, '香港主板'
                elif 'gem' in detail_url:
                    return total_name, abb_name, code, '香港创业板'
            except BaseException:
                pass
 
        # elif 'hk gem' in detail_url:
        #     # ('平安银行股份有限公司','	平安银行','000001','沪市主板')
        #     return total_name, abb_name, code, '香港创业板'
 
    def save_to_mysql(self, data): #存入数据库
        if data is None:
            pass
        else:
            self.cur.execute(
                f"replace into cninfo_listed_company(total_name, abb_name, stock_code, part) values {data}")
            self.conn.commit()
            print('存储成功:', f'{data}')
 
    def main(self): #执行函数
        base_url = 'http://www.cninfo.com.cn/cninfo-new/information/companylist'
        detail_base_url = 'http://www.cninfo.com.cn/information/brief/'
        #      http://www.cninfo.com.cn/information/brief/szmb000001.html
        hk_detail_base_url = 'http://www.cninfo.com.cn/information/hk/mb/brief'
        #      http://www.cninfo.com.cn/information/hk/mb/brief00034.html
        hk_gem_url = 'http://www.cninfo.com.cn/information/hk/gem/brief'
        #      'http://www.cninfo.com.cn/information/hk/gem/memo08005.html'
        urls_end = self.get_urls(base_url)  # [szmb000001,00001,08001]
 
        for url in urls_end:
            if ''.join(re.findall('\D', url)).isalpha():
                detail_url = detail_base_url + url + '.html'
                data = self.get_commany_details(detail_url)
                self.save_to_mysql(data)
            else:
 
                if int(url) > 8000:
                    hk_gem = hk_gem_url + url + '.html'
                    data = self.get_commany_details(hk_gem)
                else:
                    hk_detail_url = hk_detail_base_url + url + '.html'
                    data = self.get_commany_details(hk_detail_url)
                self.save_to_mysql(data)
 
 
if __name__ == '__main__':
    juchao = JuChao()
    juchao.main()