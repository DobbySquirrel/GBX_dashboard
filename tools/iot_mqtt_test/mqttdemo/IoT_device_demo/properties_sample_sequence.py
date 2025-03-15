# -*- encoding: utf-8 -*-
'''
按顺序发送多个设备属性的demo
'''
import time
import logging
import sys
sys.path.append('/mnt/c/Users/dobby/Desktop/iot_mqtt_test/mqttdemo')
from IoT_device.client.IoT_client_config import IoTClientConfig
from IoT_device.client.IoT_client import IotClient
from IoT_device.request.services_properties import ServicesProperties

# 日志设置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def report_drone_properties(drone_client, i, owner="yuhang",SenderName="3456",ReceiverName="6543"):
    """
    上报无人机配送订单和状态信息
    """
    converted_rfid = convert_to_hex_rfid(i)
    drone_order = ServicesProperties()
    drone_order.add_service_property(service_id="DroneDeliveryOrder", property='OrderNumber', value="ORD123456789")
    drone_order.add_service_property(service_id="DroneDeliveryOrder", property='RFID', value=f"GBX0000{str(i)}")
    drone_order.add_service_property(service_id="DroneDeliveryOrder", property='ReceiverName', value=ReceiverName)
    drone_order.add_service_property(service_id="DroneDeliveryOrder", property='ReceiverPhone', value=ReceiverName)
    drone_order.add_service_property(service_id="DroneDeliveryOrder", property='ReceiverAddress', value="10A")
    drone_order.add_service_property(service_id="DroneDeliveryOrder", property='SenderName', value=SenderName)
    drone_order.add_service_property(service_id="DroneDeliveryOrder", property='SenderAddress', value="yiling")
    drone_order.add_service_property(service_id="DroneDeliveryOrder", property='Time', value="123")
    drone_order.add_service_property(service_id="DroneDeliveryOrder", property='Converted_RFID', value=converted_rfid)
    drone_order.add_service_property(service_id="DroneDeliveryOrder", property='Owner', value=owner)
    drone_client.report_properties(drone_order.service_property, qos=1)
    time.sleep(1)
    
    DroneState = ServicesProperties()
    DroneState.add_service_property(service_id="DroneState", property='Altitude', value="22.52433231")  
    DroneState.add_service_property(service_id="DroneState", property='Latitude', value="34.052235")    
    DroneState.add_service_property(service_id="DroneState", property='Longitude', value="-118.243683") 
    DroneState.add_service_property(service_id="DroneState", property='State', value="Active")          
    DroneState.add_service_property(service_id="DroneState", property='Time', value="2024-11-17T08:45:00Z")
    DroneState.add_service_property(service_id="DroneState", property='VelocityX', value="5.75")        
    DroneState.add_service_property(service_id="DroneState", property='VelocityY', value="-1.20")       
    DroneState.add_service_property(service_id="DroneState", property='VelocityZ', value="0.00")        
    drone_client.report_properties(DroneState.service_property, qos=1)
    time.sleep(1)

def report_outdoor_properties(outdoor_client, i, owner="outdoor_car",SenderName="1234",ReceiverName="4321"):
    """
    上报室外配送订单和车辆状态信息
    """
    converted_rfid = convert_to_hex_rfid(i)
    outdoor_delivery_order_property = ServicesProperties()
    outdoor_delivery_order_property.add_service_property(service_id="OutdoorDeliveryOrder", property='Number', value="OD123456789")
    outdoor_delivery_order_property.add_service_property(service_id="OutdoorDeliveryOrder", property='Area', value="10A")
    outdoor_delivery_order_property.add_service_property(service_id="OutdoorDeliveryOrder", property='BoxState', value="In Use")
    outdoor_delivery_order_property.add_service_property(service_id="OutdoorDeliveryOrder", property='RFID', value=f"GBX0000{str(i)}")
    outdoor_delivery_order_property.add_service_property(service_id="OutdoorDeliveryOrder", property='ReceiverPhone', value=ReceiverName)
    outdoor_delivery_order_property.add_service_property(service_id="OutdoorDeliveryOrder", property='OrderNumber', value="ORD123456789")
    outdoor_delivery_order_property.add_service_property(service_id="OutdoorDeliveryOrder", property='ReceiverName', value=ReceiverName)
    outdoor_delivery_order_property.add_service_property(service_id="OutdoorDeliveryOrder", property='SenderName', value=SenderName)
    outdoor_delivery_order_property.add_service_property(service_id="OutdoorDeliveryOrder", property='Owner', value=owner)
    outdoor_delivery_order_property.add_service_property(service_id="OutdoorDeliveryOrder", property='Converted_RFID', 
                                                       value=converted_rfid)
    outdoor_client.report_properties(outdoor_delivery_order_property.service_property, qos=1)
    time.sleep(1)

    outdoor_car_state_property = ServicesProperties()
    outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='Number', value="CAR123456789")    
    outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='Status', value="Active")          
    outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='PositionX', value="123.45")       
    outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='PositionY', value="678.90")       
    outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='PositionZ', value="0.00")         
    outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='Latitude', value="34.052235")     
    outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='Longitude', value="-118.243683")  
    outdoor_client.report_properties(outdoor_car_state_property.service_property, qos=1)
    time.sleep(1)

