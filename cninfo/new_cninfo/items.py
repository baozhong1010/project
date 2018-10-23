# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
#
import scrapy


class NewCninfoItem_cn(scrapy.Item):  #国内基本资料
    # define the fields for your item here like:
    # name = scrapy.Field()

    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field()# 股票简称
    company_name = scrapy.Field() # 公司全称
    company_english_name = scrapy.Field() # 英文名称
    registered_address = scrapy.Field() # 注册地
    company_abb_name = scrapy.Field() # 公司简称
    legal_person = scrapy.Field() # 法定代表人
    company_secretary = scrapy.Field() # 公司董秘
    registered_capital = scrapy.Field() # 注册资本
    type_of_industry = scrapy.Field() # 行业种类
    postal_code = scrapy.Field() # 邮政编码
    company_phone = scrapy.Field() # 公司电话
    company_fax = scrapy.Field() # 公司传真
    company_website = scrapy.Field() # 公司网址
    time_to_market = scrapy.Field() # 上市时间
    ipo_time = scrapy.Field() # 招股时间
    issue_number = scrapy.Field() # 发行数量(万股)
    issue_price = scrapy.Field() # 发行价格(元)
    earnings_ratio = scrapy.Field() # 发行市盈率(倍)
    issuance_method = scrapy.Field() #发行方式
    lead_underwriter = scrapy.Field() # 主承销商
    listed_recommender = scrapy.Field() # 上市推荐人
    sponsor_institution = scrapy.Field() # 保荐机构

class NewCninfoItem_cn_hk(scrapy.Item):   #香港基本资料
    stock_code = scrapy.Field()  # 股票代码
    stock_name = scrapy.Field()# 股票简称
    address = scrapy.Field() # 公司地址
    main_business = scrapy.Field() # 主营业务
    chairman = scrapy.Field() # 主席
    category = scrapy.Field() # 行业分类
    place_of_incorporation = scrapy.Field() # 注册地点
    registrar = scrapy.Field() # 过户处
    board_lot = scrapy.Field() # 买卖单位
    issued_share = scrapy.Field() # 发行股数
    market_capitalisation_currency = scrapy.Field() # 市值货币
    market_capitalisation = scrapy.Field() # 市值
    EPS_currency = scrapy.Field() # 每股盈利货币
    earning_per_share = scrapy.Field() # 每股盈利
    EPS_adjusted_indicator = scrapy.Field() # 每股盈利经调整指示
    trading_currency = scrapy.Field() # 交易货币
    listing_date = scrapy.Field() # 上市日期
    net_profit_currency = scrapy.Field() # 纯利货币
    net_profit = scrapy.Field() # 纯利
    net_asset_value = scrapy.Field() #资产净值货币
    Net_assetvalue = scrapy.Field() # 资产净值
    indicator = scrapy.Field() # 指示


class lastest(scrapy.Item):  #最新资料
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field()
    latest_share_statu = scrapy.Field()  # 最新股本状况  存key:value值
    latest_financial_indicator = scrapy.Field()  #最新财务指标  存key:value值
    latest_announcement = scrapy.Field()   #最新公告  存key:value值
    company_note = scrapy.Field()  #公司备忘  存key:value值


class issue(scrapy.Item):   # 发行筹资
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field()
    issuance_financing = scrapy.Field()  # 最新股本状况  存key:value值
    prospectu = scrapy.Field()  #最新财务指标  存key:value值
    listing_announcement = scrapy.Field()   #最新公告  存key:value值
    share_placement_statement = scrapy.Field()  #公司备忘  存key:value值


class dividend(scrapy.Item):  # 分红
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field()
    year = scrapy.Field()  # 分红年度
    dividend_plan = scrapy.Field()  #分红方案
    equity_registration_date = scrapy.Field()   #股权登记日
    dividend_date = scrapy.Field()  #除权基准日
    red_stock_listing_day = scrapy.Field()  # 红菇上市日


class allotment(scrapy.Item):  # 配股
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field()
    year = scrapy.Field()  # 分红年度
    allotment_plan = scrapy.Field()  #配股方案
    allotment_price = scrapy.Field()   #配股价
    equity_registration_date = scrapy.Field()  #股权登记日
    dividend_date = scrapy.Field()  # 除权基准日
    start_end_date_of_issue = scrapy.Field()  #配股缴款起止日
    part_of_listing_day =  scrapy.Field()  #配股可流通部分上市日


class management(scrapy.Item):  # 高管人员
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field() # 股票简称
    name = scrapy.Field()  # 姓名
    position = scrapy.Field()  # 职位
    birth = scrapy.Field()  # 出生面粉
    gender = scrapy.Field()  #  性别
    education = scrapy.Field()  # 学历



