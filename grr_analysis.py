# -*- encoding: utf-8 -*-
"""
@File    :   grr_analysis.py
@Time    :   2026/06/28
@Author  :   SimonYuan
@Version :   1.0
@Desc    :   GRR (Gauge Repeatability & Reproducibility) 分析报告工具

功能特性:
    1. 支持 ANOVA 方差分析法和 AIAG 均值极差法两种 GRR 分析
    2. 自动计算 EV(设备变异)、AV(人员变异)、PV(零件变异) 等分量
    3. 计算 %GRR、ndc(可区分类别数) 等关键指标
    4. 生成 HTML / Markdown / PDF 三种格式的专业报告
    5. 包含丰富的图表: 方差分量图、交互作用图、箱线图等

数据格式 (CSV/Excel, 长表格式):
    operator,part,value
    Operator_A,Part_1,3.35
    Operator_A,Part_1,3.34
    Operator_A,Part_2,3.32
    ...

命令行使用:
    python grr_analysis.py --file grr_data.csv --operator operator --part part --value value
    python grr_analysis.py --file grr_data.xlsx --output ./reports

第三方集成:
    from grr_analysis import analyze_grr
    result = analyze_grr(file_path="grr_data.csv", operator_col="operator",
                         part_col="part", value_col="value")
"""

import os
import base64
import warnings
import argparse
from io import BytesIO
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use('Agg')

import matplotlib.backends.backend_pdf as pdf_backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")


# ================================ 中文字体配置 ================================

def _configure_chinese_font():
    """配置matplotlib中文字体，按优先级尝试 Windows/macOS/Linux 字体。"""
    for font in ['Microsoft YaHei', 'SimHei', 'PingFang SC', 'WenQuanYi Micro Hei']:
        try:
            plt.rcParams['font.sans-serif'] = [font] + plt.rcParams['font.sans-serif']
            break
        except Exception:
            continue
    plt.rcParams['axes.unicode_minus'] = False


# ================================ 统计常量 ================================

# d2 常量: 用于将极差转换为标准差估计, d2[样本大小]
_D2 = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704, 8: 2.847, 9: 2.970, 10: 3.078}

# K1 常量 (AIAG): 用于计算 EV 和 AV, K1[试验次数]
_K1 = {2: 0.8862, 3: 0.5908}

# K2 常量 (AIAG): 用于计算 AV, K2[操作员数量]
_K2 = {2: 0.7071, 3: 0.5231}

# K3 常量 (AIAG): 用于计算 PV, K3[零件数量]
_K3 = {2: 0.7071, 3: 0.5231, 4: 0.4467, 5: 0.4030, 6: 0.3742,
       7: 0.3534, 8: 0.3375, 9: 0.3249, 10: 0.3146,
       15: 0.2726, 20: 0.2526, 30: 0.2313, 50: 0.2085, 100: 0.1851}


# ================================ 数据加载 ================================


