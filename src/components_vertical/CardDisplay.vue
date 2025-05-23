<template>
  <div class="table-display">
    <el-table
      :data="sortedCards"
      style="width: 100%; border-radius: 5px"
      :max-height="tableHeight"
      :row-class-name="tableRowClassName"
    >
      <el-table-column prop="log_time" label="Log Time" sortable />
      <el-table-column prop="box_id" label="Box ID" />
      <el-table-column prop="status" label="Status" />
      <el-table-column prop="location" label="Location" />
      </el-table>
  </div>
</template>

<script>
import socket from "../api/socket.js"; // Assuming you have a socket.js setup for client

export default {
  name: "OrderCards",
  data() {
    return {
      cards: [],
      tableHeight: '30vh' // Keep this if you want a fixed height for the table
    };
  },
  computed: {
    sortedCards() {
      // Create a shallow copy and sort in descending order by log_time (newest on top)
      return [...this.cards].sort((a, b) => {
        // Assuming log_time is already a formatted time string
        return b.log_time.localeCompare(a.log_time);
      });
    },
    // You might want to adjust this to show the latest box status or ID
    latestBoxStatus() {
      const latestCard = this.sortedCards[0];
      return latestCard ? latestCard.status : 'N/A';
    }
  },
  methods: {
    tableRowClassName({ row, rowIndex }) {
      // Can add highlight style for the latest row
      if (rowIndex === 0) {
        return 'latest-row';
      }
      return '';
    },

    /**
     * Handles incoming box_status_logs_update from the WebSocket.
     * @param {Array<Object>} data - Array of box status log objects from the server.
     */
    handleBoxStatusLogsUpdate(data) {
      if (data && Array.isArray(data)) {
        // Map the raw data to the format expected by the table
        this.cards = data.map(item => ({
          log_time: item.timestamp || 'N/A', 
          box_id: item.box_id || 'N/A',
          status: item.status || 'N/A',
          location: item.owner_id || 'N/A',
          // Add other relevant fields from box_status_logs
        }));
        // console.log('更新箱子状态日志数据:', this.cards);
      }
    }
  },
  mounted() {
    // Ensure socket is connected
    if (!socket.connected) {
      socket.connect();
    }

    // Subscribe to box_status_logs_update events
    socket.on('box_status_logs_update', this.handleBoxStatusLogsUpdate);
    // Emit a subscription request to the server to get initial data and continuous updates
    socket.emit('subscribe_box_status_logs');
  },
  beforeUnmount() {
    // Unsubscribe from the socket event to prevent memory leaks
    socket.off('box_status_logs_update', this.handleBoxStatusLogsUpdate);
  }
};
</script>

<style>
.table-display {
  margin: 0px;
  height: 30vh;
  width: 100%; /* Ensure table container takes full width */
}

.el-table {
  --el-table-header-bg-color: #fefffe;
  --el-table-row-hover-bg-color: #f5faf7;
  font-size: 10px;
  width: 100% !important; /* Force table width to 100% */
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

/* Ensure table rows take full width */
.el-table__row {
  width: 100%;
}

/* Ensure table cells are reasonably distributed */
.el-table-column {
  width: auto !important;
}

/* Add highlight style for the latest row */
.latest-row {
  background-color: #f0f9eb !important;
}
</style>