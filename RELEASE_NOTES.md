# SPC统计分析工具 - 发布说明

## v2.4 (2026-07-06) - 规格限对比工具 & 报告优化

### ✨ 新增功能
- **limits_compare.py** — 全新的规格限对比工具
  - 将 CSV 文件中的 TEST_NAME 对应的 LOWER_LIMIT / UPPER_LIMIT 与 YAML 配置中相同 project id 的 spec_limits 进行逐项对比
  - 自动识别匹配项、差异项、仅 CSV 项、仅 YAML 项
  - 生成带时间戳的 **Markdown** 对比报告（`{datetime}_{project_id}_limits_compare.markdown`）
  - 支持 `--output` 参数指定报告输出目录
- **命令行接口** — `python limits_compare.py --file data.csv --project ehm_pcba_test`

### 🔧 功能改进
- **HTML 报告自包含** — `spc_analysis.py` 的 HTML 报告现在将图片以 Base64 内嵌，发送给他人时无需附带图片文件夹
- **GRR 报告增强** — 新增 %EV（%Repeatability）、%AV（%Reproducibility）、%GRR（%Gage R&R）三个百分比指标，在 HTML 和 Markdown 报告中显示
- **移除 img_dir** — 所有模块不再生成独立的图片文件夹，图片全部内嵌到 HTML 中
- **Windows 兼容性** — 添加控制台 UTF-8 编码设置，解决 emoji 和中文在 PowerShell 中的显示问题

### 📁 文件结构变化
- `limits_compare.py` — 新增规格限对比工具
- `spc_config.yaml` — 移除所有项目的 `img_dir` 配置项
- `spc_config_example.yaml` — 移除示例中的 `img_dir` 配置项
- `config_loader.py` — `ProjectOutputConfig` 移除 `img_dir` 字段

### 📊 报告输出变化
| 修改前 | 修改后 |
|--------|--------|
| HTML + PDF + 图片文件夹 | HTML + PDF（图片 Base64 内嵌） |
| 发送时需附带图片文件夹 | 仅需发送 HTML 和 PDF 两个文件 |

---

## v2.3 (2026-06-28) - GRR 测量系统分析

### ✨ 新增功能
- **grr_analysis.py** — 全新的 GRR (Gauge Repeatability & Reproducibility) 测量系统分析工具
  - 支持 **ANOVA 方差分析法** — 分解交互作用、误差分量，更精确
  - 支持 **AIAG 均值极差法** — 传统方法，工业界广泛使用
  - 自动计算 EV(设备变异)、AV(人员变异)、PV(零件变异) 等分量
  - 计算 %GRR、ndc(可区分类别数) 等关键指标
  - 生成 **Markdown** 报告（研究概要 + ANOVA表 + 判定标准）
  - 生成 **HTML** 报告（渐变卡片布局、%GRR 仪表盘、方差分量图、交互作用图、箱线图）
  - 生成 **PDF** 报告（A4尺寸、封面汇总表、300 DPI 高清输出）
- **analyze_grr()** — 统一主函数，一行代码完成 GRR 分析并生成三种格式报告
- **命令行接口** — `python grr_analysis.py --file grr_data.csv --method ANOVA`
- **PyQt/PySide集成** — `from spc_statistic import analyze_grr` 即可调用
- **灵活数据格式** — 支持自定义操作员/零件/测量值列名

### 📊 GRR 判定标准
| %GRR | 判定 |
|------|------|
| < 10% | ✅ 合格 — 测量系统可接受 |
| 10% ~ 30% | ⚠️ 有条件接受 — 根据应用场景决定 |
| ≥ 30% | ❌ 不合格 — 测量系统需改进 |
| ndc ≥ 5 | ✅ 足够的分辨力 |
| ndc < 5 | ❌ 分辨力不足 |

### 📁 文件结构变化
- `grr_analysis.py` — 新增 GRR 测量系统分析工具

---

## v2.2 (2026-06-28) - Cpk反向分析工具

### ✨ 新增功能
- **cpk_analysis.py** — 全新分析模式：根据目标Cpk值反向推导规格上下限
  - 核心公式: `LSL = μ - 3σ·Cpk`，`USL = μ + 3σ·Cpk`
  - 支持 CSV 和 Excel (.xlsx/.xls) 数据文件
  - 支持指定 Excel 工作表名称
  - 自动识别所有数值列，无需手动配置规格限
  - 生成现代化 HTML 报告（响应式卡片布局、内嵌直方图）
  - 生成专业 PDF 报告（A4尺寸、封面汇总表、每页2张图表）
