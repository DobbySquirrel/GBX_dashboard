<template>
  <div class="location-tracker">


    <el-text class="mx-1" style="font-size: 16px; color: #44652a; font-weight: bold;"
        >Location Tracker</el-text
      >
    <div class="tracker-content">
      <div class="device-list">
        <TransitionGroup name="device-list">
          <div 
            v-for="device in filteredDevices" 
            :key="device.id" 
            class="device-card"
            :class="{'recently-updated': device.recentlyUpdated}"
          >
            <div class="device-icon">
              <img :src="getDeviceIcon(device.type)" alt="设备图标">
            </div>
            <div class="device-info">
              <div class="device-name">{{ device.name }}</div>
              <div class="device-status" :class="device.status.toLowerCase()">
                {{ device.status }}
              </div>
              <div class="device-location">
                位置: {{ device.location }}
              </div>
              <div class="device-battery">
                电量: 
                <div class="battery-indicator">
                  <div 
                    class="battery-level" 
                    :style="{ width: device.battery + '%', backgroundColor: getBatteryColor(device.battery) }"
                  ></div>
                  <span class="battery-text">{{ device.battery }}%</span>
                </div>
              </div>
            </div>
          </div>
        </TransitionGroup>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LocationTracker',
  props: {
    droneState: {
      type: String,
      default: null
    },
    indoorCarState: {
      type: String,
      default: null
    },
    outdoorCarState: {
      type: String,
      default: null
    },
    pageType: {
      type: String,
      default: 'all', // 'drone', 'vehicle', 'all'
      validator: (value) => ['drone', 'vehicle', 'all'].includes(value)
    }
  },
  data() {
    return {
      devices: [
        {
          id: 'drone-001',
          name: '配送无人机 #001',
          type: 'drone',
          status: '配送中',
          location: '主楼区域',
          coordinates: [113.47872088332235, 22.892061020308077],
          battery: 78,
          currentOrder: 'ORDER-5',
          lastUpdate: '2分钟前'
        },
        {
          id: 'indoor-car-001',
          name: '室内无人车 #001',
          type: 'indoor-car',
          status: '待命中',
          location: 'E3实验室',
          coordinates: [113.47852336734121, 22.891218918887034],
          battery: 92,
          currentOrder: null,
          lastUpdate: '刚刚'
        },
        {
          id: 'outdoor-car-001',
          name: '室外无人车 #001',
          type: 'outdoor-car',
          status: '充电中',
          location: '停车场',
          coordinates: [113.47852336734121, 22.891218918887034],
          battery: 45,
          currentOrder: null,
          lastUpdate: '5分钟前'
        }
      ],
      deviceIcons: {
        'drone': '/drone-icon.svg',
        'indoor-car': '/indoor-car-icon.svg',
        'outdoor-car': '/outdoor-car-icon.svg',
        'courier': '/courier-icon.svg'
      },
      locations: [
        '主楼区域', 'E3实验室', '充电站', '学生宿舍区', 
        '教学楼', '图书馆', '食堂', '体育馆', '实验室', 
        '行政楼', '停车场', '校门口', '宿舍楼', '休息区'
      ],
      statusOptions: ['配送中', '待命中', '充电中', '维修中', '返程中', '休息中'],
      updateInterval: null,
      locationUpdateInterval: null
    };
  },
  computed: {
    filteredDevices() {
      if (this.pageType === 'all') {
        return this.devices;
      } else if (this.pageType === 'drone') {
        return this.devices.filter(device => device.type === 'drone');
      } else if (this.pageType === 'vehicle') {
        return this.devices.filter(device => 
          device.type === 'indoor-car' || device.type === 'outdoor-car'
        );
      }
      return this.devices;
    }
  },
  methods: {
    selectDevice(deviceId) {
      this.selectedDevice = deviceId === this.selectedDevice ? null : deviceId;
    },
    getDeviceIcon(type) {
      return this.deviceIcons[type] || '/default-icon.svg';
    },
    getDeviceTypeName(type) {
      const typeNames = {
        'drone': '无人机',
        'indoor-car': '室内无人车',
        'outdoor-car': '室外无人车',
        'courier': '配送员'
      };
      return typeNames[type] || '未知设备';
    },
    getBatteryColor(level) {
      if (level > 60) return '#4CAF50';
      if (level > 30) return '#FFC107';
      return '#F44336';
    },
    updateDeviceStatus() {
      if (this.droneState) {
        const droneDevice = this.devices.find(d => d.type === 'drone');
        if (droneDevice) {
          // 更新无人机信息
          // 示例: droneDevice.status = this.parseDroneState(this.droneState);
        }
      }
      
      if (this.indoorCarState) {
        const indoorCarDevice = this.devices.find(d => d.type === 'indoor-car');
        if (indoorCarDevice) {
          // 更新室内车信息
        }
      }
    },
    randomUpdateDeviceStatus() {
      // 随机选择1-2个设备进行更新
      const updateCount = Math.floor(Math.random() * 2) + 1;
      
      for (let i = 0; i < updateCount; i++) {
        const randomIndex = Math.floor(Math.random() * this.devices.length);
        const device = this.devices[randomIndex];
        
        // 添加 recently-updated 标记
        device.recentlyUpdated = true;
        
        if (Math.random() > 0.7) {
          const newStatus = this.statusOptions[Math.floor(Math.random() * this.statusOptions.length)];
          device.status = newStatus;
        }
        
        if (Math.random() > 0.6) {
          const newLocation = this.locations[Math.floor(Math.random() * this.locations.length)];
          device.location = newLocation;
        }
        
        device.lastUpdate = '刚刚';
        
        if (Math.random() > 0.5) {
          const batteryChange = device.status === '充电中' ? 
            Math.floor(Math.random() * 5) : 
            -Math.floor(Math.random() * 3);
          
          device.battery = Math.min(100, Math.max(5, device.battery + batteryChange));
        }
        
        if (Math.random() > 0.8) {
          if (device.currentOrder && Math.random() > 0.5) {
            device.currentOrder = null;
          } else if (!device.currentOrder && device.status === '配送中') {
            device.currentOrder = 'ORDER-' + Math.floor(Math.random() * 10000);
          }
        }
      }
      
      // 创建设备数组的副本以触发视图更新
      this.devices = [...this.devices];
      
      // 2秒后移除 recently-updated 标记
      setTimeout(() => {
        this.devices.forEach(device => {
          if (device.recentlyUpdated) {
            device.recentlyUpdated = false;
          }
        });
        this.devices = [...this.devices];
      }, 2000);
    },
    updateDeviceCoordinates() {
      this.devices.forEach(device => {
        const latOffset = (Math.random() - 0.5) * 0.0002;
        const lngOffset = (Math.random() - 0.5) * 0.0002;
        
        device.coordinates = [
          device.coordinates[0] + lngOffset,
          device.coordinates[1] + latOffset
        ];
      });
      
      this.devices = [...this.devices];
    }
  },
  watch: {
    droneState() {
      this.updateDeviceStatus();
    },
    indoorCarState() {
      this.updateDeviceStatus();
    },
    outdoorCarState() {
      this.updateDeviceStatus();
    }
  },
  mounted() {
    this.updateDeviceStatus();
    
    this.updateInterval = setInterval(() => {
      this.randomUpdateDeviceStatus();
    }, 3000);
    
    this.locationUpdateInterval = setInterval(() => {
      this.updateDeviceCoordinates();
    }, 1500);
  },
  beforeUnmount() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
    }
    if (this.locationUpdateInterval) {
      clearInterval(this.locationUpdateInterval);
    }
  }
};
</script>

