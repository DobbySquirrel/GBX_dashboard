from obs import ObsClient, GetObjectHeader, PutObjectHeader
import traceback

def download_from_obs(object_key, file_path):
    """
    从OBS下载文件
    :param object_key: OBS中的对象键名
    :param file_path: 下载到本地的文件路径
    :return: bool 下载是否成功
    """
    ak = 'NDUQZS2WFPGUUPEDRH27'
    sk = 'jhXyRbbqAMcgJtxa7LwcDQSBg8LonJTCaCzx7ORS'
    server = "https://obs.cn-south-1.myhuaweicloud.com"
    bucket_name = "gbxbox1"
    
    obs_client = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)
    try:
        headers = GetObjectHeader()
        resp = obs_client.getObject(bucket_name, object_key, file_path, headers=headers)
        
        if resp.status < 300:
            print('Download succeeded')
            return True
        else:
            print('Download failed')
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
            return False
    except:
        print('Download failed')
        print(traceback.format_exc())
        return False

def upload_to_obs(object_key, file_path):
    """
    上传文件到OBS
    :param object_key: OBS中的对象键名
    :param file_path: 要上传的本地文件路径
    :return: bool 上传是否成功
    """
    ak = 'NDUQZS2WFPGUUPEDRH27'
    sk = 'jhXyRbbqAMcgJtxa7LwcDQSBg8LonJTCaCzx7ORS'
    server = "https://obs.cn-south-1.myhuaweicloud.com"
    bucket_name = "gbxbox1"
    
    obs_client = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)
    try:
        headers = PutObjectHeader()
        resp = obs_client.putFile(bucketName=bucket_name, objectKey=object_key, 
                                file_path=file_path, headers=headers)
        
        if resp.status < 300:
            print('Upload succeeded')
            return True
        else:
            print('Upload failed')
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
            return False
    except:
        print('Upload failed')
        print(traceback.format_exc())
        return False

def delete_from_obs(object_key):
    """
    从OBS删除文件
    :param object_key: OBS中的对象键名
    :return: bool 删除是否成功
    """
    ak = 'NDUQZS2WFPGUUPEDRH27'
    sk = 'jhXyRbbqAMcgJtxa7LwcDQSBg8LonJTCaCzx7ORS'
    server = "https://obs.cn-south-1.myhuaweicloud.com"
    bucket_name = "gbxbox1"
    
    obs_client = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)
    try:
        resp = obs_client.deleteObject(bucket_name, object_key)
        
        if resp.status < 300:
            print('Delete succeeded')
            return True
        else:
            print('Delete failed')
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
            return False
    except:
        print('Delete failed')
        print(traceback.format_exc())
        return False

# 下载文件
success = download_from_obs(
    object_key="User_Score/Score_Record.csv",
    file_path="/mnt/c/Users/dobby/Desktop/iot_mqtt_test/scores.csv"
)

# # 上传文件
# success = upload_to_obs(
#     object_key="User_Score/Score_Record.csv",
#     file_path="/mnt/c/Users/dobby/Desktop/iot_mqtt_test/scores.csv"
# )

# 删除文件
success = delete_from_obs(object_key="User_Score/Score_Record.csv")