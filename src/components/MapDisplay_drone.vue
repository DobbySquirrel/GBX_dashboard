<template>
  <div ref="mapContainer_drone" class="map-container">
        <div class="title-container">
    <el-text class="mx-1" style="font-size: 18px; color: #44652a">Order Distribution map</el-text>
  </div>
    <BMap
      v-bind="$attrs"
      :center="{
        
        lng: 113.489248,
        lat: 22.895125,
      }"
      :zoom="18"
      :height="205"
      :heading="200"
      :tilt="60"
      @initd="onMapInit"
    />
  </div>
</template>

<script>
import { ref } from "vue";
// import {
//   Engine,
//   FlyManager,
//   EmptySky,
//   GeoJSONDataSource,
//   FatLine,
//   SimplePoint,
//   BubblePoint,
// } from "mapv-three";
// import * as THREE from "bmap-three";
import * as mapv from 'mapv';
import * as mapvgl from 'mapvgl';
export default {
  name: "MapComponent",
  setup() {
    const mapContainer = ref(null);

    const onMapInit = ({ map }) => {
      // Enable map settings
      var styleJson = [
        {
          featureType: "land",
          elementType: "geometry",
          stylers: {
            color: "#fffff9ff",
          },
        },
        {
          featureType: "water",
          elementType: "geometry",
          stylers: {
            color: "#c4d7f5ff",
          },
        },
        {
          featureType: "highway",
          elementType: "geometry.fill",
          stylers: {
            color: "#fffff9ff",
          },
        },
        {
          featureType: "highway",
          elementType: "geometry.stroke",
          stylers: {
            color: "#94ad79ff",
          },
        },
        {
          featureType: "nationalway",
          elementType: "geometry.fill",
          stylers: {
            color: "#b5caa0ff",
          },
        },
        {
          featureType: "arterial",
          elementType: "geometry.fill",
          stylers: {
            color: "#d4e2c6ff",
          },
        },
        {
          featureType: "cityhighway",
          elementType: "geometry.fill",
          stylers: {
            color: "#d4e2c6ff",
          },
        },
        {
          featureType: "provincialway",
          elementType: "geometry.fill",
          stylers: {
            color: "#d4e2c6ff",
          },
        },
        {
          featureType: "provincialway",
          elementType: "geometry.stroke",
          stylers: {
            color: "#b5caa0ff",
          },
        },
        {
          featureType: "tertiaryway",
          elementType: "geometry.fill",
          stylers: {
            color: "#ffffffff",
          },
        },
        {
          featureType: "tertiaryway",
          elementType: "geometry.stroke",
          stylers: {
            color: "#b5caa0ff",
          },
        },
        {
          featureType: "fourlevelway",
          elementType: "geometry.fill",
          stylers: {
            color: "#ffffffff",
          },
        },
        {
          featureType: "fourlevelway",
          elementType: "geometry.stroke",
          stylers: {
            color: "#b5caa0ff",
          },
        },
        {
          featureType: "subway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "railway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "highwaysign",
          elementType: "labels",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "highwaysign",
          elementType: "labels.icon",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "nationalwaysign",
          elementType: "labels",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "nationalwaysign",
          elementType: "labels.icon",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "provincialwaysign",
          elementType: "labels",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "provincialwaysign",
          elementType: "labels.icon",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "tertiarywaysign",
          elementType: "labels",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "tertiarywaysign",
          elementType: "labels.icon",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "subwaylabel",
          elementType: "labels",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "subwaylabel",
          elementType: "labels.icon",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "nationalway",
          elementType: "geometry.stroke",
          stylers: {
            color: "#94ad79ff",
          },
        },
        {
          featureType: "cityhighway",
          elementType: "geometry.stroke",
          stylers: {
            color: "#b5caa0ff",
          },
        },
        {
          featureType: "arterial",
          elementType: "geometry.stroke",
          stylers: {
            color: "#b5caa0ff",
          },
        },
        {
          featureType: "highway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "6",
          },
        },
        {
          featureType: "highway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "7",
          },
        },
        {
          featureType: "highway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "8",
          },
        },
        {
          featureType: "highway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "9",
          },
        },
        {
          featureType: "highway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "6",
          },
        },
        {
          featureType: "highway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "7",
          },
        },
        {
          featureType: "highway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "8",
          },
        },
        {
          featureType: "highway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "9",
          },
        },
        {
          featureType: "highway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "6",
          },
        },
        {
          featureType: "highway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "7",
          },
        },
        {
          featureType: "highway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "8",
          },
        },
        {
          featureType: "highway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "9",
          },
        },
        {
          featureType: "nationalway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "6",
          },
        },
        {
          featureType: "nationalway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "7",
          },
        },
        {
          featureType: "nationalway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "8",
          },
        },
        {
          featureType: "nationalway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "9",
          },
        },
        {
          featureType: "nationalway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "6",
          },
        },
        {
          featureType: "nationalway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "7",
          },
        },
        {
          featureType: "nationalway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "8",
          },
        },
        {
          featureType: "nationalway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "9",
          },
        },
        {
          featureType: "nationalway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "6",
          },
        },
        {
          featureType: "nationalway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "7",
          },
        },
        {
          featureType: "nationalway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "8",
          },
        },
        {
          featureType: "nationalway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "9",
          },
        },
        {
          featureType: "provincialway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "8,9",
            level: "8",
          },
        },
        {
          featureType: "provincialway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "8,9",
            level: "9",
          },
        },
        {
          featureType: "provincialway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "8,9",
            level: "8",
          },
        },
        {
          featureType: "provincialway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "8,9",
            level: "9",
          },
        },
        {
          featureType: "provincialway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "8,9",
            level: "8",
          },
        },
        {
          featureType: "provincialway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "8,9",
            level: "9",
          },
        },
        {
          featureType: "cityhighway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "6",
          },
        },
        {
          featureType: "cityhighway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "7",
          },
        },
        {
          featureType: "cityhighway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "8",
          },
        },
        {
          featureType: "cityhighway",
          stylers: {
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "9",
          },
        },
        {
          featureType: "cityhighway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "6",
          },
        },
        {
          featureType: "cityhighway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "7",
          },
        },
        {
          featureType: "cityhighway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "8",
          },
        },
        {
          featureType: "cityhighway",
          elementType: "geometry",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "9",
          },
        },
        {
          featureType: "cityhighway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "6",
          },
        },
        {
          featureType: "cityhighway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "7",
          },
        },
        {
          featureType: "cityhighway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "8",
          },
        },
        {
          featureType: "cityhighway",
          elementType: "labels",
          stylers: {
            visibility: "off",
            curZoomRegionId: "0",
            curZoomRegion: "6,9",
            level: "9",
          },
        },
        {
          featureType: "entertainment",
          elementType: "geometry",
          stylers: {
            color: "#e4f0d7ff",
          },
        },
        {
          featureType: "manmade",
          elementType: "geometry",
          stylers: {
            color: "#effcf0ff",
          },
        },
        {
          featureType: "education",
          elementType: "geometry",
          stylers: {
            color: "#e3f7e4ff",
          },
        },
        {
          featureType: "building",
          elementType: "geometry.stroke",
          stylers: {
            color: "#a1cfa4ff",
          },
        },
        {
          featureType: "poilabel",
          elementType: "labels",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "poilabel",
          elementType: "labels.icon",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "education",
          elementType: "labels.text.fill",
          stylers: {
            color: "#7a7a7aff",
          },
        },
        {
          featureType: "education",
          elementType: "labels.text.stroke",
          stylers: {
            color: "#ffffffff",
          },
        },
        {
          featureType: "education",
          elementType: "labels.text",
          stylers: {
            fontsize: 26,
          },
        },
        {
          featureType: "manmade",
          elementType: "labels.text.fill",
          stylers: {
            color: "#afafafff",
          },
        },
        {
          featureType: "manmade",
          elementType: "labels.text",
          stylers: {
            fontsize: 26,
          },
        },
        {
          featureType: "scenicspotslabel",
          elementType: "labels.text.fill",
          stylers: {
            color: "#376b6dff",
          },
        },
        {
          featureType: "scenicspots",
          elementType: "labels",
          stylers: {
            visibility: "off",
          },
        },
        {
          featureType: "scenicspotslabel",
          elementType: "labels",
          stylers: {
            visibility: "on",
          },
        },
        {
          featureType: "scenicspotslabel",
          elementType: "labels.text.stroke",
          stylers: {
            color: "#ffffffff",
            weight: 4,
          },
        },
        {
          featureType: "country",
          elementType: "labels.text.fill",
          stylers: {
            color: "#376b6dff",
          },
        },
        {
          featureType: "country",
          elementType: "labels.text.stroke",
          stylers: {
            color: "#ffffffff",
            weight: 3,
          },
        },
        {
          featureType: "water",
          elementType: "labels.text.fill",
          stylers: {
            color: "#ffffffff",
          },
        },
        {
          featureType: "water",
          elementType: "labels.text.stroke",
          stylers: {
            color: "#ffffff00",
          },
        },
        {
          featureType: "water",
          elementType: "labels.text",
          stylers: {
            fontsize: 24,
          },
        },
      ];

      map.enableScrollWheelZoom();
      map.setTilt(45);
      map.setMapStyleV2({
        styleJson: styleJson,
      });
      map.setDisplayOptions({
        skyColors: ["rgba(0, 0, 0, 0)", "rgba(0, 0, 0, 0)"],
      });
      // 指定区域数据格式化处理;
      var ptArr = [];
      // 添加泡泡点
