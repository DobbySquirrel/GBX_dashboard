# coding:utf-8
import os

from obs import ObsClient
# 认证用的ak和sk直接写到代码中有很大的安全风险，建议在配置文件或者环境变量中密文存放，使用时解密，确保安全；
# 本示例以ak和sk保存在环境变量中来实现身份验证为例，运行本示例前请先在本地环境中设置环境变量HUAWEICLOUD_SDK_AK和HUAWEICLOUD_SDK_SK。
AK = 'NDUQZS2WFPGUUPEDRH27'
SK = 'jhXyRbbqAMcgJtxa7LwcDQSBg8LonJTCaCzx7ORS'
ENDPOINT = "obs.cn-south-1.myhuaweicloud.com"

obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=ENDPOINT)

bucket_name = "gbxbox1"
remote_prefix = ""

local_folder = r"/mnt/c/Users/dobby/Desktop/iot_mqtt_test/OBS"
page = 1
failed_list = []

prefix_length = len(remote_prefix)

object_list = obsClient.listObjects(bucket_name, prefix=remote_prefix, encoding_type="url")

while True:
    print("Start to download page %s" % page)
    page += 1
    for obs_object in object_list.body["contents"]:
        object_key = obs_object["key"]
        # 将 OBS 中的对象名转换为本地路径
        download_file_path = os.path.join(local_folder, object_key[prefix_length:].replace("/", os.sep))
        print("Start to download object [%s] to [%s]" % (object_key, download_file_path))
        try:
            obsClient.downloadFile(bucket_name, object_key, taskNum=10,
                                   downloadFile=download_file_path)
        except Exception as e:
            print("Failed to download %s" % object_key)
            failed_list.append(object_key)

    # 如果 is_truncated 为 True 则说明全部列举完成，没有剩余
    if not object_list.body["is_truncated"]:
        break
    # 使用上次返回的 next_marker 作为下次列举的 marker
    object_list = obsClient.listObjects(bucket_name, prefix=remote_prefix,
                                        encoding_type="url", marker=object_list.body["next_marker"])

for i in failed_list:
    print("Failed to download %s, please try again" % i)

