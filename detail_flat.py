import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# 输入输出路径
input_dir = Path("data/details")
output_file = Path("data/detail_flat.json")

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
    json.dump(all_details, out, ensure_ascii=False)  # 去掉 indent 提升速度

print(f"✅ 已合并 {len(all_details)} 个 detail 项，保存至 {output_file}")
