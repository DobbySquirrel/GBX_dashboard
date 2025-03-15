import pymysql
from datetime import datetime

# 连接阿里云 MySQL 数据库
def connect_db():
    return pymysql.connect(
        host="139.9.35.113",  # 服务器 IP
        port=3306,                 # MySQL 端口（通常为 3306）
        user="huanghongda",  # 数据库用户名
        password="GBX2025aa",  # 数据库密码
        database="gbx",  # 数据库名称
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )

# 创建表（只需首次运行）
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rfid_inventory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rfid_id VARCHAR(50) NOT NULL,
            phone_number VARCHAR(20) DEFAULT NULL,
            status ENUM('入库', '出库', '生成订单') NOT NULL,
            in_time DATETIME DEFAULT NULL,
            out_time DATETIME DEFAULT NULL,
            order_id VARCHAR(50) DEFAULT NULL,
            order_status VARCHAR(50) DEFAULT NULL,
            record_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("数据库表已创建（如果不存在）")

# 生成订单号
def generate_order_id():
    return "GBX" + datetime.now().strftime("%Y%m%d%H%M%S")

# 插入入库记录
def insert_in_record(rfid_id):
    conn = connect_db()
    cur = conn.cursor()
    in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute('''
        INSERT INTO rfid_inventory (rfid_id, status, in_time)
        VALUES (%s, %s, %s)
    ''', (rfid_id, '入库', in_time))
    conn.commit()
    conn.close()
    print(f"RFID {rfid_id} 已入库，入库时间：{in_time}")

# 插入出库记录
def insert_out_record(rfid_id):
    conn = connect_db()
    cur = conn.cursor()
    out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute('''
        INSERT INTO rfid_inventory (rfid_id, status, out_time)
        VALUES (%s, %s, %s)
    ''', (rfid_id, '出库', out_time))
    conn.commit()
    conn.close()
    print(f"RFID {rfid_id} 已出库，出库时间：{out_time}")

# 绑定手机号并生成订单号
def bind_phone_to_rfid(rfid_id, phone_number):
    conn = connect_db()
    cur = conn.cursor()
    order_id = generate_order_id()
    bind_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cur.execute('''
        INSERT INTO rfid_inventory (rfid_id, phone_number, status, in_time, order_id)
        VALUES (%s, %s, %s, %s, %s)
    ''', (rfid_id, phone_number, '生成订单', bind_timestamp, order_id))
    
    conn.commit()
    conn.close()
    print(f"RFID {rfid_id} 绑定手机号 {phone_number}，订单号 {order_id}，绑定时间：{bind_timestamp}")

# 解绑手机号
def unbind_phone_from_rfid(rfid_id):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute('''
        UPDATE rfid_inventory
        SET phone_number = NULL, order_id = NULL
        WHERE rfid_id = %s
    ''', (rfid_id,))
    
    conn.commit()
    conn.close()
    print(f"RFID {rfid_id} 已解绑手机号码及订单号")

# 查询 RFID 是否绑定手机号
def query_phone_for_rfid(rfid_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT phone_number, order_id FROM rfid_inventory WHERE rfid_id = %s
    ''', (rfid_id,))
    result = cur.fetchone()
    conn.close()
    
    if result:
        phone_number, order_id = result['phone_number'], result['order_id']
        return f"手机号: {phone_number}, 订单号: {order_id}" if phone_number else "未绑定"
    return "未绑定"

# 查询手机号的所有记录
def query_phone_history(phone_number):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM rfid_inventory WHERE phone_number = %s
    ''', (phone_number,))
    records = cur.fetchall()
    conn.close()
    return records

# 查询 RFID 的最近一次状态
def query_latest_status(rfid_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT status FROM rfid_inventory WHERE rfid_id = %s ORDER BY record_time DESC LIMIT 1
    ''', (rfid_id,))
    result = cur.fetchone()
    conn.close()
    
    return result['status'] if result else None

# 清除所有数据
def clear_all_data():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM rfid_inventory')
    conn.commit()
    conn.close()
    print("所有数据已清除！")

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

if __name__ == "__main__":
    test_connection()
