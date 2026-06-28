# SPC统计分析工具 v2.1

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> 现代化的统计过程控制(SPC)分析工具，自动生成优美的HTML和PDF报告。  
> 支持YAML外部配置多项目管理，可轻松集成到PyQt/PySide等GUI应用。

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
      img_dir: "voltage_images"
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
- `voltage_report.html` — 现代化HTML报告
- `voltage_report.pdf` — 专业PDF报告
- `voltage_images/` — 分布图图片目录

---

## 📁 项目结构

```
spc_statistic/
├── spc_analysis.py          # 主分析引擎（计算统计量、生成报告）
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
      img_dir: "report_images"     # 分布图输出目录

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
| `spc_analysis.py` | `main()` | 执行SPC分析并生成报告 |
| `spc_statistic.py` | 统一导入 | 提供统一的包导入接口 |

### 第一步：将本项目复制到你的工程中

```
your_project/
├── main_app.py              # 你的PyQt/PySide主程序
├── spc_module/              # ← 将本项目文件复制到此目录
│   ├── spc_analysis.py
│   ├── config_loader.py
│   ├── spc_statistic.py
│   ├── spc_config.yaml      # 用户可编辑的外部配置文件
│   └── spc_config_example.yaml
└── ...
```

### 第二步：导入并使用

```python
import sys
sys.path.insert(0, "spc_module")  # 将SPC模块目录加入Python路径

from spc_analysis import main as run_spc_analysis
from config_loader import ConfigLoader
```

### 第三步：获取项目列表（填充下拉框）

```python
from PyQt5.QtWidgets import QComboBox

loader = ConfigLoader("spc_module/spc_config.yaml")
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
sys.path.insert(0, "spc_module")

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QComboBox, QLabel, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal
from spc_analysis import main as run_spc_analysis
from config_loader import ConfigLoader


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
        self.loader = ConfigLoader("spc_module/spc_config.yaml")
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
from config_loader import ConfigLoader

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
