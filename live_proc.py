import json
import os

# 输入输出文件路径
data_path = os.path.join('data', 'live_flat.json')
out_path = os.path.join('page', 'live.json')

# 读取原始数据
with open(data_path, 'r', encoding='utf-8') as f:
    flat_data = json.load(f)

result = []
for item in flat_data:
    # 判断标题
    if 'GNZ' in item.get('cnName', '').upper():
        cn_name = 'GNZ48 剧场直播'
        first_letter = 'G'
    else:
        cn_name = 'SNH48 剧场直播'
        first_letter = 'S'
    # 构造新结构
    new_item = {
        'id': item.get('id'),
        'cnName': cn_name,
        'date': '20301030',
        'contentNumber': item.get('contentNumber', ''),
        'firstLetter': first_letter,
        'duration': '当公演开始后可以观看',  # 注释
        'brief': item.get('brief', ''),
        'createTime': item.get('createTime', ''),
        'updateTime': item.get('updateTime', ''),
        'liveBroadcastSeats': []
    }
    # 处理机位
    for seat in item.get('liveBroadcastSeats', []):
        seat_obj = {
            'name': seat.get('name', ''),
            'liveBroadcastSeatAddressList': [
                {'address': addr.get('address', '')} for addr in seat.get('liveBroadcastSeatAddressList', [])
            ]
        }
        new_item['liveBroadcastSeats'].append(seat_obj)
    result.append(new_item)

# 写入新文件
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"转换完成，输出到 {out_path}")
