<template>
  <div>
    <div id="Container_Order_Distribution"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
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

// 方法定义
const parseCsvData = (csvString) => {
  if (!csvString) return []  // 如果数据为空，返回空数组
  
  try {
    const lines = csvString.trim().split('\n')
    const headers = lines[0].split(',')
    return lines.slice(1).map(line => {
      const values = line.split(',')
      return headers.reduce((obj, header, index) => {
        obj[header.trim()] = values[index]?.trim() || ''
        return obj
      }, {})
    })
  } catch (error) {
    console.error('解析CSV数据失败:', error)
    return []
  }
}

const calculateAreaCounts = () => {
  const areaCount = {}
  
  try {
    // 添加调试日志
    // console.log('Drone Data:', props.DeliveryDrone_Property_DroneDeliveryOrder)
    // console.log('Indoor Data:', props.IndoorDeliveryCar_Property_IndoorDeliveryOrder)
    // console.log('Outdoor Data:', props.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder)

    // 检查数据是否都存在
    if (props.DeliveryDrone_Property_DroneDeliveryOrder) {
      const droneData = parseCsvData(props.DeliveryDrone_Property_DroneDeliveryOrder)
      // console.log('Parsed Drone Data:', droneData)
      droneData.forEach(order => {
        const area = order.ReceiverAddress
        if (area) {
          areaCount[area] = (areaCount[area] || 0) + 1
        }
      })
    }

    if (props.IndoorDeliveryCar_Property_IndoorDeliveryOrder) {
      const indoorData = parseCsvData(props.IndoorDeliveryCar_Property_IndoorDeliveryOrder)
      // console.log('Parsed Indoor Data:', indoorData)
      indoorData.forEach(order => {
        const area = order.Area
        if (area) {
          areaCount[area] = (areaCount[area] || 0) + 1
        }
      })
    }

    if (props.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder) {
      const outdoorData = parseCsvData(props.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder)
      // console.log('Parsed Outdoor Data:', outdoorData)
      outdoorData.forEach(order => {
        const area = order.Area
        if (area) {
          areaCount[area] = (areaCount[area] || 0) + 1
        }
      })
    }

    // console.log('Area Counts:', areaCount)

    // 生成最终数据，包含所有区域
    unifiedData.value = [
      { name: "W1", value: areaCount["W1"] || 0 },
      { name: "W2", value: areaCount["W2"] || 0 },
      { name: "W3", value: areaCount["W3"] || 0 },
      { name: "W4", value: areaCount["W4"] || 0 },
      { name: "E1", value: areaCount["E1"] || 0 },
      { name: "E2", value: areaCount["E2"] || 0 },
      { name: "E3", value: areaCount["E3"] || 0 },
      { name: "E4", value: areaCount["E4"] || 0 },
      { name: "Library", value: areaCount["Library"] || 0 },
      { name: "Lecture Halls", value: areaCount["Lecture Halls"] || 0 },
      { name: "Administration Building", value: areaCount["Administration Building"] || 0 },
      { name: "Activity Center", value: areaCount["Activity Center"] || 0 },
      { name: "Block 1A", value: areaCount["Block 1A"] || 0 },
      { name: "Block 1B", value: areaCount["Block 1B"] || 0 },
      { name: "Block 3", value: areaCount["Block 3"] || 0 },
      { name: "Block 5A", value: areaCount["Block 5A"] || 0 },
      { name: "Block 5B", value: areaCount["Block 5B"] || 0 },
      { name: "Block 5C", value: areaCount["Block 5C"] || 0 },
      { name: "Block 2A", value: areaCount["Block 2A"] || 0 },
      { name: "Block 2B", value: areaCount["Block 2B"] || 0 },
      { name: "Block 4A", value: areaCount["Block 4A"] || 0 },
      { name: "Block 4B", value: areaCount["Block 4B"] || 0 },
      { name: "Block 6A", value: areaCount["Block 6A"] || 0 },
      { name: "Block 6B", value: areaCount["Block 6B"] || 0 },
      { name: "Block 6C", value: areaCount["Block 6C"] || 0 },
      { name: "Bleachers", value: areaCount["Bleachers"] || 0 },
      { name: "Stadium", value: areaCount["Stadium"] || 0 },
      { name: "Canteen", value: areaCount["Canteen"] || 0 },
      { name: "10D", value: areaCount["10D"] || 0 },
      { name: "10C", value: areaCount["10C"] || 0 },
      { name: "10B", value: areaCount["10B"] || 0 },
      { name: "10A", value: areaCount["10A"] || 0 },
      { name: "9D", value: areaCount["9D"] || 0 },
      { name: "9C", value: areaCount["9C"] || 0 },
      { name: "9B", value: areaCount["9B"] || 0 },
      { name: "9A", value: areaCount["9A"] || 0 },
      { name: "NN-8", value: areaCount["NN-8"] || 0 },
      { name: "NN-6", value: areaCount["NN-6"] || 0 },
      { name: "NN-9", value: areaCount["NN-9"] || 0 },
      { name: "NN-2", value: areaCount["NN-2"] || 0 },
      { name: "NN-3", value: areaCount["NN-3"] || 0 },
      { name: "NN-1", value: areaCount["NN-1"] || 0 },
      { name: "NN-4-5", value: areaCount["NN-4-5"] || 0 },
      { name: "Data Center", value: areaCount["Data Center"] || 0 },
      { name: "Energy Center", value: areaCount["Energy Center"] || 0 },
      { name: "Fire Control Center", value: areaCount["Fire Control Center"] || 0 }
    ]

    // console.log('Final Unified Data:', unifiedData.value)
  } catch (error) {
    console.error('计算区域数据失败:', error)
    // 设置默认数据
    unifiedData.value = [
      { name: "W1", value: 0 },
      { name: "W2", value: 0 },
      { name: "W3", value: 0 },
      { name: "W4", value: 0 },
      { name: "E1", value: 0 },
      { name: "E2", value: 0 },
      { name: "E3", value: 0 },
      { name: "E4", value: 0 },
      { name: "Library", value: 0 },
      { name: "Lecture Halls", value: 0 },
      { name: "Administration Building", value: 0 },
      { name: "Activity Center", value: 0 },
      { name: "Block 1A", value: 0 },
      { name: "Block 1B", value: 0 },
      { name: "Block 3", value: 0 },
      { name: "Block 5A", value: 0 },
      { name: "Block 5B", value: 0 },
      { name: "Block 5C", value: 0 },
      { name: "Block 2A", value: 0 },
      { name: "Block 2B", value: 0 },
      { name: "Block 4A", value: 0 },
      { name: "Block 4B", value: 0 },
      { name: "Block 6A", value: 0 },
      { name: "Block 6B", value: 0 },
      { name: "Block 6C", value: 0 },
      { name: "Bleachers", value: 0 },
      { name: "Stadium", value: 0 },
      { name: "Canteen", value: 0 },
      { name: "10D", value: 0 },
      { name: "10C", value: 0 },
      { name: "10B", value: 0 },
      { name: "10A", value: 0 },
      { name: "9D", value: 0 },
      { name: "9C", value: 0 },
      { name: "9B", value: 0 },
      { name: "9A", value: 0 },
      { name: "NN-8", value: 0 },
      { name: "NN-6", value: 0 },
      { name: "NN-9", value: 0 },
      { name: "NN-2", value: 0 },
      { name: "NN-3", value: 0 },
      { name: "NN-1", value: 0 },
      { name: "NN-4-5", value: 0 },
      { name: "Data Center", value: 0 },
      { name: "Energy Center", value: 0 },
      { name: "Fire Control Center", value: 0 }
    ]
  }
}

