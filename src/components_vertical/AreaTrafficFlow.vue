<template>
  <div>
    <div id="Container_Area_Traffic"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from "echarts"

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
const lineChart = ref(null)
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

const handleResize = () => {
  if (lineChart.value) {
    lineChart.value.resize()
  }
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

// 初始化线图的函数
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
  
  // 添加事件隔离
  lineChart.value.getZr().on('click', (event) => {
    // 阻止事件冒泡
    event.event.stopPropagation();
    event.event.preventDefault();
  });
  
  // 设置线图选项
  const option = {
    title: {
      text: 'Total Order Flow',
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
      data: ['Order Flow', 'Recycling Flow'],
      top: '10%',
      textStyle: {
        fontSize: 10
      }
    },
    xAxis: {
      type: 'category',
      data: totalTrafficData.value.map(item => item.time),
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
    series: [
      {
        name: 'Order Flow',
        type: 'line',
        smooth: true,
        data: totalTrafficData.value.map(item => item.orderValue),
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
      },
      {
        name: 'Recycling Flow',
        type: 'line',
        smooth: true,
        data: totalTrafficData.value.map(item => item.recyclingValue),
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
      }
    ],
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%'
    }
  }
  
  lineChart.value.setOption(option)
}

// 添加自动刷新功能
const autoRefresh = ref(null)

onMounted(() => {
  // 生成总流量数据
  totalTrafficData.value = generateTotalTrafficData()
  
  // 初始化图表
  initLineChart()
  
  window.addEventListener('resize', handleResize)
  
  // 设置自动刷新间隔（例如每60秒刷新一次）
  autoRefresh.value = setInterval(() => {
    totalTrafficData.value = generateTotalTrafficData()
    initLineChart()
  }, 60000) // 60秒刷新一次
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (lineChart.value) {
    lineChart.value.dispose()
  }
  // 清除自动刷新定时器
  if (autoRefresh.value) {
    clearInterval(autoRefresh.value)
  }
})

// 不再需要 updateSelectedArea 方法
</script>

<style scoped>
#Container_Area_Traffic {
  width: 100%;
  height: 100%;
  min-height: 100px;
}
</style> 