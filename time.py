from datetime import datetime, timedelta

# 读取 HTML 文件
with open("page/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 获取当前北京时间（东八区）
beijing_time = datetime.utcnow() + timedelta(hours=8)
formatted_time = beijing_time.strftime("%Y-%m-%d %H:%M")

# 构造替换内容
new_line = f'<div style="text-align:center;color:#888;font-size:13px;margin-bottom:8px;">\n    更新于北京时间 {formatted_time}\n  </div>'

# 替换原来的时间行
import re
html = re.sub(
    r'<div style="text-align:center;color:#888;font-size:13px;margin-bottom:8px;">.*?</div>',
    new_line,
    html,
    flags=re.DOTALL
)

# 写回 HTML 文件
with open("page/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ 已更新为：北京时间 {formatted_time}")
