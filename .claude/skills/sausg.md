# SAUSG 自动计算与操作指南

## 概述

SAUSG（结构通用分析与设计软件）是一款专业的结构工程分析与设计软件，包含多个专业模块。本指南涵盖各模块的使用方法。

## 软件信息

| 项目 | 说明 |
|------|------|
| 安装目录 | D:\SAUSG2027（默认） |
| 主程序 | SAUSAGE.exe |
| 计算程序 | FeaCalc64.exe / FeaCalc64S.exe / FeaCalcOMP64.exe |
| 下载链接 | https://product.pkpm.cn/productDetails?productId=56 |

## SAUSG 模块说明

| 模块 | 可执行文件 | 功能说明 |
|------|-----------|----------|
| OpenSAUSG | OpenSAUSG.exe | 通用结构分析与设计软件 |
| SAUSAGE | SAUSAGE.exe | 非线性结构分析与设计 |
| SAUSGDelta | SAUSGDelta.exe | 钢结构分析与设计 |
| SAUSGJG | SAUSGJG.exe | 结构加固分析与设计 |
| SAUSGPI | SAUSGPI.exe | 隔震结构分析与设计 |
| SAUSGZeta | SAUSGZeta.exe | 减震结构分析与设计 |

## 核心功能

### 1. 自动搜索软件安装目录

系统会自动搜索计算机中的 SAUSG 安装目录：
- 搜索 D 盘及其他盘符下的 SAUSGXXXX 文件夹
- 提取版本号，自动选择最新版本
- 如果用户指定了目录，则优先使用用户指定的目录

### 2. 用指定模块打开模型

使用 `sausg_open.py` 脚本用不同模块打开模型文件。

#### 命令格式

```bash
python .claude/skills/scripts/sausg_open.py <模型路径> [模块名称] [软件目录]
```

#### 模块名称对应关系

| 输入关键词 | 实际模块 |
|-----------|---------|
| open, opensausg, 通用 | OpenSAUSG |
| sausage, 非线性 | SAUSAGE |
| delta, 钢结构 | SAUSGDelta |
| jg, 加固 | SAUSGJG |
| pi, 隔震 | SAUSGPI |
| zeta, 减震 | SAUSGZeta |

#### 使用示例

```bash
# 用默认模块(OpenSAUSG)打开
python .claude/skills/scripts/sausg_open.py Test/Example.ssg

# 用隔震模块打开
python .claude/skills/scripts/sausg_open.py Project/Example.ssg 隔震

# 用减震模块打开
python .claude/skills/scripts/sausg_open.py Project/Example.ssg zeta

# 用指定版本的软件打开
python .claude/skills/scripts/sausg_open.py Project/Example.ssg 非线性 "D:\SAUSG2027"
```

#### 自然语言示例

用户可以直接说：
- "用隔震软件打开模型" -> 调用 SAUSGPI.exe
- "用Zeta打开模型" -> 调用 SAUSGZeta.exe
- "用非线性软件打开 Example2" -> 调用 SAUSAGE.exe
- "用钢结构模块查看模型" -> 调用 SAUSGDelta.exe

### 3. 自动计算模型

使用 `sausg_calc.py` 脚本自动运行 SAUSG 计算程序进行结构分析。

#### 命令格式

```bash
python .claude/skills/scripts/sausg_calc.py <模型路径> [软件目录] [--no-cleanup]
```

#### 参数说明

- `模型路径`: .ssg 格式的模型文件完整路径
- `软件目录`: 可选，指定 SAUSG 安装目录
- `--no-cleanup`: 可选，计算前不清理模型目录下的旧文件

#### 使用示例

```bash
# 自动搜索软件并计算（默认会清理旧文件）
python .claude/skills/scripts/sausg_calc.py Test/Example.ssg

# 指定软件目录
python .claude/skills/scripts/sausg_calc.py Project/Example2.ssg "D:\SAUSG2026"

# 不清理旧文件
python .claude/skills/scripts/sausg_calc.py Test/Example.ssg --no-cleanup
```

