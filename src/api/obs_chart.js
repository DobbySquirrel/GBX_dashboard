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
      // 直接使用 ObsClient 的 getObject 方法
      const result = await obsClient.getObject({
        Bucket: bucketName,
        Key: objectKey,
      });

      if (result.CommonMsg.Status < 300) { // 成功状态码
        // 将 Buffer 转换为文本
        const content = result.InterfaceResult.Content.toString();
        return content;
      } else {
        throw new Error(`OBS Error: ${result.CommonMsg.Message}`);
      }

    } catch (error) {
      console.error(`Attempt ${i + 1} failed:`, error);
      lastError = error;
      
      if (i === retries - 1) {
        console.error(`Failed to fetch data from OBS after ${retries} retries:`, error);
        throw lastError;
      }
      
      // 指数退避策略
      await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
    }
  }
}
