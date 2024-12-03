<template>
  <div class="chart-container">
    <div id="UserScoreBarChart"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";

export default {
  name: "UserScoreBarChart",
  props: {
    userScoreRecord: {
      type: [String, null],
      required: true,
    },
  },
  data() {
    return {
      chartData: [],
    };
  },
  watch: {
    userScoreRecord: {
      handler(newVal) {
        console.log("userScoreRecord updated: ", newVal);
        if (newVal) {
          this.updateChartData(newVal);
        }
      },
      immediate: true
    }
  },
  mounted() {
    console.log("Component mounted, userScoreRecord: ", this.userScoreRecord);
    if (this.userScoreRecord) {
      this.updateChartData(this.userScoreRecord);
    }
    window.addEventListener('resize', this.handleResize);
  },
  unmounted() {
    console.log("Component unmounted");
    window.removeEventListener('resize', this.handleResize);
    if (this.myChart) {
      this.myChart.dispose();
    }
  },
  methods: {
    updateChartData(csvData) {
      console.log("Updating chart data with CSV: ", csvData);
      const parsedData = this.parseCsvData(csvData);
      console.log("Parsed data: ", parsedData);
      this.renderBarChart(parsedData);
    },

    parseCsvData(csvData) {
      if (!csvData) {
        console.warn("No CSV data provided");
        return [];
      }

      const lines = csvData.trim().split("\n");
      console.log("CSV lines: ", lines);
      const data = lines.slice(1).map(line => {
        const values = line.split(",");
        console.log("Parsed line values: ", values);
        return {
          phone: values[0]?.trim() || 'N/A',
          score: parseInt(values[1]?.trim()) || 0,
        };
      });
      console.log("Final parsed data: ", data);
      return data;
    },

    handleResize() {
      console.log("Handling resize event");
      if (this.myChart) {
        this.myChart.resize();
      }
    },

    renderBarChart(data) {
      console.log("Rendering bar chart with data: ", data);
      // 按分数排序
      data.sort((a, b) => b.score - a.score);

      var chartDom = document.getElementById("UserScoreBarChart");
      if (!chartDom) {
        console.error("Chart DOM element not found");
        return;
      }
      var myChart = echarts.init(chartDom);
      var option = {
        title: {
          text: "User Cumulative Points",
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
          top: '30%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: data.map(item => item.phone),
          axisLabel: {
            color: "#44652a",
            interval: 0,
            rotate: 30,
            fontSize: 9,
            formatter: function(value) {
              // 如果字符串长度超过4，显示后4位
              return value.length > 4 ? value.slice(-4) : value;
            }
          }
        },
        yAxis: {
          type: 'value',
          name: 'Score',
          nameTextStyle: {
            color: "#44652a"
          },
          axisLabel: {
            color: "#44652a"
          }
        },
        series: [
          {
            name: "Return Score",
            type: "bar",
            data: data.map(item => ({
              value: item.score,
              itemStyle: {
                color: item.score >= 0 ? "rgba(145, 204, 117, 0.5)" : "rgba(255, 99, 71, 0.5)"
              }
            })),
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
  height: 30vh;
  display: flex;
  flex-direction: column;
}

#UserScoreBarChart {
  width: 100%;
  height: 100%;
  flex: 1;
  min-height: 160px;
}
</style>