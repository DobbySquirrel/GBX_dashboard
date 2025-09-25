<template>
  <div class="chart-container">
    <div class="title-container">
      <el-text class="mx-1" style="font-size: 16px; color: #44652a; font-weight: bold;">
        箱体状态
      </el-text>
    </div>
    <div id="BoxStatusChart"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import socket from "../api/socket.js" // Ensure this path is correct for your Socket.IO client

export default {
  name: "BoxStatusChart",
  data() {
    return {
      myChart: null, // Store the ECharts instance
    };
  },
  mounted() {
    this.myChart = echarts.init(document.getElementById("BoxStatusChart"));
    this.renderStatusChart({}); // Render an empty chart initially
    window.addEventListener('resize', this.handleResize);
    this.setupSocketListener();
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
    if (this.myChart) {
      this.myChart.dispose();
    }
    this.removeSocketListener();
  },
  methods: {
    setupSocketListener() {
      // CORRECTED: Emit the correct subscription event
      socket.emit('subscribe_box_status_counts');
      // CORRECTED: Listen for the correct update event
      socket.on('box_status_counts_update', this.handleBoxStatusSummaryUpdate);
    },
    removeSocketListener() {
      // CORRECTED: Remove listener for the correct update event
      socket.off('box_status_counts_update', this.handleBoxStatusSummaryUpdate);
    },
    handleBoxStatusSummaryUpdate(summaryArray) {
      console.log('原始数据 - 接收到的箱子状态汇总 (Raw Data):', summaryArray);

      const transformedSummary = {};
      summaryArray.forEach(item => {
        if (item.status && typeof item.count === 'number') {
          transformedSummary[item.status] = item.count;
        }
      });

      console.log('处理后的数据 - 转换为对象格式 (Processed Data - Object Format):', transformedSummary);

      this.renderStatusChart(transformedSummary);
    },
    handleResize() {
      if (this.myChart) {
        this.myChart.resize();
      }
    },
    renderStatusChart(statusCounts) {
      const categoriesForXAxis = Object.keys(statusCounts).sort();
      const dataForSeries = categoriesForXAxis.map(status => {
        return {
          value: statusCounts[status] || 0,
          name: status,
          itemStyle: {
            color: (status.includes('Recycle') || status === '已回到仓库')
              ? "rgba(145, 204, 117, 0.7)"
              : "rgba(250, 200, 88, 0.7)"
          }
        };
      });

      var option = {
        // title: {
        //   text: "Boxes Status",
        //   left: "center",
        //   textStyle: {
        //     color: "#44652a",
        //     fontSize: 16,
        //     fontWeight: "bold"
        //   },
        //   top: "0",
        // },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow"
          }
        },
        grid: {
          left: '3%',
          right: '10%',
          bottom: '5%',
          top: '20%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: categoriesForXAxis,
          axisLabel: {
            color: "#44652a",
            interval: 0,
            rotate: 30,
            fontSize: 12,
          
          }
        },
        yAxis: {
          type: 'value',
          show: false,
          splitLine: {
            show: false
          }
        },
        series: [
          {
            name: "Package Status",
            type: "bar",
            data: dataForSeries,
            label: {
              show: true,
              position: 'top',
              color: "#44652a",
              fontSize: 12,
              fontWeight: "bold"
            },
            barWidth: '50%'
          }
        ]
      };

      this.myChart.setOption(option, true);
    },
  },
};
</script>


<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center; 

}
.title-container {
  text-align: center;
  margin-bottom: 10px;
  margin-top: -10px;
}
#BoxStatusChart {
  width: 100%;
  height: 100%;
  flex: 1;
  min-height: 120px;
  align-items: center; 
}
</style>