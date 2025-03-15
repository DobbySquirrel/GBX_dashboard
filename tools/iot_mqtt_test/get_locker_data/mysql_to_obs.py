import pymysql
import io
import pandas as pd
from obs import ObsClient, PutObjectHeader
import traceback

def connect_db():
    """连接数据库"""
    return pymysql.connect(
        host="rm-7xvp16lkdgrben2w2bo.mysql.rds.aliyuncs.com",
        port=3306,
        user="dbuser",
        password="GBX2025aa",
        database="gbx2025",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def upload_to_obs(data_stream, object_key):
    """
    流式上传数据到OBS
    :param data_stream: 数据流对象
    :param object_key: OBS中的对象键名
    :return: bool 上传是否成功
    """
    ak = 'NDUQZS2WFPGUUPEDRH27'
    sk = 'jhXyRbbqAMcgJtxa7LwcDQSBg8LonJTCaCzx7ORS'
    server = "https://obs.cn-south-1.myhuaweicloud.com"
    bucket_name = "gbxbox1"
    
    obs_client = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)
    try:
        headers = PutObjectHeader()
        resp = obs_client.putContent(bucketName=bucket_name, 
                                   objectKey=object_key, 
                                   content=data_stream)
        
        if resp.status < 300:
            print('上传到OBS成功')
            return True
        else:
            print('上传到OBS失败')
            print('错误代码:', resp.errorCode)
            print('错误信息:', resp.errorMessage)
            return False
    except:
        print('上传到OBS失败')
        print(traceback.format_exc())
        return False

def sync_mysql_to_obs():
    """
    同步MySQL数据到OBS
    """
    try:
        # 连接数据库并获取数据
        conn = connect_db()
        query = "SELECT * FROM rfid_inventory"
        df = pd.read_sql(query, conn)
        
        # 将DataFrame转换为CSV格式的内存流
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        
        # 将StringIO转换为BytesIO，因为OBS需要二进制流
        data_stream = io.BytesIO(csv_buffer.getvalue().encode())
        
        # 使用固定的对象键名
        obs_key = "RFID_Data/rfid_inventory.csv"
        
        # 上传到OBS
        if upload_to_obs(data_stream, obs_key):
            print("数据同步完成！")
        else:
            print("数据上传到OBS失败！")
            
        # 关闭连接和流
        conn.close()
        csv_buffer.close()
        data_stream.close()
        
    except Exception as e:
        print(f"数据同步失败: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    sync_mysql_to_obs() 