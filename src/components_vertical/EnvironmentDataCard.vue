<template>
  <div class="environment-data-card">
    <div class="data-section">
      <div class="data-item">
        <img :src="treeDataURI" class="data-icon" alt="碳排放图标" />
        <div class="data-content">
          <div class="data-label">降碳量(约等于)</div>
          <div class="data-value">
            {{ carbonReduction.toLocaleString('zh-CN') }}片
            <span class="box-count">({{ totalBoxCount }}箱)</span>
          </div>
        </div>
      </div>
      
      <div class="data-item">
        <el-icon class="data-icon" color="#76c850"><Box /></el-icon>
        <div class="data-content">
          <div class="data-label">包裹总数</div>
          <div class="data-value">{{ totalBoxCount }}</div>
        </div>
      </div>
      
      <div class="data-item">
        <el-icon class="data-icon" color="#76c850"><Timer /></el-icon>
        <div class="data-content">
          <div class="data-label">平均单箱回收周期</div>
          <div class="data-value">{{ averageRecycleCycle !== 0 ? averageRecycleCycle + ' h' : 'N/A' }}</div>
        </div>
      </div>

      <div class="data-item">
        <el-icon class="data-icon" color="#76c850"><Calendar /></el-icon>
        <div class="data-content">
          <div class="data-label">平均单箱回收次数</div>
          <div class="data-value">{{ averageRecycleCount !== 0 ? averageRecycleCount : 'N/A' }}</div>
        </div>
      </div>
    </div>
    
    <div class="data-note">
      <p>注: 碳排放减少量基于每个慧达箱可循环使用100次计算（保守估计）</p>
      <p>与同等大小的一次性纸箱相比，每循环使用一次慧达箱，减少碳排放量约等于2片树叶的固碳量</p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue';
import { Box, Timer, Calendar } from "@element-plus/icons-vue";
import { treeDataURI } from "../assets/symbols/treeSymbol.js";
import socket from '../api/socket.js';

const totalBoxCount = ref(0);
const averageRecycleCycle = ref(0);
const inCabinetCount = ref(0);
const averageRecycleCount = ref(0);
const boxRecycleCountsData = ref([]);

// 处理在柜包裹数量更新
const handleCabinetStatusUpdate = (data) => {
  try {
    inCabinetCount.value = data.inCabinetCount;
    console.log('Updated in-cabinet count:', inCabinetCount.value);
  } catch (error) {
    console.error('Error processing cabinet status data:', error);
  }
};

// 处理箱子回收次数数据更新
const handleRecycleCountsUpdate = (data) => {
  try {
    let count = 0;
    if (Array.isArray(data)) {
      count = data.reduce((sum, item) => {
        return sum + (parseInt(item.recycle_count) || 0);
      }, 0);
      
      // 计算平均单箱回收次数
      if (data.length > 0) {
        const totalRecycleCount = data.reduce((sum, item) => sum + (parseInt(item.recycle_count) || 0), 0);
        averageRecycleCount.value = (totalRecycleCount / data.length).toFixed(2);
      } else {
        averageRecycleCount.value = 0;
      }
      
      boxRecycleCountsData.value = data;
    }
    totalBoxCount.value = count;
    console.log('Updated total box count:', totalBoxCount.value);
    console.log('Updated average recycle count:', averageRecycleCount.value);
  } catch (error) {
    console.error('Error processing recycle counts data:', error);
  }
};

const handleAverageRecycleCycleUpdate = (data) => {
  try {
    averageRecycleCycle.value = data;
    console.log('Updated average recycling cycle:', averageRecycleCycle.value, '小时');
  } catch (error) {
    console.error('Error processing average recycle cycle data:', error);
    averageRecycleCycle.value = 0;
  }
};

const carbonReduction = computed(() => {
  if (totalBoxCount.value === 0) return 0;
  return totalBoxCount.value * 2;
});

onMounted(() => {
  if (socket) {
    socket.emit('subscribe_box_recycle_counts');
    socket.on('box_recycle_counts_update', handleRecycleCountsUpdate);

    socket.emit('subscribe_average_recycle_cycle');
    socket.on('average_recycle_cycle_update', handleAverageRecycleCycleUpdate);

    // 订阅在柜包裹数量
    socket.emit('subscribe_cabinet_status');
    socket.on('cabinet_status_update', handleCabinetStatusUpdate);
  } else {
    console.error('Socket.IO instance not found');
  }
});

onBeforeUnmount(() => {
  if (socket) {
    socket.off('box_recycle_counts_update', handleRecycleCountsUpdate);
    socket.off('average_recycle_cycle_update', handleAverageRecycleCycleUpdate);
    socket.off('cabinet_status_update', handleCabinetStatusUpdate);
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
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.data-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  box-sizing: border-box;
  margin: 0;
  min-width: unset;
  max-width: unset;
}

.data-icon {
  width: 36px;
  height: 36px;
  margin-right: 15px;
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

.box-count {
  font-size: 14px;
  color: #666;
  margin-left: 8px;
  font-weight: normal;
}
</style>