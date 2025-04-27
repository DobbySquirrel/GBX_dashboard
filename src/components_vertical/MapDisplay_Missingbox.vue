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

export default {
  name: "MapDisplayMissingBox",
  props: {
    OutdoorDeliveryCar_Property_OutdoorCarState: {
      type: String,
      default: null,
    },
    IndoorDeliveryCar_Property_IndoorCarState: {
      type: String,
      default: null,
    },
    DeliveryDrone_Property_DroneState: {
      type: String,
      default: null,
    },
    pointsData: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      myChart: null
    };
  },
  methods: {
    convertCoordinates(coords) {
      // 地理参考点数据
      const geoItems = {
        'Latitude': [22.894559689319834, 22.886376973309183],
        'Longitude': [113.47484770222422, 113.4830306533438],
        'X': [-2.4901161193847656e-6, 1142.998168796301],
        'Y': [0, 1244.0001220703125]
      };

      // 计算转换比例
      const deltaLat = geoItems.Latitude[1] - geoItems.Latitude[0];
      const deltaLon = geoItems.Longitude[1] - geoItems.Longitude[0];
      const deltaX = geoItems.X[1] - geoItems.X[0];
      const deltaY = geoItems.Y[1] - geoItems.Y[0];

      const scaleX = deltaX / deltaLon;
      const scaleY = deltaY / deltaLat;

      // 计算偏移量
      const offsetX = geoItems.X[0] - geoItems.Longitude[0] * scaleX;
      const offsetY = geoItems.Y[0] - geoItems.Latitude[0] * scaleY;

      // 转换坐标，确保返回数组而不是元组
      return [
        coords[0] * scaleX + offsetX,
        coords[1] * scaleY + offsetY
      ];
    },
    
    initChart() {
      // 使用ref获取DOM元素
      const dom = this.$refs.missingBoxMap;
      if (!dom) return;
      
      // 如果已经有实例，先销毁
      if (this.myChart) {
        this.myChart.dispose();
      }
      
      this.myChart = echarts.init(dom, null, {
        renderer: "canvas",
        useDirtyRect: false,
      });

      // 使用传入的点数据
      const pointsData = this.pointsData || [];
      
      // 转换所有位置坐标
      const convertedLocations = pointsData.map((coords, index) => {
        const [x, y] = this.convertCoordinates(coords);
        return [x, y, `Position ${index + 1} (${coords[0].toFixed(4)}, ${coords[1].toFixed(4)})`];
      });
      
      // 默认使用第一个点作为中心，如果没有点则使用默认值
      const centerCoords = this.convertCoordinates([113.47872088332235, 22.892061020308077]);

      // 使用根路径访问 public 文件夹中的资源
      $.get('/hkust_map.svg', (svg) => {
        // 使用唯一的地图名称
        echarts.registerMap("hkust_map_missing_box", { svg: svg });
        
        const option = {
          tooltip: {
            formatter: function(params) {
              return params.data[2];
            }
          },
          geo: {
            map: "hkust_map_missing_box",
            roam: true,
            zoom: 1.5,
            label: {
              show: true,
              textBorderColor: "white",
              textBorderWidth: 2,
              fontSize: 10,
            },
            center: centerCoords,
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
            data: ['Missing Box Position (' + convertedLocations.length + ')']
          },
          series: [
            {
              type: 'scatter',
              coordinateSystem: 'geo',
              geoIndex: 0,
              symbol: 'diamond',
              symbolSize: 15,
              itemStyle: {
                color: 'red',
                opacity: 0.8
              },
              encode: {
                tooltip: 2
              },
              name: 'Missing Box Position (' + convertedLocations.length + ')',
              label: {
                show: true,
                formatter: function(params) {
                  return `${params.dataIndex + 1}`;
                },
                textBorderColor: "black",
                color: "white",
                textBorderWidth: 2,
              },
              data: convertedLocations
            }
          ],
        };
        
        this.myChart.setOption(option);
      });
    },
    
    handleResize() {
      if (this.myChart) {
        this.myChart.resize();
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      window.addEventListener("resize", this.handleResize);
    });
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.handleResize);
    if (this.myChart) {
      this.myChart.dispose();
      this.myChart = null;
    }
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  max-height: 25vh;
}

#container_missing_box {
  width: 100%;
  height: 100%;
  flex: 1;
  min-height: 100px;
}

.title-container {
  text-align: center;
  margin-bottom: 10px;
}
</style>
