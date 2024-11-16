<template>
  <div></div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { getObject } from '@/api/obs_chart.js';
import { useDataStore } from '../store';

export default {
  setup() {
    const store = useDataStore();
    
    // 文件列表配置
    const fileConfig = {
      highFrequency: [
        'IndoorDeliveryCar_Property/IndoorDeliveryCar_Property_IndoorCarState.csv',
        'OutdoorDeliveryCar_Property/OutdoorDeliveryCar_Property_OutdoorCarState.csv',
        'DeliveryDrone_Property/DeliveryDrone_Property_DroneState.csv',
        'Box/Box_owner.csv',
      ],
      lowFrequency: [
        'DeliveryDrone_Property/DeliveryDrone_Property_DroneDeliveryOrder.csv',
        'Delivery_Locker_Property/Delivery_Locker_Property_InputDelivery.csv',
        'Delivery_Locker_Property/Delivery_Locker_Property_OutputDelivery.csv',
        'Delivery_Locker_Property/Delivery_Locker_Property_RecycleDelivery.csv',
        'IndoorDeliveryCar_Property/IndoorDeliveryCar_Property_IndoorDeliveryOrder.csv',
        'OutdoorDeliveryCar_Property/OutdoorDeliveryCar_Property_OutdoorDeliveryOrder.csv',
      ]
    };

    const fetchFiles = async (files) => {
      store.setLoading(true);
      try {
        const promises = files.map(file => 
          getObject('gbxbox1', file)
            .then(content => {
              if (content) {
                store.updateData(file, content);
              }
            })
            .catch(error => {
              console.error('Failed to fetch file:', file, error);
              store.setError(`Failed to fetch ${file}: ${error.message}`);
            })
        );
        
        await Promise.all(promises);
      } catch (error) {
        console.error('Failed to fetch files:', error);
        store.setError(`Failed to fetch files: ${error.message}`);
      } finally {
        store.setLoading(false);
      }
    };

    onMounted(() => {
      store.initializeData(); // 初始化数据
      // 初始加载
      fetchFiles([...fileConfig.highFrequency, ...fileConfig.lowFrequency]);

      // 定时刷新
      setInterval(() => fetchFiles(fileConfig.highFrequency), 1000000); // 10秒
      setInterval(() => fetchFiles(fileConfig.lowFrequency), 1000000);  // 10秒
    });

    return {};
  }
};
</script>
