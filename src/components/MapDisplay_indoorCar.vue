<template>
  <div>
    <div class="title-container">
      <el-text class="mx-1" style="font-size: 20px; color: #44652a"
        >Vehicle's Route</el-text
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

      // 转换坐标
      const x = coords[0] * scaleX + offsetX;
      const y = coords[1] * scaleY + offsetY;

      return [x, y];
    }
  },
  mounted() {
    var dom = document.getElementById("container_indoorCar");
    var myChart = echarts.init(dom, null, {
      renderer: "canvas",
      useDirtyRect: false,
    });
    var app = {};
    var option;

    // 定义位置坐标
    const locations = {
      'Locker': [113.47953830802487, 22.894216859923475],
      'Helipad': [113.47872088332235, 22.892061020308077],
      'E3 Lab': [113.47852336734121, 22.891218918887034]
    };

    // 转换所有坐标
    const convertedLocations = Object.entries(locations).map(([name, coords]) => {
      const [x, y] = this.convertCoordinates(coords);
      return [x, y, name];
    });

    // 获取转换后的各个位置坐标
    const e3LabCoords = this.convertCoordinates(locations['E3 Lab']);
    const helipadCoords = this.convertCoordinates(locations['Helipad']);
    const lockerCoords = this.convertCoordinates(locations['Locker']);

    $.get('src/assets/hkust_map.svg', function (svg) {
      echarts.registerMap("hkust_map", { svg: svg });
      option = {
        tooltip: {},
        geo: {
          map: "hkust_map",
          roam: true,
          zoom: 2,
          label: {
              show: true,
            textBorderColor: "white", // Sets the border color to white
            textBorderWidth: 2, // Sets the border width
            },

            center: helipadCoords,
        },
        series: [
          {
      type: 'scatter',
      coordinateSystem: 'geo',
      geoIndex: 0,
      symbol :'pin',
      symbolSize: 40,
      itemStyle: {
        color: '#b02a02'
      },
      encode: {
        tooltip: 2
      },
      label: {
        show: true,
        formatter: function(params) {
          return params.data[2];
        },
        textBorderColor: "#b02a02", // Sets the border color to white
        color: "white", // Sets the border color to white
        textBorderWidth: 2, // Sets the border width
      },
      data: convertedLocations
    },
          {
            type: "lines",
            coordinateSystem: "geo",
            geoIndex: 0,
            polyline: true,
            effect: {
              show: true,
              period: 1,
              trailLength: 0,
              constantSpeed: 50,
            },
            data: [
              {
                // E3 Lab 到 Helipad
                lineStyle: {
                  color: "#73c0de",
                  width: 2,
                  opacity: 1,
                  type: "dotted",
                },
                effect: {
                  delay: 0,
                  symbolSize: [14, 12],
                  symbol: "arrow",
                },
                coords: [e3LabCoords, helipadCoords]
              },
              {
                // Helipad 到 Locker
                lineStyle: {
                  color: "#91CC75",
                  width: 5,
                  opacity: 1,
                  type: "dotted",
                },
                effect: {
                  delay: 10000,
                  symbolSize: [14, 12],
                  color: "#91CC75",
                  symbol: "path://M343.2 177.46C324.6 129.78 278.2 96 224 96c-70.7 0-128 57.3-128 128 0 54.2 33.78 100.6 81.46 119.2l76.94 101c-10 3.2-20 3.8-30.4 3.8C100.28 448 0 347.8 0 224 0 100.28 100.28 0 224 0c123.8 0 224 100.28 224 224 0 10.4-0.6 20.6-3.8 30.4l-101-76.94zM426.6 320h170.8l139.2-104.4c4-31.38 31-55.6 63.4-55.6 35.4 0 64 28.66 64 64 0 32.4-24.2 59.4-55.6 63.4L704 426.6v170.8l104.4 139.2c31.4 4 55.6 31 55.6 63.4 0 35.4-28.6 64-64 64-32.4 0-59.4-24.2-63.4-55.6L597.4 704h-170.8l-139.2 104.4c-4 31.4-31 55.6-63.4 55.6-35.34 0-64-28.6-64-64 0-32.4 24.22-59.4 55.6-63.4l104.4-139.2v-170.8l-104.4-139.2C184.22 283.4 160 256.4 160 224c0-35.34 28.66-64 64-64 32.4 0 59.4 24.22 63.4 55.6l139.2 104.4zM224 1024C100.28 1024 0 923.8 0 800s100.28-224 224-224c10.4 0 20.4 0.6 30.4 2l-76.94 102.8C129.78 699.4 96 745.8 96 800c0 70.6 57.3 128 128 128 54.2 0 100.6-33.8 119.2-81.4l101-77c3.2 10 3.8 20 3.8 30.4 0 123.8-100.2 224-224 224z m354-769.6c-1.4-10-2-20-2-30.4C576 100.28 676.2 0 800 0s224 100.28 224 224c0 123.8-100.2 224-224 224-10.4 0-20.4-0.6-30.4-3.8l77-101c47.6-18.6 81.4-65 81.4-121 0-68.9-57.4-128-128-128-54.2 0-100.6 35.58-119.2 83.26L578 254.4zM576 800c0-10.4 0.6-20.4 2-30.4l102.8 77c18.6 47.6 65 81.4 119.2 81.4 70.6 0 128-57.4 128-128 0-54.2-33.8-100.6-81.4-119.2L769.6 578c10-1.4 20-3.8 30.4-3.8 123.8 0 224 102 224 225.8 0 123.8-100.2 224-224 224s-224-100.2-224-224z",
                },
                coords: [helipadCoords, lockerCoords]
              },
              {
                // Locker 到 E3 Lab
                lineStyle: {
                  color: "grey",
                  width: 1,
                  opacity: 1,
                  type: "dotted",
                },
                effect: {
                  delay: 0,
                  symbolSize: [12, 12],
                  symbol: "arrow",
                },
                coords: [lockerCoords, e3LabCoords]
              }
            ]
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
#container_indoorCar {
  width: 100%;
  height: 550px;
}
.title-container {
  text-align: center;
  font-weight: bold;
}
</style>