def report_indoor_properties(indoor_client, i, owner="indoor_car",SenderName="6789",ReceiverName="8765"):
    """
    上报室内配送订单和车辆状态信息
    """
    converted_rfid = convert_to_hex_rfid(i)
    indoor_delivery_order_property = ServicesProperties()
    indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='Number', value="ID123456789")
    indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='Area', value="E2")
    indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='BoxState', value="In Use")
    indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='RFID', value=f"GBX0000{str(i)}")
    indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='ReceiverPhone', value=ReceiverName)
    indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='OrderNumber', value="ORD987654321")
    indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='ReceiverName', value=ReceiverName)
    indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='SenderName', value=SenderName)
    indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='Owner', value=owner)
    indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='Converted_RFID', 
                                                      value=converted_rfid)
    indoor_client.report_properties(indoor_delivery_order_property.service_property, qos=1)
    time.sleep(1)

    indoor_car_state_property = ServicesProperties()
    indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='Number', value="CAR987654321")    
    indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='Status', value="Active")            
    indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='PositionX', value="200.50")       
    indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='PositionY', value="300.75")       
    indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='PositionZ', value="1.50")         
    indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='Latitude', value="40.712776")     
    indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='Longitude', value="-74.005974")   
    indoor_client.report_properties(indoor_car_state_property.service_property, qos=1)
    time.sleep(1)

def convert_to_hex_rfid(number):
    """
    将编号转换为标准格式的RFID十六进制字符串
    """
    base_hex = "47 42 58 30 30"  # GBX00 的 ASCII 十六进制
    number_hex = ' '.join(f"{ord(char):02X}" for char in f"{number:03d}")  # 编号转换为3位ASCII十六进制
    suffix = "00 00 00 00 00 00 00 00"  # 8个0的十六进制表示
    return f"{base_hex} {number_hex} {suffix}"

def report_user_info(warehouse_client, i, user="liuhao"):
    """
    上报用户信息到仓库
    """
    converted_rfid = convert_to_hex_rfid(i)
    user_info = ServicesProperties()
    user_info.add_service_property(service_id="InWarehouse", property='Converted_RFID', 
                                 value=converted_rfid)
    user_info.add_service_property(service_id="InWarehouse", property='user', value=user)
    user_info.add_service_property(service_id="InWarehouse", property='id', 
                                 value=f"GBX{i:05d}")  # 例如：GBX00001
    warehouse_client.report_properties(user_info.service_property, qos=1)
    time.sleep(1)

def report_box_out(warehouse_client, i, user="wenbo"):
    """
    上报箱子出库信息到仓库
    """
    converted_rfid = convert_to_hex_rfid(i)
    box_out = ServicesProperties()
    box_out.add_service_property(service_id="BoxOut", property='id', value=f"GBX0000{str(i)}")
    box_out.add_service_property(service_id="BoxOut", property='user', value=user)
    box_out.add_service_property(service_id="BoxOut", property='Converted_RFID', 
                               value=converted_rfid)
    warehouse_client.report_properties(box_out.service_property, qos=1)
    time.sleep(1)