// Initialize the map view
var view = new mapvgl.View({
  map: map
});

// Define bubblelabel with coordinates and descriptions
const bubblelabel = [
  [113.48868, 22.893414, "香港科技大学(广州)-行政楼"],
  [113.489248, 22.895125, "香港科技大学1F食堂"],
  [113.491074, 22.890642, "香港科技大学(广州)-南宿舍区"],
  [113.490211, 22.890885, "香港科技大学(广州)"],
  [113.490309, 22.89078, "香港科技大学(广州)"],
  [113.49258, 22.89667, "香港科技大学(广州)-北宿舍区"],
  [113.492846, 22.895329, "香港科技大学(广州)-停车场"],
  [113.48895, 22.895425, "真功夫"],
  [113.488761, 22.893173, "星巴克"],
  [113.49019, 22.891725, "一碗贵粉"],
  [113.490486, 22.891633, "肯德基"],
  [113.49301, 22.890252, "万家LiFE"],
  [113.489381, 22.895, "逸林港式茶餐厅"]
];

// Convert bubblelabel to the format suitable for waveLayer data

var centerPoint = [113.489248, 22.895125];  // Coordinates of the center (香港科技大学1F食堂)

var data = bubblelabel.map((item) => {
  // Check if the current point is the center point
  if (item[0] === centerPoint[0] && item[1] === centerPoint[1]) {
    // Return specific object for the center point
    return {
      geometry: {
        type: 'Point',
        coordinates: [item[0], item[1]]  // Use the latitude and longitude from bubblelabel
      },
      color: '#f00',  // Red color for the center
      size: 8  // Larger size for the center
    };
  } else {
    // Return the original object for non-center points
    return {
      geometry: {
        type: 'Point',
        coordinates: [item[0], item[1]]  // Use the latitude and longitude from bubblelabel
      },
      color: 'rgba(0, 160, 113, 0.3)',  // Green color for other points
      size: 5  // Original size for other points
    };
  }
});


