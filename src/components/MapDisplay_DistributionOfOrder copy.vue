<template>
    
  <div ref="mapContainer_car" class="map-container_car">
    <div class="title-container">
    <el-text class="mx-1" style="font-size: 18px; color: #44652a">Order Distribution Map</el-text>
  </div>
    <BMap
      :center="{
        
        lng: 113.489248,
        lat: 22.895120,
      }"
      :zoom="16"
      :heading="0"
      :tilt="0"
      :height="205"
      v-bind="$attrs"
      @initd="onMapInit"
    />
  </div>
</template>

<script>
import { ref } from "vue";
import * as mapvgl from "mapvgl";

export default {
  name: "MapComponent",
  setup() {
    const mapContainer_car = ref(null);
    const onMapInit = ({ map }) => {
      // 指定区域数据格式化处理;
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
      var view = new mapvgl.View({
        map: map,
      });
      var data = [];
      var points = [
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
        [113.4922156948421, 22.891948143626255],
      ];

      points.forEach(function (item) {
        data.push({
          geometry: {
            type: "Point",
            coordinates: [item[0], item[1]],
          }
        });
      });
          var honeycombLayer = new mapvgl.HoneycombLayer({
        // 设置颜色梯度
gradient: {
    0.0: 'rgb(250, 50, 56)',
    0.5: 'rgb(250, 250, 56)',
    0.9: 'rgb(50, 250, 56)',
    1.0: 'rgb(50, 250, 56)'
},
        // 是否显示文字
        showText: true,
        // 设置文字样式
        textOptions: {
            fontSize: 13,
            color: '#69b0acff',
            format: function (count) {
                return count >= 10000 ? Math.round(count / 1000) + 'k'
                : count >= 1000 ? Math.round(count / 100) / 10 + 'k' : count;
            }
        },
        height: 30, // 最大值的像素高度，为0时显示平面
        // enableCluster: true, // 开启点聚合，建议数据量较大时打开，会提前根据地图级别将距离较近的点进行聚合
        opacity: 0.2, // 透明度
        maxZoom: 16, // 图层刷新最大地图级别，高于此值不再更新图层
        minZoom: 8, // 图层刷新最小地图级别，低于此值不再更新图层
        size: 40 // 蜂窝图像素宽度
    });
    view.addLayer(honeycombLayer);
    honeycombLayer.setData(data);

//     const bubblelabel = [
//   [113.48868, 22.893414, "香港科技大学(广州)-行政楼"],
//   [113.489248, 22.895125, "香港科技大学1F食堂"],
//   [113.491074, 22.890642, "香港科技大学(广州)-南宿舍区"],
//   [113.490211, 22.890885, "香港科技大学(广州)"],
//   [113.490309, 22.89078, "香港科技大学(广州)"],
//   [113.49258, 22.89667, "香港科技大学(广州)-北宿舍区"],
//   [113.492846, 22.895329, "香港科技大学(广州)-停车场"],
//   [113.48895, 22.895425, "真功夫"],
//   [113.488761, 22.893173, "星巴克"],
//   [113.49019, 22.891725, "一碗贵粉"],
//   [113.490486, 22.891633, "肯德基"],
//   [113.49301, 22.890252, "万家LiFE"],
//   [113.489381, 22.895, "逸林港式茶餐厅"]
// ];

// for (var i = 0; i < bubblelabel.length; i++) {
//   var pt = new BMapGL.Point(bubblelabel[i][0], bubblelabel[i][1]);
//   var labelopts = {
//     position: pt,
//     offset: new BMapGL.Size(0, 0)
//   };
//   var label = new BMapGL.Label(bubblelabel[i][2], labelopts);
//   label.setStyle({
//     color: "#fff",
//     backgroundColor: "rgba(0, 0, 0, 0.3)",
//     borderRadius: "10px",
//     padding: "0 10px",
//     fontSize: "12px",
//     lineHeight: "20px",
//     border: "0",
//     transform: "translateX(-50%)"
//   });
//   map.addOverlay(label);  
// }


      //end
    };

    return {
      mapContainer_car,
      onMapInit,
    };
  },
};
</script>

<style scoped>

.title-container {
  text-align: center;
  font-weight: bold;
}
</style>