def report_input_delivery(locker_client, i, owner="Locker", number="IDL123", status="Active", 
                         cell_number="C123", cell_status="C124",ReceiverPhone=''):
    """
    上报入库配送信息到储物柜
    参数:
        locker_client: IoT客户端实例
        i: RFID序号
        owner: 所有者名称
        number: 配送编号
        status: 配送状态
        cell_number: 储物格编号
        cell_status: 储物格状态
    """
    converted_rfid = convert_to_hex_rfid(i)
    input_delivery = ServicesProperties()
    input_delivery.add_service_property(service_id="InputDelivery", property='Number', value=number)
    input_delivery.add_service_property(service_id="InputDelivery", property='Status', value=status)
    input_delivery.add_service_property(service_id="InputDelivery", property='CellNumer', value=cell_number)
    input_delivery.add_service_property(service_id="InputDelivery", property='CellStatus', value=cell_status)
    input_delivery.add_service_property(service_id="InputDelivery", property='RFID', value=f"GBX0000{str(i)}")
    input_delivery.add_service_property(service_id="InputDelivery", property='Owner', value=owner)
    input_delivery.add_service_property(service_id="InputDelivery", property='ReceiverPhone', value=ReceiverPhone)
    input_delivery.add_service_property(service_id="InputDelivery", property='Converted_RFID', 
                                      value=converted_rfid)
    locker_client.report_properties(input_delivery.service_property, qos=1)
    time.sleep(1)

def report_locker_output_delivery(locker_client, i, collect_code="2437", occupy_ratio=0.7):
    """
    上报储物柜出库配送信息
    """
    converted_rfid = convert_to_hex_rfid(i)
    output_delivery = ServicesProperties()
    # 储物柜配送需要的所有属性
    output_delivery.add_service_property(service_id="OutputDelivery", property='CollectCode', value=collect_code)
    output_delivery.add_service_property(service_id="OutputDelivery", property='OccupyRatio', value=occupy_ratio)
    output_delivery.add_service_property(service_id="OutputDelivery", property='RFID', value=f"GBX0000{str(i)}")
    output_delivery.add_service_property(service_id="OutputDelivery", property='Owner', value=collect_code)
    output_delivery.add_service_property(service_id="OutputDelivery", property='ReceiverPhone', value=collect_code)
    output_delivery.add_service_property(service_id="OutputDelivery", property='Converted_RFID', value=converted_rfid)
    locker_client.report_properties(output_delivery.service_property, qos=1)
    time.sleep(1)

def report_indoor_drone_output_delivery(indoor_client, i, ReceiverPhone="2437"):
    """
    上报室内配送出库信息
    """
    converted_rfid = convert_to_hex_rfid(i)
    output_delivery = ServicesProperties()
    # 室内配送只需要这些属性
    output_delivery.add_service_property(service_id="OutputDelivery", property='RFID', value=f"GBX0000{str(i)}")
    output_delivery.add_service_property(service_id="OutputDelivery", property='Owner', value=ReceiverPhone)
    output_delivery.add_service_property(service_id="OutputDelivery", property='ReceiverPhone', value=ReceiverPhone)
    output_delivery.add_service_property(service_id="OutputDelivery", property='Converted_RFID', value=converted_rfid)
    indoor_client.report_properties(output_delivery.service_property, qos=1)
    time.sleep(1)

def report_recycle_in_delivery(locker_client, i, owner="recycle bin", box_number=2, box_list=[1,2],RecyclerPhone=''):
    """
    上报回收入库信息到储物柜
    """
    converted_rfid = convert_to_hex_rfid(i)
    recycle_delivery = ServicesProperties()
    recycle_delivery.add_service_property(service_id="RecycleInDelivery", property='BoxNumber', value=box_number)
    recycle_delivery.add_service_property(service_id="RecycleInDelivery", property='BoxList', value=box_list)
    recycle_delivery.add_service_property(service_id="RecycleInDelivery", property='RFID', value=f"GBX0000{str(i)}")
    recycle_delivery.add_service_property(service_id="RecycleInDelivery", property='Owner', value=owner)
    recycle_delivery.add_service_property(service_id="RecycleInDelivery", property='Converted_RFID', 
                                        value=converted_rfid)
    recycle_delivery.add_service_property(service_id="RecycleInDelivery", property='RecyclerPhone', value=RecyclerPhone)
    locker_client.report_properties(recycle_delivery.service_property, qos=1)
    time.sleep(1)

