# -*- encoding: utf-8 -*-
"""
@File    :   spc_analysis.py
@Time    :   2026/06/17
@Author  :   SimonYuan
@Version :   2.1
@Desc    :   通用SPC统计分析程序 - 现代化的PDF和HTML报告生成

功能特性:
1. 从YAML配置文件读取测试项目和规格限
2. 自动计算Cpk、Mean、Sigma等统计量
3. 生成现代化的PDF报告(A4尺寸,专业排版)
4. 生成响应式HTML报告(渐变背景,卡片布局)
5. 智能Cpk彩色标识
6. 长参数名自动换行

命令行使用:
    # 处理默认配置中的第一个项目
    python spc_analysis.py

    # 指定配置文件和项目
    python spc_analysis.py --config spc_config.yaml --project ehm_module_test

第三方集成（PyQt/PySide等）:
    from spc_analysis import main
    from config_loader import ConfigLoader

    loader = ConfigLoader("spc_config.yaml")
    config = loader.get_project("your_project_id")
    main(config=config)   # 直接传入ProjectConfig对象即可
"""

import os
import warnings
from typing import Dict, List, Optional, Tuple

import matplotlib.backends.backend_pdf as pdf_backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm

# 忽略matplotlib/pandas等库产生的警告信息，保持输出整洁
warnings.filterwarnings("ignore")

# 导入配置加载器（兼容包内导入和直接运行两种模式）
try:
    from .config_loader import ConfigLoader, ProjectConfig
except ImportError:
    from config_loader import ConfigLoader, ProjectConfig


# ================================ 统计计算 ================================


def calculate_cpk(data, lsl: float, usl: float) -> Optional[float]:
    """
    计算Cpk（过程能力指数）

    Cpk 衡量的是过程均值偏离规格中心的程度，同时考虑了过程的离散程度。
    公式: Cpk = min( (USL - μ) / (3σ),  (μ - LSL) / (3σ) )

    参数:
        data : array-like
            一维数值数组（样本数据），长度至少为2
        lsl : float
            规格下限（Lower Specification Limit）
        usl : float
            规格上限（Upper Specification Limit）

    返回:
        float 或 None
            - 正常情况返回 Cpk 值（float）
            - 若 sigma == 0（所有数据完全相同），返回 np.inf
            - 若数据不足（len < 2），返回 None

    使用示例:
        >>> import numpy as np
        >>> data = np.array([3.30, 3.32, 3.35, 3.31, 3.33])
        >>> calculate_cpk(data, lsl=3.2, usl=3.45)
        1.234...
    """
    if len(data) < 2:
        return None

    mu = np.mean(data)
    sigma = np.std(data, ddof=1)  # ddof=1 表示样本标准差（除以 n-1）

    if sigma == 0:
        return np.inf

    cpk = min((usl - mu) / (3 * sigma), (mu - lsl) / (3 * sigma))
    return cpk


# ================================ 图表绘制 ================================


