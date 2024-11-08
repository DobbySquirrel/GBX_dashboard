// 导入 OBS SDK
import ObsClient from 'esdk-obs-browserjs';

// 创建 ObsClient 实例
const obsClient = new ObsClient({
  access_key_id: 'NDUQZS2WFPGUUPEDRH27', // 使用Vue CLI中的环境变量 #####之后要隐藏
  secret_access_key: 'jhXyRbbqAMcgJtxa7LwcDQSBg8LonJTCaCzx7ORS',
  server: "https://obs.cn-south-1.myhuaweicloud.com", // OBS 服务器地址
});

// 定义 getObject 方法，用于下载对象
export async function getObject(bucketName, objectKey) {
  // console.log('Starting to download object:', objectKey, 'from bucket:', bucketName);
//   console.log(import.meta.env.VUE_APP_ACCESS_KEY_ID);
//   console.log(import.meta.env.VUE_APP_SECRET_ACCESS_KEY);

  try {
    // 调用OBS SDK中的 createV2SignedUrlSync 方法生成临时签名的URL
    const res = obsClient.createV2SignedUrlSync({
      Method: 'GET',
      Bucket: bucketName,
      Key: objectKey
    });

    const signedUrl = res.SignedUrl;
    // console.log('Signed URL:', signedUrl);

    // 通过fetch请求下载内容
    const response = await fetch(signedUrl);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const content = await response.text();
    // console.log('Object content received:', content);

    return content;
  } catch (error) {
    console.error('Failed to fetch data from OBS:', error);
    throw error;
  }
}