def report_recycle_out_delivery(locker_client, i, owner="box_recycler", box_number=2, box_list=[1,2]):
    """
    上报回收出库信息到储物柜
    """
    converted_rfid = convert_to_hex_rfid(i)
    recycle_delivery = ServicesProperties()
    recycle_delivery.add_service_property(service_id="RecycleOutDelivery", property='BoxNumber', value=box_number)
    recycle_delivery.add_service_property(service_id="RecycleOutDelivery", property='BoxList', value=box_list)
    recycle_delivery.add_service_property(service_id="RecycleOutDelivery", property='RFID', value=f"GBX0000{str(i)}")
    recycle_delivery.add_service_property(service_id="RecycleOutDelivery", property='Owner', value=owner)
    recycle_delivery.add_service_property(service_id="RecycleOutDelivery", property='Converted_RFID', 
                                        value=converted_rfid)
    recycle_delivery.add_service_property(service_id="RecycleOutDelivery", property='Converted_RFID', 
                                        value=converted_rfid)
    locker_client.report_properties(recycle_delivery.service_property, qos=1)
    time.sleep(1)

def report_sequential_properties(warehouse_client, outdoor_client, indoor_client, drone_client, locker_client, 
                               i_drone=1, i_outdoor=2, i_indoor=3,  # 每种配送方式使用独立的箱子编号
                               enable_warehouse=True, enable_drone=True, enable_outdoor=True, 
                               enable_indoor=True, enable_locker=True):
    """
    按顺序上报各种属性
    
    参数:
        i_drone: 无人机配送箱子的RFID序号
        i_outdoor: 室外车配送箱子的RFID序号
        i_indoor: 室内车配送箱子的RFID序号
    """
    # 仓库相关操作
    if enable_warehouse:
        # 先统一注册10个箱子，从1开始
        for i in range(1, 101):  # 改为从1开始到100
            report_user_info(warehouse_client, i)
            if i % 10 == 0:  # 每注册10个箱子暂停一下，避免消息拥堵
                time.sleep(0.1)
        time.sleep(2)

        # 再根据配送需求分别出库
        if enable_drone:
            report_box_out(warehouse_client, i_drone)
            time.sleep(1)
        if enable_outdoor:
            report_box_out(warehouse_client, i_outdoor)
            time.sleep(1)
        if enable_indoor:
            report_box_out(warehouse_client, i_indoor)
            time.sleep(1)
    outdoor_SenderName='1234'
    outdoor_ReceiverName='4321'
    drone_SenderName='13671929117'
    drone_ReceiverName='13671929117'
    drone_ReceiverName2='13671929117'
    indoor_SenderName='5678'
    indoor_ReceiverName='8765'
    # 无人机、室外和室内配 - 各自使用独立的箱子编号
    if enable_drone:
        report_drone_properties(drone_client, i_drone,SenderName=drone_SenderName,ReceiverName=drone_ReceiverName,owner="Station_1")
        report_drone_properties(drone_client, i_drone,SenderName=drone_SenderName,ReceiverName=drone_ReceiverName,owner="Drone_1")
    if enable_outdoor:
        report_outdoor_properties(outdoor_client, i_outdoor,SenderName=outdoor_SenderName,ReceiverName=outdoor_ReceiverName)
    if enable_indoor:
        report_indoor_properties(indoor_client, i_indoor,SenderName=indoor_SenderName,ReceiverName=indoor_ReceiverName)
    time.sleep(2)

    # 储物柜相关操作 - 根据配送方式使用对应的箱子编号
    if enable_locker:
        if enable_drone:
            report_drone_properties(drone_client, i_drone,SenderName=drone_SenderName,ReceiverName=drone_ReceiverName,owner="station_2")
            report_input_delivery(locker_client, i_drone,ReceiverPhone=drone_ReceiverName)
            report_indoor_drone_output_delivery(drone_client, i_drone, ReceiverPhone=drone_ReceiverName)
            report_recycle_in_delivery(drone_client, i_drone, owner="recycle bin drone",RecyclerPhone=drone_ReceiverName2)
            report_recycle_out_delivery(locker_client, i_drone)
            time.sleep(2)
            
        if enable_outdoor:
            report_input_delivery(locker_client, i_outdoor,ReceiverPhone=outdoor_ReceiverName)
            report_locker_output_delivery(locker_client, i_outdoor, collect_code=outdoor_ReceiverName)
            report_recycle_in_delivery(locker_client, i_outdoor,owner="recycle bin locker", RecyclerPhone=outdoor_ReceiverName)
            report_recycle_out_delivery(locker_client, i_outdoor)
            time.sleep(2)
            
        if enable_indoor:
            report_indoor_drone_output_delivery(indoor_client, i_indoor, ReceiverPhone=indoor_ReceiverName)
            report_recycle_in_delivery(locker_client, i_indoor, owner="recycle bin locker",RecyclerPhone=drone_ReceiverName)
            report_recycle_out_delivery(locker_client, i_indoor)
            time.sleep(2)
    print("Finish")

