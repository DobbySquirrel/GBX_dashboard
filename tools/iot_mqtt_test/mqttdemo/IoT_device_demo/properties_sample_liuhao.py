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

def report_drone_properties(iot_client):

    # delivery_time = datetime(2024, 9, 8, 9, 45, 0)
    # DroneDeliveryOrder properties
    drone_delivery_order_property = ServicesProperties()
    drone_delivery_order_property.add_service_property(service_id="UserInfo", property='id', value="GBX00001")
    drone_delivery_order_property.add_service_property(service_id="UserInfo", property='user', value="liuhao")
    # drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='ReceiverName', value="王明")
    # drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='ReceiverPhone', value="+1234567890")
    # drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='ReceiverAddress', value="学生宿舍")
    # drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='SenderName', value="Jane Smith")
    # drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='SenderAddress', value="心连心餐厅")
    # drone_delivery_order_property.add_service_property(service_id="DroneDeliveryOrder", property='Time', value=delivery_time.strftime('%Y-%m-%d %H:%M:%S'))
    #     # Report DroneDeliveryOrder properties
    iot_client.report_properties(drone_delivery_order_property.service_property, qos=1)
    #     # DroneState properties
    # path = [{
    #     'lng': 113.48925478242874,
    #     'lat': 22.89512780142586
    # }, {
    #     'lng': 113.48921937326168,
    #     'lat': 22.895053481581378
    # }, {
    #     'lng': 113.48940577165494,
    #     'lat': 22.89495360290252
    # }, {
    #     'lng': 113.48927524138237,
    #     'lat': 22.894364685880905
    # }, {
    #     'lng': 113.4897423602474,
    #     'lat': 22.893990138528295
    # }, {
    #     'lng': 113.49078439463864,
    #     'lat': 22.893174454008136
    # }, {
    #     'lng': 113.49049693687553,
    #     'lat': 22.892808226691788
    # }, {
    #     'lng': 113.49097603323875,
    #     'lat': 22.892597368255732
    # }, {
    #     'lng': 113.49120060961617,
    #     'lat': 22.892464194228914
    # }, {
    #     'lng': 113.49182044041784,
    #     'lat': 22.892156228785538
    # }, {
    #     'lng': 113.4922156948421,
    #     'lat': 22.891948143626255
    # }]

    # # Initial parameters
    # timestamp = datetime(2024, 9, 8, 10, 30, 0)  # Start time
    # takeoff_time = len(path) // 3  # Duration for takeoff
    # cruise_time = len(path) // 3  # Duration for cruising
    # landing_time = len(path) - takeoff_time - cruise_time  # Duration for landing

    # initial_altitude = 0.0  # Starting altitude
    # max_altitude = 150.0  # Maximum altitude during flight
    # velocity_x = 12.5  # Example velocity
    # velocity_y = 8.7
    # velocity_z = 0.0

    # # Iterate through the path and generate drone state properties
    # for i, point in enumerate(path):
    #     # Determine state (Takeoff, In Flight, Landing)
    #     if i < takeoff_time:
    #         altitude = initial_altitude + (max_altitude / takeoff_time) * i  # Gradually increase altitude
    #         state = "Takeoff"
    #     elif i < takeoff_time + cruise_time:
    #         altitude = max_altitude  # Maintain max altitude during cruise
    #         state = "In Flight"
    #     else:
    #         altitude = max_altitude - (max_altitude / landing_time) * (i - takeoff_time - cruise_time)  # Gradually decrease altitude
    #         state = "Landing"
        
    #     # Adding drone state properties
    #     drone_state_property = ServicesProperties()
    #     drone_state_property.add_service_property(service_id="DroneState", property='Altitude', value=str(round(altitude, 1)))
    #     drone_state_property.add_service_property(service_id="DroneState", property='Latitude', value=str(point['lat']))
    #     drone_state_property.add_service_property(service_id="DroneState", property='Longitude', value=str(point['lng']))
    #     drone_state_property.add_service_property(service_id="DroneState", property='State', value=state)
    #     drone_state_property.add_service_property(service_id="DroneState", property='Time', value=timestamp.strftime('%Y-%m-%d %H:%M:%S'))
    #     drone_state_property.add_service_property(service_id="DroneState", property='VelocityX', value=str(velocity_x))
    #     drone_state_property.add_service_property(service_id="DroneState", property='VelocityY', value=str(velocity_y))
    #     drone_state_property.add_service_property(service_id="DroneState", property='VelocityZ', value=str(velocity_z))
    #     time.sleep(2)
    #     # Report the properties (simulated)
    #     iot_client.report_properties(drone_state_property.service_property, qos=1)
        
    #     # # Clear the service_property list after each report
    #     # drone_state_property.service_property.clear()
        
    #     # Adjust timestamp and velocity for the next point
    #     timestamp += timedelta(minutes=1)  # Increment time by 2 minutes
    #     velocity_x += 0.1  # Adjust velocities slightly
    #     velocity_y += 0.1

