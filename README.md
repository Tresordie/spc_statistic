# SPC统计分析工具 v2.0

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> 现代化的统计过程控制(SPC)分析工具,自动生成整洁优美的HTML和PDF报告

**简体中文** | [English](README_EN.md)

## 📖 项目简介

SPC (Statistical Process Control) 统计分析工具是一个用于制造业质量控制的Python应用程序。它能够:

- 📊 自动计算Cpk、Mean、Sigma等关键统计指标
- 🎨 生成现代化的HTML报告(响应式设计,渐变背景,卡片布局)
- 📄 生成专业的PDF报告(A4尺寸,表格分页,300 DPI高清输出)
- 📈 绘制直方图和正态分布拟合曲线
- 🎯 智能Cpk彩色标识(优秀/可接受/不合格)
- 🔄 支持批量处理多个CSV文件

## ✨ 功能特性

### 统计分析
- ✅ 自动计算Cpk过程能力指数
- ✅ 计算均值(Mean)和标准差(Sigma)
- ✅ 直方图与正态分布曲线拟合
- ✅ 规格限(USL/LSL)可视化
- ✅ 样本数量统计

### 报告生成
- ✅ **HTML报告**:
  - 现代化渐变背景
  - 响应式卡片布局
  - 统计概览仪表板
  - Cpk值彩色标识
  - 悬停动画效果
  - 适配桌面/平板/手机

- ✅ **PDF报告**:
  - A4标准纸张尺寸
  - 表格自动分页(每页20行)
  - 专业配色方案
  - 智能文本换行
  - 300 DPI高清输出
  - 每个参数独立分布图

### 配置灵活
- ✅ 配置与代码完全分离
- ✅ 只需修改一个配置文件
- ✅ 支持任意数量测试项目
- ✅ 自动处理缺失数据
- ✅ 批量处理多个文件

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install pandas numpy matplotlib scipy
```

### 2. 配置测试项目

编辑 `spc_config.py` 文件:

```python
# 设置CSV文件路径
CSV_FILE_PATH = "./your_test_data.csv"

# 定义测试项目和规格限
SPEC_LIMITS = {
    "VCC_3V3": (3.2, 3.45),        # 3.3V电源,下限3.2V,上限3.45V
    "VCC_5V0": (4.75, 5.25),       # 5V电源
    "Current_Idle": (0.038, 0.05), # 待机电流
    # 添加更多测试项...
}
```

### 3. 运行程序

```bash
# 单文件处理
python spc_analysis.py

# 批量处理
python batch_process.py
```

### 4. 查看报告

程序会生成:
- `spc_report.html` - 现代化HTML报告
- `spc_report.pdf` - 专业PDF报告
- `spc_report_images/` - 分布图图片目录

## 📁 项目结构

```
spc_generation/
├── spc_config.py              # 配置文件(定义测试项目和规格限)
├── spc_config_example.py      # 配置示例和模板
├── spc_analysis.py            # 主程序(生成报告)
├── batch_process.py           # 批量处理工具
├── spc_report_styles.py       # 样式模块(可选)
├── README.md                  # 中文使用说明
├── README_EN.md              # 英文使用说明
└── [旧版脚本]                 # 保留作为参考
```

## 📋 使用说明

### 配置文件说明

#### spc_config.py

主要配置项:

```python
# CSV文件路径
CSV_FILE_PATH = "./data.csv"

# 输出文件配置
OUTPUT_HTML = "report.html"
OUTPUT_PDF = "report.pdf"
OUTPUT_IMG_DIR = "report_images"

# 规格限定义
SPEC_LIMITS = {
    "测试项目名称": (下限LSL, 上限USL),
}
```

#### 添加测试项目

```python
SPEC_LIMITS = {
    # 电压测试
    "Voltage_3V3": (3.2, 3.45),
    "Voltage_5V0": (4.75, 5.25),
    
    # 电流测试
    "Current_Idle": (0.038, 0.05),
    "Current_Active": (0.15, 0.25),
    
    # 温度测试
    "Temperature": (20, 80),
    
    # 添加更多...
}
```

**注意**: 测试项目名称必须与CSV文件中的列名完全一致(包括大小写)。

### CSV文件格式

CSV文件应包含:
- 第一行: 列标题(测试项目名称)
- 后续行: 测试数据
- 支持空值、非数值数据(会自动过滤)

示例:

```csv
SerialNumber,VCC_3V3,VCC_5V0,Current_Idle,OverallResult
SN001,3.35,5.02,0.042,PASS
SN002,3.33,5.01,0.041,PASS
SN003,3.34,5.03,0.043,PASS
```

### 批量处理

编辑 `batch_process.py`:

```python
csv_files = [
    "./data_batch1.csv",
    "./data_batch2.csv",
    "./data_batch3.csv",
]