# 使用示例:
def run():
    # 第一个设备：Warehouse
    warehouse_cfg = IoTClientConfig(
        server_ip='116.205.178.237',
        device_id='6729c1a340428521209c0759_wareHouse_test',
        secret='af2818be89bc46ef67e9',
        is_ssl=False
    )
    warehouse_client = IotClient(warehouse_cfg)
    warehouse_client.connect()
    warehouse_client.start()
    warehouse_client.subscribe(r'$oc/devices/6729c1a340428521209c0759_wareHouse_test/sys/properties/report')

    # 第二个设备：Drone
    drone_cfg = IoTClientConfig(
        server_ip='116.205.178.237',
        device_id='66dabbab1837002b28b35a64_test',
        secret='17e5ac2f6792094c8491',
        is_ssl=False
    )
    drone_client = IotClient(drone_cfg)
    drone_client.connect()
    drone_client.start()
    drone_client.subscribe(r'$oc/devices/66dabbab1837002b28b35a64_test/sys/properties/report')

    # 第三个设备：OutdoorDeliveryCar
    outdoor_car_cfg = IoTClientConfig(
        server_ip='116.205.178.237',
        device_id='66dd22421837002b28b3a3f3_OutdoorDeliveryCar_test',
        secret='3fc844f339d0b5c297f5',
        is_ssl=False
    )
    outdoor_car_client = IotClient(outdoor_car_cfg)
    outdoor_car_client.connect()
    outdoor_car_client.start()
    outdoor_car_client.subscribe(r'$oc/devices/66dd22421837002b28b3a3f3_OutdoorDeliveryCar_test/sys/properties/report')

    # 第四个设备：IndoorDeliveryCar
    indoor_car_cfg = IoTClientConfig(
        server_ip='116.205.178.237',
        device_id='66dabbc81837002b28b35a69_test',
        secret='9ee260ce5ca1aea29501',
        is_ssl=False
    )
    indoor_car_client = IotClient(indoor_car_cfg)
    indoor_car_client.connect()
    indoor_car_client.start()
    indoor_car_client.subscribe(r'$oc/devices/66dabbc81837002b28b35a69_test/sys/properties/report')

    # 第五个设备：Locker
    locker_cfg = IoTClientConfig(
        server_ip='116.205.178.237',
        device_id='66dd1bb4eff8e33e5f3f233f_test',
        secret='21a30b21a1f84538ef2f',
        is_ssl=False
    )
    locker_client = IotClient(locker_cfg)
    locker_client.connect()
    locker_client.start()
    locker_client.subscribe(r'$oc/devices/66dd1bb4eff8e33e5f3f233f_test/sys/properties/report')

    # 全部启用的情况
    report_sequential_properties(
        warehouse_client=warehouse_client,
        outdoor_client=outdoor_car_client,
        indoor_client=indoor_car_client,
        drone_client=drone_client,
        locker_client=locker_client,
        i_drone=1, i_outdoor=2, i_indoor=3,
        enable_warehouse=True, enable_drone=False, enable_outdoor=False,
        enable_indoor=False, enable_locker=False
    )
    # report_sequential_properties(
    #     warehouse_client=warehouse_client,
    #     outdoor_client=outdoor_car_client,
    #     indoor_client=indoor_car_client,
    #     drone_client=drone_client,
    #     locker_client=locker_client,
    #     i_drone=1, i_outdoor=2, i_indoor=3,
    #     enable_warehouse=False, enable_drone=True, enable_outdoor=True,
    #     enable_indoor=True, enable_locker=True
    # )
    

if __name__ == '__main__':
    run() 