- **analyze_with_cpk()** — 统一主函数，一行代码完成分析并返回结果字典
- **命令行接口** — `python cpk_analysis.py --file data.csv --cpk 1.33`
- **PyQt/PySide集成** — `from spc_statistic import analyze_with_cpk` 即可调用

### 🔧 功能改进
- **包导入修复** — `spc_analysis.py` 导入改为 try/except 兼容模式，同时支持包内导入和直接运行
- **__init__.py** — 新增包初始化文件，导出 `ConfigLoader`、`run_spc_analysis`、`analyze_with_cpk`
- **中文字体配置** — 自动适配 Windows/macOS/Linux 中文字体

### 📁 文件结构变化
- `cpk_analysis.py` — 新增 Cpk 反向分析工具
- `__init__.py` — 新增包初始化文件（使 spc_statistic 成为正式 Python 包）

---

## v2.1 (2026-06-28) - 增强版集成支持

### ✨ 新增功能
- **PyQt/PySide集成优化** — 提供专门针对GUI应用的集成接口，包含完整的PyQt5集成示例
- **YAML配置系统** — 支持多项目配置管理，便于在GUI中切换不同项目
- **ConfigLoader类** — 便捷的配置加载和管理工具，支持项目列表查询（`list_projects()`）
- **API增强** — `main()` 函数支持直接传入 `ProjectConfig` 对象，无需命令行参数
- **统一包接口** — 新增 `spc_statistic.py`，提供统一的模块导入入口

### 🔧 功能改进
- **配置管理** — 将原来的单项目Python配置（`spc_config.py`）升级为多项目YAML配置系统
- **代码注释** — 为所有模块添加详细的类型提示、参数说明、使用示例和集成指南
- **文档完善** — 全面重写中英文README，增加第三方集成完整指南
- **错误处理** — 改进错误处理机制，便于GUI应用捕获和显示错误
- **旧文件清理** — 删除已废弃的 `spc_config.py`、`spc_config_example.py` 和 `limits_specified_plot_deepseek_ehm_pcba_test.py`

### 📚 集成说明
- **快速集成** — 使用 `from spc_analysis import main` 即可集成核心功能
- **项目切换** — 通过 `ConfigLoader.list_projects()` 方法获取项目列表，填充GUI下拉框
- **后台运行** — 支持在 `QThread` 中运行分析以避免UI阻塞
- **类型安全** — 提供完整的类型提示支持（`ProjectConfig`、`ProjectOutputConfig` 等数据类）

### 📁 文件结构变化
- `config_loader.py` — 新增配置加载器
- `spc_config.yaml` — 新增多项目YAML配置文件
- `spc_config_example.yaml` — 新增配置示例模板
- `spc_statistic.py` — 新增统一包接口
- `API_INTERFACE.md` — 新增API接口详细说明
- `requirements.txt` — 新增依赖列表（含 pyyaml）
- ~~`spc_config.py`~~ — 已删除（由YAML替代）
- ~~`spc_config_example.py`~~ — 已删除（由YAML替代）
- ~~`batch_process.py`~~ — 已删除（批量处理直接在Python中循环调用 `main()` 即可）
- ~~`limits_specified_plot_deepseek_ehm_pcba_test.py`~~ — 已删除（旧版遗留脚本）

---

## v2.0 (2026-06-17) - 现代化报告版

### ✨ 新增功能
- **现代化HTML报告** — 渐变背景、响应式卡片布局、悬停动画效果
- **专业PDF报告** — A4尺寸、表格分页、300 DPI高清输出
- **智能Cpk标识** — 根据数值自动显示颜色和符号（✓/⚠/✗）
- **批量处理支持** — 一键处理多个项目
- **长参数名换行** — 自动处理超长参数名称

### 📊 统计分析增强
- **Cpk计算** — 支持过程能力指数计算
- **正态分布拟合** — 自动拟合数据分布曲线
- **规格限可视化** — 直观显示上下限和均值线

---

## v1.0 (2026-05-04) - 初始版本

### 🎉 基础功能
- **基础统计计算** — Cpk、Mean、Sigma等指标
- **简单图表生成** — 基础直方图和分布图
- **CSV数据处理** — 自动解析和清理数据
