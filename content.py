import json
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# 常量
BASE_URL = "https://cvrapi.letinvr.com:10443/cmsClient/content/getContentList"
HEADERS = {
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

COMMON_PAYLOAD = {
    "appId": "100024",
    "page": 1,
    "size": 10000,
    # "mac": "",
    "filmId": "123518",
    # "clientModel": "",
    "appVersion": "2.4.0",
    # "deviceId": "",
    "deviceType": 5
}

# 加载 category.json，定位 id == 9181
with open("data/category.json", "r", encoding="utf-8") as f:
    categories = json.load(f)

root = next((cat for cat in categories if cat["id"] == 9181), None)
if not root:
    print("❌ 未找到 id=9181 的分类")
    exit(1)

targets = []
for child1 in root.get("child", []):
    for child2 in child1.get("child", []):
        targets.append({
            "columnId": child2["columnId"],
            "name": child2["name"]
        })

# 只保留 columnId 最大的4个
targets = sorted(targets, key=lambda x: x["columnId"], reverse=True)[:4]

# 创建保存目录
output_dir = Path("data/contents")
output_dir.mkdir(parents=True, exist_ok=True)

# 获取内容函数
def fetch_and_save_content(column):
    column_id = column["columnId"]
    name = column["name"]
    payload = COMMON_PAYLOAD.copy()
    payload["columnId"] = column_id

    try:
        response = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=20, verify=False)
        response.raise_for_status()
        data = response.json()
        if data.get("code") == 1000:
            with open(output_dir / f"{column_id}.json", "w", encoding="utf-8") as f_out:
                json.dump(data["data"], f_out, ensure_ascii=False, indent=2)
            return True, column_id
        else:
            return False, f"{column_id} - 接口返回异常: {data.get('msg')}"
    except Exception as e:
        return False, f"{column_id} - 异常: {e}"

# 多线程执行 + tqdm 进度条
print(f"🔍 共 {len(targets)} 个子类，开始获取内容...")
results = []
with ThreadPoolExecutor(max_workers=6) as executor:
    futures = {executor.submit(fetch_and_save_content, col): col for col in targets}
    for future in tqdm(as_completed(futures), total=len(futures), desc="获取中"):
        success, info = future.result()
        results.append((success, info))

# 结果统计
ok = sum(1 for s, _ in results if s)
failures = [info for s, info in results if not s]

print(f"\n✅ 成功获取 {ok} 个内容列表")
if failures:
    print(f"❌ 失败 {len(failures)} 个：")
    for f in failures:
        print("  -", f)
