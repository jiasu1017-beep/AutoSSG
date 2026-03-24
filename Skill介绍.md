# 用 AI Agent 进行 SAUSG 计算：SAUSG Skill 简介

## 引子：AI Agent 时代的工程设计

2026 年的今天，如果你还在用传统方式做结构分析——手动点击软件菜单、一步步设置参数、等待计算完成——那你就 out 了！

现在，工程师的正确姿势是：**动动嘴皮子，AI Agent 帮你把活儿干了。**

"帮我打开减震模型算一下。"

"好的，马上算！"

然后你就可以去喝杯咖啡回来，结果已经静静躺在那里了。

这一切是怎么实现的？答案就是：**AI Agent + Skill = 你的私人工程助手**。

---

## 什么是 AI Agent？

### 简单来说

**AI Agent（智能代理）** 就是帮你干活的"数字员工"。

它不像以前的 AI，只能回答问题、聊聊天。现在的 AI Agent 可以：
- 接收你的指令
- 理解你要做什么
- 调用各种工具和软件
- 把结果反馈给你

### 打个比方

| 角色 | 能力 |
|------|------|
| 传统 AI | 相当于一个**知识渊博的教授**，你问什么它答什么，但让它干活？对不起，不会。 |
| AI Agent | 相当于一个**靠谱的助理**，你交代任务，它想办法完成，包括调用各种软件工具。 |

### AI Agent 的核心能力

1. **理解自然语言**：你说"帮我算一下这个模型"，它听得懂。
2. **调用工具**：它能启动各种软件、执行脚本、操作文件。
3. **自动化流程**：把原本需要手动操作的步骤变成自动化。

---

## AI Agent 如何与专业软件结合？

这是一个很现实的问题：AI Agent 再聪明，它也不知道怎么操作你电脑里的专业软件啊！

### 答案就是：Skill（技能）

**Skill** 就是告诉 AI Agent "怎么做某件事"的说明书。

打个比方：

- **AI Agent** = 刚入职的名校毕业生，理论基础扎实，但不懂你们公司的业务流程。
- **Skill** = 老员工写的《业务操作手册》。
- **毕业生 + 操作手册** = 完美员工，马上就能干活！

### Skill 的工作原理

```
你说："用减震软件打开 example2.ssg"
    ↓
AI Agent 接收指令
    ↓
AI Agent 查阅 Skill 文档（sausg.md）
    ↓
AI Agent 知道：哦，"减震软件" = SAUSGZeta.exe
    ↓
AI Agent 执行：启动 SAUSGZeta.exe 并打开模型
    ↓
返回结果："已打开，进程ID 24880"
```

有了 Skill，AI Agent 就知道该如何操作各种专业软件了！

---

## SAUSG Skill 详解

### 什么是 SAUSG Skill？

**SAUSG Skill**（即 `sausg.md`）是专门为 **SAUSG 软件**定制的 Skill 文档。

SAUSG 是干嘛的？它是**结构工程分析与设计软件**，搞建筑、桥梁、地下结构设计的工程师每天都要用到。

SAUSG 旗下有多个模块：

| 模块 | 可执行文件 | 用途 |
|------|-----------|------|
| OpenSAUSG | OpenSAUSG.exe | 通用结构分析 |
| SAUSAGE | SAUSAGE.exe | 非线性分析 |
| SAUSGDelta | SAUSGDelta.exe | 钢结构设计 |
| SAUSGJG | SAUSGJG.exe | 结构加固 |
| SAUSGPI | SAUSGPI.exe | 隔震结构 |
| SAUSGZeta | SAUSGZeta.exe | **减震结构** |

### SAUSG Skill 做什么？

它告诉 AI Agent：
- 怎么打开 SAUSG 的各种模块
- 怎么运行结构计算
- 怎么批量处理多个模型
- 怎么处理各种异常情况

---

## 如何使用 SAUSG Skill？

### 方式一：直接说话（推荐）

就像使唤自己员工一样，直接下达命令：

| 你说的话 | AI Agent 做什么 |
|---------|----------------|
| 用减震软件打开 example2.ssg | 自动启动 SAUSGZeta.exe 打开模型 |
| 用隔震模块计算这个模型 | 自动启动 SAUSGPI.exe 并运行计算 |
| 帮我算一下 Project 目录下的所有模型 | 批量计算，顺序执行 |
| 用非线性软件查看结果 | 自动启动 SAUSAGE.exe |

### 方式二：使用底层脚本

如果你想更精细地控制，可以直接调用 Python 脚本：

```bash
# 用减震模块打开模型
python .claude/skills/scripts/sausg_open.py Project/Example2.ssg 减震

# 用隔震模块打开模型
python .claude/skills/scripts/sausg_open.py Project/Example2.ssg 隔震

# 自动计算模型
python .claude/skills/scripts/sausg_calc.py Project/Example2.ssg

# 指定软件版本
python .claude/skills/scripts/sausg_calc.py Project/Example2.ssg "D:\SAUSG2026"
```

