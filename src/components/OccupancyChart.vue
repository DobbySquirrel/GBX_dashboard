<template>
  <div class="chart-container">
    <div id="OccupancyChart"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'OccupancyChart',
  props: {
    OutdoorDeliveryCar_Property_OutdoorCarState: {
      type: [String, null],
      required: true
    },
    IndoorDeliveryCar_Property_IndoorCarState: {
      type: [String, null],
      required: true
    },
    DeliveryDrone_Property_DroneState: {
      type: [String, null],
      required: true
    },
    Delivery_Locker_Property_InputDelivery: {
      type: [String, null],
      required: true
    }
  },
  data() {
    return {
      ActivatedValue: [],
      UnactivatedValue: [],
    localOutdoorCarState: this.OutdoorDeliveryCar_Property_OutdoorCarState,
    localIndoorCarState: this.IndoorDeliveryCar_Property_IndoorCarState,
    localDroneState: this.DeliveryDrone_Property_DroneState,
    localLockerState: this.Delivery_Locker_Property_InputDelivery,
    };
  },
watch: {
   OutdoorDeliveryCar_Property_OutdoorCarState(newVal) {
    this.localOutdoorCarState = newVal;
    this.onDataUpdate();
  },
  IndoorDeliveryCar_Property_IndoorCarState(newVal) {
    this.localIndoorCarState = newVal;
    this.onDataUpdate();
  },
  DeliveryDrone_Property_DroneState(newVal) {
    this.localDroneState = newVal;
    this.onDataUpdate();
  },
  Delivery_Locker_Property_InputDelivery(newVal) {
    this.localLockerState = newVal;
    this.onDataUpdate();
  }
},

  mounted() {
    this.initChart();
    // 添加窗口大小变化监听
    window.addEventListener('resize', this.handleResize);
    if (this.OutdoorDeliveryCar_Property_OutdoorCarState && 
        this.IndoorDeliveryCar_Property_IndoorCarState && 
        this.DeliveryDrone_Property_DroneState && 
        this.Delivery_Locker_Property_InputDelivery) {
      this.parseCsvData(
        this.OutdoorDeliveryCar_Property_OutdoorCarState,
        this.IndoorDeliveryCar_Property_IndoorCarState,
        this.DeliveryDrone_Property_DroneState,
        this.Delivery_Locker_Property_InputDelivery
      );
    }
  },

  unmounted() {
    // 组件销毁时移除监听
    window.removeEventListener('resize', this.handleResize);
  },

  methods: {
    onDataUpdate() {
    // 检查所有本地属性是否都有最新数据
    if (
      this.localOutdoorCarState &&
      this.localIndoorCarState &&
      this.localDroneState &&
      this.localLockerState
    ) {
      // 使用本地数据进行解析和图表更新
      this.parseCsvData(
        this.localOutdoorCarState,
        this.localIndoorCarState,
        this.localDroneState,
        this.localLockerState
      );
    }
  },
  parseCsvData(OutdoorCarState, IndoorCarState, DroneState, LockerState) {
    // Helper function to count the number of activated rows
    const countActivatedRows = (csvData, name) => {
      // 如果数据为空，返回0
      if (!csvData || csvData.trim() === '') {
        return 0;
      }

      const lines = csvData.trim().split('\n');
      // 如果只有头部或没有数据，返回0
      if (lines.length <= 1) {
        return 0;
      }

      const headers = lines[0].split(',');
      const data = lines.slice(1).map(line => {
        const values = line.split(',');
        return headers.reduce((obj, header, index) => {
          obj[header.trim()] = values[index] ? values[index].trim() : '';
          return obj;
        }, {});
      });

      // 简化状态判断逻辑
      let activeCount = 0;
      if (name === "Outdoor" || name === "Indoor") {
        activeCount = data.filter(row => row.Status === "Active").length;
      } else if (name === "Drone") {
        activeCount = data.filter(row => row.State === "Active").length;
      } else if (name === "Locker") {
        activeCount = data.filter(row => row.Status === "Active").length;
      }

      return Math.min(activeCount, 1); // 确保返回值不超过1
    };

    // 计算每种类型的激活数量
    const outdoorCarActivated = countActivatedRows(OutdoorCarState, 'Outdoor');
    const indoorCarActivated = 1; // 强制设置为1
    const droneActivated = countActivatedRows(DroneState, 'Drone');
    const lockerActivated = countActivatedRows(LockerState, 'Locker');

    // 设置激活值
    this.ActivatedValue = [
      { value: lockerActivated, symbol: this.getSymbolForVehicleType('Locker'), symbolRepeat: 'true', symbolSize: ["60%", "60%"] },
      { value: indoorCarActivated, symbol: this.getSymbolForVehicleType('Indoor_Car'), symbolRepeat: 'true', symbolSize: ["70%", "50%"] },
      { value: outdoorCarActivated, symbol: this.getSymbolForVehicleType('Outdoor_Car'), symbolRepeat: 'true', symbolSize: ["70%", "50%"] },
      { value: droneActivated, symbol: this.getSymbolForVehicleType('Drone'), symbolRepeat: 'true', symbolSize: ["65%", "65%"] }
    ];

    // 设置总数值（都为1）
    this.UnactivatedValue = [
      { value: 1, symbol: this.getSymbolForVehicleType('Locker'), symbolRepeat: 'true', animationDuration: 0, symbolSize: ["60%", "60%"] },
      { value: 1, symbol: this.getSymbolForVehicleType('Indoor_Car'), symbolRepeat: 'true', animationDuration: 0, symbolSize: ["70%", "50%"] },
      { value: 1, symbol: this.getSymbolForVehicleType('Outdoor_Car'), symbolRepeat: 'true', animationDuration: 0, symbolSize: ["70%", "50%"] },
      { value: 1, symbol: this.getSymbolForVehicleType('Drone'), symbolRepeat: 'true', animationDuration: 0, symbolSize: ["65%", "65%"] }
    ];

    // 更新图表
    this.updateChart();
  },
  
  getSymbolForVehicleType(vehicleType) {
    const pathSymbols = {
  Locker:
    'path://M151.552 913.408h20.48v49.152c0 24.576 20.48 40.96 40.96 40.96H368.64c20.48 0 40.96-16.384 40.96-40.96v-49.152h204.8v49.152c0 24.576 20.48 40.96 40.96 40.96h155.648c24.576 0 40.96-16.384 40.96-40.96v-49.152h20.48c73.728 0 131.072-57.344 131.072-131.072V151.552c0-73.728-57.344-131.072-131.072-131.072H151.552C77.824 20.48 20.48 77.824 20.48 151.552v630.784c0 73.728 57.344 131.072 131.072 131.072z m-8.192-221.184h69.632c8.192 0 16.384-8.192 16.384-16.384v-118.784c0-8.192-8.192-16.384-16.384-16.384H143.36V397.312h69.632c8.192 0 16.384-8.192 16.384-16.384v-122.88c0-8.192-8.192-12.288-16.384-12.288H143.36V151.552c0-4.096 4.096-8.192 8.192-8.192h720.896c4.096 0 8.192 4.096 8.192 8.192v630.784c0 4.096-4.096 8.192-8.192 8.192H151.552c-4.096 0-8.192-4.096-8.192-8.192v-90.112zM626.688 495.616v69.632c0 24.576 16.384 40.96 40.96 40.96s40.96-16.384 40.96-40.96v-61.44-8.192c32.768-16.384 57.344-49.152 57.344-90.112 0-53.248-45.056-98.304-98.304-98.304-53.248 0-98.304 45.056-98.304 98.304 0 40.96 24.576 77.824 57.344 90.112z',
  Drone:
    'path://M343.2 177.46C324.6 129.78 278.2 96 224 96c-70.7 0-128 57.3-128 128 0 54.2 33.78 100.6 81.46 119.2l76.94 101c-10 3.2-20 3.8-30.4 3.8C100.28 448 0 347.8 0 224 0 100.28 100.28 0 224 0c123.8 0 224 100.28 224 224 0 10.4-0.6 20.6-3.8 30.4l-101-76.94zM426.6 320h170.8l139.2-104.4c4-31.38 31-55.6 63.4-55.6 35.4 0 64 28.66 64 64 0 32.4-24.2 59.4-55.6 63.4L704 426.6v170.8l104.4 139.2c31.4 4 55.6 31 55.6 63.4 0 35.4-28.6 64-64 64-32.4 0-59.4-24.2-63.4-55.6L597.4 704h-170.8l-139.2 104.4c-4 31.4-31 55.6-63.4 55.6-35.34 0-64-28.6-64-64 0-32.4 24.22-59.4 55.6-63.4l104.4-139.2v-170.8l-104.4-139.2C184.22 283.4 160 256.4 160 224c0-35.34 28.66-64 64-64 32.4 0 59.4 24.22 63.4 55.6l139.2 104.4zM224 1024C100.28 1024 0 923.8 0 800s100.28-224 224-224c10.4 0 20.4 0.6 30.4 2l-76.94 102.8C129.78 699.4 96 745.8 96 800c0 70.6 57.3 128 128 128 54.2 0 100.6-33.8 119.2-81.4l101-77c3.2 10 3.8 20 3.8 30.4 0 123.8-100.2 224-224 224z m354-769.6c-1.4-10-2-20-2-30.4C576 100.28 676.2 0 800 0s224 100.28 224 224c0 123.8-100.2 224-224 224-10.4 0-20.4-0.6-30.4-3.8l77-101c47.6-18.6 81.4-65 81.4-121 0-68.9-57.4-128-128-128-54.2 0-100.6 35.58-119.2 83.26L578 254.4zM576 800c0-10.4 0.6-20.4 2-30.4l102.8 77c18.6 47.6 65 81.4 119.2 81.4 70.6 0 128-57.4 128-128 0-54.2-33.8-100.6-81.4-119.2L769.6 578c10-1.4 20-3.8 30.4-3.8 123.8 0 224 102 224 225.8 0 123.8-100.2 224-224 224s-224-100.2-224-224z',
  Indoor_Car:'path://M821.333333 213.333333a42.666667 42.666667 0 0 1 36.181334 20.053334l2.602666 4.821333 117.333334 256a42.666667 42.666667 0 0 1 3.626666 13.226667L981.333333 512v256a42.666667 42.666667 0 0 1-37.674666 42.368L938.666667 810.666667h-21.333334a128 128 0 0 1-255.786666 7.509333L661.333333 810.666667H426.666667a128 128 0 0 1-255.786667 7.509333L170.666667 810.666667H128a42.666667 42.666667 0 0 1-42.368-37.674667L85.333333 768v-170.666667a42.666667 42.666667 0 0 1 37.674667-42.368L128 554.666667h512V256a42.666667 42.666667 0 0 1 37.674667-42.368L682.666667 213.333333h138.666666z m-32 554.666667a42.666667 42.666667 0 1 0 0 85.333333 42.666667 42.666667 0 0 0 0-85.333333zM298.666667 768a42.666667 42.666667 0 1 0 0 85.333333 42.666667 42.666667 0 0 0 0-85.333333z m341.333333-128H170.666667v85.333333h32.597333c23.466667-26.197333 57.472-42.666667 95.402667-42.666666 37.930667 0 71.978667 16.469333 95.402666 42.666666H640v-85.333333z m153.941333-341.333333H725.333333v401.109333A127.402667 127.402667 0 0 1 789.333333 682.666667c37.930667 0 71.978667 16.469333 95.402667 42.666666H896v-203.946666L793.941333 298.666667zM554.666667 128a42.666667 42.666667 0 0 1 42.666666 42.666667v298.666666a42.666667 42.666667 0 0 1-42.666666 42.666667H149.333333a42.666667 42.666667 0 0 1-41.728-33.706667l-64-298.666666A42.666667 42.666667 0 0 1 85.333333 128z m256-42.666667a42.666667 42.666667 0 0 1 4.992 85.034667L810.666667 170.666667h-128a42.666667 42.666667 0 0 1-4.992-85.034667L682.666667 85.333333h128z',
  Outdoor_Car: 'path://M874.666667 853.333333v63.957334A64.064 64.064 0 0 1 810.666667 981.333333c-35.349333 0-64-28.565333-64-64.042666V853.333333H277.333333v63.957334A64.064 64.064 0 0 1 213.333333 981.333333c-35.349333 0-64-28.565333-64-64.042666V853.333333c-58.816-0.085333-106.666667-47.893333-106.666666-106.517333V490.517333c0-37.013333 18.88-69.568 47.573333-88.661333l66.133333-264.661333C169.728 83.904 222.506667 42.666667 277.269333 42.666667h469.504c54.869333 0 107.541333 41.258667 120.853334 94.528l66.197333 264.789333A106.453333 106.453333 0 0 1 981.333333 490.517333v256.298667A106.602667 106.602667 0 0 1 874.666667 853.333333zM784.832 157.888C780.992 142.549333 762.432 128 746.752 128H277.248c-15.573333 0-34.24 14.592-38.08 29.888L182.634667 384h658.709333l-56.533333-226.112zM128 490.517333v256.298667c0 11.52 9.685333 21.184 21.482667 21.184h725.034666A21.269333 21.269333 0 0 0 896 746.816V490.517333c0-11.52-9.685333-21.184-21.482667-21.184H149.482667A21.269333 21.269333 0 0 0 128 490.517333zM277.333333 682.666667a64 64 0 1 1 0-128 64 64 0 0 1 0 128z m469.333334 0a64 64 0 1 1 0-128 64 64 0 0 1 0 128z',
  
    };
    return pathSymbols[vehicleType];
  },

    initChart() {
      var chartDom = document.getElementById('OccupancyChart');
      this.myChart = echarts.init(chartDom);
      
      // 所有值都设为1
      this.ActivatedValue = [
        { value: 1, symbol: this.getSymbolForVehicleType('Locker'), symbolRepeat: 'true', symbolSize: ["60%", "60%"] },
        { value: 1, symbol: this.getSymbolForVehicleType('Indoor_Car'), symbolRepeat: 'true', symbolSize: ["70%", "50%"] },
        { value: 1, symbol: this.getSymbolForVehicleType('Outdoor_Car'), symbolRepeat: 'true', symbolSize: ["70%", "50%"] },
        { value: 1, symbol: this.getSymbolForVehicleType('Drone'), symbolRepeat: 'true', symbolSize: ["65%", "65%"] }
      ];

      this.UnactivatedValue = [
        { value: 1, symbol: this.getSymbolForVehicleType('Locker'), symbolRepeat: 'true', animationDuration: 0, symbolSize: ["60%", "60%"] },
        { value: 1, symbol: this.getSymbolForVehicleType('Indoor_Car'), symbolRepeat: 'true', animationDuration: 0, symbolSize: ["70%", "50%"] },
        { value: 1, symbol: this.getSymbolForVehicleType('Outdoor_Car'), symbolRepeat: 'true', animationDuration: 0, symbolSize: ["70%", "50%"] },
        { value: 1, symbol: this.getSymbolForVehicleType('Drone'), symbolRepeat: 'true', animationDuration: 0, symbolSize: ["65%", "65%"] }
      ];

      this.updateChart();
    },

updateChart() {
  const option = {
    title: {
      text: 'Vehicle Occupancy Rate',
      left: "center",
      textStyle: {
        color: "#44652a",
        fontSize: 12
      },
      top: '0%',
    },
    legend: {
      data: ['Activated', 'Count'],
      top: '10%',
      left: 'center',
      textStyle: {
        fontSize: 10  
      }

    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      containLabel: true,
      left: '0%', // 向左对齐
      bottom: '0%',
      top: '18%',
    },
    yAxis: {
      data: ['Locker', 'Indoor_Car', 'Outdoor_Car', 'Drone'],
      inverse: true,
      position: 'left',
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        margin: 30,
        fontSize: 10,
      },
    },
    xAxis: {
      max: 14,
      splitLine: { show: true },
      axisLabel: { show: false },
      axisTick: { show: false },
      axisLine: { show: false }
    },
    series: [
      {
        type: 'pictorialBar',
        name: 'Activated',
        barCategoryGap: 0,
        symbolBoundingData: 10,
        animationDuration: 0,
        symbolSize: ["80%", "80%"],
        z: 10,
        label: {
          show: true,
          position: 'left',
          offset: [0, 0],
          fontSize: 10,
          color: "#67c23a",
        },
        itemStyle: {
          color: '#91CC75'
        },
        data: this.ActivatedValue
      },
      {
        name: 'Count',
        type: 'pictorialBar',
        animationDuration: 0,
        symbolBoundingData: 10,
        symbolSize: ["80%", "80%"],
        label: {
          show: true,
          position: 'right',
          offset: [10, 0],
          fontSize: 10,
        },
        itemStyle: {
          color: 'rgba(128, 128, 128, 0.8)'
        },
        data: this.UnactivatedValue
      }
    ]
  };

  this.myChart.setOption(option);
},

    handleResize() {
      if (this.myChart) {
        this.myChart.resize();
      }
    },
  }
};
</script>
<style scoped>
.chart-container {
  width: 100%;
  height: 30vh; /* 修改为25vh以占据视窗高度的25% */
  display: flex;
  flex-direction: column;
}

#OccupancyChart {
  width: 100%;
  height: 100%;
  flex: 1;
  min-height: 150px; /* 可以适当调整最小高度 */
}
</style>

