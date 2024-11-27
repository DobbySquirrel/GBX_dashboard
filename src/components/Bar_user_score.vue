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
    Box_owner: {
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
      this.renderBarChart(parsedData);
    },

    parseCsvData(csvData) {
      if (!csvData) return [];
      
      // 添加时间格式化函数
      const formatTime = (timeString) => {
        try {
          // 解析时间字符串，例如："20241107T092711Z"
          const year = timeString.substring(0, 4);
          const month = timeString.substring(4, 6);
          const day = timeString.substring(6, 8);
          const hour = timeString.substring(9, 11);
          const minute = timeString.substring(11, 13);
          const second = timeString.substring(13, 15);

          // 创建 UTC 时间
          return new Date(Date.UTC(
            parseInt(year),
            parseInt(month) - 1,
            parseInt(day),
            parseInt(hour),
            parseInt(minute),
            parseInt(second)
          ));
        } catch (error) {
          console.error('Error formatting time:', error);
          return new Date(timeString);
        }
      };

      const lines = csvData.trim().split("\n");
      const data = lines.slice(1).map(line => {
        const values = line.split(",");
        return {
          eventTime: formatTime(values[0]?.trim()),    // 使用新的时间格式化方法
          Owner: values[4]?.trim() || 'N/A',
          status: values[3]?.trim() || 'N/A',
          RFID: values[5]?.trim() || 'N/A'
        };
      });
// 按时间顺序对所有记录进行排序
data.sort((a, b) => a.eventTime - b.eventTime);

// 初始化用户分数对象
const scores = {};
// 遍历所有记录，找出参与取箱或还箱的用户，初始化他们的分数为0
data.forEach(record => {
    if ((record.status === 'OutputDelivery' || record.status === 'RecycleInDelivery') 
        && record.Owner !== 'N/A' 
        && !scores.hasOwnProperty(record.Owner)) {
        scores[record.Owner] = 0;
    }
});

// 创建一个对象来存储每个箱子的使用记录
const boxCycles = {};
// 按箱子ID分组所有记录
data.forEach(record => {
    if (!boxCycles[record.RFID]) {
        boxCycles[record.RFID] = [];
    }
    boxCycles[record.RFID].push(record);
});

// 处理每个箱子的使用记录来计算用户分数
Object.values(boxCycles).forEach(boxRecords => {
    // currentCycle用于存储当前箱子的一个完整使用周期（从取出到归还）
    let currentCycle = [];
    
    boxRecords.forEach(record => {
        currentCycle.push(record);
        
        // 当遇到还箱记录时，说明一个使用周期结束
        if (record.status === 'RecycleInDelivery') {
            // 在当前周期中查找取箱记录和还箱记录
            const outputRecord = currentCycle.find(r => r.status === 'OutputDelivery');
            const recycleRecord = currentCycle.find(r => r.status === 'RecycleInDelivery');

            if (outputRecord && recycleRecord) {
                // 确保还箱时间晚于取箱时间
                if (recycleRecord.eventTime >= outputRecord.eventTime) {
                    // 判断取箱和还箱是否为同一用户
                    if (outputRecord.Owner === recycleRecord.Owner) {
                        // 同一用户取还箱，奖励10分
                        scores[recycleRecord.Owner] += 10;
                    } else {
                        // 不同用户：
                        scores[recycleRecord.Owner] += 10;    // 还箱者奖励10分
                        scores[outputRecord.Owner] -= 50;     // 取箱者扣50分
                    }
                } else {
                    console.warn('检测到异常：还箱时间早于取箱时间', {
                        boxId: recycleRecord.RFID,
                        outputTime: outputRecord.eventTime,
                        recycleTime: recycleRecord.eventTime
                    });
                }
            }
            
            // 重置周期记录，准备记录下一个周期
            currentCycle = [];
        }
    });
});

      return Object.entries(scores).map(([Owner, score]) => ({
        Owner,
        score
      }));
    },

    handleResize() {
      if (this.myChart) {
        this.myChart.resize();
      }
    },

    renderBarChart(data) {
      // 按分数排序
      data.sort((a, b) => b.score - a.score);

      var chartDom = document.getElementById("UserScoreBarChart");
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
          data: data.map(item => item.Owner),
          axisLabel: {
            color: "#44652a",
            interval: 0,
            rotate: 30,
            fontSize: 9
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