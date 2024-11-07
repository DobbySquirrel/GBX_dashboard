<template>
  <div class="table-display">
    <!-- 使用表格代替卡片显示 -->
    
    <el-table
      :data="cards"
      style="width: 100%; border-radius: 10px"
      max-height="150"
      :row-class-name="tableRowClassName"
    >
      <el-table-column prop="Time" label="订单时间" />
      <el-table-column prop="Number" label="编号" />
      <el-table-column prop="Vehicle" label="载具" />
      <el-table-column prop="BoxState" label="状态" />
      <el-table-column prop="Emission" label="碳排放量" />
    </el-table>
  </div>
</template>

<script>
export default {
  name: "OrderCards",
  props: {
    DeliveryDrone_Property_DroneDeliveryOrder: {
      type: [String, null],
      required: true,
    },
    IndoorDeliveryCar_Property_IndoorDeliveryOrder: {
      type: [String, null],
      required: true,
    },
    OutdoorDeliveryCar_Property_OutdoorDeliveryOrder: {
      type: [String, null],
      required: true,
    },
  },
  data() {
    return {
      localDeliveryDrone_Property_DroneDeliveryOrder:
        this.DeliveryDrone_Property_DroneDeliveryOrder,
      localIndoorDeliveryCar_Property_IndoorDeliveryOrder:
        this.IndoorDeliveryCar_Property_IndoorDeliveryOrder,
      localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder:
        this.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder,
      cards: [],
    };
  },
  watch: {
    DeliveryDrone_Property_DroneDeliveryOrder(newVal) {
      this.localDeliveryDrone_Property_DroneDeliveryOrder = newVal;
      this.onDataUpdate();
    },
    IndoorDeliveryCar_Property_IndoorDeliveryOrder(newVal) {
      this.localIndoorDeliveryCar_Property_IndoorDeliveryOrder = newVal;
      this.onDataUpdate();
    },
    OutdoorDeliveryCar_Property_OutdoorDeliveryOrder(newVal) {
      this.localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder = newVal;
      this.onDataUpdate();
    },
  },
  mounted() {
    if (
      this.DeliveryDrone_Property_DroneDeliveryOrder &&
      this.IndoorDeliveryCar_Property_IndoorDeliveryOrder &&
      this.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder
    ) {
      this.cards = this.parseCsvData(
        this.DeliveryDrone_Property_DroneDeliveryOrder,
        this.IndoorDeliveryCar_Property_IndoorDeliveryOrder,
        this.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder
      );
    }
  },
  methods: {
    tableRowClassName({ row, rowIndex }) {
      if (row.BoxState === "Arrived") {
        return "success-row";
      }
      return "";
    },

    onDataUpdate() {
      // Check if all local properties have updated data
      if (
        this.localDeliveryDrone_Property_DroneDeliveryOrder &&
        this.localIndoorDeliveryCar_Property_IndoorDeliveryOrder &&
        this.localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder
      ) {
        // Parse and update cards with the latest data
        this.cards = this.parseCsvData(
          this.localDeliveryDrone_Property_DroneDeliveryOrder,
          this.localIndoorDeliveryCar_Property_IndoorDeliveryOrder,
          this.localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder
        );
      }
    },
    parseCsvData(
      DeliveryDrone_Property_DroneDeliveryOrder,
      IndoorDeliveryCar_Property_IndoorDeliveryOrder,
      OutdoorDeliveryCar_Property_OutdoorDeliveryOrder
    ) {
      const getLastRow = (csvData) => {
        const lines = csvData.trim().split("\n");
        const headers = lines[0].split(",");
        const lastLine = lines[lines.length - 1].split(",");

        return headers.reduce((obj, header, index) => {
          obj[header.trim()] = lastLine[index].trim();
          return obj;
        }, {});
      };

      // Get the last row for each CSV
      const latestDroneData = getLastRow(
        DeliveryDrone_Property_DroneDeliveryOrder
      );
      const latestIndoorData = getLastRow(
        IndoorDeliveryCar_Property_IndoorDeliveryOrder
      );
      const latestOutdoorData = getLastRow(
        OutdoorDeliveryCar_Property_OutdoorDeliveryOrder
      );

      // Construct card data based on the latest data
      return [
        {
          Number: latestDroneData.OrderNumber || "N/A",
          Vehicle: "Drone",
          BoxState: latestDroneData.BoxState || "Arrived",
          Emission: 10,
          Time: latestDroneData.event_time,
        },
        {
          Number: latestIndoorData.Number || "N/A",
          Vehicle: "Indoor",
          BoxState: latestIndoorData.BoxState || "N/A",
          Emission: 5,
          Time: latestDroneData.event_time,
        },
        {
          Number: latestOutdoorData.Number || "N/A",
          Vehicle: "Outdoor",
          BoxState: latestOutdoorData.BoxState || "N/A",
          Emission: 8,
          Time: latestDroneData.event_time,
        },
      ];
    },
  },
};
</script>


<style>
.table-display {
  margin: 5px;
}

.el-table .success-row {
  --el-table-tr-bg-color: #e0f7e951; /* 设置状态为 Arrived 时的行颜色为浅绿色 */
}

.el-table-column {
  opacity: 0.8; /* 设置表格及列的透明度 */
}
</style>

