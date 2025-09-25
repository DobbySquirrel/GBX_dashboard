<template>
  <div class="chart-container">
    <div ref="chart" id="RecycleCabinetOccupancyLine"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import { boxDataURI } from "../assets/symbols/BoxSymbol.js";
import { paperboxDataURI } from "../assets/symbols/paperboxSymbol.js";
import { treeDataURI } from "../assets/symbols/treeSymbol.js";

import socket from "../api/socket.js"; // 直接导入 socket 实例
import { onMounted, nextTick } from 'vue';

export default {
  data() {
    return {
      recycleBoxCount: 0,
      myChart: null,
      chartInitialized: false,
      averageRecycleCycle: 0, // 添加这个变量来存储平均回收周期
      totalRecycledBoxes: 0, // Added to store total recycled boxes
    };
  },
  methods: {
    handleRecycleCountsUpdate(data) {
      try {
        let totalRecycleCount = 0;
        
        if (Array.isArray(data)) {
          totalRecycleCount = data.reduce((sum, item) => {
            return sum + (parseInt(item.recycle_count) || 0);
          }, 0);
        }
        
        this.recycleBoxCount = totalRecycleCount;
        console.log('Updated recycling box count:', totalRecycleCount);
        
        // 确保图表已初始化后再更新
        if (this.chartInitialized) {
          this.updateChart();
        } else {
          this.initChart(); // 如果图表还未初始化，先初始化
        }
      } catch (error) {
        console.error('Error processing recycle counts data:', error);
      }
    },

    handleAverageRecycleCycleUpdate(data) {
      try {
        this.averageRecycleCycle = data;
        console.log('收到平均回收周期更新:', this.averageRecycleCycle);
        if (this.chartInitialized) {
          this.updateChart();
        }
      } catch (error) {
        console.error('处理平均回收周期数据时出错:', error);
      }
    },

    initChart() {
      const chartDom = this.$refs.chart;
      if (!chartDom) {
        console.warn('Chart DOM element not found');
        return;
      }

      // 如果已经有实例，先销毁
      if (this.myChart) {
        this.myChart.dispose();
      }

      try {
        this.myChart = echarts.init(chartDom);
        this.chartInitialized = true;
        this.updateChart();
      } catch (error) {
        console.error('Failed to initialize chart:', error);
      }
    },

    updateChart() {
      if (!this.myChart || !this.chartInitialized) {
        console.warn('图表尚未初始化');
        return;
      }

      const boxSymbolURI = boxDataURI;
      const treeSymbolURI = treeDataURI;
      const paperboxSymbolURI = paperboxDataURI;

      const option = {
        title: {
          text: '碳排放增益对比',
          left: 'center',
          textStyle: {
            color: '#44652a',
            fontSize: 16,
            fontWeight: 'bold'
          },
          top: 0
        },
        xAxis: [{
  name: '等价类型',
  nameLocation: 'center',
  nameGap: 35,
  nameTextStyle: {
    color: '#44652a',
    fontSize: 12,
    fontWeight: 'bold'
  },
  data: ['Recycling Box', 'Tree Leaf', 'Paper Box'],
  axisTick: { show: false },
  axisLine: { show: false },
  axisLabel: {
    margin: 20,
    color: '#44652a',
    fontSize: 12,
    interval: 0,
    padding: [0, 0, 0, 0]
  }
}],
        yAxis: {
          splitLine: { show: false },
          axisTick: { show: false },
          axisLine: { show: false },
          axisLabel: { show: false }
        },
        animationEasing: 'elasticOut',
        series: [
          {
            type: 'pictorialBar',
            name: '回收箱',
            emphasis: {
              scale: true
            },
            label: {
              show: true,
              position: 'top',
              formatter: '{c}',
              fontSize: 14,
              color: '#44652a',
              fontWeight: 'bold'
            },
            data: [
              {
                value: this.totalRecycledBoxes || 0,
                symbol: 'image://' + boxDataURI,
                symbolRepeat: true,
                symbolSize: ['50%', '5%'],
                symbolMargin: '-20%',
                animationDelay: function (dataIndex, params) {
                  return params.index * 30;
                }
              },
              {
                value: Math.floor((this.recycleBoxCount || 0) * 2),
                symbol: 'image://' + treeDataURI,
                symbolRepeat: true,
                symbolSize: ['12%', '12%'],
                symbolMargin: '0%',
                animationDelay: function (dataIndex, params) {
                  return params.index * 30;
                },
                label: {
                  show: true,
                  position: 'top',
                  formatter: '{c}',
                  fontSize: 14,
                  color: '#44652a',
                  fontWeight: 'bold'
                }
              },
              {
                value: (this.recycleBoxCount || 0),
                symbol: 'image://' + paperboxDataURI,
                symbolRepeat: true,
                symbolSize: ['45%', '22%'],
                symbolMargin: '-20%',
                animationDelay: function (dataIndex, params) {
                  return params.index * 30;
                },
                label: {
                  show: true,
                  position: 'top',
                  formatter: '{c}',
                  fontSize: 14,
                  color: '#44652a',
                  fontWeight: 'bold'
                }
              }
            ]
          },
          {
            name: '底座',
            type: 'pictorialBar',
            barGap: '-100%',
            symbol: 'rect',
            itemStyle: {
              color: '#e0e9d2'
            },
            silent: true,
            symbolOffset: [0, '50%'],
            z: -10,
            data: [
              {
                value: 1,
                symbolSize: ['130%', 12]
              },
              {
                value: 1,
                symbolSize: ['130%', 12]
              },
              {
                value: 1,
                symbolSize: ['130%', 12]
              }
            ]
          }
        ],
        grid: {
          left: '3%',
          right: '5%',
          bottom: '15%',
          top: '12%',
          containLabel: true
        },
      };

      try {
        this.myChart.setOption(option, true);
      } catch (error) {
        console.error('更新图表失败:', error);
      }
    },

    handleResize() {
      if (this.myChart && this.chartInitialized) {
        this.myChart.resize();
      }
    },
  },
  mounted() {
    nextTick(async () => {
      try {
        await this.$nextTick();
        this.initChart();

        if (socket) {
          // 订阅箱子回收次数
          socket.emit('subscribe_box_recycle_counts');
          socket.on('box_recycle_counts_update', this.handleRecycleCountsUpdate);

          // 订阅平均回收周期
          socket.emit('subscribe_average_recycle_cycle');
          socket.on('average_recycle_cycle_update', this.handleAverageRecycleCycleUpdate);

          // 订阅总回收箱子数量
          socket.emit('subscribe_total_recycled_boxes');
          
          // 监听总回收箱子数量更新
          socket.on('total_recycled_boxes_update', (data) => {
            this.totalRecycledBoxes = data.totalRecycledBoxes;
            console.log('总回收箱子数量:', this.totalRecycledBoxes);
          });
        } else {
          console.error('Socket.IO 实例未找到');
        }

        window.addEventListener('resize', this.handleResize);
      } catch (error) {
        console.error('组件挂载时出错:', error);
      }
    });
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
    
    if (socket) {
      socket.off('box_recycle_counts_update', this.handleRecycleCountsUpdate);
      socket.off('average_recycle_cycle_update', this.handleAverageRecycleCycleUpdate);
      socket.off('total_recycled_boxes_update');
    }
    
    if (this.myChart) {
      this.myChart.dispose();
      this.myChart = null;
    }
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
}
#RecycleCabinetOccupancyLine {
  width: 100%;
  height: 100%;
}
</style>