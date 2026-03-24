## 说明

SAUSG软件安装目录为D:\SAUSG2026.2，执行程序为SAUSAGE.exe

模型文件为.ssg

采用命令行 SAUSAGE.exe TYPE=OPEN BATCH=0 PATH="F:\00AI\AutoSSG\Test\Example.ssg" 可启动软件自动进行计算，F:\00AI\AutoSSG\Test\Example.ssg为模型路径。

FeaCalc64.exe/FeaCalc64S.exe/FeaCalcOMP64.exe为计算程序，三者任意一个启动即开始计算，应等待计算完成，返回运行情况。

## 软件安装目录

软件安装目录一般为SAUSGXXXX，XXXX为版本号。如果用户指定了软件安装目录，则在用户指定的目录下启动软件；如果用户未指定，则自动搜索计算机中的安装的软件（搜索SAUSAGE.exe文件），如果安装多个版本的软件，则使用最新版本的软件；如果无法找到软件路径，则提示用户下载https://product.pkpm.cn/productDetails?productId=56

## 多模块

软件模块包括OpenSAUSG.exe（OpenSAUSG）、SAUSAGE.exe（非线性）、SAUSGDelta.exe（钢结构）、SAUSGJG.exe（加固）、SAUSGPI.exe（隔震）、SAUSGZeta.exe（减震）等模块，支持用户用不同模块打开
例如：用户说用隔震软件打开模型，则调用SAUSGPI.exe打开模型。
例如：用户说用Zeta打开模型，则调用SAUSGZeta.exe打开模型。

## 注意要点

* 不要同时启动多个计算程序