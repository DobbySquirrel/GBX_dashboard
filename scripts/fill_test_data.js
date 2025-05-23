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

// 生成随机数据
const generateDroneData = (index) => {
  const now = new Date();
  return {
    device_id: "drone-001",
    event_time: now.toISOString(),
    Altitude: 100 + Math.random() * 10,
    Latitude: 22.3 + (Math.random() * 0.1),
    Longitude: 114.2 + (Math.random() * 0.1),
    State: ["飞行中", "运送中", "返航中", "待命中"][Math.floor(Math.random() * 4)],
    Time: now,
    VelocityX: Math.random() * 5 - 2.5,
    VelocityY: Math.random() * 5 - 2.5,
    VelocityZ: Math.random() * 2 - 1
  };
};

const generateIndoorCarData = (index) => {
  const now = new Date();
  return {
    device_id: "car-001",
    event_time: now.toISOString(),
    Number: "C" + (1000 + index),
    Status: ["运送中", "待命中", "充电中", "维修中"][Math.floor(Math.random() * 4)],
    PositionX: 20 + Math.random() * 10,
    PositionY: 30 + Math.random() * 15,
    PositionZ: 0
  };
};

// 填充测试数据
const fillTestData = async () => {
  try {
    console.log("开始填充测试数据...");
    
    // 填充无人机数据
    for (let i = 0; i < 20; i++) {
      const droneData = generateDroneData(i);
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
      console.log(`已插入无人机数据 #${i+1}`);
      
      // 等待一小段时间
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // 填充室内车数据
    for (let i = 0; i < 20; i++) {
      const carData = generateIndoorCarData(i);
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
      console.log(`已插入室内车数据 #${i+1}`);
      
      // 等待一小段时间
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    console.log("测试数据填充完成！");
  } catch (error) {
    console.error("填充测试数据失败:", error);
  } finally {
    // 关闭连接池
    await pool.end();
  }
};

// 执行填充
fillTestData(); 