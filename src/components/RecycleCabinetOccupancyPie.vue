<template>
  <div>
    <div id="LockerStatusPieChart"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";

export default {
  name: "LockerStatusPieChart",
  props: {
    Delivery_Locker_Property_InputDelivery: {
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
    Delivery_Locker_Property_InputDelivery(newData) {
      if (newData) {
        this.parseCsvData(newData);
      }
    },
  },
  mounted() {
    if (this.Delivery_Locker_Property_InputDelivery) {
      this.parseCsvData(this.Delivery_Locker_Property_InputDelivery);
    }
  },
  methods: {
    parseCsvData(csvData) {
      const data = this.Rows(csvData);
      // Store parsed data for chart rendering
      this.chartData = data;

      // Extract status counts
      const lockedCells = new Set();
      const unlockedCells = new Set();

      data.forEach((row) => {
        if (row.CellStatus === "Locked") {
          lockedCells.add(row.CellNumer);
        } else if (row.CellStatus === "Unlocked") {
          unlockedCells.add(row.CellNumer);
        }
      });

      // Calculate difference
      const difference = new Set(
        [...lockedCells].filter((cell) => !unlockedCells.has(cell))
      );
      const lockedCount = difference.size;
      const unlockedCount = unlockedCells.size;
      const totalCells = 10;
      const unactivatedCount = totalCells - lockedCount - unlockedCount;

      // Map data to chart
      this.renderLockerStatusPieChart([
        { value: unlockedCount, name: "Unlocked",itemStyle: {color: "rgba(145, 204, 117, 0.5)"}},
        { value: lockedCount, name: "Locked" ,itemStyle: {color: "rgba(250, 200, 88, 0.5)"}},
        { value: unactivatedCount, name: "Unactivated",itemStyle: {color: "rgba(128, 128, 128, 0.5)"} },
      ]);
    },

    Rows(csvData) {
      const lines = csvData.trim().split("\n");
      const headers = lines[0].split(","); // Assuming CSV data has headers
      return lines.slice(1).map((line) => {
        const values = line.split(",");
        return headers.reduce((obj, header, index) => {
          obj[header.trim()] = values[index].trim();
          return obj;
        }, {});
      });
    },

    renderLockerStatusPieChart(data) {
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
        legend: {
          orient: "vertical",
          left: "left",
          top: "5%", // Keep the legend at the top
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
        show: true, // Enable label display
        position: 'top', // Show label above the point
        formatter: '{b} Locker {c}', // Use {c} to show the value of the data point
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
    },
  },
};
</script>

<style scoped>
#LockerStatusPieChart {
  width: 100%;
  height: 250px;
}
</style>