#### 自动清理功能

计算前会自动清理模型目录下的以下文件：

| 类型 | 文件扩展名 |
|------|-----------|
| 结果文件 | .BCR, .BEM, .BLR, .PAR, .DEF |
| 日志文件 | .MSG |
| 中间文件 | .D01~.D05, .EIG, .FRQ, .MFQ, .MOD, .MOF, .NSD, .NSF |
| 输出文件 | .INP, .TXT, .DAT, .CSV |
| 图片文件 | .jpg, .png |
| 结果文件夹 | StaticResult/, EarthQuakeResult/, DesignResult/ |

**注意**: 模型文件本身（.ssg）不会被删除。

#### 计算进度提示

计算过程中会实时显示各阶段进度：

| 阶段 | 完成标志 |
|------|---------|
| 网格划分 | .BCR 或 .BEM 文件生成 |
| 初始分析 | StaticResult 文件夹（.FRQ/.MFQ/.NSF） |
| 动力时程分析 | EarthQuakeResult 文件夹 |
| 结果报告 | .DOCX 计算报告 |

#### 主要结果输出

计算完成后自动输出主要结果：

- 基本周期 (T1, T2, T3...)
- 频率 (f1, f2, f3...)
- 楼层总重
- 底部反力 (Rx, Ry, Rz)
- 计算报告文件名

### 4. 批量计算多个模型

**重要：必须等待前一个模型计算完成后再计算下一个模型！**

由于系统会检测是否有计算程序正在运行，因此批量计算时需要顺序执行：

```bash
# 第1个模型计算完成后再执行第2个
python .claude/skills/scripts/sausg_calc.py Project/Model1.ssg
# 等待上述计算完成后，再执行下一个
python .claude/skills/scripts/sausg_calc.py Project/Model2.ssg
# 等待计算完成后再执行下一个
python .claude/skills/scripts/sausg_calc.py Project/Model3.ssg
```

## 项目结构

```
F:\00AI\AutoSSG\
├── Project\                 # 项目模型文件目录
│   └── Example2.ssg         # 示例模型
├── Test\                    # 测试目录
│   └── Example.ssg          # 测试用模型
├── run.bat                  # 快捷启动脚本
├── SAUSG说明.md             # SAUSG 软件说明
├── .claude\
│   └── skills\
│       ├── saucg.md         # 本文档
│       └── scripts\
│           ├── saucg_calc.py  # 计算脚本（支持自动搜索软件）
│           └── saucg_open.py   # 模块启动脚本（支持自动搜索软件）
```

## 支持的终端环境

脚本同时支持 **cmd** 和 **PowerShell** 两种终端环境。

### cmd
```cmd
python .claude/skills/scripts/sausg_calc.py Test/Example.ssg
```

### PowerShell
```powershell
python .claude/skills/scripts/sausg_calc.py Test/Example.ssg
```

脚本会自动处理编码问题，确保在两种环境下都能正常显示中文。

## 重要注意事项

1. **不要同时启动多个计算程序**
   - 系统会自动检测是否有计算程序正在运行
   - 如果有程序正在运行，会提示用户等待

2. **批量计算必须顺序执行**
   - **必须**等待前一个模型计算完成后再计算下一个
   - 禁止同时启动多个计算任务
   - 每计算完一个模型后再启动下一个

3. **软件自动搜索**
   - 默认搜索 D:\SAUSG2027
   - 如果未找到，会自动搜索其他盘符
   - 支持多版本，自动选择最新版本

4. **计算时间**
   - 计算时间可能较长，请耐心等待
   - 计算完成后结果保存在模型同目录下

5. **软件未找到**
   - 如果无法找到软件，会提示下载链接
   - 下载地址：https://product.pkpm.cn/productDetails?productId=56