def load_grr_data(file_path: str, operator_col: str = 'operator',
                  part_col: str = 'part', value_col: str = 'value',
                  sheet_name=None) -> pd.DataFrame:
    """
    加载 GRR 数据文件并验证格式。

    参数:
        file_path : str       - 数据文件路径 (.csv / .xlsx / .xls)
        operator_col : str    - 操作员列名
        part_col : str        - 零件列名
        value_col : str       - 测量值列名
        sheet_name            - Excel 工作表名称

    返回:
        pd.DataFrame - 包含 operator, part, value 三列的 tidy 格式数据

    异常:
        FileNotFoundError, ValueError
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"数据文件不存在: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext in ('.xlsx', '.xls'):
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        raise ValueError(f"不支持的文件格式: {ext}")

    # 验证必需列
    for col in [operator_col, part_col, value_col]:
        if col not in df.columns:
            raise ValueError(f"找不到列 '{col}'。文件中的列: {list(df.columns)}")

    # 提取并清理数据
    tidy_df = df[[operator_col, part_col, value_col]].copy()
    tidy_df.columns = ['operator', 'part', 'value']
    tidy_df['value'] = pd.to_numeric(tidy_df['value'], errors='coerce')
    tidy_df = tidy_df.dropna(subset=['value'])

    if tidy_df.empty:
        raise ValueError("数据中没有有效的数值记录")

    return tidy_df


def convert_wide_to_long(
    file_path: str,
    n_operators: int = 3,
    n_parts: int = 10,
    operator_names: Optional[List[str]] = None,
    part_names: Optional[List[str]] = None,
    sheet_name: Optional[str] = None
) -> Tuple[pd.DataFrame, List[str]]:
    """
    将宽表格式的 GRR 数据转换为长表格式。

    适用场景:
        数据按 GRR 实验顺序排列，每行是一个测量记录，多列为测量参数。
        例如: 3 操作员 × 10 零件 × 3 次试验 = 90 行，每行包含多个测量参数。

    数据排列顺序 (按行):
        试验1: Op_A×n_parts, Op_B×n_parts, Op_C×n_parts
        试验2: Op_A×n_parts, Op_B×n_parts, Op_C×n_parts
        ...

    参数:
        file_path : str            - 数据文件路径 (.csv / .xlsx / .xls)
        n_operators : int          - 操作员数量 (默认: 3)
        n_parts : int              - 零件数量 (默认: 10)
        operator_names : list, 可选 - 操作员名称列表 (默认: ['Operator_1', 'Operator_2', ...])
        part_names : list, 可选     - 零件名称列表 (默认: ['Part_1', 'Part_2', ...])
        sheet_name : str, 可选      - Excel 工作表名称

    返回:
        tuple - (long_df, numeric_cols)
            long_df      - 长表格式数据，包含 operator, part, parameter, value 列
            numeric_cols - 测量参数列名列表
    """
    # 加载原始数据
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"数据文件不存在: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext in ('.xlsx', '.xls'):
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        raise ValueError(f"不支持的文件格式: {ext}")

    n_rows = len(df)
    n_trials = n_rows // (n_operators * n_parts)

    if n_rows != n_operators * n_parts * n_trials:
        raise ValueError(
            f"数据行数({n_rows})不能被 操作员数({n_operators}) × 零件数({n_parts}) 整除。"
            f"\n请检查 n_operators 和 n_parts 参数是否正确。"
        )

    # 生成操作员和零件名称
    if operator_names is None:
        operator_names = [f'Operator_{i+1}' for i in range(n_operators)]
    if part_names is None:
        part_names = [f'Part_{i+1}' for i in range(n_parts)]

    # 按 GRR 实验顺序分配操作员和零件
    # 顺序: 每个 trial 中, Op_A 测 Part_1~N, Op_B 测 Part_1~N, ...
    op_list = []
    pt_list = []
    for trial in range(n_trials):
        for op_idx in range(n_operators):
            for pt_idx in range(n_parts):
                op_list.append(operator_names[op_idx])
                pt_list.append(part_names[pt_idx])

    # 识别数值测量列 (排除元数据列)
    numeric_cols = []
    for col in df.columns:
        converted = pd.to_numeric(df[col], errors='coerce')
        valid_ratio = converted.notna().mean()
        # 只保留至少 80% 为有效数值的列
        if valid_ratio >= 0.8:
            numeric_cols.append(col)

    if not numeric_cols:
        raise ValueError("数据中没有找到有效的数值测量列")

    # 构建长表格式数据
    records = []
    for idx in range(n_rows):
        for col in numeric_cols:
            val = pd.to_numeric(df.at[idx, col], errors='coerce')
            if pd.notna(val):
                records.append({
                    'operator': op_list[idx],
                    'part': pt_list[idx],
                    'parameter': col,
                    'value': val,
                })

    long_df = pd.DataFrame(records)
    print(f"✅ 宽表→长表转换完成:")
    print(f"   原始数据: {n_rows} 行 × {len(df.columns)} 列")
    print(f"   操作员: {operator_names}")
    print(f"   零件: {part_names}")
    print(f"   试验次数: {n_trials}")
    print(f"   测量参数: {len(numeric_cols)} 个")
    print(f"   长表数据: {len(long_df)} 行")

    return long_df, numeric_cols


# ================================ ANOVA 方差分析法 ================================


def _grr_anova(tidy_df: pd.DataFrame) -> Dict:
    """
    使用 ANOVA (方差分析法) 进行 GRR 分析。

    模型: Y = μ + Operator + Part + Operator×Part + ε
    通过分解方差得到各变异分量。

    返回:
        dict - 包含完整 ANOVA GRR 分析结果
    """
    operators = sorted(tidy_df['operator'].unique())
    parts = sorted(tidy_df['part'].unique())
    n_op = len(operators)
    n_pt = len(parts)

    # 构建数据矩阵: data[operator_idx][part_idx] = [trial_values]
    data = {}
    n_trials_list = []
    for op in operators:
        data[op] = {}
        for pt in parts:
            vals = tidy_df[(tidy_df['operator'] == op) & (tidy_df['part'] == pt)]['value'].values
            data[op][pt] = vals
            n_trials_list.append(len(vals))

    # 检查试验次数一致性
    n_trials = int(np.mean(n_trials_list))
    if len(set(n_trials_list)) > 1:
        # 取最小公共试验次数
        n_trials = min(n_trials_list)
        for op in operators:
            for pt in parts:
                data[op][pt] = data[op][pt][:n_trials]

    N = n_op * n_pt * n_trials  # 总观测数

    # 计算各均值
    grand_mean = tidy_df['value'].mean()
    op_means = {op: tidy_df[tidy_df['operator'] == op]['value'].mean() for op in operators}
    pt_means = {pt: tidy_df[tidy_df['part'] == pt]['value'].mean() for pt in parts}
    cell_means = {}
    for op in operators:
        cell_means[op] = {}
        for pt in parts:
            cell_means[op][pt] = data[op][pt].mean()

    # ---- 平方和分解 (Sum of Squares Decomposition) ----
    # 模型: Y_ijk = μ + α_i(操作员) + β_j(零件) + (αβ)_ij(交互) + ε_ijk
    #
    # SS_Total = Σ(Y_ijk - Ȳ...)²               总变异
    # SS_Operator = n_pt * n * Σ(Ȳ_i. - Ȳ...)²    操作员间变异
    # SS_Part = n_op * n * Σ(Ȳ_.j - Ȳ...)²        零件间变异
    # SS_Cells = n * Σ(Ȳ_ij - Ȳ_i. - Ȳ_.j + Ȳ...)²  单元格变异(含交互+误差)
    # SS_Error = Σ(Y_ijk - Ȳ_ij)²               组内变异(重复性)
    ss_total = ((tidy_df['value'] - grand_mean) ** 2).sum()

    # SS_Operator (行间)
    ss_operator = n_pt * n_trials * sum((op_means[op] - grand_mean) ** 2 for op in operators)

    # SS_Part (列间)
    ss_part = n_op * n_trials * sum((pt_means[pt] - grand_mean) ** 2 for pt in parts)

    # SS_Cells (单元格)
    ss_cells = n_trials * sum(
        (cell_means[op][pt] - op_means[op] - pt_means[pt] + grand_mean) ** 2
        for op in operators for pt in parts
    )

    # SS_Error (组内/重复性)
    ss_error = sum(
        (data[op][pt][t] - cell_means[op][pt]) ** 2
        for op in operators for pt in parts for t in range(n_trials)
    )

    # ---- 自由度 (Degrees of Freedom) ----
    # df_Operator = a - 1
    # df_Part = b - 1
    # df_Interaction = (a-1)(b-1)
    # df_Error = ab(n-1)
    # df_Total = N - 1
    df_operator = n_op - 1
    df_part = n_pt - 1
    df_interaction = (n_op - 1) * (n_pt - 1)
    df_error = n_op * n_pt * (n_trials - 1)
    df_total = N - 1

    # ---- 均方 (Mean Squares) ----
    # MS = SS / df
    # MS_Operator = SS_Operator / df_Operator
    # MS_Part = SS_Part / df_Part
    # MS_Interaction = SS_Interaction / df_Interaction
    # MS_Error = SS_Error / df_Error
    ss_interaction = ss_cells  # 交互作用平方和
    ms_operator = ss_operator / df_operator if df_operator > 0 else 0
    ms_part = ss_part / df_part if df_part > 0 else 0
    ms_interaction = ss_interaction / df_interaction if df_interaction > 0 else 0
    ms_error = ss_error / df_error if df_error > 0 else 0

    # ---- 方差分量估计 (Variance Component Estimation) ----
    # σ²_e = MS_Error                            重复性方差 (EV²)
    # σ²_o = (MS_Operator - MS_Interaction) / (b*n)  再现性方差 (AV²)
    # σ²_p = (MS_Part - MS_Interaction) / (a*n)     零件间方差 (PV²)
    # σ²_op = (MS_Interaction - MS_Error) / n       交互作用方差
    sigma2_e = ms_error  # 重复性 (EV²)
    sigma2_o = (ms_operator - ms_interaction) / (n_pt * n_trials) if n_pt * n_trials > 0 else 0
    sigma2_p = (ms_part - ms_interaction) / (n_op * n_trials) if n_op * n_trials > 0 else 0
    sigma2_op = (ms_interaction - ms_error) / n_trials if n_trials > 0 else 0

    # 确保方差非负
    sigma2_o = max(sigma2_o, 0)
    sigma2_p = max(sigma2_p, 0)
    sigma2_op = max(sigma2_op, 0)

    # ---- 汇总 GRR 结果 ----
    # GRR² = σ²_o + σ²_e  (测量系统变异 = 再现性 + 重复性)
    # PV² = σ²_p          (零件间变异)
    # TV² = GRR² + PV²    (总变异)
    # %GRR = (σ_GRR / σ_TV) × 100%
    # ndc = floor(1.41 × σ_PV / σ_GRR)  可区分类别数
    var_grr = sigma2_o + sigma2_e
    var_pv = sigma2_p
    var_tv = var_grr + var_pv

    std_grr = np.sqrt(var_grr)
    std_pv = np.sqrt(var_pv)
    std_tv = np.sqrt(var_tv)

    pct_grr = (std_grr / std_tv * 100) if std_tv > 0 else 0
    ndc = int(1.41 * (std_pv / std_grr)) if std_grr > 0 else 0

    return {
        'method': 'ANOVA',
        'operators': operators, 'parts': parts,
        'n_op': n_op, 'n_pt': n_pt, 'n_trials': n_trials, 'N': N,
        'grand_mean': grand_mean,
        'op_means': op_means, 'pt_means': pt_means,
        'cell_means': cell_means, 'data': data,
        # ANOVA 表
        'ss_operator': ss_operator, 'df_operator': df_operator, 'ms_operator': ms_operator,
        'ss_part': ss_part, 'df_part': df_part, 'ms_part': ms_part,
        'ss_interaction': ss_cells, 'df_interaction': df_interaction, 'ms_interaction': ms_interaction,
        'ss_error': ss_error, 'df_error': df_error, 'ms_error': ms_error,
        'ss_total': ss_total, 'df_total': df_total,
        # 方差分量
        'sigma2_e': sigma2_e, 'sigma2_o': sigma2_o,
        'sigma2_p': sigma2_p, 'sigma2_op': sigma2_op,
        # GRR 结果
        'EV': np.sqrt(sigma2_e), 'AV': np.sqrt(sigma2_o),
        'var_grr': var_grr, 'var_pv': var_pv, 'var_tv': var_tv,
        'std_grr': std_grr, 'std_pv': std_pv, 'std_tv': std_tv,
        'pct_grr': pct_grr, 'ndc': ndc,
    }


# ================================ AIAG 均值极差法 ================================


def _grr_aiag(tidy_df: pd.DataFrame) -> Dict:
    """
    使用 AIAG 均值极差法 (Average-Range Method) 进行 GRR 分析。

    原理:
        1. 计算每个操作员对每个零件的测量均值和极差
        2. 计算操作员平均极差 R̄ → 用于估计重复性 EV = R̄ × K1
        3. 计算操作员均值极差 X_diff → 用于估计再现性 AV
        4. 计算零件均值极差 Rp → 用于估计零件变异 PV = Rp × K3
        5. 合成 GRR = sqrt(EV² + AV²), TV = sqrt(GRR² + PV²)

    常量说明:
        K1 - 将极差转换为标准差的系数, 取决于试验次数 (2或3)
        K2 - 计算 AV 时的系数, 取决于操作员数量 (2或3)
        K3 - 计算 PV 时的系数, 取决于零件数量 (2~100)

    返回:
        dict - 包含完整 AIAG GRR 分析结果
    """
    operators = sorted(tidy_df['operator'].unique())
    parts = sorted(tidy_df['part'].unique())
    n_op = len(operators)
    n_pt = len(parts)

    # ---- 步骤1: 构建数据矩阵并计算单元格统计量 ----
    # data[op][pt] = 该操作员对该零件的所有测量值
    data = {}
    n_trials_list = []
    for op in operators:
        data[op] = {}
        for pt in parts:
            vals = tidy_df[(tidy_df['operator'] == op) & (tidy_df['part'] == pt)]['value'].values
            data[op][pt] = vals
            n_trials_list.append(len(vals))
    n_trials = min(n_trials_list)  # 取最小公共试验次数

    # ---- 步骤2: 计算每个操作员-零件组合的均值和极差 ----
    # cell_means[op][pt] = 该组合的测量均值
    # cell_ranges[op][pt] = 该组合的测量极差 (max - min)
    cell_means = {}
    cell_ranges = {}
    for op in operators:
        cell_means[op] = {}
        cell_ranges[op] = {}
        for pt in parts:
            v = data[op][pt][:n_trials]
            cell_means[op][pt] = v.mean()
            cell_ranges[op][pt] = v.max() - v.min()

    # ---- 步骤3: 计算操作员级别的汇总统计量 ----
    # op_avg_range[op] = 该操作员对所有零件的平均极差
    # op_mean[op] = 该操作员对所有零件的总均值
    op_avg_range = {}
    op_mean = {}
    for op in operators:
        ranges = [cell_ranges[op][pt] for pt in parts]
        op_avg_range[op] = np.mean(ranges)
        means = [cell_means[op][pt] for pt in parts]
        op_mean[op] = np.mean(means)

    # R̄: 所有操作员平均极差的均值 → 用于计算 EV
    R_bar = np.mean(list(op_avg_range.values()))
    # X_diff: 操作员均值之间的极差 (max - min) → 用于计算 AV
    X_diff = max(op_mean.values()) - min(op_mean.values())

    # ---- 步骤4: 计算零件级别统计量 ----
    pt_means = {}
    for pt in parts:
        vals = [cell_means[op][pt] for op in operators]
        pt_means[pt] = np.mean(vals)
    # Rp: 零件均值之间的极差 → 用于计算 PV
    Rp = max(pt_means.values()) - min(pt_means.values())

    # 总均值
    grand_mean = np.mean(list(op_mean.values()))

    # ---- 步骤5: 查找 AIAG 常量 (K1, K2, K3) ----
    # K1 取决于试验次数, K2 取决于操作员数, K3 取决于零件数
    K1_val = _K1.get(n_trials, 0)
    K2_val = _K2.get(n_op, 0)
    K3_val = _K3.get(n_pt, 0)
    # 对于不在常量表中的零件数，使用线性插值
    if K3_val == 0 and n_pt not in _K3:
        sorted_keys = sorted(_K3.keys())
        for i in range(len(sorted_keys) - 1):
            if sorted_keys[i] < n_pt < sorted_keys[i + 1]:
                ratio = (n_pt - sorted_keys[i]) / (sorted_keys[i + 1] - sorted_keys[i])
                K3_val = _K3[sorted_keys[i]] + ratio * (_K3[sorted_keys[i + 1]] - _K3[sorted_keys[i]])
                break

    # ---- 步骤6: 计算各变异分量 ----
    # EV (Equipment Variation) = R̄ × K1, 设备变异/重复性
    EV = R_bar * K1_val if K1_val > 0 else 0
    # AV (Appraiser Variation) = sqrt((X_diff×K2)² - EV²/(n_pt×n_trials)), 人员变异/再现性
    AV_sq = (X_diff * K2_val) ** 2 - (EV ** 2) / (n_pt * n_trials)
    AV = np.sqrt(max(AV_sq, 0))  # max 确保非负
    # PV (Part Variation) = Rp × K3, 零件间变异
    PV = Rp * K3_val if K3_val > 0 else 0

    # ---- 步骤7: 合成总变异 ----
    # GRR = sqrt(EV² + AV²)  测量系统变异
    GRR = np.sqrt(EV ** 2 + AV ** 2)
    # TV = sqrt(GRR² + PV²)  总变异
    TV = np.sqrt(GRR ** 2 + PV ** 2)

    # %GRR: 测量系统占总变异的百分比
    pct_grr = (GRR / TV * 100) if TV > 0 else 0
    # ndc: 可区分类别数 (number of distinct categories)
    ndc = int(1.41 * (PV / GRR)) if GRR > 0 else 0

    return {
        'method': 'AIAG',
        'operators': operators, 'parts': parts,
        'n_op': n_op, 'n_pt': n_pt, 'n_trials': n_trials,
        'N': n_op * n_pt * n_trials,
        'grand_mean': grand_mean,
        'op_means': op_mean, 'pt_means': pt_means,
        'cell_means': cell_means, 'data': data,
        'R_bar': R_bar, 'X_diff': X_diff, 'Rp': Rp,
        'EV': EV, 'AV': AV, 'PV': PV,
        'GRR': GRR, 'TV': TV,
        'var_grr': GRR ** 2, 'var_pv': PV ** 2, 'var_tv': TV ** 2,
        'std_grr': GRR, 'std_pv': PV, 'std_tv': TV,
        'pct_grr': pct_grr, 'ndc': ndc,
        # 兼容 HTML/PDF 报告中引用的方差分量字段
        'sigma2_e': EV ** 2,
        'sigma2_o': AV ** 2,
        'sigma2_p': PV ** 2,
        'sigma2_op': 0.0,
    }


# ================================ 图表绘制 ================================


def _fig_to_base64(fig: plt.Figure) -> str:
    """
    将 matplotlib Figure 转换为 Base64 编码的 PNG 字符串。

    用于将图表内嵌到 HTML 报告中，无需外部图片文件。
    转换后自动关闭 Figure 释放内存。
    """
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_b64


def _plot_variance_components(result: Dict) -> plt.Figure:
    """
    绘制方差分量柱状图。

    展示 EV(重复性)、AV(再现性)、GRR(合计)、PV(零件)、TV(总变异)
    五个分量的标准差值，用于直观比较各变异分量的大小。
    """
    _configure_chinese_font()
    fig, ax = plt.subplots(figsize=(8, 5))

    labels = ['EV\n(重复性)', 'AV\n(再现性)', 'GRR\n(合计)', 'PV\n(零件)', 'TV\n(总变异)']
    if result['method'] == 'ANOVA':
        values = [result['EV'], np.sqrt(result['sigma2_o']),
                  result['std_grr'], result['std_pv'], result['std_tv']]
    else:
        values = [result['EV'], result['AV'], result['GRR'], result['PV'], result['TV']]

    colors = ['#4C72B0', '#DD8452', '#C44E52', '#55A868', '#8172B2']
    bars = ax.bar(labels, values, color=colors, edgecolor='white', width=0.6)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.02,
                f'{val:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylabel('标准差 (σ)', fontsize=11)
    ax.set_title('方差分量图', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(values) * 1.15)
    plt.tight_layout()
    return fig


def _plot_interaction(result: Dict) -> plt.Figure:
    """
    绘制操作员×零件交互作用图。

    每条线代表一个操作员，X轴为零件，Y轴为测量均值。
    如果各线基本平行 → 交互作用小；如果交叉 → 交互作用大。
    理想的 GRR 研究中，各线应近似平行且间距小。
    """
    _configure_chinese_font()
    fig, ax = plt.subplots(figsize=(10, 5))

    operators = result['operators']
    parts = result['parts']
    cell_means = result['cell_means']

    colors = plt.cm.Set2(np.linspace(0, 1, len(operators)))
    for i, op in enumerate(operators):
        means = [cell_means[op][pt] for pt in parts]
        ax.plot(range(len(parts)), means, 'o-', color=colors[i],
                label=op, linewidth=2, markersize=6)

    ax.set_xticks(range(len(parts)))
    ax.set_xticklabels(parts, rotation=45, ha='right')
    ax.set_xlabel('零件', fontsize=11)
    ax.set_ylabel('测量均值', fontsize=11)
    ax.set_title('操作员 × 零件 交互作用图', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def _plot_boxplot(tidy_df: pd.DataFrame) -> plt.Figure:
    """
    绘制按操作员分组的箱线图。

    用于观察各操作员测量值的分布情况（中位数、离散度、异常值）。
    理想情况下各操作员的箱体应高度一致。
    """
    _configure_chinese_font()
    fig, ax = plt.subplots(figsize=(10, 5))

    operators = sorted(tidy_df['operator'].unique())
    data_by_op = [tidy_df[tidy_df['operator'] == op]['value'].values for op in operators]

    bp = ax.boxplot(data_by_op, labels=operators, patch_artist=True, widths=0.5)
    colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52']
    for patch, color in zip(bp['boxes'], colors[:len(operators)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_xlabel('操作员', fontsize=11)
    ax.set_ylabel('测量值', fontsize=11)
    ax.set_title('各操作员测量值分布', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    return fig


def _plot_part_boxplot(tidy_df: pd.DataFrame) -> plt.Figure:
    """
    绘制按零件分组的箱线图。

    用于观察各零件测量值的分布情况。
    零件间应有明显差异（否则 ndc 会很低），说明测量系统能区分不同零件。
    """
    _configure_chinese_font()
    fig, ax = plt.subplots(figsize=(10, 5))

    parts = sorted(tidy_df['part'].unique())
    data_by_pt = [tidy_df[tidy_df['part'] == pt]['value'].values for pt in parts]

    bp = ax.boxplot(data_by_pt, labels=parts, patch_artist=True, widths=0.6)
    cmap = plt.cm.Set3(np.linspace(0, 1, len(parts)))
    for patch, color in zip(bp['boxes'], cmap):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_xticklabels(parts, rotation=45, ha='right')
    ax.set_xlabel('零件', fontsize=11)
    ax.set_ylabel('测量值', fontsize=11)
    ax.set_title('各零件测量值分布', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    return fig


def _plot_grr_gauge(result: Dict) -> plt.Figure:
    """
    绘制 %GRR 仪表盘图（环形图）。

    中心显示 %GRR 值和 ndc 值，颜色表示判定结果:
        绿色: %GRR < 10%  → 合格
        橙色: 10% ≤ %GRR < 30% → 有条件接受
        红色: %GRR ≥ 30% → 不合格
    """
    _configure_chinese_font()
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))

    pct = result['pct_grr']
    ndc = result['ndc']

    # 判定等级
    if pct < 10:
        status, color = '合格 (< 10%)', '#4CAF50'
    elif pct < 30:
        status, color = '有条件接受 (10%-30%)', '#FF9800'
    else:
        status, color = '不合格 (> 30%)', '#f44336'

    # 绘制环形图
    sizes = [pct, 100 - pct]
    wedges, texts = ax.pie(sizes, colors=[color, '#e0e0e0'],
                           startangle=90, wedgeprops=dict(width=0.4))

    # 中心文字
    ax.text(0, 0.1, f'%GRR', ha='center', va='center', fontsize=14, color='#666')
    ax.text(0, -0.1, f'{pct:.2f}%', ha='center', va='center',
            fontsize=28, fontweight='bold', color=color)
    ax.text(0, -0.35, f'ndc = {ndc}', ha='center', va='center',
            fontsize=16, color='#444')
    ax.set_title(f'测量系统分析判定: {status}', fontsize=13, fontweight='bold',
                 pad=20, color=color)
    plt.tight_layout()
    return fig


# ================================ Markdown 报告 ================================


def generate_markdown_report(result: Dict, tidy_df: pd.DataFrame,
                             file_path: str, output_path: str) -> str:
    """
    生成 Markdown 格式的 GRR 分析报告。

    报告内容包括:
        1. 研究概要（操作员数、零件数、试验次数等）
        2. GRR 结果汇总（EV/AV/GRR/PV/TV/%GRR/ndc + 判定）
        3. ANOVA 方差分析表 或 AIAG 参数表
        4. %GRR 判定标准参考表

    参数:
        result      - GRR 分析结果字典
        tidy_df     - 整理后的数据 DataFrame
        file_path   - 原始数据文件路径（用于报告标题）
        output_path - Markdown 文件输出路径

    返回:
        str - 生成的 Markdown 文件路径
    """
    r = result
    lines = []

    lines.append(f"# GRR 测量系统分析报告\n")
    lines.append(f"**数据文件**: {os.path.basename(file_path)}  ")
    lines.append(f"**分析方法**: {r['method']}  ")
    lines.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")

    lines.append(f"---\n")
    lines.append(f"## 1. 研究概要\n")
    lines.append(f"| 项目 | 值 |")
    lines.append(f"|------|-----|")
    lines.append(f"| 操作员数量 | {r['n_op']} |")
    lines.append(f"| 零件数量 | {r['n_pt']} |")
    lines.append(f"| 试验次数 | {r['n_trials']} |")
    lines.append(f"| 总观测数 | {r['N']} |")
    lines.append(f"| 总均值 | {r['grand_mean']:.6f} |\n")

    lines.append(f"---\n")
    lines.append(f"## 2. GRR 结果汇总\n")

    # 判定
    pct = r['pct_grr']
    ndc = r['ndc']
    if pct < 10:
        verdict = '✅ 合格 (%GRR < 10%)'
    elif pct < 30:
        verdict = '⚠️ 有条件接受 (10% ≤ %GRR < 30%)'
    else:
        verdict = '❌ 不合格 (%GRR ≥ 30%)'

    lines.append(f"| 指标 | 值 | 说明 |")
    lines.append(f"|------|-----|------|")
    lines.append(f"| EV (重复性) | {r['EV']:.6f} | 设备变异 |")
    if r['method'] == 'ANOVA':
        lines.append(f"| AV (再现性) | {np.sqrt(r['sigma2_o']):.6f} | 操作员变异 |")
    else:
        lines.append(f"| AV (再现性) | {r['AV']:.6f} | 操作员变异 |")
    lines.append(f"| GRR (合计) | {r['std_grr']:.6f} | 测量系统变异 |")
    lines.append(f"| PV (零件) | {r['std_pv']:.6f} | 零件间变异 |")
    lines.append(f"| TV (总变异) | {r['std_tv']:.6f} | 总变异 |")
    lines.append(f"| **%GRR** | **{pct:.2f}%** | **测量系统占比** |")
    lines.append(f"| **ndc** | **{ndc}** | **可区分类别数** |")
    lines.append(f"| **判定** | **{verdict}** | |")
    lines.append("")

    # ANOVA 表
    if r['method'] == 'ANOVA':
        lines.append(f"---\n")
        lines.append(f"## 3. ANOVA 方差分析表\n")
        lines.append(f"| 来源 | 平方和(SS) | 自由度(df) | 均方(MS) |")
        lines.append(f"|------|-----------|-----------|---------|")
        lines.append(f"| 操作员 | {r['ss_operator']:.6f} | {r['df_operator']} | {r['ms_operator']:.6f} |")
        lines.append(f"| 零件 | {r['ss_part']:.6f} | {r['df_part']} | {r['ms_part']:.6f} |")
        lines.append(f"| 交互作用 | {r['ss_interaction']:.6f} | {r['df_interaction']} | {r['ms_interaction']:.6f} |")
        lines.append(f"| 误差 | {r['ss_error']:.6f} | {r['df_error']} | {r['ms_error']:.6f} |")
        lines.append(f"| **总计** | **{r['ss_total']:.6f}** | **{r['df_total']}** | |\n")

        lines.append(f"## 4. 方差分量估计\n")
        lines.append(f"| 分量 | 方差 | 占比 |")
        lines.append(f"|------|------|------|")
        total_var = r['var_tv'] if r['var_tv'] > 0 else 1
        lines.append(f"| 重复性 (EV²) | {r['sigma2_e']:.6f} | {r['sigma2_e']/total_var*100:.1f}% |")
        lines.append(f"| 再现性 (AV²) | {r['sigma2_o']:.6f} | {r['sigma2_o']/total_var*100:.1f}% |")
        lines.append(f"| 交互作用 | {r['sigma2_op']:.6f} | {r['sigma2_op']/total_var*100:.1f}% |")
        lines.append(f"| 零件变异 (PV²) | {r['sigma2_p']:.6f} | {r['sigma2_p']/total_var*100:.1f}% |")
        lines.append(f"| **总变异** | **{total_var:.6f}** | **100%** |\n")
    else:
        lines.append(f"---\n")
        lines.append(f"## 3. AIAG 均值极差法参数\n")
        lines.append(f"| 参数 | 值 |")
        lines.append(f"|------|-----|")
        lines.append(f"| 平均极差 R̄ | {r.get('R_bar', 0):.6f} |")
        lines.append(f"| 操作员均值极差 X_diff | {r.get('X_diff', 0):.6f} |")
        lines.append(f"| 零件极差 Rp | {r.get('Rp', 0):.6f} |\n")

    lines.append(f"---\n")
    lines.append(f"## {'4' if r['method'] == 'ANOVA' else '4'}. %GRR 判定标准\n")
    lines.append(f"| %GRR 范围 | 判定 | 说明 |")
    lines.append(f"|-----------|------|------|")
    lines.append(f"| < 10% | ✅ 合格 | 测量系统可接受 |")
    lines.append(f"| 10% ~ 30% | ⚠️ 有条件接受 | 根据应用场景决定 |")
    lines.append(f"| ≥ 30% | ❌ 不合格 | 测量系统需改进 |")
    lines.append(f"| ndc ≥ 5 | ✅ | 足够的分辨力 |")
    lines.append(f"| ndc < 5 | ❌ | 分辨力不足 |\n")

    lines.append(f"---\n")
    lines.append(f"*报告由 SPC统计分析工具 自动生成 — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path


# ================================ HTML 报告 ================================


def generate_html_report(result: Dict, tidy_df: pd.DataFrame,
                         file_path: str, output_path: str) -> str:
    """
    生成 HTML 格式的 GRR 分析报告（含内嵌图表）。

    报告采用现代化渐变背景 + 卡片布局设计，包含:
        1. 头部信息卡片（文件名、方法、时间）
        2. 研究概要卡片（操作员/零件/试验次数/总观测数）
        3. GRR 结果卡片（%GRR 仪表盘 + 各分量数值）
        4. 方差分量图、%GRR 仪表盘图
        5. 交互作用图、操作员箱线图、零件箱线图
        6. 详细数据表（标准差、方差、占比）

    所有图表以 Base64 编码内嵌，无需外部图片文件。

    参数:
        result      - GRR 分析结果字典
        tidy_df     - 整理后的数据 DataFrame
        file_path   - 原始数据文件路径
        output_path - HTML 文件输出路径

    返回:
        str - 生成的 HTML 文件路径
    """
    _configure_chinese_font()

    # 生成图表
    fig_components = _plot_variance_components(result)
    fig_interaction = _plot_interaction(result)
    fig_boxplot_op = _plot_boxplot(tidy_df)
    fig_boxplot_pt = _plot_part_boxplot(tidy_df)
    fig_gauge = _plot_grr_gauge(result)

    img_components = _fig_to_base64(fig_components)
    img_interaction = _fig_to_base64(fig_interaction)
    img_boxplot_op = _fig_to_base64(fig_boxplot_op)
    img_boxplot_pt = _fig_to_base64(fig_boxplot_pt)
    img_gauge = _fig_to_base64(fig_gauge)

    r = result
    pct = r['pct_grr']
    ndc = r['ndc']
    if pct < 10:
        verdict, vcolor = '✅ 合格', '#4CAF50'
    elif pct < 30:
        verdict, vcolor = '⚠️ 有条件接受', '#FF9800'
    else:
        verdict, vcolor = '❌ 不合格', '#f44336'

    av_val = np.sqrt(r['sigma2_o']) if r['method'] == 'ANOVA' else r['AV']

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GRR 测量系统分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
            min-height: 100vh; padding: 30px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .card {{
            background: white; border-radius: 16px; padding: 28px;
            margin-bottom: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }}
        .header h1 {{ font-size: 28px; color: #333; margin-bottom: 12px; }}
        .header-info {{ display: flex; flex-wrap: wrap; gap: 16px; font-size: 14px; color: #666; }}
        .header-info span {{ background: #f0f2f5; padding: 6px 16px; border-radius: 8px; }}
        .card h2 {{ font-size: 20px; color: #333; margin-bottom: 16px; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px; }}
        .result-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; }}
        .result-item {{ padding: 16px; border-radius: 12px; text-align: center; background: #f8f9fa; }}
        .result-item .number {{ font-size: 28px; font-weight: bold; }}
        .result-item .label {{ font-size: 13px; color: #888; margin-top: 4px; }}
        .verdict {{ font-size: 24px; font-weight: bold; color: {vcolor}; text-align: center; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th {{ background: #f8f9fa; padding: 10px 8px; text-align: center; font-weight: 600; color: #555; border-bottom: 2px solid #e0e0e0; }}
        td {{ padding: 8px; text-align: center; border-bottom: 1px solid #eee; color: #333; }}
        tr:hover {{ background: #f5f5f5; }}
        .chart-img {{ width: 100%; border-radius: 8px; margin-top: 12px; }}
        .charts-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
        .footer {{ text-align: center; color: rgba(255,255,255,0.7); font-size: 12px; padding: 20px; }}
        @media (max-width: 768px) {{ .charts-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
<div class="container">
    <div class="card header">
        <h1>📊 GRR 测量系统分析报告</h1>
        <div class="header-info">
            <span>📁 数据文件: {os.path.basename(file_path)}</span>
            <span>📐 分析方法: {r['method']}</span>
            <span>📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
        </div>
    </div>

    <div class="card">
        <h2>📋 研究概要</h2>
        <div class="result-grid">
            <div class="result-item"><div class="number">{r['n_op']}</div><div class="label">操作员</div></div>
            <div class="result-item"><div class="number">{r['n_pt']}</div><div class="label">零件</div></div>
            <div class="result-item"><div class="number">{r['n_trials']}</div><div class="label">试验次数</div></div>
            <div class="result-item"><div class="number">{r['N']}</div><div class="label">总观测数</div></div>
        </div>
    </div>

    <div class="card">
        <h2>🎯 GRR 结果</h2>
        <div class="verdict">{verdict}</div>
        <div class="result-grid">
            <div class="result-item"><div class="number">{r['EV']:.4f}</div><div class="label">EV (重复性)</div></div>
            <div class="result-item"><div class="number">{av_val:.4f}</div><div class="label">AV (再现性)</div></div>
            <div class="result-item"><div class="number">{r['std_grr']:.4f}</div><div class="label">GRR (合计)</div></div>
            <div class="result-item"><div class="number">{r['std_pv']:.4f}</div><div class="label">PV (零件)</div></div>
            <div class="result-item"><div class="number" style="color:{vcolor}">{pct:.2f}%</div><div class="label">%GRR</div></div>
            <div class="result-item"><div class="number">{ndc}</div><div class="label">ndc</div></div>
        </div>
    </div>

    <div class="card">
        <h2>📊 方差分量图</h2>
        <img class="chart-img" src="data:image/png;base64,{img_components}" alt="方差分量图">
    </div>

    <div class="card">
        <h2>🎯 %GRR 仪表盘</h2>
        <img class="chart-img" src="data:image/png;base64,{img_gauge}" alt="%GRR 仪表盘">
    </div>

    <div class="card">
        <h2>📈 分析图表</h2>
        <div class="charts-grid">
            <div>
                <h3 style="text-align:center; margin-bottom:8px;">操作员×零件交互作用图</h3>
                <img class="chart-img" src="data:image/png;base64,{img_interaction}" alt="交互作用图">
            </div>
            <div>
                <h3 style="text-align:center; margin-bottom:8px;">各操作员测量值分布</h3>
                <img class="chart-img" src="data:image/png;base64,{img_boxplot_op}" alt="操作员箱线图">
            </div>
        </div>
        <div style="margin-top: 24px;">
            <h3 style="text-align:center; margin-bottom:8px;">各零件测量值分布</h3>
            <img class="chart-img" src="data:image/png;base64,{img_boxplot_pt}" alt="零件箱线图">
        </div>
    </div>

    <div class="card">
        <h2>📋 详细数据表</h2>
        <table>
            <thead><tr><th>来源</th><th>标准差(σ)</th><th>方差(σ²)</th><th>占总变异%</th></tr></thead>
            <tbody>
                <tr><td>EV (重复性)</td><td>{r['EV']:.6f}</td><td>{r['sigma2_e']:.6f}</td><td>{r['sigma2_e']/max(r['var_tv'],1e-10)*100:.1f}%</td></tr>
                <tr><td>AV (再现性)</td><td>{av_val:.6f}</td><td>{r['sigma2_o']:.6f}</td><td>{r['sigma2_o']/max(r['var_tv'],1e-10)*100:.1f}%</td></tr>
                <tr><td>GRR (合计)</td><td>{r['std_grr']:.6f}</td><td>{r['var_grr']:.6f}</td><td>{r['var_grr']/max(r['var_tv'],1e-10)*100:.1f}%</td></tr>
                <tr><td>PV (零件)</td><td>{r['std_pv']:.6f}</td><td>{r['var_pv']:.6f}</td><td>{r['var_pv']/max(r['var_tv'],1e-10)*100:.1f}%</td></tr>
                <tr style="font-weight:bold"><td>TV (总变异)</td><td>{r['std_tv']:.6f}</td><td>{r['var_tv']:.6f}</td><td>100.0%</td></tr>
            </tbody>
        </table>
    </div>

    <div class="footer">
        GRR 测量系统分析报告 — SPC统计分析工具 自动生成 — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</div>
</body>
</html>"""

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path


