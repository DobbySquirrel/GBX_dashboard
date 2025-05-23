import pymysql
from datetime import datetime

# 连接MySQL 数据库
def connect_db():
    return pymysql.connect(
        host="113.45.11.133",  # 服务器 IP
        port=3306,                 # MySQL 端口（通常为 3306）
        user="Gbx",  # 数据库用户名
        password="Gbx_123123",  # 数据库密码
        database="gbx",  # 数据库名称
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )


# 获取最新数据
def print_latest_data():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rfid_inventory ORDER BY id DESC LIMIT 1")
    record = cur.fetchone()
    conn.close()
    
    if record:
        print("最新的数据记录为：")
        print(record)
    else:
        print("数据库中没有数据。")

# 测试数据库连接
def test_connection():
    try:
        conn = connect_db()
        print("数据库连接成功！")
        conn.close()
        return True
    except Exception as e:
        print(f"数据库连接失败！错误信息：{str(e)}")
        return False

# 获取数据库中的所有表
def get_all_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    tables = cur.fetchall()
    conn.close()
    
    if tables:
        print("数据库中的所有表：")
        for table in tables:
            # 表名在字典的第一个值中
            print(list(table.values())[0])
    else:
        print("数据库中没有表。")

if __name__ == "__main__":
    test_connection()
    get_all_tables()  # 添加调用获取所有表的函数
