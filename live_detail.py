import requests
import json
from pathlib import Path

url = "https://cvrapi.letinvr.com:10443/cmsClient/content/getContentDetail"

headers = {
    "User-Agent": "UnityPlayer/2020.3.37f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)",
    "Accept": "*/*",
    "Accept-Encoding": "deflate, gzip",
    "Content-Type": "application/json",
    "columnTag": "20220506104225",
    "X-Unity-Version": "2020.3.37f1"
}

content_numbers = ["42681814", "42268397"]

Path("data/lives").mkdir(parents=True, exist_ok=True)

for content_number in content_numbers:
    payload = {
        "deviceType": 5,
        "contentNumber": content_number,
        "contentType": 4
    }
    response = requests.post(url, headers=headers, json=payload, verify=False)
    if response.status_code == 200:
        resp_json = response.json()
        if resp_json.get("code") == 1000:
            detail = resp_json["data"]
            out_path = Path(f"data/lives/{content_number}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(detail, f, ensure_ascii=False, indent=2)
            print(f"✅ 成功保存至 {out_path}")
        else:
            print(f"❌ contentNumber={content_number} 接口返回错误:", resp_json.get("msg"))
            # 跳过
    else:
        print(f"❌ contentNumber={content_number} 请求失败，状态码:", response.status_code)
        #
