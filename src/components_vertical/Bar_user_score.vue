<template>
  <div class="chart-container">
    <div id="UserScoreBarChart"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import socket from "../api/socket.js"; 

export default {
  name: "UserScoreBarChart",

  data() {
    return {
      chartData: [],
      myChart: null, // Initialize myChart to null
    };
  },

  mounted() {
    // console.log("Component mounted, userScoreRecord: ", this.userScoreRecord);
    this.myChart = echarts.init(document.getElementById("UserScoreBarChart"));
    this.renderBarChart(this.chartData); // Render with initial empty data

    // Listen for real-time updates from the server
    socket.on('user_score_update', (data) => {
      // console.log('Received user_score_update:', data);
      this.updateChartData(data);
    });

    // Request initial data when component mounts
    socket.emit('subscribe_user_score');

    window.addEventListener('resize', this.handleResize);
  },
  unmounted() {
    window.removeEventListener('resize', this.handleResize);
    if (this.myChart) {
      this.myChart.dispose();
    }
    // Clean up socket listener
    socket.off('user_score_update');
  },
  methods: {
    updateChartData(data) {
      // console.log("Updating chart data with: ", data);
      this.chartData = data; // Assign the directly received data
      this.renderBarChart(this.chartData);
    },

    handleResize() {
      if (this.myChart) {
        this.myChart.resize();
      }
    },

    renderBarChart(data) {
      if (!this.myChart) {
        // console.error("ECharts instance not initialized.");
        return;
      }
      
      // Sort data by score in descending order
      data.sort((a, b) => b.total_points - a.total_points);

      // Get the top 5 and bottom 5 data
      const top5 = data.slice(0, 5);
      // Ensure bottom5 always contains unique users if data.length is small
      const bottom5StartIndex = Math.max(data.length - 5, 0);
      let bottom5 = data.slice(bottom5StartIndex);

      // Filter out any users from bottom5 that are already in top5 to avoid redundancy
      const top5Phones = new Set(top5.map(item => item.phone));
      bottom5 = bottom5.filter(item => !top5Phones.has(item.phone));


      // Combine them
      let displayData = [];
      if (data.length <= 10) {
        displayData = data; // If 10 or fewer items, show all
      } else {
        displayData = [...top5, ...bottom5];
        // Re-sort the combined data for consistent display if necessary
        displayData.sort((a, b) => b.total_points - a.total_points);
      }

      var option = {
        title: {
          text: "User Cumulative Points (Top 5 & Bottom 5)",
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
          left: '0%',
          right: '10%',
          bottom: '5%',
          top: '20%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: displayData.map(item => item.phone),
          axisLabel: {
            color: "#44652a",
            interval: 0,
            rotate: 30,
            fontSize: 10,
            formatter: function(value) {
              return value.length > 4 ? value.slice(-4) : value;
            }
          }
        },
        yAxis: {
          type: 'value',
          name: 'Score',
          nameTextStyle: {
            color: "#44652a",
            fontSize: 12
          },
          axisLabel: {
            color: "#44652a",
            fontSize: 10
          }
        },
        series: [
          {
            name: "Return Score",
            type: "bar",
            data: displayData.map(item => ({
              value: item.total_points,
              itemStyle: {
                // Determine color based on whether the item is in the bottom 5
                color: bottom5.some(bottomItem => bottomItem.phone === item.phone) 
                        ? "rgba(255, 99, 71, 0.7)" // Red for bottom 5
                        : (item.total_points >= 0 ? "rgba(145, 204, 117, 0.7)" : "rgba(255, 99, 71, 0.7)") // Original logic for others
              }
            })),
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

      this.myChart.setOption(option);
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
  justify-content: flex-start;
  align-items: flex-start;
}

#UserScoreBarChart {
  width: 100%;
  height: 100%;
  flex: 1;
  min-height: 120px;
}
</style>