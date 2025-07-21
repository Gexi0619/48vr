#!/usr/bin/env python3
"""
数据清理脚本 - 彻底删除所有旧数据文件
用于在重新获取数据前进行大换血清理
"""

import shutil
import os
from pathlib import Path

def remove_path(path, description):
    """安全删除路径（文件或目录）"""
    try:
        if path.exists():
            if path.is_file():
                path.unlink()
                print(f"🗑️  已删除文件: {description}")
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"🗑️  已删除目录: {description}")
            return True
        else:
            print(f"⚠️  路径不存在，跳过: {description}")
            return False
    except Exception as e:
        print(f"❌ 删除失败 {description}: {e}")
        return False

def main():
    print("🚀 开始清理所有旧数据...")
    print("=" * 50)
    
    # 要删除的路径列表
    paths_to_remove = [
        # 主要数据文件
        (Path("data/category.json"), "分类数据文件"),
        (Path("data/content_flat.json"), "内容扁平化数据文件"),
        (Path("data/detail_flat.json"), "详情扁平化数据文件"),
        (Path("data/detail_sip.json"), "详情SIP数据文件"),
        (Path("data/live_flat.json"), "直播扁平化数据文件"),
        
        # 内容目录
        (Path("data/contents"), "内容详细数据目录"),
        
        # 详情目录
        (Path("data/details"), "详情数据目录"),
        
        # 直播目录
        (Path("data/lives"), "直播数据目录"),
        
        # 页面目录（如果需要的话）
        # (Path("page"), "页面目录"),
    ]
    
    # 统计
    success_count = 0
    total_count = len(paths_to_remove)
    
    # 逐个删除
    for path, description in paths_to_remove:
        if remove_path(path, description):
            success_count += 1
    
    print("=" * 50)
    print(f"📊 清理结果: {success_count}/{total_count} 成功")
    
    # 检查是否需要重新创建 data 目录
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir(exist_ok=True)
        print("📁 已重新创建空的 data 目录")
    
    print("✅ 数据清理完成！现在可以运行 run_old.py 进行大换血了")

if __name__ == "__main__":
    # 自动跳过确认，直接执行清理
    print("⚠️  自动模式：跳过确认，直接执行清理操作！")
    main()