def plot_histogram_with_modern_style(
    data,
    param_name: str,
    lsl: float,
    usl: float,
    mean: float,
    std: float,
    cpk: float,
    image_path: str,
) -> plt.Figure:
    """
    绘制现代化的直方图 + 正态分布拟合曲线，并保存为PNG图片。

    生成的图表包含:
    - 蓝色半透明直方图（数据分布）
    - 红色正态分布拟合曲线
    - 绿色虚线标注的规格上下限（LSL / USL）
    - 橙色实线标注的均值线
    - 左上角 Cpk 信息框（颜色根据 Cpk 值自动变化）

    参数:
        data : array-like
            一维数值数组
        param_name : str
            参数名称（显示在标题中）
        lsl : float
            规格下限
        usl : float
            规格上限
        mean : float
            样本均值
        std : float
            样本标准差
        cpk : float
            过程能力指数
        image_path : str
            PNG图片保存路径

    返回:
        matplotlib.figure.Figure
            生成的Figure对象（调用者负责 plt.close()）
    """
    # 创建A4尺寸的figure（横向: 11.69 x 8.27 英寸，300 DPI）
    fig = plt.figure(figsize=(11.69, 8.27), dpi=300)

    # 创建主坐标轴,留出标题和说明空间 [left, bottom, width, height]
    ax = fig.add_axes([0.10, 0.15, 0.82, 0.72])

    # --- 绘制直方图 ---
    # bins数量取30和唯一值数量的较小值，避免过多空柱
    n, bins, patches = ax.hist(
        data,
        bins=min(30, len(np.unique(data))),
        density=True,          # 归一化为概率密度
        alpha=0.7,
        color="#3498db",       # 蓝色
        edgecolor="#2980b9",
        linewidth=1.0,
        label="Data Distribution",
    )

    # --- 绘制拟合正态曲线 ---
    # 在数据范围内生成300个等距点，计算对应的正态分布概率密度
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

    # --- 绘制规格限（LSL/USL）和均值线 ---
    ax.axvline(lsl, color="#27ae60", linestyle="--", lw=2.5,
               label=f"LSL = {lsl:.3f}", alpha=0.8)
    ax.axvline(usl, color="#27ae60", linestyle="--", lw=2.5,
               label=f"USL = {usl:.3f}", alpha=0.8)
    ax.axvline(mean, color="#e67e22", linestyle="-", lw=2.5,
               label=f"Mean = {mean:.3f}", alpha=0.9)

    # --- 智能Cpk显示 ---
    # 根据Cpk值选择不同颜色和符号：
    #   Cpk >= 1.33  →  绿色 ✓（优秀）
    #   1.0 <= Cpk < 1.33  →  黄色 ⚠（可接受）
    #   Cpk < 1.0    →  红色 ✗（不合格）
    #   Cpk == inf   →  绿色 ∞（标准差为0）
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

    # Cpk信息框(放在左上角，带圆角边框)
    ax.text(
        0.02, 0.97, cpk_text,
        transform=ax.transAxes,
        fontsize=14, fontweight="bold",
        verticalalignment="top", horizontalalignment="left",
        color=cpk_color,
        bbox=dict(boxstyle="round,pad=0.6", facecolor="white",
                  edgecolor=cpk_color, alpha=0.95, linewidth=2),
    )

    # --- 处理长参数名（自动换行） ---
    # 当下划线替换为空格后超过60字符时，按单词边界自动折行
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

    # --- 标题和标签 ---
    ax.set_title(f"Parameter: {display_name}", fontsize=16,
                 fontweight="bold", pad=20, color="#2c3e50")

    # 副标题（样本数，显示在x轴下方）
    ax.text(0.5, -0.15, f"Sample Size: n = {len(data)}",
            transform=ax.transAxes, fontsize=11, ha="center", color="#7f8c8d")

    ax.set_xlabel("Value", fontsize=13, fontweight="bold", color="#2c3e50", labelpad=10)
    ax.set_ylabel("Probability Density", fontsize=13, fontweight="bold",
                  color="#2c3e50", labelpad=10)

    # 图例（右上角）
    ax.legend(loc="upper right", fontsize=9.5, framealpha=0.9,
              edgecolor="#bdc3c7", facecolor="#f8f9fa")

    # 网格（半透明虚线）
    ax.grid(True, alpha=0.3, linestyle="--", linewidth=0.8, color="#95a5a6")

    # 刻度样式
    ax.tick_params(axis="both", which="major", labelsize=10, colors="#34495e")

    # 坐标轴边框颜色
    for spine in ax.spines.values():
        spine.set_color("#bdc3c7")
        spine.set_linewidth(1.2)

    # 自动调整布局
    plt.tight_layout()

    # 保存PNG图片（150 DPI，用于嵌入HTML报告）
    plt.savefig(image_path, dpi=150, bbox_inches="tight")

    return fig


# ================================ PDF报告生成 ================================