# def report_outdoor_car_properties(iot_client):
#     # Initialize service property objects and IoT client
#     outdoor_delivery_order_property_1 = ServicesProperties()
#     outdoor_delivery_order_property_2 = ServicesProperties()
#     outdoor_car_state_property = ServicesProperties()

#     # Define path for car's positions (latitude and longitude)
#     car_path = [{
#         'lng': 113.48925478242874,
#         'lat': 22.89512780142586
#     }, {
#         'lng': 113.48921937326168,
#         'lat': 22.895053481581378
#     }, {
#         'lng': 113.48940577165494,
#         'lat': 22.89495360290252
#     }, {
#         'lng': 113.48927524138237,
#         'lat': 22.894364685880905
#     }]

#     # Initialize position values
#     position_x = 0.0  # Starting position X
#     position_y = 0.0  # Starting position Y
#     position_z = 0.0  # Static Z value for this simulation
#     position_increment = 0.1  # Increment to simulate movement

#     # Delivery orders for the same car
#     outdoor_delivery_order_property_1.add_service_property(service_id="OutdoorDeliveryOrder", property='Number', value="Outdoor_car1")
#     outdoor_delivery_order_property_1.add_service_property(service_id="OutdoorDeliveryOrder", property='Area', value="W")
#     outdoor_delivery_order_property_1.add_service_property(service_id="OutdoorDeliveryOrder", property='BoxState', value="In Transit")
#     outdoor_delivery_order_property_1.add_service_property(service_id="OutdoorDeliveryOrder", property='BoxRFID', value="RFID987654322")
#     outdoor_delivery_order_property_1.add_service_property(service_id="OutdoorDeliveryOrder", property='Path', value="Route 1")
#     outdoor_delivery_order_property_1.add_service_property(service_id="OutdoorDeliveryOrder", property='User', value="宋辉")
#     iot_client.report_properties(outdoor_delivery_order_property_1.service_property, qos=1)
#     # Second order for the same outdoor car
#     outdoor_delivery_order_property_2.add_service_property(service_id="OutdoorDeliveryOrder", property='Number', value="Outdoor_car1")
#     outdoor_delivery_order_property_2.add_service_property(service_id="OutdoorDeliveryOrder", property='Area', value="W")
#     outdoor_delivery_order_property_2.add_service_property(service_id="OutdoorDeliveryOrder", property='BoxState', value="In Transit")
#     outdoor_delivery_order_property_2.add_service_property(service_id="OutdoorDeliveryOrder", property='BoxRFID', value="RFID987654323")
#     outdoor_delivery_order_property_2.add_service_property(service_id="OutdoorDeliveryOrder", property='Path', value="Route 1")
#     outdoor_delivery_order_property_2.add_service_property(service_id="OutdoorDeliveryOrder", property='User', value="王强")
#     time.sleep(2)
#     iot_client.report_properties(outdoor_delivery_order_property_2.service_property, qos=1)
#     # Iterate through the path and update OutdoorCarState for each point, simulating movement
#     for i, point in enumerate(car_path):
#         outdoor_car_state_property = ServicesProperties()
        
