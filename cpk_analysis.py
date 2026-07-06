# -*- encoding: utf-8 -*-
"""
@File    :   cpk_analysis.py
@Time    :   2026/06/28
@Author  :   SimonYuan
@Version :   1.0
@Desc    :   基于目标Cpk值的反向分析工具

功能特性:
    1. 用户指定目标Cpk值和数据文件（CSV/Excel）
    2. 根据目标Cpk值，反向计算每列数据的规格上下限
       公式: LSL = μ - 3σ·Cpk,  USL = μ + 3σ·Cpk
    3. 为每列数据绘制直方图（含正态分布曲线和规格限标注）
    4. 生成现代化的HTML报告（响应式卡片布局）
    5. 生成专业的PDF报告（A4尺寸，300 DPI）

命令行使用:
    # 基本用法
    python cpk_analysis.py --file data.csv --cpk 1.33

    # 指定输出路径
    python cpk_analysis.py --file data.xlsx --cpk 1.33 --output ./reports

    # 指定工作表（Excel文件）
    python cpk_analysis.py --file data.xlsx --cpk 1.67 --sheet Sheet1

第三方集成（PyQt/PySide等）:
    from cpk_analysis import analyze_with_cpk

    result = analyze_with_cpk(
        file_path="data.csv",
        target_cpk=1.33,
        output_dir="./reports"
    )
    # result 包含: stats_list, html_path, pdf_path
"""

import argparse
import base64
import os
import warnings
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Optional, Tuple

import matplotlib

matplotlib.use("Agg")  # 使用非交互式后端，支持无GUI环境（服务器/打包exe）

import matplotlib.backends.backend_pdf as pdf_backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm

# 忽略matplotlib/pandas等库产生的警告信息，保持输出整洁
warnings.filterwarnings("ignore")


# ================================ 中文字体配置 ================================


def _configure_chinese_font():
    """
    配置matplotlib中文字体，确保图表标题和标签正确显示中文。

    按优先级依次尝试以下字体:
        1. Microsoft YaHei（微软雅黑）- Windows 默认中文字体
        2. SimHei（黑体）              - Windows 备选
        3. PingFang SC                 - macOS 中文字体
        4. WenQuanYi Micro Hei         - Linux 中文字体

    同时设置负号显示为正常字符（避免 '-' 显示为方块）。
    """
    for font in ["Microsoft YaHei", "SimHei", "PingFang SC", "WenQuanYi Micro Hei"]:
        try:
            plt.rcParams["font.sans-serif"] = [font] + plt.rcParams["font.sans-serif"]
            break
        except Exception:
            continue
    plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号


# ================================ 数据加载 ================================


