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
      :zoom="20"
      :height="205"
      :heading="200"
      :tilt="60"
      @initd="onMapInit"
    />
  </div>
</template>

<script>
import { ref } from "vue";
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
      
      const carlineLayer = new mapvgl.CarLineLayer({
        url: "/mapv/gl/examples/model/car.gltf",
        autoPlay: true,
        scale: 15,
      });

      view.addLayer(carlineLayer);
      carlineLayer.setData(data);    

  map.setDefaultCursor('default');


    var coordinates = data[0].geometry.coordinates;
    var point = [];
    for (var i = 0; i < coordinates.length; i += 1) {
        point.push(new BMapGL.Point(coordinates[i][0], coordinates[i][1]));
    }

    var pl = new BMapGL.Polyline(point, {strokeWeight: 4, strokeColor:'#76c850', strokeStyle:'dashed'});
    

    var trackAni = new BMapGLLib.TrackAnimation(map, pl, {
        overallView: false,
        tilt: 55,
        heading: 130,
        zoom: 18,
        duration: 15000,
        delay: 100,
        autoPlay: true
    });
    trackAni.start();
  
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
.BMap_cpyCtrl {
   display: none;
 }
.anchorBL {
   display: none;
}
.title-container {
  text-align: center;
  font-weight: bold;
}
</style>