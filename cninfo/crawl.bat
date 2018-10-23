%~d0
cd %~dp0
start scrapy crawl cninfo_financial
start scrapy crawl cninfocrawler -a crawl_mode=dividend
start scrapy crawl cninfocrawler -a crawl_mode=lastest
start scrapy crawl cninfocrawler -a crawl_mode=brief
start scrapy crawl cninfocrawler -a crawl_mode=issue
start scrapy crawl cninfocrawler -a crawl_mode=management
start scrapy crawl cninfocrawler -a crawl_mode=stockstructure
start scrapy crawl cninfocrawler -a crawl_mode=allotment
start scrapy crawl cninfo_shareholders
start scrapy crawl cninfo_periodic
start scrapy crawl cninfo_relation
start scrapy crawl cninfo_continuou
start scrapy crawl cninfo_charter
start scrapy crawl cninfo_hk_infomation
start scrapy crawl two_network_companies
start scrapy crawl infodis_share_transfer
start scrapy crawl cninfo_full_announcement
scrapy crawl cninfo_announcement_summary