def generate_pdf_report(
    stats: List[Dict],
    fig_dict: Dict[str, plt.Figure],
    output_pdf: str,
):
    """
    生成专业的PDF统计报告。

    报告结构:
    1. 统计表格页（每页最多20行，自动分页）
    2. 每个参数各一页的分布图

    参数:
        stats : list of dict
            统计结果列表，每个dict包含:
            {Parameter, Mean, Sigma, LSL, USL, Cpk, n}
        fig_dict : dict
            {参数名: Figure对象} 的映射，由 plot_histogram_with_modern_style() 返回
        output_pdf : str
            输出PDF文件路径
    """
    with pdf_backend.PdfPages(output_pdf) as pdf:
        # ====== 第一部分: 统计表格（自动分页） ======
        rows_per_page = 20  # 每页最多显示行数
        total_rows = len(stats)
        total_pages = (total_rows + rows_per_page - 1) // rows_per_page

        for page_idx in range(total_pages):
            # 创建A4尺寸的figure
            fig_table = plt.figure(figsize=(11.69, 8.27), dpi=300)

            # 获取当前页数据切片
            start_idx = page_idx * rows_per_page
            end_idx = min(start_idx + rows_per_page, total_rows)
            page_stats = stats[start_idx:end_idx]
            actual_rows = len(page_stats)

            # 准备表格数据（转换为字符串列表）
            table_data = []
            for s in page_stats:
                table_data.append([
                    s["Parameter"], s["Mean"], s["Sigma"],
                    s["LSL"], s["USL"], s["Cpk"], str(s["n"]),
                ])

            columns = ["Parameter", "Mean", "Sigma", "LSL", "USL", "Cpk", "n"]

            # 创建坐标轴（几乎占满整页，留出标题空间）
            ax = fig_table.add_axes([0.05, 0.05, 0.90, 0.88])
            ax.axis("off")

            # 创建表格，指定各列宽度比例
            table = ax.table(
                cellText=table_data, colLabels=columns,
                loc="center", cellLoc="center",
                colWidths=[0.32, 0.12, 0.12, 0.11, 0.11, 0.11, 0.11],
            )

            # 表格整体字体和行高
            table.auto_set_font_size(False)
            table.set_fontsize(7)
            table.scale(1, 1.5)

            # 设置表头样式（深色背景 + 白色粗体字）
            for col_idx in range(len(columns)):
                cell = table[0, col_idx]
                cell.set_facecolor("#2c3e50")
                cell.set_text_props(color="white", fontweight="bold", fontsize=7.5)
                cell.set_edgecolor("#34495e")
                cell.set_linewidth(1.5)

            # 设置数据行样式（交替行背景色 + 细边框）
            for row_idx in range(1, actual_rows + 1):
                # 奇数行白色，偶数行浅灰
                bg_color = "#ffffff" if row_idx % 2 == 1 else "#f8f9fa"

                for col_idx in range(len(columns)):
                    cell = table[row_idx, col_idx]
                    cell.set_facecolor(bg_color)
                    cell.set_edgecolor("#dee2e6")
                    cell.set_linewidth(0.5)
                    # 数据列居中对齐
                    if col_idx > 0:
                        cell.set_text_props(ha="center", va="center")

                # Parameter列特殊处理: 左对齐 + 长文本按下划线自动换行
                param_cell = table[row_idx, 0]
                param_text = param_cell.get_text().get_text()

                if len(param_text) > 28:
                    # 按下划线分割，逐段拼接直到超过28字符后换行
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

            # 添加页面标题（多页时显示页码）
            if total_pages > 1:
                title_text = f"SPC Statistical Summary (Page {page_idx + 1}/{total_pages})"
            else:
                title_text = "SPC Statistical Summary"

            fig_table.text(0.5, 0.96, title_text, ha="center", va="top",
                           fontsize=14, fontweight="bold", color="#2c3e50")

            # 保存当前PDF页并关闭figure释放内存
            pdf.savefig(fig_table, dpi=300, bbox_inches="tight")
            plt.close(fig_table)

        # ====== 第二部分: 分布图（每个参数一页） ======
        for idx, s in enumerate(stats):
            param = s["Parameter"]
            if param in fig_dict:
                fig = fig_dict[param]

                # 在图表底部添加页脚信息
                fig.text(0.5, 0.02,
                         f"SPC Report - {param} ({idx + 1}/{len(stats)})",
                         ha="center", va="bottom", fontsize=8,
                         color="#7f8c8d", alpha=0.7)

                # 保存到PDF并关闭figure
                pdf.savefig(fig, dpi=300, bbox_inches="tight")
                plt.close(fig)


