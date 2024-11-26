<template>
  <div class="common-layout">
    <el-container>
      <!-- 加载状态显示 -->
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
      <el-main >
        <div>
          <el-row :gutter="10">
            <!-- 左侧部分 -->
            <el-col :span="5" class="left">
              <!-- 左上一: 占用率 -->
              <div class="left1 card">
                <OccupancyChart
                  :OutdoorDeliveryCar_Property_OutdoorCarState="data.outdoorCarState"
                  :IndoorDeliveryCar_Property_IndoorCarState="data.indoorCarState"
                  :DeliveryDrone_Property_DroneState="data.droneState"
                  :Delivery_Locker_Property_InputDelivery="data.inputDelivery"
                />
              </div>

              <!-- 左上二: 订单数量趋势 -->
              <div class="left2 card">
                <OrderCountChart
                  :DeliveryDrone_Property_DroneDeliveryOrder="data.droneDeliveryOrder"
                  :IndoorDeliveryCar_Property_IndoorDeliveryOrder="data.indoorDeliveryOrder"
                  :OutdoorDeliveryCar_Property_OutdoorDeliveryOrder="data.outdoorDeliveryOrder"
                />
              </div>
              <!-- 回收柜使用情况和回收柜占用情况饼图 -->
              <div class="left3 card">

                                  <RecycleCabinetOccupancyChart
                    :Delivery_Locker_Property_InputDelivery="data.inputDelivery"
                    :Delivery_Locker_Property_OutputDelivery="data.outputDelivery"
                    :Delivery_Locker_Property_RecycleDelivery="data.recycleDelivery"
                  />
              </div>
            </el-col>

            <!-- 中间地图部分 -->
            <el-col :span="14" class="middle card">
              <!-- 暂时注释掉 MapDisplay_indoorCar 组件 -->
              <!-- <MapDisplay_indoorCar
                :OutdoorDeliveryCar_Property_OutdoorCarState="data.outdoorCarState"
                :IndoorDeliveryCar_Property_IndoorCarState="data.indoorCarState"
                :DeliveryDrone_Property_DroneState="data.droneState"
              /> -->

              <CardDisplay
                :Box_owner="data.boxOwner"
              />
            </el-col>
            <!-- 右侧新增的可视化部分 -->
            <el-col :span="5" class="right">
              <!-- 右上一: 速度数据图表 -->
              <div class="right1 card">
                                <RecycleBoxStatusPie
:Box_owner="data.boxOwner"
                />
              </div>
              <div class="right2 card">
                <MapDisplay_DistributionOfOrder
                :DeliveryDrone_Property_DroneDeliveryOrder="data.droneDeliveryOrder"
                  :IndoorDeliveryCar_Property_IndoorDeliveryOrder="data.indoorDeliveryOrder"
                  :OutdoorDeliveryCar_Property_OutdoorDeliveryOrder="data.outdoorDeliveryOrder"
                />
              </div>
                            <div class="right3 card">
                <!-- <MapDisplay_outdoorCar
                  :Delivery_Locker_Property_InputDelivery="data.inputDelivery"
                  :Delivery_Locker_Property_OutputDelivery="data.outputDelivery"
                  :Delivery_Locker_Property_RecycleDelivery="data.recycleDelivery"
                /> -->
                <Bar_user_score
:Box_owner="data.boxOwner"
                />

              </div>
            </el-col>
          </el-row>
        </div>
      </el-main>
      <ObsDownloader @update-data="handleDataUpdate" />
    </el-container>
  </div>
</template>

<script>
import { useDataStore } from './store';
import AppHeader from "./components/Header.vue";
import CardDisplay from "./components/CardDisplay.vue";
import ObsDownloader from "./components/ObsDownloader.vue";
import OccupancyChart from "./components/OccupancyChart.vue";
import OrderCountChart from "./components/OrderCountChart.vue";
import RecycleCabinetOccupancyChart from "./components/RecycleCabinetOccupancyChart.vue";
import RecycleBoxStatusPie from "./components/RecycleBoxStatusPie.vue";
import MapDisplay_indoorCar from "./components/MapDisplay_indoorCar.vue";
import MapDisplay_outdoorCar from "./components/MapDisplay_outdoorCar.vue";
import MapDisplay_drone from "./components/MapDisplay_drone.vue";
import MapDisplay_DistributionOfOrder from "./components/MapDisplay_DistributionOfOrder.vue";
import { ElButton } from "element-plus";
import { storeToRefs } from 'pinia';
import Bar_user_score from "./components/Bar_user_score.vue";

export default {
  components: {
    OccupancyChart,
    OrderCountChart,
    RecycleCabinetOccupancyChart,
    RecycleBoxStatusPie,
    MapDisplay_indoorCar,
    ObsDownloader,
    ElButton,
    AppHeader,
    MapDisplay_outdoorCar,
    MapDisplay_drone,
    CardDisplay,
    MapDisplay_DistributionOfOrder,
    Bar_user_score,
  },
  
  setup() {
    const store = useDataStore();
    const { data, loading, error } = storeToRefs(store);

    // 处理数据更新
    const handleDataUpdate = ({ file, content }) => {
      store.updateData(file, content);
    };

    return {
      data,
      loading,
      error,
      handleDataUpdate,
    };
  },
};
</script>
<style>
/* 添加 el-container 相关样式 */
.el-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  height: auto;
  overflow: visible;
}

/* 确保 header 不会与内容重叠 */
.el-header {
  position: relative;
  flex-shrink: 0;
  height: 10vh !important;
  padding: 5px;
  min-height: 150px;
  
  overflow: hidden;
}

/* 确保主体内容正确显示 */
.el-main {
  flex: 1;
  height: auto;
  padding: 5px;
  overflow: visible;
  margin-top: 5px;
}

/* 保持原有样式 */
.card {
  padding: 8px;
  background-color: white;
  border-radius: 10px;
  margin: 4px 0px;
  height: auto;
  min-height: 200px;
}

.left1, .left3 {
  height: 30vh; /* 修改为25vh以占据视窗高度的25% */
  min-height: 150px; /* 可以适当调整最小高度 */
}
.left2 {
  height: 30vh; /* 修改为25vh以占据视窗高度的25% */
  min-height: 150px; /* 可以适当调整最小高度 */
}

.right1 {
  height: 20vh; /* 修改为25vh以占据视窗高度的25% */
  min-height: 150px; /* 设置最小高度 */
}
 .right2 {
  height: 30vh; /* 修改为25vh以占据视窗高度的25% */
  min-height: 150px; /* 设置最小高度 */
}
.right3 {
  height: 40vh; /* 修改为25vh以占据视窗高度的25% */
  min-height: 150px; /* 设置最小高度 */
}
.middle {
  min-height: 600px;
  height: calc(90vh + 60px);
}

.common-layout {
  background-color: rgba(211, 211, 211, 0.278);
  border-radius: 30px;
  min-height: 90vh;
  height: auto;
  padding: 10px;
  overflow: visible;
}


</style>