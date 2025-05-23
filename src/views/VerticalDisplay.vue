<template>
  <div class="vertical-layout">
    <el-container>
      <!-- 头部 -->
      <el-header>
        <AppHeader 
          :DeliveryDrone_Property_DroneDeliveryOrder="data.droneDeliveryOrder"
          :IndoorDeliveryCar_Property_IndoorDeliveryOrder="data.indoorDeliveryOrder"
          :OutdoorDeliveryCar_Property_OutdoorDeliveryOrder="data.outdoorDeliveryOrder"
          :Delivery_Locker_Property_RecycleDelivery="data.recycleDelivery"
          :Box_owner="data.boxOwner"
        />
      </el-header>
      <!-- 主体内容 -->
      <el-main>
        <div>
          <el-row :gutter="10">
            <!-- 上部分 - 实时数据 -->
            <el-col :span="24" class="top-section">
              <h3>Live Data</h3>
              <div class="live-container card">
                <live_MapDisplay
                  :OutdoorDeliveryCar_Property_OutdoorCarState="data.outdoorCarState"
                  :IndoorDeliveryCar_Property_IndoorCarState="data.indoorCarState"
                  :DeliveryDrone_Property_DroneState="data.droneState"
                />
              </div>
            </el-col>
            
            
            <!-- 下部分 - 图表区域 -->
            <el-col :span="24" class="bottom-section">
              <h3>History Data (1000 Orders)</h3>
              <el-row :gutter="10">
                <!-- 左侧图表 -->
                <el-col :span="8">
                  <div class="chart-card card">
                    <RecycleCabinetOccupancyChart
                      :Box_owner="data.boxOwner"
                    />
                  </div>
                </el-col>
                
                <!-- 中间图表 -->
                <el-col :span="8">
                  <div class="chart-card card">
                    <Bar_user_score
                      :userScoreRecord="data.userScoreRecord"
                    />
                  </div>
                </el-col>
                
                <!-- 右侧图表 -->
                <el-col :span="8">
                  <div class="chart-card card">
                    <RecycleBoxStatusPie
                      :Box_owner="data.boxOwner"
                    />
                  </div>
                </el-col>
              </el-row>
            </el-col>
                        <!-- 中部分 - 历史数据 -->
                        <el-col :span="24" class="middle-section">
              <div class="history-container card">
               
                <AreaTrafficFlow
                  :DeliveryDrone_Property_DroneDeliveryOrder="data.droneDeliveryOrder"
                  :IndoorDeliveryCar_Property_IndoorDeliveryOrder="data.indoorDeliveryOrder"
                  :OutdoorDeliveryCar_Property_OutdoorDeliveryOrder="data.outdoorDeliveryOrder"
                />
              </div>
            </el-col>
            <!-- 最下部分 - 额外图表 -->
            <el-col :span="24" class="extra-section">
              <el-row :gutter="10">
                <!-- 左侧额外图表 -->
                <el-col :span="12">
                  <div class="extra-chart-card card" @click.stop>
                    <MapDisplay_DistributionOfOrder_nre
                      :DeliveryDrone_Property_DroneDeliveryOrder="data.droneDeliveryOrder"
                      :IndoorDeliveryCar_Property_IndoorDeliveryOrder="data.indoorDeliveryOrder"
                      :OutdoorDeliveryCar_Property_OutdoorDeliveryOrder="data.outdoorDeliveryOrder"
                      @map-interaction="handleMapInteraction"
                    />
                  </div>
                </el-col>
                
                <!-- 右侧额外图表 -->
                <el-col :span="12">
                  <div class="extra-chart-card card">
                    <MapDisplay_Missingbox :points-data="[[113.47953830802487, 22.894216859923475], [113.47872088332235, 22.892061020308077]]" />
                  </div>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
        </div>
      </el-main>
      <ObsDownloader @update-data="handleDataUpdate" />
    </el-container>
  </div>
</template>

<script>
import { useDataStore } from '../store';
import AppHeader from "../components_vertical/Header.vue";
import MapDisplay_Missingbox from "../components_vertical/MapDisplay_Missingbox.vue";
import CardDisplay from "../components_vertical/CardDisplay.vue";
import live_MapDisplay from "../components_vertical/live_MapDisplay.vue";
import ObsDownloader from "../components_vertical/ObsDownloader.vue";
import OccupancyChart from "../components_vertical/OccupancyChart.vue";
import OrderCountChart from "../components_vertical/OrderCountChart.vue";
import RecycleCabinetOccupancyChart from "../components_vertical/EnvironmentalBenfits.vue";
import RecycleBoxStatusPie from "../components_vertical/RecycleBoxStatus.vue";
import MapDisplay_DistributionOfOrder_nre from "../components_vertical/MapDisplay_DistributionOfOrder_nre.vue";
import Bar_user_score from "../components_vertical/Bar_user_score.vue";
import AreaTrafficFlow from "../components_vertical/AreaTrafficFlow.vue";
import { storeToRefs } from 'pinia';
import { ref } from 'vue';

