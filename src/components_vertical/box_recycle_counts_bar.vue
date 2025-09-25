<template>
    <div class="chart-container">
      <div id="BoxRecycleCountChart"></div>
    </div>
  </template>
  
  <script>
  import * as echarts from "echarts";
  import socket from "../api/socket.js";
  
  export default {
    name: "BoxRecycleCountChart", // Or box_recycle_counts_bar
    data() {
      return {
        myChart: null,
        boxRecycleCountsData: [],
      };
    },
    mounted() {
      this.initChart();
      window.addEventListener('resize', this.handleResize);
  
      if (socket) {
        socket.emit('subscribe_box_recycle_counts');
        socket.on('box_recycle_counts_update', (data) => {
          console.log('Received box_recycle_counts_update:', data);
          this.boxRecycleCountsData = data;
          this.updateChart();
        });
      } else {
        console.error('Socket.IO instance not found. Ensure socket.js is correctly configured.');
      }
    },
    unmounted() {
      window.removeEventListener('resize', this.handleResize);
      if (this.myChart) {
        this.myChart.dispose();
      }
      if (socket) {
        socket.off('box_recycle_counts_update');
      }
    },
    methods: {
      initChart() {
        const chartDom = document.getElementById('BoxRecycleCountChart');
        this.myChart = echarts.init(chartDom);
        this.updateChart();
      },
      updateChart() {
        if (!this.boxRecycleCountsData || this.boxRecycleCountsData.length === 0) {
          this.myChart.setOption({
            title: {
              text: "No Box Recycle Data Available",
              left: "center",
              textStyle: {
                color: "#44652a",
                fontSize: 16,
                fontWeight: "bold"
              }
            },
            xAxis: { show: false },
            yAxis: { show: false },
            series: [],
            tooltip: {}
          }, true);
          return;
        }
  
        // Sort data by recycle_count in descending order
        const sortedData = [...this.boxRecycleCountsData].sort((a, b) => b.recycle_count - a.recycle_count);
  
        // --- Display only the top 10 ---
        const top10Data = sortedData.slice(0, 10);
  
        // Extract box_ids and recycle_counts for the chart from the top 10
        const boxIds = top10Data.map(item => item.box_id);
        const recycleCounts = top10Data.map(item => item.recycle_count);
  
        // --- Calculate Average Recycle Count for the displayed data ---
        const totalRecycleCount = recycleCounts.reduce((sum, count) => sum + count, 0);
        const averageRecycleCount = top10Data.length > 0 ? (totalRecycleCount / top10Data.length).toFixed(2) : 0;
  
        const option = {
          title: {
            text: "回收次数前10的箱体ID", // Updated title
            left: "center",
            textStyle: {
              color: "#44652a",
              fontSize: 16,
              fontWeight: "bold"
            },
            top: "0",
          },
          tooltip: {
            trigger: "axis",
            axisPointer: {
              type: "shadow"
            }
          },
          grid: {
            left: '10%',
            right: '3%',
            bottom: '5%', // Give more space at the bottom for potentially more rotated labels
            top: '15%', // Give more space at the top for title and label
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: boxIds,
            axisLabel: {
              color: "#44652a",
              interval: 0,
              rotate: 45, // Keep rotation for readability
              fontSize: 10,
              formatter: function(value) {
                return value.length > 8 ? '...' + value.slice(-8) : value;
              }
            },
            axisTick: {
              alignWithLabel: true
            },
            z: 10
          },
          yAxis: {
            type: 'value',
            name: 'Count',
            nameTextStyle: {
              color: "#44652a",
              fontSize: 12
            },
            axisLabel: {
              color: "#44652a",
              fontSize: 10
            },
            splitLine: {
              lineStyle: {
                type: 'dashed',
                color: '#e0e0e0'
              }
            },
            minInterval: 1 // Ensure y-axis shows integer ticks for counts
          },
          series: [
            {
              name: "Recycle Count",
              type: "bar",
              data: recycleCounts,
              itemStyle: {
                color: "#e0e9d2",
                borderRadius: [5, 5, 0, 0]
              },
              label: {
                show: true,
                position: 'top',
                color: "#44652a",
                fontSize: 12,
                fontWeight: "bold"
              },
              barWidth: '60%',
              // --- Add markLine for average ---

            }
          ]
        };
  
        this.myChart.setOption(option, true);
      },
      handleResize() {
        if (this.myChart) {
          this.myChart.resize();
        }
      }
    },
  };
  </script>
  
  <style scoped>
  .chart-container {
    width: 100%;
    height: 100%; /* Will take 100% of the parent's height */
    display: flex;
    flex-direction: column;
  }
  
  #BoxRecycleCountChart {
    width: 100%;
    height: 100%; /* Will take 100% of the container's height */
    flex: 1;
    min-height: 100px; /* This is a fallback, actual height comes from parent */
  }
  </style>