from ClientConf import ClientConf
from MqttClient import MqttClient
import os
from typing import Optional


def main():
    
    client_conf = ClientConf()
    client_conf.host = "0458774161.st1.iotda-app.cn-south-1.myhuaweicloud.com"
    client_conf.port = 8883
    client_conf.topic = "InputBox_RecycleInBox"
    # mqtt接入凭据access_key可使用环境变量的方式注入
    client_conf.access_key = 'MImHc8W7'
    # mqtt接入凭据access_code可使用环境变量的方式注入
    client_conf.access_code = "1LxO05huIQDlUjpCSAqUwe4tphoizwx0"
    client_conf.instance_id = "220e6462-38bf-48b9-84e1-c490265d5ae6"
    mqtt_client = MqttClient(client_conf)
    if mqtt_client.connect() != 0:
        print("init failed")
        return
if __name__ == "__main__":
    main()
