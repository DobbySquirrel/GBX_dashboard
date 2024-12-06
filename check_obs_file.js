// 引入obs库
// 使用npm安装
import ObsClient from "esdk-obs-nodejs";
// 使用源码安装
// 创建ObsClient实例
const obsClient = new ObsClient({
  // 推荐通过环境变量获取AKSK，这里也可以使用其他外部引入方式传入，如果使用硬编码可能会存在泄露风险
  // 您可以登录访问管理控制台获取访问密钥AK/SK，获取方式请参见https://support.huaweicloud.com/usermanual-ca/ca_01_0003.html
  access_key_id: 'NDUQZS2WFPGUUPEDRH27',
  secret_access_key: 'jhXyRbbqAMcgJtxa7LwcDQSBg8LonJTCaCzx7ORS',

  server: "https://obs.cn-south-1.myhuaweicloud.com",
});

async function getObjectContent() {
  try {
    const params = {
      Bucket: "gbxbox1",
      Key: 'User_Score/Score_Record.csv',
    };
    
    // 获取对象内容
    const result = await obsClient.getObject(params);
    if (result.CommonMsg.Status <= 300) {
      console.log("获取对象成功!");
      console.log("RequestId:", result.CommonMsg.RequestId);
      console.log("ETag:", result.InterfaceResult.ETag);
      console.log("内容类型:", result.InterfaceResult.ContentType);
      
      // 输出文件内容
      const content = result.InterfaceResult.Content.toString();
      console.log("文件内容:", content);
      return;
    }
    
    console.log("OBS错误：请求被拒绝");
    console.log("状态码:", result.CommonMsg.Status);
    console.log("错误代码:", result.CommonMsg.Code);
    console.log("错误信息:", result.CommonMsg.Message);
    console.log("RequestId:", result.CommonMsg.RequestId);
  } catch (error) {
    console.log("发生异常：可能是网络问题或其他内部错误");
    console.log(error);
  }
}

getObjectContent();
