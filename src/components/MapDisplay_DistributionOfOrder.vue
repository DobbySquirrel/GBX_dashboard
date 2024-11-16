<template>
  <div>
    <div id="Container_Order_Distribution"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from "echarts"
import $ from "jquery"

// 定义 props
const props = defineProps({
  DeliveryDrone_Property_DroneDeliveryOrder: {
    type: [String, null],
    required: true
  },
  IndoorDeliveryCar_Property_IndoorDeliveryOrder: {
    type: [String, null],
    required: true
  },
  OutdoorDeliveryCar_Property_OutdoorDeliveryOrder: {
    type: [String, null],
    required: true
  }
})

// 响应式数据
const myChart = ref(null)
const unifiedData = ref([])
const localDeliveryDrone_Property_DroneDeliveryOrder = ref(props.DeliveryDrone_Property_DroneDeliveryOrder)
const localIndoorDeliveryCar_Property_IndoorDeliveryOrder = ref(props.IndoorDeliveryCar_Property_IndoorDeliveryOrder)
const localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder = ref(props.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder)

// 方法定义
const parseCsvData = (csvString) => {
  const lines = csvString.trim().split('\n')
  const headers = lines[0].split(',')
  return lines.slice(1).map(line => {
    const values = line.split(',')
    return headers.reduce((obj, header, index) => {
      obj[header.trim()] = values[index].trim()
      return obj
    }, {})
  })
}

const calculateAreaCounts = () => {
  const areaCount = {}
  
  // 处理无人机订单数据
  const droneData = parseCsvData(localDeliveryDrone_Property_DroneDeliveryOrder.value)
  droneData.forEach(order => {
    const area = order.ReceiverAddress
    areaCount[area] = (areaCount[area] || 0) + 1
  })

  // 处理室内配送车订单数据
  const indoorData = parseCsvData(localIndoorDeliveryCar_Property_IndoorDeliveryOrder.value)
  indoorData.forEach(order => {
    const area = order.Area
    areaCount[area] = (areaCount[area] || 0) + 1
  })

  // 处理室外配送车订单数据
  const outdoorData = parseCsvData(localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder.value)
  outdoorData.forEach(order => {
    const area = order.Area
    areaCount[area] = (areaCount[area] || 0) + 1
  })

  // 生成最终数据
  unifiedData.value = [
    { name: "W1", value: areaCount["W1"] || 0 },
    { name: "W2", value: areaCount["W2"] || 0 },
    // ... 其他区域数据 ...
    { name: "Fire Control Center", value: areaCount["Fire Control Center"] || 0 }
  ]
}

const updateChart = () => {
  if (!myChart.value) return
  
  const maxValue = Math.max(...unifiedData.value.map(item => item.value || 0))
  const option = {
    title: {
      text: "Order Distribution Map",
      left: "center",
      textStyle: {
        color: "#44652a",
      },
      top: "0%",
    },
    tooltip: {},
    visualMap: {
      min: 0,
      max: maxValue > 0 ? maxValue : 10,
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
        textBorderColor: "white",
        textBorderWidth: 2,
      },
    },
    grid: {
      top: "60%",
    },
    series: [
      {
        name: "Orders",
        type: "map",
        map: "hkust_gz_map",
        emphasis: {
          label: {
            show: false,
          },
        },
        selectedMode: false,
        data: unifiedData.value
      },
    ],
  }

  myChart.value.setOption(option)
}

const handleResize = () => {
  if (myChart.value) {
    myChart.value.resize()
  }
}

