# SPC Statistical Analysis Tool v2.1

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A modern Statistical Process Control (SPC) analysis tool that automatically generates beautiful HTML and PDF reports.  
> Supports multi-project YAML configuration and can be easily integrated into PyQt/PySide GUI applications.

[简体中文](README.md) | **English**

---

## 📖 Overview

The SPC (Statistical Process Control) Statistical Analysis Tool is a Python toolkit designed for quality control in manufacturing. It provides:

- 📊 Automatic calculation of key statistical metrics (Cpk, Mean, Sigma)
- 🎨 Modern HTML reports (responsive design, gradient backgrounds, card layouts)
- 📄 Professional PDF reports (A4 size, table pagination, 300 DPI HD output)
- 📈 Histogram and normal distribution curve fitting
- 🎯 Intelligent Cpk color coding (Excellent/Acceptable/Poor)
- 🔄 Batch processing of multiple projects via YAML configuration
- 🔌 Clean Python API for easy integration into PyQt/PySide GUI applications

---

## ✨ Features

### Statistical Analysis
- ✅ Automatic Cpk process capability index calculation
- ✅ Mean and Standard Deviation (Sigma) computation
- ✅ Histogram with normal distribution curve fitting
- ✅ Specification limits (USL/LSL) visualization
- ✅ Sample size statistics

### Report Generation
- ✅ **HTML Reports**: Modern gradient backgrounds, responsive card layouts, statistical overview dashboard, Cpk value color coding, hover animation effects, desktop/tablet/mobile compatible
- ✅ **PDF Reports**: A4 standard paper size, automatic table pagination (20 rows per page), professional color scheme, intelligent text wrapping, 300 DPI high-quality output, individual distribution plot for each parameter

### Configuration & Integration
- ✅ YAML external configuration file, complete separation of config and code
- ✅ Single configuration file manages multiple projects
- ✅ Supports both absolute and relative paths
- ✅ Automatic missing data handling
- ✅ Clean Python API interface for easy integration with PyQt/PySide

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies:
```
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.4.0
scipy>=1.7.0
pyyaml>=5.4.0
```

### 2. Edit YAML Configuration File

Copy `spc_config_example.yaml` to `spc_config.yaml`, then edit:

```yaml
version: "1.0"

# Base directory for all relative paths
base_dir: "F:/your/data/directory"

projects:
  - name: "My Project - PCBA Voltage Test"
    id: "my_pcba_voltage_test"        # Unique ID, used in CLI and API calls
    csv_file: "./test_data.csv"        # Relative to base_dir
    output:
      html: "voltage_report.html"
      pdf: "voltage_report.pdf"
      img_dir: "voltage_images"
    spec_limits:
      # Format: CSV column name: [LSL, USL]
      # Column names must exactly match those in your CSV file
      Voltage_3V3: [3.2, 3.45]
      Voltage_5V0: [4.75, 5.25]
      Current_Idle: [0.038, 0.05]
```

> 💡 See `spc_config_example.yaml` for a detailed configuration template.

### 3. Run the Program

```bash
# Process the first project in the configuration file
python spc_analysis.py

# Specify configuration file and project
python spc_analysis.py --config spc_config.yaml --project my_pcba_voltage_test

# Batch process multiple projects (loop in Python)
from spc_analysis import main
from config_loader import ConfigLoader

loader = ConfigLoader("spc_config.yaml")
for config in loader.get_all_projects():
    main(config=config)
```

### 4. View Reports

The program generates:
- `voltage_report.html` — Modern HTML report
- `voltage_report.pdf` — Professional PDF report
- `voltage_images/` — Distribution plot images directory

---

## 📁 Project Structure

```
spc_statistic/
├── spc_analysis.py          # Main analysis engine (compute stats, generate reports)
├── config_loader.py         # YAML configuration loader (load, validate, parse)
├── spc_statistic.py         # Unified package interface (for module import)
├── spc_config.yaml          # YAML multi-project configuration (create your own)
├── spc_config_example.yaml  # YAML configuration example template
├── requirements.txt         # Python dependencies
├── README.md                # Chinese documentation
├── README_EN.md             # English documentation
├── RELEASE_NOTES.md         # Release notes
└── API_INTERFACE.md         # Detailed API reference
```

---

## 📋 YAML Configuration Guide

### Configuration File Format

```yaml
version: "1.0"                     # Configuration file version

base_dir: "F:/data/project"        # Base directory
                                   # All relative paths are resolved relative to this

projects:                          # Project list (define as many as you need)

  - name: "Project Display Name"   # Display name (for GUI dropdowns, etc.)
    id: "project_id"               # Unique ID (for CLI --project arg and API calls)
    csv_file: "./data.csv"         # CSV data file path
                                   # Absolute paths used as-is; relative paths use base_dir
    output:
      html: "report.html"          # HTML report output path
      pdf: "report.pdf"            # PDF report output path
      img_dir: "report_images"     # Distribution images output directory

    spec_limits:                   # Specification limits definition
      # Format: CSV column name: [LSL, USL]
      # ⚠️ Column names must exactly match those in your CSV file (case-sensitive)
      Voltage_3V3: [3.2, 3.45]
      Current_Idle: [0.038, 0.05]
```

### Path Resolution Rules

| Path Type | Example | Resolved To |
|-----------|---------|-------------|
| Absolute path | `F:/data/test.csv` | Used as-is |
| Relative path | `./test.csv` | `base_dir` + `./test.csv` |

### CSV File Format Requirements

- First row: Column headers (test parameter names)
- Subsequent rows: Test data
- Supports null and non-numeric values (automatically filtered)

