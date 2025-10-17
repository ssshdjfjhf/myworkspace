import requests
import json
import os 

# 填写你的API Key
# 2. 验证环境变量是否设置成功
API_KEY = os.getenv("BOCHA_API_KEY")  # 读取环境变量中的API Key
# 请求配置
url = "https://api.bochaai.com/v1/web-search"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "query": "天空为什么是蓝色的？",  # 搜索关键词
    "summary": True,               # 显示摘要
    "count": 5,                    # 返回5条结果
    "page": 1                      # 第一页
}

# 发送请求
response = requests.post(url, headers=headers, data=json.dumps(payload))

# 解析结果
if response.status_code == 200: # 请求成功
    results = response.json() # 解析JSON结果
    print("搜索成功！结果如下：")
    for item in results["data"]["webPages"]["value"]: # 遍历搜索结果
        print(f"标题：{item['name']}")
        print(f"链接：{item['url']}")
        print(f"摘要：{item['snippet']}\n")
else:
    print(f"请求失败！错误码：{response.status_code}, 详情：{response.text}")