import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# 输入输出路径
input_dir = Path("data/lives")
output_file = Path("data/live_flat.json")

def load_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 读取失败 {file.name}：{e}")
        return None

files = list(sorted(input_dir.glob("*.json")))
all_details = []

with ThreadPoolExecutor() as executor:
    results = executor.map(load_json, files)
    for data in results:
        if data is not None:
            all_details.append(data)

with open(output_file, "w", encoding="utf-8") as out:
    json.dump(all_details, out, ensure_ascii=False, indent=2)

print(f"✅ 已合并 {len(all_details)} 个 detail 项，保存至 {output_file}")

def simplify_live_data(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    simplified = []
    for item in data:
        simple = {
            "id": item.get("id"),
            "cnName": item.get("cnName"),
            "contentNumber": item.get("contentNumber"),
            "firstLetter": item.get("firstLetter"),
            "brief": item.get("brief"),
            "createTime": item.get("createTime"),
            "updateTime": item.get("updateTime"),
            "liveBroadcastSeats": []
        }
        for seat in item.get("liveBroadcastSeats", []):
            # 跳过“免费机位”
            if seat.get("name") == "免费机位":
                continue
            simple_seat = {
                "id": seat.get("id"),
                "name": seat.get("name"),
                "liveBroadcastSeatAddressList": []
            }
            for addr in seat.get("liveBroadcastSeatAddressList", []):
                simple_addr = {
                    "address": addr.get("address")
                }
                simple_seat["liveBroadcastSeatAddressList"].append(simple_addr)
            # 只保留有地址的机位
            if simple_seat["liveBroadcastSeatAddressList"]:
                simple["liveBroadcastSeats"].append(simple_seat)
        simplified.append(simple)
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(simplified, out, ensure_ascii=False, indent=2)
    print(f"✅ 已生成简洁版，保存至 {output_path}")

# 生成简洁版
simplify_live_data(output_file, Path("data/live_flat.json"))
