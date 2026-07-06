# -*- encoding: utf-8 -*-
"""
SPC统计分析工具包

本包提供SPC统计分析和报告生成功能，可集成到PyQt/PySide等GUI应用中。

主要模块:
    config_loader  - YAML配置加载器（加载、校验、解析YAML配置文件）
    spc_analysis   - SPC分析引擎（计算统计量、生成HTML/PDF报告）
    cpk_analysis   - Cpk反向分析工具（根据目标Cpk值计算规格限）
    grr_analysis   - GRR测量系统分析（ANOVA/AIAG方法，生成HTML/MD/PDF报告）

使用方式:
    from spc_statistic import ConfigLoader, run_spc_analysis
    # 或者
    from spc_statistic.config_loader import ConfigLoader
    from spc_statistic.spc_analysis import main as run_spc_analysis
"""

from .config_loader import ConfigLoader, ProjectConfig, ProjectOutputConfig, SPCConfig
from .spc_analysis import main as run_spc_analysis
from .cpk_analysis import analyze_with_cpk
from .grr_analysis import analyze_grr, analyze_grr_wide, convert_wide_to_long

__all__ = [
    "ConfigLoader",
    "ProjectConfig",
    "ProjectOutputConfig",
    "SPCConfig",
    "run_spc_analysis",
    "analyze_with_cpk",
    "analyze_grr",
    "analyze_grr_wide",
    "convert_wide_to_long",
]
