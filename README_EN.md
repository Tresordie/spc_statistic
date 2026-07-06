# SPC Statistical Analysis Tool v2.4

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A modern Statistical Process Control (SPC) analysis tool that automatically generates beautiful HTML and PDF reports.  
> Supports multi-project YAML configuration and can be easily integrated into PyQt/PySide GUI applications.  
> Supports Cpk analysis + GRR measurement system analysis + spec limits comparison tool.  
> HTML reports embed images as Base64 — only HTML+PDF files needed when sharing.

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
- 🔬 **New** Cpk reverse analysis: specify a target Cpk value to automatically derive specification limits (LSL/USL)
- 📂 **New** Direct analysis of CSV and Excel (.xlsx/.xls) data files
- 📐 **New** GRR measurement system analysis (ANOVA/AIAG methods), generates HTML/Markdown/PDF reports
- 📐 GRR reports include %EV, %AV, %GRR percentage metrics
- 🔍 **New** Spec limits comparison tool: compare CSV file spec limits against YAML configuration item by item
- 📦 **Improved** HTML reports embed images as Base64 — no separate image folder needed, easier to share

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

### Cpk Reverse Analysis (New)
- ✅ Specify target Cpk value to automatically derive specification limits (LSL/USL)
- ✅ Supports CSV and Excel (.xlsx/.xls) data files
- ✅ Automatically identifies all numeric columns — no manual spec limit configuration needed
- ✅ Supports specifying Excel sheet name
- ✅ Generates HTML + PDF analysis reports
- ✅ Histograms with normal distribution fitting curves and specification limit annotations

### GRR Measurement System Analysis
- ✅ Supports ANOVA method and AIAG average-range method
- ✅ Automatically calculates EV (repeatability), AV (reproducibility), PV (part variation), %GRR, ndc
- ✅ Reports include %EV, %AV, %GRR percentage metrics
- ✅ Supports custom operator/part/measurement value column names
- ✅ Generates HTML + Markdown + PDF reports in three formats
- ✅ Includes variance component charts, interaction plots, box plots, %GRR gauge
- ✅ Automatic measurement system pass/conditional/failed determination

### Spec Limits Comparison Tool (New)
- ✅ Compare CSV file's TEST_NAME / LOWER_LIMIT / UPPER_LIMIT against YAML config's spec_limits for the same project ID
- ✅ Automatically identifies matched, different, CSV-only, and YAML-only items
- ✅ Generates timestamped Markdown comparison report
- ✅ Highlights test items with differences

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
- `voltage_report.html` — Modern HTML report (images Base64 embedded, self-contained)
- `voltage_report.pdf` — Professional PDF report

---

## 🔬 Cpk Reverse Analysis (New)

Unlike the traditional approach of “known spec limits → calculate Cpk”, the Cpk reverse analysis tool supports **known target Cpk → derive spec limits**.

### Core Principle

Derive reasonable specification limits from data statistics and a target Cpk value:

$$
LSL = \mu - 3\sigma \cdot Cpk \qquad USL = \mu + 3\sigma \cdot Cpk
$$

### Command Line Usage

```bash
# Basic usage: specify data file and target Cpk value
python cpk_analysis.py --file data.csv --cpk 1.33

# Specify output directory
python cpk_analysis.py --file data.xlsx --cpk 1.33 --output ./reports

# Specify Excel sheet name
python cpk_analysis.py --file data.xlsx --cpk 1.67 --sheet Sheet1
```

### Third-Party Integration

```python
from spc_statistic import analyze_with_cpk

result = analyze_with_cpk(
    file_path="data.csv",      # Data file path (CSV or Excel)
    target_cpk=1.33,           # Target Cpk value
    output_dir="./reports"     # Report output directory (optional)
)

# View results
for s in result['stats_list']:
    print(f"{s['column']}: LSL={s['lsl']:.4f}, USL={s['usl']:.4f}")
print(f"HTML report: {result['html_path']}")
print(f"PDF report: {result['pdf_path']}")
```

### Return Value

`analyze_with_cpk()` returns a dictionary containing:

| Key | Type | Description |
|------|------|------|
| `stats_list` | `list[dict]` | Statistical results for each column (includes mean, std, lsl, usl, cpk_achieved, etc.) |
| `html_path` | `str` | Full path to the generated HTML report |
| `pdf_path` | `str` | Full path to the generated PDF report |
| `file_path` | `str` | Original data file path |
| `target_cpk` | `float` | Target Cpk value |

---

## 📐 GRR Measurement System Analysis (New)

GRR (Gauge Repeatability & Reproducibility) evaluates measurement system variation to determine if a measurement system is reliable.

### Analysis Methods

| Method | Description | Features |
|--------|-------------|----------|
| **ANOVA** (default) | Analysis of Variance | Decomposes interaction and error components, more precise |
| **AIAG** | Average-Range Method | Traditional method, widely used in industry |

### Data Format

Data files (CSV/Excel) use a long format with three columns: operator, part, and measurement value:

```csv
operator,part,value
Operator_A,Part_1,3.35
Operator_A,Part_1,3.34
Operator_A,Part_2,3.32
Operator_B,Part_1,3.36
...
```

> 💡 Column names can be customized using `--operator`, `--part`, `--value` parameters

