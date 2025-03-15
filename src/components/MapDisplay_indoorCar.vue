<template>
  <div class="chart-container">
    <div class="title-container">
      <el-text class="mx-1" style="font-size: 12px; color: #44652a"
        >Let's find the missing box!</el-text
      >
    </div>
    <div id="container_indoorCar"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import $ from "jquery";

export default {
  name: "MapDisplay",
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
    }
  },
  mounted() {
    var dom = document.getElementById("container_indoorCar");
    var myChart = echarts.init(dom, null, {
      renderer: "canvas",
      useDirtyRect: false,
    });
    var option;

    // 使用传入的点数据
    const pointsData = this.pointsData || [];
    
    // 转换所有位置坐标
    const convertedLocations = pointsData.map((coords, index) => {
      const [x, y] = this.convertCoordinates(coords);
      return [x, y, `Position ${index + 1} (${coords[0].toFixed(4)}, ${coords[1].toFixed(4)})`]; // 添加经纬度信息
    });
    
    // 默认使用第一个点作为中心，如果没有点则使用默认值
    const centerCoords = this.convertCoordinates([113.47872088332235, 22.892061020308077]);

    // 使用根路径访问 public 文件夹中的资源
    $.get('/hkust_map.svg', function (svg) {
      echarts.registerMap("hkust_map", { svg: svg });
      option = {
        tooltip: {
          formatter: function(params) {
            // 只返回数据中的第三个元素（位置信息），不显示标记符号
            return params.data[2];
          }
        },
        geo: {
          map: "hkust_map",
          roam: true,
          zoom: 2,
          label: {
              show: true,
            textBorderColor: "white", // Sets the border color to white
            textBorderWidth: 2, // Sets the border width
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
          itemWidth: 10,  // 设置图例标记的宽度
          itemHeight: 10, // 设置图例标记的高度
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
      myChart.setOption(option);
    });

    // Resize chart when window size changes
    window.addEventListener("resize", myChart.resize);
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 30vh;
  display: flex;
  flex-direction: column;
}

#container_indoorCar {
  width: 100%;
  height: 100%;
  flex: 1;
  min-height: 160px;
}

.title-container {
  text-align: center;
  font-weight: bold;
}
</style>