class stockstructure(scrapy.Item):  # 股本结构
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field()# 股票简称
    change_date = scrapy.Field() # 变动日期
    reason_for_change = scrapy.Field() # 变动原因
    circulated_share = scrapy.Field() # 已流通股份
    rmb_common_stock = scrapy.Field() # 人民币普通股
    domestically_listed_foreign_share_B = scrapy.Field() # 境内上市外资股（B股）
    domestically_listed_foreign_share = scrapy.Field() # 境外上市外资股
    other_outstanding_share = scrapy.Field() # 其他流通股
    restricted_share = scrapy.Field() # 流通受限股份
    state_owned_share = scrapy.Field() # 国有股
    domestic_share_other_than_state_owned_share = scrapy.Field() # 国有股以外的内资股
    foreign_shareholding = scrapy.Field() # 外资持股
    placing_legal_person_share = scrapy.Field() # 配售法人股
    uncirculated_share = scrapy.Field() # 未流通股份
    state_owned_share_1 = scrapy.Field() # 国有gu
    domestic_legal_person_holding = scrapy.Field() # 境内法人持股
    foreign_legal_person_holding_share = scrapy.Field() # 境外法人持股
    natural_person_holding = scrapy.Field() #自然人持股
    other_undistributed_share = scrapy.Field() # 其他未流通股
    total_sharecapital = scrapy.Field() # 总股本



class balancesheet(scrapy.Item):    #资产负债表
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field() # 股票简称
    year = scrapy.Field()  # 年
    reporting_period = scrapy.Field()  # 报告期
    table_content = scrapy.Field()  # 表格内容


class incomestatements(scrapy.Item):  #利润表
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field()
    year = scrapy.Field()  # 年
    reporting_period = scrapy.Field()  # 报告期
    table_content = scrapy.Field()  # 表格内容


class cashflow(scrapy.Item):   #现金流
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field()
    year = scrapy.Field()  # 年
    reporting_period = scrapy.Field()  # 报告期
    table_content = scrapy.Field()  # 表格内容


class financialreport(scrapy.Item):   #综合能力
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field()
    year = scrapy.Field()  # 年
    reporting_period = scrapy.Field()  # 报告期
    table_content = scrapy.Field()  # 表格内容


class cninfo_ten_shareholder(scrapy.Item):   #十大股东
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field()
    deadline = scrapy.Field()  # 截至尼日
    shareholder_name = scrapy.Field()  # 股东名称
    number_of_share_held = scrapy.Field()  # 持股数量
    shareholding_ratio = scrapy.Field()  # 持股比例
    nature_of_share = scrapy.Field() #股份性质

class cninfo_periodic_report(scrapy.Item):  #定期报告
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field() #股票简称
    type = scrapy.Field()  # 公告类型
    title = scrapy.Field()  # 标题
    publish_time = scrapy.Field()  # 公告时间
    path = scrapy.Field()  # 本地储存路径
    adjunct_url = scrapy.Field() #网上预览地址


class cninfo_investor_relation_information(scrapy.Item):  #投资者关系
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field() #股票简称
    type = scrapy.Field()  # 公告类型
    title = scrapy.Field()  # 标题
    publish_time = scrapy.Field()  # 公告时间
    path = scrapy.Field()  # 本地储存路径
    adjunct_url = scrapy.Field() #网上预览地址


class cninfo_continuou_supervision_view(scrapy.Item):  #持续督导意见
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field() #股票简称
    type = scrapy.Field()  # 公告类型
    title = scrapy.Field()  # 标题
    publish_time = scrapy.Field()  # 公告时间
    path = scrapy.Field()  # 本地储存路径
    adjunct_url = scrapy.Field() #网上预览地址


class cninfo_charter_system(scrapy.Item):  #章程制度
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field() #股票简称
    type = scrapy.Field()  # 公告类型
    title = scrapy.Field()  # 标题
    publish_time = scrapy.Field()  # 公告时间
    path = scrapy.Field()  # 本地储存路径
    adjunct_url = scrapy.Field() #网上预览地址


class cninfo_hk_information_bulletin(scrapy.Item):  #章程制度
    stock_code = scrapy.Field()  # 股票代码
    stock_abb_name = scrapy.Field() #股票简称
    title = scrapy.Field()  # 标题
    publish_time = scrapy.Field()  # 公告时间
    path = scrapy.Field()  # 本地储存路径
    adjunct_url = scrapy.Field() #网上预览地址



