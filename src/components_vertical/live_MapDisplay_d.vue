<template>
  <div class="map-wrapper">
    <div class="title-container">
      <el-text class="mx-1" style="font-size: 16px; color: #44652a; font-weight: bold;"
        >Live</el-text
      >
    </div>
    <div id="container_indoorCar" class="map-container"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import $ from "jquery";
import { droneSymbolPath } from "../assets/symbols/droneSymbol.js";
import { CarSymbolPath } from "../assets/symbols/CarSymbol.js"; // Still used for Indoor Car
import socket from "../api/socket.js";

export default {
  name: "MapDisplay",
  props: {
    // These props are now unused based on the real-time data driven approach
    IndoorDeliveryCar_Property_IndoorCarState: {
      type: String,
      default: null,
    },
    DeliveryDrone_Property_DroneState: {
      type: String,
      default: null,
    },
    pageType: {
      type: String,
      default: 'all',
    }
  },
  data() {
    // Define the start and end points for each vehicle's path

    const indoorCarPathPoints = [
      [100, 100], // Indoor car start point (example coordinates)
      [500, 600]  // Indoor car end point (example coordinates)
    ];
        const dronePathPoints = [
      [153.00, 178.50], // Drone start point
      [153.00, 189.50], // 转折点
      [157.50, 203.00], // 转折点
      [157.50, 211.50], // 转折点
      [157.50, 221.00], // 转折点
      [157.50, 231.00], // 转折点
      [157.50, 240.00], // 转折点
      [157.50, 251.00], // 转折点
      [157.50, 260.00], // 转折点
      [162.50, 276.50], // 转折点
      [168.00, 285.50]  // Drone end point
    ];
    const vector1PathPoints = [
      [97.50, 591.00], // 起始点
      [120.00, 571.00], // 转折点
      [134.50, 555.00], // 转折点
      [147.50, 540.00], // 转折点
      [156.00, 523.00], // 转折点
      [162.50, 501.50], // 转折点
      [169.00, 482.50], // 转折点
      [179.50, 470.50], // 转折点
      [203.00, 457.00], // 转折点
      [237.00, 443.00], // 转折点
      [258.50, 431.00], // 转折点
      [267.00, 418.50], // 转折点
      [267.00, 397.00], // 转折点
      [258.50, 378.00], // 转折点
      [252.00, 356.50], // 转折点
      [237.00, 344.00], // 转折点
      [220.00, 344.00], // 转折点
      [203.00, 367.50], // 转折点
      [198.24, 387.48], // 转折点
      [190.00, 397.00], // 转折点
      [183.41, 404.62], // 转折点
      [169.00, 412.00], // 转折点
      [169.00, 412.00], // 转折点
      [161.65, 418.00], // 转折点
      [156.00, 418.50], // 转折点
      [144.17, 419.55], // 转折点
      [134.50, 397.00], // 转折点
      [134.50, 397.00], // 转折点
      [122.77, 380.03], // 转折点
      [120.00, 367.50], // 转折点
      [117.47, 356.06], // 转折点
      [120.00, 337.50], // 转折点
      [120.00, 337.50]  // 结束点
    ];

    

return {
  indoorCarPosition: indoorCarPathPoints[0],
  indoorCarChart: null,
  dronePosition: dronePathPoints[0],

  indoorCarStatus: "运送中 (0%)",
  droneStatus: "运送中 (0%)",

  // Arrays to store historical data for drawing trajectories
  droneHistory: [],
  indoorCarHistory: [],
  historyBufferSize: 50, // Number of historical points to retain for trajectories

  dronePathPoints: dronePathPoints,
  indoorCarPathPoints: indoorCarPathPoints,
  vector1PathPoints: vector1PathPoints, // 添加这一行！

  convertedLocations: [] // For fixed locations, if any
};
  },
  methods: {
    /**
     * Helper function to interpolate a point on a line given a percentage.
     * The percentage value (0 to 1) determines the position between start and end.
     */
     interpolateMultiSegmentPath(pathPoints, percentage) {
  if (!pathPoints || pathPoints.length < 2) return pathPoints[0] || [0, 0];
  
  const clampedPercentage = Math.max(0, Math.min(1, parseFloat(percentage)));
  
  // Calculate total path length
  let totalLength = 0;
  const segmentLengths = [];
  
  for (let i = 0; i < pathPoints.length - 1; i++) {
    const dx = pathPoints[i + 1][0] - pathPoints[i][0];
    const dy = pathPoints[i + 1][1] - pathPoints[i][1];
    const segmentLength = Math.sqrt(dx * dx + dy * dy);
    segmentLengths.push(segmentLength);
    totalLength += segmentLength;
  }
  
  // Find which segment we're in
  let currentLength = 0;
  let targetLength = clampedPercentage * totalLength;
  
  for (let i = 0; i < pathPoints.length - 1; i++) {
    if (targetLength <= currentLength + segmentLengths[i]) {
      // We're in this segment
      const segmentProgress = (targetLength - currentLength) / segmentLengths[i];
      const start = pathPoints[i];
      const end = pathPoints[i + 1];
      
      const x = start[0] + (end[0] - start[0]) * segmentProgress;
      const y = start[1] + (end[1] - start[1]) * segmentProgress;
      return [x, y];
    }
    currentLength += segmentLengths[i];
  }
  
  // If we reach here, we're at the end
  return pathPoints[pathPoints.length - 1];
},
    interpolatePoint(start, end, percentage) {
      // Ensure percentage is a number and clamped between 0 and 1
      const clampedPercentage = Math.max(0, Math.min(1, parseFloat(percentage)));
      const x = start[0] + (end[0] - start[0]) * clampedPercentage;
      const y = start[1] + (end[1] - start[1]) * clampedPercentage;
      return [x, y];
    },

    /**
     * Dynamically generates the series data for ECharts based on the current pageType.
     */
     getSeriesBasedOnPageType() {
      const baseSeries = [
        // Static scatter points for fixed locations (if any)
        {
          type: 'scatter',
          coordinateSystem: 'geo',
          geoIndex: 0,
          symbol: 'pin',
          symbolSize: 40,
          itemStyle: {
            color: '#999999'
          },
          encode: {
            tooltip: 2
          },
          label: {
            show: true,
            formatter: function(params) {
              return params.data[2];
            },
            textBorderColor: "black",
            color: "white",
            textBorderWidth: 3,
          },
          data: this.convertedLocations
        }
      ];

      // Add Drone series if pageType is 'drone' or 'all'
      if (this.pageType === 'drone' || this.pageType === 'all') {
        baseSeries.push(
          // Drone path display (新增)
          {
            name: 'Drone Path',
            type: 'lines',
            coordinateSystem: 'geo',
            geoIndex: 0,
            lineStyle: {
              color: '#91cc75',
              width: 3,
              opacity: 0.8,
              curveness: 0
            },
            data: this.dronePathPoints.slice(0, -1).map((item, index) => {
              return {
                coords: [this.dronePathPoints[index], this.dronePathPoints[index + 1]]
              };
            }).filter(item => item.coords[0] && item.coords[1])
          },
          // Drone path points (新增)
          {
            name: 'Drone Path Points',
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbol: 'circle',
            symbolSize: 6,
            itemStyle: {
              color: '#91cc75'
            },
            data: this.dronePathPoints,
            z: 5
          },
          // Drone historical route (dashed line)
          {
            name: 'Drone Route',
            type: 'lines',
            coordinateSystem: 'geo',
            geoIndex: 0,
            lineStyle: {
              color: '#91cc75',
              width: 2,
              opacity: 0.6,
              curveness: 0.2,
              type: 'dashed'
            },
            data: this.droneHistory.slice(0, -1).map((item, index) => {
              return {
                coords: [this.droneHistory[index], this.droneHistory[index + 1]]
              };
            }).filter(item => item.coords[0] && item.coords[1])
          },
          // Drone current position (scatter with custom symbol)
          {
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbolSize: [30, 30],
            symbol: "path://" + droneSymbolPath,
            itemStyle: {
              color: '#91cc75'
            },
            data: [this.dronePosition], // Use the dynamically calculated drone position
            name: 'Drone Position',
            z: 10, // Ensure it's rendered on top
            label: {
              show: true,
              position: 'top',
              distance: 10,
              formatter: () => {
                return `位置: (${Math.round(this.dronePosition[0])}, ${Math.round(this.dronePosition[1])})\n状态: ${this.droneStatus}`;
              },
              backgroundColor: 'rgba(50,50,50,0.7)',
              borderRadius: 4,
              padding: [4, 8],
              color: '#fff',
              lineHeight: 16,
              fontSize: 15
            }
          }
        );
      }

      // Add Indoor Car series if pageType is 'car', 'vehicle', or 'all'
      if (this.pageType === 'car' || this.pageType === 'vehicle' || this.pageType === 'all') {
        baseSeries.push(
          // Indoor Car historical route (dashed line)
          {
            name: 'Indoor Car Route',
            type: 'lines',
            coordinateSystem: 'geo',
            geoIndex: 0,
            lineStyle: {
              color: '#5470c6',
              width: 2,
              opacity: 0.6,
              curveness: 0.2,
              type: 'dashed'
            },
            data: this.indoorCarHistory.slice(0, -1).map((item, index) => {
              return {
                coords: [this.indoorCarHistory[index], this.indoorCarHistory[index + 1]]
              };
            }).filter(item => item.coords[0] && item.coords[1])
          },
          // Indoor Car current position (scatter with custom symbol)
          {
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbolSize: [30, 30],
            symbol: "path://" + CarSymbolPath,
            itemStyle: {
              color: '#5470c6'
            },
            data: [this.indoorCarPosition], // Use the dynamically calculated indoor car position
            name: 'Indoor Car Position',
            z: 10, // Ensure it's rendered on top
            label: {
              show: true,
              position: 'top',
              distance: 10,
              formatter: () => {
                return `位置: (${Math.round(this.indoorCarPosition[0])}, ${Math.round(this.indoorCarPosition[1])})\n状态: ${this.indoorCarStatus}`;
              },
              backgroundColor: 'rgba(50,50,50,0.7)',
              borderRadius: 4,
              padding: [4, 8],
              color: '#fff',
              lineHeight: 16,
              fontSize: 15
            }
          }
        );
        
        baseSeries.push(
          // Vector1 路径显示
          {
            name: 'Vector1 Path',
            type: 'lines',
            coordinateSystem: 'geo',
            geoIndex: 0,
            lineStyle: {
              color: '#5470c6',
              width: 3,
              opacity: 0.8,
              curveness: 0
            },
            data: this.vector1PathPoints.slice(0, -1).map((item, index) => {
              return {
                coords: [this.vector1PathPoints[index], this.vector1PathPoints[index + 1]]
              };
            }).filter(item => item.coords[0] && item.coords[1])
          },
          // Vector1 路径点标记
          {
            name: 'Vector1 Points',
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbol: 'circle',
            symbolSize: 6,
            itemStyle: {
              color: '#5470c6'
            },
            data: this.vector1PathPoints,
            z: 5
          }
        );
      }

      return baseSeries;
    },

    /**
     * Generates the legend data for ECharts based on the current pageType.
     */
    getLegendData() {
      const legendData = [];

      if (this.pageType === 'drone' || this.pageType === 'all') {
        legendData.push({ name: 'Drone Route' });
      }

      if (this.pageType === 'car' || this.pageType === 'vehicle' || this.pageType === 'all') {
        legendData.push({ name: 'Indoor Car Route' });
      }

      return legendData;
    },

    /**
     * Updates the drone's position and status based on incoming real-time data.
     * Assumes `data[0]` is the latest data point if server orders by ID DESC.
     */
     updateDronePosition(data) {
  if (!data || !this.indoorCarChart || data.length === 0) return;

  // Access the first element, which is the latest when sorted DESC by ID from server
  const latestDataPoint = data[0]; 
  const currentState = parseFloat(latestDataPoint.State);

  // 检测是否有新任务（状态从100变为小于100，或者从0开始增长）
  if (currentState < 100 && (this.droneLastState === 100 || this.droneLastState === 0)) {
    this.droneHasActiveTask = true;
    // 重置历史轨迹，开始新任务
    this.droneHistory = [];
  }

// 如果状态是100且之前有任务，说明任务完成
if (currentState === 100 && this.droneHasActiveTask) {
  this.droneHasActiveTask = false;
  this.droneStatus = "运送中 (100%)";
  // 保持在终点位置
  this.dronePosition = this.dronePathPoints[this.dronePathPoints.length - 1];
} else if (this.droneHasActiveTask) {
    // 任务进行中
    const newPosition = this.interpolateMultiSegmentPath(
      this.dronePathPoints,
      currentState / 100
    );

    // Add to history and maintain buffer size
    this.droneHistory.push(newPosition);
    if (this.droneHistory.length > this.historyBufferSize) {
      this.droneHistory.shift();
    }

    this.dronePosition = newPosition;
    this.droneStatus = `运送中 (${currentState.toFixed(0)}%)`;
  }

  // 更新最后的状态
  this.droneLastState = currentState;

  // 只更新无人机相关的数据
  const series = this.indoorCarChart.getOption().series;
  
  // 找到无人机位置系列的索引
  const dronePositionIndex = series.findIndex(s => s.name === 'Drone Position');
  if (dronePositionIndex !== -1) {
    series[dronePositionIndex].data = [this.dronePosition];
  }
  
  // 找到无人机历史轨迹系列的索引
  const droneRouteIndex = series.findIndex(s => s.name === 'Drone Route');
  if (droneRouteIndex !== -1) {
    series[droneRouteIndex].data = this.droneHistory.slice(0, -1).map((item, index) => {
      return {
        coords: [this.droneHistory[index], this.droneHistory[index + 1]]
      };
    }).filter(item => item.coords[0] && item.coords[1]);
  }

  // 只更新变化的部分
  this.indoorCarChart.setOption({
    series: series
  });
},

    /**
     * Updates the indoor car's position and status based on incoming real-time data.
     * **Updated to use `data[0]` to get the latest data point, matching drone logic.**
     */
     updateIndoorCarPosition(data) {
  if (!data || !this.indoorCarChart || data.length === 0) return;

  // Access the first element, which should be the latest if server is ORDER BY id DESC
  const latestDataPoint = data[0]; 
  const currentStatus = parseFloat(latestDataPoint.Status);

  // 检测是否有新任务（状态从100变为小于100，或者从0开始增长）
  if (currentStatus < 100 && (this.indoorCarLastStatus === 100 || this.indoorCarLastStatus === 0)) {
    this.indoorCarHasActiveTask = true;
    // 重置历史轨迹，开始新任务
    this.indoorCarHistory = [];
  }

// 如果状态是100且之前有任务，说明任务完成
if (currentStatus === 100 && this.indoorCarHasActiveTask) {
  this.indoorCarHasActiveTask = false;
  this.indoorCarStatus = "运送中 (100%)";
  // 保持在终点位置
  this.indoorCarPosition = this.vector1PathPoints[this.vector1PathPoints.length - 1];
} else if (this.indoorCarHasActiveTask) {
    // 任务进行中
    const newPosition = this.interpolateMultiSegmentPath(
      this.vector1PathPoints,
      currentStatus / 100
    );

    // Add to history and maintain buffer size
    this.indoorCarHistory.push(newPosition);
    if (this.indoorCarHistory.length > this.historyBufferSize) {
      this.indoorCarHistory.shift();
    }

    this.indoorCarPosition = newPosition;
    this.indoorCarStatus = `运送中 (${currentStatus.toFixed(0)}%)`;
  }

  // 更新最后的状态
  this.indoorCarLastStatus = currentStatus;

  // 只更新室内车相关的数据
  const series = this.indoorCarChart.getOption().series;
  
  // 找到室内车位置系列的索引
  const carPositionIndex = series.findIndex(s => s.name === 'Indoor Car Position');
  if (carPositionIndex !== -1) {
    series[carPositionIndex].data = [this.indoorCarPosition];
  }
  
  // 找到室内车历史轨迹系列的索引
  const carRouteIndex = series.findIndex(s => s.name === 'Indoor Car Route');
  if (carRouteIndex !== -1) {
    series[carRouteIndex].data = this.indoorCarHistory.slice(0, -1).map((item, index) => {
      return {
        coords: [this.indoorCarHistory[index], this.indoorCarHistory[index + 1]]
      };
    }).filter(item => item.coords[0] && item.coords[1]);
  }

  // 只更新变化的部分
  this.indoorCarChart.setOption({
    series: series
  });
},

    /**
     * Subscribes to real-time updates from the WebSocket server based on pageType.
     */
    subscribeToRealTimeUpdates() {
      if (!socket.connected) {
        socket.connect();
      }

      // 在订阅前先清除之前的监听器，避免重复订阅
      this.unsubscribeFromRealTimeUpdates();

      if (this.pageType === 'drone' || this.pageType === 'all') {
        socket.on('drone_state_update', (data) => {
          console.log('收到无人机数据更新:', data);
          if (data && data.length > 0) {
            this.updateDronePosition(data);
          }
        });
        socket.emit('subscribe_drone_state');
      }

      if (this.pageType === 'car' || this.pageType === 'vehicle' || this.pageType === 'all') {
        socket.on('indoor_car_state_update', (data) => {
          console.log('收到室内车数据更新:', data);
          if (data && data.length > 0) {
            this.updateIndoorCarPosition(data);
          }
        });
        socket.emit('subscribe_indoor_car_state');
      }

      // 添加连接错误处理
      socket.on('connect_error', (error) => {
        console.error('Socket连接错误:', error);
        this.reconnectSocket();
      });

      socket.on('disconnect', () => {
        console.log('Socket断开连接，尝试重连...');
        this.reconnectSocket();
      });
    },

    /**
     * Unsubscribes from all real-time updates when the component is unmounted.
     */
    unsubscribeFromRealTimeUpdates() {
      // 移除所有相关的事件监听器
      socket.off('drone_state_update');
      socket.off('indoor_car_state_update');
      socket.off('connect_error');
      socket.off('disconnect');
      
      // 如果socket还连接着，则断开连接
      if (socket.connected) {
        socket.disconnect();
      }
    },

    // 添加重连方法
    reconnectSocket() {
      if (!socket.connected) {
        setTimeout(() => {
          socket.connect();
          this.subscribeToRealTimeUpdates();
        }, 1000);
      }
    },

    /**
     * Initializes the ECharts instance and sets up the map.
     */
    initChart() {
      var dom = document.getElementById("container_indoorCar");
      var myChart = echarts.init(dom, null, {
        renderer: "canvas",
        useDirtyRect: false,
      });

      this.indoorCarChart = myChart;

      this.convertedLocations = [];

      const that = this; // Store 'this' context for use inside the $.get callback

      let mapFileName = '';
      let boundingCoords = [[0, 0], [642.19, 813.25]]; // Default for haibei_map.svg
      let center = [370, 360]; // Default for 'all' or fallback map

      if (this.pageType === 'drone') {
  mapFileName = 'haibei_map.svg'; // 改为和vehicle一样的地图
  boundingCoords = [[0, 0], [642.19, 813.25]];
  center = [320, 500]; // 调整为适合无人机路径的中心点
} else if (this.pageType === 'car' || this.pageType === 'vehicle') {
  mapFileName = 'haibei_map.svg';
  boundingCoords = [[0, 0], [642.19, 813.25]];
  center = [320, 500];
} else {
  // Default or 'all' case
  mapFileName = 'haibei_map.svg';
  boundingCoords = [[0, 0], [642.19, 813.25]];
  center = [370, 360];
}

      $.get(mapFileName, function (svg) {
        echarts.registerMap("hkust_map_live", { svg: svg });
        const option = {
          tooltip: {},
          geo: {
            map: "hkust_map_live",
            boundingCoords: boundingCoords,
            zoom: 1,
            label: {
              show: true,
              textBorderColor: "white",
              textBorderWidth: 2,
              fontSize: 15,
            },
            center: center,
          },
          legend: {
            orient: 'vertical',
            right: '1%',
            top: '1%',
            data: that.getLegendData(),
            textStyle: {
              color: '#333',
              fontSize: 15,
            }
          },
          series: that.getSeriesBasedOnPageType()
        };
        myChart.setOption(option);
      });

      window.addEventListener("resize", myChart.resize);
    },

    /**
     * Updates the map's center.
     */
    updateMapCenter(position) {
      if (this.indoorCarChart) {
        this.indoorCarChart.setOption({
          geo: {
            center: position
          }
        });
      }
    },

    // 添加页面可见性变化处理方法
    handleVisibilityChange() {
      if (document.hidden) {
        this.unsubscribeFromRealTimeUpdates();
      } else {
        this.subscribeToRealTimeUpdates();
      }
    },
  },
  mounted() {
    this.initChart();
    this.subscribeToRealTimeUpdates();

    // 添加页面可见性变化监听
    document.addEventListener('visibilitychange', this.handleVisibilityChange);
  },
  beforeUnmount() {
    this.unsubscribeFromRealTimeUpdates();

    if (this.indoorCarChart) {
      window.removeEventListener("resize", this.indoorCarChart.resize);
    }

    // 移除页面可见性变化监听
    document.removeEventListener('visibilitychange', this.handleVisibilityChange);
  },
};
</script>

<style scoped>
.map-wrapper {
  position: relative;
  width: 100%;
  height: 800px; /* Adjust height as needed */
  overflow: hidden;
}

#container_indoorCar {
  width: 100%;
  min-width: 800px; /* Ensure a minimum width for the map */
  margin: 0 auto;
  position: relative;
  max-width: 100%;
  height: 100%;
}

.title-container {
  text-align: center;
  margin-bottom: 10px;
  position: relative;
  z-index: 10; /* Ensure title is above map if needed */
}

.map-container {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>