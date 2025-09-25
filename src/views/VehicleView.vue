<template>
  <div class="vehicle-view">
    <!-- 添加 Header 组件并确保其有足够宽度 -->
    <div class="header-container">
      <Header />
    </div>

    <div class="content-container">
      <!-- 左侧地图 -->
      <div class="map-container">
        <live_MapDisplay
          pageType="vehicle"
        />
      </div>
      
      <!-- 右侧面板 -->
      <div class="right-panels">
        <!-- 订单显示面板 -->
        <div class="card-content">
          <div class="title-container">
            <el-text class="mx-1" style="font-size: 16px; color: #44652a; font-weight: bold;">无人车</el-text>
          </div>
          <OrderDisplayPanel pageType="vehicle" />
        </div>
        <div class="card-content2">
          <div class="title-container">
            <el-text class="mx-1" style="font-size: 16px; color: #44652a; font-weight: bold;">机柜</el-text>
          </div>
          <CardDisplay />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 导入所需的组件和API
import CardDisplay from '@/components_vertical/CardDisplay.vue';
import Header from '@/components_vertical/Header.vue';
import { ref, onUnmounted } from 'vue';
import live_MapDisplay from '@/components_vertical/live_MapDisplay.vue';
import OrderDisplayPanel from '@/components_vertical/OrderDisplayPanel.vue';

// 在组件卸载时触发全局事件
onUnmounted(() => {
  window.dispatchEvent(new Event('viewUnmounted'));
});
</script>

<style scoped>
.vehicle-view {
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header-container {
  width: 100%;
  margin-bottom: 0px;
  overflow: visible; /* 确保内容不被裁剪 */
}

h1 {
  color: #44652a;
  margin-bottom: 20px;
  margin-top: 10px;
}

.content-container {
  display: grid;
  grid-template-columns: 1.5fr 1fr; /* 左侧地图占1.5份，右侧面板占1份 */
  gap: 20px;
  flex: 1;
}

.data-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  color: #44652a;
}

.card-content {
  min-height: 200px;
  height: calc(30% - 10px);
  overflow: hidden;
}

.card-content2 {
  min-height: 100px;
  height: calc(20% + 60px);
  overflow: hidden;
}

.right-panels {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.order-card {
  flex: 1;
}

.tracker-card {
  flex: 1;
}

.map-container {
  height: 100%;
}

/* 响应式布局 */
@media screen and (max-width: 1200px) {
  .content-container {
    grid-template-columns: 1fr;
  }
  
  .right-panels {
    flex-direction: row;
  }
}

@media screen and (max-width: 768px) {
  .right-panels {
    flex-direction: column;
  }
}

/* 添加响应式设计 */
@media screen and (max-height: 800px) {
  .vehicle-view {
    padding: 10px;
  }
  
  h1 {
    margin-bottom: 10px;
    margin-top: 5px;
    font-size: 1em;
  }
  
  .card-content {
    min-height: 150px;
  }
  
  .map-container {
    height: 500px;
  }
  .right-panels {
  display: flex;
  flex-direction: column;
  gap: 8px; /* 或 0，间距更小 */
  /* height: 100%;  // 删除这行 */
  /* align-items: flex-start; // 删除这行 */
}
.title-container {
  text-align: center;
  width: 100%;
  margin-bottom: 10px;
  margin-top: -10px;
}

.card-content,
.card-content2 {
  min-height: unset;
  height: auto;
  overflow: visible;
  display: block;
  align-items: unset;
  flex: unset;
  margin: 0;
  padding: 0;
}

}
</style> 