```csv
SerialNumber,Voltage_3V3,Voltage_5V0,Current_Idle,OverallResult
SN001,3.35,5.02,0.042,PASS
SN002,3.33,5.01,0.041,PASS
SN003,3.34,5.03,0.043,PASS
```

---

## 🔌 Third-Party Integration Guide

This project is designed as a **standalone Python toolkit** with a clean API interface, making it very easy to integrate into PyQt/PySide or other GUI applications.

### Core API

| Module | Entry Point | Description |
|--------|-------------|-------------|
| `config_loader.py` | `ConfigLoader` | Load and manage YAML configurations |
| `spc_analysis.py` | `main()` | Execute SPC analysis and generate reports |
| `spc_statistic.py` | Unified import | Provides unified package import interface |

### Step 1: Copy This Project Into Your Application

```
your_project/
├── main_app.py              # Your PyQt/PySide main application
├── spc_module/              # ← Copy this project's files here
│   ├── spc_analysis.py
│   ├── config_loader.py
│   ├── spc_statistic.py
│   ├── spc_config.yaml      # User-editable external config file
│   └── spc_config_example.yaml
└── ...
```

### Step 2: Import and Use

```python
import sys
sys.path.insert(0, "spc_module")  # Add SPC module directory to Python path

from spc_analysis import main as run_spc_analysis
from config_loader import ConfigLoader
```

### Step 3: Get Project List (Populate Dropdown)

```python
from PyQt5.QtWidgets import QComboBox

loader = ConfigLoader("spc_module/spc_config.yaml")
loader.load()

combo = QComboBox()
for project_id, project_name in loader.list_projects():
    combo.addItem(project_name, project_id)
```

### Step 4: Execute Analysis (Recommended in Background Thread)

```python
from PyQt5.QtCore import QThread, pyqtSignal

class SPCWorker(QThread):
    """Background thread: runs SPC analysis without blocking UI"""
    finished = pyqtSignal(str)   # Completion signal
    error = pyqtSignal(str)      # Error signal

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        try:
            run_spc_analysis(config=self.config)
            self.finished.emit("Analysis reports generated successfully!")
        except Exception as e:
            self.error.emit(str(e))

# Usage example
selected_id = combo.currentData()
config = loader.get_project(selected_id)

worker = SPCWorker(config)
worker.finished.connect(lambda msg: print(msg))
worker.error.connect(lambda err: print(f"Error: {err}"))
worker.start()
```

### Complete Integration Example

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
            self.finished.emit("Analysis reports generated!")
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPC Statistical Analysis Tool")
        self.resize(400, 200)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Load configuration
        self.loader = ConfigLoader("spc_module/spc_config.yaml")
        self.loader.load()

        # Project selection dropdown
        layout.addWidget(QLabel("Select project:"))
        self.combo = QComboBox()
        for pid, pname in self.loader.list_projects():
            self.combo.addItem(pname, pid)
        layout.addWidget(self.combo)

        # Run button
        self.btn = QPushButton("Start Analysis")
        self.btn.clicked.connect(self.start_analysis)
        layout.addWidget(self.btn)

        self.status = QLabel("Ready")
        layout.addWidget(self.status)

    def start_analysis(self):
        project_id = self.combo.currentData()
        config = self.loader.get_project(project_id)

        self.worker = SPCWorker(config)
        self.worker.finished.connect(self.on_done)
        self.worker.error.connect(self.on_error)
        self.status.setText("Analyzing...")
        self.btn.setEnabled(False)
        self.worker.start()

    def on_done(self, msg):
        self.status.setText(msg)
        self.btn.setEnabled(True)
        QMessageBox.information(self, "Done", msg)

    def on_error(self, err):
        self.status.setText("Analysis failed")
        self.btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Analysis failed:\n{err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
```

### Error Handling Recommendations

```python
from config_loader import ConfigLoader

try:
    loader = ConfigLoader("spc_config.yaml")
    loader.load()
    config = loader.get_project("my_project")
except FileNotFoundError:
    print("Configuration file not found, please check the path")
except ValueError as e:
    print(f"Configuration file format error: {e}")
except KeyError:
    print("Specified project ID does not exist")
```

---

## 🎯 Cpk Standard Reference

| Cpk Value | Grade | Description |
|-----------|-------|-------------|
| Cpk ≥ 1.67 | A | Excellent process capability |
| 1.33 ≤ Cpk < 1.67 | B | Good process capability |
| 1.0 ≤ Cpk < 1.33 | C | Acceptable process capability |
| Cpk < 1.0 | D | Insufficient process capability |

---

## ❓ FAQ

### Q: Column not found error?
A: Check if the parameter names in `spec_limits` **exactly match** the CSV column names (including case and underscores).

### Q: Some test items don't generate plots?
A: Check if the column has valid numeric data in the CSV. Null or non-numeric values are automatically filtered.

### Q: How to analyze only some parameters?
A: Comment out unwanted parameters in the YAML `spec_limits` section (add `#` at the beginning of the line).

### Q: Is one-sided specification supported?
A: Current version supports two-sided specifications. For one-sided specs, set the other side to a very large/small value.

### Q: How to let users modify config after packaging as exe?
A: Place `spc_config.yaml` in the same directory as the exe. Users can edit it with any text editor. The program reads it automatically on startup.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit Issues and Pull Requests.

## 📞 Contact

- Author: SimonYuan
- Website: https://tresordie.github.io/

## 🙏 Acknowledgments

- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [Matplotlib](https://matplotlib.org/) - Plotting library
- [NumPy](https://numpy.org/) - Numerical computing
- [SciPy](https://scipy.org/) - Scientific computing

---

⭐ If this project helps you, please give it a star!
