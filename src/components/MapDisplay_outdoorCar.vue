<template>
  <div class="map-container-outdoor"> <!-- 使用class来定义样式 -->

     <div class="title-container">
    <el-text class="mx-1" style="font-size: 18px; color: #44652a">Dynamic Route Simulation</el-text>
  </div>
    <BMap
      v-bind="$attrs"
      :center="{
        'lng': 113.48925478242874,
        'lat': 22.89512780142586
      }"
      :zoom="24"
      :plugins="['TrackAnimation']"
      :height="205"
      ref="map_outdoor"
      @pluginReady="handleInitd"
      @initd="onMapInit"
    />
    
  </div>
</template>

<script setup lang="ts">
  import { ref, watch } from 'vue'
  import { useTrackAnimation } from 'vue3-baidu-map-gl'
  const map_outdoor = ref(null)
  const { setPath, start, cancel, stop, proceed, status } = useTrackAnimation(map_outdoor, {
duration: 15000,
delay: 1,
zoom:18,
overallView:false
  })
  const path = [{
    'lng': 113.48925478242874,
    'lat': 22.89512780142586
  }, {
    'lng': 113.48921937326168,
    'lat': 22.895053481581378
  }, {
    'lng': 113.48940577165494,
    'lat': 22.89495360290252
  }, {
    'lng': 113.48927524138237,
    'lat': 22.894364685880905
  }, {
    'lng': 113.4897423602474,
    'lat': 22.893990138528295
  }, {
    'lng': 113.49078439463864,
    'lat': 22.893174454008136
  }, {
    'lng': 113.49049693687553,
    'lat': 22.892808226691788
  }, {
    'lng': 113.49097603323875,
    'lat': 22.892597368255732
  }, {
    'lng': 113.49120060961617,
    'lat': 22.892464194228914
  }, {
    'lng': 113.49182044041784,
    'lat': 22.892156228785538
  }, {
    'lng': 113.4922156948421,
    'lat':22.891948143626255
  }]
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
        [113.489381, 22.895, "逸林港式茶餐厅"],
      ];

      //添加label
      for (var i = 0; i < bubblelabel.length; i++) {
        var pt = new BMapGL.Point(bubblelabel[i][0], bubblelabel[i][1]);
        var marker = new BMapGL.Marker(pt);
        // 创建文本标注对象，设置坐标和标签文字
        var labelopts = {
          position: pt, // 使用坐标点pt作为标签的位置
          offset: new BMapGL.Size(0, 0), // 设置文本偏移量
        };
        var label = new BMapGL.Label(bubblelabel[i][2], labelopts); // 设置标签内容为对应名称
        label.setStyle({
          color: "#fff",
          backgroundColor: "rgba(0, 0, 0, 0.3)",
          borderRadius: "10px",
          padding: "0 10px",
          fontSize: "12px",
          lineHeight: "20px",
          border: "0",
          transform: "translateX(-50%)",
        });

        // 添加marker及文本标注
        map.addOverlay(label); // 再添加文本标签


      }
      
      }
  function handleInitd() {
    
    setPath(path)
    setPath(path)
    if (status.value === 'INITIAL') {
      setTimeout(() => {
        start() // Start the animation after 2 seconds if status is INITIAL
      }, 4000)
    }
  }

  watch(status, (newStatus) => {
    if (newStatus === 'INITIAL') {
      setTimeout(() => {
        start() // 循环播放动画，延迟2秒启动
      }, 0)
    }
  })

</script>

<style>

.BMap_cpyCtrl {
   display: none;
 }
.anchorBL {
   display: none;
}
/* .map-container-outdoor {
  width: 95%;
  height: 250px;
 
} */
.title-container {
  text-align: center;
  font-weight: bold;
}
</style>