### 实际效果展示

**场景：打开减震模型**

```
用户：用减震软件打开 example2.ssg

AI Agent：
正在搜索 SAUSG 安装目录...
找到 SAUSG 版本: 2026
正在启动 SAUSGZeta (减震结构分析与设计)...
软件目录: D:\SAUSG2026
模型: F:/00AI/AutoSSG/Project/Example2.ssg
进程ID: 24880
状态: 软件已启动并打开模型 ✓
```

**场景：计算结构模型**

```
用户：计算 example2.ssg

AI Agent：
正在搜索 SAUSG 安装目录...
找到 SAUSG 版本: 2026
正在启动计算程序 FeaCalc64.exe...
计算已启动，请耐心等待...
（计算完成后自动通知你）
```

---

## SAUSG Skill 的技术细节

### 自动搜索软件

SAUSG Skill 内置了**自动搜索功能**：

- 自动扫描 D 盘及其他盘符下的 SAUSG 安装目录
- 自动提取版本号，优先使用最新版本
- 如果你指定了目录，就用你指定的

### 批量处理能力

支持批量计算多个模型：

```bash
# 第1个模型
python .claude/skills/scripts/sausg_calc.py Project/Model1.ssg
# 等待完成...

# 第2个模型
python .claude/skills/scripts/sausg_calc.py Project/Model2.ssg
# 等待完成...

# 第3个模型
python .claude/skills/scripts/sausg_calc.py Project/Model3.ssg
```

**重要**：必须等一个算完再算下一个！AI Agent 会自动检测是否有计算程序在运行。

### 兼容性

- 支持 cmd 和 PowerShell 两种终端
- 自动处理中文编码
- 支持多版本 SAUSG 共存

---

## 如何制作自己的 Skill？

看到这里，你可能已经想到了：我能不能也做一个自己的 Skill？

当然可以！跟着我做：

### 第一步：确定需求

你想让 AI Agent 帮你做什么？

比如：
- 每天自动发送天气报告
- 一键批量处理文件
- 自动写周报、发邮件
- 调用某个特定软件

### 第二步：准备执行脚本

大多数 Skill 需要一个 Python 脚本来执行具体操作：

```python
# 示例：hello.py
import sys

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "世界"
    print(f"你好，{name}！任务已完成。")

if __name__ == "__main__":
    main()
```

### 第三步：写 Skill 文档

创建一个 `.md` 文件，告诉 AI Agent 什么时候该用这个技能：

```markdown
# 我的 Skill

## 功能

向指定的人打招呼。

## 触发方式

打招呼 <名字>

## 示例

打招呼 小明
# AI 回答：你好，小明！任务已完成。
```

### 第四步：放到指定目录

把写好的 Skill 放到 `.claude/skills/` 目录下。

### 第五步：测试

大功告成！现在你可以试试：

```
用户：打招呼 小明
AI Agent：你好，小明！任务已完成。 ✓
```

---

## 为什么 AI Agent + Skill 是未来？

### 传统方式 vs AI Agent 方式

| 对比项 | 传统方式 | AI Agent + Skill 方式 |
|-------|---------|---------------------|
| 打开软件 | 手动点击开始菜单 → 找到软件 → 打开 | 说一句话，AI 帮你打开 |
| 设置参数 | 一个个手动输入 | 说一句话，AI 自动设置 |
| 运行计算 | 点击"计算"按钮等待 | 说一句话，AI 启动计算 |
| 查看结果 | 手动打开结果文件 | AI 自动展示结果 |
| 批量处理 | 一个个手动操作 | 说一句话，AI 批量处理 |

### 效率提升

以前需要 10 分钟的操作，现在 10 秒搞定。

而且最重要的是：**你不需要记住任何软件的操作步骤**。

你只需要告诉 AI 你要什么结果，AI 会想办法帮你实现。

---

## 总结

**AI Agent + Skill = 工程设计的未来**

- **AI Agent** 是帮你干活的智能助理
- **Skill** 是 AI Agent 的操作手册
- **SAUSG Skill** 就是专门为结构工程设计的操作手册

有了 SAUSG Skill，你只需要说一句话，AI Agent 就会：
1. 自动找到并启动 SAUSG 软件
2. 自动打开或计算模型
3. 自动处理各种异常情况
4. 自动返回结果给你

而制作自己的 Skill 也不难：确定需求 → 写脚本 → 写文档 → 测试，五步搞定！

---

## 彩蛋：SAUSG 模块顺口溜

> 通用 Open 领头走，
> 非线性找 SAUSAGE，
> 钢结构 Delta 来，
> 加固 JG 帮你忙，
> 隔震 PI 不能少，
> 减震 Zeta 最重要！

---

*本文档介绍如何通过 AI Agent + SAUSG Skill 进行结构工程计算*
