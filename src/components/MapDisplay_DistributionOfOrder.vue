<template>
  <div>
    <div id="Container_Order_Distribution"></div>
    <div id="Container_Area_Traffic"></div>
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
const selectedAreaName = ref('')
const selectedAreaData = ref([])
const showLineChart = ref(true) // 默认显示线图
const totalTrafficData = ref([]) // 存储总流量数据

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
      // 添加过滤逻辑，只保留 Owner 为 Station_1 的数据
      const filteredDroneData = droneData.filter(order => order.owner === 'Station_1')
      
      // console.log('Parsed Drone Data:', filteredDroneData)
      filteredDroneData.forEach(order => {
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
  if (lineChart.value && showLineChart.value) {
    lineChart.value.resize()
  }
}

// 生成随机流量数据的函数
const generateRandomTimeData = (areaName) => {
  const now = new Date()
  const data = []
  
  // 检查是否是回收区域
  const isRecyclingArea = ['Block 1B', 'Block 2B', 'Block 3', 'Block 5A', 'Block 5B'].includes(areaName)
  
  // 生成过去24小时的数据，每小时一个点
  for (let i = 23; i >= 0; i--) {
    const time = new Date(now)
    time.setHours(now.getHours() - i)
    
    const orderValue = Math.floor(Math.random() * 10) + 1  // 1-10的随机数
    const recyclingValue = isRecyclingArea ? Math.floor(Math.random() * 8) + 1 : 0  // 回收区域有回收数据
    
    data.push({
      time: time.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
      orderValue: orderValue,
      recyclingValue: recyclingValue,
      isRecycling: isRecyclingArea  // 添加回收标记
    })
  }
  
  return data
}

// 生成总流量数据
const generateTotalTrafficData = () => {
  const now = new Date()
  const data = []
  
  // 生成过去24小时的数据，每小时一个点
  for (let i = 23; i >= 0; i--) {
    const time = new Date(now)
    time.setHours(now.getHours() - i)
    
    // 订单流量值较大，范围在20-50之间
    const orderValue = Math.floor(Math.random() * 30) + 20
    // 回收流量值较小，范围在10-30之间
    const recyclingValue = Math.floor(Math.random() * 20) + 10
    
    data.push({
      time: time.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
      orderValue: orderValue,
      recyclingValue: recyclingValue
    })
  }
  
  return data
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
    
    // 为回收区域添加特殊标记
    const markPoints = recyclingAreas.map(area => {
      const areaData = unifiedData.value.find(item => item.name === area)
      return {
        name: area,
        value: areaData ? areaData.value : 0,
        itemStyle: {
          color: '#3498db'  // 蓝色标记
        },
        label: {
          show: true,
          formatter: '{b}',
          fontSize: 8,
          color: '#fff',
          backgroundColor: '#3498db',
          padding: [2, 4]
        }
      }
    })
    
    const option = {
      title: [
        {
          text: "Order Distribution Map",
          left: "center",
          textStyle: {
            color: "#44652a",
            fontSize: 12
          },
          top: "0%",
        },
        {
          text: "Blue Areas: Recycling Places",
          left: "center",
          textStyle: {
            color: "#3498db",
            fontSize: 10
          },
          top: "4%",
        }
      ],
      tooltip: {
        trigger: 'item',
        formatter: function(params) {
          const isRecyclingArea = recyclingAreas.includes(params.name)
          return `${params.name}: ${params.value} ${isRecyclingArea ? '(Recycling Place)' : ''}`
        }
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
      series: [
        {
          name: "Orders",
          type: "map",
          map: "hkust_gz_map",
          roam: true,
          emphasis: {
            label: {
              show: false,
            },
            itemStyle: {
              areaColor: '#FFA500',  // 鼠标悬停时变为橙色
            }
          },
          selectedMode: 'single',  // 改为单选模式
          select: {
            itemStyle: {
              areaColor: '#FFFF00'  // 选中时变为黄色
            }
          },
          data: unifiedData.value.map(item => {
            // 为回收区域添加特殊样式
            if (recyclingAreas.includes(item.name)) {
              return {
                ...item,
                itemStyle: {
                  areaColor: 'rgba(52, 152, 219, 0.3)',  // 蓝色半透明背景
                  borderColor: '#3498db',
                  borderWidth: 1
                }
              }
            }
            return item
          }),
          itemStyle: {
            areaColor: '#fff',
            borderColor: '#ccc'
          },
          // 添加布局相关配置
          layoutCenter: ['50%', '50%'],
          layoutSize: '140%',
          aspectScale: 1
        }
      ]
    }
    
    // 生成总流量数据
    totalTrafficData.value = generateTotalTrafficData()
    
    // 默认显示总流量图
    selectedAreaName.value = ''
    selectedAreaData.value = totalTrafficData.value
    initLineChart()
    
    if (myChart.value) {
      myChart.value.setOption(option, true)
      
      // 添加点击事件监听
      myChart.value.on('click', function(params) {
        if (params.componentType === 'series' && params.seriesType === 'map') {
          const areaName = params.name
          const areaData = unifiedData.value.find(item => item.name === areaName)
          
          if (areaData) {
            // 如果点击的是当前选中的区域，则取消选中并显示总流量图
            if (selectedAreaName.value === areaName) {
              myChart.value.dispatchAction({
                type: 'mapUnSelect',
                seriesIndex: 0,
                name: areaName
              })
              selectedAreaName.value = ''
              selectedAreaData.value = totalTrafficData.value
              initLineChart()
            } else {
              // 否则选中新区域并显示该区域的流量图
              selectedAreaName.value = areaName
              selectedAreaData.value = generateRandomTimeData(areaName)
              initLineChart()
            }
          }
        }
      })
    }
  } catch (error) {
    console.error("初始化图表失败:", error)
  }
}

// 添加线图相关变量
const lineChart = ref(null)

// 修改初始化线图的函数
const initLineChart = () => {
  // 获取线图容器
  const dom = document.getElementById("Container_Area_Traffic")
  if (!dom) {
    console.error('找不到线图容器元素')
    return
  }
  
  // 如果已有实例，先销毁
  if (lineChart.value) {
    lineChart.value.dispose()
  }
  
  // 创建新实例
  lineChart.value = echarts.init(dom)
  
  // 检查是否是回收区域或总流量图
  const isRecyclingArea = selectedAreaName.value && 
    ['Block 1B', 'Block 2B', 'Block 3', 'Block 5A', 'Block 5B'].includes(selectedAreaName.value)
  const isTotalFlow = !selectedAreaName.value
  
  // 设置线图标题
  const title = selectedAreaName.value ? 
    `${selectedAreaName.value} Flow` : 
    'Total Order Flow'
  
  // 准备系列数据
  const series = [
    {
      name: 'Order Flow',
      type: 'line',
      smooth: true,
      data: selectedAreaData.value.map(item => item.orderValue || item.value),
      itemStyle: {
        color: '#91CC75'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(145, 204, 117, 0.5)' },
            { offset: 1, color: 'rgba(145, 204, 117, 0.1)' }
          ]
        }
      }
    }
  ]
  
  // 如果是回收区域或总流量图，添加回收流量线
  if (isRecyclingArea || isTotalFlow) {
    series.push({
      name: 'Recycling Flow',
      type: 'line',
      smooth: true,
      data: selectedAreaData.value.map(item => item.recyclingValue || 0),
      itemStyle: {
        color: '#3498db'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(52, 152, 219, 0.5)' },
            { offset: 1, color: 'rgba(52, 152, 219, 0.1)' }
          ]
        }
      }
    })
  }
  
  // 设置线图选项
  const option = {
    title: {
      text: title,
      left: 'center',
      textStyle: {
        color: "#44652a",
        fontSize: 12
      }
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: (isRecyclingArea || isTotalFlow) ? ['Order Flow', 'Recycling Flow'] : ['Order Flow'],
      top: '10%',
      textStyle: {
        fontSize: 10
      }
    },
    xAxis: {
      type: 'category',
      data: selectedAreaData.value.map(item => item.time),
      axisLabel: {
        fontSize: 10
      }
    },
    yAxis: {
      type: 'value',
      name: 'Count',
      nameTextStyle: {
        fontSize: 10
      },
      axisLabel: {
        fontSize: 10
      }
    },
    series: series,
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%'
    }
  }
  
  lineChart.value.setOption(option)
}

