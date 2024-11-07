<template>
  <div>
    <div v-if="chartData.length > 0">
      <!-- ECharts line chart -->
      <div ref="chart" id="RecycleCabinetOccupancyLine"></div>
    </div>
    <div v-else>
      <p>加载中...</p>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  props: {
    Delivery_Locker_Property_OutputDelivery: {
      type: [String, null],
      default: null,
    },
  },
  data() {
    return {
      chartData: [], // Parsed chart data
    };
  },
  watch: {
    // Watch the prop for changes and update the chart when the data is received
    Delivery_Locker_Property_OutputDelivery(newData) {
      if (newData) {
        this.parseCsvData(newData);
      }
    },
  },
  methods: {
    // Method to parse CSV data
    parseCsvData(csvData) {
      const lines = csvData.trim().split('\n');
      const result = [];

      // Extract headers
      const headers = lines[0].split(',');

      // Find index of event_time and OccupyRatio columns
      const eventTimeIndex = headers.indexOf('event_time');
      const occupyRatioIndex = headers.indexOf('OccupyRatio');

      // Parse each line of CSV and extract relevant data
      lines.slice(1).forEach((line) => {
        const values = line.split(',');
        result.push({
          event_time: values[eventTimeIndex],
          occupyRatio: parseFloat(values[occupyRatioIndex]),
        });
      });

      // Sort the data by event_time (optional)
      result.sort((a, b) => new Date(a.event_time) - new Date(b.event_time));

      // Store parsed data for chart rendering
      this.chartData = result;

      // Call method to render the chart
      this.renderChart();
    },

    // Method to render the ECharts line chart
    renderChart() {
      this.$nextTick(() => {
        const chartDom = this.$refs.chart;
        if (!chartDom) return;

        const chartInstance = echarts.init(chartDom);

 const option = {
  title: {
    text: 'Recycling Cabinet',
      left: "center",
      textStyle: {
      color: "#44652a",
    },
    top: '0%',
  },
  legend: {
    data: ["occupyRatio"],
    orient: 'vertical',
    left: 'top',
    top: '10%',
  },
  xAxis: {
    type: 'category',
    data: this.chartData.map(item => item.event_time), // Use event_time as x-axis data
  },
  yAxis: {
    type: 'value',
  },
      grid: {
      containLabel: true,
      left: '0%', // 向左对齐
      bottom: '0%',
      top: '18%',
    },
  series: [
    {
      name: "occupyRatio",
      data: this.chartData.map(item => item.occupyRatio), // Use OccupyRatio as y-axis data
      type: 'line',
      smooth: true,
      lineStyle: {
        color: '#91CC75', // Set line color to green
      },
      itemStyle: {
        color: '#91CC75', // Set point (symbol) color to green
      },
      label: {
        show: true, // Enable label display
        position: 'top', // Show label above the point
        formatter: '{c}', // Use {c} to show the value of the data point
        color: "#44652a",

      },
    },
  ],
};


        chartInstance.setOption(option);
      });
    },
  },
  mounted() {
    if (this.Delivery_Locker_Property_OutputDelivery) {
      this.parseCsvData(this.Delivery_Locker_Property_OutputDelivery);
    }
  },
};
</script>

<style scoped>
/* Chart container styling */
#RecycleCabinetOccupancyLine {
  width: 100%;
  height: 225px;
}
</style>
