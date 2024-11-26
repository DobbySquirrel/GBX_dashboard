// 导入 OBS SDK
import ObsClient from 'esdk-obs-browserjs';

// 创建 ObsClient 实例
const obsClient = new ObsClient({
  access_key_id: import.meta.env.VITE_OBS_ACCESS_KEY_ID,
  secret_access_key: import.meta.env.VITE_OBS_SECRET_ACCESS_KEY,
  server: import.meta.env.VITE_OBS_SERVER
});

// 定义 getObject 方法,添加重试机制和错误处理
export async function getObject(bucketName, objectKey, retries = 3) {
  let lastError = null;
  
  for (let i = 0; i < retries; i++) {
    try {
      const result = await obsClient.getObject({
        Bucket: bucketName,
        Key: objectKey,
      });

      if (result.CommonMsg.Status < 300) {
        const content = result.InterfaceResult.Content.toString();
        return content;
      } else {
        if (result.CommonMsg.Status === 404) {
          return '';
        }
        throw new Error(`OBS Error: ${result.CommonMsg.Message}`);
      }

    } catch (error) {
      if (error.message.includes('does not exist')) {
        return '';
      }
      
      lastError = error;
      
      if (i === retries - 1) {
        return '';
      }
      
      await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
    }
  }
  
  return '';
}