class cninfo_infodis_two_network_companies_and_delisting_company(scrapy.Item): #两网公司及退市公司
    stock_code = scrapy.Field()  # 股票代码
    industry_category = scrapy.Field()  # 行业类别
    announcement_category = scrapy.Field()  # 公告类别
    title = scrapy.Field()  # 标题
    announment_id = scrapy.Field() #pdf文件id
    publish_time = scrapy.Field()  # 公告时间
    adjunct_url = scrapy.Field()  # 网上预览地址
    path = scrapy.Field()  # 本地保存地址

class cninfo_infodis_share_transfer_system_listing_company(scrapy.Item): #股份转让挂牌
    stock_code = scrapy.Field()  # 股票代码
    industry_category = scrapy.Field()  # 行业类别
    announcement_category = scrapy.Field()  # 公告类别
    title = scrapy.Field()  # 标题
    announment_id = scrapy.Field() #pdf文件id
    publish_time = scrapy.Field()  # 公告时间
    adjunct_url = scrapy.Field()  # 网上预览地址
    path = scrapy.Field()  # 本地保存地址

class cninfo_full_announcement(scrapy.Item):
    stock_code = scrapy.Field()  # 股票代码
    type = scrapy.Field()  # 标题
    announcement_title = scrapy.Field()  # 公告标题
    announcement_id = scrapy.Field()  # 公告id
    adjunct_url = scrapy.Field() #pdf文件yulandizhi
    publish_time = scrapy.Field()  # 公告时间
    path = scrapy.Field()  # 本地保存地址


class cninfo_announcement_summary(scrapy.Item):  #定期报告
    stock_code = scrapy.Field()  # 股票代码
    announcement_title = scrapy.Field()  # 标题
    publish_time = scrapy.Field()  # 公告时间
    content = scrapy.Field() #网上预览地址


class ZiliaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #基础资料字段
    code = scrapy.Field()     #债券代码
    bond_abb_name = scrapy.Field()      #债券简称
    part = scrapy.Field()   #债券类别
    bond_name = scrapy.Field()   #债券全称
    bond_english_name = scrapy.Field()  #债券英文全称
    type_of_bond = scrapy.Field()   #债券种类
    bond_form = scrapy.Field()  #债券形式
    interest_payment_method = scrapy.Field()    #付息方式
    value_date = scrapy.Field() #起息日
    expiry_date = scrapy.Field()    #到期日
    redemption_date = scrapy.Field()    #兑付日
    repayment_period = scrapy.Field()   #偿还期限（月）
    interest_date_description = scrapy.Field()  #付息日期说明
    date_of_listing = scrapy.Field()    #上市日期
    termination_of_listing_date = scrapy.Field()    #终止上市日期
    unit_denomination = scrapy.Field()  #单位面值（元）
    interest_rate_type = scrapy.Field()     #利率类型
    coupon_rate = scrapy.Field()    #票面利率（%）
    applicable_date_of_interest_rate_start = scrapy.Field()     #利率起始适用日期
    interest_rate_termination_date = scrapy.Field()     #利率终止适用日期

class FxsituationItem(scrapy.Item):
    #发行情况字段
    code = scrapy.Field()   #债券代码
    issue_object = scrapy.Field()   #发行对象
    issue_price = scrapy.Field()     #发行价格（元）
    exchange_online_issuance_start_date = scrapy.Field()    #发行起始日
    exchange_online_end_date = scrapy.Field()   #发行终止日
    actual_circulation = scrapy.Field()     #实际发行量（万元）
    issuance_method = scrapy.Field()    #发行方式

class BeiwangItem(scrapy.Item):
    #备忘字段
    code = scrapy.Field()   #债券代码
    bond_event = scrapy.Field()     #备忘事件
    bond_time = scrapy.Field()      #备忘时间

class AnnouncementItem(scrapy.Item):
    #公告字段
    code = scrapy.Field()   #债券代码
    gg_title = scrapy.Field()   #公告标题
    gg_id = scrapy.Field()      #公告ID
    gg_time = scrapy.Field()    #公告发布时间
    gg_url = scrapy.Field()     #公告链接
    file_path = scrapy.Field()  #公告存储路径
    download_base_url = scrapy.Field()      #公告下载路径

class Yupilu_AnnouncementItem(scrapy.Item): #预披露公告
    announcement_title = scrapy.Field()    #公告标题
    announcementId = scrapy.Field()     #公告ID
    publish_time = scrapy.Field()       #公告发布时间
    adjunct_url = scrapy.Field()        #公告文件链接
    file_path = scrapy.Field()      #公告存储路径