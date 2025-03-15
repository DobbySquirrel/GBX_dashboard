# -*- coding: utf-8 -*-
import time
import uuid
import hashlib
import base64
import requests #需要先使用pip install requests命令安装依赖
import os

# 必填,请参考"开发准备"获取如下数据,替换为实际值
url = '	https://smsapi.cn-south-1.myhuaweicloud.com:443/sms/batchSendSms/v1' #APP接入地址(在控制台"应用管理"页面获取)+接口访问URI
# // 认证用的appKey和appSecret硬编码到代码中或者明文存储都有很大的安全风险，建议在配置文件或者环境变量中密文存放，使用时解密，确保安全；
APP_KEY = os.getenv("APP_KEY") #APP_Key
APP_KEY = '0xC23o253LS2dxnxFWHV4fzA6Spc' #APP_Key
APP_SECRET = os.getenv("APP_SECRET") #APP_Secret
APP_SECRET = 'lmv6nplJYqOfXzqwgouU11DhQbhg' #APP_Secret
sender = "cs106900001987" #国内短信签名通道号
TEMPLATE_ID = "a61c9c47545841228c7f127c3b447309" #模板ID

#条件必填,国内短信关注,当templateId指定的模板类型为通用模板时生效且必填,必须是已审核通过的,与模板类型一致的签名名称
signature = "华为云短信测试" #签名名称

# 必填,全局号码格式(含国家码),示例:+86151****6789,多个号码之间用英文逗号分隔
receiver = "+8613671929117" #短信接收人号码
# receiver = "+8619866135474" #短信接收人号码
# # receiver = "+8613128779225" #短信接收人号码

# 选填,短信状态报告接收地址,推荐使用域名,为空或者不填表示不接收状态报告
statusCallBack = ""

'''
选填,使用无变量模板时请赋空值 TEMPLATE_PARAM = '';
单变量模板示例:模板内容为"您的验证码是${1}"时,TEMPLATE_PARAM可填写为'["369751"]'
双变量模板示例:模板内容为"您有${1}件快递请到${2}领取"时,TEMPLATE_PARAM可填写为'["3","人民公园正门"]'
模板中的每个变量都必须赋值，且取值不能为空
查看更多模板规范和变量规范:产品介绍>短信模板须知和短信变量须知
'''
TEMPLATE_PARAM = '["123"]' #模板变量，此处以单变量验证码短信为例，请客户自行生成6位验证码，并定义为字符串类型，以杜绝首位0丢失的问题（例如：002569变成了2569）。

'''
构造X-WSSE参数值
@param appKey: string
@param appSecret: string
@return: string
'''
def buildWSSEHeader(appKey, appSecret):
    now = time.strftime('%Y-%m-%dT%H:%M:%SZ') #Created
    nonce = str(uuid.uuid4()).replace('-', '') #Nonce
    digest = hashlib.sha256((nonce + now + appSecret).encode()).hexdigest()

    digestBase64 = base64.b64encode(digest.encode()).decode() #PasswordDigest
    return 'UsernameToken Username="{}",PasswordDigest="{}",Nonce="{}",Created="{}"'.format(appKey, digestBase64, nonce, now)

def send_sms(template_id, receiver, template_param):
    """
    发送短信的函数
    
    Args:
        template_id (str): 模板ID
        receiver (str): 接收者手机号（格式如：+8613671929117）
        template_param (str): 模板参数（JSON字符串，如：'["123"]'）
    
    Returns:
        dict/str: 响应结果
    """
    # 请求Headers
    print(f"Send SMS to {receiver} with template_id {template_id} and template_param {template_param}")
    # return("success")
    header = {'Authorization': 'WSSE realm="SDP",profile="UsernameToken",type="Appkey"',
              'X-WSSE': buildWSSEHeader(APP_KEY, APP_SECRET)}
    
    # 请求Body
    formData = {'from': sender,
                'to': receiver,
                'templateId': template_id,
                'templateParas': template_param,
                'statusCallback': statusCallBack,
                'signature': signature
                }
    
    r = requests.post(url, data=formData, headers=header, verify=False)
    
    try:
        response_body = r.json()
        # print("响应内容:", response_body)
        
        # if response_body.get('code') == '000000':
        #     result = response_body.get('result', [])
        #     if result:
        #         status = result[0].get('status')
        #         smsMsgId = result[0].get('smsMsgId')
                
        #         if status == 'DELIVRD' or status == '000000':
        #             print('发送短信成功. smsMsgId:', smsMsgId)
        #         else:
        #             print('发送短信失败. smsMsgId:', smsMsgId)
        #             print('失败状态码:', status)
        # else:
        #     print('API调用失败')
        #     print('错误代码:', response_body.get('code'))
        #     print('错误描述:', response_body.get('description'))
            
        #     if 'result' in response_body and response_body['result']:
        #         status = response_body['result'][0].get('status')
        #         smsMsgId = response_body['result'][0].get('smsMsgId')
        #         print('短信ID:', smsMsgId)
        #         print('状态码:', status)
            
        return response_body
    except ValueError as e:
        # print("解析响应失败:")
        # print(r.text)
        return r.text

def main():
    # 示例调用
    template_id = "a61c9c47545841228c7f127c3b447309"  # 默认模板ID
    receiver = "+8613671929117"  # 默认接收者
    template_param = '["-123"]'  # 默认模板参数
    
    return send_sms(template_id, receiver, template_param)

if __name__ == '__main__':
    main() 
