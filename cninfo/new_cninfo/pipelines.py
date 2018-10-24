# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#

import pymysql
from new_cninfo.items import *
conn = pymysql.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                       db='cninfo', charset='utf8')
cursor = conn.cursor()
def save_to_sql(sql, params=None):
    try:
        cursor.execute(sql, params)
        conn.commit()
        print('NEW')
    except:
        print('OLD')
class NewCninfoPipeline(object):
    def __init__(self):

        self.conn = pymysql.connect(
            host='172.16.0.20',
            port=3306,
            user='zhangxiaogang',  # 使用自己的用户名
            passwd='gangxiaozhang',  # 使用自己的密码
            db='cninfo',  # 数据库名
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, NewCninfoItem_cn):
            sql_cn = 'insert into cninfo_company_overview(stock_code,stock_abb_name,company_name,company_english_name,registered_address,company_abb_name,legal_person,company_secretary,registered_capital,type_of_industry,postal_code,company_phone,company_fax,company_website,time_to_market,ipo_time,issue_number,issue_price,earnings_ratio,issuance_method,lead_underwriter,listed_recommender,sponsor_institution) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
                     ' on duplicate key update legal_person=%s,company_secretary=%s,registered_capital=%s'
            lis = (
                item['stock_code'],
                item['stock_abb_name'],
                item['company_name'],
                item['company_english_name'],
                item['registered_address'],
                item['company_abb_name'],
                item['legal_person'],
                item['company_secretary'],
                item['registered_capital'],
                item['type_of_industry'],
                item['postal_code'],
                item['company_phone'],
                item['company_fax'],
                item['company_website'],
                item['time_to_market'],
                item['ipo_time'],
                item['issue_number'],
                item['issue_price'],
                item['earnings_ratio'],
                item['issuance_method'],
                item['lead_underwriter'],
                item['listed_recommender'],
                item['sponsor_institution'],
                item['legal_person'],
                item['company_secretary'],
                item['registered_capital'],)
            self.cur.execute(sql_cn, lis)
            self.conn.commit()
        elif isinstance(item, NewCninfoItem_cn_hk):
            sql_cn_hk = 'insert into cninfo_company_hk_overview(stock_code,stock_name,address,main_business,chairman,category,place_of_incorporation,registrar,board_lot,issued_share,market_capitalisation_currency,market_capitalisation,EPS_currency,earning_per_share,EPS_adjusted_indicator,trading_currency,listing_date,net_profit_currency,net_profit,net_asset_value,Net_assetvalue,indicator) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ' \
                        'on duplicate key update chairman=%s,market_capitalisation=%s,earning_per_share=%s,Net_assetvalue=%s,indicator=%s '
            lis = (
                item['stock_code'],
                item['stock_abb_name'],
                item['address'],
                item['main_business'],
                item['chairman'],
                item['category'],
                item['place_of_incorporation'],
                item['registrar'],
                item['board_lot'],
                item['issued_share'],
                item['market_capitalisation_currency'],
                item['market_capitalisation'],
                item['EPS_currency'],
                item['earning_per_share'],
                item['EPS_adjusted_indicator'],
                item['trading_currency'],
                item['listing_date'],
                item['net_profit_currency'],
                item['net_profit'],
                item['net_asset_value'],
                item['Net_assetvalue'],
                item['indicator'],

                item['chairman'],
                item['market_capitalisation'],
                item['earning_per_share'],
                item['Net_assetvalue'],
                item['indicator'],
            )

            self.cur.execute(sql_cn_hk, lis)
            self.conn.commit()
        return item
