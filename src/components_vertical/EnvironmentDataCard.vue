<template>
  <div class="environment-data-card">
    <div class="data-section">
      <div class="data-item">
        <el-icon class="data-icon" color="#76c850"><Odometer /></el-icon>
        <div class="data-content">
          <div class="data-label">碳排放减少量</div>
          <div class="data-value">{{ carbonReduction.toLocaleString('zh-CN') }} kg</div>
        </div>
      </div>
      
      <div class="data-item">
        <el-icon class="data-icon" color="#76c850"><Box /></el-icon>
        <div class="data-content">
          <div class="data-label">可回收包装使用率</div>
          <div class="data-value">{{ recyclingRate }}%</div>
        </div>
      </div>
      
      <div class="data-item">
        <el-icon class="data-icon" color="#76c850"><Timer /></el-icon> <div class="data-content">
          <div class="data-label">箱子平均回收周期</div>
          <div class="data-value">{{ averageRecycleCycle !== 0 ? averageRecycleCycle + ' h' : 'N/A' }}</div>
        </div>
      </div>
    </div>
    
    <div class="data-note">
      <p>注: 碳排放减少量基于每个绿色包装盒可循环使用20次计算</p>
      <p>与同等大小的一次性纸箱相比，每个绿色包装盒可减少约0.5267g碳排放</p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue';
import { Odometer, Box, Timer } from "@element-plus/icons-vue"; // Import Timer icon
import socket from '../api/socket.js'; // Ensure the path to your socket.js is correct

// Reactive variable to store the total box count from the socket (for carbon reduction and recycling rate)
const totalBoxCount = ref(0);
// Reactive variable to store the average recycling cycle from the socket
const averageRecycleCycle = ref(0);

// Method to handle updates for recycle counts (for carbon reduction and recycling rate)
const handleRecycleCountsUpdate = (data) => {
  try {
    let count = 0;
    if (Array.isArray(data)) {
      count = data.reduce((sum, item) => {
        return sum + (parseInt(item.recycle_count) || 0);
      }, 0);
    }
    totalBoxCount.value = count;
    console.log('Updated total box count for environment data card:', totalBoxCount.value);
  } catch (error) {
    console.error('Error processing recycle counts data in environment data card:', error);
  }
};

// Method to handle updates for average recycling cycle
const handleAverageRecycleCycleUpdate = (data) => {
  try {
    // Assuming 'data' directly contains the calculated average cycle in hours
    averageRecycleCycle.value = data;
    console.log('Updated average recycling cycle:', averageRecycleCycle.value, '小时');
  } catch (error) {
    console.error('Error processing average recycle cycle data:', error);
    averageRecycleCycle.value = 0; // Reset if error
  }
};

// 计算碳排放减少量 (remains the same)
const carbonReduction = computed(() => {
  if (totalBoxCount.value === 0) return 0;
  return (totalBoxCount.value * 0.5267 / 1000) * 1000;
});

// 计算可回收包装使用率 (remains the same, adjust maxBoxesFor100Percent as needed)
const recyclingRate = computed(() => {
  if (totalBoxCount.value === 0) return 0;
  const maxBoxesFor100Percent = 500; 
  return Math.min(100, Math.round((totalBoxCount.value / maxBoxesFor100Percent) * 100));
});

onMounted(() => {
  if (socket) {
    // Subscribe to existing recycle counts for carbon reduction and recycling rate
    socket.emit('subscribe_box_recycle_counts');
    socket.on('box_recycle_counts_update', handleRecycleCountsUpdate);

    // New: Subscribe to average recycle cycle
    socket.emit('subscribe_average_recycle_cycle');
    socket.on('average_recycle_cycle_update', handleAverageRecycleCycleUpdate);

  } else {
    console.error('Socket.IO instance not found. Ensure socket.js is correctly configured.');
  }
});

onBeforeUnmount(() => {
  if (socket) {
    socket.off('box_recycle_counts_update', handleRecycleCountsUpdate);
    // New: Unsubscribe from average recycle cycle
    socket.off('average_recycle_cycle_update', handleAverageRecycleCycleUpdate);
  }
});
</script>

<style scoped>
.environment-data-card {
  background-color: #f7fcf5;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

.data-section {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.data-item {
  display: flex;
  align-items: center;
  margin: 10px;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  flex: 1;
  min-width: 250px;
  max-width: 30%;
  box-sizing: border-box;
}

.data-icon {
  font-size: 36px;
  margin-right: 15px;
  color: #76c850; /* Green color for icons */
}

.data-content {
  display: flex;
  flex-direction: column;
}

.data-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.data-value {
  font-size: 24px;
  font-weight: bold;
  color: #44652a; /* Darker green for values */
}

.data-note {
  font-size: 12px;
  color: #888;
  border-top: 1px solid #eee;
  padding-top: 15px;
  margin-top: 15px;
  line-height: 1.6;
}

.data-note p {
  margin: 5px 0;
}
</style>