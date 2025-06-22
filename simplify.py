import json
import re
from pathlib import Path
import shutil

input_path = Path("data/detail_flat.json")
output_path = Path("data/detail_sip.json")

def duration_to_seconds(duration_str):
    """将 'HH:MM:SS' 转为秒数"""
    try:
        h, m, s = map(int, duration_str.split(":"))
        return h * 3600 + m * 60 + s
    except:
        return 0  # 如果格式异常，返回 0

def extract_date_from_cnname(cnname):
    """从 cnName 提取六位数字并转为八位日期"""
    match = re.search(r'(\d{6})', cnname)
    if match:
        six_digit = match.group(1)
        yy = int(six_digit[:2])
        yyyy = 2000 + yy if yy < 50 else 1900 + yy  # 00-49 是2000年以后的，50-99 是1900年代
        return f"{yyyy}{six_digit[2:]}"
    return None

with open(input_path, "r", encoding="utf-8") as f:
    all_details = json.load(f)

simplified_list = []

for item in all_details:
    duration_str = item.get("duration", "00:00:00")
    if duration_to_seconds(duration_str) < 3600:
        print(f"跳过：id={item.get('id')}，cnName={item.get('cnName')}，duration={duration_str}")
        continue  # ⛔ 跳过小于1小时的视频

    cnname = item.get("cnName", "")
    date_str = extract_date_from_cnname(cnname)

    simplified = {
        "id": item.get("id"),
        "cnName": cnname,
        "date": date_str,
        "contentNumber": item.get("contentNumber"),
        "firstLetter": item.get("firstLetter"),
        "duration": duration_str,
        "brief": item.get("brief"),
        "createTime": item.get("createTime"),
        "updateTime": item.get("updateTime"),
        "liveBroadcastSeats": []
    }

    for seat in item.get("liveBroadcastSeats", []):
        new_seat = {
            "name": seat.get("name"),
            "liveBroadcastSeatAddressList": []
        }

        for addr in seat.get("liveBroadcastSeatAddressList", []):
            new_seat["liveBroadcastSeatAddressList"].append({
                "address": addr.get("address")
            })

        simplified["liveBroadcastSeats"].append(new_seat)

    simplified_list.append(simplified)

# 保存输出
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(simplified_list, f, ensure_ascii=False, indent=2)

print(f"✅ 成功生成精简文件，共 {len(simplified_list)} 条，保存为：{output_path}")

# 复制并重命名到 page/data.json
dst_path = Path("page/data.json")
dst_path.parent.mkdir(parents=True, exist_ok=True)  # 确保目标目录存在
shutil.copyfile(output_path, dst_path)
print(f"✅ 已复制到：{dst_path}")
