<template>
  <div>
    <div class="title-container">
      <el-text class="mx-1" style="font-size: 18px; color: #44652a"
        >Order Distribution Map</el-text
      >
    </div>
    <div id="Container_Order_Distribution"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import $ from "jquery";
// Import the SVG file from the assets directory
// import floorplangeojson from "@/assets/map.geojson";

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
  mounted() {
    var dom = document.getElementById("Container_Order_Distribution");
    var myChart = echarts.init(dom, null, {
      renderer: "canvas",
      useDirtyRect: false,
    });
    var app = {};
    var option;

    // Use the imported SVG file
    $.get("src/assets/hkust_gz_map.svg", function (svg) {
      echarts.registerMap("MacOdrum-LV5-floorplan-web", { svg: svg });
      option = {
        tooltip: {},
        visualMap: {
          map: "MacOdrum-LV5-floorplan-web",
          roam: true,
          zoom: 5,
          min: 5,
          max: 100,
          itemHeight:250,
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
            textBorderColor: "white", // Sets the border color to white
            textBorderWidth: 2, // Sets the border width
          },
          },
          grid: {
            top: "100%", // Adjust this value to move the image up or down
          },
          series: [
            {
              name: "MacOdrum",
              type: "map",
              map: "MacOdrum-LV5-floorplan-web",
              emphasis: {
                label: {
                show: false,
              },
            },
            selectedMode: false,

            data: [
              { name: "W1", value: 12 },
              { name: "W2", value: 38 },
              { name: "W3", value: 24 },
              { name: "W4", value: 47 },
              { name: "E1", value: 29 },
              { name: "E2", value: 15 },
              { name: "E3", value: 34 },
              { name: "E4", value: 53 },
              { name: "Library", value: 22 },
              { name: "Lecture Halls", value: 41 },
              { name: "Administration Building", value: 19 },
              { name: "Activity Center", value: 30 },
              { name: "Block 1A", value: 45 },
              { name: "Block 1B", value: 27 },
              { name: "Block 3", value: 17 },
              { name: "Block 5A", value: 32 },
              { name: "Block 5B", value: 23 },
              { name: "Block 5C", value: 46 },
              { name: "Block 2A", value: 37 },
              { name: "Block 2B", value: 51 },
              { name: "Block 4A", value: 33 },
              { name: "Block 4B", value: 59 },
              { name: "Block 6A", value: 28 },
              { name: "Block 6B", value: 42 },
              { name: "Block 6C", value: 26 },
              { name: "Bleachers", value: 1 },
              { name: "Stadium", value: 35 },
              { name: "Canteen", value: 31 },
              { name: "10D", value: 34 },
              { name: "10C", value: 27 },
              { name: "10B", value: 15 },
              { name: "10A", value: 42 },
              { name: "9D", value: 20 },
              { name: "9C", value: 37 },
              { name: "9B", value: 29 },
              { name: "9A", value: 33 },
              { name: "NN-8", value: 24 },
              { name: "NN-6", value: 31 },
              { name: "NN-9", value: 26 },
              { name: "NN-2", value: 19 },
              { name: "NN-3", value: 28 },
              { name: "NN-1", value: 22 },
              { name: "NN-4-5", value: 35 },
              { name: "Data Center", value: 40 },
              { name: "Energy Center", value: 30 },
              { name: "Fire Control Center", value: 38 },
            ],
          },
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
#Container_Order_Distribution {
  width: 100%;
  height: 205px;
}
.title-container {
  text-align: center;
  font-weight: bold;
}
</style>
