from obs import GetObjectHeader
from obs import ObsClient
import os
import traceback

# 推荐通过环境变量获取AKSK，这里也可以使用其他外部引入方式传入。如果使用硬编码可能会存在泄露风险
# 您可以登录访问管理控制台获取访问密钥AK/SK，获取方式请参见https://support.huaweicloud.com/usermanual-ca/ca_01_0003.html。
ak = 'NDUQZS2WFPGUUPEDRH27'
sk = 'jhXyRbbqAMcgJtxa7LwcDQSBg8LonJTCaCzx7ORS'
server = "https://obs.cn-south-1.myhuaweicloud.com"
# 创建obsClient实例
# 如果使用临时AKSK和SecurityToken访问OBS，需要在创建实例时通过security_token参数指定securityToken值
obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)
try:
    # 下载对象的附加头域
    headers = GetObjectHeader()
    # 下载到本地的路径,localfile为包含本地文件名称的全路径
    downloadPath = '/mnt/c/Users/dobby/Desktop/iot_mqtt_test/OBS/DeliveryDrone_Property_DroneState.csv'
    bucketName = "gbxbox1"
    objectKey = "DeliveryDrone_Property/DeliveryDrone_Property_DroneState.csv"
    # 文件下载
    resp = obsClient.getObject(bucketName, objectKey, downloadPath, headers=headers)
    # 返回码为2xx时，接口调用成功，否则接口调用失败
    if resp.status < 300:
        print('Get Object Succeeded')
        print('requestId:', resp.requestId)
        print('url:', resp.body.url)
    else:
        print('Get Object Failed')
        print('requestId:', resp.requestId)
        print('errorCode:', resp.errorCode)
        print('errorMessage:', resp.errorMessage)
except:
    print('Get Object Failed') 
    print(traceback.format_exc())

from obs import ObsClient
from obs import PutObjectHeader
import os
import traceback

# 如果使用临时AKSK和SecurityToken访问OBS，需要在创建实例时通过security_token参数指定securityToken值
obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)
try:
    # 上传对象的附加头域
    headers = PutObjectHeader()
    bucketName = "gbxbox1"
    # 对象名，即上传后的文件名
    objectKey = "User_Score/User_Score_Record_2.csv"
    # 待上传文件的完整路径，如aa/bb.txt
    file_path = downloadPath
    # 文件上传
    resp = obsClient.putFile(bucketName=bucketName, objectKey=objectKey, file_path=file_path, headers=headers)
    # 返回码为2xx时，接口调用成功，否则接口调用失败
    if resp.status < 300:
        print('Put File Succeeded')
        print('requestId:', resp.requestId)
        print('etag:', resp.body.etag)
        print('versionId:', resp.body.versionId)
        print('storageClass:', resp.body.storageClass)
    else:
        print('Put File Failed')
        print('requestId:', resp.requestId)
        print('errorCode:', resp.errorCode)
        print('errorMessage:', resp.errorMessage)
except:
    print('Put File Failed')
    print(traceback.format_exc())