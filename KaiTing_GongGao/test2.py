import  fool
import pymysql

conn = pymysql.connect(host='172.16.0.20', port=3306, user='zhangxiaogang', passwd='gangxiaozhang',
                           db='cninfo', charset='utf8')
cursor = conn.cursor()


def save_to_sql(sql):
    try:
        cursor.execute(sql)
        conn.commit()
        print('NEW')
    except:
        print('OLD')

def main():
    sql = "select * from cninfo_bond_overview"
    cursor.execute(sql)
    for info in cursor.fetchall():
        bond_name = info[4]
        company_name = parse(bond_name)
        sql1 = "update cninfo_bond_overview set company_name='%s' where bond_name='%s'" % (company_name,bond_name)
        cursor.execute(sql1)
        print(sql1)

def parse(bond_name):
    words, ners = fool.analysis(bond_name)
    for info in ners:
        for contents in info:
            if 'company' in contents:
                return contents[3]

if __name__ == '__main__':
    main()