#         # Add properties to the car state
#         outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='Number', value="Ourdoor_car1")
#         outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='Status', value="Active")
#         outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='PositionX', value=str(round(position_x, 1)))
#         outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='PositionY', value=str(round(position_y, 1)))
#         outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='PositionZ', value=str(position_z))  # Static Z value
#         outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='Latitude', value=str(point['lat']))
#         outdoor_car_state_property.add_service_property(service_id="OutdoorCarState", property='Longitude', value=str(point['lng']))
#         time.sleep(1)
#         # Report the car state at each position (simulated)
#         iot_client.report_properties(outdoor_car_state_property.service_property, qos=1)

#         # Increment position to simulate movement
#         position_x += position_increment  # Increase position X slightly
#         position_y += position_increment  # Increase position Y slightly

#     # Report the delivery order properties (simulated)
    
# def report_indoor_delivery_car_properties(iot_client):
#     # Initial position values
#     position_x = 0.0
#     position_y = 0.0
#     position_z = 0.0
#     position_increment = 0.1  # Increment step for continuous change

#     # IndoorDeliveryOrder properties
#     indoor_delivery_order_property = ServicesProperties()
#     indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='Number', value="Indoor_car1")
#     indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='Area', value="Building B")
#     indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='BoxState', value="In Transit")
#     indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='BoxRFID', value="RFID987654324")
#     indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='Path', value="W1")
#     indoor_delivery_order_property.add_service_property(service_id="IndoorDeliveryOrder", property='User', value="刘鑫")

#     # Report IndoorDeliveryOrder properties
#     time.sleep(2)
#     iot_client.report_properties(indoor_delivery_order_property.service_property, qos=1)

#     # Simulate continuous position changes and report multiple times
#     for i in range(5):  # Example: report 5 continuous position updates
#         # IndoorCarState properties with continuously changing X and Y positions
#         indoor_car_state_property = ServicesProperties()
#         indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='Number', value="IDC987")
#         indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='Status', value="Active")
#         indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='PositionX', value=str(round(position_x, 1)))
#         indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='PositionY', value=str(round(position_y, 1)))
#         indoor_car_state_property.add_service_property(service_id="IndoorCarState", property='PositionZ', value=str(position_z))  # Static Z value
#         time.sleep(2)
#         # Report IndoorCarState properties
#         iot_client.report_properties(indoor_car_state_property.service_property, qos=1)

#         # Increment the position values for the next report
#         position_x += position_increment
#         position_y += position_increment



# def report_delivery_locker_properties(iot_client):
#     # List of CellNumbers and statuses for multiple cells
#     cell_numbers = ["C123", "C124", "C125", "C126"]
#     cell_statuses = ["Unlocked", "Locked", "Unlocked", "Locked"]
    
#     # Loop through each cell and report InputDelivery properties
#     for i in range(len(cell_numbers)):
#         input_delivery_property = ServicesProperties()
#         input_delivery_property.add_service_property(service_id="InputDelivery", property='Number', value="IDL123")
#         input_delivery_property.add_service_property(service_id="InputDelivery", property='Status', value="Available")
#         input_delivery_property.add_service_property(service_id="InputDelivery", property='CellNumer', value=cell_numbers[i])
#         input_delivery_property.add_service_property(service_id="InputDelivery", property='CellStatus', value=cell_statuses[i])
#         time.sleep(2)
#         # Report each InputDelivery property for the cells
#         iot_client.report_properties(input_delivery_property.service_property, qos=1)

#     # List of CollectCodes and OccupyRatios for OutputDelivery
#     output_collect_codes = ["COL456", "COL457", "COL458", "COL459"]
#     output_occupy_ratios = [0.5, 0.7, 0.4, 0.9]

#     # Loop through each OutputDelivery and report properties
#     for i in range(len(output_collect_codes)):
#         output_delivery_property = ServicesProperties()
#         output_delivery_property.add_service_property(service_id="OutputDelivery", property='CollectCode', value=output_collect_codes[i])
#         output_delivery_property.add_service_property(service_id="OutputDelivery", property='OccupyRatio', value=str(output_occupy_ratios[i]))
#         time.sleep(2)
#         # Report each OutputDelivery property
#         iot_client.report_properties(output_delivery_property.service_property, qos=1)

