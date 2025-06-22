import requests
import json
from pathlib import Path

# 请求目标地址
url = "https://cvrapi.letinvr.com:10443/cmsClient/content/getCategoryList"

# 请求头，用户信息不需要填写
headers = {
    "Host": "cvrapi.letinvr.com:10443",
    "User-Agent": "UnityPlayer/2020.3.37f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)",
    "Accept": "*/*",
    "Accept-Encoding": "deflate, gzip",
    # "Cookie": "",
    "Content-Type": "application/json",
    # "userId": "",
    # "token": "",
    # "mac": "",
    # "filmId": "",
    "X-Unity-Version": "2020.3.37f1"
}

# 请求体
payload = {
    "filmId": "123518",
    # "mac": "",
    # "clientModel": "",
    "appVersion": "2.4.0",
    # "deviceId": "",
    "deviceType": 5,
    # "userId": ""
}

# 发送请求
response = requests.post(url, headers=headers, json=payload, verify=False)

# 检查状态码并保存
if response.status_code == 200:
    data = response.json()
    if data.get("code") == 1000:
        Path("data").mkdir(exist_ok=True)
        with open("data/category.json", "w", encoding="utf-8") as f:
            json.dump(data["data"], f, ensure_ascii=False, indent=2)
        print("✅ 已保存到 data/category.json")
    else:
        print("❌ 接口返回错误:", data.get("msg"))
else:
    print("❌ 请求失败，状态码:", response.status_code)
