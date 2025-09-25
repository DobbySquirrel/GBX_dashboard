<template>
  <div class="table-display">
    <el-table
      :data="sortedCards"
      style="width: 100%; border-radius: 5px"
      :max-height="tableHeight"
      :row-class-name="tableRowClassName"
    >
      <el-table-column prop="event_time" label="Time" sortable />
      <el-table-column prop="RFID" label="Box ID" />
      <el-table-column prop="service_id" label="Service ID"  width="160" />
      <el-table-column prop="owner" label="Owner" />
    </el-table>
  </div>
</template>

<script>
import socket from "../api/socket.js";

export default {
  name: "OrderCards",
  props: {
    pageType: {
      type: String,
      default: '', // Set a default empty string or 'N/A'
    }
  },
  data() {
    return {
      cards: [],
      tableHeight: '30vh',
      latestCardRFID: null,
      animationTimeout: null,
    };
  },
  computed: {
    filteredCards() {
      let filtered = this.cards;
      if (this.pageType === 'drone') {
        filtered = filtered.filter(card => card.product_id === '66dabbab1837002b28b35a64');
      } else if (this.pageType === 'vehicle') {
        filtered = filtered.filter(card => card.product_id === '66dabbc81837002b28b35a69');
      }
      return filtered;
    },
    sortedCards() {
      return [...this.filteredCards].sort((a, b) => {
        return b.event_time.localeCompare(a.event_time);
      });
    },
    latestBoxservice_id() {
      const latestCard = this.sortedCards[0];
      return latestCard ? latestCard.service_id : 'N/A';
    }
  },
  methods: {
  tableRowClassName({ row, rowIndex }) {
  let classNames = '';
  // 只看行索引，第一行就是最新的
  if (rowIndex === 0) {
    classNames += ' latest-row';
  } 
  if (row.RFID === this.latestCardRFID) {
    classNames += ' new-row-animation';
  }
  return classNames.trim();
},
    formatTime(timeString) {
      if (!timeString || timeString === 'N/A') return 'N/A';
      try {
        const year = timeString.substring(0, 4);
        const month = timeString.substring(4, 6);
        const day = timeString.substring(6, 8);
        const hour = timeString.substring(9, 11);
        const minute = timeString.substring(11, 13);
        const second = timeString.substring(13, 15);

        const isoString = `${year}-${month}-${day}T${hour}:${minute}:${second}Z`;
        const utcDate = new Date(isoString);

        if (isNaN(utcDate.getTime())) {
          throw new Error('Invalid date format');
        }

        return utcDate.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: false,
          timeZone: 'Asia/Shanghai'
        }).replace(',', '');
      } catch (error) {
        console.error('Error formatting time:', error);
        return timeString;
      }
    },

handleBoxOwnerUpdate(data) {
      if (data && Array.isArray(data)) {
        // Store the RFID of the current first card before updating `cards`
        const oldFirstCardRFID = this.sortedCards.length > 0 ? this.sortedCards[0].RFID : null;

        this.cards = data.map(item => {
          let displayOwner = item.owner || 'N/A';
          
          // 如果是drone数据，转换Owner显示名称
          if (item.product_id === '66dabbab1837002b28b35a64') {
            switch (item.owner) {
              case 'Station_1':
                displayOwner = '停机坪_1';
                break;
              case 'Drone_1':
                displayOwner = '无人机';
                break;
              case 'station_2':
                displayOwner = '停机坪_2';
                break;
              case 'recycle bin':
                displayOwner = '回收柜';
                break;
              default:
                displayOwner = item.owner || 'N/A';
            }
          }

          return {
            event_time: this.formatTime(item.event_time || 'N/A'),
            RFID: item.RFID || 'N/A',
            owner: displayOwner,
            service_id: item.service_id || 'N/A',
            product_id: item.product_id || 'N/A'
          };
        });

        // After updating cards, check if the first card in the *sorted and filtered* list has changed
        if (this.sortedCards.length > 0 && this.sortedCards[0].RFID !== oldFirstCardRFID) {
          if (this.animationTimeout) {
            clearTimeout(this.animationTimeout);
          }

          this.latestCardRFID = this.sortedCards[0].RFID;

          this.animationTimeout = setTimeout(() => {
            this.latestCardRFID = null;
          }, 600);
        }

        console.log('更新箱子数据:', this.cards);
      }
    }
  },
  mounted() {
    if (!socket.connected) {
      socket.connect();
    }
    socket.on('box_owner_update', this.handleBoxOwnerUpdate);
    socket.emit('subscribe_box_owner');
  },
  beforeUnmount() {
    socket.off('box_owner_update', this.handleBoxOwnerUpdate);
    if (this.animationTimeout) {
      clearTimeout(this.animationTimeout);
    }
  }
};
</script>

<style>
.table-display {
  margin: 0px;
  height: 30vh;
  width: 100%;
}

.el-table {
  --el-table-header-bg-color: #fefffe;
  --el-table-row-hover-bg-color: #f5faf7;
  font-size: 15px;
  width: 100% !important;
}

.el-table th {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
  font-size: 15px !important;
}

.el-table td {
  color: #606661;
  font-size: 13px !important;
}

.el-table__row {
  width: 100%;
}

.el-table-column {
  width: auto !important;
}

/* Add latest row highlight */
.latest-row {
  background-color: #f0f9eb !important;
}

@keyframes slide-fade-in {
  from {
    opacity: 0;
    transform: translateY(-25px); /* Increased slide distance */
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.new-row-animation {
  animation: slide-fade-in 0.8s ease-out forwards; /* Longer duration */
}
</style>