const handleResize = () => {
  if (myChart.value) {
    myChart.value.resize()
  }
}

const initChart = async () => {
  const dom = document.getElementById("Container_Order_Distribution")
  if (!dom) {
    console.error('找不到容器元素')
    return
  }

  try {
    // 确保在创建实例前销旧的实例
    if (myChart.value) {
      myChart.value.dispose()
    }
    
    // 加载 SVG
    const response = await fetch('/hkust_gz_map.svg')
    if (!response.ok) {
      throw new Error(`加载SVG失败: ${response.status}`)
    }
    const svg = await response.text()
    
    // 添加调试输出
    // console.log('SVG content:', svg)
    
    // 正确解析和注册地图数据
    const mapData = {
      svg: svg,
      // 添加地图的基本信息
      regions: [{
        name: 'hkust_gz_map',
        svg: svg,
        left: 0,
        top: 0,
        width: 1000,
        height: 1000
      }]
    }
    
    // 确保地图只注册一次
    if (!echarts.getMap('hkust_gz_map')) {
      echarts.registerMap("hkust_gz_map", mapData)
    }

    myChart.value = echarts.init(dom, null, {
      renderer: "canvas",
      useDirtyRect: false,
    })
    
    // 计算数据
    calculateAreaCounts()
    
    const maxValue = Math.max(...unifiedData.value.map(item => item.value || 0))
    
    const option = {
      title: {
        text: "Order Distribution Map",
        left: "center",
        textStyle: {
          color: "#44652a",
          fontSize: 12
        },
        top: "0%",
      },
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c}'
      },
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
      series: [{
        name: "Orders",
        type: "map",
        map: "hkust_gz_map",
        roam: true,
        emphasis: {
          label: {
            show: false,
          },
        },
        selectedMode: false,
        data: unifiedData.value,
        itemStyle: {
          areaColor: '#fff',
          borderColor: '#ccc'
        },
        // 添加布局相关配置
        layoutCenter: ['50%', '50%'],
        layoutSize: '100%',
        aspectScale: 1
      }]
    }
    
    if (myChart.value) {
      myChart.value.setOption(option, true)
    }
  } catch (error) {
    console.error("初始化图表失败:", error)
  }
}

// watch 部分的修改
watch([
  () => props.DeliveryDrone_Property_DroneDeliveryOrder,
  () => props.IndoorDeliveryCar_Property_IndoorDeliveryOrder,
  () => props.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder
], async () => {
  try {
    if (myChart.value) {
      // 重新计算数据
      calculateAreaCounts()
      const maxValue = Math.max(...unifiedData.value.map(item => item.value || 0))
      
      // 更新数据和最大值
      myChart.value.setOption({
        visualMap: {
          max: maxValue > 0 ? maxValue : 10
        },
        series: [{
          data: unifiedData.value
        }]
      })
    }
  } catch (error) {
    console.error('更新图表失败:', error)
  }
}, { 
  deep: true,
  immediate: true
})

// 添加自动刷新功能
const autoRefresh = ref(null)

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
  
  // 设置自动刷新间隔（例如每5秒刷新一次）
  autoRefresh.value = setInterval(() => {
    if (myChart.value) {
      calculateAreaCounts()
      const maxValue = Math.max(...unifiedData.value.map(item => item.value || 0))
      myChart.value.setOption({
        visualMap: {
          max: maxValue > 0 ? maxValue : 10
        },
        series: [{
          type: 'map',
          data: unifiedData.value
        }]
      })
    }
  }, 5000) // 5秒刷新一次
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (myChart.value) {
    myChart.value.dispose()
  }
  // 清除自动刷新定时器
  if (autoRefresh.value) {
    clearInterval(autoRefresh.value)
  }
})
</script>

<style scoped>
#Container_Order_Distribution {
  height: 30vh;
  min-height: 150px;
}
</style>
