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
      StatusMap: {
        'UserInfo': 'Warehouse',
        'DroneDeliveryOrder': 'Delivering',
        'InputDelivery': 'Deposit',
        'OutputDelivery': 'Pickup',
        'RecycleInDelivery': 'RecycleIn',
        'RecycleOutDelivery': 'RecycleOut',
      }
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
          latestStatuses[item.RFID] = this.StatusMap[item.Status] || item.Status;
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
        acc[status] = (acc[status] || 0) + 1;
        return acc;
      }, {});

      const data = Object.entries(statusCount).map(([name, value]) => ({
        value,
        name,
        itemStyle: { 
          color: (name === 'RecycleIn' || name === 'RecycleOut') 
            ? "rgba(145, 204, 117, 0.5)"  // 绿色 - 回收相关状态
            : "rgba(250, 200, 88, 0.5)"   // 黄色 - 其他状态
        }
      }));

      var chartDom = document.getElementById("LockerStatusPieChart");
      var myChart = echarts.init(chartDom);
      var option = {
        title: {
          text: "Locker Status",
          left: "center",
          textStyle: {
            color: "#44652a",
          },
          top: "0%",
        },
        tooltip: {
          trigger: "item",
        },
       
        series: [
          {
            name: "Package Status",
            type: "pie",
            radius: ["30%", "50%"],
            itemStyle: {
              borderRadius: 6,
              borderColor: "#fff",
              borderWidth: 2,
            },
            data: data,
            labelLine: {
              smooth: 0.2,
              length: 2,
              length2: 2,
            },
            label: {
              show: true,
              position: 'top',
              formatter: '{b}:{c}',
              color: "#44652a",
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 200,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
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
  min-height: 140px;
}
</style>