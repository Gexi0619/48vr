import json
from pathlib import Path

input_dir = Path("data/contents")
output_file = Path("data/content_flat.json")

all_contents = []

# 遍历目录下的所有 JSON 文件
for file in sorted(input_dir.glob("*.json")):
    try:
        with open(file, "r", encoding="utf-8") as f:
            content_list = json.load(f)
            if isinstance(content_list, list):
                for item in content_list:
                    item.pop("productInfo", None)
                    all_contents.append(item)
    except Exception as e:
        print(f"⚠️ 无法读取 {file.name}：{e}")

# 保存合并结果
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(all_contents, out, ensure_ascii=False, indent=2)

print(f"✅ 成功合并 {len(all_contents)} 条内容，保存至 {output_file}")