# 或自动扫描目录
import glob
csv_files = glob.glob("./data/*.csv")
```

运行:

```bash
python batch_process.py
```

所有报告将保存在 `batch_reports/` 目录。

## 📊 报告示例

### HTML报告特性

- **页眉**: 渐变色标题和说明
- **统计概览卡片**:
  - 总参数数量
  - 总样本数量
  - Cpk ≥ 1.33 (优秀) 数量
  - 1.0 ≤ Cpk < 1.33 (可接受) 数量
- **统计表格**: 响应式表格,Cpk值彩色显示
- **分布图网格**: 自适应网格布局

### PDF报告特性

- **统计表格页**: 自动分页,专业排版
- **分布图页**: 每个参数一页,A4尺寸高清输出
- **配色方案**: 深灰蓝色表头,交替行颜色
- **高清输出**: 300 DPI分辨率

## 🔧 高级用法

### 自定义样式

编辑 `spc_analysis.py` 中的函数:

- `plot_histogram_with_modern_style()` - 图表样式
- `generate_pdf_report()` - PDF排版
- `generate_html_report()` - HTML样式

### 多项目配置

为不同项目创建独立配置文件:

```bash
# 项目A
cp spc_config.py spc_config_project_a.py

# 项目B
cp spc_config.py spc_config_project_b.py

# 修改 spc_analysis.py 导入对应配置
# from spc_config_project_a import ...
```

### 集成到CI/CD

```yaml
# GitHub Actions 示例
- name: Generate SPC Report
  run: |
    pip install pandas numpy matplotlib scipy
    python spc_analysis.py
```

## 📝 依赖项

```
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.4.0
scipy>=1.7.0
```

安装:

```bash
pip install -r requirements.txt
```

或手动安装:

```bash
pip install pandas numpy matplotlib scipy
```

## 🎯 Cpk标准参考

| Cpk值 | 等级 | 说明 |
|-------|------|------|
| Cpk ≥ 1.67 | A级 | 过程能力优秀 |
| 1.33 ≤ Cpk < 1.67 | B级 | 过程能力良好 |
| 1.0 ≤ Cpk < 1.33 | C级 | 过程能力可接受 |
| Cpk < 1.0 | D级 | 过程能力不足 |

## ❓ 常见问题

### Q: 提示找不到列?
A: 检查 `SPEC_LIMITS` 中的测试项目名称是否与CSV列名完全一致(包括大小写和下划线)。

### Q: 某些测试项没有生成图表?
A: 检查CSV中该列是否有有效的数值数据。空值或非数值会被自动过滤。

### Q: 如何只测试部分项目?
A: 在 `SPEC_LIMITS` 中注释掉不需要的项目(在行前加 `#`)。

### Q: 支持单边规格吗?
A: 当前版本支持双边规格。如需单边规格,请设置另一侧为极大/极小值。

### Q: 如何修改报告标题?
A: 编辑 `spc_analysis.py` 中 `generate_html_report()` 和 `generate_pdf_report()` 函数的标题文本。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📞 联系方式

- 作者: SimonYuan
- 网站: https://tresordie.github.io/
- Email: [your-email@example.com]

## 🙏 致谢

- [Pandas](https://pandas.pydata.org/) - 数据处理
- [Matplotlib](https://matplotlib.org/) - 图表绘制
- [NumPy](https://numpy.org/) - 数值计算
- [SciPy](https://scipy.org/) - 统计分析

## 📊 版本历史

- **v2.0** (2026-06-17)
  - ✨ 配置与代码分离
  - 🎨 现代化报告设计
  - 📱 响应式HTML布局
  - 📄 专业PDF排版
  - 🔄 批量处理支持

- **v1.0** (2026-05-04)
  - 🎉 初始版本发布
  - 📊 基础统计计算
  - 📈 简单图表生成

---

⭐ 如果这个项目对你有帮助,请给个Star!
