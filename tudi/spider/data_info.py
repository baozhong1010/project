import MySQLdb

conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='root',
                           db='test', charset='utf8')
cursor = conn.cursor()

def get_info_xing_zheng_qu():
    sql = "select * from xing_zheng_qu"
    cursor.execute(sql)
    contents = cursor.fetchall()
    for info in contents:
        name = info[0]
        id = info[1]
        yield [name,id]

def get_info_gong_ying_way():
    sql = "select * from gong_ying_way"
    cursor.execute(sql)
    contents = cursor.fetchall()
    for info in contents:
        name = info[0]
        id = info[1]
        yield [name,id]