def load_data(file_path: str, sheet_name=None) -> pd.DataFrame:
    """
    加载CSV或Excel数据文件。

    参数:
        file_path : str
            数据文件的完整路径，支持 .csv 和 .xlsx/.xls 格式
        sheet_name : str 或 int, 可选
            Excel文件的工作表名称或索引（默认: 第一个工作表）
            对CSV文件无效

    返回:
        pd.DataFrame
            加载的数据，仅保留数值类型的列

    异常:
        FileNotFoundError : 文件不存在
        ValueError        : 文件格式不支持或没有数值列
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"数据文件不存在: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        raise ValueError(f"不支持的文件格式: {ext}（仅支持 .csv / .xlsx / .xls）")

    # 仅保留数值类型的列（跳过文本列、日期列等非数值数据）
    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.empty:
        raise ValueError("数据文件中没有找到数值类型的列")

    return numeric_df


# ================================ 统计分析 ================================


def calculate_column_statistics(data: pd.Series, target_cpk: float) -> Dict:
    """
    对单列数据进行完整的统计分析，并根据目标Cpk值反推规格限。

    反向推导公式:
        由 Cpk = min( (USL-μ)/(3σ), (μ-LSL)/(3σ) )
        令两侧对称: LSL = μ - 3σ·Cpk,  USL = μ + 3σ·Cpk

    参数:
        data : pd.Series
            单列数值数据
        target_cpk : float
            用户指定的目标Cpk值

    返回:
        dict
            包含以下键值:
            - column: str      - 列名
            - count: int       - 有效样本数
            - mean: float      - 均值(μ)
            - std: float       - 标准差(σ)
            - min: float       - 最小值
            - max: float       - 最大值
            - target_cpk       - 目标Cpk值
            - lsl: float       - 计算得到的规格下限
            - usl: float       - 计算得到的规格上限
            - cpk_achieved     - 实际达到的Cpk值（应等于目标值）
            - valid: bool      - 数据是否有效（样本数≥2且标准差>0）
    """
    clean_data = data.dropna()
    count = len(clean_data)

    if count < 2:
        return {
            "column": data.name,
            "count": count,
            "mean": np.nan,
            "std": np.nan,
            "min": np.nan,
            "max": np.nan,
            "target_cpk": target_cpk,
            "lsl": np.nan,
            "usl": np.nan,
            "cpk_achieved": np.nan,
            "valid": False,
        }

    mean_val = float(clean_data.mean())
    std_val = float(clean_data.std(ddof=1))  # 样本标准差（贝塞尔校正）
    min_val = float(clean_data.min())
    max_val = float(clean_data.max())

    # 标准差为0：所有数据完全相同，无法计算有意义的规格限
    if std_val == 0 or np.isnan(std_val):
        return {
            "column": data.name,
            "count": count,
            "mean": mean_val,
            "std": 0.0,
            "min": min_val,
            "max": max_val,
            "target_cpk": target_cpk,
            "lsl": mean_val,
            "usl": mean_val,
            "cpk_achieved": float("inf"),
            "valid": False,
        }

    # ---- 核心公式：根据目标Cpk反推规格限 ----
    # LSL = μ - 3σ × Cpk
    lsl = mean_val - 3 * std_val * target_cpk
    # USL = μ + 3σ × Cpk
    usl = mean_val + 3 * std_val * target_cpk

    # 验证：用计算出的规格限反算Cpk，应等于目标值
    cpk_achieved = min(
        (usl - mean_val) / (3 * std_val), (mean_val - lsl) / (3 * std_val)
    )

    return {
        "column": data.name,
        "count": count,
        "mean": mean_val,
        "std": std_val,
        "min": min_val,
        "max": max_val,
        "target_cpk": target_cpk,
        "lsl": lsl,
        "usl": usl,
        "cpk_achieved": cpk_achieved,
        "valid": True,
    }


def analyze_all_columns(df: pd.DataFrame, target_cpk: float) -> List[Dict]:
    """
    对数据框中所有数值列进行统计分析。

    参数:
        df : pd.DataFrame
            包含数值数据的数据框
        target_cpk : float
            用户指定的目标Cpk值

    返回:
        list[dict]
            每列的统计分析结果列表（结构同 calculate_column_statistics 的返回值）
    """
    results = []
    for col in df.columns:
        stats = calculate_column_statistics(df[col], target_cpk)
        results.append(stats)
    return results


# ================================ 图表绘制 ================================


def _plot_histogram(
    data: pd.Series, stats: Dict, fig_width: float = 10, fig_height: float = 5
) -> plt.Figure:
    """
    为单列数据绘制直方图，包含正态分布曲线和规格限标注。

    图表元素:
        - 蓝色半透明直方图（密度归一化）
        - 红色正态分布拟合曲线
        - 绿色虚线：均值(μ)
        - 橙色虚线：规格下限(LSL)和规格上限(USL)
        - 标题显示列名、Cpk值和规格限

    参数:
        data : pd.Series
            单列数值数据
        stats : dict
            该列的统计分析结果（由 calculate_column_statistics 返回）
        fig_width : float
            图表宽度（英寸），默认10
        fig_height : float
            图表高度（英寸），默认5

    返回:
        matplotlib.figure.Figure
            绘制完成的图表对象
    """
    clean_data = data.dropna().values

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # --- 直方图（密度归一化，便于与概率密度曲线叠加）---
    ax.hist(
        clean_data,
        bins=30,
        density=True,
        alpha=0.6,
        color="#4C72B0",
        edgecolor="white",
        label="数据分布",
    )

    # --- 正态分布拟合曲线 ---
    x_range = np.linspace(
        stats["min"] - 3 * stats["std"], stats["max"] + 3 * stats["std"], 200
    )
    pdf_curve = norm.pdf(x_range, stats["mean"], stats["std"])
    ax.plot(x_range, pdf_curve, "r-", linewidth=2, label="正态分布拟合")

    # --- 均值线（绿色虚线）---
    ax.axvline(
        stats["mean"],
        color="#2ca02c",
        linestyle="--",
        linewidth=1.5,
        label=f"μ = {stats['mean']:.4f}",
    )

    # --- 规格下限 LSL（橙色虚线）---
    ax.axvline(
        stats["lsl"],
        color="#ff7f0e",
        linestyle="--",
        linewidth=1.5,
        label=f"LSL = {stats['lsl']:.4f}",
    )

    # --- 规格上限 USL（橙色虚线）---
    ax.axvline(
        stats["usl"],
        color="#ff7f0e",
        linestyle="--",
        linewidth=1.5,
        label=f"USL = {stats['usl']:.4f}",
    )

    # --- 标题和标签 ---
    ax.set_title(
        f"{stats['column']}  |  Cpk = {stats['cpk_achieved']:.2f}  |  "
        f"LSL = {stats['lsl']:.4f}    USL = {stats['usl']:.4f}",
        fontsize=12,
        fontweight="bold",
    )
    ax.set_xlabel("测量值", fontsize=10)
    ax.set_ylabel("概率密度", fontsize=10)
    ax.legend(loc="upper right", fontsize=8, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def _fig_to_base64(fig: plt.Figure) -> str:
    """
    将matplotlib图表对象转换为Base64编码的PNG字符串。
    用于嵌入HTML报告中，避免外部图片文件依赖。

    参数:
        fig : matplotlib.figure.Figure
            图表对象

    返回:
        str
            Base64编码的PNG图片字符串
    """
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_base64


# ================================ HTML报告 ================================


def generate_html_report(
    stats_list: List[Dict], file_path: str, target_cpk: float, output_path: str
) -> str:
    """
    生成现代化的HTML分析报告。

    报告结构:
        1. 报告头部 — 标题、数据文件信息、目标Cpk值
        2. 汇总表格 — 所有列的统计结果，Cpk颜色标识
        3. 详细图表 — 每列的直方图（Base64内嵌）

    颜色规则:
        - 绿色(#4CAF50): Cpk ≥ 目标值（达标）
        - 红色(#f44336): Cpk < 目标值（未达标）

    参数:
        stats_list : list[dict]
            各列的统计分析结果
        file_path : str
            原始数据文件路径（用于报告显示）
        target_cpk : float
            用户指定的目标Cpk值
        output_path : str
            HTML报告的输出完整路径

    返回:
        str
            生成的HTML文件路径
    """
    _configure_chinese_font()

    # 统计有效/无效的列数
    valid_stats = [s for s in stats_list if s["valid"]]
    invalid_count = len(stats_list) - len(valid_stats)

    # 预加载原始数据（避免在循环中重复读取文件）
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            raw_df = pd.read_csv(file_path)
        else:
            raw_df = pd.read_excel(file_path)
    except Exception:
        raw_df = None

    # ---- 构建HTML内容 ----
    html_parts = []

    # 头部
    html_parts.append(f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPC Cpk分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 30px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }}
        .header h1 {{
            font-size: 28px;
            color: #333;
            margin-bottom: 16px;
        }}
        .header-info {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            font-size: 14px;
            color: #666;
        }}
        .header-info span {{
            background: #f0f2f5;
            padding: 6px 16px;
            border-radius: 8px;
        }}
        .summary {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }}
        .summary h2 {{
            font-size: 20px;
            color: #333;
            margin-bottom: 16px;
        }}
        .summary-stats {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }}
        .stat-card {{
            flex: 1;
            min-width: 120px;
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            background: #f8f9fa;
        }}
        .stat-card .number {{
            font-size: 32px;
            font-weight: bold;
        }}
        .stat-card .label {{
            font-size: 13px;
            color: #888;
            margin-top: 4px;
        }}
        .pass {{ color: #4CAF50; }}
        .fail {{ color: #f44336; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        th {{
            background: #f8f9fa;
            padding: 12px 8px;
            text-align: center;
            font-weight: 600;
            color: #555;
            border-bottom: 2px solid #e0e0e0;
        }}
        td {{
            padding: 10px 8px;
            text-align: center;
            border-bottom: 1px solid #eee;
            color: #333;
        }}
        tr:hover {{ background: #f5f5f5; }}
        .cpk-badge {{
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 13px;
        }}
        .cpk-pass {{ background: #e8f5e9; color: #2e7d32; }}
        .cpk-fail {{ background: #ffebee; color: #c62828; }}
        .chart-card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }}
        .chart-card h3 {{
            font-size: 16px;
            color: #333;
            margin-bottom: 16px;
        }}
        .chart-card img {{
            width: 100%;
            border-radius: 8px;
        }}
        .footer {{
            text-align: center;
            color: rgba(255,255,255,0.7);
            font-size: 12px;
            padding: 20px;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📊 SPC Cpk 分析报告</h1>
        <div class="header-info">
            <span>📁 数据文件: {os.path.basename(file_path)}</span>
            <span>🎯 目标Cpk: {target_cpk}</span>
            <span>📅 分析时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
        </div>
    </div>
""")

    # 汇总卡片
    html_parts.append(f"""
    <div class="summary">
        <h2>📋 分析汇总</h2>
        <div class="summary-stats">
            <div class="stat-card">
                <div class="number">{len(stats_list)}</div>
                <div class="label">总参数数</div>
            </div>
            <div class="stat-card">
                <div class="number pass">{len(valid_stats)}</div>
                <div class="label">有效参数</div>
            </div>
            <div class="stat-card">
                <div class="number fail">{invalid_count}</div>
                <div class="label">无效参数</div>
            </div>
            <div class="stat-card">
                <div class="number">{target_cpk}</div>
                <div class="label">目标Cpk</div>
            </div>
        </div>
    </div>
""")

    # 汇总表格
    html_parts.append("""
    <div class="summary">
        <h2>📊 详细数据</h2>
        <table>
            <thead>
                <tr>
                    <th>序号</th>
                    <th>参数名称</th>
                    <th>样本数</th>
                    <th>均值(μ)</th>
                    <th>标准差(σ)</th>
                    <th>最小值</th>
                    <th>最大值</th>
                    <th>LSL</th>
                    <th>USL</th>
                    <th>Cpk</th>
                    <th>公差范围</th>
                </tr>
            </thead>
            <tbody>
""")

    for idx, s in enumerate(stats_list, 1):
        if not s["valid"]:
            html_parts.append(f"""
                <tr>
                    <td>{idx}</td>
                    <td style="text-align:left; font-weight:500;">{s["column"]}</td>
                    <td>{s["count"]}</td>
                    <td colspan="8" style="color:#999;">数据无效（样本不足或标准差为零）</td>
                </tr>""")
            continue

        # 计算公差范围（USL - LSL），用于评估规格合理性
        tolerance = s["usl"] - s["lsl"]

        html_parts.append(f"""
                <tr>
                    <td>{idx}</td>
                    <td style="text-align:left; font-weight:500;">{s["column"]}</td>
                    <td>{s["count"]}</td>
                    <td>{s["mean"]:.4f}</td>
                    <td>{s["std"]:.4f}</td>
                    <td>{s["min"]:.4f}</td>
                    <td>{s["max"]:.4f}</td>
                    <td>{s["lsl"]:.4f}</td>
                    <td>{s["usl"]:.4f}</td>
                    <td><span class="cpk-badge cpk-pass">{s["cpk_achieved"]:.2f}</span></td>
                    <td>{tolerance:.4f}</td>
                </tr>""")

    html_parts.append("""
            </tbody>
        </table>
    </div>
""")

    # ---- 详细图表（每列一张直方图，Base64内嵌到HTML中）----
    for s in stats_list:
        if not s["valid"] or raw_df is None:
            continue
        # 从预加载的DataFrame中获取对应列的数据
        if s["column"] not in raw_df.columns:
            continue
        col_data = raw_df[s["column"]].dropna()
        if len(col_data) < 2:
            continue

        # 绘制直方图并转换为Base64字符串
        fig = _plot_histogram(col_data, s)
        img_b64 = _fig_to_base64(fig)

        html_parts.append(f"""
    <div class="chart-card">
        <h3>📈 {s["column"]}</h3>
        <img src="data:image/png;base64,{img_b64}" alt="{s["column"]}">
    </div>
""")

    # 页脚
    html_parts.append(f"""
    <div class="footer">
        SPC Cpk分析报告 — 由 SPC统计分析工具 自动生成 — {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    </div>
</div>
</body>
</html>
""")

    # 写入文件
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

    return output_path


# ================================ PDF报告 ================================


def generate_pdf_report(
    stats_list: List[Dict], file_path: str, target_cpk: float, output_path: str
) -> str:
    """
    生成专业的PDF分析报告（A4尺寸，300 DPI）。

    报告结构:
        第1页: 封面 + 汇总表格
        后续页: 每页2个直方图（2×1布局）

    参数:
        stats_list : list[dict]
            各列的统计分析结果
        file_path : str
            原始数据文件路径
        target_cpk : float
            用户指定的目标Cpk值
        output_path : str
            PDF报告的输出完整路径

    返回:
        str
            生成的PDF文件路径
    """
    _configure_chinese_font()

    valid_stats = [s for s in stats_list if s["valid"]]
    invalid_count = len(stats_list) - len(valid_stats)

    # A4尺寸（英寸）: 210mm × 297mm
    A4_W, A4_H = 8.27, 11.69

    # 预加载原始数据用于绘制直方图（避免在循环中重复读取文件）
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            raw_df = pd.read_csv(file_path)
        else:
            raw_df = pd.read_excel(file_path)
    except Exception:
        raw_df = None

    with pdf_backend.PdfPages(output_path) as pdf_out:
        # ==================== 第1页: 封面 + 汇总表 ====================
        fig = plt.figure(figsize=(A4_W, A4_H))

        # 顶部标题区域
        ax_header = fig.add_axes([0.05, 0.88, 0.9, 0.10])
        ax_header.set_xlim(0, 1)
        ax_header.set_ylim(0, 1)
        ax_header.axis("off")
        ax_header.text(
            0.5,
            0.65,
            "SPC Cpk 分析报告",
            ha="center",
            va="center",
            fontsize=24,
            fontweight="bold",
            color="#333333",
        )
        ax_header.text(
            0.5,
            0.25,
            f"数据文件: {os.path.basename(file_path)}    |    "
            f"目标Cpk: {target_cpk}    |    "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ha="center",
            va="center",
            fontsize=10,
            color="#666666",
        )

        # 汇总信息
        ax_summary = fig.add_axes([0.05, 0.78, 0.9, 0.08])
        ax_summary.set_xlim(0, 1)
        ax_summary.set_ylim(0, 1)
        ax_summary.axis("off")
        ax_summary.text(
            0.5,
            0.5,
            f"总参数: {len(stats_list)}    |    "
            f"有效: {len(valid_stats)}    |    "
            f"无效: {invalid_count}    |    "
            f"目标Cpk: {target_cpk}",
            ha="center",
            va="center",
            fontsize=12,
            color="#444",
        )

        # 汇总表格
        col_labels = [
            "序号",
            "参数名称",
            "样本数",
            "均值",
            "标准差",
            "最小值",
            "最大值",
            "LSL",
            "USL",
            "Cpk",
            "公差范围",
        ]
        n_rows = len(stats_list) + 1  # +1 for header
        col_widths = [0.04, 0.16, 0.06, 0.09, 0.08, 0.09, 0.09, 0.09, 0.09, 0.07, 0.07]

        table_data = []
        for idx, s in enumerate(stats_list, 1):
            if s["valid"]:
                cpk_str = f"{s['cpk_achieved']:.2f}"
                tolerance = f"{s['usl'] - s['lsl']:.4f}"
                table_data.append(
                    [
                        str(idx),
                        str(s["column"]),
                        str(s["count"]),
                        f"{s['mean']:.4f}",
                        f"{s['std']:.4f}",
                        f"{s['min']:.4f}",
                        f"{s['max']:.4f}",
                        f"{s['lsl']:.4f}",
                        f"{s['usl']:.4f}",
                        cpk_str,
                        tolerance,
                    ]
                )
            else:
                table_data.append(
                    [
                        str(idx),
                        str(s["column"]),
                        str(s["count"]),
                        "—",
                        "—",
                        "—",
                        "—",
                        "—",
                        "—",
                        "—",
                        "—",
                    ]
                )

        ax_table = fig.add_axes([0.03, 0.05, 0.94, 0.70])
        ax_table.axis("off")

        table = ax_table.table(
            cellText=table_data,
            colLabels=col_labels,
            colWidths=col_widths,
            loc="center",
            cellLoc="center",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(7)
        table.scale(1, 1.4)

        # 表头样式
        for j in range(len(col_labels)):
            cell = table[0, j]
            cell.set_facecolor("#4C72B0")
            cell.set_text_props(color="white", fontweight="bold", fontsize=7)
            cell.set_edgecolor("white")

        # 数据行样式（斑马纹 + Cpk颜色标识）
        for i in range(1, len(table_data) + 1):
            bg = "#f0f4f8" if i % 2 == 0 else "white"
            for j in range(len(col_labels)):
                cell = table[i, j]
                cell.set_facecolor(bg)
                cell.set_edgecolor("#dddddd")

        pdf_out.savefig(fig, dpi=300)
        plt.close(fig)

        # ==================== 后续页: 直方图 ====================
        valid_items = [s for s in stats_list if s["valid"]]

        if raw_df is not None:
            # 每页2个图表（2行×1列）
            for page_start in range(0, len(valid_items), 2):
                page_items = valid_items[page_start : page_start + 2]
                n_charts = len(page_items)

                fig = plt.figure(figsize=(A4_W, A4_H))

                # 页眉
                fig.text(
                    0.5,
                    0.97,
                    f"SPC Cpk 分析报告 — 详细图表",
                    ha="center",
                    va="top",
                    fontsize=14,
                    fontweight="bold",
                    color="#333333",
                )
                fig.text(
                    0.5,
                    0.945,
                    f"目标Cpk: {target_cpk}    |    "
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    ha="center",
                    va="top",
                    fontsize=9,
                    color="#888888",
                )

                for chart_idx, s in enumerate(page_items):
                    if s["column"] not in raw_df.columns:
                        continue
                    col_data = raw_df[s["column"]].dropna()
                    if len(col_data) < 2:
                        continue

                    # 计算图表位置（留出页眉和边距空间）
                    # [left, bottom, width, height]
                    if n_charts == 1:
                        ax = fig.add_axes([0.08, 0.35, 0.84, 0.50])
                    else:
                        if chart_idx == 0:
                            ax = fig.add_axes([0.08, 0.52, 0.84, 0.38])
                        else:
                            ax = fig.add_axes([0.08, 0.08, 0.84, 0.38])

                    # 在当前axes上绘制直方图
                    clean_data = col_data.values
                    ax.hist(
                        clean_data,
                        bins=30,
                        density=True,
                        alpha=0.6,
                        color="#4C72B0",
                        edgecolor="white",
                        label="数据分布",
                    )

                    x_range = np.linspace(
                        s["min"] - 3 * s["std"], s["max"] + 3 * s["std"], 200
                    )
                    pdf_curve = norm.pdf(x_range, s["mean"], s["std"])
                    ax.plot(x_range, pdf_curve, "r-", linewidth=2, label="正态分布拟合")
                    ax.axvline(
                        s["mean"],
                        color="#2ca02c",
                        linestyle="--",
                        linewidth=1.5,
                        label=f"μ = {s['mean']:.4f}",
                    )
                    ax.axvline(
                        s["lsl"],
                        color="#ff7f0e",
                        linestyle="--",
                        linewidth=1.5,
                        label=f"LSL = {s['lsl']:.4f}",
                    )
                    ax.axvline(
                        s["usl"],
                        color="#ff7f0e",
                        linestyle="--",
                        linewidth=1.5,
                        label=f"USL = {s['usl']:.4f}",
                    )

                    ax.set_title(
                        f"{s['column']}  |  Cpk = {s['cpk_achieved']:.2f}",
                        fontsize=11,
                        fontweight="bold",
                    )
                    ax.set_xlabel("测量值", fontsize=9)
                    ax.set_ylabel("概率密度", fontsize=9)
                    ax.legend(loc="upper right", fontsize=7, framealpha=0.9)
                    ax.grid(True, alpha=0.3)

                pdf_out.savefig(fig, dpi=300)
                plt.close(fig)

    return output_path


# ================================ 主函数 ================================


def analyze_with_cpk(
    file_path: str,
    target_cpk: float,
    output_dir: Optional[str] = None,
    sheet_name: Optional[str] = None,
) -> Dict:
    """
    基于目标Cpk值的数据分析主函数（推荐第三方集成使用此函数）。

    完整流程:
        1. 加载数据文件（CSV/Excel）
        2. 计算每列的统计量（均值、标准差、最值）
        3. 根据目标Cpk反推每列的规格上下限（LSL/USL）
        4. 生成HTML报告
        5. 生成PDF报告

    参数:
        file_path : str
            数据文件路径（.csv / .xlsx / .xls）
        target_cpk : float
            目标Cpk值（如 1.0, 1.33, 1.67, 2.0）
        output_dir : str, 可选
            报告输出目录（默认: 数据文件所在目录下的 cpk_reports 子目录）
        sheet_name : str, 可选
            Excel文件的工作表名称（对CSV无效）

    返回:
        dict
            {
                'stats_list': list[dict],  # 各列的统计分析结果
                'html_path': str,          # HTML报告路径
                'pdf_path': str,           # PDF报告路径
                'file_path': str,          # 数据文件路径
                'target_cpk': float,       # 目标Cpk值
            }

    使用示例:
        >>> result = analyze_with_cpk("test_data.csv", target_cpk=1.33)
        >>> for s in result['stats_list']:
        ...     print(f"{s['column']}: Cpk={s['cpk_achieved']:.2f}, "
        ...           f"LSL={s['lsl']:.4f}, USL={s['usl']:.4f}")
    """
    # 确定输出目录
    if output_dir is None:
        base_dir = os.path.dirname(os.path.abspath(file_path))
        output_dir = os.path.join(base_dir, "cpk_reports")
    os.makedirs(output_dir, exist_ok=True)

    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    html_path = os.path.join(output_dir, f"{base_name}_cpk_{timestamp}.html")
    pdf_path = os.path.join(output_dir, f"{base_name}_cpk_{timestamp}.pdf")

    # 步骤1: 加载数据
    print(f"📂 加载数据文件: {file_path}")
    df = load_data(file_path, sheet_name=sheet_name)
    print(f"   共 {len(df.columns)} 个数值列, {len(df)} 行数据")

    # 步骤2-3: 计算统计量和规格限
    print(f"🎯 目标Cpk值: {target_cpk}")
    print(f"📊 正在计算各列统计量和规格限...")
    stats_list = analyze_all_columns(df, target_cpk)

    # 打印简要结果
    for s in stats_list:
        if s["valid"]:
            print(
                f"   📊 {s['column']}: Cpk={s['cpk_achieved']:.2f}, "
                f"LSL={s['lsl']:.4f}, USL={s['usl']:.4f}, "
                f"公差={s['usl'] - s['lsl']:.4f}"
            )
        else:
            print(f"   ⚠️ {s['column']}: 数据无效（样本不足或标准差为零）")

    # 步骤4: 生成HTML报告
    print(f"📄 生成HTML报告: {html_path}")
    generate_html_report(stats_list, file_path, target_cpk, html_path)

    # 步骤5: 生成PDF报告
    print(f"📄 生成PDF报告: {pdf_path}")
    generate_pdf_report(stats_list, file_path, target_cpk, pdf_path)

    # 汇总统计
    valid_stats = [s for s in stats_list if s["valid"]]

    print()
    print("=" * 60)
    print(f"🎉 报告生成完成！")
    print(f"   HTML: {html_path}")
    print(f"   PDF:  {pdf_path}")
    print(f"   总参数: {len(stats_list)}, 有效: {len(valid_stats)}")
    print("=" * 60)

    return {
        "stats_list": stats_list,
        "html_path": html_path,
        "pdf_path": pdf_path,
        "file_path": file_path,
        "target_cpk": target_cpk,
    }


# ================================ 命令行入口 ================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SPC Cpk反向分析工具 — 根据目标Cpk值计算规格限并生成分析报告"
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        required=True,
        help="数据文件路径（支持 .csv / .xlsx / .xls）",
    )
    parser.add_argument(
        "--cpk",
        "-c",
        type=float,
        required=True,
        help="目标Cpk值（如 1.0, 1.33, 1.67, 2.0）",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="报告输出目录（默认: 数据文件目录下的 cpk_reports）",
    )
    parser.add_argument(
        "--sheet",
        "-s",
        type=str,
        default=None,
        help="Excel工作表名称（仅对.xlsx/.xls文件有效）",
    )
    args = parser.parse_args()

    analyze_with_cpk(
        file_path=args.file,
        target_cpk=args.cpk,
        output_dir=args.output,
        sheet_name=args.sheet,
    )
