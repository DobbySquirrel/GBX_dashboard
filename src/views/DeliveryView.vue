<template>
  <div class="delivery-view">
    <div class="header-container">
      <Header />
    </div>

    <div class="content-container">
      <el-row :gutter="20" class="chart-row">
        <el-col :span="8">
          <el-card class="chart-card">
            <div class="chart-content">
              <MapDisplay_Missingbox/>
            </div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="chart-card">
            <div class="chart-content">
              <Bar_user_score/>
            </div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="chart-card">
            <div class="chart-content">
              <BoxStatusChart />
            </div>
          </el-card>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-card class="data-card">
            <div class="card-content">
              <CardDisplay/>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
// 导入所需的组件
import Header from '@/components_vertical/Header.vue';
import { onMounted } from 'vue'; // Only onMounted is needed now
import MapDisplay_Missingbox from "../components_vertical/MapDisplay_Missingbox.vue";
import Bar_user_score from "../components_vertical/Bar_user_score.vue";
import BoxStatusChart from "../components_vertical/RecycleBoxStatus.vue";
import CardDisplay from "../components_vertical/CardDisplay.vue";

// 添加生命周期钩子，确保组件挂载后重新渲染图表
onMounted(() => {
  // 强制重新渲染图表
  setTimeout(() => {
    window.dispatchEvent(new Event('resize'));
  }, 300);
});
</script>

<style scoped>
.delivery-view {
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header-container {
  width: 100%;
  margin-bottom: 0px;
  overflow: visible;
}

.content-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.data-card {
  margin-bottom: 20px;
}

.chart-row {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 10%;
  font-weight: bold;
  font-size: small;
  color: #44652a;
}

.card-content {
  min-height: 200px;
  height: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.chart-card {
  height: 400px;
  display: flex;
  flex-direction: column;
}

.chart-content {
  height: 100%;
  width: 100%;
  flex: 1;
  min-height: 300px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.area-flow-container {
  height: 300px;
}

/* 响应式布局 */
@media screen and (max-width: 1200px) {
  .el-col {
    width: 100% !important;
    margin-bottom: 20px;
  }
  
  .chart-card {
    height: 300px;
  }
}

@media screen and (max-width: 768px) {
  .delivery-view {
    padding: 10px;
  }
  
  .card-content {
    min-height: 200px;
  }
  
  .area-flow-container {
    height: 200px;
  }
}
</style> 