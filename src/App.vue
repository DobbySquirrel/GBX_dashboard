<template>
  <div class="common-layout">
    <el-container>
      <!-- 头部 -->
      <el-header height="225px">
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
        />
      </el-header>
      <!-- 主体内容 -->
      <el-main height="750px">
        <div>
          <el-row :gutter="20">
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
            </el-col>
            <!-- 右侧新增的可视化部分 -->
            <el-col :span="5" class="right">
              <!-- 右上一: 速度数据图表 -->
              <div class="right1 card">
                <!-- <MapDisplay_drone
                  :OutdoorDeliveryCar_Property_OutdoorDeliveryOrderDetail="
                    OutdoorDeliveryCar_Property_OutdoorDeliveryOrderDetail
                  "
                  :IndoorDeliveryCar_Property_IndoorDeliveryOrderDetail="
                    IndoorDeliveryCar_Property_IndoorDeliveryOrderDetail
                  "
                  :DeliveryDrone_Property_DroneDeliveryOrderDetail="
                    DeliveryDrone_Property_DroneDeliveryOrderDetail
                  "
                /> -->
                                <RecycleCabinetOccupancyPie
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
              <div class="right2 card">
                <MapDisplay_DistributionOfOrder
                  :OutdoorDeliveryCar_Property_OutdoorCarSpeed="
                    OutdoorDeliveryCar_Property_OutdoorCarSpeed
                  "
                  :IndoorDeliveryCar_Property_IndoorCarSpeed="
                    IndoorDeliveryCar_Property_IndoorCarSpeed
                  "
                  :DeliveryDrone_Property_DroneSpeed="
                    DeliveryDrone_Property_DroneSpeed
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
import RecycleCabinetOccupancyPie from "./components/RecycleCabinetOccupancyPie.vue";
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
    RecycleCabinetOccupancyPie,
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
    },
  },
};
</script>
<style>
/* 主体内容布局 */
.card {
  padding: 10px;
  background-color: white;
  border-radius: 10px;
  margin: 10px 0px; /* 上下为 10px，左右为 0px */
}
.left1 .left2 .left3 {
  height: 250px;
}

.right1,
.right2,
.right3 {
  height: 225px;
}
.middle {
  height: 755px;
}
/* 底部样式 */
.bottom {
  padding: 20px;
  text-align: center;
}
.common-layout {
  background-color: rgba(211, 211, 211, 0.278);
  border-radius: 30px;
}
</style>