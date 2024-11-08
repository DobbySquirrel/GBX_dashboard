<template>
  <div class="common-layout">
    <el-container>
      <!-- 头部 -->
      <el-header height="200px">
        <AppHeader
          :DeliveryDrone_Property_DroneDeliveryOrder="
            DeliveryDrone_Property_DroneDeliveryOrder
          "
          :IndoorDeliveryCar_Property_IndoorDeliveryOrder="
            IndoorDeliveryCar_Property_IndoorDeliveryOrder
          "
          :OutdoorDeliveryCar_Property_OutdoorDeliveryOrder="
            OutdoorDeliveryCar_Property_OutdoorDeliveryOrder
          "
          :Delivery_Locker_Property_RecycleDelivery="
            Delivery_Locker_Property_RecycleDelivery
          "
          :Box_owner="Box_owner"
        />
      </el-header>
      <!-- 主体内容 -->
      <el-main>
        <div>
          <el-row :gutter="10">
            <!-- 左侧部分 -->
            <el-col :span="5" class="left">
              <!-- 左上一: 占用率 -->
              <div class="left1 card">
                <OccupancyChart
                  :OutdoorDeliveryCar_Property_OutdoorCarState="
                    OutdoorDeliveryCar_Property_OutdoorCarState
                  "
                  :IndoorDeliveryCar_Property_IndoorCarState="
                    IndoorDeliveryCar_Property_IndoorCarState
                  "
                  :DeliveryDrone_Property_DroneState="
                    DeliveryDrone_Property_DroneState
                  "
                  :Delivery_Locker_Property_InputDelivery="
                    Delivery_Locker_Property_InputDelivery
                  "
                />
              </div>

              <!-- 左上二: 订单数量趋势 -->
              <div class="left2 card">
                <OrderCountChart
                  :DeliveryDrone_Property_DroneDeliveryOrder="
                    DeliveryDrone_Property_DroneDeliveryOrder
                  "
                  :IndoorDeliveryCar_Property_IndoorDeliveryOrder="
                    IndoorDeliveryCar_Property_IndoorDeliveryOrder
                  "
                  :OutdoorDeliveryCar_Property_OutdoorDeliveryOrder="
                    OutdoorDeliveryCar_Property_OutdoorDeliveryOrder
                  "
                />
              </div>
              <!-- 回收柜使用情况和回收柜占用情况饼图 -->
              <div class="left3 card">

                                  <RecycleCabinetOccupancyChart
                    :Delivery_Locker_Property_InputDelivery="
                      Delivery_Locker_Property_InputDelivery
                    "
                    :Delivery_Locker_Property_OutputDelivery="
                      Delivery_Locker_Property_OutputDelivery
                    "
                    :Delivery_Locker_Property_RecycleDelivery="
                      Delivery_Locker_Property_RecycleDelivery
                    "
                  />
              </div>
            </el-col>

            <!-- 中间地图部分 -->
            <el-col :span="14" class="middle card">
              <MapDisplay_indoorCar
                :OutdoorDeliveryCar_Property_OutdoorCarState="
                  OutdoorDeliveryCar_Property_OutdoorCarState
                "
                :IndoorDeliveryCar_Property_IndoorCarState="
                  IndoorDeliveryCar_Property_IndoorCarState
                "
                :DeliveryDrone_Property_DroneState="
                  DeliveryDrone_Property_DroneState
                "
              />

              <CardDisplay
            
                :Box_owner="Box_owner"
              />
            </el-col>
            <!-- 右侧新增的可视化部分 -->
            <el-col :span="5" class="right">
              <!-- 右上一: 速度数据图表 -->
              <div class="right1 card">
                                <RecycleBoxStatusPie