<style scoped>
.location-tracker {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(221, 221, 221, 0.4);
  border-radius: 8px;
  overflow: hidden;
  background-color: rgb(255, 255, 255);
  box-sizing: border-box;
  backdrop-filter: blur(2px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding-top: 5px;
}

.tracker-header {
  padding: 5px;
  flex-shrink: 0;
  border-bottom: 1px solid rgba(221, 221, 221, 0.4);
}

.tracker-header h2 {
  margin: 0;
  font-size: 16px;
  text-align: center;
  color: #333;
  font-weight: 600;
}

.tracker-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.device-list {
  width: 95%;
  height: 100%;
  overflow-y: auto;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.device-list::-webkit-scrollbar {
  width: 4px;
}

.device-list::-webkit-scrollbar-track {
  background: rgba(241, 241, 241, 0.85);
  border-radius: 3px;
}

.device-list::-webkit-scrollbar-thumb {
  background: rgba(221, 221, 221, 0.85);
  border-radius: 3px;
}

.device-list::-webkit-scrollbar-thumb:hover {
  background: rgba(204, 204, 204, 0.85);
}

.device-card {
  background-color: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  padding: 10px;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  min-height: 55px;
}

.device-icon {
  width: 30px;
  height: 30px;
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(245, 245, 245, 0.7);
  border-radius: 8px;
}

.device-icon img {
  width: 20px;
  height: 20px;
}

.device-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.device-name {
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 1px;
  color: #333;
}

.device-status {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 10px;
  display: inline-block;
  margin-bottom: 1px;
  width: fit-content;
  min-width: 45px;
  text-align: center;
  font-weight: 500;
}

.device-status.配送中 {
  background-color: rgba(24, 144, 255, 0.1);
  color: #1890ff;
}

.device-status.待命中 {
  background-color: rgba(82, 196, 26, 0.1);
  color: #52c41a;
}

.device-status.充电中 {
  background-color: rgba(250, 173, 20, 0.1);
  color: #faad14;
}

.device-location {
  font-size: 12px;
  color: #666;
}

.device-battery {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #666;
  gap: 6px;
}

.battery-indicator {
  flex: 1;
  height: 10px;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 5px;
  overflow: hidden;
  position: relative;
  max-width: 80px;
}

.battery-level {
  height: 100%;
  transition: width 1s ease, background-color 1s ease;
}

.battery-text {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  color: #333;
  font-weight: 500;
}

.device-list-enter-active {
  transition: all 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28);
}

.device-list-leave-active {
  transition: all 0.5s cubic-bezier(0.6, 0.04, 0.98, 0.34);
}

.device-list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.device-list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.device-list-move {
  transition: transform 0.8s ease;
}

@keyframes pulse-update {
  0% {
    box-shadow: 0 0 0 3px  rgba(82, 196, 26, 0.2);
  }
  70% {
    box-shadow: 0 0 0 3px  rgba(82, 196, 26, 0.2);
  }
  100% {
    box-shadow: 0 0 0 3px  rgba(82, 196, 26, 0.2);
  }
}

.device-card.recently-updated {
  animation: pulse-update 2s ease-out;
}

.device-status.维修中 {
  background-color: rgba(245, 34, 45, 0.1);
  color: #f5222d;
}

.device-status.返程中 {
  background-color: rgba(114, 46, 209, 0.1);
  color: #722ed1;
}

.device-status.休息中 {
  background-color: rgba(144, 144, 144, 0.1);
  color: #909090;
}

.value.维修中 {
  color: #f5222d;
}

.value.返程中 {
  color: #722ed1;
}

.value.休息中 {
  color: #909090;
}

@media screen and (max-width: 768px) {
  .tracker-content {
    flex-direction: column;
  }
  
  .device-list {
    width: 100%;
    max-height: 40%;
    border-right: none;
    border-bottom: 1px solid rgba(221, 221, 221, 0.4);
  }
  
  .device-details {
    padding: 10px;
  }
  
  .label {
    width: 70px;
    font-size: 12px;
  }
  
  .value {
    font-size: 12px;
  }
}

@media screen and (width: 1680px) and (height: 3200px) {
  .tracker-header h2 {
    font-size: 24px;
  }
  
  .device-name {
    font-size: 18px;
  }

  .device-status {
    font-size: 14px;
    padding: 3px 8px;
    min-width: 50px;
  }
  
  .device-location {
    font-size: 16px;
  }
  
  .details-header h3 {
    font-size: 22px;
  }
  
  .label, .battery-label {
    width: 90px;
  }
  
  .value {
    max-width: 180px;
  }
  
  .device-icon {
    width: 40px;
    height: 40px;
  }
  
  .device-icon img {
    width: 32px;
    height: 32px;
  }
  
  .battery-indicator {
    max-width: 150px;
    height: 20px;
  }
  
  .battery-text {
    font-size: 14px;
  }
}
</style> 