class NewCninfofinPipeline(object):
    def __init__(self):

        self.conn = pymysql.connect(
            host='172.16.0.20',
            port=3306,
            user='zhangxiaogang',  # 使用自己的用户名
            passwd='gangxiaozhang',  # 使用自己的密码
            db='cninfo',  # 数据库名
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, balancesheet):   #资产负债表
            sql = 'replace into cninfo_fin_ind_balance_sheet(stock_code,stock_abb_name,year,reporting_period,table_content) VALUES (%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['year'],
            item['reporting_period'],
            item['table_content']
            )
            self.cur.execute(sql, lis)
            self.conn.commit()


        elif isinstance(item, incomestatements):   #利润表
            sql = 'replace into cninfo_fin_ind_income_statement(stock_code,stock_abb_name,year,reporting_period,table_content) VALUES (%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['year'],
            item['reporting_period'],
            item['table_content']
            )
            self.cur.execute(sql, lis)
            self.conn.commit()
        elif isinstance(item, cashflow):  #现金流
            sql = 'replace into cninfo_fin_ind_cash_flow_sheet(stock_code,stock_abb_name,year,reporting_period,table_content) VALUES (%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['year'],
            item['reporting_period'],
            item['table_content']
            )
            self.cur.execute(sql, lis)
            self.conn.commit()
        elif isinstance(item, financialreport): #综合能力
            sql = 'replace into cninfo_fin_ind_ability_index(stock_code,stock_abb_name,year,reporting_period,table_content) VALUES (%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['year'],
            item['reporting_period'],
            item['table_content']
            )
            self.cur.execute(sql, lis)
            self.conn.commit()
        elif isinstance(item,lastest):  #最新资料
            sql = 'replace into cninfo_latest_information(stock_code,stock_abb_name,latest_share_statu,latest_financial_indicator,latest_announcement,company_note) VALUES (%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['latest_share_statu'],
            item['latest_financial_indicator'],
            item['latest_announcement'],
            item['company_note']
            )
            self.cur.execute(sql,lis)
            self.conn.commit()
        elif isinstance(item,issue):  #发行筹资
            sql = 'replace into cninfo_issuance_financing(stock_code,stock_abb_name,issuance_financing,prospectu,listing_announcement,share_placement_statement) VALUES (%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['issuance_financing'],
            item['prospectu'],
            item['listing_announcement'],
            item['share_placement_statement']
            )
            self.cur.execute(sql,lis)
            self.conn.commit()
        elif isinstance(item,dividend):  #分红
            sql = 'replace into cninfo_dd_dividend(stock_code,stock_abb_name,year,dividend_plan,equity_registration_date,dividend_date,red_stock_listing_day) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['year'],
            item['dividend_plan'],
            item['equity_registration_date'],
            item['dividend_date'],
            item['red_stock_listing_day']
            )
            self.cur.execute(sql,lis)
            self.conn.commit()
        elif isinstance(item,allotment):  #配股
            sql = 'replace into cninfo_dd_allotment(stock_code,stock_abb_name,year,allotment_plan,allotment_price,equity_registration_date,dividend_date,start_end_date_of_issue,part_of_listing_day) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['year'],
            item['allotment_plan'],
            item['allotment_price'],
            item['equity_registration_date'],
            item['dividend_date'],
            item['start_end_date_of_issue'],
            item['part_of_listing_day']
            )
            self.cur.execute(sql,lis)
            self.conn.commit()
        elif isinstance(item,management):  #高管人员
            sql = 'replace into cninfo_executives(stock_code,stock_abb_name,name,position,birth,gender,education) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['name'],
            item['position'],
            item['birth'],
            item['gender'],
            item['education'],
            )
            self.cur.execute(sql,lis)
            self.conn.commit()
        elif isinstance(item,stockstructure):  #股本结构
            sql = 'replace into cninfo_equity_structure(stock_code,stock_abb_name,change_date,reason_for_change,circulated_share,rmb_common_stock,domestically_listed_foreign_share_B,domestically_listed_foreign_share,other_outstanding_share,restricted_share,state_owned_share,domestic_share_other_than_state_owned_share,foreign_shareholding,placing_legal_person_share,uncirculated_share,state_owned_share_1,domestic_legal_person_holding,foreign_legal_person_holding_share,natural_person_holding,other_undistributed_share,total_sharecapital) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            lis = (
                item['stock_code'],
                item['stock_abb_name'],
                item['change_date'],
                item['reason_for_change'],
                item['circulated_share'],
                item['rmb_common_stock'],
                item['domestically_listed_foreign_share_B'],
                item['domestically_listed_foreign_share'],
                item['other_outstanding_share'],
                item['restricted_share'],
                item['state_owned_share'],
                item['domestic_share_other_than_state_owned_share'],
                item['foreign_shareholding'],
                item['placing_legal_person_share'],
                item['uncirculated_share'],
                item['state_owned_share_1'],
                item['domestic_legal_person_holding'],
                item['foreign_legal_person_holding_share'],
                item['natural_person_holding'],
                item['other_undistributed_share'],
                item['total_sharecapital'],
            )
            self.cur.execute(sql,lis)
            self.conn.commit()
        elif isinstance(item,cninfo_ten_shareholder):  #股本比例
            sql = 'replace into cninfo_ten_shareholder(stock_code,stock_abb_name,deadline,shareholder_name,number_of_share_held,shareholding_ratio,nature_of_share) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['deadline'],
            item['shareholder_name'],
            item['number_of_share_held'],
            item['shareholding_ratio'],
            item['nature_of_share'],
            )
            self.cur.execute(sql,lis)
            self.conn.commit()
        elif isinstance(item,cninfo_periodic_report):  #定期报告
            sql = 'replace into cninfo_periodic_report(stock_code,stock_abb_name,type,title,publish_time,path,adjunct_url) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['type'],
            item['title'],
            item['publish_time'],
            item['path'],
            item['adjunct_url'],
            )
            self.cur.execute(sql,lis)
            self.conn.commit()

        elif isinstance(item,cninfo_investor_relation_information):  #投资者关系
            sql = 'replace into cninfo_investor_relation_information(stock_code,stock_abb_name,type,title,publish_time,path,adjunct_url) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['type'],
            item['title'],
            item['publish_time'],
            item['path'],
            item['adjunct_url'],
            )
            self.cur.execute(sql,lis)
            self.conn.commit()
        elif isinstance(item,cninfo_continuou_supervision_view):  #持续督导意见
            sql = 'replace into cninfo_continuou_supervision_view(stock_code,stock_abb_name,type,title,publish_time,path,adjunct_url) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['type'],
            item['title'],
            item['publish_time'],
            item['path'],
            item['adjunct_url'],
            )
            self.cur.execute(sql,lis)
            self.conn.commit()

        elif isinstance(item,cninfo_charter_system):  #章程制度
            sql = 'replace into cninfo_charter_system(stock_code,stock_abb_name,type,title,publish_time,path,adjunct_url) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['type'],
            item['title'],
            item['publish_time'],
            item['path'],
            item['adjunct_url'],
            )
            self.cur.execute(sql,lis)
            self.conn.commit()

        elif isinstance(item,cninfo_hk_information_bulletin):  #章程制度
            sql = 'replace into cninfo_hk_information_bulletin(stock_code,stock_abb_name,title,publish_time,path,adjunct_url) VALUES (%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['stock_abb_name'],
            item['title'],
            item['publish_time'],
            item['path'],
            item['adjunct_url'],
            )
            self.cur.execute(sql,lis)
            self.conn.commit()

        elif isinstance(item,cninfo_infodis_two_network_companies_and_delisting_company):  #两网公司及退市公司
            sql = 'replace into cninfo_infodis_two_network_companies_and_delisting_company(stock_code,industry_category,announcement_category,title,announment_id,publish_time,adjunct_url,path) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['industry_category'],
            item['announcement_category'],
            item['title'],
            item['announment_id'],
            item['publish_time'],
            item['adjunct_url'],
            item['path'],
            )
            self.cur.execute(sql,lis)
            self.conn.commit()
        elif isinstance(item,cninfo_infodis_share_transfer_system_listing_company):  #股份转让挂牌
            sql = 'replace into cninfo_infodis_share_transfer_system_listing_company(stock_code,industry_category,announcement_category,title,announment_id,publish_time,adjunct_url,path) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['industry_category'],
            item['announcement_category'],
            item['title'],
            item['announment_id'],
            item['publish_time'],
            item['adjunct_url'],
            item['path'],
            )
            self.cur.execute(sql,lis)
            self.conn.commit()

        elif isinstance(item,cninfo_full_announcement):  #公告全文
            sql = 'replace into cninfo_full_announcement(stock_code,type,announcement_title,announcement_id,adjunct_url,publish_time,path) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['type'],
            item['announcement_title'],
            item['announcement_id'],
            item['adjunct_url'],
            item['publish_time'],
            item['path'],

            )
            self.cur.execute(sql,lis)
            self.conn.commit()

        elif isinstance(item,cninfo_announcement_summary):  #公告摘要
            sql = 'replace into cninfo_announcement_summary(stock_code,announcement_title,publish_time,content) VALUES (%s,%s,%s,%s)'
            lis = (
            item['stock_code'],
            item['announcement_title'],
            item['publish_time'],
            item['content'],
            )
            self.cur.execute(sql,lis)
            self.conn.commit()

        elif isinstance(item,ZiliaoItem):#基础资料
            sql = "insert into cninfo_bond_overview values(%s,%s,now(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" \
                  " on duplicate key update bond_code=%s,bond_abb_name=%s,type=%s,bond_name=%s, bond_english_name=%s, type_of_bond=%s," \
                  "bond_form=%s,interest_payment_method=%s,value_date=%s,expiry_date=%s,redemption_date=%s,repayment_period=%s," \
                  "interest_date_description=%s, date_of_listing=%s, termination_of_listing_date=%s, unit_denomination=%s," \
                  "interest_rate_type=%s, coupon_rate=%s, applicable_date_of_interest_rate_start=%s,interest_rate_termination_date=%s"
            save_to_sql(sql, (
                item['code'],
                item['bond_abb_name'],
                item['part'],
                item['bond_name'],
                item['bond_english_name'],
                item['type_of_bond'],
                item['bond_form'],
                item['interest_payment_method'],
                item['value_date'],
                item['expiry_date'],
                item['redemption_date'],
                item['repayment_period'],
                item['interest_date_description'],
                item['date_of_listing'],
                item['termination_of_listing_date'],
                item['unit_denomination'],
                item['interest_rate_type'],
                item['coupon_rate'],
                item['applicable_date_of_interest_rate_start'],
                item['interest_rate_termination_date'],

                item['code'], item['bond_abb_name'], item['part'], item['bond_name'],
                item['bond_english_name'],
                item['type_of_bond'], item['bond_form'], item['interest_payment_method'],
                item['value_date'],
                item['expiry_date'], item['redemption_date'], item['repayment_period'],
                item['interest_date_description'],
                item['date_of_listing'], item['termination_of_listing_date'], item['unit_denomination'],
                item['interest_rate_type'], item['coupon_rate'],
                item['applicable_date_of_interest_rate_start'],
                item['interest_rate_termination_date'],))
        elif isinstance(item,FxsituationItem):
            fx_sql = "insert into cninfo_bond_issuance_situation values(%s,now(),%s,%s,%s,%s,%s,%s) on duplicate key update bond_code=%s,issue_object=%s," \
                     "issue_price=%s,exchange_online_issuance_start_date=%s,exchange_online_end_date=%s,actual_circulation=%s,issuance_method=%s"

            save_to_sql(fx_sql, (item['code'],
                                 item['issue_object'],
                                 item['issue_price'],
                                 item['exchange_online_issuance_start_date'],
                                 item['exchange_online_end_date'],
                                 item['actual_circulation'],
                                 item['issuance_method'],

                                 item['code'],
                                 item['issue_object'],
                                 item['issue_price'],
                                 item['exchange_online_issuance_start_date'],
                                 item['exchange_online_end_date'],
                                 item['actual_circulation'],
                                 item['issuance_method'],))

        elif isinstance(item, BeiwangItem):
            sql = "replace into cninfo_bond_bond_memo values (%s,now(),%s,%s)"
            save_to_sql(sql, (item['code'], item['bond_event'], item['bond_time']))

        elif isinstance(item, AnnouncementItem):
            sql = "insert into cninfo_bond_latest_announcement values(%s,now(),%s,%s,%s,%s,%s,%s) " \
                  "on duplicate key update bond_code=%s," \
                  "announcement_title=%s,announcement_id=%s,publish_time=%s,adjunct_url=%s,path=%s"
            save_to_sql(sql, (item['code'],
                              item['gg_title'],
                              item['gg_id'],
                              item['gg_time'],
                              item['gg_url'],
                              item['file_path'],
                              item['download_base_url'],

                              item['code'],
                              item['gg_title'],
                              item['gg_id'],
                              item['gg_time'],
                              item['gg_url'],
                              item['file_path']))
        return item
