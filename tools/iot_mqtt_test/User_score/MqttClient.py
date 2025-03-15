import os
import ssl
import threading
import time
import traceback
import secrets
from ClientConf import ClientConf
import paho.mqtt.client as mqtt
import json
import csv
from download_upload import download_from_obs, upload_to_obs

class MqttClient:
    def __init__(self, client_conf: ClientConf):
        self.__host = client_conf.host
        self.__port = client_conf.port
        self.__access_key = client_conf.access_key
        self.__access_code = client_conf.access_code
        self.__topic = client_conf.topic
        self.__instance_id = client_conf.instance_id
        self.__qos = client_conf.qos
        self.__paho_client: Optional[mqtt.Client] = None
        self.__connect_result_code = -1
        self.__default_backoff = 1000
        self.__retry_times = 0
        self.__min_backoff = 1 * 1000  # 1s
        self.__max_backoff = 30 * 1000  # 30s

    def connect(self):
        self.__valid_params()
        rc = self.__connect()
        while rc != 0:
            # 退避重连
            low_bound = int(self.__default_backoff * 0.8)
            high_bound = int(self.__default_backoff * 1.0)
            random_backoff = secrets.randbelow(high_bound - low_bound)
            backoff_with_jitter = int(pow(2, self.__retry_times)) * (random_backoff + low_bound)
            wait_time_ms = self.__max_backoff if (self.__min_backoff + backoff_with_jitter) > self.__max_backoff else (
                    self.__min_backoff + backoff_with_jitter)
            wait_time_s = round(wait_time_ms / 1000, 2)
            print("client will try to reconnect after " + str(wait_time_s) + " s")
            time.sleep(wait_time_s)
            self.__retry_times += 1
            self.close()  # 释放之前的connection
            rc = self.__connect()
            # rc为0表示建链成功，其它表示连接不成功
            if rc != 0:
                print("connect with result code: " + str(rc))
                if rc == 134:
                    print("connect failed with bad username or password, "
                          "reconnection will not be performed")
                    pass
        return rc
    def __connect(self):
        try:
            timestamp = self.current_time_millis()
            user_name = "accessKey=" + self.__access_key + "|timestamp=" + timestamp
            if self.__instance_id:
                user_name = user_name + "|instanceId=" + self.__instance_id
            pass_word = self.__access_code
            self.__paho_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "mqttClient")
            # 关闭自动重试， 采用手动重试的式刷新时间戳
            self.__paho_client._reconnect_on_failure = False
            # 设置回调函数
            self._set_callback()
            # topic放在userdata中，调函数直接拿topic订阅
            self.__paho_client.user_data_set(self.__topic)
            self.__paho_client.username_pw_set(user_name, pass_word)
            # 当前mqtt broker仅支持TLS1.2
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            # 不校验服务端证书
            context.verify_mode = ssl.CERT_NONE
            context.check_hostname = False
            self.__paho_client.tls_set_context(context)
            rc = self.__paho_client.connect(self.__host, self.__port)
            self.__connect_result_code = rc
            if rc == 0:
                threading.Thread(target=self.__paho_client.loop_forever, args=(1, False), name="MqttThread").start()
            # 等待建链
            time.sleep(1)
        except Exception as e:
            self.__connect_result_code = -1
            print("Mqtt connection error. traceback: " + traceback.format_exc())
        if self.__paho_client.is_connected():
            return 0
        else:
            return self.__connect_result_code
    def __valid_params(self):
        assert self.__access_key is not None
        assert self.__access_code is not None
        assert self.__topic is not None

    @staticmethod
    def current_time_millis():
        return str(int(round(time.time() * 1000)))
    def _set_callback(self):
        # 当平台响应连接请求时，执行self._on_connect()
        self.__paho_client.on_connect = self._on_connect
        # 当与平台断开连接时，执行self._on_disconnect()
        self.__paho_client.on_disconnect = self._on_disconnect
        # 当订阅topic时，执行self._on_subscribe
        self.__paho_client.on_subscribe = self._on_subscribe
        # 当接收到一个原始消息时，执行self._on_message()
        self.__paho_client.on_message = self._on_message
    def _on_connect(self, client, userdata, flags, rc: mqtt.ReasonCode, properties):
        if rc == 0:
            print("Connected to Mqtt Broker! topic " + self.__topic)
            client.subscribe(userdata, 1)
        else:
            # 只有当用户名或密码错误，才不进行自动重连。
            # 如果这里不使用disconnect()方法，那么loop_forever会一直进行重连。
            if rc == 134:
                self.__paho_client.disconnect()
            print("Failed to connect. return code :" + str(rc.value) + ", reason" + rc.getName())
    def _on_subscribe(self, client, userdata, mid, granted_qos, properties):
        print("Subscribed: " + str(mid) + " " + str(granted_qos) + " topic: " + self.__topic)
    def _on_message(self, client, userdata, message: mqtt.MQTTMessage):
        try:
            from send_message import send_sms
            import json
            
            payload = json.loads(message.payload.decode())
            services = payload['notify_data']['body']['services']
            
            recycle_template_id = "a61c9c47545841228c7f127c3b447309"
            output_template_id = "a61c9c47545841228c7f127c3b447309"
            
            rfid_phone_map = self.load_rfid_phone_map()
            

            for service in services:
                service_id = service['service_id']
                print(f"Service ID: {service_id}")
                
                if service_id == 'InputDelivery':
                    properties = service['properties']
                    receiver_phone = properties.get('ReceiverPhone')
                    receiver_RFID = properties.get('RFID')
                    print(f"ReceiverPhone: {receiver_phone}")
                    print(f"ReceiverRFID: {receiver_RFID}")
                    
                    if receiver_RFID:
                        rfid_phone_map[receiver_RFID] = {'receiver_phone': receiver_phone}
                    
                    if receiver_phone:
                        formatted_phone = f"+86{receiver_phone}"
                        template_param = f'["123"]'
                        response = send_sms(output_template_id, formatted_phone, template_param)
                        print("接收人短信发送结果:", response)
                
                elif service_id == 'RecycleInDelivery':
                    properties = service['properties']
                    recycler_phone = properties.get('RecyclerPhone')
                    RFID = properties.get('RFID')
                    print(f"RecyclerPhone: {recycler_phone}")
                    print(f"RFID: {RFID}")
                    scores = self.load_scores()
                    if RFID in rfid_phone_map:
                        stored_receiver_phone = rfid_phone_map[RFID].get('receiver_phone')
                        if stored_receiver_phone and stored_receiver_phone != recycler_phone:
                            formatted_receiver_phone = f"+86{stored_receiver_phone}"
                            formatted_recycler_phone = f"+86{recycler_phone}"
                            scores[recycler_phone] = scores.get(recycler_phone, 0) + 10
                            scores[stored_receiver_phone] = scores.get(stored_receiver_phone, 0) - 50
                            template_param_receiver = f'["10{scores.get(stored_receiver_phone, 0)}"]'
                            template_param_recycler = f'["50{scores.get(recycler_phone, 0)}"]'
                            response_receiver = send_sms(output_template_id, formatted_receiver_phone, template_param_receiver)
                            response_recycler = send_sms(recycle_template_id, formatted_recycler_phone, template_param_recycler)
                            print("接收信发送结果:", response_receiver)
                            print("回收人短信发送结果:", response_recycler)
                        elif recycler_phone:
                            formatted_recycler_phone = f"+86{recycler_phone}"
                            template_param = f'["10{scores.get(recycler_phone, 0)}"]'
                            scores[recycler_phone] = scores.get(recycler_phone, 0) + 10
                            response = send_sms(recycle_template_id, formatted_recycler_phone, template_param)
                            print("回收人短信发送结果:", response)
                        self.save_scores(scores)

            self.save_rfid_phone_map(rfid_phone_map)
            
                
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
        except KeyError as e:
            print(f"键值获取错误: {e}")
        except Exception as e:
            print(f"处理消息时发生错误: {e}")

    def load_scores(self):
        scores = {}
        object_key = "User_Score/Score_Record.csv"
        file_path = "scores.csv"
        
        # 尝试从OBS下载文件
        if not os.path.exists(file_path):
            download_success = download_from_obs(object_key, file_path)
            if not download_success:
                print("无法从OBS下载文件，将创建新的分数记录")
        
        # 读取本地文件
        if os.path.exists(file_path):
            with open(file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    scores[row['phone']] = int(row['score'])
        return scores

    def save_scores(self, scores):
        object_key = "User_Score/Score_Record.csv"
        file_path = "scores.csv"
        
        # 保存到本地文件
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['phone', 'score'])
            writer.writeheader()
            for phone, score in scores.items():
                writer.writerow({'phone': phone, 'score': score})
        
        # 上传到OBS
        upload_success = upload_to_obs(object_key, file_path)
        if not upload_success:
            print("上传分数记录到OBS失败")

    def load_rfid_phone_map(self):
        if os.path.exists('rfid_phone_map.json'):
            with open('rfid_phone_map.json', 'r') as file:
                return json.load(file)
        return {}

    def save_rfid_phone_map(self, rfid_phone_map):
        with open('rfid_phone_map.json', 'w') as file:
            json.dump(rfid_phone_map, file)

    def _on_disconnect(self, client, userdata, flags, rc, properties):
        print("Disconnect to Mqtt Broker. topic: " + self.__topic)
        # 断链后将客户端主动关闭，手动重连刷新时间戳
        try:
            self.__paho_client.disconnect()
        except Exception as e:
            print("Mqtt connection error. traceback: " + traceback.format_exc())
        self.connect()
    def close(self):
        if self.__paho_client is not None and self.__paho_client.is_connected():
            try:
                self.__paho_client.disconnect()
                print("Mqtt connection close")
            except Exception as e:
                print("paho client disconnect failed. exception: " + str(e))
        else:
            pass
