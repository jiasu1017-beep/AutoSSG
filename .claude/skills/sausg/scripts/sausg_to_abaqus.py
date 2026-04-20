#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAUSG 模型转 ABAQUS INP 文件
使用 SSG2INPmain.exe 将 .ssg 模型转换为 ABAQUS 可读的 .inp 文件
"""

import subprocess
import sys
import os
import glob
from typing import Optional, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

DEFAULT_SAUSG_DIR = "D:\\SAUSG2026.2"
SSG2INP_EXE = "SSG2INP\\SSG2INPmain.exe"


def find_sausg_dir(user_specified: str = None) -> str:
    """查找 SAUSG 安装目录"""
    if user_specified:
        if os.path.isdir(user_specified):
            return user_specified

    for drive in ['D:', 'C:', 'E:', 'F:']:
        try:
            result = subprocess.run(
                f'dir /ad /b {drive}\\SAUSG* 2>nul',
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        dir_path = os.path.join(drive, line.strip())
                        if os.path.isdir(dir_path):
                            return dir_path
        except Exception:
            continue

    return DEFAULT_SAUSG_DIR


def convert_single(model_path: str, output_dir: str = None, sausg_dir: str = None) -> dict:
    """转换单个模型文件"""
    model_path = os.path.abspath(model_path)

    if not os.path.exists(model_path):
        return {"status": "error", "message": f"模型文件不存在: {model_path}"}

    if not model_path.lower().endswith('.ssg'):
        return {"status": "error", "message": "模型文件必须是 .ssg 格式"}

    SAUSG_DIR = find_sausg_dir(sausg_dir)
    exe_path = os.path.join(SAUSG_DIR, SSG2INP_EXE)

    if not os.path.exists(exe_path):
        return {"status": "error", "message": f"转换程序不存在: {exe_path}"}

    if output_dir:
        output_dir = os.path.abspath(output_dir)
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                return {"status": "error", "message": f"无法创建输出目录: {e}"}
    else:
        output_dir = os.path.dirname(model_path)

    cmd = f'"{exe_path}" PATH="{output_dir}" NAME="{os.path.basename(model_path)}"'

    print(f"正在转换模型为 ABAQUS INP 格式...")
    print(f"源文件: {model_path}")
    print(f"输出目录: {output_dir}")
    print(f"命令: {cmd}")

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=SAUSG_DIR
        )

        if result.returncode == 0:
            inp_file = os.path.join(output_dir, os.path.basename(model_path).replace('.ssg', '.inp'))
            return {
                "status": "success",
                "message": f"转换成功",
                "inp_file": inp_file,
                "sausg_dir": SAUSG_DIR
            }
        else:
            return {
                "status": "error",
                "message": f"转换失败: {result.stderr or result.stdout}"
            }

    except Exception as e:
        return {"status": "error", "message": f"转换异常: {str(e)}"}


def convert_batch(input_dir: str, pattern: str = "*.ssg", output_dir: str = None, sausg_dir: str = None) -> dict:
    """批量转换目录下的所有模型"""
    input_dir = os.path.abspath(input_dir)

    if not os.path.isdir(input_dir):
        return {"status": "error", "message": f"目录不存在: {input_dir}"}

    ssg_files = glob.glob(os.path.join(input_dir, pattern))
    if not ssg_files:
        return {"status": "error", "message": f"在 {input_dir} 中未找到匹配 {pattern} 的模型文件"}

    print(f"找到 {len(ssg_files)} 个模型文件待转换")

    results = []
    for ssg_file in ssg_files:
        print(f"\n{'='*60}")
        result = convert_single(ssg_file, output_dir, sausg_dir)
        results.append(result)
        status_icon = "✓" if result["status"] == "success" else "✗"
        print(f"{status_icon} {os.path.basename(ssg_file)}: {result['message']}")

    success_count = sum(1 for r in results if r["status"] == "success")
    return {
        "status": "success",
        "message": f"批量转换完成: {success_count}/{len(ssg_files)} 成功",
        "results": results
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("SAUSG 模型转 ABAQUS INP 工具")
        print("=" * 60)
        print("用法:")
        print("  # 转换单个文件")
        print('  python sausg_to_abaqus.py "F:\\00AI\\AutoSSG\\Test\\Model.ssg"')
        print()
        print("  # 转换目录下所有模型")
        print('  python sausg_to_abaqus.py "F:\\00AI\\AutoSSG\\Test" "*.ssg"')
        print()
        print("  # 指定输出目录")
        print('  python sausg_to_abaqus.py "F:\\00AI\\AutoSSG\\Test" "*.ssg" "F:\\Output"')
        print()
        print("  # 指定软件安装目录")
        print('  python sausg_to_abaqus.py "F:\\00AI\\AutoSSG\\Test" "*.ssg" "F:\\Output" "D:\\SAUSG2026"')
        sys.exit(0)

    input_path = sys.argv[1]

    if len(sys.argv) > 2:
        pattern = sys.argv[2]
    else:
        pattern = None

    if os.path.isfile(input_path):
        result = convert_single(input_path)
    elif os.path.isdir(input_path):
        result = convert_batch(input_path, pattern or "*.ssg")
    else:
        result = {"status": "error", "message": f"路径不存在: {input_path}"}

    print(f"\n状态: {result['status']}")
    print(f"消息: {result['message']}")

    sys.exit(0 if result["status"] == "success" else 1)