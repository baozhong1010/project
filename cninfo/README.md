巨潮资讯爬虫

AUTH : 杜建业
UPDATE: 20180911

python -V = 3.6.4
scrapy -V = 1.5.0

所需环境 cmd 执行 pip install -r requirements.txt

官网地址:http://www.cninfo.com.cn/information/companyinfo_n.html?fulltext?szmb000001

数据库地址172.0.16.20------cninfo

数据表说明表cninfo_a_tip

使用说明:

    scrapy crawl cninfocrawler    #上市公司(hk_cn)概况+最新资料+发行筹资+分红+配股+高管人员+股本结构

    start scrapy crawl cninfocrawler -a crawl_mode=dividend  #分红

    start scrapy crawl cninfocrawler -a crawl_mode=lastest   #最新资料

    start scrapy crawl cninfocrawler -a crawl_mode=brief    #概况

    start scrapy crawl cninfocrawler -a crawl_mode=issue    #发行筹资

    start scrapy crawl cninfocrawler -a crawl_mode=management  #高管人员

    start scrapy crawl cninfocrawler -a crawl_mode=stockstructure #股本结构

    start scrapy crawl cninfocrawler -a crawl_mode=allotment  #配股

    scrapy crawl cninfo_financial  # 上市公司财务指标

    scrapy crawl cninfo_shareholders  # 上市公司十大股东

    scrapy crawl cninfo_periodic  # 上市公司定期公告

    scrapy crawl cninfo_relation  # 上市公司投资者关系

    scrapy crawl cninfo_continuou  # 上市公司持续督导意见

    scrapy crawl cninfo_charter # 上市公司章程制度

    scrapy crawl cninfo_hk_infomation # 香港上市公司公告

    scrapy crawl scrapy crawl two_network_companies # 两网公司及退市公司

    scrapy crawl infodis_share_transfer # 股份转让系统挂牌公司

    scrapy crawl cninfo_full_announcement # 公告全文

    scrapy crawl cninfo_announcement_summary #公告摘要

    ......







