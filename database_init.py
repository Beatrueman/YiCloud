import pymysql
import config

def check_table(table_name):
    conn = None
    try:
        conn = pymysql.connect(host=config.host, user=config.user, password=config.password, port=3306,database=config.database)
        cursor = conn.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        return cursor.fetchone() is not None
    except pymysql.Error as e:
        print("数据库错误：",e)
    finally:
        if conn and conn.open:
            conn.close()

def db_init(filename):
    global conn, cursor
    conn = None
    try:
        # 连接数据库
        conn = pymysql.connect(host=config.host ,user=config.user, password=config.password,port=3306,database=config.database)
        # 创建一个数据库游标用于执行sql查询并处理查询结果。
        cursor = conn.cursor()

        # 逐行读取sql文件
        with open(filename, 'r') as sql_file:
            queries = sql_file.read()
            query_list = queries.split(';')

            # 逐行执行查询语句
            for query in query_list:
                if query.strip()!='':
                    cursor.execute(query)

            # 提交事务
            conn.commit()
            print("数据库初始化完成！")


    except pymysql.Error as e:
        print("数据库错误：",e)


    finally:
        if conn and conn.open:
            cursor.close()
            conn.close()

def main():
    sql_file = '/YiCloud/database/cloud_user.sql'
    if not check_table('cloud_user'):
        db_init(sql_file)
    else:
        print('已存在cloud_user表，无需初始化数据库。')

if __name__ == '__main__':
    main()

