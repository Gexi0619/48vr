import json
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from datetime import datetime

# === 请求配置 ===
URL = "https://cvrapi.letinvr.com:10443/cmsClient/content/getContentDetail"
HEADERS_TEMPLATE = {
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

# === 路径 ===
input_file = Path("data/content_flat.json")
output_dir = Path("data/details")
output_dir.mkdir(parents=True, exist_ok=True)

def parse_time(s):
    # 兼容空值和不同格式
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return datetime.min

# === 加载内容列表 ===
with open(input_file, "r", encoding="utf-8") as f:
    contents = json.load(f)

# 只取 updateTime 最新的20个
contents = sorted(
    [c for c in contents if isinstance(c, dict) and c.get("updateTime")],
    key=lambda x: parse_time(x.get("updateTime")),
    reverse=True
)[:20]

# === 请求函数（带 Session 和文件检查） ===
def fetch_detail(item):
    content_number = item.get("contentNumber")
    column_tag = item.get("columnTag")
    content_type = item.get("contentType", 2)
    output_path = output_dir / f"{content_number}.json"

    # ✅ 跳过已存在文件
    if output_path.exists():
        return True, f"{content_number}（已存在）"

    headers = HEADERS_TEMPLATE.copy()
    headers["columnTag"] = column_tag

    payload = {
        "deviceType": 5,
        "contentNumber": content_number,
        "contentType": content_type
    }

    try:
        with requests.Session() as session:
            response = session.post(URL, headers=headers, json=payload, timeout=10, verify=False)
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 1000:
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(data["data"], f, ensure_ascii=False, indent=2)
                    return True, content_number
                else:
                    return False, f"{content_number} - 接口错误: {data.get('msg')}"
            else:
                return False, f"{content_number} - HTTP错误: {response.status_code}"
    except Exception as e:
        return False, f"{content_number} - 异常: {e}"

# === 高并发执行 ===
results = []
with ThreadPoolExecutor(max_workers=24) as executor:  # ✅ 增加线程数
    futures = {executor.submit(fetch_detail, item): item for item in contents}
    for future in tqdm(as_completed(futures), total=len(futures), desc="高速获取详情"):
        results.append(future.result())

# === 总结 ===
successes = [r for r in results if r[0]]
failures = [r[1] for r in results if not r[0]]

print(f"\n✅ 成功获取 {len(successes)} 条")
if successes:
    print("获取到的项目 contentName：")
    for ok, info in successes:
        # info 可能是 contentNumber 或 contentNumber（已存在），需查找原始内容
        content_number = str(info).split("（")[0]
        item = next((c for c in contents if str(c.get("contentNumber")) == content_number), None)
        if item:
            print(f"  - {item.get('contentName', '')} ({content_number})")
        else:
            print(f"  - 未知 ({content_number})")

print(f"❌ 失败 {len(failures)} 条")
if failures:
    print("部分失败示例：")
    for f in failures[:10]:
        print("  -", f)
