import subprocess
import sys
import os

# 依次运行的脚本
scripts = ["remove.py", "category.py", "old_content.py", "content_flat.py", "old_detail.py", "detail_flat.py", "simplify.py", "time.py"]

def run_script(script_name):
    print(f"\n-------\n🔄 正在运行 {script_name}...")
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            check=True  # 如果非0退出码会抛异常
        )
        print(f"✅ {script_name} 运行完成")
        if result.stdout:
            print("📄 输出：\n", result.stdout)
        if result.stderr:
            print("⚠️ 错误输出：\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"❌ 运行 {script_name} 时出错：\n{e.stderr}")
        return False
    return True

def main():
    print("🚀 启动批处理执行...\n")

    for script in scripts:
        if not os.path.exists(script):
            print(f"⚠️ 警告：找不到 {script}，跳过。")
            continue
        success = run_script(script)
        if not success:
            print("⛔ 中断后续执行。")
            break

    print("\n🏁 所有任务执行完毕。")

if __name__ == "__main__":
    main()
