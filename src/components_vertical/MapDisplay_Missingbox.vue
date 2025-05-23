<template>
  <div class="chart-container">
    <div class="title-container">
      <el-text class="mx-1" style="font-size: 16px; color: #44652a; font-weight: bold;"
        >Let's find the missing box!</el-text
      >
    </div>
    <div id="container_missing_box" ref="missingBoxMap"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import $ from "jquery";
import socket from "../api/socket"; // 确保此路径指向您的 socket.js 文件

export default {
  name: "MapDisplayMissingBox",
  props: {
    pointsData: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      myChart: null,
      dbRawPointsData: [], // 存储从 Socket.IO 获取的原始丢失箱子数据
      socketConnected: false,
    };
  },
  computed: {
    // 根据 RFID 去重，获取每个丢失箱子的最新位置
    latestMissingBoxes() {
      const latest = {};
      [...this.pointsData, ...this.dbRawPointsData].forEach(item => {
        if (item && item.RFID) {
          latest[item.RFID] = item;
        }
      });
      return Object.values(latest);
    },
    // 合并 props 传入的数据和从 Socket.IO 获取的数据，并进行 RFID 去重，用于图表展示
    allPointsData() {
      return this.latestMissingBoxes.map(item => {
        const longitude = parseFloat(item?.longitude || item?.Longitude);
        const latitude = parseFloat(item?.latitude || item?.Latitude);
        return isNaN(longitude) || isNaN(latitude) || !item?.RFID
          ? null
          : [longitude, latitude, item.RFID];
      }).filter(Boolean); // 移除无效数据点
    },
  },
  methods: {
    // 将经纬度坐标转换为地图上的像素坐标
    convertCoordinates(coords) {
      // 请根据您的实际地图和地理参考点进行调整
      const geoItems = {
        "Latitude": [22.88464154052963,22.89464776491583],
  "Longitude": [113.46989968040322,113.4828121621228],
        'X': [0, 1802.25], // 对应 SVG 的坐标范围
        'Y': [1495.18, 0], // 对应 SVG 的坐标范围，注意 Y 轴可能需要反向
      };
      const deltaLon = geoItems.Longitude[1] - geoItems.Longitude[0];
      const deltaLat = geoItems.Latitude[1] - geoItems.Latitude[0];
      const deltaX = geoItems.X[1] - geoItems.X[0];
      const deltaY = geoItems.Y[1] - geoItems.Y[0];

      if (deltaLon === 0 || deltaLat === 0) {
        return [NaN, NaN]; // 避免除以零
      }

      const ratioX = deltaX / deltaLon;
      const ratioY = deltaY / deltaLat;

      const offsetX = geoItems.X[0] - geoItems.Longitude[0] * ratioX;
      const offsetY = geoItems.Y[0] - geoItems.Latitude[0] * ratioY;

      const x = coords[0] * ratioX + offsetX;
      const y = coords[1] * ratioY + offsetY;

      return [x, y];
    },

    // 处理从 Socket.IO 接收到的丢失箱子数据更新
    handleMissingBoxUpdate(data) {
      console.log('接收到丢失箱子更新:', data);
      if (Array.isArray(data)) {
        this.dbRawPointsData = data.map(item => ({
          latitude: parseFloat(item?.latitude || item?.Latitude),
          longitude: parseFloat(item?.longitude || item?.Longitude),
          RFID: item?.RFID,
          // 可以根据服务器发送的数据结构添加其他需要的属性
          ...item,
        }));
        this.updateChart();
      }
    },

    // 更新 ECharts 图表
    updateChart() {
      if (!this.myChart) return;

      const chartData = this.allPointsData.map(item => {
        const convertedCoords = this.convertCoordinates([item[0], item[1]]);
        return [...convertedCoords, `RFID: ${item[2]} (${item[0]?.toFixed(4)}, ${item[1]?.toFixed(4)})`];
      }).filter(item => !isNaN(item[0]) && !isNaN(item[1]));

      this.myChart.setOption({
        legend: {
          data: [`丢失箱子 (${chartData.length})`],
        },
        series: [
          {
            name: `丢失箱子 (${chartData.length})`,
            type: 'scatter',
            coordinateSystem: 'geo',
            geoIndex: 0,
            symbol: 'diamond',
            symbolSize: 15,
            itemStyle: {
              color: 'red',
              opacity: 0.8,
            },
            encode: {
              tooltip: 2,
            },
            label: {
              show: true,
              formatter: (params) => `${params.dataIndex + 1}`,
              textBorderColor: 'black',
              color: 'white',
              textBorderWidth: 2,
            },
            data: chartData,
          },
        ],
      });
    },

    // 初始化 ECharts 图表
    initChart() {
      const dom = this.$refs.missingBoxMap;
      if (!dom) return;

      if (this.myChart) {
        this.myChart.dispose();
      }

      this.myChart = echarts.init(dom, null, {
        renderer: 'canvas',
        useDirtyRect: false,
      });

      // 初始地图中心点，请根据您的实际需求调整
      const initialCenter = [901.125,747.59];

      $.get('/hkust_map_with_station.svg', (svg) => {
        echarts.registerMap('hkust_map_missing_box', { svg: svg });

        const option = {
          tooltip: {
            formatter: (params) => params.data[2],
          },
          geo: {
            map: 'hkust_map_missing_box',
            roam: true,
            zoom: 1.5,
            label: {
              show: true,
              textBorderColor: 'white',
              textBorderWidth: 2,
              fontSize: 10,
            },
            center: initialCenter,
          },
          legend: {
            orient: 'vertical',
            left: '1%',
            top: '1%',
            textStyle: {
              color: '#333',
              fontSize: 10,
            },
            itemWidth: 10,
            itemHeight: 10,
            data: [`丢失箱子 (0)`],
          },
          series: [], // 数据在 updateChart 中动态添加
        };

        this.myChart.setOption(option);
      });
    },

    // 处理窗口 resize 事件
    handleResize() {
      if (this.myChart) {
        this.myChart.resize();
      }
    },

    // 初始化 Socket.IO 连接和监听器
    initSocketConnection() {
      if (!socket.connected) {
        socket.connect();
      }

      socket.on('connect', () => {
        console.log('MapDisplayMissingBox: 已连接到 Socket.IO 服务器');
        this.socketConnected = true;
        socket.emit('subscribe_missing_box'); // 连接成功后订阅丢失箱子数据
      });

      socket.on('disconnect', () => {
        console.log('MapDisplayMissingBox: 与 Socket.IO 服务器断开连接');
        this.socketConnected = false;
      });

      socket.on('connect_error', (error) => {
        console.error('MapDisplayMissingBox: Socket.IO 连接错误:', error);
        this.socketConnected = false;
      });

      socket.on('missing_box_update', this.handleMissingBoxUpdate);
    },

    // 移除 Socket.IO 监听器
    removeSocketListeners() {
      socket.off('missing_box_update', this.handleMissingBoxUpdate);
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      window.addEventListener('resize', this.handleResize);
      this.initSocketConnection();
    });
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
    this.removeSocketListeners();
    if (this.myChart) {
      this.myChart.dispose();
      this.myChart = null;
    }
  },
  watch: {
    // 监听 props 传入的点数据变化
    pointsData: {
      handler() {
        this.updateChart();
      },
      deep: true,
    },
  },
};
</script>


<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  max-height: 100%;
}

#container_missing_box {
  width: 100%;
  height: 100%;
  flex: 1;
  min-height: 290px;
}

.title-container {
  text-align: center;
  margin-bottom: 10px;
}
</style>
