# SPC统计分析工具 v2.4

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> 现代化的统计过程控制(SPC)分析工具，自动生成优美的HTML和PDF报告。  
> 支持YAML外部配置多项目管理，可轻松集成到PyQt/PySide等GUI应用。  
> 支持 Cpk 分析 + GRR 测量系统分析 + 规格限对比工具。  
> HTML报告图片Base64内嵌，发送时仅需HTML+PDF两个文件。

**简体中文** | [English](README_EN.md)

---

## 📖 项目简介

SPC (Statistical Process Control) 统计分析工具是一个用于制造业质量控制的Python工具包。它能够:

- 📊 自动计算Cpk、Mean、Sigma等关键统计指标
- 🎨 生成现代化的HTML报告（响应式设计、渐变背景、卡片布局）
- 📄 生成专业的PDF报告（A4尺寸、表格分页、300 DPI高清输出）
- 📈 绘制直方图和正态分布拟合曲线
- 🎯 智能Cpk彩色标识（优秀/可接受/不合格）
- 🔄 支持通过YAML配置文件批量处理多个项目
- 🔌 提供清晰的Python API，易于集成到PyQt/PySide等GUI应用
- 🔬 **新增** Cpk反向分析：指定目标Cpk值，自动推导每列数据的规格上下限（LSL/USL）
- 📂 **新增** 支持 CSV 和 Excel (.xlsx/.xls) 数据文件直接分析
- 📐 **新增** GRR 测量系统分析（ANOVA/AIAG 方法），生成 HTML/Markdown/PDF 报告
- 📐 GRR 报告包含 %EV、%AV、%GRR 等百分比指标
- 🔍 **新增** 规格限对比工具：将 CSV 文件中的规格限与 YAML 配置进行逐项对比
- 📦 **优化** HTML报告图片Base64内嵌，无需单独图片文件夹，发送更便捷

---

## ✨ 功能特性

### 统计分析
- ✅ 自动计算Cpk过程能力指数
- ✅ 计算均值(Mean)和标准差(Sigma)
- ✅ 直方图与正态分布曲线拟合
- ✅ 规格限(USL/LSL)可视化
- ✅ 样本数量统计

### 报告生成
- ✅ **HTML报告**: 现代化渐变背景、响应式卡片布局、统计概览仪表板、Cpk值彩色标识、悬停动画效果、适配桌面/平板/手机
- ✅ **PDF报告**: A4标准纸张尺寸、表格自动分页(每页20行)、专业配色方案、智能文本换行、300 DPI高清输出、每个参数独立分布图

### 配置与集成
- ✅ YAML外部配置文件，配置与代码完全分离
- ✅ 一个配置文件管理多个项目
- ✅ 支持绝对路径和相对路径
- ✅ 自动处理缺失数据
- ✅ 提供清晰的Python API接口，便于集成到PyQt/PySide

### Cpk反向分析（新增）
- ✅ 指定目标Cpk值，自动反推规格上下限（LSL/USL）
- ✅ 支持 CSV 和 Excel (.xlsx/.xls) 数据文件
- ✅ 自动识别所有数值列，无需手动配置规格限
- ✅ 支持指定 Excel 工作表名称
- ✅ 生成 HTML + PDF 分析报告
- ✅ 直方图 + 正态分布拟合曲线 + 规格限标注

### 规格限对比工具（新增）
- ✅ 将 CSV 文件中的 TEST_NAME / LOWER_LIMIT / UPPER_LIMIT 与 YAML 配置中相同 project id 的 spec_limits 逐项对比
- ✅ 自动识别匹配项、差异项、仅 CSV 项、仅 YAML 项
- ✅ 生成带时间戳的 Markdown 对比报告
- ✅ 重点标示存在差异的测试项

### GRR 测量系统分析
- ✅ 支持 ANOVA 方差分析法 和 AIAG 均值极差法
- ✅ 自动计算 EV(重复性)、AV(再现性)、PV(零件变异)、%GRR、ndc
- ✅ 报告包含 %EV、%AV、%GRR 百分比指标
- ✅ 支持自定义操作员/零件/测量值列名
- ✅ 生成 HTML + Markdown + PDF 三种格式报告
- ✅ 包含方差分量图、交互作用图、箱线图、%GRR仪表盘
- ✅ 自动判定测量系统合格/有条件接受/不合格

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

