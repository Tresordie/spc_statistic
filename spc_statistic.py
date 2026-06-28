"""
SPC统计分析工具包

这是一个用于制造业质量控制的统计过程控制(SPC)分析工具。
它能够自动计算Cpk、Mean、Sigma等关键统计指标，并生成现代化的HTML和PDF报告。

主要模块：
- spc_analysis: 主分析引擎，包含核心的数据分析和报告生成功能
- config_loader: 配置管理模块，负责加载和解析YAML格式的配置文件

集成说明：
此包专为集成到PyQt/PySide GUI应用而设计，提供了清晰的API接口。
"""

__version__ = "2.1"
__author__ = "SimonYuan"
__email__ = "tresordie@163.com"

# 导出主要接口
try:
    from config_loader import (
        ConfigLoader,
        ProjectConfig,
        ProjectOutputConfig,
        SPCConfig,
    )
    from spc_analysis import main as run_spc_analysis
except ImportError:
    from .config_loader import (
        ConfigLoader,
        ProjectConfig,
        ProjectOutputConfig,
        SPCConfig,
    )
    from .spc_analysis import main as run_spc_analysis

__all__ = [
    "run_spc_analysis",
    "ConfigLoader",
    "ProjectConfig",
    "ProjectOutputConfig",
    "SPCConfig",
]