const initChart = async () => {
  const dom = document.getElementById("Container_Order_Distribution")
  myChart.value = echarts.init(dom, null, {
    renderer: "canvas",
    useDirtyRect: false,
  })
  
  try {
    // 尝试从不同位置加载SVG文件
    const response = await fetch('/hkust_gz_map.svg')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const svg = await response.text()
    
    // 注册地图时添加必要的地图数据结构
    echarts.registerMap("hkust_gz_map", {
      svg: svg,
      // 添加地图区域数据
      regions: [
        { name: "W1", svg: { path: [] } },
        { name: "W2", svg: { path: [] } },
        { name: "W3", svg: { path: [] } },
        { name: "W4", svg: { path: [] } },
        { name: "E1", svg: { path: [] } },
        { name: "E2", svg: { path: [] } },
        { name: "E3", svg: { path: [] } },
        { name: "E4", svg: { path: [] } },
        { name: "Library", svg: { path: [] } },
        { name: "Lecture Halls", svg: { path: [] } },
        { name: "Administration Building", svg: { path: [] } },
        { name: "Activity Center", svg: { path: [] } },
        { name: "Block 1A", svg: { path: [] } },
        { name: "Block 1B", svg: { path: [] } },
        { name: "Block 3", svg: { path: [] } },
        { name: "Block 5A", svg: { path: [] } },
        { name: "Block 5B", svg: { path: [] } },
        { name: "Block 5C", svg: { path: [] } },
        { name: "Block 2A", svg: { path: [] } },
        { name: "Block 2B", svg: { path: [] } },
        { name: "Block 4A", svg: { path: [] } },
        { name: "Block 4B", svg: { path: [] } },
        { name: "Block 6A", svg: { path: [] } },
        { name: "Block 6B", svg: { path: [] } },
        { name: "Block 6C", svg: { path: [] } },
        { name: "Bleachers", svg: { path: [] } },
        { name: "Stadium", svg: { path: [] } },
        { name: "Canteen", svg: { path: [] } },
        { name: "10D", svg: { path: [] } },
        { name: "10C", svg: { path: [] } },
        { name: "10B", svg: { path: [] } },
        { name: "10A", svg: { path: [] } },
        { name: "9D", svg: { path: [] } },
        { name: "9C", svg: { path: [] } },
        { name: "9B", svg: { path: [] } },
        { name: "9A", svg: { path: [] } },
        { name: "NN-8", svg: { path: [] } },
        { name: "NN-6", svg: { path: [] } },
        { name: "NN-9", svg: { path: [] } },
        { name: "NN-2", svg: { path: [] } },
        { name: "NN-3", svg: { path: [] } },
        { name: "NN-1", svg: { path: [] } },
        { name: "NN-4-5", svg: { path: [] } },
        { name: "Data Center", svg: { path: [] } },
        { name: "Energy Center", svg: { path: [] } },
        { name: "Fire Control Center", svg: { path: [] } }
      ]
    })
    
    // 确保在地图注册完成后再更新图表
    await nextTick()
    updateChart()
  } catch (error) {
    console.error("加载地图失败:", error)
  }
}

const onDataUpdate = () => {
  if (localDeliveryDrone_Property_DroneDeliveryOrder.value &&
      localIndoorDeliveryCar_Property_IndoorDeliveryOrder.value &&
      localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder.value) {
    calculateAreaCounts()
    updateChart()
  }
}

// 监听属性变化
watch(() => props.DeliveryDrone_Property_DroneDeliveryOrder, (newVal) => {
  localDeliveryDrone_Property_DroneDeliveryOrder.value = newVal
  onDataUpdate()
})

watch(() => props.IndoorDeliveryCar_Property_IndoorDeliveryOrder, (newVal) => {
  localIndoorDeliveryCar_Property_IndoorDeliveryOrder.value = newVal
  onDataUpdate()
})

watch(() => props.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder, (newVal) => {
  localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder.value = newVal
  onDataUpdate()
})

// 生命周期钩子
onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
  if (props.DeliveryDrone_Property_DroneDeliveryOrder && 
      props.IndoorDeliveryCar_Property_IndoorDeliveryOrder && 
      props.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder) {
    calculateAreaCounts()
    updateChart()
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (myChart.value) {
    myChart.value.dispose()
  }
})
</script>

<style scoped>
#Container_Order_Distribution {
  width: 90%;
  height: 25vh;
  min-height: 200px;
  padding: 5px;
}
</style>