### Command Line Usage

```bash
# Basic usage (default ANOVA method)
python grr_analysis.py --file grr_data.csv

# Use AIAG method
python grr_analysis.py --file grr_data.csv --method AIAG

# Custom column names
python grr_analysis.py --file data.xlsx --operator 操作员 --part 零件 --value 测量值

# Specify output directory
python grr_analysis.py --file grr_data.csv --output ./reports
```

### Third-Party Integration

```python
from spc_statistic import analyze_grr

result = analyze_grr(
    file_path="grr_data.csv",
    operator_col="operator",   # Operator column name
    part_col="part",           # Part column name
    value_col="value",         # Measurement value column name
    method="ANOVA",            # Analysis method: 'ANOVA' or 'AIAG'
    output_dir="./reports"     # Report output directory (optional)
)

# View results
r = result['result']
print(f"%GRR: {r['pct_grr']:.2f}%")
print(f"ndc: {r['ndc']}")
print(f"Verdict: {'✅ Pass' if r['pct_grr'] < 10 else '❌ Fail'}")
print(f"Markdown report: {result['markdown_path']}")
print(f"HTML report: {result['html_path']}")
print(f"PDF report: {result['pdf_path']}")
```

### Return Value

`analyze_grr()` returns a dictionary containing:

| Key | Type | Description |
|------|------|------|
| `result` | `dict` | GRR analysis results (includes EV, AV, PV, %GRR, ndc, etc.) |
| `markdown_path` | `str` | Markdown report path |
| `html_path` | `str` | HTML report path |
| `pdf_path` | `str` | PDF report path |

### GRR Acceptance Criteria

| %GRR | Verdict | Description |
|------|---------|-------------|
| < 10% | ✅ Pass | Measurement system acceptable |
| 10% ~ 30% | ⚠️ Conditional | Decide based on application |
| ≥ 30% | ❌ Fail | Measurement system needs improvement |
| ndc ≥ 5 | ✅ | Sufficient resolution |
| ndc < 5 | ❌ | Insufficient resolution |

### Spec Limits Comparison (New)

Validates whether the spec limits in a CSV data file match the YAML configuration, useful for quality audits and data verification.

#### Command Line Usage

```bash
# Basic usage
python limits_compare.py --file data.csv --project ehm_pcba_test

# Specify config file and output directory
python limits_compare.py --file data.csv --project ehm_pcba_test --config spc_config.yaml --output ./reports
```

#### Output

- Console prints comparison results (matched, different, CSV-only, YAML-only items)
- Generates Markdown comparison report (`{datetime}_{project_id}_limits_compare.markdown`)

---

## 📁 Project Structure

```
spc_statistic/
├── __init__.py              # Package initialization file (exports main APIs)
├── spc_analysis.py          # Main analysis engine (known spec limits → calculate Cpk)
├── cpk_analysis.py          # Cpk reverse analysis (known Cpk → derive spec limits)
├── grr_analysis.py          # GRR measurement system analysis (ANOVA/AIAG methods)
├── limits_compare.py        # Spec limits comparison tool (CSV vs YAML config)
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
| `spc_analysis.py` | `main()` | Known spec limits → calculate Cpk and generate reports |
| `cpk_analysis.py` | `analyze_with_cpk()` | Known target Cpk → derive spec limits and generate reports |
| `grr_analysis.py` | `analyze_grr()` | GRR measurement system analysis (ANOVA/AIAG) and generate reports |
| `limits_compare.py` | `main()` | Spec limits comparison (CSV vs YAML config), generates Markdown report |
| `spc_statistic.py` | Unified import | Provides unified package import interface |

### Step 1: Copy This Project Into Your Application

```
your_project/
├── main_app.py              # Your PyQt/PySide main application
├── spc_statistic/           # ← Copy this project's files here (as a Python package)
│   ├── __init__.py
│   ├── spc_analysis.py
│   ├── cpk_analysis.py
│   ├── config_loader.py
│   ├── spc_statistic.py
│   ├── spc_config.yaml      # User-editable external config file
│   └── spc_config_example.yaml
└── ...
```

### Step 2: Import and Use

```python
# Method 1: Import as a package (recommended)
from spc_statistic import ConfigLoader, run_spc_analysis, analyze_with_cpk

# Method 2: Import from submodules
from spc_statistic.config_loader import ConfigLoader
from spc_statistic.spc_analysis import main as run_spc_analysis
from spc_statistic.cpk_analysis import analyze_with_cpk
```

### Step 3: Get Project List (Populate Dropdown)

```python
from PyQt5.QtWidgets import QComboBox

loader = ConfigLoader("spc_statistic/spc_config.yaml")
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
sys.path.insert(0, ".")  # Ensure the parent directory of spc_statistic is in Python path

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
        self.loader = ConfigLoader("spc_statistic/spc_config.yaml")
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
from spc_statistic import ConfigLoader, analyze_with_cpk

# Error handling for YAML configuration mode
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

# Error handling for Cpk reverse analysis
try:
    result = analyze_with_cpk("data.csv", target_cpk=1.33)
except FileNotFoundError as e:
    print(f"Data file not found: {e}")
except ValueError as e:
    print(f"Data file format error: {e}")
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
