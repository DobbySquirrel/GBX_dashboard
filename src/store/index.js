import { defineStore } from 'pinia';

export const useDataStore = defineStore('data', {
  state: () => ({
    loading: false,
    error: null,
    data: {
      droneState: null,
      droneDeliveryOrder: null,
      indoorCarState: null,
      indoorDeliveryOrder: null,
      outdoorCarState: null,
      outdoorDeliveryOrder: null,
      inputDelivery: null,
      outputDelivery: null,
      recycleDelivery: null,
      boxOwner: null,
    }
  }),

  actions: {
    updateData(file, content) {
      if (!content) return;
      
      // 使用映射表来简化判断逻辑
      const dataMapping = {
        'DroneState': 'droneState',
        'DroneDeliveryOrder': 'droneDeliveryOrder',
        'IndoorCarState': 'indoorCarState',
        'IndoorDeliveryOrder': 'indoorDeliveryOrder',
        'OutdoorCarState': 'outdoorCarState',
        'OutdoorDeliveryOrder': 'outdoorDeliveryOrder',
        'InputDelivery': 'inputDelivery',
        'OutputDelivery': 'outputDelivery',
        'RecycleDelivery': 'recycleDelivery',
        'Box_owner': 'boxOwner'
      };

      // 遍历映射表查找匹配的文件名
      for (const [key, stateKey] of Object.entries(dataMapping)) {
        if (file.includes(key)) {
          this.data[stateKey] = content;
          break;
        }
      }
    },

    setLoading(status) {
      this.loading = status;
    },

    setError(error) {
      this.error = error;
    },

    initializeData() {
      this.data = {
        droneState: null,
        droneDeliveryOrder: null,
        indoorCarState: null,
        indoorDeliveryOrder: null,
        outdoorCarState: null,
        outdoorDeliveryOrder: null,
        inputDelivery: null,
        outputDelivery: null,
        recycleDelivery: null,
        boxOwner: null,
      };
    }
  }
}); 