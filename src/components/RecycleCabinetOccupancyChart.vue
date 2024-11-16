<template>
  <div class="chart-container">
    <div ref="chart" id="RecycleCabinetOccupancyLine"></div>
    <p v-if="chartData.length === 0">加载中...</p>
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
      localDelivery_Locker_Property_OutputDelivery: this.Delivery_Locker_Property_OutputDelivery,
      chartData: [],
      myChart: null,
    };
  },
  watch: {
    Delivery_Locker_Property_OutputDelivery(newVal) {
      this.localDelivery_Locker_Property_OutputDelivery = newVal;
      if (newVal) {
        this.parseCsvData(newVal);
      }
    },
  },
  methods: {
    formatTime(timeString) {
      try {
        // 解析时间字符串，例如："20241107T092711Z"
        const year = timeString.substring(0, 4);
        const month = timeString.substring(4, 6);
        const day = timeString.substring(6, 8);
        const hour = timeString.substring(9, 11);
        const minute = timeString.substring(11, 13);
        const second = timeString.substring(13, 15);

        // 创建 UTC 时间
        const utcDate = new Date(Date.UTC(
          parseInt(year),
          parseInt(month) - 1,
          parseInt(day),
          parseInt(hour),
          parseInt(minute),
          parseInt(second)
        ));

        // 转换为中国时区时间并格式化
        return `${utcDate.getFullYear()}/${String(utcDate.getMonth() + 1).padStart(2, '0')}/${String(utcDate.getDate()).padStart(2, '0')} ${String(utcDate.getHours()).padStart(2, '0')}:${String(utcDate.getMinutes()).padStart(2, '0')}`;
      } catch (error) {
        console.error('Error formatting time:', error);
        return timeString;
      }
    },

    parseCsvData(csvData) {
      try {
        const lines = csvData.trim().split('\n');
        if (lines.length <= 1) {
          console.error('No data in CSV');
          return;
        }

        const headers = lines[0].split(',').map(h => h.trim());
        const eventTimeIndex = headers.indexOf('event_time');
        const occupyRatioIndex = headers.indexOf('OccupyRatio');

        if (eventTimeIndex === -1 || occupyRatioIndex === -1) {
          console.error('Required columns not found:', headers);
          return;
        }

        const result = [];
        
        // 解析每一行数据
        for (let i = 1; i < lines.length; i++) {
          const values = lines[i].split(',').map(v => v.trim());
          if (values.length >= Math.max(eventTimeIndex, occupyRatioIndex) + 1) {
            const timeValue = values[eventTimeIndex];
            const ratioValue = values[occupyRatioIndex];
            
            if (timeValue && !isNaN(parseFloat(ratioValue))) {
              result.push({
                event_time: this.formatTime(timeValue),
                occupyRatio: parseFloat(ratioValue)
              });
            }
          }
        }

        // console.log('Parsed data:', result); // 添加调试日志

        // 按时间排序
        result.sort((a, b) => new Date(a.event_time) - new Date(b.event_time));
        
        this.chartData = result;
        this.updateChart();
      } catch (error) {
        console.error('Error parsing CSV data:', error);
      }
    },

    initChart() {
      const chartDom = this.$refs.chart;
      if (!chartDom) return;
      this.myChart = echarts.init(chartDom);
      this.updateChart();
    },

    updateChart() {
      if (!this.myChart || !this.chartData.length) {
        // console.log('No chart instance or no data'); // 添加调试日志
        return;
      }

      const option = {
        title: {
          text: 'Recycling Cabinet',
          left: "center",
          textStyle: {
            color: "#44652a",
          },
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985',
            },
          },
        },
        legend: {
          data: ["occupyRatio"],
          orient: 'vertical',
          left: 'top',
          top: '10%',
          left: '10%'
        },
        grid: {
          left: '3%',
          right: '10%',
          bottom: '5%',
          containLabel: true,
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: this.chartData.map(item => item.event_time),
          axisLabel: {
            formatter: function(value) {
              return value.split(' ')[1];
            },
            interval: 'auto',
            rotate: 0,
            margin: 8,
            hideOverlap: true
          }
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: "occupyRatio",
            data: this.chartData.map(item => ({
              value: item.occupyRatio,
              time: item.event_time
            })),
            type: 'line',
            smooth: true,
            lineStyle: {
              color: '#91CC75',
            },
            itemStyle: {
              color: '#91CC75',
            },
            label: {
              show: true,
              position: 'top',
              formatter: '{c}',
              color: "#44652a",
            },
          },
        ],
      };

      // console.log('Chart option:', option); // 添加调试日志
      this.myChart.setOption(option);
    },

    handleResize() {
      if (this.myChart) {
        this.myChart.resize();
      }
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      if (this.Delivery_Locker_Property_OutputDelivery) {
        // console.log('Initial data:', this.Delivery_Locker_Property_OutputDelivery); // 添加调试日志
        this.parseCsvData(this.Delivery_Locker_Property_OutputDelivery);
      }
      window.addEventListener('resize', this.handleResize);
    });
  },
  unmounted() {
    window.removeEventListener('resize', this.handleResize);
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
  height: 25vh;
  position: relative;
}

#RecycleCabinetOccupancyLine {
  width: 100%;
  height: 100%;
  min-height: 150px;
}
</style>
