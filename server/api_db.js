import express from 'express';
import cors from 'cors';

// 创建并配置 API 服务
export function setupApiServer(pool, dbConfig) {
  const app = express();

  // 中间件
  app.use(cors({
    origin: ['http://localhost:5173', 'http://localhost:8080'],
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true
  }));
  app.use(express.json());

  // 测试数据库连接
  app.get('/api/test', async (req, res) => {
    try {
      const connection = await pool.getConnection();
      connection.release();
      res.json({ message: '数据库连接成功' });
    } catch (error) {
      console.error('数据库连接失败:', error);
      res.status(500).json({ error: '数据库连接失败', details: error.message });
    }
  });

  // 获取所有表名
  app.get('/api/tables', async (req, res) => {
    try {
      const [rows] = await pool.query(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = ?",
        [dbConfig.database]
      );

      // 添加调试信息
      console.log('数据库返回的表数据:', rows);

      // 检查实际的列名
      if (rows.length > 0) {
        const firstRow = rows[0];
        const columnName = Object.keys(firstRow).find(key =>
          key.toLowerCase() === 'table_name' ||
          key === 'TABLE_NAME'
        );

        if (columnName) {
          const tables = rows.map(row => row[columnName]);
          console.log('处理后的表名列表:', tables);
          return res.json(tables);
        }
      }

      // 如果无法确定列名，直接返回原始数据
      res.json(rows);
    } catch (error) {
      console.error('获取表列表失败:', error);
      res.status(500).json({ error: '获取表列表失败', details: error.message });
    }
  });

  // 获取表结构
  app.get('/api/tables/:tableName/structure', async (req, res) => {
    const { tableName } = req.params;
    
    try {
      const [columns] = await pool.query(
        `SELECT column_name, column_type, is_nullable, column_key, column_default, extra 
         FROM information_schema.columns 
         WHERE table_schema = ? AND table_name = ? 
         ORDER BY ordinal_position`, 
        [dbConfig.database, tableName]
      );
      
      res.json(columns);
    } catch (error) {
      console.error(`获取表 ${tableName} 结构失败:`, error);
      res.status(500).json({ error: `获取表 ${tableName} 结构失败`, details: error.message });
    }
  });

  // 获取表数据
  app.get('/api/tables/:tableName', async (req, res) => {
    const { tableName } = req.params;
    const limit = parseInt(req.query.limit || '1000');
    const offset = parseInt(req.query.offset || '0');
    
    console.log(`请求表数据: ${tableName}, limit: ${limit}, offset: ${offset}`);
    
    try {
      // 使用参数化查询防止SQL注入
      const [rows] = await pool.query(`SELECT * FROM \`${tableName}\` LIMIT ? OFFSET ?`, [limit, offset]);
      
      // 获取总记录数
      const [countResult] = await pool.query(`SELECT COUNT(*) as total FROM \`${tableName}\``);
      
      const total = countResult[0].total;
      
      res.json({
        data: rows,
        pagination: {
          total,
          limit,
          offset,
          pages: Math.ceil(total / limit)
        }
      });
    } catch (error) {
      console.error(`获取表 ${tableName} 数据失败:`, error);
      res.status(500).json({ error: `获取表 ${tableName} 数据失败`, details: error.message });
    }
  });

  return app;
}