依赖列表:
```
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.4.0
scipy>=1.7.0
pyyaml>=5.4.0
```

### 2. 编辑YAML配置文件

复制 `spc_config_example.yaml` 为 `spc_config.yaml`，然后编辑:

```yaml
version: "1.0"

# 所有相对路径的基础目录
base_dir: "F:/your/data/directory"

projects:
  - name: "我的项目 - PCBA电压测试"
    id: "my_pcba_voltage_test"        # 唯一标识，用于命令行和API调用
    csv_file: "./test_data.csv"        # 相对于 base_dir 的路径
    output:
      html: "voltage_report.html"
      pdf: "voltage_report.pdf"
    spec_limits:
      # 格式: CSV列名: [LSL下限, USL上限]
      # 列名必须与CSV文件中的列名完全一致
      Voltage_3V3: [3.2, 3.45]
      Voltage_5V0: [4.75, 5.25]
      Current_Idle: [0.038, 0.05]
```

> 💡 详细配置示例请参考 `spc_config_example.yaml`

### 3. 运行程序

```bash
# 处理配置文件中的第一个项目
python spc_analysis.py

# 指定配置文件和项目
python spc_analysis.py --config spc_config.yaml --project my_pcba_voltage_test

# 批量处理多个项目（在Python中循环调用）
from spc_analysis import main
from config_loader import ConfigLoader

loader = ConfigLoader("spc_config.yaml")
for config in loader.get_all_projects():
    main(config=config)
```

### 4. 查看报告

程序会生成:
- `voltage_report.html` — 现代化HTML报告（图片Base64内嵌，自包含）
- `voltage_report.pdf` — 专业PDF报告

---

## 🔬 Cpk反向分析（新增）

与传统的“已知规格限 → 计算Cpk”不同，Cpk反向分析工具支持**已知目标Cpk值 → 反推规格限**。

### 核心原理

根据目标Cpk值，利用数据统计反推合理的规格上下限：

$$
LSL = \mu - 3\sigma \cdot Cpk \qquad USL = \mu + 3\sigma \cdot Cpk
$$

### 命令行使用

```bash
# 基本用法：指定数据文件和目标Cpk值
python cpk_analysis.py --file data.csv --cpk 1.33

# 指定输出目录
python cpk_analysis.py --file data.xlsx --cpk 1.33 --output ./reports

# 指定Excel工作表
python cpk_analysis.py --file data.xlsx --cpk 1.67 --sheet Sheet1
```

### 第三方集成

```python
from spc_statistic import analyze_with_cpk

result = analyze_with_cpk(
    file_path="data.csv",      # 数据文件路径（CSV或Excel）
    target_cpk=1.33,           # 目标Cpk值
    output_dir="./reports"     # 报告输出目录（可选）
)

# 查看结果
for s in result['stats_list']:
    print(f"{s['column']}: LSL={s['lsl']:.4f}, USL={s['usl']:.4f}")
print(f"HTML报告: {result['html_path']}")
print(f"PDF报告: {result['pdf_path']}")
```

### 返回值说明

`analyze_with_cpk()` 返回一个字典，包含：

| 键 | 类型 | 说明 |
|------|------|------|
| `stats_list` | `list[dict]` | 各列的统计结果（含 mean, std, lsl, usl, cpk_achieved 等） |
| `html_path` | `str` | 生成的HTML报告完整路径 |
| `pdf_path` | `str` | 生成的PDF报告完整路径 |
| `file_path` | `str` | 原始数据文件路径 |
| `target_cpk` | `float` | 目标Cpk值 |

---

## 📐 GRR 测量系统分析（新增）

GRR (Gauge Repeatability & Reproducibility) 用于评估测量系统的变异，判断测量系统是否可靠。

### 分析方法

| 方法 | 说明 | 特点 |
|------|------|------|
| **ANOVA** (默认) | 方差分析法 | 分解交互作用、误差分量，更精确 |
| **AIAG** | 均值极差法 | 传统方法，工业界广泛使用 |

### 数据格式

数据文件 (CSV/Excel) 采用长表格式，包含操作员、零件、测量值三列：

