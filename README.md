# AutoSSG

SAUSG 结构分析软件自动化工具，集成 Claude Code Skill。

## 功能特性

- **自动打开模型** - 用指定模块打开 .ssg 模型文件
- **自动计算** - 自动运行结构计算，实时显示进度
- **多模块支持** - 支持 OpenSAUSG、SAUSAGE、SAUSGDelta、SAUSGJG、SAUSGPI、SAUSGZeta 等模块
- **自动搜索** - 自动搜索计算机中的 SAUSG 安装目录，优先使用最新版本
- **结果解析** - 自动读取并展示计算结果（周期、频率、底部反力等）

## 使用方法

### 通过 Claude Code（推荐）

直接告诉 AI 你要做什么：

| 指令 | 操作 |
|------|------|
| 用减震软件打开 Example.ssg | 启动 SAUSGZeta.exe 打开模型 |
| 计算 Project/Example.ssg | 自动运行计算并等待完成 |
| 用隔震模块计算这个模型 | 启动 SAUSGPI.exe 并运行计算 |

### 直接运行脚本

```bash
# 打开模型（默认使用 OpenSAUSG）
python .claude/skills/scripts/sausg_open.py Project/Example.ssg

# 用指定模块打开
python .claude/skills/scripts/sausg_open.py Project/Example.ssg 隔震

# 运行计算
python .claude/skills/scripts/sausg_calc.py Project/Example.ssg
```

## 项目结构

```
AutoSSG/
├── .claude/
│   └── skills/
│       └── scripts/
│           ├── saussg_open.py    # 模型打开脚本
│           └── saussg_calc.py    # 计算脚本
├── Project/                      # 单模型测试目录
├── MulProject/                   # 多模型测试目录
├── run.bat                       # 快速启动脚本
└── README.md
```

## 计算进度说明

计算分为四个阶段，系统会实时显示各阶段完成状态：

1. **网格划分** - .BCR/.BEM 文件生成
2. **初始分析** - StaticResult 文件夹，包含 .FRQ/.MFQ/.NSF 文件
3. **动力时程分析** - EarthQuakeResult 文件夹
4. **结果报告** - .docx 计算报告生成

## 注意事项

- 不要同时启动多个计算程序
- 支持 cmd 和 PowerShell 环境
- 模型文件使用 .ssg 格式
- 在trae中使用，需要将python加入白名单