// Create a wave layer with specific effects
var waveLayer = new mapvgl.CircleLayer({
  type: 'wave',  // Add wave effect
  radius: r => 1.6 * r,  // Radius calculation for wave expansion
  duration: 0,  // Speed of the wave expansion
  trail: 4,  // Number of waves shown
});

// Add wave layer to the view
view.addLayer(waveLayer);

// Set the data for the wave layer from the bubblelabel
waveLayer.setData(data);

// Optionally, you can still add the labels from bubblelabel as well
for (var i = 0; i < bubblelabel.length; i++) {
  var pt = new BMapGL.Point(bubblelabel[i][0], bubblelabel[i][1]);
  var labelopts = {
    position: pt,
    offset: new BMapGL.Size(0, 0)
  };
  var label = new BMapGL.Label(bubblelabel[i][2], labelopts);
  label.setStyle({
    color: "#fff",
    backgroundColor: "rgba(0, 0, 0, 0.3)",
    borderRadius: "10px",
    padding: "0 10px",
    fontSize: "12px",
    lineHeight: "20px",
    border: "0",
    transform: "translateX(-50%)"
  });
  map.addOverlay(label);  // Add the label to the map  
}
var centerPoint = bubblelabel[1];  // [113.489248, 22.895125]

// Construct fly line data based on Bezier curves
var flyData = [];
var curve = new mapvgl.BezierCurve();

