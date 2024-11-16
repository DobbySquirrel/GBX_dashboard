<template>
  <div>
    <div id="Container_Order_Distribution"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import $ from "jquery";

export default {
  name: "MapDisplay",
  props: {
    DeliveryDrone_Property_DroneDeliveryOrder: {
      type: [String, null],
      required: true
    },
    IndoorDeliveryCar_Property_IndoorDeliveryOrder: {
      type: [String, null],
      required: true
    },
    OutdoorDeliveryCar_Property_OutdoorDeliveryOrder: {
      type: [String, null],
      required: true
    }
  },
  data() {
    return {
      localDeliveryDrone_Property_DroneDeliveryOrder: this.DeliveryDrone_Property_DroneDeliveryOrder,
      localIndoorDeliveryCar_Property_IndoorDeliveryOrder: this.IndoorDeliveryCar_Property_IndoorDeliveryOrder,
      localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder: this.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder,
      unifiedData: []
    }
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
    }
  },
  mounted() {
    this.initChart();
    window.addEventListener('resize', this.handleResize);
    if (this.DeliveryDrone_Property_DroneDeliveryOrder && 
        this.IndoorDeliveryCar_Property_IndoorDeliveryOrder && 
        this.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder) {
      this.calculateAreaCounts();
      this.updateChart();
    }
  },
  unmounted() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    onDataUpdate() {
      if (this.localDeliveryDrone_Property_DroneDeliveryOrder &&
          this.localIndoorDeliveryCar_Property_IndoorDeliveryOrder &&
          this.localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder) {
        this.calculateAreaCounts();
        this.updateChart();
      }
    },

    parseCsvData(csvString) {
      const lines = csvString.trim().split('\n');
      const headers = lines[0].split(',');
      return lines.slice(1).map(line => {
        const values = line.split(',');
        return headers.reduce((obj, header, index) => {
          obj[header.trim()] = values[index].trim();
          return obj;
        }, {});
      });
    },

    calculateAreaCounts() {
      const areaCount = {};
      
      // 处理无人机订单数据
      const droneData = this.parseCsvData(this.localDeliveryDrone_Property_DroneDeliveryOrder);
      droneData.forEach(order => {
        const area = order.ReceiverAddress;
        areaCount[area] = (areaCount[area] || 0) + 1;
      });

      // 处理室内配送车订单数据
      const indoorData = this.parseCsvData(this.localIndoorDeliveryCar_Property_IndoorDeliveryOrder);
      indoorData.forEach(order => {
        const area = order.Area;
        areaCount[area] = (areaCount[area] || 0) + 1;
      });

      // 处理室外配送车订单数据
      const outdoorData = this.parseCsvData(this.localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder);
      outdoorData.forEach(order => {
        const area = order.Area;
        areaCount[area] = (areaCount[area] || 0) + 1;
      });

      // 生成最终数据
      this.unifiedData = [
        { name: "W1", value: areaCount["W1"] || 0 },
        { name: "W2", value: areaCount["W2"] || 0 },
        { name: "W3", value: areaCount["W3"] || 0 },
        { name: "W4", value: areaCount["W4"] || 0 },
        { name: "E1", value: areaCount["E1"] || 0 },
        { name: "E2", value: areaCount["E2"] || 0 },
        { name: "E3", value: areaCount["E3"] || 0 },
        { name: "E4", value: areaCount["E4"] || 0 },
        { name: "Library", value: areaCount["Library"] || 0 },
        { name: "Lecture Halls", value: areaCount["Lecture Halls"] || 0 },
        { name: "Administration Building", value: areaCount["Administration Building"] || 0 },
        { name: "Activity Center", value: areaCount["Activity Center"] || 0 },
        { name: "Block 1A", value: areaCount["Block 1A"] || 0 },
        { name: "Block 1B", value: areaCount["Block 1B"] || 0 },
        { name: "Block 3", value: areaCount["Block 3"] || 0 },
        { name: "Block 5A", value: areaCount["Block 5A"] || 0 },
        { name: "Block 5B", value: areaCount["Block 5B"] || 0 },
        { name: "Block 5C", value: areaCount["Block 5C"] || 0 },
        { name: "Block 2A", value: areaCount["Block 2A"] || 0 },
        { name: "Block 2B", value: areaCount["Block 2B"] || 0 },
        { name: "Block 4A", value: areaCount["Block 4A"] || 0 },
        { name: "Block 4B", value: areaCount["Block 4B"] || 0 },
        { name: "Block 6A", value: areaCount["Block 6A"] || 0 },
        { name: "Block 6B", value: areaCount["Block 6B"] || 0 },
        { name: "Block 6C", value: areaCount["Block 6C"] || 0 },
        { name: "Bleachers", value: areaCount["Bleachers"] || 0 },
        { name: "Stadium", value: areaCount["Stadium"] || 0 },
        { name: "Canteen", value: areaCount["Canteen"] || 0 },
        { name: "10D", value: areaCount["10D"] || 0 },
        { name: "10C", value: areaCount["10C"] || 0 },
        { name: "10B", value: areaCount["10B"] || 0 },
        { name: "10A", value: areaCount["10A"] || 0 },
        { name: "9D", value: areaCount["9D"] || 0 },
        { name: "9C", value: areaCount["9C"] || 0 },
        { name: "9B", value: areaCount["9B"] || 0 },
        { name: "9A", value: areaCount["9A"] || 0 },
        { name: "NN-8", value: areaCount["NN-8"] || 0 },
        { name: "NN-6", value: areaCount["NN-6"] || 0 },
        { name: "NN-9", value: areaCount["NN-9"] || 0 },
        { name: "NN-2", value: areaCount["NN-2"] || 0 },
        { name: "NN-3", value: areaCount["NN-3"] || 0 },
        { name: "NN-1", value: areaCount["NN-1"] || 0 },
        { name: "NN-4-5", value: areaCount["NN-4-5"] || 0 },
        { name: "Data Center", value: areaCount["Data Center"] || 0 },
        { name: "Energy Center", value: areaCount["Energy Center"] || 0 },
        { name: "Fire Control Center", value: areaCount["Fire Control Center"] || 0 }
      ];
    },

    async initChart() {
      var dom = document.getElementById("Container_Order_Distribution");
      this.myChart = echarts.init(dom, null, {
        renderer: "canvas",
        useDirtyRect: false,
      });
      
      try {
        const response = await fetch("/hkust_gz_map.svg");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const svg = await response.text();
        echarts.registerMap("hkust_gz_map", { svg: svg });
        this.updateChart();
      } catch (error) {
        console.error("加载SVG失败:", error);
        alert("地图文件加载失败，请确认文件存在");
      }
    },

    updateChart() {
      const maxValue = Math.max(...this.unifiedData.map(item => item.value || 0));
      
      const option = {
        title: {
          text: "Order Distribution Map",
          left: "center",
          textStyle: {
            color: "#44652a",
          },
          top: "0%",
        },
        tooltip: {},
        visualMap: {
          min: 0,
          max: maxValue > 0 ? maxValue : 10, // 使用实际数据的最大值
          orient: "horizontal",
          text: ["", "Order"],
          realtime: true,
          top: "80%",
          textStyle: { fontSize: 12 },
          calculable: true,
          inRange: {
            color: ["white", "#FFF2CD", "#91CC75", "green"],
          },
          label: {
            show: true,
            textBorderColor: "white",
            textBorderWidth: 2,
          },
        },
        grid: {
          top: "60%",
        },
        series: [
          {
            name: "Orders",
            type: "map",
            map: "hkust_gz_map",
            emphasis: {
              label: {
                show: false,
              },
            },
            selectedMode: false,
            data: this.unifiedData
          },
        ],
      };

      if (this.myChart) {
        this.myChart.setOption(option);
      }
    },

    handleResize() {
      if (this.myChart) {
        this.myChart.resize();
      }
    }
  }
};
</script>

<style scoped>
#Container_Order_Distribution {
  width: 90%;
  height: 25vh;
  min-height: 200px;
  padding: 5px;
}
</style>
