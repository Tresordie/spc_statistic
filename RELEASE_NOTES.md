# SPC统计分析工具 - 发布说明

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
