# -*- encoding: utf-8 -*-
'''
平台设置属性，查询属性，设备上报属性demo
'''
import time
import logging
from datetime import datetime, timedelta
import json
import sys
sys.path.append('/mnt/c/Users/dobby/Desktop/iot_mqtt_test/mqttdemo')
from IoT_device.client.IoT_client_config import IoTClientConfig
from IoT_device.client.IoT_client import IotClient
from IoT_device.request.services_properties import ServicesProperties
# 日志设置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def report_warehouse_properties(iot_client):

    # warehouse properties
    warehouse_delivery_order_property = ServicesProperties()
    warehouse_delivery_order_property.add_service_property(service_id="UserInfo", property='id', value="GBX00007")
    warehouse_delivery_order_property.add_service_property(service_id="UserInfo", property='user', value="liuhao1")
    warehouse_delivery_order_property.add_service_property(service_id="UserInfo", property='Converted_RFID', value="E0 00 20 24 11 05 00 00 00 00 01 11")

    iot_client.report_properties(warehouse_delivery_order_property.service_property, qos=1)
    time.sleep(2)
def report_drone_properties(iot_client):
    delivery_time = datetime(2024, 9, 8, 9, 45, 0)
    # DroneDeliveryOrder properties
    drone_delivery_order_property = ServicesProperties()
    drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='OrderNumber', value="ORD123456789")
    drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='ReceiverName', value="王明")
    drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='ReceiverPhone', value="+1234567890")
    drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='ReceiverAddress', value="NN-6")
    drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='SenderName', value="Jane Smith")
    drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='SenderAddress', value="心连心餐厅")
    drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='Time', value=delivery_time.strftime('%Y-%m-%d %H:%M:%S'))
    drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='RFID', value="GBX00007")
    drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='Owner', value="yuhang")
    drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='Converted_RFID', value="E0 00 20 24 11 05 00 00 00 00 01 11")
        # Report DroneDeliveryOrder properties
    iot_client.report_properties(drone_delivery_order_property.service_property, qos=1)

def report_delivery_locker_properties(iot_client):
    input_delivery_property = ServicesProperties()
    input_delivery_property.add_service_property(service_id="InputDelivery", property='Number', value="IDL123")
    input_delivery_property.add_service_property(service_id="InputDelivery", property='Status', value="Available")
    input_delivery_property.add_service_property(service_id="InputDelivery", property='CellNumer', value='C123')
    input_delivery_property.add_service_property(service_id="InputDelivery", property='CellStatus', value="C124")
    input_delivery_property.add_service_property(service_id="InputDelivery", property='RFID', value="GBX00005")
    input_delivery_property.add_service_property(service_id="InputDelivery", property='Owner', value="hongda")
    input_delivery_property.add_service_property(service_id="InputDelivery", property='Converted_RFID', value="E0 00 20 24 11 05 00 00 00 00 01 11")
    time.sleep(2)
    # Report each InputDelivery property for the cells
    iot_client.report_properties(input_delivery_property.service_property, qos=1)

    output_delivery_property = ServicesProperties()
    output_delivery_property.add_service_property(service_id="OutputDelivery", property='CollectCode', value='2437')
    output_delivery_property.add_service_property(service_id="OutputDelivery", property='OccupyRatio', value=0.5)
    output_delivery_property.add_service_property(service_id="OutputDelivery", property='RFID', value="GBX00005")
    output_delivery_property.add_service_property(service_id="OutputDelivery", property='Owner', value="xibin")
    output_delivery_property.add_service_property(service_id="OutputDelivery", property='Converted_RFID', value="E0 00 20 24 11 05 00 00 00 00 01 11")
    time.sleep(2)
    # Report each OutputDelivery property
    iot_client.report_properties(output_delivery_property.service_property, qos=1)

    # RecycleDelivery properties: BoxNumber表示回收柜中箱子的个数
    recycle_box_lists = [[1, 2], [1, 3], [2, 4], [3, 6]]  # 不同回收柜内的箱子编号列表

    recycle_delivery_property = ServicesProperties()
    # BoxNumber 直接用 BoxList 的长度表示
    recycle_delivery_property.add_service_property(service_id="RecycleDelivery", property='BoxNumber', value=2)
    recycle_delivery_property.add_service_property(service_id="RecycleDelivery", property='BoxList', value=[1,2])
    recycle_delivery_property.add_service_property(service_id="RecycleDelivery", property='RFID', value="GBX00001")
    recycle_delivery_property.add_service_property(service_id="RecycleDelivery", property='Owner', value="zibo")
    recycle_delivery_property.add_service_property(service_id="RecycleDelivery", property='Converted_RFID', value="E0 00 20 24 11 05 00 00 00 00 00 01")
    time.sleep(2)
    iot_client.report_properties(recycle_delivery_property.service_property, qos=1)


def run():
    # 第一个设备：DroneState 和 DroneDeliveryOrder
    warehouse_cfg = IoTClientConfig(server_ip='116.205.178.237',
                                device_id='6729c1a340428521209c0759_WareHouse_Reader01',
                                secret='2aa35b6108ded7c889ee', is_ssl=False)
    warehouse_client = IotClient(warehouse_cfg)
    warehouse_client.connect()
    warehouse_client.start()
    warehouse_client.subscribe(r'$oc/devices/' + '6729c1a340428521209c0759_WareHouse_Reader01'+ r'/sys/properties/report')
    # 第二个设备： DroneDeliveryOrder
    drone_cfg = IoTClientConfig(server_ip='116.205.178.237',
                                device_id='66dabbab1837002b28b35a64_Device_Identification_1581F6GKB23C0040092',
                                secret='681bee8fdc1b21b5b040', is_ssl=False)
    drone_client = IotClient(drone_cfg)
    drone_client.connect()
    drone_client.start()
    drone_client.subscribe(r'$oc/devices/' + '66dabbab1837002b28b35a64_Device_Identification_1581F6GKB23C0040092'+ r'/sys/properties/report')

    # 第三个设备：DeliveryLocker
    locker_cfg = IoTClientConfig(server_ip='116.205.178.237',
                                 device_id='66dd1bb4eff8e33e5f3f233f_test',
                                 secret='d4db2fbcbca2ae3ab766', is_ssl=False)
    locker_client = IotClient(locker_cfg)
    locker_client.connect()
    locker_client.start()
    locker_client.subscribe(r'$oc/devices/' + '66dd1bb4eff8e33e5f3f233f_test'+ r'/sys/properties/report')

    # 定时上报属性
    while True:

        # 上报 DroneDeliveryOrder 的属性
        report_warehouse_properties(warehouse_client)

        # # 上报 DroneDeliveryOrder 的属性
        report_drone_properties(drone_client)
        
        # # # 上报 DeliveryLocker 的属性
        # report_delivery_locker_properties(locker_client)
        
        break
        time.sleep(5)

if __name__ == '__main__':
    run()
