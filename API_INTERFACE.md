# SPC统计分析工具 - API接口说明

## 概述

SPC统计分析工具提供了一套简洁的API，便于集成到PyQt/PySide或其他Python应用中。主要通过`spc_analysis.py`和`config_loader.py`两个模块提供功能。

## 核心模块

### 1. spc_analysis 模块

这是主要的分析引擎模块，包含核心的数据分析和报告生成功能。

#### 主要函数

**`main(config: ProjectConfig = None, config_yaml: str = None, project_id: str = None)`**

主分析函数，执行完整的SPC分析流程。

- **参数**：
  - `config` (ProjectConfig, 可选): 直接传入项目配置对象，推荐在GUI应用中使用
  - `config_yaml` (str, 可选): YAML配置文件路径
  - `project_id` (str, 可选): 项目ID，与config_yaml配合使用

- **功能**：
  - 读取CSV数据
  - 计算统计指标(Cpk、Mean、Sigma等)
  - 生成HTML和PDF报告
  - 生成分布图

- **示例**：
```python
from spc_analysis import main
from config_loader import ConfigLoader

# 方法1：直接传入配置对象
loader = ConfigLoader("spc_config.yaml")
project_config = loader.get_project("ehm_module_test")
main(config=project_config)

# 方法2：通过文件路径和项目ID
main(config_yaml="spc_config.yaml", project_id="ehm_module_test")
```

### 2. config_loader 模块

配置管理模块，负责加载和解析YAML格式的配置文件。

#### 主要类

**`ConfigLoader(config_path: Optional[str] = None)`**

YAML配置加载器类。

- **构造函数参数**：
  - `config_path` (str, 可选): 配置文件路径，默认为"spc_config.yaml"

- **主要方法**：

  **`load() -> SPCConfig`**
  - 加载并解析YAML配置文件
  - 返回SPCConfig对象

  **`get_project(project_id: str) -> ProjectConfig`**
  - 按ID获取项目配置
  - 参数：project_id - 项目唯一标识符
  - 返回：ProjectConfig对象

  **`get_project_by_name(name: str) -> ProjectConfig`**
  - 按名称获取项目配置
  - 参数：name - 项目显示名称
  - 返回：ProjectConfig对象

  **`list_projects() -> List[Tuple[str, str]]`**
  - 获取所有项目列表
  - 返回：[(项目ID, 项目名称), ...]
  - **特别适用于GUI应用填充ComboBox**

  **`get_all_projects() -> List[ProjectConfig]`**
  - 获取所有项目配置列表
  - 返回：ProjectConfig对象列表

- **示例**：
```python
from config_loader import ConfigLoader

# 初始化加载器
loader = ConfigLoader("spc_config.yaml")

# 加载配置
config = loader.load()

# 获取项目列表（用于GUI下拉框）
projects = loader.list_projects()
for proj_id, proj_name in projects:
    print(f"ID: {proj_id}, Name: {proj_name}")

# 获取特定项目配置
project = loader.get_project("ehm_module_test")
```

#### 数据类

**`ProjectConfig`**
- `name` (str): 项目显示名称
- `id` (str): 项目唯一标识
- `csv_file` (str): CSV数据文件路径
- `output` (ProjectOutputConfig): 输出配置
- `spec_limits` (Dict[str, Tuple[float, float]]): 规格限制，格式为{参数名: (LSL, USL)}

**`ProjectOutputConfig`**
- `html` (str): HTML输出文件路径
- `pdf` (str): PDF输出文件路径
- `img_dir` (str): 图片输出目录

## 集成最佳实践

### 1. PyQt/PySide集成示例

```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from spc_analysis import main
from config_loader import ConfigLoader

class SPCAnalyzerThread(QThread):
    """SPC分析线程，避免阻塞UI"""
    finished = pyqtSignal(str)  # 完成信号
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def run(self):
        try:
            main(config=self.config)
            self.finished.emit("分析完成！")
        except Exception as e:
            self.finished.emit(f"分析失败: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("SPC统计分析工具")
        self.setGeometry(100, 100, 400, 300)
        
        # 初始化组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 项目选择下拉框
        self.project_combo = QComboBox()
        self.load_projects()
        layout.addWidget(QLabel("选择项目:"))
        layout.addWidget(self.project_combo)
        
        # 分析按钮
        self.analyze_btn = QPushButton("开始分析")
        self.analyze_btn.clicked.connect(self.start_analysis)
        layout.addWidget(self.analyze_btn)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        layout.addWidget(self.status_label)
        
        # 加载配置
        self.loader = ConfigLoader("spc_config.yaml")
        
    def load_projects(self):
        """加载项目到下拉框"""
        projects = self.loader.list_projects()
        for proj_id, proj_name in projects:
            self.project_combo.addItem(proj_name, proj_id)
    
    def start_analysis(self):
        """开始分析"""
        # 获取选中的项目ID
        current_index = self.project_combo.currentIndex()
        project_id = self.project_combo.itemData(current_index)
        
        if not project_id:
            self.status_label.setText("请选择一个项目")
            return
            
        # 获取项目配置
        try:
            config = self.loader.get_project(project_id)
            
            # 在后台线程中运行分析
            self.analyzer_thread = SPCAnalyzerThread(config)
            self.analyzer_thread.finished.connect(self.on_analysis_finished)
            self.analyzer_thread.start()
            
            self.status_label.setText("正在分析...")
            self.analyzer_thread.finished.connect(lambda msg: print(msg))
        except Exception as e:
            self.status_label.setText(f"配置错误: {str(e)}")
    
    def on_analysis_finished(self, message):
        """分析完成回调"""
        self.status_label.setText(message)
```

### 2. 错误处理

在集成应用中，建议添加适当的错误处理：

```python
try:
    main(config=config)
except FileNotFoundError as e:
    # 处理文件未找到错误
    print(f"配置文件或数据文件不存在: {e}")
except ValueError as e:
    # 处理配置格式错误
    print(f"配置格式错误: {e}")
except Exception as e:
    # 处理其他错误
    print(f"分析过程中发生错误: {e}")
```

### 3. 配置文件管理

- `spc_config.yaml` - 主配置文件，包含所有项目定义
- `spc_config_example.yaml` - 配置模板，供用户参考创建自己的配置文件

## 依赖关系

- pandas >= 1.3.0
- numpy >= 1.20.0
- matplotlib >= 3.4.0
- scipy >= 1.7.0
- pyyaml >= 5.4.0 (新增)

## 版本兼容性

- v2.1+ 支持YAML配置系统和增强的API
- v2.0 提供现代化报告功能
- 向后兼容早期版本的配置方式