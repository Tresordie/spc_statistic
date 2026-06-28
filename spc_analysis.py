# -*- encoding: utf-8 -*-
"""
@File    :   spc_analysis.py
@Time    :   2026/06/17
@Author  :   SimonYuan
@Version :   2.0
@Desc    :   通用SPC统计分析程序 - 现代化的PDF和HTML报告生成

功能特性:
1. 从配置文件读取测试项目和规格限
2. 自动计算Cpk、Mean、Sigma等统计量
3. 生成现代化的PDF报告(A4尺寸,专业排版)
4. 生成响应式HTML报告(渐变背景,卡片布局)
5. 智能Cpk彩色标识
6. 长参数名自动换行

使用方法:
1. 编辑 spc_config.py 配置测试项目和规格限
2. 运行: python spc_analysis.py
3. 查看生成的HTML和PDF报告
"""

import os
import warnings

import matplotlib.backends.backend_pdf as pdf_backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm

# 忽略警告信息
warnings.filterwarnings("ignore")

# 导入配置
try:
    from spc_config import (
        CSV_FILE_PATH,
        OUTPUT_HTML,
        OUTPUT_IMG_DIR,
        OUTPUT_PDF,
        SPEC_LIMITS,
    )
except ImportError:
    print("错误: 找不到 spc_config.py 配置文件!")
    print("请确保 spc_config.py 与 spc_analysis.py 在同一目录下")
    exit(1)


# ================================ 辅助函数 ================================


def calculate_cpk(data, lsl, usl):
    """
    计算Cpk值

    参数:
        data: 数据数组
        lsl: 规格下限
        usl: 规格上限

    返回:
        Cpk值,如果sigma为0则返回inf
    """
    if len(data) < 2:
        return None

    mu = np.mean(data)
    sigma = np.std(data, ddof=1)

    if sigma == 0:
        return np.inf

    cpk = min((usl - mu) / (3 * sigma), (mu - lsl) / (3 * sigma))
    return cpk


def plot_histogram_with_modern_style(
    data, param_name, lsl, usl, mean, std, cpk, image_path
):
    """
    绘制现代化的直方图+正态分布曲线

    特性:
    - A4尺寸 (11.69 x 8.27英寸)
    - 专业配色方案
    - 智能Cpk显示(根据值显示不同颜色和符号)
    - 长参数名自动换行
    - 300 DPI高清输出
    """
    # 创建A4尺寸的figure
    fig = plt.figure(figsize=(11.69, 8.27), dpi=300)

    # 创建主坐标轴,留出标题和说明空间
    ax = fig.add_axes([0.10, 0.15, 0.82, 0.72])

    # 绘制直方图
    n, bins, patches = ax.hist(
        data,
        bins=min(30, len(np.unique(data))),
        density=True,
        alpha=0.7,
        color="#3498db",
        edgecolor="#2980b9",
        linewidth=1.0,
        label="Data Distribution",
    )

    # 绘制拟合正态曲线
    x = np.linspace(min(data), max(data), 300)
    pdf = norm.pdf(x, mean, std)
    ax.plot(
        x,
        pdf,
        "r-",
        lw=3,
        label=f"Normal Distribution\n($\\mu$={mean:.3f}, $\\sigma$={std:.3f})",
        alpha=0.9,
    )

    # 绘制规格限和均值线
    ax.axvline(
        lsl,
        color="#27ae60",
        linestyle="--",
        lw=2.5,
        label=f"LSL = {lsl:.3f}",
        alpha=0.8,
    )
    ax.axvline(
        usl,
        color="#27ae60",
        linestyle="--",
        lw=2.5,
        label=f"USL = {usl:.3f}",
        alpha=0.8,
    )
    ax.axvline(
        mean,
        color="#e67e22",
        linestyle="-",
        lw=2.5,
        label=f"Mean = {mean:.3f}",
        alpha=0.9,
    )

    # 智能Cpk显示(根据值显示不同颜色)
    if np.isinf(cpk):
        cpk_text = "Cpk = ∞"
        cpk_color = "#27ae60"
    elif cpk >= 1.33:
        cpk_text = f"Cpk = {cpk:.3f} ✓"
        cpk_color = "#27ae60"
    elif cpk >= 1.0:
        cpk_text = f"Cpk = {cpk:.3f} ⚠"
        cpk_color = "#f39c12"
    else:
        cpk_text = f"Cpk = {cpk:.3f} ✗"
        cpk_color = "#e74c3c"

    # Cpk信息框(放在左上角)
    ax.text(
        0.02,
        0.97,
        cpk_text,
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        verticalalignment="top",
        horizontalalignment="left",
        color=cpk_color,
        bbox=dict(
            boxstyle="round,pad=0.6",
            facecolor="white",
            edgecolor=cpk_color,
            alpha=0.95,
            linewidth=2,
        ),
    )

    # 处理长参数名(自动换行)
    display_name = param_name.replace("_", " ")
    if len(display_name) > 60:
        words = display_name.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 > 55:
                lines.append(current_line)
                current_line = word
            else:
                current_line += (" " if current_line else "") + word
        if current_line:
            lines.append(current_line)
        display_name = "\n".join(lines)

    # 标题
    ax.set_title(
        f"Parameter: {display_name}",
        fontsize=16,
        fontweight="bold",
        pad=20,
        color="#2c3e50",
    )

    # 副标题(样本数)
    ax.text(
        0.5,
        -0.15,
        f"Sample Size: n = {len(data)}",
        transform=ax.transAxes,
        fontsize=11,
        ha="center",
        color="#7f8c8d",
    )

    # 轴标签
    ax.set_xlabel("Value", fontsize=13, fontweight="bold", color="#2c3e50", labelpad=10)
    ax.set_ylabel(
        "Probability Density",
        fontsize=13,
        fontweight="bold",
        color="#2c3e50",
        labelpad=10,
    )

    # 图例
    ax.legend(
        loc="upper right",
        fontsize=9.5,
        framealpha=0.9,
        edgecolor="#bdc3c7",
        facecolor="#f8f9fa",
    )

    # 网格
    ax.grid(True, alpha=0.3, linestyle="--", linewidth=0.8, color="#95a5a6")

    # 刻度样式
    ax.tick_params(axis="both", which="major", labelsize=10, colors="#34495e")

    # 坐标轴边框
    for spine in ax.spines.values():
        spine.set_color("#bdc3c7")
        spine.set_linewidth(1.2)

    # 自动调整布局
    plt.tight_layout()

    # 保存PNG(用于HTML)
    plt.savefig(image_path, dpi=150, bbox_inches="tight")

    return fig


