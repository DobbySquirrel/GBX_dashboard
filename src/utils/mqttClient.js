import mqtt from 'mqtt/dist/mqtt.min.js';
import { ref } from 'vue';

const messages = ref([]);

// 订阅topic名称
var topic = "RecycleInBox";
// 接入凭证键值，可通过环境变量预置
var accessKey = 'MImHc8W7';
// 接入凭证密钥，可通过环境变量预置
var accessCode = "1LxO05huIQDlUjpCSAqUwe4tphoizwx0";
// mqtt接入地址
var mqttHost = "0458774161.st1.iotda-app.cn-south-1.myhuaweicloud.com";
// mqtt接入端口
var mqttPort = 8883;
// 实例Id
var instanceId = "220e6462-38bf-48b9-84e1-c490265d5ae6";
// mqtt client id
var clientId = "username";
// mqtt 客户端
var client = null;

connectWithRetry();

async function connectWithRetry() {
    // 退避重试，从1s依次x2，直到20s。
    var duration = 1000;
    var maxDuration = 20000;
    var success = connect(topic);
    var times = 0;
    while (!success) {
       await sleep(duration)
       if (duration < maxDuration) {
          duration *= 2
       }
       times++
       console.log('connect mqtt broker retry. times: ' + times)
        if (client == null) {
            connect(topic)
            continue
        }
       client.end(true, function() {
            connect(topic)
        });
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(() => resolve(), ms))
}

function connect(topic) {
    try {
        client = mqtt.connect(getClientOptions())
        if (client == null) {
            return false
        }
        client.on('connect', connectCallBack)
        client.subscribe(topic, subscribeCallBack)
        client.on('message', messageCallBack)
        client.on('error', clientErrorCallBack)
        client.on('close', closeCallBack)
        return true
    } catch (error) {
        console.log('connect to mqtt broker failed. err ' + error)
    }
    return false
}

function getClientOptions() {
    var timestamp = Math.round(new Date);
    const username = 'accessKey=' + accessKey + '|timestamp=' + timestamp + '|instanceId=' + instanceId;
    var options = {
        host: mqttHost,
        port: mqttPort,
        connectTimeout: 4000,
        clientId: clientId,
        protocol: 'mqtts',
        keepalive: 120,
        username: username,
        password: accessCode,
        rejectUnauthorized: false,
        secureProtocol: 'TLSv1_2_method'
    };
    return options;
};

function connectCallBack() {
    console.log('connect mqtt server success');
};

function subscribeCallBack(err, granted) {
    if (err != null || granted[0].qos === 128) {
        console.log('subscribe topic failed. granted: ' + granted[0].qos)
        return
    }
    console.log('subscribe topic success. granted: ' + granted[0].qos);
};

function clientErrorCallBack(err) {
    console.log('mqtt client error ' + err);
};

function messageCallBack(topic, message) {
    console.log('receive message ' + message);
    messages.value.push(message.toString());
};

function closeCallBack() {
    console.log('Disconnected from mqtt broker')
    client.end(true, function() {
        console.log('close connection');
        connectWithRetry();
     });
} 