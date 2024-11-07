<template>
  <!-- <div>
    <h1>OBS 数据仪表盘</h1>

    <div>
      <h2>高频更新文件</h2>
      <div v-for="(content, index) in highFrequencyFileContents" :key="index">
        <h3>文件 {{ highFrequencyFiles[index] }} 内容</h3>
        <pre>{{ content }}</pre> 
      </div>
    </div>

    <div>
      <h2>低频更新文件</h2>
      <div v-for="(content, index) in lowFrequencyFileContents" :key="index">
        <h3>文件 {{ lowFrequencyFiles[index] }} 内容</h3>
        <pre>{{ content }}</pre> 
      </div>
    </div>
  </div> -->
  <div></div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { getObject } from '@/api/obs_chart.js';

export default {
  setup(props, { emit }) {
    const highFrequencyFileContents = ref([]); // 高频更新文件内容
    const lowFrequencyFileContents = ref([]); // 低频更新文件内容
    const bucketName = 'gbxbox1'; // OBS 存储桶名称

    // 高频更新的文件列表
    const highFrequencyFiles = [
      'IndoorDeliveryCar_Property/IndoorDeliveryCar_Property_IndoorCarState.csv',
      'OutdoorDeliveryCar_Property/OutdoorDeliveryCar_Property_OutdoorCarState.csv',
      'DeliveryDrone_Property/DeliveryDrone_Property_DroneState.csv',
    ];

    // 低频更新的文件列表
    const lowFrequencyFiles = [
      'DeliveryDrone_Property/DeliveryDrone_Property_DroneDeliveryOrder.csv',
      'Delivery_Locker_Property/Delivery_Locker_Property_InputDelivery.csv',
      'Delivery_Locker_Property/Delivery_Locker_Property_OutputDelivery.csv',
      'Delivery_Locker_Property/Delivery_Locker_Property_RecycleDelivery.csv',
      'IndoorDeliveryCar_Property/IndoorDeliveryCar_Property_IndoorDeliveryOrder.csv',
      'OutdoorDeliveryCar_Property/OutdoorDeliveryCar_Property_OutdoorDeliveryOrder.csv',
    ];

    // 下载高频更新文件的方法
    const fetchHighFrequencyFiles = async () => {
      for (const file of highFrequencyFiles) {
        try {
          const content = await getObject(bucketName, file);
          highFrequencyFileContents.value.push(content); // 将每个高频文件的内容存储
          emit('update-data', { file, content });
        } catch (error) {
          console.error('Failed to fetch high frequency file:', file, error);
        }
      }
    };

    // 下载低频更新文件的方法
    const fetchLowFrequencyFiles = async () => {
      for (const file of lowFrequencyFiles) {
        try {
          const content = await getObject(bucketName, file);
          lowFrequencyFileContents.value.push(content); // 将每个低频文件的内容存储
          emit('update-data', { file, content });
        } catch (error) {
          console.error('Failed to fetch low frequency file:', file, error);
        }
      }
    };

    // 在组件挂载时分别下载高频和低频文件
    onMounted(() => {
      fetchHighFrequencyFiles();
      fetchLowFrequencyFiles();

      // 定期刷新高频更新文件
      setInterval(() => {
        highFrequencyFileContents.value = []; // 清空旧的内容
        fetchHighFrequencyFiles();
      }, 600000); // 设置刷新频率为10分钟
    });

    return {
      highFrequencyFileContents,
      lowFrequencyFileContents,
      highFrequencyFiles, // 传递文件列表到模板中
      lowFrequencyFiles,  // 传递文件列表到模板中
    };
  },
};
</script>
