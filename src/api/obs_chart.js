// 导入 OBS SDK
import ObsClient from 'esdk-obs-browserjs';

// 创建 ObsClient 实例
const obsClient = new ObsClient({
  access_key_id: import.meta.env.VITE_OBS_ACCESS_KEY_ID,
  secret_access_key: import.meta.env.VITE_OBS_SECRET_ACCESS_KEY,
  server: 'https://obs.cn-south-1.myhuaweicloud.com'
});

// 改进的 getObject 方法
export async function getObject(bucketName, objectKey, retries = 3) {
  let lastError = null;
  
  for (let i = 0; i < retries; i++) {
    try {
      const result = await obsClient.getObject({
        Bucket: bucketName,
        Key: objectKey,
        'ResponseCacheControl': 'no-cache',
        'RequestHeader': {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache'
        }
      });

      if (result.CommonMsg.Status < 300) {
        const content = result.InterfaceResult.Content.toString();
        return content;
      } else {
        console.error('OBS Response Status:', result.CommonMsg.Status);
        console.error('OBS Response Message:', result.CommonMsg.Message);
        
        if (result.CommonMsg.Status === 404) {
          return '';
        }
        throw new Error(`OBS Error: ${result.CommonMsg.Message}`);
      }
    } catch (error) {
      console.error(`OBS Error (Attempt ${i + 1}/${retries}):`, error);
      lastError = error;
      
      if (i === retries - 1) {
        console.error('All retries failed for:', objectKey);
        return '';
      }
      
      await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
    }
  }
  
  return '';
}