```csv
operator,part,value
Operator_A,Part_1,3.35
Operator_A,Part_1,3.34
Operator_A,Part_2,3.32
Operator_B,Part_1,3.36
...
```

> 💡 列名可以自定义，通过 `--operator`、`--part`、`--value` 参数指定

### 命令行使用

```bash
# 基本用法（默认 ANOVA 方法）
python grr_analysis.py --file grr_data.csv

# 使用 AIAG 方法
python grr_analysis.py --file grr_data.csv --method AIAG

# 自定义列名
python grr_analysis.py --file data.xlsx --operator 操作员 --part 零件 --value 测量值

# 指定输出目录
python grr_analysis.py --file grr_data.csv --output ./reports
```

### 第三方集成

```python
from spc_statistic import analyze_grr

result = analyze_grr(
    file_path="grr_data.csv",
    operator_col="operator",   # 操作员列名
    part_col="part",           # 零件列名
    value_col="value",         # 测量值列名
    method="ANOVA",            # 分析方法: 'ANOVA' 或 'AIAG'
    output_dir="./reports"     # 报告输出目录（可选）
)

# 查看结果
r = result['result']
print(f"%GRR: {r['pct_grr']:.2f}%")
print(f"ndc: {r['ndc']}")
print(f"判定: {'✅ 合格' if r['pct_grr'] < 10 else '❌ 不合格'}")
print(f"Markdown报告: {result['markdown_path']}")
print(f"HTML报告: {result['html_path']}")
print(f"PDF报告: {result['pdf_path']}")
```

### 返回值说明

`analyze_grr()` 返回一个字典，包含：

| 键 | 类型 | 说明 |
|------|------|------|
| `result` | `dict` | GRR 分析结果（含 EV, AV, PV, %GRR, ndc 等） |
| `markdown_path` | `str` | Markdown 报告路径 |
| `html_path` | `str` | HTML 报告路径 |
| `pdf_path` | `str` | PDF 报告路径 |

### GRR 判定标准

| %GRR | 判定 | 说明 |
|------|------|------|
| < 10% | ✅ 合格 | 测量系统可接受 |
| 10% ~ 30% | ⚠️ 有条件接受 | 根据应用场景决定 |
| ≥ 30% | ❌ 不合格 | 测量系统需改进 |
| ndc ≥ 5 | ✅ | 足够的分辨力 |
| ndc < 5 | ❌ | 分辨力不足 |

### 规格限对比（新增）

用于验证 CSV 数据文件中的规格限是否与 YAML 配置保持一致，便于质量审核和数据校验。

#### 命令行使用

```bash
# 基本用法
python limits_compare.py --file data.csv --project ehm_pcba_test

# 指定配置文件和输出目录
python limits_compare.py --file data.csv --project ehm_pcba_test --config spc_config.yaml --output ./reports
```

#### 输出

- 控制台打印对比结果（匹配项、差异项、仅CSV项、仅YAML项）
- 生成 Markdown 对比报告（`{datetime}_{project_id}_limits_compare.markdown`）

---

## 📁 项目结构

```
spc_statistic/
├── __init__.py              # 包初始化文件（导出主要API）
├── spc_analysis.py          # 主分析引擎（已知规格限 → 计算Cpk）
├── cpk_analysis.py          # Cpk反向分析（已知Cpk → 反推规格限）
├── grr_analysis.py          # GRR测量系统分析（ANOVA/AIAG方法）
├── limits_compare.py        # 规格限对比工具（CSV vs YAML配置）
├── config_loader.py         # YAML配置加载器（加载、校验、解析配置）
├── spc_statistic.py         # 统一包接口（便于作为模块导入）
├── spc_config.yaml          # YAML多项目配置文件（需自行创建）
├── spc_config_example.yaml  # YAML配置示例模板（可复制为 spc_config.yaml）
├── requirements.txt         # Python依赖列表
├── README.md                # 中文文档
├── README_EN.md             # 英文文档
├── RELEASE_NOTES.md         # 版本发布说明
└── API_INTERFACE.md         # API接口详细说明
```

---

## 📋 YAML配置文件说明

### 配置文件格式

