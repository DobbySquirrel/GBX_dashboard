<template>
  <div class="table-display">
    <el-table
      :data="sortedCards"
      style="width: 100%; border-radius: 5px"
      :max-height="tableHeight"
      :row-class-name="tableRowClassName"
    >
      <el-table-column prop="event_time" label="Time" sortable />
      <el-table-column prop="RFID" label="RFID" />
      <el-table-column prop="Status" label="Status" />
      <el-table-column prop="owner" label="Owner" />
    </el-table>
  </div>
</template>

<script>
export default {
  name: "OrderCards",
  props: {
    Box_owner: {
      type: [String, null],
      required: true,
    },
  },
  data() {
    return {
      cards: [],
      StatusMap: {
        'UserInfo': 'Out of Warehouse',
        'DroneDeliveryOrder': 'Drone Delivery',
        'InputDelivery': 'Locker Deposit',
        'OutputDelivery': 'Locker Pickup',
        'RecycleDelivery': 'Locker Recycling'
      },
      tableHeight: '30vh'
    };
  },
  computed: {
    sortedCards() {
      return [...this.cards].sort((a, b) => {
        const timeA = new Date(a.event_time);
        const timeB = new Date(b.event_time);
        return timeB - timeA; // 降序排列，最新的在前
      });
    },
    latestBoxStatus() {
      const latestCard = this.sortedCards[0];
      return latestCard ? latestCard.Status : 'N/A';
    }
  },
  watch: {
    Box_owner: {
      handler(newVal) {
        if (newVal) {
          this.cards = this.parseCsvData(newVal);
        }
      },
      immediate: true
    }
  },
  methods: {
    tableRowClassName({ row, rowIndex }) {
      return '';
    },

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
          parseInt(month) - 1, // 月份从0开始
          parseInt(day),
          parseInt(hour),
          parseInt(minute),
          parseInt(second)
        ));

        // 转换为中国时区（UTC+8）
        const chinaTime = new Date(utcDate.getTime());

        // 格式化输出
        return `${chinaTime.getFullYear()}/${String(chinaTime.getMonth() + 1).padStart(2, '0')}/${String(chinaTime.getDate()).padStart(2, '0')} ${String(chinaTime.getHours()).padStart(2, '0')}:${String(chinaTime.getMinutes()).padStart(2, '0')}`;
      } catch (error) {
        console.error('Error formatting time:', error);
        return timeString;
      }
    },

    parseCsvData(csvData) {
      if (!csvData) return [];
      
      try {
        const lines = csvData.trim().split("\n");
        // console.log(lines);
        const dataRows = lines.slice(1).reverse(); // 反转数据行
        const lastRows = dataRows.slice(0, 7); // 取前5行
        
        return lastRows.map(line => {
          const values = line.split(",");
          const status = values[3]?.trim() || 'N/A';
          return {
            event_time: this.formatTime(values[0]?.trim() || 'N/A'),
            RFID: values[5]?.trim() || 'N/A',
            owner: values[4]?.trim() || 'N/A',
            Status: this.StatusMap[status] || status // 使用映射表转换状态
          };
        });
      } catch (error) {
        console.error('Error parsing CSV data:', error);
        return [];
      }
    }
  }
};
</script>

<style>
.table-display {
  margin: 0px;
  height: 30vh;
  min-height: 300px;
}

.el-table {
  --el-table-header-bg-color: #fefffe;
  --el-table-row-hover-bg-color: #f5faf7;
  font-size: 10px;
}

.el-table th {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
  font-size: 10px;
}

.el-table td {
  color: #606661;
  font-size: 10px;
}

</style>

