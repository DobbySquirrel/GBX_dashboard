import { createServer } from 'http';
import mysql from 'mysql2/promise';
import dotenv from 'dotenv';
import { setupSocketIO } from './Socket.js';
import { setupApiServer } from './api_db.js';

// 加载环境变量
dotenv.config();

const port = process.env.PORT || 3000;

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

// 设置 API 服务
const app = setupApiServer(pool, dbConfig);

// 创建 HTTP 服务器
const httpServer = createServer(app);

// 设置 Socket.IO 服务
setupSocketIO(httpServer, pool);

// 启动服务器
httpServer.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
});