def generate_pdf_report(stats, fig_dict, output_pdf):
    """
    生成现代化的PDF报告

    特性:
    - A4纸张尺寸
    - 表格分页处理(每页20行)
    - 专业配色方案
    - 智能文本换行
    - 300 DPI高清输出
    """
    with pdf_backend.PdfPages(output_pdf) as pdf:
        # ====== 第一部分:统计表格 ======
        rows_per_page = 20
        total_rows = len(stats)
        total_pages = (total_rows + rows_per_page - 1) // rows_per_page

        for page_idx in range(total_pages):
            # 创建A4尺寸的figure
            fig_table = plt.figure(figsize=(11.69, 8.27), dpi=300)

            # 获取当前页数据
            start_idx = page_idx * rows_per_page
            end_idx = min(start_idx + rows_per_page, total_rows)
            page_stats = stats[start_idx:end_idx]
            actual_rows = len(page_stats)

            # 准备表格数据
            table_data = []
            for s in page_stats:
                table_data.append(
                    [
                        s["Parameter"],
                        s["Mean"],
                        s["Sigma"],
                        s["LSL"],
                        s["USL"],
                        s["Cpk"],
                        str(s["n"]),
                    ]
                )

            columns = ["Parameter", "Mean", "Sigma", "LSL", "USL", "Cpk", "n"]

            # 创建坐标轴,留出标题空间
            ax = fig_table.add_axes([0.05, 0.05, 0.90, 0.88])
            ax.axis("off")

            # 创建表格
            table = ax.table(
                cellText=table_data,
                colLabels=columns,
                loc="center",
                cellLoc="center",
                colWidths=[0.32, 0.12, 0.12, 0.11, 0.11, 0.11, 0.11],
            )

            # 表格整体样式
            table.auto_set_font_size(False)
            table.set_fontsize(7)
            table.scale(1, 1.5)

            # 设置表头样式
            for col_idx in range(len(columns)):
                cell = table[0, col_idx]
                cell.set_facecolor("#2c3e50")
                cell.set_text_props(color="white", fontweight="bold", fontsize=7.5)
                cell.set_edgecolor("#34495e")
                cell.set_linewidth(1.5)

            # 设置数据行样式
            for row_idx in range(1, actual_rows + 1):
                # 交替行背景色
                if row_idx % 2 == 1:
                    bg_color = "#ffffff"
                else:
                    bg_color = "#f8f9fa"

                for col_idx in range(len(columns)):
                    cell = table[row_idx, col_idx]
                    cell.set_facecolor(bg_color)
                    cell.set_edgecolor("#dee2e6")
                    cell.set_linewidth(0.5)

                    # 数据列居中对齐
                    if col_idx > 0:
                        cell.set_text_props(ha="center", va="center")

                # Parameter列特殊处理:左对齐 + 长文本换行
                param_cell = table[row_idx, 0]
                param_text = param_cell.get_text().get_text()

                # 智能换行处理
                if len(param_text) > 28:
                    words = param_text.split("_")
                    lines = []
                    current_line = ""

                    for word in words:
                        test_line = current_line + ("_" if current_line else "") + word
                        if len(test_line) > 28 and current_line:
                            lines.append(current_line)
                            current_line = word
                        else:
                            current_line = test_line

                    if current_line:
                        lines.append(current_line)

                    wrapped_text = "\n".join(lines)
                    param_cell.get_text().set_text(wrapped_text)
                    param_cell.set_text_props(ha="left", va="center", fontsize=6.5)
                else:
                    param_cell.set_text_props(ha="left", va="center")

            # 添加页面标题
            if total_pages > 1:
                title_text = (
                    f"SPC Statistical Summary (Page {page_idx + 1}/{total_pages})"
                )
            else:
                title_text = "SPC Statistical Summary"

            fig_table.text(
                0.5,
                0.96,
                title_text,
                ha="center",
                va="top",
                fontsize=14,
                fontweight="bold",
                color="#2c3e50",
            )

            # 保存PDF页
            pdf.savefig(fig_table, dpi=300, bbox_inches="tight")
            plt.close(fig_table)

        # ====== 第二部分:分布图 ======
        for idx, s in enumerate(stats):
            param = s["Parameter"]
            if param in fig_dict:
                fig = fig_dict[param]

                # 添加页脚信息
                fig.text(
                    0.5,
                    0.02,
                    f"SPC Report - {param} ({idx + 1}/{len(stats)})",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    color="#7f8c8d",
                    alpha=0.7,
                )

                # 保存到PDF
                pdf.savefig(fig, dpi=300, bbox_inches="tight")
                plt.close(fig)