# ================================ HTML报告生成 ================================


def generate_html_report(stats: List[Dict], img_dir: str, output_html: str):
    """
    生成现代化的响应式HTML统计报告。

    报告结构:
    1. 渐变色页眉
    2. 统计概览卡片（总参数数、总样本数、Cpk分布统计）
    3. 统计表格（Cpk值根据大小自动着色）
    4. 分布图卡片网格
    5. 页脚

    参数:
        stats : list of dict
            统计结果列表，每个dict包含:
            {Parameter, Mean, Sigma, LSL, USL, Cpk, n}
        img_dir : str
            分布图PNG图片所在目录
        output_html : str
            输出HTML文件路径
    """
    # HTML模板（包含完整的CSS样式定义）
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

    # --- 生成统计表格行 ---
    # 遍历每个参数的统计数据，根据Cpk值设置不同的CSS颜色类
    for s in stats:
        # 根据Cpk值设置颜色类: cpk-good(绿) / cpk-warning(黄) / cpk-bad(红)
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

    # --- 生成分布图卡片 ---
    # 为每个参数生成一个带标题和图片的卡片
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

    # 写入HTML文件（UTF-8编码，支持中文和特殊字符）
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)


# ================================ 主程序入口 ================================


def main(config: ProjectConfig = None, config_yaml: str = None, project_id: str = None):
    """
    主函数: 读取CSV数据, 计算统计量, 生成HTML和PDF报告。

    这是本模块的唯一入口函数。支持三种调用方式（三选一）:

    方式1 - 直接传入配置对象（推荐用于PyQt/PySide集成）:
        loader = ConfigLoader("spc_config.yaml")
        config = loader.get_project("ehm_module_test")
        main(config=config)

    方式2 - 传入YAML路径 + 项目ID:
        main(config_yaml="spc_config.yaml", project_id="ehm_module_test")

    方式3 - 不传参数（使用默认配置文件中的第一个项目）:
        main()

    参数:
        config : ProjectConfig, optional
            项目配置对象。包含csv_file、output、spec_limits等全部信息。
            传入此参数时，config_yaml和project_id将被忽略。
        config_yaml : str, optional
            YAML配置文件路径。需配合project_id使用。
            若不指定，默认使用脚本同级目录下的 spc_config.yaml。
        project_id : str, optional
            项目唯一标识符（对应YAML中项目的 id 字段）。
            若不指定，使用配置文件中的第一个项目。

    异常:
        FileNotFoundError : CSV数据文件不存在时抛出
        ValueError        : YAML配置格式错误时抛出
    """
    # --- 步骤0: 配置解析 ---
    # 若未直接传入config对象，则从YAML文件中加载
    if config is None:
        loader = ConfigLoader(config_yaml)
        loader.load()
        if project_id:
            config = loader.get_project(project_id)
        else:
            all_projects = loader.get_all_projects()
            config = all_projects[0]

    print("=" * 60)
    print("SPC Statistical Analysis Tool v2.1")
    print("=" * 60)
    print()

    # --- 步骤1: 读取CSV数据 ---
    # 使用pandas读取CSV，自动处理空值和常见缺失值标记
    print(f"📖 Reading data from: {config.csv_file}")
    try:
        df = pd.read_csv(
            config.csv_file, keep_default_na=True, na_values=["", " ", "null", "NULL"]
        )
        print(f"✅ Loaded {len(df)} rows successfully")
    except FileNotFoundError:
        print(f"❌ Error: File '{config.csv_file}' not found!")
        print("Please check the file path in config file")
        return
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    print()

    # --- 步骤2: 创建输出目录 ---
    # 确保图片输出目录存在，若不存在则自动创建
    os.makedirs(config.output.img_dir, exist_ok=True)

    # --- 步骤3: 逐个处理spec_limits中定义的测试参数 ---
    # stats 用于收集表格数据，fig_dict 用于收集分布图
    stats = []
    fig_dict = {}

    print(f"📊 Processing {len(config.spec_limits)} test items...")
    print()

    for param, (lsl, usl) in config.spec_limits.items():
        # 3a. 检查CSV中是否存在该参数的列
        if param not in df.columns:
            print(f"⚠️  Warning: Column '{param}' not found, skipping.")
            continue

        # 3b. 数据清洗: 强制转换为数值类型，无法转换的变为NaN后丢弃
        data = pd.to_numeric(df[param], errors="coerce").dropna()

        if len(data) == 0:
            print(f"⚠️  Warning: No valid numeric data for '{param}', skipping.")
            continue

        # 3c. 计算统计量
        mean_val = np.mean(data)
        sigma_val = np.std(data, ddof=1)  # 样本标准差
        cpk = calculate_cpk(data, lsl, usl)

        # 3d. 格式化Cpk显示值
        if cpk is not None and not np.isinf(cpk):
            cpk_display = f"{cpk:.3f}"
        else:
            cpk_display = "inf"

        # 3e. 将统计结果追加到列表（用于生成表格报告）
        stats.append({
            "Parameter": param,
            "Mean": f"{mean_val:.4f}",
            "Sigma": f"{sigma_val:.4f}",
            "LSL": f"{lsl:.4f}",
            "USL": f"{usl:.4f}",
            "Cpk": cpk_display,
            "n": len(data),
        })

        # 3f. 绘制分布图并保存PNG（用于HTML报告）
        img_file = os.path.join(config.output.img_dir, f"{param.replace('/', '_')}.png")
        fig = plot_histogram_with_modern_style(
            data, param, lsl, usl, mean_val, sigma_val, cpk, img_file
        )
        fig_dict[param] = fig

        print(f"  ✓ {param} (n={len(data)}, Cpk={cpk_display})")

    print()
    print(f"✅ Successfully processed {len(stats)} test items")
    print()

    # --- 步骤4: 生成HTML报告 ---
    print(f"🌐 Generating HTML report: {config.output.html}")
    generate_html_report(stats, config.output.img_dir, config.output.html)
    print(f"✅ HTML report saved to: {config.output.html}")
    print()

    # --- 步骤5: 生成PDF报告 ---
    print(f"📄 Generating PDF report: {config.output.pdf}")
    generate_pdf_report(stats, fig_dict, config.output.pdf)
    print(f"✅ PDF report saved to: {config.output.pdf}")
    print()

    # --- 步骤6: 输出统计摘要到控制台 ---
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
    acceptable = len([s for s in stats if s["Cpk"] != "inf" and 1.0 <= float(s["Cpk"]) < 1.33])
    poor = len([s for s in stats if s["Cpk"] != "inf" and float(s["Cpk"]) < 1.0])

    print(f"Cpk ≥ 1.33 (Excellent): {excellent}")
    print(f"1.0 ≤ Cpk < 1.33 (Acceptable): {acceptable}")
    print(f"Cpk < 1.0 (Poor): {poor}")
    print("=" * 60)
    print()
    print("🎉 All reports generated successfully!")
    print(f"   - HTML: {config.output.html}")
    print(f"   - PDF:  {config.output.pdf}")
    print(f"   - Images: {config.output.img_dir}/")
    print()


# ================================ 命令行入口 ================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="SPC Statistical Analysis Tool - "
                    "从CSV数据生成SPC统计分析报告（HTML + PDF）"
    )
    parser.add_argument(
        "--config", type=str, default=None,
        help="YAML配置文件路径（默认: 脚本同级目录下的 spc_config.yaml）"
    )
    parser.add_argument(
        "--project", type=str, default=None,
        help="项目ID（对应YAML中项目的id字段；不指定则使用第一个项目）"
    )
    args = parser.parse_args()

    main(config_yaml=args.config, project_id=args.project)
