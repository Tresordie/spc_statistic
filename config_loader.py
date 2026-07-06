# -*- encoding: utf-8 -*-
"""
@File    :   config_loader.py
@Time    :   2026/06/28
@Author  :   SimonYuan
@Version :   1.1
@Desc    :   YAML配置加载器 - 加载、校验、解析spc_config.yaml

本模块定义了SPC分析所需的全部配置数据结构，并提供 ConfigLoader 类来
从YAML文件中加载、校验和解析这些配置。

数据类层次结构:
    SPCConfig                       # 顶层配置（包含版本号、基础目录和项目列表）
    ├── ProjectConfig               # 单个项目的完整配置
    │   ├── name: str               # 项目显示名称
    │   ├── id: str                 # 项目唯一标识
    │   ├── csv_file: str           # CSV数据文件路径
    │   ├── output: ProjectOutputConfig  # 输出路径配置
    │   │   ├── html: str           # HTML报告输出路径
    │   │   └── pdf: str            # PDF报告输出路径
    │   └── spec_limits: dict       # {参数名: (LSL, USL)} 规格限
    └── projects: list[ProjectConfig]

命令行使用:
    本模块不直接作为命令行入口，但可配合 spc_analysis.py 使用:
    python spc_analysis.py --config spc_config.yaml --project ehm_module_test

第三方集成（PyQt/PySide等）:
    from config_loader import ConfigLoader

    loader = ConfigLoader("spc_config.yaml")
    loader.load()                          # 加载并解析配置文件
    projects = loader.list_projects()      # [(id, name), ...] 用于填充下拉框
    config = loader.get_project("ehm_module_test")  # 获取指定项目配置
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import yaml


@dataclass
class ProjectOutputConfig:
    """
    单个项目的输出路径配置。

    属性:
        html    : str  生成的HTML报告文件路径（绝对路径，图片以Base64内嵌）
        pdf     : str  生成的PDF报告文件路径（绝对路径）

    YAML对应字段:
        output:
          html: "report.html"
          pdf: "report.pdf"
    """

    html: str     # 输出HTML文件路径
    pdf: str      # 输出PDF文件路径


@dataclass
class ProjectConfig:
    """
    单个项目的完整配置。

    属性:
        name        : str                          项目显示名称（如 "EHM PCBA test"）
        id          : str                          项目唯一标识（如 "ehm_pcba_test"）
        csv_file    : str                          CSV数据文件的绝对路径
        output      : ProjectOutputConfig          输出路径配置
        spec_limits : Dict[str, Tuple[float, float]]
                    规格限字典，格式为 {参数名: (LSL下限, USL上限)}
                    参数名必须与CSV文件中的列名完全一致

    YAML对应字段:
        - name: "EHM PCBA test"
          id: "ehm_pcba_test"
          csv_file: "./data.csv"
          output: { html: ..., pdf: ... }
          spec_limits:
            VCC_3V3: [3.2, 3.45]
            VCC_5V0: [4.75, 5.25]
    """

    name: str                                       # 项目显示名称
    id: str                                         # 项目唯一标识
    csv_file: str                                   # CSV数据文件路径
    output: ProjectOutputConfig                     # 输出路径配置
    spec_limits: Dict[str, Tuple[float, float]]     # {参数名: (LSL, USL)}


@dataclass
class SPCConfig:
    """
    顶层配置，对应一个完整的YAML配置文件。

    属性:
        version  : str                配置文件版本号（如 "1.0"）
        base_dir : str                基础目录，用于解析相对路径
        projects : List[ProjectConfig] 所有项目的配置列表
    """

    version: str                     # 配置文件版本号
    base_dir: str                    # 基础目录（用于解析相对路径）
    projects: List[ProjectConfig]    # 项目列表


class ConfigLoader:
    """
    YAML配置加载器。

    负责读取YAML文件、校验格式、解析为结构化的配置对象。
    支持绝对路径和相对路径（相对路径基于YAML中的 base_dir 字段解析）。

    典型用法:
        loader = ConfigLoader("spc_config.yaml")
        spc_config = loader.load()          # 加载并解析
        project = loader.get_project("ehm_module_test")  # 按ID获取项目

    异常:
        FileNotFoundError : 配置文件不存在
        ValueError        : 配置文件为空或格式错误
    """

    DEFAULT_CONFIG_FILENAME = "spc_config.yaml"

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化加载器

        参数:
            config_path: YAML配置文件路径。
                         若为None，则在脚本所在目录查找默认文件名。
        """
        if config_path is None:
            # 默认在脚本同级目录查找
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, self.DEFAULT_CONFIG_FILENAME)

        self._config_path = config_path
        self._config: Optional[SPCConfig] = None

    @property
    def config_path(self) -> str:
        """返回配置文件路径"""
        return self._config_path

    def load(self) -> SPCConfig:
        """
        加载并解析YAML配置文件

        返回: SPCConfig 对象
        异常: FileNotFoundError, ValueError(格式错误)
        """
        if not os.path.exists(self._config_path):
            raise FileNotFoundError(f"配置文件不存在: {self._config_path}")

        with open(self._config_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        if raw is None:
            raise ValueError(f"配置文件为空: {self._config_path}")

        self._config = self._parse_config(raw)
        return self._config

    def _parse_config(self, raw: dict) -> SPCConfig:
        """
        解析原始YAML字典为结构化 SPCConfig 对象。

        参数:
            raw : dict
                yaml.safe_load() 返回的原始字典

        返回:
            SPCConfig 对象

        异常:
            ValueError : 缺少 projects 字段或项目格式错误
        """
        version = str(raw.get("version", "1.0"))
        base_dir = raw.get("base_dir", "")

        projects_raw = raw.get("projects", [])
        if not projects_raw:
            raise ValueError("配置文件中没有定义任何项目(projects为空)")

        projects = []
        for idx, proj_raw in enumerate(projects_raw):
            try:
                project = self._parse_project(proj_raw, base_dir)
                projects.append(project)
            except (KeyError, ValueError) as e:
                proj_name = proj_raw.get("name", f"#{idx + 1}")
                raise ValueError(f"项目 '{proj_name}' 配置错误: {e}") from e

        return SPCConfig(version=version, base_dir=base_dir, projects=projects)

    def _parse_project(self, raw: dict, base_dir: str) -> ProjectConfig:
        """
        解析单个项目的YAML字典为 ProjectConfig 对象。

        参数:
            raw      : dict  单个项目的原始字典（YAML中 projects 列表的一个元素）
            base_dir : str   基础目录，用于解析相对路径

        返回:
            ProjectConfig 对象

        异常:
            KeyError   : 缺少必需字段（csv_file / output / spec_limits）
            ValueError : 字段格式不正确
        """
        name = raw.get("name", "")
        # 若未指定id，则用name中的空格替换为下划线作为默认id
        proj_id = raw.get("id", name.replace(" ", "_"))
        csv_file = self._resolve_path(raw["csv_file"], base_dir)

        output_raw = raw.get("output", {})
        if not output_raw:
            raise ValueError("缺少 output 配置")

        output = ProjectOutputConfig(
            html=self._resolve_path(output_raw["html"], base_dir),
            pdf=self._resolve_path(output_raw["pdf"], base_dir),
        )

        spec_limits_raw = raw.get("spec_limits", {})
        if not spec_limits_raw:
            raise ValueError("缺少 spec_limits 配置")

        spec_limits = {}
        for param_name, limits in spec_limits_raw.items():
            if not isinstance(limits, (list, tuple)) or len(limits) != 2:
                raise ValueError(
                    f"参数 '{param_name}' 的规格限格式错误，"
                    f"需要 [LSL, USL] 格式，实际为: {limits}"
                )
            spec_limits[str(param_name)] = (float(limits[0]), float(limits[1]))

        return ProjectConfig(
            name=name,
            id=proj_id,
            csv_file=csv_file,
            output=output,
            spec_limits=spec_limits,
        )

    @staticmethod
    def _resolve_path(path: str, base_dir: str) -> str:
        """
        解析路径：绝对路径直接使用，相对路径基于base_dir拼接

        规则:
            - 绝对路径（如 F:/data/xxx 或 C:\\data\\xxx）直接使用
            - 其他视为相对路径，拼接 base_dir
        """
        if os.path.isabs(path):
            return os.path.normpath(path)
        if base_dir:
            return os.path.normpath(os.path.join(base_dir, path))
        return os.path.normpath(path)

    # ---- 便捷查询方法 ----

    def get_project(self, project_id: str) -> ProjectConfig:
        """
        按id获取单个项目配置

        参数:
            project_id: 项目唯一标识

        返回: ProjectConfig 对象
        异常: KeyError(项目不存在)
        """
        if self._config is None:
            self.load()
        for proj in self._config.projects:
            if proj.id == project_id:
                return proj
        raise KeyError(f"未找到项目: {project_id}")

    def get_project_by_name(self, name: str) -> ProjectConfig:
        """
        按name获取单个项目配置

        参数:
            name: 项目显示名称

        返回: ProjectConfig 对象
        异常: KeyError(项目不存在)
        """
        if self._config is None:
            self.load()
        for proj in self._config.projects:
            if proj.name == name:
                return proj
        raise KeyError(f"未找到项目: {name}")

    def list_projects(self) -> List[Tuple[str, str]]:
        """
        列出所有项目的 (id, name) 对
        专门用于PyQt5/PySide的ComboBox填充

        返回: [(project_id, project_name), ...]
        
        集成说明:
            此方法特别适合用于填充GUI中的项目选择下拉框。在PyQt/PySide应用中，
            可以直接使用此方法的返回值来填充QComboBox控件。
        """
        if self._config is None:
            self.load()
        return [(p.id, p.name) for p in self._config.projects]

    def get_all_projects(self) -> List[ProjectConfig]:
        """
        获取所有项目配置列表。

        返回:
            List[ProjectConfig]  所有项目的配置对象列表
        """
        if self._config is None:
            self.load()
        return self._config.projects
