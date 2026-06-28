# SPC Statistical Analysis Tool v2.0

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A modern Statistical Process Control (SPC) analysis tool that automatically generates clean and beautiful HTML and PDF reports

[简体中文](README.md) | **English**

## 📖 Overview

The SPC (Statistical Process Control) Statistical Analysis Tool is a Python application designed for quality control in manufacturing. It provides:

- 📊 Automatic calculation of key statistical metrics (Cpk, Mean, Sigma)
- 🎨 Modern HTML reports (responsive design, gradient backgrounds, card layouts)
- 📄 Professional PDF reports (A4 size, table pagination, 300 DPI HD output)
- 📈 Histogram and normal distribution curve fitting
- 🎯 Intelligent Cpk color coding (Excellent/Acceptable/Poor)
- 🔄 Batch processing support for multiple CSV files

## ✨ Features

### Statistical Analysis
- ✅ Automatic Cpk process capability index calculation
- ✅ Mean and Standard Deviation (Sigma) computation
- ✅ Histogram with normal distribution curve fitting
- ✅ Specification limits (USL/LSL) visualization
- ✅ Sample size statistics

### Report Generation
- ✅ **HTML Reports**:
  - Modern gradient backgrounds
  - Responsive card layouts
  - Statistical overview dashboard
  - Cpk value color coding
  - Hover animation effects
  - Desktop/Tablet/Mobile compatible

- ✅ **PDF Reports**:
  - A4 standard paper size
  - Automatic table pagination (20 rows per page)
  - Professional color scheme
  - Intelligent text wrapping
  - 300 DPI high-quality output
  - Individual distribution plot for each parameter

### Flexible Configuration
- ✅ Complete separation of configuration and code
- ✅ Modify only one configuration file
- ✅ Support for unlimited test items
- ✅ Automatic missing data handling
- ✅ Batch processing support

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install pandas numpy matplotlib scipy
```

### 2. Configure Test Items

Edit the `spc_config.py` file:

```python
# Set CSV file path
CSV_FILE_PATH = "./your_test_data.csv"

# Define test items and specification limits
SPEC_LIMITS = {
    "VCC_3V3": (3.2, 3.45),        # 3.3V power supply, LSL=3.2V, USL=3.45V
    "VCC_5V0": (4.75, 5.25),       # 5V power supply
    "Current_Idle": (0.038, 0.05), # Idle current
    # Add more test items...
}
```

### 3. Run the Program

```bash
# Single file processing
python spc_analysis.py

# Batch processing
python batch_process.py
```

### 4. View Reports

The program generates:
- `spc_report.html` - Modern HTML report
- `spc_report.pdf` - Professional PDF report
- `spc_report_images/` - Distribution plot images directory

## 📁 Project Structure

```
spc_generation/
├── spc_config.py              # Configuration file (define test items and limits)
├── spc_config_example.py      # Configuration examples and templates
├── spc_analysis.py            # Main program (generates reports)
├── batch_process.py           # Batch processing tool
├── spc_report_styles.py       # Style module (optional)
├── README.md                  # Chinese documentation
├── README_EN.md              # English documentation
└── [legacy scripts]           # Kept for reference
```

## 📋 Usage Guide

### Configuration File

#### spc_config.py

Main configuration options:

```python
# CSV file path
CSV_FILE_PATH = "./data.csv"

# Output file configuration
OUTPUT_HTML = "report.html"
OUTPUT_PDF = "report.pdf"
OUTPUT_IMG_DIR = "report_images"

# Specification limits definition
SPEC_LIMITS = {
    "Test Item Name": (LSL, USL),
}
```

#### Adding Test Items

```python
SPEC_LIMITS = {
    # Voltage tests
    "Voltage_3V3": (3.2, 3.45),
    "Voltage_5V0": (4.75, 5.25),
    
    # Current tests
    "Current_Idle": (0.038, 0.05),
    "Current_Active": (0.15, 0.25),
    
    # Temperature tests
    "Temperature": (20, 80),
    
    # Add more...
}
```

**Note**: Test item names must exactly match the column names in the CSV file (including case sensitivity).

### CSV File Format

CSV files should contain:
- First row: Column headers (test item names)
- Subsequent rows: Test data
- Supports null and non-numeric values (automatically filtered)

Example:

```csv
SerialNumber,VCC_3V3,VCC_5V0,Current_Idle,OverallResult
SN001,3.35,5.02,0.042,PASS
SN002,3.33,5.01,0.041,PASS
SN003,3.34,5.03,0.043,PASS
```

### Batch Processing

Edit `batch_process.py`:

```python
csv_files = [
    "./data_batch1.csv",
    "./data_batch2.csv",
    "./data_batch3.csv",
]

