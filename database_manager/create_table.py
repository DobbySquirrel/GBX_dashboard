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

# 创建所有表格
def create_all_tables():
    conn = connect_db()
    cur = conn.cursor()
    
    # 室内配送车状态表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS IndoorDeliveryCar_Property_State (
        id INT AUTO_INCREMENT PRIMARY KEY,
        device_id VARCHAR(50) NOT NULL,
        event_time VARCHAR(50) NOT NULL,
        Number VARCHAR(50),
        Status Float,
        PositionX DECIMAL(30,20),
        PositionY DECIMAL(30,20),
        PositionZ DECIMAL(30,20)
    )
    """)
    
    # 室内配送车订单表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS IndoorDeliveryCar_Property_Order (
        id INT AUTO_INCREMENT PRIMARY KEY,
        event_time VARCHAR(50) NOT NULL,
        product_id VARCHAR(50),
        device_id VARCHAR(50),
        Number VARCHAR(50),
        Area VARCHAR(50),
        BoxState VARCHAR(50),
        RFID VARCHAR(50),
        ReceiverPhone VARCHAR(20),
        OrderNumber VARCHAR(50),
        ReceiverName VARCHAR(50),
        SenderName VARCHAR(50),
        Owner VARCHAR(50),
        Converted_RFID VARCHAR(50)
    )
    """)
    
    # 配送无人机状态表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS DeliveryDrone_Property_State (
        id INT AUTO_INCREMENT PRIMARY KEY,
        device_id VARCHAR(50) NOT NULL,
        event_time VARCHAR(50) NOT NULL,
        Altitude DECIMAL(30,20),
        Latitude DECIMAL(30,20),
        Longitude DECIMAL(30,20),
        State Float,
        Time DATETIME,
        VelocityX DECIMAL(30,20),
        VelocityY DECIMAL(30,20),
        VelocityZ DECIMAL(30,20)
    )
    """)
    
    # 配送无人机订单表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS DeliveryDrone_Property_Order (
        id INT AUTO_INCREMENT PRIMARY KEY,
        device_id VARCHAR(50) NOT NULL,
        event_time VARCHAR(50) NOT NULL,
        OrderNumber VARCHAR(50),
        RFID VARCHAR(50),
        ReceiverName VARCHAR(50),
        ReceiverPhone VARCHAR(20),
        ReceiverAddress VARCHAR(100),
        SenderName VARCHAR(50),
        SenderAddress VARCHAR(100),
        Time DATETIME,
        converted_RFID VARCHAR(50),
        owner VARCHAR(50)
    )
    """)
    
    # 包裹所有者表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Box_owner (
        id INT AUTO_INCREMENT PRIMARY KEY,
        event_time VARCHAR(50) NOT NULL,
        product_id VARCHAR(50),
        device_id VARCHAR(50),
        service_id VARCHAR(50),
        owner VARCHAR(50),
        RFID VARCHAR(50),
        converted_RFID VARCHAR(50)
    )
    """)
    
    # 用户积分记录表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS User_Score_Record (
        id INT AUTO_INCREMENT PRIMARY KEY,
        device_id VARCHAR(50),
        event_time VARCHAR(50) NOT NULL,
        RFID VARCHAR(50),
        owner VARCHAR(50),
        converted_RFID VARCHAR(50),
        phone VARCHAR(20),
        service_id VARCHAR(50)
    )
    """)
    
    # 包裹丢失表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Box_Missing (
        id INT AUTO_INCREMENT PRIMARY KEY,
        time DATETIME,
        altitude DECIMAL(30,20),
        latitude DECIMAL(30,20),
        longitude DECIMAL(30,20),
        status VARCHAR(50),
        RFID VARCHAR(50),
        converted_RFID VARCHAR(50),
        device_id VARCHAR(50)
    )
    """)
    
    conn.commit()
    conn.close()
    print("所有表格创建成功！")

def drop_tables():
    conn = connect_db()
    cur = conn.cursor()
    
    # 要删除的表格列表
    tables_to_drop = [
        "IndoorDeliveryCar_Property_State",
        "IndoorDeliveryCar_Property_Order",
        "DeliveryDrone_Property_State",
        "DeliveryDrone_Property_Order",
        "Box_owner",
        "User_Score_Record",
        "Box_Missing",
        # 旧表名也保留，以防它们仍然存在
        "deliverydrone_property_dronedeliveryorder",
        "deliverydrone_property_dronestate",
        "indoordeliverycar_property_indoorcarstate",
        "indoordeliverycar_property_indoordeliveryorder",
        "boxmissing"
    ]
    
    for table in tables_to_drop:
        try:
            cur.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"表 {table} 已成功删除")
        except Exception as e:
            print(f"删除表 {table} 时出错: {str(e)}")
    
    conn.commit()
    conn.close()
    print("指定表格删除操作完成！")

def insert_missing_box_data():
    conn = connect_db()
    cur = conn.cursor()
    
    # 准备插入的数据
    missing_boxes = [
        {
            'time': datetime.now(),
            'altitude': 100.5,
            'latitude': 113.47953830802487,
            'longitude': 22.894216859923475,
            'status': '丢失',
            'RFID': 'RFID001',
            'converted_RFID': 'C_RFID001'
        },
        {
            'time': datetime.now(),
            'altitude': 95.2,
            'latitude': 113.47872088332235,
            'longitude': 22.892061020308077,
            'status': '丢失',
            'RFID': 'RFID002',
            'converted_RFID': 'C_RFID002'
        }
    ]
    
    # 插入数据
    for box in missing_boxes:
        try:
            cur.execute("""
            INSERT INTO Box_Missing (time, altitude, latitude, longitude, status, RFID, converted_RFID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                box['time'], 
                box['altitude'], 
                box['latitude'], 
                box['longitude'], 
                box['status'], 
                box['RFID'], 
                box['converted_RFID']
            ))
            print(f"成功插入丢失包裹数据，RFID: {box['RFID']}")
        except Exception as e:
            print(f"插入数据失败: {str(e)}")
    
    conn.commit()
    conn.close()
    print("丢失包裹数据插入完成！")

if __name__ == "__main__":
    test_connection()
    drop_tables()  # 删除指定的表格
    get_all_tables()  # 添加调用获取所有表的函数
    create_all_tables()  # 创建所有表格
    # insert_missing_box_data()  # 插入丢失包裹数据