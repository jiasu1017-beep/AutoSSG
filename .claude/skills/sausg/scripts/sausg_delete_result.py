#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAUSG 删除计算结果脚本
用于删除模型目录下的计算结果文件

功能：
- 删除模型目录下除 .ssg 和 Userdata 外的所有文件
- 支持 dry-run 模式（只显示不删除）
"""

import os
import sys
import shutil
from typing import Optional


def normalize_windows_path(model_path: str) -> str:
    """将模型路径转换为Windows绝对路径格式"""
    if os.path.isabs(model_path) and (':' in model_path):
        if len(model_path) >= 2 and model_path[1] == ':':
            return model_path[0].upper() + model_path[1:]
        return model_path

    if '/' in model_path or '\\' in model_path:
        if model_path[0].isalpha() and len(model_path) > 2 and model_path[1] == '/':
            drive = model_path[0].upper()
            rest = model_path[2:].replace('/', '\\')
            model_path = drive + ':' + rest

    if not os.path.isabs(model_path):
        cwd = os.getcwd()
        model_path = os.path.join(cwd, model_path)

    model_path = os.path.normpath(model_path)

    if len(model_path) >= 2 and model_path[1] == ':':
        model_path = model_path[0].upper() + model_path[1:]

    return model_path


def delete_calc_results(model_path: str, dry_run: bool = True) -> dict:
    """
    删除模型目录下的计算结果（保留 .ssg 和 Userdata）

    Args:
        model_path: 模型文件路径或目录路径
        dry_run: 如果为True，只显示要删除的文件但不实际删除

    Returns:
        dict: 包含删除结果的字典
    """
    # 转换路径
    model_path = normalize_windows_path(model_path)

    # 判断是文件还是目录
    if os.path.isfile(model_path):
        model_dir = os.path.dirname(model_path)
    elif os.path.isdir(model_path):
        model_dir = model_path
    else:
        return {"status": "error", "message": f"路径不存在: {model_path}"}

    deleted_files = []
    deleted_folders = []
    skipped_items = []
    errors = []

    if not os.path.isdir(model_dir):
        return {"status": "error", "message": f"目录不存在: {model_dir}"}

    try:
        for item in os.listdir(model_dir):
            item_upper = item.upper()
            item_path = os.path.join(model_dir, item)

            # 保留 .ssg 文件
            if item_upper.endswith('.SSG'):
                skipped_items.append(f"{item} (.ssg文件)")
                continue

            # 保留 Userdata 文件夹
            if item == 'Userdata':
                skipped_items.append(f"{item}/ (Userdata文件夹)")
                continue

            # 删除其他文件和文件夹
            try:
                if dry_run:
                    if os.path.isdir(item_path):
                        deleted_folders.append(item)
                    else:
                        deleted_files.append(item)
                else:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                        deleted_folders.append(item)
                    else:
                        os.remove(item_path)
                        deleted_files.append(item)
            except Exception as e:
                errors.append(f"删除失败: {item}, 错误: {e}")

    except Exception as e:
        return {"status": "error", "message": f"访问目录出错: {e}"}

    return {
        "status": "success",
        "deleted_files": deleted_files,
        "deleted_folders": deleted_folders,
        "skipped_items": skipped_items,
        "errors": errors,
        "total_deleted": len(deleted_files) + len(deleted_folders)
    }


def format_delete_result(result: dict) -> str:
    """格式化删除结果为可读字符串"""
    lines = []

    if result["status"] == "error":
        return f"错误: {result['message']}"

    lines.append("=" * 50)
    lines.append("删除结果预览:" if result.get("dry_run", True) else "删除完成:")
    lines.append("=" * 50)

    if result["deleted_folders"]:
        lines.append(f"\n将删除的文件夹 ({len(result['deleted_folders'])} 个):")
        for folder in result["deleted_folders"]:
            lines.append(f"  - {folder}/")

    if result["deleted_files"]:
        lines.append(f"\n将删除的文件 ({len(result['deleted_files'])} 个):")
        for f in result["deleted_files"]:
            lines.append(f"  - {f}")
        if len(result["deleted_files"]) > 20:
            lines.append(f"  ... 还有 {len(result['deleted_files']) - 20} 个文件")

    if result["skipped_items"]:
        lines.append(f"\n将保留的项目 ({len(result['skipped_items'])} 个):")
        for item in result["skipped_items"]:
            lines.append(f"  - {item}")

    if result["errors"]:
        lines.append(f"\n错误 ({len(result['errors'])} 个):")
        for err in result["errors"]:
            lines.append(f"  - {err}")

    lines.append(f"\n总计: 将删除 {result['total_deleted']} 个项目")

    return "\n".join(lines)


if __name__ == "__main__":
    # 解析参数
    dry_run = True
    model_path = None

    for arg in sys.argv[1:]:
        if arg == '--confirm':
            dry_run = False
        elif not arg.startswith('-'):
            model_path = arg

    if not model_path:
        print("SAUSG 删除计算结果脚本")
        print("=" * 50)
        print("用法: python sausg_delete_result.py <模型文件或目录> [--confirm]")
        print()
        print("功能: 删除模型目录下的所有计算结果，保留 .ssg 和 Userdata 文件夹")
        print()
        print("参数:")
        print("  模型文件或目录: .ssg 文件路径或模型目录路径")
        print("  --confirm: 确认删除（不指定则只显示预览）")
        print()
        print("示例:")
        print('  python sausg_delete_result.py Test/Example.ssg')
        print('  python sausg_delete_result.py Test/Example.ssg --confirm')
        print('  python sausg_delete_result.py Test/')
        sys.exit(1)

    result = delete_calc_results(model_path, dry_run)

    # 判断是否真的执行了删除（dry_run 模式下仍显示预览）
    result["dry_run"] = dry_run
    print(format_delete_result(result))

    if dry_run:
        print("\n" + "=" * 50)
        print("提示: 以上是预览结果，实际删除请添加 --confirm 参数")

    sys.exit(0 if result["status"] == "success" else 1)