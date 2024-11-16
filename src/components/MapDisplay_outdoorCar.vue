<template>
  <div class="chart-container">
    <div class="title-container">
      <el-text class="mx-1" style="font-size: 18px; color: #44652a">Car's Route Simulation</el-text>
    </div>
    <div ref="map_container" id="outdoor-car-map">
      <BMap
        :height="mapHeight"
        v-bind="$attrs"
        :center="{
          'lng': 113.48925478242874,
          'lat': 22.89512780142586
        }"
        :zoom="24"
        :plugins="['TrackAnimation']"
        ref="map_outdoor"
        @pluginReady="handleInitd"
        @initd="onMapInit"
        class="bmap"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useTrackAnimation } from 'vue3-baidu-map-gl'
import { outdoorCarMapStyle } from '../assets/mapStyles/outdoorCarMapStyle'
import * as echarts from "echarts";
import $ from "jquery";

const map_outdoor = ref(null)
const mapHeight = ref(0)

// 计算地图高度
const calculateMapHeight = () => {
  const windowHeight = window.innerHeight
  mapHeight.value = Math.floor(windowHeight * 0.30) // 30%的视窗高度
}

// 添加窗口大小变化监听
onMounted(async () => {
  try {
    // 使用加载器加载地图
    await window.BMapGLLoader.load();
    
    window.addEventListener('resize', handleResize);
    calculateMapHeight();
    
    // 加载地图
    const dom = document.getElementById("container_outdoorCar");
    const myChart = echarts.init(dom, null, {
      renderer: "canvas",
      useDirtyRect: false,
    });

    // 使用 import.meta.env.BASE_URL 获取基础路径
    const svgPath = `${import.meta.env.BASE_URL}hkust_gz_map.svg`;
    
    $.get(svgPath, function (svg) {
      echarts.registerMap("hkust_gz_map", { svg: svg });
      // 在这里设置你的 echarts option
      const option = {
        // 你的 echarts 配置
      };
      myChart.setOption(option);
    });
  } catch (error) {
    console.error('Failed to load map:', error);
  }
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

const handleResize = () => {
  if (map_outdoor.value) {
    calculateMapHeight() // 重新计算高度
    map_outdoor.value.resize()
  }
}

const { setPath, start, cancel, stop, proceed, status } = useTrackAnimation(map_outdoor, {
duration: 15000,
delay: 1,
zoom:18,
overallView:false
  })
  const path = [{
    'lng': 113.490145,
    'lat': 22.893705
}, {
    'lng': 113.49081,
    'lat': 22.893222
}, {
    'lng': 113.491861,
    'lat': 22.895273
}, {
    'lng': 113.491861,
    'lat': 22.895273
}, {
    'lng': 113.492256,
    'lat': 22.896184
}, {
    'lng': 113.491223,
    'lat': 22.896742
}, {
    'lng': 113.49156,
    'lat': 22.897146
}]
 const onMapInit = ({ map }) => {
      // Enable map settings
      map.enableScrollWheelZoom();
      map.setTilt(45);
      map.setMapStyleV2({
        styleJson: outdoorCarMapStyle,
      });
      map.setDisplayOptions({
        skyColors: ["rgba(0, 0, 0, 0)", "rgba(0, 0, 0, 0)"],
      });
      
      // 指定区域数据格式化处理;
      var ptArr = [];
      // 添加泡泡点
      const bubblelabel: [number, number, string][] = [
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
      for (let i = 0; i < bubblelabel.length; i++) {
        const pt = new BMapGL.Point(bubblelabel[i][0], bubblelabel[i][1]);
        const marker = new BMapGL.Marker(pt);
        // 创建文本标注对象，设置坐标和标签文字
        const labelopts = {
          position: pt, // 使用坐标点pt作为标签的位置
          offset: new BMapGL.Size(0, 0), // 设置文本偏移量
        };
        const label = new BMapGL.Label(bubblelabel[i][2], labelopts); // 设置标签内容为对应名称
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

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
}

#outdoor-car-map {
  width: 100%;
  flex: 1;
  position: relative;
}

.bmap {
  width: 100%;
  height: 100%;
}

.title-container {
  text-align: center;
  font-weight: bold;
}

/* 隐藏百度地图版权信息 */
:deep(.BMap_cpyCtrl) {
  display: none;
}

:deep(.anchorBL) {
  display: none;
}
</style>