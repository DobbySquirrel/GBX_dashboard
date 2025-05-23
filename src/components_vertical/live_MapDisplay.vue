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
    const dronePathPoints = [
      [300, 200], // Drone start point (example coordinates)
      [700, 600]  // Drone end point (example coordinates)
    ];
    const indoorCarPathPoints = [
      [100, 100], // Indoor car start point (example coordinates)
      [500, 600]  // Indoor car end point (example coordinates)
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

      convertedLocations: [] // For fixed locations, if any
    };
  },
  methods: {
    /**
     * Helper function to interpolate a point on a line given a percentage.
     * The percentage value (0 to 1) determines the position between start and end.
     */
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
              fontSize: 12
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
              color: '#fac858',
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
              color: '#fac858'
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
              fontSize: 12
            }
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

      // Calculate new position based on the drone's path points and its 'State' percentage
      const newPosition = this.interpolatePoint(
        this.dronePathPoints[0], // Start of the path
        this.dronePathPoints[1], // End of the path
        latestDataPoint.State   // Use the 'State' as the percentage
      );

      // Add to history and maintain buffer size
      this.droneHistory.push(newPosition);
      if (this.droneHistory.length > this.historyBufferSize) {
        this.droneHistory.shift(); // Remove the oldest point
      }

      this.dronePosition = newPosition;
      // Update status display with percentage
      this.droneStatus = `运送中 (${(parseFloat(latestDataPoint.State) * 100).toFixed(0)}%)`;

      this.indoorCarChart.setOption({
        series: this.getSeriesBasedOnPageType()
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

      // Calculate new position based on the indoor car's path points and its 'Status' percentage
      const newPosition = this.interpolatePoint(
        this.indoorCarPathPoints[0], // Start of the path
        this.indoorCarPathPoints[1], // End of the path
        latestDataPoint.Status // Assuming 'Status' field for percentage
      );

      // Add to history and maintain buffer size
      this.indoorCarHistory.push(newPosition);
      if (this.indoorCarHistory.length > this.historyBufferSize) {
        this.indoorCarHistory.shift(); // Remove the oldest point
      }

      this.indoorCarPosition = newPosition;
      // Update status display with percentage
      this.indoorCarStatus = `运送中 (${(parseFloat(latestDataPoint.Status) * 100).toFixed(0)}%)`;

      this.indoorCarChart.setOption({
        series: this.getSeriesBasedOnPageType()
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
        mapFileName = 'hkust_map_with_station.svg';
        boundingCoords = [[0, 0], [1802.25, 1495.18]]; // Adjust to actual bounds of your SVG
        center = [700, 800]; // Adjust to appropriate center for drone map
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
              fontSize: 10,
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
              fontSize: 10,
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