# ================================ PDF 报告 ================================


def generate_pdf_report(result: Dict, tidy_df: pd.DataFrame,
                        file_path: str, output_path: str) -> str:
    """
    生成 PDF 格式的 GRR 分析报告（A4尺寸，300 DPI）。

    报告分页结构:
        第1页: 封面 + 结果汇总表 + ANOVA表(或AIAG参数)
        第2页: 详细图表（方差分量图、%GRR仪表盘、交互作用图、箱线图）

    使用 matplotlib.backends.backend_pdf.PdfPages 生成，
    表格采用交替行背景色，图表以子图方式排列。

    参数:
        result      - GRR 分析结果字典
        tidy_df     - 整理后的数据 DataFrame
        file_path   - 原始数据文件路径
        output_path - PDF 文件输出路径

    返回:
        str - 生成的 PDF 文件路径
    """
    _configure_chinese_font()
    A4_W, A4_H = 8.27, 11.69
    r = result
    pct = r['pct_grr']
    ndc = r['ndc']
    av_val = np.sqrt(r['sigma2_o']) if r['method'] == 'ANOVA' else r['AV']

    if pct < 10:
        verdict, vcolor = '合格 (%GRR < 10%)', '#4CAF50'
    elif pct < 30:
        verdict, vcolor = '有条件接受 (10%-30%)', '#FF9800'
    else:
        verdict, vcolor = '不合格 (%GRR ≥ 30%)', '#f44336'

    with pdf_backend.PdfPages(output_path) as pdf_out:

        # ---- 第1页: 封面 + 结果汇总表 ----
        fig = plt.figure(figsize=(A4_W, A4_H))

        # 标题
        fig.text(0.5, 0.95, 'GRR 测量系统分析报告', ha='center', va='top',
                 fontsize=24, fontweight='bold', color='#1a237e')
        fig.text(0.5, 0.91,
                 f'数据文件: {os.path.basename(file_path)}  |  '
                 f'方法: {r["method"]}  |  '
                 f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                 ha='center', va='top', fontsize=10, color='#666')

        # 概要信息
        fig.text(0.5, 0.86,
                 f'操作员: {r["n_op"]}  |  零件: {r["n_pt"]}  |  '
                 f'试验次数: {r["n_trials"]}  |  总观测数: {r["N"]}',
                 ha='center', va='top', fontsize=12, color='#444')

        # 判定结果
        fig.text(0.5, 0.80, f'判定: {verdict}', ha='center', va='top',
                 fontsize=18, fontweight='bold', color=vcolor)

        # 结果汇总表
        col_labels = ['指标', '标准差(σ)', '方差(σ²)', '占总变异%']
        table_data = [
            ['EV (重复性)', f"{r['EV']:.6f}", f"{r['sigma2_e']:.6f}",
             f"{r['sigma2_e']/max(r['var_tv'],1e-10)*100:.1f}%"],
            ['AV (再现性)', f"{av_val:.6f}", f"{r['sigma2_o']:.6f}",
             f"{r['sigma2_o']/max(r['var_tv'],1e-10)*100:.1f}%"],
            ['GRR (合计)', f"{r['std_grr']:.6f}", f"{r['var_grr']:.6f}",
             f"{r['var_grr']/max(r['var_tv'],1e-10)*100:.1f}%"],
            ['PV (零件)', f"{r['std_pv']:.6f}", f"{r['var_pv']:.6f}",
             f"{r['var_pv']/max(r['var_tv'],1e-10)*100:.1f}%"],
            ['TV (总变异)', f"{r['std_tv']:.6f}", f"{r['var_tv']:.6f}", "100.0%"],
            ['%GRR', f"{pct:.2f}%", '', ''],
            ['ndc', f"{ndc}", '', ''],
        ]

        ax_table = fig.add_axes([0.1, 0.45, 0.8, 0.30])
        ax_table.axis('off')
        table = ax_table.table(cellText=table_data, colLabels=col_labels,
                               loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.6)

        for j in range(len(col_labels)):
            cell = table[0, j]
            cell.set_facecolor('#1a237e')
            cell.set_text_props(color='white', fontweight='bold')
            cell.set_edgecolor('white')
        for i in range(1, len(table_data) + 1):
            bg = '#f0f4f8' if i % 2 == 0 else 'white'
            for j in range(len(col_labels)):
                table[i, j].set_facecolor(bg)
                table[i, j].set_edgecolor('#ddd')

        # ANOVA 表
        if r['method'] == 'ANOVA':
            fig.text(0.5, 0.40, 'ANOVA 方差分析表', ha='center', va='top',
                     fontsize=14, fontweight='bold', color='#333')
            anova_labels = ['来源', '平方和(SS)', '自由度(df)', '均方(MS)']
            anova_data = [
                ['操作员', f"{r['ss_operator']:.6f}", str(r['df_operator']), f"{r['ms_operator']:.6f}"],
                ['零件', f"{r['ss_part']:.6f}", str(r['df_part']), f"{r['ms_part']:.6f}"],
                ['交互作用', f"{r['ss_interaction']:.6f}", str(r['df_interaction']), f"{r['ms_interaction']:.6f}"],
                ['误差', f"{r['ss_error']:.6f}", str(r['df_error']), f"{r['ms_error']:.6f}"],
                ['总计', f"{r['ss_total']:.6f}", str(r['df_total']), ''],
            ]
            ax_anova = fig.add_axes([0.1, 0.08, 0.8, 0.28])
            ax_anova.axis('off')
            t2 = ax_anova.table(cellText=anova_data, colLabels=anova_labels,
                                loc='center', cellLoc='center')
            t2.auto_set_font_size(False)
            t2.set_fontsize(9)
            t2.scale(1, 1.5)
            for j in range(len(anova_labels)):
                t2[0, j].set_facecolor('#0d47a1')
                t2[0, j].set_text_props(color='white', fontweight='bold')
                t2[0, j].set_edgecolor('white')
            for i in range(1, len(anova_data) + 1):
                bg = '#f0f4f8' if i % 2 == 0 else 'white'
                for j in range(len(anova_labels)):
                    t2[i, j].set_facecolor(bg)
                    t2[i, j].set_edgecolor('#ddd')
        else:
            fig.text(0.5, 0.35,
                     f'AIAG 参数: R̄ = {r.get("R_bar",0):.6f}  |  '
                     f'X_diff = {r.get("X_diff",0):.6f}  |  Rp = {r.get("Rp",0):.6f}',
                     ha='center', va='top', fontsize=11, color='#444')

        pdf_out.savefig(fig, dpi=300)
        plt.close(fig)

        # ---- 第2页: 图表 ----
        fig = plt.figure(figsize=(A4_W, A4_H))
        fig.text(0.5, 0.97, 'GRR 分析报告 — 详细图表', ha='center', va='top',
                 fontsize=14, fontweight='bold', color='#333')

        # 2x2 图表布局
        fig_components = _plot_variance_components(result)
        fig_gauge = _plot_grr_gauge(result)
        fig_interaction = _plot_interaction(result)
        fig_boxplot_op = _plot_boxplot(tidy_df)

        # 将各图表绘制到子图中
        ax1 = fig.add_axes([0.05, 0.52, 0.45, 0.40])
        ax2 = fig.add_axes([0.55, 0.52, 0.40, 0.40])
        ax3 = fig.add_axes([0.05, 0.05, 0.45, 0.40])
        ax4 = fig.add_axes([0.55, 0.05, 0.45, 0.40])

        # 复制各图表的内容到新子图
        for src_ax, dst_ax in [(fig_components.axes[0], ax1),
                               (fig_gauge.axes[0], ax2),
                               (fig_interaction.axes[0], ax3),
                               (fig_boxplot_op.axes[0], ax4)]:
            # 简单方式：直接截图拼接
            pass

        # 简化：直接保存为图片再嵌入
        for src_fig, dst_ax, title in [
            (fig_components, ax1, ''),
            (fig_gauge, ax2, ''),
            (fig_interaction, ax3, ''),
            (fig_boxplot_op, ax4, ''),
        ]:
            buf = BytesIO()
            src_fig.savefig(buf, format='png', dpi=100, bbox_inches='tight',
                            facecolor='white', edgecolor='none')
            buf.seek(0)
            img = plt.imread(buf)
            dst_ax.imshow(img)
            dst_ax.axis('off')
            plt.close(src_fig)

        pdf_out.savefig(fig, dpi=300)
        plt.close(fig)

    return output_path