# Or auto-scan directory
import glob
csv_files = glob.glob("./data/*.csv")
```

Run:

```bash
python batch_process.py
```

All reports will be saved in the `batch_reports/` directory.

## 📊 Report Examples

### HTML Report Features

- **Header**: Gradient title and description
- **Statistics Overview Cards**:
  - Total parameters count
  - Total samples count
  - Cpk ≥ 1.33 (Excellent) count
  - 1.0 ≤ Cpk < 1.33 (Acceptable) count
- **Statistics Table**: Responsive table with color-coded Cpk values
- **Distribution Plots Grid**: Adaptive grid layout

### PDF Report Features

- **Statistics Table Pages**: Automatic pagination, professional layout
- **Distribution Plot Pages**: One page per parameter, A4 size HD output
- **Color Scheme**: Dark blue-gray headers, alternating row colors
- **HD Output**: 300 DPI resolution

## 🔧 Advanced Usage

### Customizing Styles

Edit functions in `spc_analysis.py`:

- `plot_histogram_with_modern_style()` - Chart styling
- `generate_pdf_report()` - PDF layout
- `generate_html_report()` - HTML styling

### Multi-Project Configuration

Create separate configuration files for different projects:

```bash
# Project A
cp spc_config.py spc_config_project_a.py

# Project B
cp spc_config.py spc_config_project_b.py

# Modify spc_analysis.py to import corresponding configuration
# from spc_config_project_a import ...
```

### CI/CD Integration

```yaml
# GitHub Actions Example
- name: Generate SPC Report
  run: |
    pip install pandas numpy matplotlib scipy
    python spc_analysis.py
```

## 📝 Dependencies

```
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.4.0
scipy>=1.7.0
```

Install:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pandas numpy matplotlib scipy
```

## 🎯 Cpk Standard Reference

| Cpk Value | Grade | Description |
|-----------|-------|-------------|
| Cpk ≥ 1.67 | A | Excellent process capability |
| 1.33 ≤ Cpk < 1.67 | B | Good process capability |
| 1.0 ≤ Cpk < 1.33 | C | Acceptable process capability |
| Cpk < 1.0 | D | Insufficient process capability |

## ❓ FAQ

### Q: Column not found error?
A: Check if the test item names in `SPEC_LIMITS` exactly match the CSV column names (including case and underscores).

### Q: Some test items don't generate plots?
A: Check if the column has valid numeric data in the CSV. Null or non-numeric values are automatically filtered.

### Q: How to test only some items?
A: Comment out unwanted items in `SPEC_LIMITS` (add `#` at the beginning of the line).

### Q: Is one-sided specification supported?
A: Current version supports two-sided specifications. For one-sided specs, set the other side to a very large/small value.

### Q: How to modify report titles?
A: Edit the title text in `generate_html_report()` and `generate_pdf_report()` functions in `spc_analysis.py`.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit Issues and Pull Requests.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

- Author: SimonYuan
- Website: https://tresordie.github.io/
- Email: [your-email@example.com]

## 🙏 Acknowledgments

- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [Matplotlib](https://matplotlib.org/) - Plotting library
- [NumPy](https://numpy.org/) - Numerical computing
- [SciPy](https://scipy.org/) - Scientific computing

## 📊 Version History

- **v2.0** (2026-06-17)
  - ✨ Separated configuration from code
  - 🎨 Modern report design
  - 📱 Responsive HTML layout
  - 📄 Professional PDF layout
  - 🔄 Batch processing support

- **v1.0** (2026-05-04)
  - 🎉 Initial release
  - 📊 Basic statistical calculations
  - 📈 Simple chart generation

---

⭐ If this project helps you, please give it a star!
