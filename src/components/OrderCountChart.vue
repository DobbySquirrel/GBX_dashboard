<template>
  <div id="OrderCountChart"></div>
</template>

<script>
import * as echarts from "echarts";

  // <!-- 左上二: 订单数量趋势 -->

export default {
  name: "Order Quantity Trend",
    props: {
    DeliveryDrone_Property_DroneDeliveryOrder: {
      type: [String, null],
      required: true
    },
    IndoorDeliveryCar_Property_IndoorDeliveryOrder: {
      type: [String, null],
      required: true
    },
    OutdoorDeliveryCar_Property_OutdoorDeliveryOrder: {
      type: [String, null],
      required: true
    }
  },
  data(){
return{
    localDeliveryDrone_Property_DroneDeliveryOrder: this.DeliveryDrone_Property_DroneDeliveryOrder,
    localIndoorDeliveryCar_Property_IndoorDeliveryOrder: this.IndoorDeliveryCar_Property_IndoorDeliveryOrder,
    localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder: this.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder,
    unifiedData: []
}

  },
  watch:{

   DeliveryDrone_Property_DroneDeliveryOrder(newVal) {
    this.localDeliveryDrone_Property_DroneDeliveryOrder = newVal;
    this.onDataUpdate();
  },
  IndoorDeliveryCar_Property_IndoorDeliveryOrder(newVal) {
    this.localIndoorDeliveryCar_Property_IndoorDeliveryOrder = newVal;
    this.onDataUpdate();
  },
  OutdoorDeliveryCar_Property_OutdoorDeliveryOrder(newVal) {
    this.localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder = newVal;
    this.onDataUpdate();
  },

  },
  mounted() {
     this.initChart(); 
    if (this.DeliveryDrone_Property_DroneDeliveryOrder && this.IndoorDeliveryCar_Property_IndoorDeliveryOrder && this.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder) {
      this.unifiedData = this.parseCsvData(
        this.DeliveryDrone_Property_DroneDeliveryOrder,
        this.IndoorDeliveryCar_Property_IndoorDeliveryOrder,
        this.OutdoorDeliveryCar_Property_OutdoorDeliveryOrder,
      );
      this.updateChart();
    }
},
  methods:{
        onDataUpdate() {
    // 检查所有本地属性是否都有最新数据
    if (
      this.localDeliveryDrone_Property_DroneDeliveryOrder &&
      this.localIndoorDeliveryCar_Property_IndoorDeliveryOrder &&
      this.localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder
    ) {
      // 使用本地数据进行解析和图表更新
      this.unifiedData = this.parseCsvData(
        this.localDeliveryDrone_Property_DroneDeliveryOrder,
        this.localIndoorDeliveryCar_Property_IndoorDeliveryOrder,
        this.localOutdoorDeliveryCar_Property_OutdoorDeliveryOrder
      );
      this.updateChart();
    }
  },
parseCsvData(DeliveryDrone_Property_DroneDeliveryOrder, IndoorDeliveryCar_Property_IndoorDeliveryOrder, OutdoorDeliveryCar_Property_OutdoorDeliveryOrder) {
  const countOrderNumbersByTime = (csvData, timeField, orderField) => {
    const lines = csvData.trim().split('\n');
    const headers = lines[0].split(',');
    const data = lines.slice(1).map(line => {
      const values = line.split(',');
      return headers.reduce((obj, header, index) => {
        obj[header.trim()] = values[index].trim();
        return obj;
      }, {});
    });

    // Aggregate OrderNumbers by event_time
    const orderCountByTime = {};
    data.forEach(row => {
      const eventTime = row[timeField];
      if (!orderCountByTime[eventTime]) {
        orderCountByTime[eventTime] = 0;
      }
      orderCountByTime[eventTime] += 1;
    });

    // Accumulate counts over time
    const sortedTimes = Object.keys(orderCountByTime).sort();
    let cumulativeCount = 0;
    const result = {};
    sortedTimes.forEach(time => {
      cumulativeCount += orderCountByTime[time];
      result[time] = cumulativeCount;
    });
    return result;
  };

  // Calculate counts for each CSV
  const droneOrderCounts = countOrderNumbersByTime(DeliveryDrone_Property_DroneDeliveryOrder, 'event_time', 'OrderNumber');
  const indoorOrderCounts = countOrderNumbersByTime(IndoorDeliveryCar_Property_IndoorDeliveryOrder, 'event_time', 'Number');
  const outdoorOrderCounts = countOrderNumbersByTime(OutdoorDeliveryCar_Property_OutdoorDeliveryOrder, 'event_time', 'Number');

  // Aggregate data into unified timestamps
  const allEventTimes = new Set([...Object.keys(droneOrderCounts), ...Object.keys(indoorOrderCounts), ...Object.keys(outdoorOrderCounts)]);
  const unifiedData = Array.from(allEventTimes).sort().map(time => {
    return {
      event_time: time,
      DroneOrderCount: droneOrderCounts[time] || 0,
      IndoorDeliveryCarOrderCount: indoorOrderCounts[time] || 0,
      OutdoorDeliveryCarOrderCount: outdoorOrderCounts[time] || 0
    };
  });

  // Fill in missing data by carrying forward the last known count
  for (let i = 1; i < unifiedData.length; i++) {
    unifiedData[i].DroneOrderCount = unifiedData[i].DroneOrderCount || unifiedData[i - 1].DroneOrderCount;
    unifiedData[i].IndoorDeliveryCarOrderCount = unifiedData[i].IndoorDeliveryCarOrderCount || unifiedData[i - 1].IndoorDeliveryCarOrderCount;
    unifiedData[i].OutdoorDeliveryCarOrderCount = unifiedData[i].OutdoorDeliveryCarOrderCount || unifiedData[i - 1].OutdoorDeliveryCarOrderCount;
  }

  return unifiedData;
},

initChart() {
  var chartDom = document.getElementById('OrderCountChart');
  this.myChart = echarts.init(chartDom);
  this.updateChart();
},

updateChart() {
  const option = {
    title: {
      text: "Package Quantity Trend",
      left: "center",
      textStyle: {
      color: "#44652a",
    },
    top: '0%',
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
        label: {
          backgroundColor: "#6a7985",
        },
      },
    },
    legend: {
      data: ["Drone Orders", "Indoor Delivery Car Orders", "Outdoor Delivery Car Orders"],
      top: '10%',
      left: 'center',
      left: '2%',
    },
    grid: {
      left: '0%', // 向左对齐
      bottom: '0%',
      right:'0%',
      top: '18%',
      containLabel: true,
    },
    xAxis: [
      {
        type: "category",
        boundaryGap: false,
        data: this.unifiedData.map(item => item.event_time),
      },
    ],
    yAxis: [
      {
        type: "value",
      },
    ],
    series: [
      {
        name: "Drone Orders",
        type: "line",
        stack: "Total",
        areaStyle: {color:"rgba(250, 200, 88, 0.5)"},
        color:"#fac858",
        emphasis: {
          focus: "series",
        },
        data: this.unifiedData.map(item => item.DroneOrderCount),
      },
      {
        name: "Indoor Delivery Car Orders",
        type: "line",
        stack: "Total",
        areaStyle: {color:"rgba(115, 192, 222, 0.5)"}, 
        
        color:"#73c0de",
        emphasis: {
          focus: "series",
        },
        data: this.unifiedData.map(item => item.IndoorDeliveryCarOrderCount),
      },
      {
        name: "Outdoor Delivery Car Orders",
        type: "line",
        stack: "Total",
        color:"#91CC75",
        areaStyle: {color:"rgba(145, 204, 117, 0.5)"},
        emphasis: {
          focus: "series",
        },
        data: this.unifiedData.map(item => item.OutdoorDeliveryCarOrderCount),
      },
    ],
  };

  this.myChart.setOption(option);
}

    }


};
</script>

<style scoped>
#OrderCountChart {
  width: 90%;
  height: 225px; 
}
</style>