// Loop through all other points in the bubblelabel and create fly lines
for (var i = 0; i < bubblelabel.length; i++) {
  if (i !== 1) { // Skip the center point itself
    var startPoint = { lng: centerPoint[0], lat: centerPoint[1] };
    var endPoint = { lng: bubblelabel[i][0], lat: bubblelabel[i][1] };

    // Set options for Bezier curve from the center to each other point
    curve.setOptions({
      start: [startPoint.lng, startPoint.lat],
      end: [endPoint.lng, endPoint.lat]
    });
    var curveModelData = curve.getPoints();

    flyData.push({
      geometry: {
        type: 'LineString',
        coordinates: curveModelData
      },
      properties: {
        count: Math.random()  // Randomized count for properties (optional)
      }
    });
  }
}

// Add a layer for static lines
var lineLayer = new mapvgl.LineLayer({
  blend: 'lighter',
  width: 1,
  color: 'rgba(85, 255, 6, 1)'
});
view.addLayer(lineLayer);
lineLayer.setData(flyData);

// Add a layer for animated fly lines
var flyLayer = new mapvgl.LineLayer({
  blend: 'lighter',
  color: 'rgba(85, 255, 6, 1)',
  
  width: 2,
  animation: true,
  duration: 2,  // Cycle duration in seconds
  trailLength: 0.8,  // Tail length ratio
  interval: 0.2  // Particle length ratio
});
view.addLayer(flyLayer);
flyLayer.setData(flyData);
var data = [
  {
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [113.48925478242874, 22.89512780142586],
        [113.48921937326168, 22.895053481581378],
        [113.48940577165494, 22.89495360290252],
        [113.48927524138237, 22.894364685880905],
        [113.4897423602474, 22.893990138528295],
        [113.49078439463864, 22.893174454008136],
        [113.49049693687553, 22.892808226691788],
        [113.49097603323875, 22.892597368255732],
        [113.49120060961617, 22.892464194228914],
        [113.49182044041784, 22.892156228785538],
        [113.4922156948421, 22.891948143626255]
      ]
    }
  }
];
//       const lineLayer_car = new mapvgl.LineLayer({
//         width: 1,
//         color: "rgba(0, 0, 0, 0.5)",
//         style: "road",
//         enablePicked: true,
//         onClick: (e) => {
//           console.log(e);
//         },
//       });
//       view.addLayer(lineLayer_car);
//       lineLayer_car.setData(data);
//       const carlineLayer = new mapvgl.CarLineLayer({
//         url: "/mapv/gl/examples/model/car.gltf",
//         autoPlay: true,
//         scale: 15,
//       });

//       view.addLayer(carlineLayer);
//       carlineLayer.setData(data);

// var points = [
//         [113.48925478242874, 22.89512780142586],
//         [113.48921937326168, 22.895053481581378],
//         [113.48940577165494, 22.89495360290252],
//         [113.48927524138237, 22.894364685880905],
//         [113.4897423602474, 22.893990138528295],
//         [113.49078439463864, 22.893174454008136],
//         [113.49049693687553, 22.892808226691788],
//         [113.49097603323875, 22.892597368255732],
//         [113.49120060961617, 22.892464194228914],
//         [113.49182044041784, 22.892156228785538],
//         [113.4922156948421, 22.891948143626255],
//       ];

