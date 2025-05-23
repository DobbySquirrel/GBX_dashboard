import mysql from 'mysql2/promise';
import dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

// 数据库连接配置
const dbConfig = {
  host: process.env.DB_HOST || "113.45.11.133",
  port: parseInt(process.env.DB_PORT || "3306"),
  user: process.env.DB_USER || "Gbx",
  password: process.env.DB_PASSWORD || "Gbx_123123",
  database: process.env.DB_NAME || "gbx",
  charset: process.env.DB_CHARSET || "utf8"
};

// 创建数据库连接池
const pool = mysql.createPool(dbConfig);

// 定义原始路径点
const droneRoute = [
  [356, 370], [370, 380], [385, 390], [400, 400], 
  [415, 410], [428, 420], [420, 430], [410, 440],
  [390, 450], [370, 460], [356, 450], [360, 430],
  [365, 410], [370, 390], [360, 380]
];

const indoorCarRoute = [
  [230, 420], [260, 440], [290, 460],
  [320, 480], [350, 500], [380, 520], [410, 540],
  [440, 560], [470, 580], [440, 600], [410, 620],
  [380, 600], [350, 580], [320, 560], [290, 540],
  [260, 520], [230, 500], [200, 480], [230, 460]
];

// 路径索引
let droneRouteIndex = 0;
let indoorCarRouteIndex = 0;

// 生成基于路径点的数据
const generateDroneData = () => {
  const now = new Date();
  const currentPoint = droneRoute[droneRouteIndex];
  const nextIndex = (droneRouteIndex + 1) % droneRoute.length;
  const nextPoint = droneRoute[nextIndex];
  
  // 计算速度向量 (简单的差分)
  const velocityX = nextPoint[0] - currentPoint[0];
  const velocityY = nextPoint[1] - currentPoint[1];
  
  // 更新索引
  droneRouteIndex = nextIndex;
  
  // 将地图坐标转换为经纬度格式 (反向转换)
  // 假设 Longitude = (x - 300) / 100, Latitude = (y - 300) / 100
  const longitude = (currentPoint[0] - 300) / 100;
  const latitude = (currentPoint[1] - 300) / 100;
  
  return {
    device_id: "drone-001",
    event_time: now.toISOString(),
    Altitude: 100 + Math.random() * 5,
    Latitude: latitude,
    Longitude: longitude,
    State: ["飞行中", "运送中", "返航中", "待命中"][Math.floor(Math.random() * 4)],
    Time: now,
    VelocityX: velocityX / 10,
    VelocityY: velocityY / 10,
    VelocityZ: Math.random() * 0.5 - 0.25
  };
};

const generateIndoorCarData = () => {
  const now = new Date();
  const currentPoint = indoorCarRoute[indoorCarRouteIndex];
  
  // 更新索引
  indoorCarRouteIndex = (indoorCarRouteIndex + 1) % indoorCarRoute.length;
  
  // 将地图坐标转换为位置格式 (反向转换)
  // 假设 PositionX = (x - 200) / 10, PositionY = (y - 400) / 10
  const positionX = (currentPoint[0] - 200) / 10;
  const positionY = (currentPoint[1] - 400) / 10;
  
  return {
    device_id: "car-001",
    event_time: now.toISOString(),
    Number: "C" + (1000 + Math.floor(Math.random() * 10)),
    Status: ["运送中", "待命中", "充电中", "维修中"][Math.floor(Math.random() * 4)],
    PositionX: positionX,
    PositionY: positionY,
    PositionZ: 0
  };
};

// 持续生成测试数据
const generateContinuousData = async () => {
  try {
    console.log("开始持续生成测试数据...");
    console.log("按 Ctrl+C 停止");
    
    // 每3秒生成一次数据
    setInterval(async () => {
      try {
        // 生成并插入无人机数据
        const droneData = generateDroneData();
        await pool.query(
          `INSERT INTO DeliveryDrone_Property_State 
           (device_id, event_time, Altitude, Latitude, Longitude, State, Time, VelocityX, VelocityY, VelocityZ) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
          [
            droneData.device_id,
            droneData.event_time,
            droneData.Altitude,
            droneData.Latitude,
            droneData.Longitude,
            droneData.State,
            droneData.Time,
            droneData.VelocityX,
            droneData.VelocityY,
            droneData.VelocityZ
          ]
        );
        console.log(`已插入新的无人机数据 - ${new Date().toLocaleTimeString()} - 位置: (${droneData.Longitude.toFixed(4)}, ${droneData.Latitude.toFixed(4)})`);
        
        // 生成并插入室内车数据
        const carData = generateIndoorCarData();
        await pool.query(
          `INSERT INTO IndoorDeliveryCar_Property_State 
           (device_id, event_time, Number, Status, PositionX, PositionY, PositionZ) 
           VALUES (?, ?, ?, ?, ?, ?, ?)`,
          [
            carData.device_id,
            carData.event_time,
            carData.Number,
            carData.Status,
            carData.PositionX,
            carData.PositionY,
            carData.PositionZ
          ]
        );
        console.log(`已插入新的室内车数据 - ${new Date().toLocaleTimeString()} - 位置: (${carData.PositionX.toFixed(2)}, ${carData.PositionY.toFixed(2)})`);
      } catch (error) {
        console.error("插入数据失败:", error);
      }
    }, 500);
  } catch (error) {
    console.error("持续生成数据失败:", error);
    await pool.end();
    process.exit(1);
  }
};

// 执行持续生成
generateContinuousData();

// 处理程序退出
process.on('SIGINT', async () => {
  console.log("正在停止数据生成...");
  await pool.end();
  process.exit(0);
}); 