# ================================ 主函数 ================================


def analyze_grr(
    file_path: str,
    operator_col: str = 'operator',
    part_col: str = 'part',
    value_col: str = 'value',
    output_dir: Optional[str] = None,
    method: str = 'ANOVA',
    sheet_name: Optional[str] = None
) -> Dict:
    """
    GRR 分析主函数（推荐第三方集成使用）。

    完整流程:
        1. 加载数据文件
        2. 执行 GRR 分析 (ANOVA 或 AIAG 方法)
        3. 生成 Markdown / HTML / PDF 三种格式报告

    参数:
        file_path : str          - 数据文件路径 (.csv / .xlsx / .xls)
        operator_col : str       - 操作员列名 (默认: 'operator')
        part_col : str           - 零件列名 (默认: 'part')
        value_col : str          - 测量值列名 (默认: 'value')
        output_dir : str, 可选   - 报告输出目录
        method : str             - 分析方法: 'ANOVA' 或 'AIAG' (默认: 'ANOVA')
        sheet_name : str, 可选   - Excel 工作表名称

    返回:
        dict - {
            'result': dict,        # GRR 分析结果
            'markdown_path': str,  # Markdown 报告路径
            'html_path': str,      # HTML 报告路径
            'pdf_path': str,       # PDF 报告路径
        }
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(file_path)), 'grr_reports')
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    md_path = os.path.join(output_dir, f"{base_name}_grr_{timestamp}.md")
    html_path = os.path.join(output_dir, f"{base_name}_grr_{timestamp}.html")
    pdf_path = os.path.join(output_dir, f"{base_name}_grr_{timestamp}.pdf")

    # 步骤1: 加载数据
    print(f"📂 加载数据文件: {file_path}")
    tidy_df = load_grr_data(file_path, operator_col, part_col, value_col, sheet_name)
    operators = sorted(tidy_df['operator'].unique())
    parts = sorted(tidy_df['part'].unique())
    print(f"   操作员: {operators}")
    print(f"   零件: {parts}")
    print(f"   总观测数: {len(tidy_df)}")

    # 步骤2: 执行 GRR 分析
    print(f"📐 分析方法: {method}")
    if method.upper() == 'ANOVA':
        result = _grr_anova(tidy_df)
    else:
        result = _grr_aiag(tidy_df)

    # 打印结果
    pct = result['pct_grr']
    ndc = result['ndc']
    if pct < 10:
        verdict = '✅ 合格'
    elif pct < 30:
        verdict = '⚠️ 有条件接受'
    else:
        verdict = '❌ 不合格'

    print(f"\n{'='*50}")
    print(f"📊 GRR 分析结果:")
    print(f"   EV (重复性):   {result['EV']:.6f}")
    av_val = np.sqrt(result['sigma2_o']) if method == 'ANOVA' else result['AV']
    print(f"   AV (再现性):   {av_val:.6f}")
    print(f"   GRR (合计):    {result['std_grr']:.6f}")
    print(f"   PV (零件):     {result['std_pv']:.6f}")
    print(f"   TV (总变异):   {result['std_tv']:.6f}")
    print(f"   %GRR:          {pct:.2f}%")
    print(f"   ndc:           {ndc}")
    print(f"   判定:          {verdict}")
    print(f"{'='*50}")

    # 步骤3: 生成报告
    print(f"📄 生成 Markdown 报告: {md_path}")
    generate_markdown_report(result, tidy_df, file_path, md_path)

    print(f"📄 生成 HTML 报告: {html_path}")
    generate_html_report(result, tidy_df, file_path, html_path)

    print(f"📄 生成 PDF 报告: {pdf_path}")
    generate_pdf_report(result, tidy_df, file_path, pdf_path)

    print(f"\n🎉 所有报告生成完成！")

    return {
        'result': result,
        'markdown_path': md_path,
        'html_path': html_path,
        'pdf_path': pdf_path,
    }


# ================================ 宽表汇总报告 ================================


def _generate_wide_summary_html(
    summary_list: List[Dict], file_path: str, output_path: str,
    n_op: int, n_pt: int, n_trials: int, method: str,
    spec_limits: Optional[Dict] = None
) -> str:
    """
    生成宽表 GRR 分析的汇总 HTML 报告。

    报告包含:
        1. 研究概要 (操作员/零件/试验次数/参数数量)
        2. 汇总统计表 (所有参数的 %SV, %TOL, ndc, 判定)
        3. 颜色编码: 绿色=合格, 橙色=有条件接受, 红色=不合格
    """
    _configure_chinese_font()

    # 统计各等级数量
    n_pass = sum(1 for s in summary_list if s['pct_grr'] < 10)
    n_cond = sum(1 for s in summary_list if 10 <= s['pct_grr'] < 30)
    n_fail = sum(1 for s in summary_list if s['pct_grr'] >= 30)

    # 按 %GRR 降序排序 (最差的在前面)
    sorted_list = sorted(summary_list, key=lambda x: x['pct_grr'], reverse=True)

    has_tol = spec_limits is not None

    rows_html = ''
    for s in sorted_list:
        pct = s['pct_grr']
        if pct < 10:
            badge_color, badge_text = '#4CAF50', '✅ 合格'
            row_bg = ''
        elif pct < 30:
            badge_color, badge_text = '#FF9800', '⚠️ 条件接受'
            row_bg = 'background:#fff8e1;'
        else:
            badge_color, badge_text = '#f44336', '❌ 不合格'
            row_bg = 'background:#ffebee;'

        # %Tolerance 列
        pct_tol = s.get('pct_tol')
        tol_cell = ''
        if has_tol:
            if pct_tol is not None:
                if pct_tol < 10:
                    tc = '#4CAF50'
                elif pct_tol < 30:
                    tc = '#FF9800'
                else:
                    tc = '#f44336'
                tol_cell = f'<td style="font-weight:bold;color:{tc}">{pct_tol:.2f}%</td>'
            else:
                tol_cell = '<td style="color:#999">-</td>'

        rows_html += f"""<tr style="{row_bg}">
            <td style="text-align:left;font-weight:500">{s['parameter']}</td>
            <td>{s['EV']:.6f}</td>
            <td>{s['AV']:.6f}</td>
            <td>{s['GRR']:.6f}</td>
            <td>{s['PV']:.6f}</td>
            <td>{s.get('pct_ev', 0):.2f}%</td>
            <td>{s.get('pct_av', 0):.2f}%</td>
            <td style="font-weight:bold">{pct:.2f}%</td>
            {tol_cell}
            <td>{s['ndc']}</td>
            <td style="color:{badge_color};font-weight:bold">{badge_text}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GRR 宽表分析汇总报告</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Microsoft YaHei','Segoe UI',Arial,sans-serif;
               background:linear-gradient(135deg,#1a237e 0%,#0d47a1 100%);
               min-height:100vh; padding:30px; }}
        .container {{ max-width:1400px; margin:0 auto; }}
        .card {{ background:white; border-radius:16px; padding:28px;
                 margin-bottom:24px; box-shadow:0 10px 40px rgba(0,0,0,0.15); }}
        .header h1 {{ font-size:26px; color:#333; margin-bottom:12px; }}
        .header-info {{ display:flex; flex-wrap:wrap; gap:12px; font-size:13px; color:#666; }}
        .header-info span {{ background:#f0f2f5; padding:6px 14px; border-radius:8px; }}
        .card h2 {{ font-size:18px; color:#333; margin-bottom:16px;
                     border-bottom:2px solid #e0e0e0; padding-bottom:8px; }}
        .summary-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:14px; }}
        .summary-item {{ padding:14px; border-radius:12px; text-align:center; background:#f8f9fa; }}
        .summary-item .number {{ font-size:26px; font-weight:bold; }}
        .summary-item .label {{ font-size:12px; color:#888; margin-top:4px; }}
        .stat-pass .number {{ color:#4CAF50; }}
        .stat-cond .number {{ color:#FF9800; }}
        .stat-fail .number {{ color:#f44336; }}
        table {{ width:100%; border-collapse:collapse; font-size:12px; }}
        th {{ background:#f8f9fa; padding:10px 6px; text-align:center; font-weight:600;
              color:#555; border-bottom:2px solid #e0e0e0; position:sticky; top:0; }}
        td {{ padding:7px 6px; text-align:center; border-bottom:1px solid #eee; color:#333; }}
        tr:hover {{ background:#f0f4ff !important; }}
        .table-wrap {{ max-height:600px; overflow-y:auto; border-radius:8px; border:1px solid #e0e0e0; }}
        .footer {{ text-align:center; color:rgba(255,255,255,0.7); font-size:12px; padding:20px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="card header">
        <h1>📊 GRR 宽表分析汇总报告</h1>
        <div class="header-info">
            <span>📁 数据文件: {os.path.basename(file_path)}</span>
            <span>📐 分析方法: {method}</span>
            <span>📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
        </div>
    </div>

    <div class="card">
        <h2>📋 研究概要</h2>
        <div class="summary-grid">
            <div class="summary-item"><div class="number">{n_op}</div><div class="label">操作员</div></div>
            <div class="summary-item"><div class="number">{n_pt}</div><div class="label">零件</div></div>
            <div class="summary-item"><div class="number">{n_trials}</div><div class="label">试验次数</div></div>
            <div class="summary-item"><div class="number">{len(summary_list)}</div><div class="label">测量参数</div></div>
            <div class="summary-item stat-pass"><div class="number">{n_pass}</div><div class="label">✅ 合格</div></div>
            <div class="summary-item stat-cond"><div class="number">{n_cond}</div><div class="label">⚠️ 条件接受</div></div>
            <div class="summary-item stat-fail"><div class="number">{n_fail}</div><div class="label">❌ 不合格</div></div>
        </div>
    </div>

    <div class="card">
        <h2>📊 各参数 GRR 结果汇总 (按 %SV 降序)</h2>
        <div class="table-wrap">
        <table>
            <thead><tr>
                <th>测量参数</th><th>EV(重复性)</th><th>AV(再现性)</th>
                <th>GRR(合计)</th><th>PV(零件)</th><th>%EV</th><th>%AV</th><th>%GRR</th>{'<th>%TOL</th>' if has_tol else ''}<th>ndc</th><th>判定</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        </div>
    </div>

    <div class="card">
        <h2>📐 %GRR 判定标准</h2>
        <table>
            <thead><tr><th>%GRR 范围</th><th>判定</th><th>说明</th></tr></thead>
            <tbody>
                <tr><td>&lt; 10%</td><td style="color:#4CAF50;font-weight:bold">✅ 合格</td><td>测量系统可接受</td></tr>
                <tr><td>10% ~ 30%</td><td style="color:#FF9800;font-weight:bold">⚠️ 有条件接受</td><td>根据应用场景决定</td></tr>
                <tr><td>≥ 30%</td><td style="color:#f44336;font-weight:bold">❌ 不合格</td><td>测量系统需改进</td></tr>
                <tr><td>ndc ≥ 5</td><td style="color:#4CAF50;font-weight:bold">✅</td><td>足够的分辨力</td></tr>
                <tr><td>ndc &lt; 5</td><td style="color:#f44336;font-weight:bold">❌</td><td>分辨力不足</td></tr>
            </tbody>
        </table>
    </div>

    <div class="footer">
        GRR 宽表分析汇总报告 — SPC统计分析工具 自动生成 — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</div>
</body>
</html>"""

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return output_path


def _generate_wide_summary_md(
    summary_list: List[Dict], file_path: str, output_path: str,
    n_op: int, n_pt: int, n_trials: int, method: str,
    spec_limits: Optional[Dict] = None
) -> str:
    """生成宽表 GRR 分析的汇总 Markdown 报告。"""
    sorted_list = sorted(summary_list, key=lambda x: x['pct_grr'], reverse=True)
    n_pass = sum(1 for s in summary_list if s['pct_grr'] < 10)
    n_cond = sum(1 for s in summary_list if 10 <= s['pct_grr'] < 30)
    n_fail = sum(1 for s in summary_list if s['pct_grr'] >= 30)
    has_tol = spec_limits is not None

    lines = [
        f"# GRR 宽表分析汇总报告\n",
        f"**数据文件**: {os.path.basename(file_path)}  ",
        f"**分析方法**: {method}  ",
        f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"---\n",
        f"## 1. 研究概要\n",
        f"| 项目 | 值 |",
        f"|------|-----|",
        f"| 操作员数量 | {n_op} |",
        f"| 零件数量 | {n_pt} |",
        f"| 试验次数 | {n_trials} |",
        f"| 测量参数数量 | {len(summary_list)} |",
        f"| 规格限来源 | {'YAML配置' if has_tol else '未提供'} |",
        f"| ✅ 合格参数 | {n_pass} |",
        f"| ⚠️ 有条件接受 | {n_cond} |",
        f"| ❌ 不合格参数 | {n_fail} |\n",
        f"---\n",
        f"## 2. 各参数 GRR 结果汇总\n",
    ]

    if has_tol:
        lines.append(f"| 测量参数 | EV | AV | GRR | PV | %EV | %AV | %GRR | %TOL | ndc | 判定 |")
        lines.append(f"|----------|-----|-----|------|-----|------|------|------|------|-----|------|")
    else:
        lines.append(f"| 测量参数 | EV | AV | GRR | PV | %EV | %AV | %GRR | ndc | 判定 |")
        lines.append(f"|----------|-----|-----|------|-----|------|------|------|-----|------|")

    for s in sorted_list:
        pct = s['pct_grr']
        if pct < 10:
            verdict = '✅ 合格'
        elif pct < 30:
            verdict = '⚠️ 条件接受'
        else:
            verdict = '❌ 不合格'

        pct_ev = s.get('pct_ev', 0)
        pct_av = s.get('pct_av', 0)
        row = (f"| {s['parameter']} | {s['EV']:.6f} | {s['AV']:.6f} | "
               f"{s['GRR']:.6f} | {s['PV']:.6f} | {pct_ev:.2f}% | {pct_av:.2f}% | **{pct:.2f}%**")
        if has_tol:
            pct_tol = s.get('pct_tol')
            if pct_tol is not None:
                row += f" | **{pct_tol:.2f}%**"
            else:
                row += " | -"
        row += f" | {s['ndc']} | {verdict} |"
        lines.append(row)

    lines.append(f"\n---\n")
    lines.append(f"## 3. 判定标准\n")
    lines.append(f"| 指标 | 范围 | 判定 | 说明 |")
    lines.append(f"|------|------|------|------|")
    lines.append(f"| %EV / %AV / %GRR / %TOL | < 10% | ✅ 合格 | 测量系统可接受 |")
    lines.append(f"| %EV / %AV / %GRR / %TOL | 10% ~ 30% | ⚠️ 有条件接受 | 根据应用场景决定 |")
    lines.append(f"| %EV / %AV / %GRR / %TOL | ≥ 30% | ❌ 不合格 | 测量系统需改进 |")
    lines.append(f"| ndc | ≥ 5 | ✅ | 足够的分辨力 |")
    lines.append(f"| ndc | < 5 | ❌ | 分辨力不足 |")
    if has_tol:
        lines.append(f"\n> **%EV** = %Repeatability = (σ_EV / σ_TV) × 100%")
        lines.append(f"> **%AV** = %Reproducibility = (σ_AV / σ_TV) × 100%")
        lines.append(f"> **%GRR** = %Gage R&R = (σ_GRR / σ_TV) × 100%")
        lines.append(f"> **%TOL** = %Tolerance = (6σ_GRR / (USL - LSL)) × 100%")
    else:
        lines.append(f"\n> **%EV** = %Repeatability = (σ_EV / σ_TV) × 100%")
        lines.append(f"> **%AV** = %Reproducibility = (σ_AV / σ_TV) × 100%")
        lines.append(f"> **%GRR** = %Gage R&R = (σ_GRR / σ_TV) × 100%")
    lines.append(f"\n---\n")
    lines.append(f"*报告由 SPC统计分析工具 自动生成 — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return output_path


# ================================ 宽表 GRR 分析主函数 ================================


def analyze_grr_wide(
    file_path: str,
    n_operators: int = 3,
    n_parts: int = 10,
    operator_names: Optional[List[str]] = None,
    part_names: Optional[List[str]] = None,
    output_dir: Optional[str] = None,
    method: str = 'ANOVA',
    parameters: Optional[List[str]] = None,
    detailed_params: Optional[List[str]] = None,
    spec_limits: Optional[Dict[str, Tuple[float, float]]] = None,
    sheet_name: Optional[str] = None
) -> Dict:
    """
    宽表格式 GRR 分析主函数。

    自动将宽表数据转换为长表格式，对每个测量参数执行 GRR 分析，
    并生成汇总报告。

    参数:
        file_path : str              - 数据文件路径 (.csv / .xlsx / .xls)
        n_operators : int            - 操作员数量 (默认: 3)
        n_parts : int                - 零件数量 (默认: 10)
        operator_names : list, 可选   - 操作员名称 (默认: ['Operator_1', ...])
        part_names : list, 可选       - 零件名称 (默认: ['Part_1', ...])
        output_dir : str, 可选        - 报告输出目录
        method : str                 - 分析方法: 'ANOVA' 或 'AIAG' (默认: 'ANOVA')
        parameters : list, 可选       - 指定分析的参数列表 (默认: 所有数值列)
        detailed_params : list, 可选  - 需要生成详细报告的参数 (默认: 仅汇总)
        spec_limits : dict, 可选      - 规格限 {参数名: (LSL, USL)}
                                        用于计算 %Tolerance = 6σ_GRR / (USL-LSL) × 100%
                                        可从 YAML 配置文件的 spec_limits 读取
        sheet_name : str, 可选        - Excel 工作表名称

    返回:
        dict - {
            'summary_list': list,       # 各参数 GRR 结果列表 (含 %SV 和 %TOL)
            'summary_html': str,        # 汇总 HTML 报告路径
            'summary_md': str,          # 汇总 Markdown 报告路径
            'detailed_reports': dict,   # 各参数详细报告 {参数名: {html, md, pdf}}
            'n_pass': int,              # 合格参数数 (%SV)
            'n_conditional': int,       # 有条件接受参数数 (%SV)
            'n_fail': int,              # 不合格参数数
        }
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(file_path)), 'grr_reports')
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # 步骤1: 宽表→长表转换
    print(f"\n{'='*60}")
    print(f"📂 宽表 GRR 分析")
    print(f"{'='*60}")
    long_df, numeric_cols = convert_wide_to_long(
        file_path, n_operators, n_parts, operator_names, part_names, sheet_name
    )

    # 过滤指定参数
    if parameters:
        numeric_cols = [c for c in numeric_cols if c in parameters]
        if not numeric_cols:
            raise ValueError(f"指定的参数在数据中未找到: {parameters}")

    print(f"\n📐 分析方法: {method}")
    print(f"📊 待分析参数: {len(numeric_cols)} 个\n")

    # 步骤2: 对每个参数执行 GRR 分析
    summary_list = []
    detailed_reports = {}
    n_total = len(numeric_cols)

    for i, param in enumerate(numeric_cols, 1):
        # 提取该参数的子数据
        param_df = long_df[long_df['parameter'] == param].copy()
        if param_df.empty:
            continue

        try:
            if method.upper() == 'ANOVA':
                result = _grr_anova(param_df)
            else:
                result = _grr_aiag(param_df)

            av_val = np.sqrt(result['sigma2_o']) if method == 'ANOVA' else result['AV']

            # 计算 %Study Variation 各分量
            # %EV = (EV / TV) × 100% = (σ_repeatability / σ_total) × 100%
            # %AV = (AV / TV) × 100% = (σ_reproducibility / σ_total) × 100%
            # %GRR = (GRR / TV) × 100% = %SV (已计算)
            std_tv = result['std_tv']
            pct_ev = (result['EV'] / std_tv * 100) if std_tv > 0 else 0
            pct_av = (av_val / std_tv * 100) if std_tv > 0 else 0
            pct_grr = result['pct_grr']

            # 计算 %Tolerance (如果提供了规格限)
            # %TOL = (6 × σ_GRR / (USL - LSL)) × 100%
            pct_tol = None
            if spec_limits and param in spec_limits:
                lsl, usl = spec_limits[param]
                tolerance = usl - lsl
                if tolerance > 0:
                    pct_tol = (6 * result['std_grr'] / tolerance) * 100

            summary_list.append({
                'parameter': param,
                'EV': result['EV'],
                'AV': av_val,
                'GRR': result['std_grr'],
                'PV': result['std_pv'],
                'TV': std_tv,
                'pct_ev': pct_ev,               # %Repeatability (%EV)
                'pct_av': pct_av,               # %Reproducibility (%AV)
                'pct_grr': pct_grr,             # %Gage R&R (%SV)
                'pct_tol': pct_tol,             # %Tolerance (%TOL)
                'ndc': result['ndc'],
                'result': result,
            })

            # 打印进度
            pct = pct_grr
            if pct < 10:
                verdict = '✅'
            elif pct < 30:
                verdict = '⚠️'
            else:
                verdict = '❌'
            tol_str = f", %TOL={pct_tol:.2f}%" if pct_tol is not None else ""
            print(f"   [{i}/{n_total}] {param}: %EV={pct_ev:.2f}%, %AV={pct_av:.2f}%, %GRR={pct:.2f}%{tol_str}, ndc={result['ndc']} {verdict}")

            # 生成详细报告 (如果指定)
            if detailed_params and param in detailed_params:
                param_dir = os.path.join(output_dir, 'detailed', param)
                os.makedirs(param_dir, exist_ok=True)
                md_p = os.path.join(param_dir, f"{param}_grr_{timestamp}.md")
                html_p = os.path.join(param_dir, f"{param}_grr_{timestamp}.html")
                pdf_p = os.path.join(param_dir, f"{param}_grr_{timestamp}.pdf")
                generate_markdown_report(result, param_df, file_path, md_p)
                generate_html_report(result, param_df, file_path, html_p)
                generate_pdf_report(result, param_df, file_path, pdf_p)
                detailed_reports[param] = {
                    'markdown_path': md_p,
                    'html_path': html_p,
                    'pdf_path': pdf_p,
                }

        except Exception as e:
            print(f"   [{i}/{n_total}] {param}: ⚠️ 分析失败 - {e}")

    # 步骤3: 生成汇总报告
    n_pass = sum(1 for s in summary_list if s['pct_grr'] < 10)
    n_cond = sum(1 for s in summary_list if 10 <= s['pct_grr'] < 30)
    n_fail = sum(1 for s in summary_list if s['pct_grr'] >= 30)

    summary_html = os.path.join(output_dir, f"{base_name}_grr_summary_{timestamp}.html")
    summary_md = os.path.join(output_dir, f"{base_name}_grr_summary_{timestamp}.md")

    print(f"\n📄 生成汇总 Markdown 报告: {summary_md}")
    _generate_wide_summary_md(
        summary_list, file_path, summary_md,
        n_operators, n_parts, n_total, method, spec_limits
    )

    print(f"📄 生成汇总 HTML 报告: {summary_html}")
    _generate_wide_summary_html(
        summary_list, file_path, summary_html,
        n_operators, n_parts, n_total, method, spec_limits
    )

    # 打印汇总
    print(f"\n{'='*60}")
    print(f"📊 GRR 宽表分析汇总:")
    print(f"   总参数数:       {len(summary_list)}")
    print(f"   ✅ 合格:        {n_pass} ({n_pass/len(summary_list)*100:.1f}%)")
    print(f"   ⚠️ 有条件接受:  {n_cond} ({n_cond/len(summary_list)*100:.1f}%)")
    print(f"   ❌ 不合格:      {n_fail} ({n_fail/len(summary_list)*100:.1f}%)")
    if detailed_params:
        print(f"   详细报告:       {len(detailed_reports)} 个参数")
    print(f"{'='*60}")
    print(f"\n🎉 所有报告生成完成！")

    return {
        'summary_list': summary_list,
        'summary_html': summary_html,
        'summary_md': summary_md,
        'detailed_reports': detailed_reports,
        'n_pass': n_pass,
        'n_conditional': n_cond,
        'n_fail': n_fail,
    }


# ================================ 命令行入口 ================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="GRR 测量系统分析工具 — 生成 HTML/Markdown/PDF 报告"
    )
    parser.add_argument("--file", "-f", type=str, required=True,
                        help="数据文件路径 (.csv / .xlsx / .xls)")
    parser.add_argument("--method", type=str, default="ANOVA", choices=['ANOVA', 'AIAG'],
                        help="分析方法 (默认: ANOVA)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="报告输出目录")
    parser.add_argument("--sheet", type=str, default=None,
                        help="Excel 工作表名称")

    # 长表模式参数 (默认)
    parser.add_argument("--operator", type=str, default="operator",
                        help="[长表模式] 操作员列名 (默认: operator)")
    parser.add_argument("--part", type=str, default="part",
                        help="[长表模式] 零件列名 (默认: part)")
    parser.add_argument("--value", type=str, default="value",
                        help="[长表模式] 测量值列名 (默认: value)")

    # 宽表模式参数
    parser.add_argument("--wide", "-w", action="store_true",
                        help="启用宽表模式 (数据按 GRR 实验顺序排列，每行多列测量参数)")
    parser.add_argument("--n-operators", type=int, default=3,
                        help="[宽表模式] 操作员数量 (默认: 3)")
    parser.add_argument("--n-parts", type=int, default=10,
                        help="[宽表模式] 零件数量 (默认: 10)")
    parser.add_argument("--op-names", type=str, nargs='+', default=None,
                        help="[宽表模式] 操作员名称 (例: --op-names Op_A Op_B Op_C)")
    parser.add_argument("--pt-names", type=str, nargs='+', default=None,
                        help="[宽表模式] 零件名称 (例: --pt-names P1 P2 ... P10)")
    parser.add_argument("--params", type=str, nargs='+', default=None,
                        help="[宽表模式] 指定分析的参数列名 (默认: 所有数值列)")
    parser.add_argument("--detailed", type=str, nargs='+', default=None,
                        help="[宽表模式] 需要生成详细报告的参数 (默认: 仅汇总)")

    # 规格限参数 (用于计算 %Tolerance)
    parser.add_argument("--config", type=str, default=None,
                        help="YAML 配置文件路径 (读取 spec_limits 计算 %%Tolerance)")
    parser.add_argument("--project", type=str, default=None,
                        help="YAML 配置文件中的项目 ID")

    args = parser.parse_args()

    # 从 YAML 配置读取规格限
    spec_limits = None
    if args.config:
        try:
            from config_loader import ConfigLoader
            loader = ConfigLoader(args.config)
            loader.load()
            if args.project:
                project_cfg = loader.get_project(args.project)
            else:
                # 默认使用第一个项目
                projects = loader.list_projects()
                if projects:
                    project_cfg = loader.get_project(projects[0][0])
                else:
                    project_cfg = None
            if project_cfg and hasattr(project_cfg, 'spec_limits'):
                spec_limits = project_cfg.spec_limits
                print(f"📋 从 YAML 加载规格限: {len(spec_limits)} 个参数")
        except Exception as e:
            print(f"⚠️ 读取 YAML 配置失败: {e}")
            print("   将不计算 %Tolerance")

    if args.wide:
        # 宽表模式
        analyze_grr_wide(
            file_path=args.file,
            n_operators=args.n_operators,
            n_parts=args.n_parts,
            operator_names=args.op_names,
            part_names=args.pt_names,
            output_dir=args.output,
            method=args.method,
            parameters=args.params,
            detailed_params=args.detailed,
            spec_limits=spec_limits,
            sheet_name=args.sheet,
        )
    else:
        # 长表模式 (默认)
        analyze_grr(
            file_path=args.file,
            operator_col=args.operator,
            part_col=args.part,
            value_col=args.value,
            output_dir=args.output,
            method=args.method,
            sheet_name=args.sheet,
        )
