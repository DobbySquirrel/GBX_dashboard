<template>
  <div class="environment-view">
    <div class="header-container">
      <Header />
    </div>

    <div class="content-container">
      <el-row :gutter="20" class="chart-row">
        <el-col :span="12">
          <el-card class="data-card">
            <div class="card-content">
              <EnvironmentDataCard/>
            </div>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card class="data-card">
            <div class="card-content">
              <RecycleCabinetOccupancyChart />
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="chart-row">
        <el-col :span="12">
          <el-card class="data-card2">
            <div class="chart-card-content">
              <OrderCountChart/>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="data-card2">
            <div class="chart-card-content">
              <box_recycle_counts_bar/>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import Header from '@/components_vertical/Header.vue';
import { onMounted, onUnmounted, nextTick } from 'vue';
import RecycleCabinetOccupancyChart from "../components_vertical/EnvironmentalBenfits.vue";
import box_recycle_counts_bar from "../components_vertical/box_recycle_counts_bar.vue";
import OrderCountChart from "../components_vertical/OrderCountChart.vue";
import EnvironmentDataCard from "../components_vertical/EnvironmentDataCard.vue";
import socket from "../api/socket.js";

// 在组件卸载时触发全局事件
onUnmounted(() => {
  window.dispatchEvent(new Event('viewUnmounted'));
  unsubscribeFromUpdates();
});

// 添加订阅函数
const subscribeToUpdates = () => {
  if (!socket.connected) {
    socket.connect();
  }

  // 订阅所需的数据更新
  socket.emit('subscribe_box_recycle_counts');
  socket.emit('subscribe_average_recycle_cycle');
  socket.emit('subscribe_box_order_binding_times');
  socket.emit('subscribe_user_score');
  socket.emit('subscribe_box_status_counts');
  socket.emit('subscribe_box_status_logs');
  socket.emit('subscribe_missing_box');
};

// 添加取消订阅函数
const unsubscribeFromUpdates = () => {
  if (socket.connected) {
    socket.off('box_recycle_counts_update');
    socket.off('average_recycle_cycle_update');
    socket.off('box_order_binding_times_update');
    socket.off('user_score_update');
    socket.off('box_status_counts_update');
    socket.off('box_status_logs_update');
    socket.off('missing_box_update');
    socket.disconnect();
  }
};

onMounted(() => {
  // 确保组件完全挂载后再订阅数据
  nextTick(() => {
    subscribeToUpdates();
    
    // 添加重连逻辑
    socket.on('connect_error', () => {
      console.log('连接错误，尝试重新连接...');
      setTimeout(subscribeToUpdates, 1000);
    });

    socket.on('disconnect', () => {
      console.log('连接断开，尝试重新连接...');
      setTimeout(subscribeToUpdates, 1000);
    });

    // 触发窗口 resize 事件以确保图表正确渲染
    setTimeout(() => {
      window.dispatchEvent(new Event('resize'));
      window.dispatchEvent(new Event('viewMounted'));
    }, 300);
  });
});

// 添加页面可见性变化处理
const handleVisibilityChange = () => {
  if (document.hidden) {
    unsubscribeFromUpdates();
  } else {
    subscribeToUpdates();
  }
};

// 添加页面可见性监听
onMounted(() => {
  document.addEventListener('visibilitychange', handleVisibilityChange);
});

onUnmounted(() => {
  document.removeEventListener('visibilitychange', handleVisibilityChange);
});
</script>

<style scoped>
/* Your existing styles */
.environment-view {
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header-container {
  width: 100%;
  margin-bottom: 10px;
  overflow: visible;
}

h1 {
  color: #44652a;
  margin-bottom: 20px;
}

.content-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chart-row {
  margin-bottom: 0px;
}

.data-card {
  margin-bottom: 0px;
  height: 100%;
  /* Increase max-height significantly, or set a fixed height */
  max-height: 350px; /* Or even 400px if needed */
  /* If you want it to always be a certain height, use height instead of max-height */
  /* height: 350px; */
}
.data-card2 {
  margin-bottom: 0px;
  height: 100%;
  min-height: 250px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  color: #44652a;
}

.card-content {
  min-height: 80px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chart-card-content {
  min-height: 80px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chart-container {
  height: 250px;
  width: 100%;
}

/* Responsive layout */
@media screen and (max-width: 1200px) {
  .el-col {
    width: 100% !important;
    margin-bottom: 20px;
  }
}

@media screen and (max-width: 768px) {
  .environment-view {
    padding: 10px;
  }

  .card-content {
    min-height: 100px;
  }

  .chart-container {
    height: 250px;
  }
}
</style>