// 在 watch 部分添加回收区域的样式应用
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
          data: unifiedData.value.map(item => {
            // 为回收区域添加特殊样式
            if (recyclingAreas.includes(item.name)) {
              return {
                ...item,
                itemStyle: {
                  areaColor: 'rgba(52, 152, 219, 0.3)',  // 蓝色半透明背景
                  borderColor: '#3498db',
                  borderWidth: 1
                }
              }
            }
            return item
          })
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

// 定义回收区域列表作为常量，便于复用
const recyclingAreas = ['Block 1B', 'Block 2B', 'Block 3', 'Block 5A', 'Block 5B']

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
          data: unifiedData.value.map(item => {
            // 为回收区域添加特殊样式
            if (recyclingAreas.includes(item.name)) {
              return {
                ...item,
                itemStyle: {
                  areaColor: 'rgba(52, 152, 219, 0.3)',  // 蓝色半透明背景
                  borderColor: '#3498db',
                  borderWidth: 1
                }
              }
            }
            return item
          })
        }]
      })
      
      // 如果没有选中区域，更新总流量数据
      if (!selectedAreaName.value) {
        totalTrafficData.value = generateTotalTrafficData()
        selectedAreaData.value = totalTrafficData.value
        initLineChart()
      }
    }
  }, 60000) // 60秒刷新一次
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (myChart.value) {
    myChart.value.dispose()
  }
  if (lineChart.value) {
    lineChart.value.dispose()
  }
  // 清除自动刷新定时器
  if (autoRefresh.value) {
    clearInterval(autoRefresh.value)
  }
})
</script>

<style scoped>
#Container_Order_Distribution {
  width: 100%;
  height: 48vh;
  min-height: 100px;
}
#Container_Area_Traffic {
  width: 100%;
  height: 25vh;
  min-height: 100px;
  margin-top: 10px;
}
.title-container {
  text-align: center;
  font-weight: bold;
}
</style>