:Box_owner="Box_owner"
                />
              </div>
              <div class="right2 card">
                <MapDisplay_DistributionOfOrder
                :DeliveryDrone_Property_DroneDeliveryOrder="
                    DeliveryDrone_Property_DroneDeliveryOrder
                  "
                  :IndoorDeliveryCar_Property_IndoorDeliveryOrder="
                    IndoorDeliveryCar_Property_IndoorDeliveryOrder
                  "
                  :OutdoorDeliveryCar_Property_OutdoorDeliveryOrder="
                    OutdoorDeliveryCar_Property_OutdoorDeliveryOrder
                  "
                />
              </div>
                            <div class="right3 card">
                <MapDisplay_outdoorCar
                  :Delivery_Locker_Property_InputDelivery="
                    Delivery_Locker_Property_InputDelivery
                  "
                  :Delivery_Locker_Property_OutputDelivery="
                    Delivery_Locker_Property_OutputDelivery
                  "
                  :Delivery_Locker_Property_RecycleDelivery="
                    Delivery_Locker_Property_RecycleDelivery
                  "
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
import AppHeader from "./components/Header.vue";
import CardDisplay from "./components/CardDisplay.vue";
import ObsDownloader from "./components/ObsDownloader.vue";
import OccupancyChart from "./components/OccupancyChart.vue";
import OrderCountChart from "./components/OrderCountChart.vue";
import RecycleCabinetOccupancyChart from "./components/RecycleCabinetOccupancyChart.vue";
import RecycleBoxStatusPie from "./components/RecycleBoxStatusPie.vue";
import MapDisplay_indoorCar from "./components/MapDisplay_indoorCar.vue"; // 地图展示组件
import MapDisplay_outdoorCar from "./components/MapDisplay_outdoorCar.vue"; // 地图展示组件
import MapDisplay_drone from "./components/MapDisplay_drone.vue"; // 地图展示组件
import MapDisplay_DistributionOfOrder from "./components/MapDisplay_DistributionOfOrder.vue"; // 地图展示组件
import { ElButton } from "element-plus";
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
  },
  data() {
    return {
      IndoorDeliveryCar_Property_IndoorCarState: "", // 新增室内车数据
      OutdoorDeliveryCar_Property_OutdoorCarState: "", // 新增室外车数据
      DeliveryDrone_Property_DroneState: "", // 新增无人机数据
      DeliveryDrone_Property_DroneDeliveryOrder: "", // 新增无人机交付订单数据
      Delivery_Locker_Property_InputDelivery: "", // 新增输入交付数据
      Delivery_Locker_Property_OutputDelivery: "", // 新增输出交付数据
      Delivery_Locker_Property_RecycleDelivery: "", // 新增回收交付数据
      IndoorDeliveryCar_Property_IndoorDeliveryOrder: "", // 新增室内车交付订单数据
      OutdoorDeliveryCar_Property_OutdoorDeliveryOrder: "", // 新增室外车交付订单数据
      Box_owner: "", // 新增 Box_owner 数据
    };
  },
  methods: {
    handleDataUpdate({ file, content }) {
      const contentString = content || "";
      if (file.includes("DroneDeliveryOrder")) {
        this.DeliveryDrone_Property_DroneDeliveryOrder = contentString;
      }
      if (file.includes("InputDelivery")) {
        this.Delivery_Locker_Property_InputDelivery = contentString;
      }
      if (file.includes("OutputDelivery")) {
        this.Delivery_Locker_Property_OutputDelivery = contentString;
      }
      if (file.includes("RecycleDelivery")) {
        this.Delivery_Locker_Property_RecycleDelivery = contentString;
      }
      if (file.includes("IndoorDeliveryOrder")) {
        this.IndoorDeliveryCar_Property_IndoorDeliveryOrder = contentString;
      }
      if (file.includes("OutdoorDeliveryOrder")) {
        this.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder = contentString;
      }
      if (file.includes("DroneState")) {
        this.DeliveryDrone_Property_DroneState = contentString;
      }
      if (file.includes("IndoorCarState")) {
        this.IndoorDeliveryCar_Property_IndoorCarState = contentString;
      }
      if (file.includes("OutdoorCarState")) {
        this.OutdoorDeliveryCar_Property_OutdoorCarState = contentString;
      }
      if (file.includes("Box_owner")) {
        this.Box_owner = contentString;
      }
    },
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
  flex-shrink: 0;  /* 防止header被压缩 */
  height: 25vh !important; /* 设置为视窗高度的20% */
  padding: 10px;

}

/* 确保主体内容正确显示 */
.el-main {
  flex: 1;
  height: auto;
  padding: 10px;
  overflow: visible;
}

/* 保持原有样式 */
.card {
  padding: 10px;
  background-color: white;
  border-radius: 10px;
  margin: 5px 0px;
  height: auto;
  min-height: 200px;
}

.left1, .left3 {
  height: 25vh; /* 修改为25vh以占据视窗高度的25% */
  min-height: 150px; /* 可以适当调整最小高度 */
}
.left2 {
  height: 28vh; /* 修改为25vh以占据视窗高度的25% */
  min-height: 150px; /* 可以适当调整最小高度 */
}

.right1 {
  height: 15vh; /* 修改为25vh以占据视窗高度的25% */
  min-height: 150px; /* 设置最小高度 */
}
 .right2 {
  height: 25vh; /* 修改为25vh以占据视窗高度的25% */
  min-height: 150px; /* 设置最小高度 */
}
.right3 {
  height: 35vh; /* 修改为25vh以占据视窗高度的25% */
  min-height: 150px; /* 设置最小高度 */
}
.middle {
  min-height: 745px;
  height: auto;
}

.common-layout {
  background-color: rgba(211, 211, 211, 0.278);
  border-radius: 30px;
  min-height: 100vh;
  height: auto;
  padding: 10px;
  overflow: visible;
}


</style>