from client_conf import ClientConf
from mqtt_client import MqttClient
import os

def main():
    client_conf = ClientConf()
    client_conf.host = "0458774161.st1.iotda-device.cn-south-1.myhuaweicloud.com"
    client_conf.port = 8883
    client_conf.topic = "$oc/devices/66dd22421837002b28b3a3f3_test/sys/properties/report"
    client_conf.access_key = "q88Tkytm"#username
    client_conf.access_code = "UIuju9pzcYYu64hwctN3M0tUp49NYrYP"#password
    client_conf.instance_id = "66dd22421837002b28b3a3f3_test_0_0_2024090805"

    mqtt_client = MqttClient(client_conf)
    if mqtt_client.connect() != 0:
        print("Connection failed")

if __name__ == "__main__":
    main()
# {
#     "services": [ {
#             "service_id": "OutdoorCarState",
#             "properties": {
#                 "Number": "",
#                 "Status": "",
#                 "PositionX": "0.0",
#                 "PositionY": "0.0",
#                 "PositionZ": "0.0"
#             }
#         }]
# }
# #######################################
# {
#     "services": [        {
#             "service_id": "OutdoorDeliveryOrder",
#             "properties": {
#                 "Number": "",
#                 "Area": "",
#                 "BoxState": "",
#                 "BoxRFID": "",
#                 "Path": "",
#                 "User": ""
#             }
#         }]
# }