```yaml
version: "1.0"                     # 配置文件版本号

base_dir: "F:/data/project"        # 基础目录
                                   # 所有相对路径都基于此目录解析

projects:                          # 项目列表（可定义任意多个项目）

  - name: "项目显示名称"            # 显示名称（用于GUI下拉框等）
    id: "project_id"               # 唯一标识（用于命令行 --project 参数和API调用）
    csv_file: "./data.csv"         # CSV数据文件路径
                                   # 绝对路径直接使用，相对路径基于 base_dir
    output:
      html: "report.html"          # HTML报告输出路径
      pdf: "report.pdf"            # PDF报告输出路径

    spec_limits:                   # 规格限定义
      # 格式: CSV列名: [LSL下限, USL上限]
      # ⚠️ 列名必须与CSV文件中的列名完全一致（包括大小写）
      Voltage_3V3: [3.2, 3.45]
      Current_Idle: [0.038, 0.05]
```

### 路径解析规则

| 路径类型 | 示例 | 解析结果 |
|---------|------|---------|
| 绝对路径 | `F:/data/test.csv` | 直接使用 |
| 相对路径 | `./test.csv` | `base_dir` + `./test.csv` |

### CSV文件格式要求

- 第一行: 列标题（测试参数名称）
- 后续行: 测试数据
- 支持空值、非数值数据（会自动过滤）

```csv
SerialNumber,Voltage_3V3,Voltage_5V0,Current_Idle,OverallResult
SN001,3.35,5.02,0.042,PASS
SN002,3.33,5.01,0.041,PASS
SN003,3.34,5.03,0.043,PASS
```

---

## 🔌 第三方集成指南

本项目设计为**独立的Python工具包**，提供了清晰的API接口，可以非常方便地集成到PyQt/PySide或其他GUI应用中。

### 核心API

| 模块 | 入口 | 说明 |
|------|------|------|
| `config_loader.py` | `ConfigLoader` | 加载和管理YAML配置 |
| `spc_analysis.py` | `main()` | 已知规格限 → 计算Cpk并生成报告 |
| `cpk_analysis.py` | `analyze_with_cpk()` | 已知目标Cpk → 反推规格限并生成报告 |
| `grr_analysis.py` | `analyze_grr()` | GRR测量系统分析（ANOVA/AIAG）并生成报告 |
| `limits_compare.py` | `main()` | 规格限对比（CSV vs YAML配置）生成Markdown报告 |
| `spc_statistic.py` | 统一导入 | 提供统一的包导入接口 |

### 第一步：将本项目复制到你的工程中

```
your_project/
├── main_app.py              # 你的PyQt/PySide主程序
├── spc_statistic/           # ← 将本项目文件复制到此目录（作为Python包）
│   ├── __init__.py
│   ├── spc_analysis.py
│   ├── cpk_analysis.py
│   ├── config_loader.py
│   ├── spc_statistic.py
│   ├── spc_config.yaml      # 用户可编辑的外部配置文件
│   └── spc_config_example.yaml
└── ...
```

### 第二步：导入并使用

```python
# 方式一：作为包导入（推荐）
from spc_statistic import ConfigLoader, run_spc_analysis, analyze_with_cpk

# 方式二：从子模块导入
from spc_statistic.config_loader import ConfigLoader
from spc_statistic.spc_analysis import main as run_spc_analysis
from spc_statistic.cpk_analysis import analyze_with_cpk
```

### 第三步：获取项目列表（填充下拉框）

```python
from PyQt5.QtWidgets import QComboBox

loader = ConfigLoader("spc_statistic/spc_config.yaml")
loader.load()

combo = QComboBox()
for project_id, project_name in loader.list_projects():
    combo.addItem(project_name, project_id)
```

### 第四步：执行分析（推荐在后台线程中）

```python
from PyQt5.QtCore import QThread, pyqtSignal

class SPCWorker(QThread):
    """后台线程：执行SPC分析，避免阻塞UI"""
    finished = pyqtSignal(str)   # 完成信号
    error = pyqtSignal(str)      # 错误信号

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        try:
            run_spc_analysis(config=self.config)
            self.finished.emit("分析报告已生成！")
        except Exception as e:
            self.error.emit(str(e))

# 使用示例
selected_id = combo.currentData()
config = loader.get_project(selected_id)

worker = SPCWorker(config)
worker.finished.connect(lambda msg: print(msg))
worker.error.connect(lambda err: print(f"错误: {err}"))
worker.start()
```