//       points.forEach(function (item) {
//         data.push({
//           geometry: {
//             type: "Point",
//             coordinates: [item[0], item[1]],
//           }
//         });
//       });
//           var honeycombLayer = new mapvgl.HoneycombLayer({
//         // 设置颜色梯度
// gradient: {
//     0.0: 'rgb(250, 50, 56)',
//     0.5: 'rgb(250, 250, 56)',
//     0.9: 'rgb(50, 250, 56)',
//     1.0: 'rgb(50, 250, 56)'
// },
//         // 是否显示文字
//         showText: true,
//         // 设置文字样式
//         textOptions: {
//             fontSize: 13,
//             color: '#69b0acff',
//             format: function (count) {
//                 return count >= 10000 ? Math.round(count / 1000) + 'k'
//                 : count >= 1000 ? Math.round(count / 100) / 10 + 'k' : count;
//             }
//         },
//         height: 10, // 最大值的像素高度，为0时显示平面
//         // enableCluster: true, // 开启点聚合，建议数据量较大时打开，会提前根据地图级别将距离较近的点进行聚合
//         opacity: 0.3, // 透明度
//         maxZoom: 16, // 图层刷新最大地图级别，高于此值不再更新图层
//         minZoom: 8, // 图层刷新最小地图级别，低于此值不再更新图层
//         size: 40 // 蜂窝图像素宽度
//     });
    // view.addLayer(honeycombLayer);
    // honeycombLayer.setData(data);
      // const bubblePoints = [
      //   [113.48868, 22.893414],
      //   [113.489248, 22.895125],
      //   [113.491074, 22.890642],
      //   [113.490211, 22.890885],
      //   [113.490309, 22.89078],
      //   [113.49258, 22.89667],
      //   [113.492846, 22.895329],
      //   [113.48895, 22.895425],
      //   [113.488761, 22.893173],
      //   [113.49019, 22.891725],
      //   [113.490486, 22.891633],
      //   [113.49301, 22.890252],
      //   [113.489381, 22.895],
      // ];
      // // Create a 3D engine instance
      // const engine = new Engine(map);
      // const center = [113.48925478242874, 22.89512780142586];
      // // Add sky element for lighting
      // const sky = engine.add(new EmptySky());
      // sky.time = 3600 * 14.5;

      // // Add source point
      // const sourcePoint = engine.add(
      //   new SimplePoint({
      //     color: "red",
      //     size: 10,
      //   })
      // );
      // GeoJSONDataSource.fromGeoJSON({
      //   type: "FeatureCollection",
      //   features: [
      //     {
      //       type: "Feature",
      //       geometry: {
      //         type: "Point",
      //         coordinates: [...center, 0.0],
      //       },
      //     },
      //   ],
      // }).then((pointDataSource) => {
      //   sourcePoint.dataSource = pointDataSource;
      // });

      // const bubbleGeoJSON = {
      //   type: "FeatureCollection",
      //   features: bubblePoints.map((point) => ({
      //     type: "Feature",
      //     geometry: {
      //       type: "Point",
      //       coordinates: [...point, 0.0],
      //     },
      //   })),
      // };
      // GeoJSONDataSource.fromGeoJSON(bubbleGeoJSON).then((bubbleDataSource) => {
      //   const bubble = engine.add(
      //     new BubblePoint({
      //       color: "rgba(0, 160, 117, 1.0)",
      //       size: 50,
      //       type: "Wave",
      //       duration: 10,
      //     })
      //   );
      //   bubble.dataSource = bubbleDataSource;
      // });

      // // Create GeoJSON data for fly lines from center to each destination
      // const flylineGeoJSON = {
      //   type: "FeatureCollection",
      //   features: bubblePoints.map((dest) => ({
      //     type: "Feature",
      //     geometry: {
      //       type: "LineString",
      //       coordinates: [center, [...dest, 0.0]],
      //     },
      //   })),
      // };

      // // Create GeoJSON data source and add dynamic fly lines
      // GeoJSONDataSource.fromGeoJSON(flylineGeoJSON).then((dataSource) => {
      //   const flyLine = engine.add(
      //     new FatLine({
      //       color: "#67c23a",
      //       lineWidth: 3,
      //       keepSize: true,
      //       emissive: new THREE.Color(0.2, 0.4, 0.2, 0.8),
      //       enableAnimation: false,
      //     })
      //   );
      //   flyLine.material.side = THREE.DoubleSide;
      //   dataSource.isCurve = true;
      //   flyLine.dataSource = dataSource;
      // });
    
    
    
    // end
    };

    return {
      mapContainer,
      onMapInit,
    };
  },
};
</script>

<style>

.title-container {
  text-align: center;
  font-weight: bold;
}
</style>