export default {
  name: 'VerticalDisplay',
  components: {
    AppHeader,
    live_MapDisplay,
    CardDisplay,
    ObsDownloader,
    OccupancyChart,
    MapDisplay_Missingbox,
    OrderCountChart,
    RecycleCabinetOccupancyChart,
    RecycleBoxStatusPie,
    MapDisplay_DistributionOfOrder_nre,
    Bar_user_score,
    AreaTrafficFlow
  },
  
  setup() {
    const store = useDataStore();
    const { data, loading, error } = storeToRefs(store);

    // 处理数据更新
    const handleDataUpdate = ({ file, content }) => {
      store.updateData(file, content);
    };

    // 添加地图交互处理函数
    const handleMapInteraction = (event) => {
      // 阻止事件传播到其他组件
      event?.stopPropagation?.();
      // 可以在这里处理地图交互逻辑
    };

    return {
      data,
      loading,
      error,
      handleDataUpdate,
      handleMapInteraction
    };
  },
};
</script>

<style>
.vertical-layout {
  background-color: rgba(211, 211, 211, 0.278);
  border-radius: 30px;
  height: 100vh;
  padding: 15px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.el-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.el-header {
  position: relative;
  flex-shrink: 0;
  height: 15vh !important;
  padding: 5px;
  min-height: 150px;
  max-height: 300px;
  overflow: hidden;
  margin-bottom: 5px;
}

.header-placeholder {
  background-color: white;
  border-radius: 10px;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.el-main {
  flex: 1;
  padding: 5px;
  overflow-y: auto;
  overflow-x: hidden;
  margin-top: 5px;
}

.card {
  padding: 15px;
  background-color: white;
  border-radius: 10px;
  margin: 5px 0px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.placeholder-content {
  background-color: #f0f0f0;
  width: 100%;
  height: 90%;
  border-radius: 5px;
}

.top-section, .middle-section, .bottom-section, .extra-section {
  margin-bottom: 8px;
}

.live-container {
  height: 28vh;
  min-height: 160px;
}

.history-container {
  height: 8vh;
  min-height: 80px;
}

.chart-card {
  height: 14vh;
  min-height: 110px;
}

.extra-chart-card {
  height: 18vh;
  min-height: 180px;
}

h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 1.8em;
  font-weight: bold;
}

/* 针对竖屏比例的媒体查询 */
@media screen and (min-width: 800px) {
  .live-container {
    height: 28vh;
  }
  
  .history-container {
    height: 8vh;
  }
  
  .chart-card {
    height: 14vh;
  }
  
  .extra-chart-card {
    height: 18vh;
  }
}

/* 针对较小屏幕的媒体查询 */
@media screen and (max-width: 768px) {
  .el-col {
    width: 100% !important;
  }
  
  .chart-card, .extra-chart-card {
    margin-bottom: 8px;
  }
  
  h3 {
    font-size: 1.5em;
  }
}

/* 针对1680*3200屏幕的特定调整 */
@media screen and (width: 1680px) and (height: 3200px) {
  .vertical-layout {
    transform: none;
    width: 100%;
    height: 100%;
    padding: 15px;
  }
  
  .el-main {
    overflow-y: hidden;
    padding: 8px;
  }
  
  .live-container {
    height: 32vh;
  }
  
  .history-container {
    height: 10vh;
  }
  
  .chart-card {
    height: 15vh;
  }
  
  .extra-chart-card {
    height: 20vh;
  }
  
  .top-section, .middle-section, .bottom-section, .extra-section {
    margin-bottom: 10px;
  }
  
  .card {
    margin: 6px 0;
  }
}

/* 确保所有图表容器内的内容不溢出 */
.chart-card > div, .extra-chart-card > div, .live-container > div, .history-container > div {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

/* 移除之前的缩放样式 */
@media screen and (max-height: 1200px) {
  .vertical-layout {
    transform: none;
    width: 100%;
    height: 100%;
  }
}
</style> 