def generate_html_report(stats, img_dir, output_html):
    """
    生成现代化的HTML报告

    特性:
    - 渐变背景
    - 统计概览卡片
    - 响应式表格(Cpk值彩色显示)
    - 图表网格布局
    - 悬停动画效果
    """
    html_content = (
        """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SPC Statistical Summary Report</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                min-height: 100vh;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }
            
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            
            .stats-summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                padding: 30px;
                background: #f8f9fa;
            }
            
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.3s ease;
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
            }
            
            .stat-card .number {
                font-size: 2em;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            
            .stat-card .label {
                color: #7f8c8d;
                font-size: 0.9em;
            }
            
            .content {
                padding: 40px;
            }
            
            .section-title {
                font-size: 1.8em;
                color: #2c3e50;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #3498db;
                font-weight: 600;
            }
            
            .table-container {
                overflow-x: auto;
                margin-bottom: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                background: white;
            }
            
            thead {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
            }
            
            th {
                padding: 15px 10px;
                text-align: center;
                font-weight: 600;
                font-size: 0.95em;
                letter-spacing: 0.5px;
            }
            
            tbody tr {
                border-bottom: 1px solid #ecf0f1;
                transition: background-color 0.2s ease;
            }
            
            tbody tr:hover {
                background-color: #f8f9fa;
            }
            
            tbody tr:nth-child(even) {
                background-color: #fafbfc;
            }
            
            tbody tr:nth-child(even):hover {
                background-color: #f0f1f2;
            }
            
            td {
                padding: 12px 10px;
                text-align: center;
                font-size: 0.9em;
            }
            
            td:first-child {
                text-align: left;
                font-weight: 500;
                color: #2c3e50;
                max-width: 300px;
                word-wrap: break-word;
            }
            
            .cpk-good {
                color: #27ae60;
                font-weight: bold;
            }
            
            .cpk-warning {
                color: #f39c12;
                font-weight: bold;
            }
            
            .cpk-bad {
                color: #e74c3c;
                font-weight: bold;
            }
            
            .plots-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
                gap: 30px;
                margin-top: 30px;
            }
            
            .plot-card {
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);
                overflow: hidden;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .plot-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 24px rgba(0,0,0,0.15);
            }
            
            .plot-header {
                background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                color: white;
                padding: 15px 20px;
                font-weight: 600;
                font-size: 1.1em;
            }
            
            .plot-body {
                padding: 20px;
                text-align: center;
            }
            
            .plot-body img {
                max-width: 100%;
                height: auto;
                border-radius: 8px;
            }
            
            .footer {
                background: #2c3e50;
                color: white;
                text-align: center;
                padding: 20px;
                font-size: 0.9em;
            }
            
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 1.8em;
                }
                
                .plots-grid {
                    grid-template-columns: 1fr;
                }
                
                .content {
                    padding: 20px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 SPC Statistical Summary</h1>
                <p>Comprehensive Statistical Process Control Analysis Report</p>
            </div>
            
            <div class="stats-summary">
                <div class="stat-card">
                    <div class="number">"""
        + str(len(stats))
        + """</div>
                    <div class="label">Total Parameters</div>
                </div>
                <div class="stat-card">
                    <div class="number">"""
        + str(sum(s["n"] for s in stats))
        + """</div>
                    <div class="label">Total Samples</div>
                </div>
                <div class="stat-card">
                    <div class="number">"""
        + str(len([s for s in stats if s["Cpk"] != "inf" and float(s["Cpk"]) >= 1.33]))
        + """</div>
                    <div class="label">Cpk ≥ 1.33 (Excellent)</div>
                </div>
                <div class="stat-card">
                    <div class="number">"""
        + str(
            len(
                [
                    s
                    for s in stats
                    if s["Cpk"] != "inf"
                    and float(s["Cpk"]) < 1.33
                    and float(s["Cpk"]) >= 1.0
                ]
            )
        )
        + """</div>
                    <div class="label">1.0 ≤ Cpk < 1.33 (Acceptable)</div>
                </div>
            </div>
            
            <div class="content">
                <h2 class="section-title">📋 Summary Statistics</h2>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Parameter</th>
                                <th>Mean</th>
                                <th>Sigma</th>
                                <th>LSL</th>
                                <th>USL</th>
                                <th>Cpk</th>
                                <th>Sample Size</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    )

    # 生成表格行
    for s in stats:
        # 根据Cpk值设置颜色类
        try:
            if s["Cpk"] == "inf":
                cpk_class = "cpk-good"
            else:
                cpk_val = float(s["Cpk"])
                if cpk_val >= 1.33:
                    cpk_class = "cpk-good"
                elif cpk_val >= 1.0:
                    cpk_class = "cpk-warning"
                else:
                    cpk_class = "cpk-bad"
        except:
            cpk_class = ""

        html_content += f"""                            <tr>
                                <td>{s["Parameter"]}</td>
                                <td>{s["Mean"]}</td>
                                <td>{s["Sigma"]}</td>
                                <td>{s["LSL"]}</td>
                                <td>{s["USL"]}</td>
                                <td class="{cpk_class}">{s["Cpk"]}</td>
                                <td>{s["n"]}</td>
                            </tr>
"""

    html_content += """                        </tbody>
                    </table>
                </div>
                
                <h2 class="section-title">📈 Distribution Plots</h2>
                <div class="plots-grid">
"""

    # 生成图表卡片
    for s in stats:
        param_safe = s["Parameter"].replace("/", "_")
        img_file = os.path.join(img_dir, f"{param_safe}.png")
        html_content += f"""                    <div class="plot-card">
                        <div class="plot-header">{s["Parameter"]}</div>
                        <div class="plot-body">
                            <img src="{img_file}" alt="{s["Parameter"]} Distribution">
                        </div>
                    </div>
"""

    html_content += """                </div>
            </div>
            
            <div class="footer">
                <p>Generated by SPC Analysis Tool | Statistical Process Control Report</p>
            </div>
        </div>
    </body>
    </html>"""

    # 写入HTML文件
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)


# ================================ 主程序 ================================


def main():
    """主函数:读取CSV数据,计算统计量,生成报告"""

    print("=" * 60)
    print("SPC Statistical Analysis Tool v2.0")
    print("=" * 60)
    print()

    # 1. 读取CSV数据
    print(f"📖 Reading data from: {CSV_FILE_PATH}")
    try:
        df = pd.read_csv(
            CSV_FILE_PATH, keep_default_na=True, na_values=["", " ", "null", "NULL"]
        )
        print(f"✅ Loaded {len(df)} rows successfully")
    except FileNotFoundError:
        print(f"❌ Error: File '{CSV_FILE_PATH}' not found!")
        print("Please check the file path in spc_config.py")
        return
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    print()

    # 2. 创建输出目录
    os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

    # 3. 处理每个测试项目
    stats = []
    fig_dict = {}

    print(f"📊 Processing {len(SPEC_LIMITS)} test items...")
    print()

    for param, (lsl, usl) in SPEC_LIMITS.items():
        # 检查列是否存在
        if param not in df.columns:
            print(f"⚠️  Warning: Column '{param}' not found, skipping.")
            continue

        # 数据清洗
        data = pd.to_numeric(df[param], errors="coerce").dropna()

        if len(data) == 0:
            print(f"⚠️  Warning: No valid numeric data for '{param}', skipping.")
            continue

        # 计算统计量
        mean_val = np.mean(data)
        sigma_val = np.std(data, ddof=1)
        cpk = calculate_cpk(data, lsl, usl)

        # Cpk显示值
        if cpk is not None and not np.isinf(cpk):
            cpk_display = f"{cpk:.3f}"
        else:
            cpk_display = "inf"

        # 添加到统计列表
        stats.append(
            {
                "Parameter": param,
                "Mean": f"{mean_val:.4f}",
                "Sigma": f"{sigma_val:.4f}",
                "LSL": f"{lsl:.4f}",
                "USL": f"{usl:.4f}",
                "Cpk": cpk_display,
                "n": len(data),
            }
        )

        # 绘制图表
        img_file = os.path.join(OUTPUT_IMG_DIR, f"{param.replace('/', '_')}.png")
        fig = plot_histogram_with_modern_style(
            data, param, lsl, usl, mean_val, sigma_val, cpk, img_file
        )
        fig_dict[param] = fig

        print(f"  ✓ {param} (n={len(data)}, Cpk={cpk_display})")

    print()
    print(f"✅ Successfully processed {len(stats)} test items")
    print()

    # 4. 生成HTML报告
    print(f"🌐 Generating HTML report: {OUTPUT_HTML}")
    generate_html_report(stats, OUTPUT_IMG_DIR, OUTPUT_HTML)
    print(f"✅ HTML report saved to: {OUTPUT_HTML}")
    print()

    # 5. 生成PDF报告
    print(f"📄 Generating PDF report: {OUTPUT_PDF}")
    generate_pdf_report(stats, fig_dict, OUTPUT_PDF)
    print(f"✅ PDF report saved to: {OUTPUT_PDF}")
    print()

    # 6. 输出统计摘要
    print("=" * 60)
    print("📊 STATISTICAL SUMMARY")
    print("=" * 60)
    print(f"Total Parameters: {len(stats)}")
    print(f"Total Samples: {sum(s['n'] for s in stats)}")

    cpk_values = [float(s["Cpk"]) for s in stats if s["Cpk"] != "inf"]
    if cpk_values:
        print(f"Avg Cpk: {np.mean(cpk_values):.3f}")
        print(f"Min Cpk: {np.min(cpk_values):.3f}")
        print(f"Max Cpk: {np.max(cpk_values):.3f}")

    excellent = len([s for s in stats if s["Cpk"] != "inf" and float(s["Cpk"]) >= 1.33])
    acceptable = len(
        [s for s in stats if s["Cpk"] != "inf" and 1.0 <= float(s["Cpk"]) < 1.33]
    )
    poor = len([s for s in stats if s["Cpk"] != "inf" and float(s["Cpk"]) < 1.0])

    print(f"Cpk ≥ 1.33 (Excellent): {excellent}")
    print(f"1.0 ≤ Cpk < 1.33 (Acceptable): {acceptable}")
    print(f"Cpk < 1.0 (Poor): {poor}")
    print("=" * 60)
    print()
    print("🎉 All reports generated successfully!")
    print(f"   - HTML: {OUTPUT_HTML}")
    print(f"   - PDF:  {OUTPUT_PDF}")
    print(f"   - Images: {OUTPUT_IMG_DIR}/")
    print()


if __name__ == "__main__":
    main()
    print(f"   - PDF:  {OUTPUT_PDF}")
    print(f"   - Images: {OUTPUT_IMG_DIR}/")
    print()


if __name__ == "__main__":
    main()
