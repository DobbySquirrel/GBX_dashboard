import { Server } from 'socket.io';

// 创建并配置 Socket.io 服务
export function setupSocketIO(httpServer, pool) {
  const io = new Server(httpServer, {
    cors: {
      origin: ['http://localhost:5173', 'http://localhost:8080'],
      methods: ['GET', 'POST'],
      credentials: true
    },
    // 添加重连配置
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 1000
  });

  // 在现有的连接处理代码前添加
  io.on('connect_error', (error) => {
    console.error('连接错误:', error);
  });

  io.on('connect_timeout', (timeout) => {
    console.error('连接超时:', timeout);
  });

  // Helper function to get box status counts
  const getBoxStatusCounts = async () => {
    try {
      const [rows] = await pool.query(`
        SELECT
          t1.status,
          COUNT(t1.box_id) AS count
        FROM
          box_status_logs AS t1
        JOIN (
          SELECT
            box_id,
            MAX(timestamp) AS max_timestamp
          FROM
            box_status_logs
          GROUP BY
            box_id
        ) AS t2
        ON
          t1.box_id = t2.box_id AND t1.timestamp = t2.max_timestamp
        GROUP BY
          t1.status
      `);
      return rows;
    } catch (error) {
      console.error('获取箱子状态计数失败:', error);
      return [];
    }
  };
  // New helper function to get box recycle counts
  const getBoxRecycleCounts = async () => {
    try {
      const [rows] = await pool.query(`
        SELECT
          box_id,
          COUNT(*) AS recycle_count
        FROM
          box_status_logs
        WHERE
          status = '箱子已回收'
        GROUP BY
          box_id
      `);
      return rows;
    } catch (error) {
      console.error('获取箱子回收次数失败:', error);
      return [];
    }
  };
    // New helper function to get box order binding times
    const getBoxOrderBindingTimes = async () => {
      try {
        const [rows] = await pool.query(`
          SELECT
            box_id,
            order_id,
            timestamp
          FROM
            box_status_logs
          WHERE
            status = '绑定订单'
          ORDER BY
            timestamp DESC
          LIMIT 100 -- Get the latest 100 binding events, adjust as needed
        `);
        return rows;
      } catch (error) {
        console.error('获取箱子绑定订单时间失败:', error);
        return [];
      }
    };
    // --- New Helper Function: getAverageRecycleCycle ---
  const getAverageRecycleCycle = async () => {
    try {
      // Step 1: Get all '绑定订单' and '箱子已回收' logs for all boxes
      const [logs] = await pool.query(`
        SELECT
          box_id,
          status,
          timestamp
        FROM
          box_status_logs
        WHERE
          status IN ('绑定订单', '箱子已回收')
        ORDER BY
          box_id, timestamp ASC
      `);

      const boxCycles = {}; // Stores arrays of timestamps for each box's cycles
      logs.forEach(log => {
        if (!boxCycles[log.box_id]) {
          boxCycles[log.box_id] = [];
        }
        boxCycles[log.box_id].push(log);
      });

      let totalCycleDuration = 0; // in milliseconds
      let completedCyclesCount = 0;

      for (const boxId in boxCycles) {
        const boxLogs = boxCycles[boxId];
        let bindTimestamp = null;

        for (const log of boxLogs) {
          if (log.status === '绑定订单') {
            bindTimestamp = log.timestamp;
          } else if (log.status === '箱子已回收' && bindTimestamp) {
            // Found a '箱子已回收' after a '绑定订单'
            const cycleDuration = log.timestamp.getTime() - bindTimestamp.getTime();
            if (cycleDuration >= 0) { // Ensure timestamp is valid (recycled after bind)
              totalCycleDuration += cycleDuration;
              completedCyclesCount++;
            }
            bindTimestamp = null; // Reset for the next cycle of the same box
          }
        }
      }

      if (completedCyclesCount === 0) {
        return 0; // No completed cycles yet
      }

      // Calculate average in milliseconds, then convert to hours or days for readability
      const averageMillis = totalCycleDuration / completedCyclesCount;
      // Convert to hours (1000 ms/s * 60 s/min * 60 min/hr)
      const averageHours = averageMillis / (1000 * 60 * 60);

      // Optionally, format for display (e.g., to 2 decimal places)
      return parseFloat(averageHours.toFixed(2));
    } catch (error) {
      console.error('获取箱子平均回收周期失败:', error);
      return 0;
    }
  };

  // Socket.IO 连接处理
  io.on('connection', (socket) => {
    console.log('客户端已连接:', socket.id);

    // 监听客户端订阅丢失箱子位置更新
    socket.on('subscribe_missing_box', async () => {
      console.log('客户端订阅丢失箱子位置更新:', socket.id);
      // 立即发送一次当前数据
      try {
        const [rows] = await pool.query(`SELECT * FROM box_missing`);
        socket.emit('missing_box_update', rows);
      } catch (error) {
        console.error('获取丢失箱子数据失败:', error);
      }
    });

    // 监听客户端订阅无人机状态更新
    socket.on('subscribe_drone_state', async () => {
      console.log('客户端订阅无人机状态更新:', socket.id);
      // 立即发送一次当前数据
      try {
        const [rows] = await pool.query(`
          SELECT * FROM DeliveryDrone_Property_State
          ORDER BY id DESC LIMIT 10
        `);
        socket.emit('drone_state_update', rows);
      } catch (error) {
        console.error('获取无人机状态数据失败:', error);
      }
    });

    // 监听客户端订阅室内车状态更新
    socket.on('subscribe_indoor_car_state', async () => {
      console.log('客户端订阅室内车状态更新:', socket.id);
      // 立即发送一次当前数据
      try {
        const [rows] = await pool.query(`
          SELECT * FROM IndoorDeliveryCar_Property_State
          ORDER BY id DESC LIMIT 10
        `);
        socket.emit('indoor_car_state_update', rows);
      } catch (error) {
        console.error('获取室内车状态数据失败:', error);
      }
    });

    // 新增：监听客户端订阅箱子主人更新
    socket.on('subscribe_box_owner', async () => {
      console.log('客户端订阅箱子主人更新:', socket.id);
      // 立即发送一次当前数据
      try {
        const [rows] = await pool.query(`SELECT * FROM box_owner`);
        socket.emit('box_owner_update', rows);
      } catch (error) {
        console.error('获取箱子主人数据失败:', error);
      }
    });

    // 新增：监听客户端订阅用户积分更新
    socket.on('subscribe_user_score', async () => {
      console.log('客户端订阅用户积分更新:', socket.id);
      // 立即发送一次当前数据
      try {
        const [rows] = await pool.query(`
          SELECT
            phone,
            SUM(points) AS total_points
          FROM
            user_credits_log
          GROUP BY
            phone
        `);
        socket.emit('user_score_update', rows);
      } catch (error) {
        console.error('获取用户积分数据失败:', error);
      }
    });

    // 新增：监听客户端订阅箱子状态日志更新
    socket.on('subscribe_box_status_logs', async () => {
      console.log('客户端订阅箱子状态日志更新:', socket.id);
      // 立即发送一次当前数据
      try {
        const [rows] = await pool.query(`SELECT * FROM box_status_logs ORDER BY log_id DESC LIMIT 100`); // 获取最新的100条日志
        socket.emit('box_status_logs_update', rows);
      } catch (error) {
        console.error('获取箱子状态日志数据失败:', error);
      }
    });
    // New: Listen for client subscription to box recycle counts
    socket.on('subscribe_box_recycle_counts', async () => {
      console.log('客户端订阅箱子回收次数更新:', socket.id);
      // Immediately send current data
      const boxRecycleCounts = await getBoxRecycleCounts();
      socket.emit('box_recycle_counts_update', boxRecycleCounts);
    });
      // New: Listen for client subscription to box order binding times
      socket.on('subscribe_box_order_binding_times', async () => {
        console.log('客户端订阅箱子绑定订单时间更新:', socket.id);
        // Immediately send current data
        const boxOrderBindingTimes = await getBoxOrderBindingTimes();
        socket.emit('box_order_binding_times_update', boxOrderBindingTimes);
      });

    // --- New Socket Event Listener: subscribe_average_recycle_cycle ---
    socket.on('subscribe_average_recycle_cycle', async () => {
      console.log('客户端订阅箱子平均回收周期更新:', socket.id);
      const averageCycle = await getAverageRecycleCycle();
      socket.emit('average_recycle_cycle_update', averageCycle);
    });
    // New: Listen for client subscription to box status counts
    socket.on('subscribe_box_status_counts', async () => {
      console.log('客户端订阅箱子状态计数更新:', socket.id);
      // Immediately send current data
      const boxStatusCounts = await getBoxStatusCounts();
      socket.emit('box_status_counts_update', boxStatusCounts);
    });
    // 客户端断开连接
    socket.on('disconnect', () => {
      console.log('客户端断开连接:', socket.id);
    });
  });




  // 设置定时任务，定期检查数据库并推送更新
  const startDataUpdates = async () => {
    let lastDroneData = null;
    let lastIndoorCarData = null;
    let lastMissingBoxData = null;
    let lastBoxOwnerData = null;
    let lastUserScoreData = null;
    let lastBoxStatusLogsData = null;
    let lastBoxStatusCountsData = null; // New: Record last box status counts data
    let lastBoxRecycleCountsData = null; // New: Record last box recycle counts data
    let lastBoxOrderBindingTimesData = null; // New: Record last box order binding times data
    let lastAverageRecycleCycleData = null; // New: Record last average recycle cycle data

    setInterval(async () => {
      try {
        // 检查无人机数据更新
        const [droneRows] = await pool.query(`SELECT * FROM DeliveryDrone_Property_State ORDER BY id DESC LIMIT 10`);

        const currentDroneData = JSON.stringify(droneRows);
        if (currentDroneData !== lastDroneData) {
          lastDroneData = currentDroneData;
          io.emit('drone_state_update', droneRows);
          console.log('推送无人机状态更新:', droneRows);
        }

        // 检查室内车数据更新
        const [carRows] = await pool.query(`SELECT * FROM IndoorDeliveryCar_Property_State ORDER BY id DESC LIMIT 10`);

        const currentCarData = JSON.stringify(carRows);
        if (currentCarData !== lastIndoorCarData) {
          lastIndoorCarData = currentCarData;
          io.emit('indoor_car_state_update', carRows);
          console.log('推送室内车状态更新:', carRows);
        }

        // 检查丢失箱子数据更新
        const [boxRows] = await pool.query(`SELECT * FROM box_missing`);

        const currentBoxData = JSON.stringify(boxRows);
        if (currentBoxData !== lastMissingBoxData) {
          lastMissingBoxData = currentBoxData;
          io.emit('missing_box_update', boxRows);
          console.log('推送丢失箱子位置更新:', boxRows);
        }

        // 新增：检查箱子主人数据更新
        const [ownerRows] = await pool.query(`SELECT * FROM box_owner`);

        const currentOwnerData = JSON.stringify(ownerRows);
        if (currentOwnerData !== lastBoxOwnerData) {
          lastBoxOwnerData = currentOwnerData;
          io.emit('box_owner_update', ownerRows);
          console.log('推送箱子主人更新:', ownerRows);
        }

        // 新增：检查用户积分数据更新
        const [userScoreRows] = await pool.query(`
          SELECT
            phone,
            SUM(points) AS total_points
          FROM
            user_credits_log
          GROUP BY
            phone
        `);

        const currentUserScoreData = JSON.stringify(userScoreRows);
        if (currentUserScoreData !== lastUserScoreData) {
          lastUserScoreData = currentUserScoreData;
          io.emit('user_score_update', userScoreRows);
          console.log('推送用户积分更新:', userScoreRows);
        }

        // 新增：检查箱子状态日志数据更新
        const [boxStatusLogsRows] = await pool.query(`SELECT * FROM box_status_logs ORDER BY log_id DESC LIMIT 100`);
        const currentBoxStatusLogsData = JSON.stringify(boxStatusLogsRows);
        if (currentBoxStatusLogsData !== lastBoxStatusLogsData) {
          lastBoxStatusLogsData = currentBoxStatusLogsData;
          io.emit('box_status_logs_update', boxStatusLogsRows);
          console.log('推送箱子状态日志更新:', boxStatusLogsRows);
        }
       // New: Check and push box status counts updates
       const boxStatusCounts = await getBoxStatusCounts();
       const currentBoxStatusCountsData = JSON.stringify(boxStatusCounts);
       if (currentBoxStatusCountsData !== lastBoxStatusCountsData) {
         lastBoxStatusCountsData = currentBoxStatusCountsData;
         io.emit('box_status_counts_update', boxStatusCounts);
         console.log('推送箱子状态计数更新:', boxStatusCounts);
       }
      // New: Check and push box recycle counts updates
      const boxRecycleCounts = await getBoxRecycleCounts();
      const currentBoxRecycleCountsData = JSON.stringify(boxRecycleCounts);
      if (currentBoxRecycleCountsData !== lastBoxRecycleCountsData) {
        lastBoxRecycleCountsData = currentBoxRecycleCountsData;
        io.emit('box_recycle_counts_update', boxRecycleCounts);
        console.log('推送箱子回收次数更新:', boxRecycleCounts);
      }
        // New: Check and push box order binding times updates
        const boxOrderBindingTimes = await getBoxOrderBindingTimes();
        const currentBoxOrderBindingTimesData = JSON.stringify(boxOrderBindingTimes);
        if (currentBoxOrderBindingTimesData !== lastBoxOrderBindingTimesData) {
          lastBoxOrderBindingTimesData = currentBoxOrderBindingTimesData;
          io.emit('box_order_binding_times_update', boxOrderBindingTimes);
          console.log('推送箱子绑定订单时间更新:', boxOrderBindingTimes);
        }

        // --- New: Check and push average recycle cycle updates ---
        const averageRecycleCycle = await getAverageRecycleCycle();
        const currentAverageRecycleCycleData = JSON.stringify(averageRecycleCycle);
        if (currentAverageRecycleCycleData !== lastAverageRecycleCycleData) {
          lastAverageRecycleCycleData = currentAverageRecycleCycleData;
          io.emit('average_recycle_cycle_update', averageRecycleCycle);
          console.log('推送箱子平均回收周期更新 (小时):', averageRecycleCycle);
        }

      } catch (error) {
        console.error('获取实时数据失败:', error);
      }
    }, 800);
  };

  // 启动定时更新
  startDataUpdates();

  return io;
}