### 完整集成示例

```python
import sys
sys.path.insert(0, ".")  # 确保 spc_statistic 包的父目录在 Python 路径中

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QComboBox, QLabel, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal
from spc_statistic import ConfigLoader, run_spc_analysis, analyze_with_cpk


class SPCWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        try:
            run_spc_analysis(config=self.config)
            self.finished.emit("分析报告已生成！")
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPC统计分析工具")
        self.resize(400, 200)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 加载配置
        self.loader = ConfigLoader("spc_statistic/spc_config.yaml")
        self.loader.load()

        # 项目选择下拉框
        layout.addWidget(QLabel("选择分析项目:"))
        self.combo = QComboBox()
        for pid, pname in self.loader.list_projects():
            self.combo.addItem(pname, pid)
        layout.addWidget(self.combo)

        # 执行按钮
        self.btn = QPushButton("开始分析")
        self.btn.clicked.connect(self.start_analysis)
        layout.addWidget(self.btn)

        self.status = QLabel("就绪")
        layout.addWidget(self.status)

    def start_analysis(self):
        project_id = self.combo.currentData()
        config = self.loader.get_project(project_id)

        self.worker = SPCWorker(config)
        self.worker.finished.connect(self.on_done)
        self.worker.error.connect(self.on_error)
        self.status.setText("正在分析...")
        self.btn.setEnabled(False)
        self.worker.start()

    def on_done(self, msg):
        self.status.setText(msg)
        self.btn.setEnabled(True)
        QMessageBox.information(self, "完成", msg)

    def on_error(self, err):
        self.status.setText("分析失败")
        self.btn.setEnabled(True)
        QMessageBox.critical(self, "错误", f"分析失败:\n{err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
```

### 错误处理建议

```python
from spc_statistic import ConfigLoader, analyze_with_cpk

# YAML配置模式的错误处理
try:
    loader = ConfigLoader("spc_config.yaml")
    loader.load()
    config = loader.get_project("my_project")
except FileNotFoundError:
    print("配置文件不存在，请检查路径")
except ValueError as e:
    print(f"配置文件格式错误: {e}")
except KeyError:
    print("指定的项目ID不存在")

# Cpk反向分析的错误处理
try:
    result = analyze_with_cpk("data.csv", target_cpk=1.33)
except FileNotFoundError as e:
    print(f"数据文件不存在: {e}")
except ValueError as e:
    print(f"数据文件格式错误: {e}")
```

---

## 🎯 Cpk标准参考

| Cpk值 | 等级 | 说明 |
|-------|------|------|
| Cpk ≥ 1.67 | A级 | 过程能力优秀 |
| 1.33 ≤ Cpk < 1.67 | B级 | 过程能力良好 |
| 1.0 ≤ Cpk < 1.33 | C级 | 过程能力可接受 |
| Cpk < 1.0 | D级 | 过程能力不足 |

---

## ❓ 常见问题

### Q: 提示找不到列？
A: 检查 `spec_limits` 中的参数名是否与CSV列名**完全一致**（包括大小写和下划线）。

### Q: 某些测试项没有生成图表？
A: 检查CSV中该列是否有有效的数值数据。空值或非数值会被自动过滤。

### Q: 如何只分析部分参数？
A: 在YAML配置文件的 `spec_limits` 中注释掉不需要的参数（行前加 `#`）。

### Q: 支持单边规格吗？
A: 当前版本支持双边规格。如需单边规格，可将另一侧设为极大/极小值。

### Q: 打包为exe后如何让用户修改配置？
A: 将 `spc_config.yaml` 放在exe同级目录，用户可直接用文本编辑器修改。程序启动时自动读取。

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📞 联系方式

- 作者: SimonYuan
- 网站: https://tresordie.github.io/

## 🙏 致谢

- [Pandas](https://pandas.pydata.org/) - 数据处理
- [Matplotlib](https://matplotlib.org/) - 图表绘制
- [NumPy](https://numpy.org/) - 数值计算
- [SciPy](https://scipy.org/) - 统计分析

---

⭐ 如果这个项目对你有帮助，请给个Star!
