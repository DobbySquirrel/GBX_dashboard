<template>
  <div class="chart-container">
    <div id="OrderCountChart"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import socket from "../api/socket.js"; // Import your Socket.IO client instance

export default {
  name: "Order Quantity Trend",
  data() {
    return {
      myChart: null, // Initialize myChart
      chartData: [],
    };
  },
  mounted() {
    this.initChart();
    // Add window resize listener
    window.addEventListener('resize', this.handleResize);

    // --- Socket.IO Integration ---
    if (socket) {
      // Subscribe to the new event
      socket.emit('subscribe_box_order_binding_times');

      // Listen for updates
      socket.on('box_order_binding_times_update', (data) => {
        console.log('Received box_order_binding_times_update:', data);
        this.processSocketDataForChart(data); // Process and store the data
        this.updateChart(); // Update the chart with new data
      });
    } else {
      console.error('Socket.IO instance not found. Ensure socket.js is correctly configured.');
    }
  },
  unmounted() {
    // Remove listener on component destruction
    window.removeEventListener('resize', this.handleResize);
    // Disconnect Socket.IO listener if component is unmounted
    if (socket) {
      socket.off('box_order_binding_times_update');
    }
  },
  methods: {
    processSocketDataForChart(socketData) {
      const orderBindingCounts = {};
      socketData.forEach(item => {
        // Parse the ISO 8601 timestamp (e.g., "2025-05-15T23:21:54.000Z")
        const date = new Date(item.timestamp);
        // Group by hour (YYYY-MM-DD HH) for the X-axis
        // Now, format the key to include the full date and hour for accurate grouping and display
        const hourKey = `${date.getFullYear()}/${String(date.getMonth() + 1).padStart(2, '0')}/${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:00`;

        if (!orderBindingCounts[hourKey]) {
          orderBindingCounts[hourKey] = 0;
        }
        orderBindingCounts[hourKey]++;
      });

      const sortedTimes = Object.keys(orderBindingCounts).sort();
      let cumulativeBoundOrderCount = 0;
      this.chartData = sortedTimes.map(time => {
        cumulativeBoundOrderCount += orderBindingCounts[time];
        return {
          event_time: time,
          BoundOrderCount: cumulativeBoundOrderCount,
        };
      });
    },

    initChart() {
      var chartDom = document.getElementById('OrderCountChart');
      this.myChart = echarts.init(chartDom);
      this.updateChart();
    },

    updateChart() {
      if (this.chartData.length === 0) {
        this.myChart.setOption({
          title: { text: "No Data Available" },
          series: [],
          xAxis: { data: [] },
          yAxis: {},
        });
        return;
      }

      const option = {
        title: {
          text: "Package Quantity Trend (Bound Orders)",
          left: "center",
          textStyle: {
            color: "#44652a",
            fontSize: 15
          },
          top: '0%',
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#6a7985",
              fontSize: 10
            },
          },
        },
        legend: {
          data: ["Bound Orders"],
          top: '8%',
          left: 'center',
          textStyle: {
            fontSize: 8
          },
          itemWidth: 12,
          itemHeight: 8
        },
        grid: {
          left: '3%',
          right: '10%',
          bottom: 0,
          top: '25%',
          containLabel: true,
        },
        xAxis: [
          {
            type: "category",
            boundaryGap: false,
            data: this.chartData.map(item => item.event_time),
            axisLabel: {
              // Updated formatter to include the date and time
              formatter: function(value) {
                // value is like "YYYY/MM/DD HH:MM"
                const parts = value.split(' '); // ["YYYY/MM/DD", "HH:MM"]
                const datePart = parts[0].substring(5); // "MM/DD"
                const timePart = parts[1]; // "HH:MM"
                return `${datePart}\n${timePart}`; // Display date on one line, time on another
              },
              interval: 'auto',
              rotate: 0, // Keep rotation at 0 for multi-line labels
              margin: 8,
              hideOverlap: true
            }
          },
        ],
        yAxis: [
          {
            type: "value",
          },
        ],
        series: [
          {
            name: "Bound Orders",
            type: "line",
            color: "#3CB371", // MediumSeaGreen HTML color
            areaStyle: {
              color: "#e0e9d2" // Corresponding rgba for area fill
            },
            emphasis: {
              focus: "series",
            },
            data: this.chartData.map(item => item.BoundOrderCount),
          },
        ],
      };

      this.myChart.setOption(option);
    },

    handleResize() {
      if (this.myChart) {
        this.myChart.resize();
      }
    }
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

#OrderCountChart {
  width: 100%;
  height: 100%;
  flex: 1;
  min-height: 100px;
}
</style>