#     # RecycleDelivery properties: BoxNumber表示回收柜中箱子的个数
#     recycle_box_lists = [[1, 2], [1, 3], [2, 4], [3, 6]]  # 不同回收柜内的箱子编号列表

#     for i in range(len(recycle_box_lists)):
#         recycle_delivery_property = ServicesProperties()
#         # BoxNumber 直接用 BoxList 的长度表示
#         recycle_delivery_property.add_service_property(service_id="RecycleDelivery", property='BoxNumber', value=str(len(recycle_box_lists[i])))
#         recycle_delivery_property.add_service_property(service_id="RecycleDelivery", property='BoxList', value=recycle_box_lists[i])
#         time.sleep(2)
#         iot_client.report_properties(recycle_delivery_property.service_property, qos=1)


def run():
    # 第一个设备：DroneState 和 DroneDeliveryOrder
    drone_cfg = IoTClientConfig(server_ip='116.205.178.237',
                                device_id='6729c1a340428521209c0759_wareHouse_test',
                                secret='9d972ca3bef9285d20dfb9b43a3a7925', is_ssl=False)
    drone_client = IotClient(drone_cfg)
    drone_client.connect()
    drone_client.start()
    drone_client.subscribe(r'$oc/devices/' + '6729c1a340428521209c0759_wareHouse_test'+ r'/sys/properties/report')
    # 第二个设备：OutdoorDeliveryCar
    # outdoor_car_cfg = IoTClientConfig(server_ip='116.205.178.237',
    #                                   device_id='66dd22421837002b28b3a3f3_OutdoorDeliveryCar_test',
    #                                   secret='2801bae19024ed3856c64f2e57d38957', is_ssl=False)
    # outdoor_car_client = IotClient(outdoor_car_cfg)
    # outdoor_car_client.connect()
    # outdoor_car_client.start()
    # outdoor_car_client.subscribe(r'$oc/devices/' + '66dd22421837002b28b3a3f3_OutdoorDeliveryCar_test'+ r'/sys/properties/report')

    # # 第三个设备：IndoorDeliveryCar
    # indoor_delivery_car_cfg = IoTClientConfig(server_ip='116.205.178.237',
    #                                           device_id='66dabbc81837002b28b35a69_test',
    #                                           secret='f697040ef7e291386103', is_ssl=False)
    # indoor_delivery_car_client = IotClient(indoor_delivery_car_cfg)
    # indoor_delivery_car_client.connect()
    # indoor_delivery_car_client.start()
    # indoor_delivery_car_client.subscribe(r'$oc/devices/' + '66dabbc81837002b28b35a69_test'+ r'/sys/properties/report')

    # # 第四个设备：DeliveryLocker
    # locker_cfg = IoTClientConfig(server_ip='116.205.178.237',
    #                              device_id='66dd1bb4eff8e33e5f3f233f_test',
    #                              secret='91a1f51ea7c79e183190d0c39e2507f8', is_ssl=False)
    # locker_client = IotClient(locker_cfg)
    # locker_client.connect()
    # locker_client.start()
    # locker_client.subscribe(r'$oc/devices/' + '66dd1bb4eff8e33e5f3f233f_test'+ r'/sys/properties/report')

    # 定时上报属性
    while True:
        # 上报 DroneState 和 DroneDeliveryOrder 的属性
        report_drone_properties(drone_client)
        
        # # 上报 OutdoorDeliveryCar 的属性
        # report_outdoor_car_properties(outdoor_car_client)
        
        # # 上报 DeliveryLocker 的属性
        # report_delivery_locker_properties(locker_client)
        
        # # 上报 IndoorDeliveryCar 的属性
        # report_indoor_delivery_car_properties(indoor_delivery_car_client)
        
        break
        time.sleep(5)

if __name__ == '__main__':
    run()
