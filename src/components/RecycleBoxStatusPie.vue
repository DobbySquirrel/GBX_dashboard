<template>
  <div class="chart-container">
    <div id="LockerStatusPieChart"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";

export default {
  name: "LockerStatusPieChart",
  props: {
    Box_owner: {
      type: [String, null],
      required: true,
    },
  },
  data() {
    return {
      chartData: [], // Parsed chart data
    };
  },
  watch: {
    Box_owner: {
      handler(newVal) {
        if (newVal) {
          this.updateChartData(newVal);
        }
      },
      immediate: true
    }
  },
  mounted() {
    if (this.Box_owner) {
      this.updateChartData(this.Box_owner);
    }
    window.addEventListener('resize', this.handleResize);
  },
  unmounted() {
    window.removeEventListener('resize', this.handleResize);
    if (this.myChart) {
      this.myChart.dispose();
    }
  },
  methods: {
    updateChartData(csvData) {
      const parsedData = this.parseCsvData(csvData);
      const latestStatuses = this.getLatestStatuses(parsedData);
      this.renderStatusPieChart(latestStatuses);
    },

    parseCsvData(csvData) {
      if (!csvData) return [];
      const lines = csvData.trim().split("\n");
      return lines.slice(1).reverse().map(line => {
        const values = line.split(",");
        return {
          event_time: values[0]?.trim() || 'N/A',
          RFID: values[5]?.trim() || 'N/A',
          Status: values[3]?.trim() || 'N/A'
        };
      });
    },

    getLatestStatuses(data) {
      if (!data.length) return [];
      const latestStatuses = {};
      data.forEach(item => {
        if (!latestStatuses[item.RFID]) {
          latestStatuses[item.RFID] = item.Status;
        }
      });
      return Object.values(latestStatuses);
    },

    handleResize() {
      const chartDom = document.getElementById("LockerStatusPieChart");
      if (chartDom) {
        const chartInstance = echarts.init(chartDom);
        chartInstance.resize();
      }
    },

    renderStatusPieChart(statuses) {
      const statusCount = statuses.reduce((acc, status) => {
        if (status === "UserInfo") status = "InWarehouse";
        acc[status] = (acc[status] || 0) + 1;
        return acc;
      }, {});

      // 定义固定的状态顺序
      const statusOrder = [
        'InWarehouse',
        'BoxOut',
        'OutdoorDeliveryOrder',
        'DroneDeliveryOrder',
        'IndoorDeliveryOrder',
        'InputDelivery',
        'OutputDelivery',
        'RecycleInDelivery',
        'RecycleOutDelivery'
      ];

      // 按照预定义顺序重新组织数据
      const orderedData = statusOrder.map(status => ({
        value: statusCount[status] || 0,
        name: status,
        itemStyle: { 
          color: (status === 'RecycleInDelivery' || status === 'RecycleOutDelivery') 
            ? "rgba(145, 204, 117, 0.5)"
            : "rgba(250, 200, 88, 0.5)"
        }
      }));

      var chartDom = document.getElementById("LockerStatusPieChart");
      var myChart = echarts.init(chartDom);
      var option = {
        title: {
          text: "Boxes Status",
          left: "center",
          textStyle: {
            color: "#44652a",
            fontSize: 12
          },
          top: "-2%",
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow"
          }
        },
        grid: {
          left: '7%',
          right: '4%',
          bottom: '0%',
          top: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: statusOrder,  // 使用预定义的顺序
          axisLabel: {
            color: "#44652a",
            interval: 0,
            rotate: 30,
            fontSize: 9
          }
        },
        yAxis: {
          type: 'value',
          show: false,  // 隐藏Y轴
          splitLine: {
            show: false  // 隐藏背景网格线
          }
        },
        series: [
          {
            name: "Package Status",
            type: "bar",
            data: orderedData,  // 使用排序后的数据
            label: {
              show: true,
              position: 'top',
              color: "#44652a",
              fontSize: 9
            },
            barWidth: '40%'
          }
        ]
      };
      
      myChart.setOption(option);
      this.myChart = myChart;
    },
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 15vh;
  display: flex;
  flex-direction: column;
}

#LockerStatusPieChart {
  width: 100%;
  height: 100%;
  flex: 1;
  min-height: 160px;
}
</style>