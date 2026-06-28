import os
import warnings

import matplotlib.backends.backend_pdf as pdf_backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm

warnings.filterwarnings("ignore")

# fmt: off
spec_limits = {
    "VBATT_ON_4V2"                                 : (4.1, 4.3),
    "PP4V2_VSYS_DYNAMO"                            : (4.1, 4.3),
    "PP4V2_VSYS_SOLAR"                             : (4.1, 4.3),
    "PP4V2_VSYS_MUX"                               : (4.1, 4.3),
    "PP5V0_BOOST"                                  : (4.74, 5.17),
    "PP3V3_SYSTEM"                                 : (3.2, 3.45),
    "DUT_BQ1_VBat"                                 : (3.4, 3.6),
    "DUT_BQ2_VBat"                                 : (3.4, 3.6),
    "Charger_Difference"                           : (-0.1, 0.1),
    "VBATT_Current_IDLE"                           : (0.038, 0.05),
    "AccX"                                         : (-0.01, 0.032),
    "AccY"                                         : (-0.01, 0.04),
    "AccZ"                                         : (-1.1, -0.9),
    "ACC_SQRT"                                     : (0.9, 1.1),
    "GyroX"                                        : (-1.2, 1.2),
    "GyroY"                                        : (-3, 2),
    "GyroZ"                                        : (-1.4, 1.4),
    "PP5V0_T2P_Disabled"                           : (0, 0.2),
    "PP5V0_T2P_Enabled"                            : (4.74, 5.17),
    "MCU_TO_T2P_UART_TXD_5V_OUT_HIGH"              : (4.74, 5.17),
    "MCU_TO_T2P_UART_TXD_5V_OUT_LOW"               : (0, 0.2),
    "T2P_TO_MCU_UART_RXD_5V_IN_HIGH"               : (1, 1),
    "T2P_TO_MCU_UART_RXD_5V_IN_HIGH2"              : (4.74, 5.17),
    "T2P_TO_MCU_UART_RXD_5V_IN_LOW"                : (0, 0),
    "T2P_TO_MCU_UART_RXD_5V_IN_LOW2"               : (0, 0.2),
    "PP5V0_T2P_500mA_Load_Voltage"                 : (4.74, 5.17),
    "PP5V0_T2P_500mA_Load_Current"                 : (0.49, 0.51),
    "PP5V0_T2P_1000mA_Load_OverCurrent_Volt"       : (0, 0.1),
    "PP5V0_T2P_Voltage_ELoad_Disabled"             : (0, 0.1),
    "PP5V0_IMMOB_Disabled"                         : (0, 0.2),
    "PP5V0_IMMOB_Enabled"                          : (4.74, 5.17),
    "PP5V0_IMMOB_500mA_Load_Voltage"               : (4.74, 5.17),
    "PP5V0_IMMOB_500mA_Load_Current"               : (0.49, 0.51),
    "PP5V0_IMMOB_1000mA_Load_OverCurrent_Volt"     : (0, 0.1),
    "PP5V0_IMMOB_Voltage_ELoad_Disabled"           : (0, 0.1),
    "IMMOB_TO_MCU_HALL_5V_IN_HIGH"                 : (1, 1),
    "IMMOB_TO_MCU_HALL_5V_IN_LOW"                  : (0, 0),
    "MCU_BI_IMMOB_IO2_5V_OUT_HIGH_PA7"             : (0, 0),
    "MCU_BI_IMMOB_IO2_5V_OUT_HIGH_Volt"            : (4.74, 5.17),
    "MCU_BI_IMMOB_IO2_5V_OUT_LOW_PA7"              : (1, 1),
    "MCU_BI_IMMOB_IO2_5V_OUT_LOW_Volt"             : (0, 0.2),
    "MCU_BI_IMMOB_IO2_IN_HIGH_PA7"                 : (0, 0),
    "MCU_BI_IMMOB_IO2_IN_HIGH_PC4"                 : (1, 1),
    "MCU_BI_IMMOB_IO2_IN_LOW_PA7"                  : (1, 1),
    "MCU_BI_IMMOB_IO2_IN_LOW_PC4"                  : (0, 0),
    "Motor_Direction1_Voltage"                     : (4.6, 5.0),
    "Motor_Direction1_Current"                     : (0.29, 0.35),
    "Motor_Direction2_Voltage"                     : (-5.0, -4.6),
    "Motor_Direction2_Current"                     : (0.29, 0.35),
    "Fake_Wheel_Power_4Hz"                         : (4.75, 5.25),
    "Motor_Direction2_Halted_Voltage"              : (-0.2, 0.2),
    "Motor_Direction2_Halted_Current"              : (-0.002, 0.002),
    "Battery_Simulator_3V5"                        : (3.45, 3.55),
    "Recovery_Port_NoInput_Detect"                 : (0, 0.2),
    "PPVAR_VCU_CONN_ADCRead_RP_NoInput"            : (0, 0.2),
    "Recovery_Power_Apply"                         : (11.5, 12.5),
    "Recovery_Port_Input_Detect"                   : (1, 1),
    "PPVAR_VCU_CONN_ADCRead_RP_Input"              : (10.5, 12),
    "PP12V0_RECOVERY_RVP_ADCRead_RP_Input"         : (10.5, 12),
    "VBUS1_NTC_Normal_RP"                          : (10.5, 12),
    "VBAT1_NTC_Normal_RP"                          : (3.75, 3.95),
    "IBUS1_NTC_Normal_RP"                          : (450, 650),
    "IBAT1_NTC_Normal_RP"                          : (1200, 1600),
    "VBUS2_NTC_Normal_RP"                          : (10.5, 12),
    "VBAT2_NTC_Normal_RP"                          : (3.75, 3.95),
    "IBUS2_NTC_Normal_RP"                          : (-20, 80),
    "IBAT2_NTC_Normal_RP"                          : (0, 100),
    "Battery_Current_RP12V_NTC_Normal"             : (-1.6, -1.2),
    "VBUS1_NTC_Cold_RP"                            : (11.5, 12.5),
    "VBAT1_NTC_Cold_RP"                            : (3.45, 3.55),
    "IBUS1_NTC_Cold_RP"                            : (0, 100),
    "IBAT1_NTC_Cold_RP"                            : (0, 100),
    "Battery_Current_RP12V_NTC_Cold"               : (0, 0.005),
    "VBUS1_NTC_Hot_RP"                             : (11.5, 12.5),
    "VBAT1_NTC_Hot_RP"                             : (3.45, 3.55),
    "IBUS1_NTC_Hot_RP"                             : (0, 100),
    "IBAT1_NTC_Hot_RP"                             : (0, 100),
    "Battery_Current_RP12V_NTC_Hot"                : (0, 0.005),
    "HCT_DET_State"                                : (1, 1),
    "HCT_Power"                                    : (41.5, 42.5),
    "HCT_Power_Detect_State"                       : (0, 0),
    "PPVAR_VCU_CONN_ADCRead_HCT_Input"             : (11.5, 12.5),
    "VBUS2_NTC_Normal_HCT"                         : (11.5, 12.5),
    "VBAT2_NTC_Normal_HCT"                         : (3.7, 3.85),
    "IBUS2_NTC_Normal_HCT"                         : (300, 450),
    "IBAT2_NTC_Normal_HCT"                         : (900, 1200),
    "Battery_Current_HCT_NTC_Normal"               : (-1.2, -0.9),
    "VBUS2_NTC_Hot_RP"                             : (11.5, 12.5),
    "VBAT2_NTC_Hot_RP"                             : (3.45, 3.55),
    "IBUS2_NTC_Hot_RP"                             : (-20, 90),
    "IBAT2_NTC_Hot_RP"                             : (0, 100),
    "Battery_Current_HCT_NTC_Hot"                  : (0, 0.08),
    "Solar_Power"                                  : (7.75, 8.25),
    "VBUS1_NTC_Normal_SolarLowCurrent"             : (6, 8),
    "VBAT1_NTC_Normal_SolarLowCurrent"             : (3.5, 3.65),
    "IBUS1_NTC_Normal_SolarLowCurrent"             : (150, 300),
    "IBAT1_NTC_Normal_SolarLowCurrent"             : (200, 450),
    "Battery_Current_SolarLowCurrent_NTC_Normal"   : (-0.45, -0.2),
    "Solar_Power_Apply_HighCurrent"                : (7.75, 8.25),
    "VBUS1_NTC_Normal_SolarHighCurrent"            : (6, 8),
    "VBAT1_NTC_Normal_SolarHighCurrent"            : (3.7, 4),
    "IBUS1_NTC_Normal_SolarHighCurrent"            : (500, 900),
    "IBAT1_NTC_Normal_SolarHighCurrent"            : (900, 1600),
    "Battery_Current_SolarHighCurrent_NTC_Normal"  : (-1.6, -0.9),
    "Dynamo_Simulator"                             : (3.5, 4.5),
    "Dynamo_5mph_Doubler_Voltage"                  : (8, 10.5),
    "VBUS2_NTC_Normal_Dynamo5mph"                  : (5, 10.5),
    "VBAT2_NTC_Normal_Dynamo5mph"                  : (3.4, 3.65),
    "IBUS2_NTC_Normal_Dynamo5mph"                  : (0, 150),
    "IBAT2_NTC_Normal_Dynamo5mph"                  : (-100, 150),
    "Battery_Current_Dynamo5mph_NTC_Normal"        : (-0.15, 0.1),
    "Dynamo_Simulator_15mph"                       : (5.75, 6.25),
    "Dynamo_15mph_Doubler_Voltage"                 : (12, 16.5),
    "Dynamo_15mph_Speed_Pulse_Sense"               : (1500, 2500),
    "VBUS2_NTC_Normal_Dynamo15mph"                 : (9.5, 11.5),
    "VBAT2_NTC_Normal_Dynamo15mph"                 : (3.4, 3.65),
    "IBUS2_NTC_Normal_Dynamo15mph"                 : (50, 200),
    "IBAT2_NTC_Normal_Dynamo15mph"                 : (50, 500),
    "Battery_Current_Dynamo15mph_NTC_Normal"       : (-0.5, 0.2),
    "Dynamo_15mph_Doubler_NoLoad"                  : (13, 17),
    "VBUS2_NTC_Normal_Dynamo15mph_NoLoad"          : (11.5, 12.5),
    "VBAT2_NTC_Normal_Dynamo15mph_NoLoad"          : (3.45, 3.55),
    "IBUS2_NTC_Normal_Dynamo15mph_NoLoad"          : (-75, 200),
    "IBAT2_NTC_Normal_Dynamo15mph_NoLoad"          : (0, 100),
    "Battery_Current_Dynamo15mph_NTC_Normal_NoLoad": (0, 0.1),
    "Dynamo_Simulator_40mph"                       : (13.5, 14.5),
    "Dynamo_40mph_Doubler_Voltage"                 : (35, 42),
    "Dynamo_40mph_Doubler_ZenerD504_Temp"          : (10, 45),
    "Dynamo_40mph_Doubler_ZenerD505_Temp"          : (10, 45),
    "VBUS2_NTC_Normal_Dynamo40mph_NoLoad"          : (11.5, 12.5),
    "VBAT2_NTC_Normal_Dynamo40mph_NoLoad"          : (3.45, 3.55),
    "IBUS2_NTC_Normal_Dynamo40mph_NoLoad"          : (-20, 80),
    "IBAT2_NTC_Normal_Dynamo40mph_NoLoad"          : (0, 100),
    "Battery_Current_Dynamo40mph_NTC_Normal_NoLoad": (0, 0.1),
    "PPVAR_VCU_CONN_Power_Input"                   : (11.8, 12.2),
    "PPVAR_VCU_Voltage_Read"                       : (11, 12.5),
    "VBUS2_NTC_Normal_VCU"                         : (11, 12.5),
    "VBAT2_NTC_Normal_VCU"                         : (3.6, 3.9),
    "IBUS2_NTC_Normal_VCU"                         : (250, 500),
    "IBAT2_NTC_Normal_VCU"                         : (900, 1200),
    "Battery_Current_VCU_NTC_Normal"               : (-1.2, -0.9),
    "PPVAR_VCU_Backup_Voltage_OTG_Disabled"        : (10.5, 11.5),
    "CableLock_Voltage"                            : (10.5, 11.5),
    "CableLockConn_ELoad_Voltage"                  : (10, 11.5),
    "IBAT2_NTC_Normal_OTG"                         : (-1500, -900),
    "IBUS2_NTC_Normal_OTG"                         : (-500, -200),
    "TailLight_OTG_Verify"                         : (10, 11.5),
    "TailLight_Enabled_Out_Voltage"                : (10, 11.5),
    "TailLight_Enabled_Out_Current"                : (0, 0.1),
    "TailLight_Disabled_Out_Voltage"               : (0, 0.6),
    "TailLight_Disabled_Out_Current"               : (0, 0.002),
    "LowPower_Mode_Current"                        : (0.002, 0.004),
}
# fmt: on


# ================================ 辅助函数 ================================
def calculate_cpk(data, lsl, usl):
    """计算 Cpk，如果 sigma 为零则返回 inf"""
    if len(data) < 2:
        return None
    mu = np.mean(data)
    sigma = np.std(data, ddof=1)
    if sigma == 0:
        return np.inf
    cpk = min((usl - mu) / (3 * sigma), (mu - lsl) / (3 * sigma))
    return cpk


def plot_histogram_with_norm(data, param_name, lsl, usl, mean, std, cpk, image_path):
    """绘制直方图+拟合正态曲线，并在图中显示 Cpk 值，返回 figure 对象"""
    # 创建A4尺寸的figure
    fig = plt.figure(figsize=(11.69, 8.27), dpi=300)
    
    # 创建主坐标轴，留出标题和说明空间
    ax = fig.add_axes([0.10, 0.15, 0.82, 0.72])
    
    # 绘制直方图
    n, bins, patches = ax.hist(
        data,
        bins=min(30, len(np.unique(data))),
        density=True,
        alpha=0.7,
        color='#3498db',
        edgecolor='#2980b9',
        linewidth=1.0,
        label='Data Distribution'
    )
    
    # 绘制拟合正态曲线
    x = np.linspace(min(data), max(data), 300)
    pdf = norm.pdf(x, mean, std)
    ax.plot(
        x, pdf,
        'r-',
        lw=3,
        label=f'Normal Distribution\n($\mu$={mean:.3f}, $\sigma$={std:.3f})',
        alpha=0.9
    )
    
    # 绘制规格限和均值线
    ax.axvline(lsl, color='#27ae60', linestyle='--', lw=2.5, 
               label=f'LSL = {lsl:.3f}', alpha=0.8)
    ax.axvline(usl, color='#27ae60', linestyle='--', lw=2.5, 
               label=f'USL = {usl:.3f}', alpha=0.8)
    ax.axvline(mean, color='#e67e22', linestyle='-', lw=2.5, 
               label=f'Mean = {mean:.3f}', alpha=0.9)
    
    # Cpk 信息框（放在左上角）
    if np.isinf(cpk):
        cpk_text = 'Cpk = ∞'
        cpk_color = '#27ae60'
    elif cpk >= 1.33:
        cpk_text = f'Cpk = {cpk:.3f} ✓'
        cpk_color = '#27ae60'
    elif cpk >= 1.0:
        cpk_text = f'Cpk = {cpk:.3f} ⚠'
        cpk_color = '#f39c12'
    else:
        cpk_text = f'Cpk = {cpk:.3f} ✗'
        cpk_color = '#e74c3c'
    
    # Cpk框样式
    ax.text(0.02, 0.97, cpk_text,
            transform=ax.transAxes,
            fontsize=14,
            fontweight='bold',
            verticalalignment='top',
            horizontalalignment='left',
            color=cpk_color,
            bbox=dict(
                boxstyle='round,pad=0.6',
                facecolor='white',
                edgecolor=cpk_color,
                alpha=0.95,
                linewidth=2
            ))
    
    # 处理参数名（用于标题显示）
    display_name = param_name.replace('_', ' ')
    if len(display_name) > 60:
        # 长参数名分行显示
        words = display_name.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 > 55:
                lines.append(current_line)
                current_line = word
            else:
                current_line += (' ' if current_line else '') + word
        if current_line:
            lines.append(current_line)
        display_name = '\n'.join(lines)
    
    # 标题（使用参数名和样本数）
    ax.set_title(
        f'Parameter: {display_name}',
        fontsize=16,
        fontweight='bold',
        pad=20,
        color='#2c3e50'
    )
    
    # 副标题（样本数）
    ax.text(0.5, -0.15, f'Sample Size: n = {len(data)}',
            transform=ax.transAxes,
            fontsize=11,
            ha='center',
            color='#7f8c8d')
    
    # 轴标签
    ax.set_xlabel('Value', fontsize=13, fontweight='bold', 
                  color='#2c3e50', labelpad=10)
    ax.set_ylabel('Probability Density', fontsize=13, 
                  fontweight='bold', color='#2c3e50', labelpad=10)
    
    # 图例（放在右上角外侧）
    ax.legend(
        loc='upper right',
        fontsize=9.5,
        framealpha=0.9,
        edgecolor='#bdc3c7',
        facecolor='#f8f9fa'
    )
    
    # 网格
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.8, 
            color='#95a5a6')
    
    # 刻度样式
    ax.tick_params(axis='both', which='major', labelsize=10,
                   colors='#34495e')
    
    # 设置坐标轴边框颜色
    for spine in ax.spines.values():
        spine.set_color('#bdc3c7')
        spine.set_linewidth(1.2)
    
    # 自动调整布局
    plt.tight_layout()
    
    # 保存PNG（用于HTML）
    plt.savefig(image_path, dpi=150, bbox_inches='tight')
    
    return fig


# ================================ 主程序 ================================
def generate_report(
    csv_file_path,
    output_html="test_report.html",
    output_pdf="test_report.pdf",
    img_dir="report_images",
):
    df = pd.read_csv(
        csv_file_path, keep_default_na=True, na_values=["", " ", "null", "NULL"]
    )
    print(f"Loaded {len(df)} rows from {csv_file_path}")

    stats = []
    os.makedirs(img_dir, exist_ok=True)

    # 存储每个参数对应的 figure 对象，用于 PDF 生成
    fig_dict = {}

    for param, (lsl, usl) in spec_limits.items():
        if param not in df.columns:
            print(f"Warning: Column '{param}' not found, skipping.")
            continue
        data = pd.to_numeric(df[param], errors="coerce").dropna()
        if len(data) == 0:
            print(f"Warning: No valid numeric data for '{param}', skipping.")
            continue

        mean_val = np.mean(data)
        sigma_val = np.std(data, ddof=1)
        cpk = calculate_cpk(data, lsl, usl)
        cpk_display = f"{cpk:.3f}" if cpk is not None and not np.isinf(cpk) else "inf"

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

        img_file = os.path.join(img_dir, f"{param.replace('/', '_')}.png")
        fig = plot_histogram_with_norm(
            data, param, lsl, usl, mean_val, sigma_val, cpk, img_file
        )
        fig_dict[param] = fig  # 保存 figure 供 PDF 使用

    # ------------------- 生成 HTML (现代化设计) -------------------
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EHM PCBA Statistical Summary Report</title>
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
                <h1>📊 EHM PCBA Statistical Summary</h1>
                <p>Comprehensive Statistical Process Control Analysis Report</p>
            </div>
            
            <div class="stats-summary">
                <div class="stat-card">
                    <div class="number">""" + str(len(stats)) + """</div>
                    <div class="label">Total Parameters</div>
                </div>
                <div class="stat-card">
                    <div class="number">""" + str(sum(s['n'] for s in stats)) + """</div>
                    <div class="label">Total Samples</div>
                </div>
                <div class="stat-card">
                    <div class="number">""" + str(len([s for s in stats if s['Cpk'] != 'inf' and float(s['Cpk']) >= 1.33])) + """</div>
                    <div class="label">Cpk ≥ 1.33</div>
                </div>
                <div class="stat-card">
                    <div class="number">""" + str(len([s for s in stats if s['Cpk'] != 'inf' and float(s['Cpk']) < 1.33 and float(s['Cpk']) >= 1.0])) + """</div>
                    <div class="label">1.0 ≤ Cpk < 1.33</div>
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
    
    for s in stats:
        # 根据Cpk值设置颜色类
        try:
            if s['Cpk'] == 'inf':
                cpk_class = 'cpk-good'
            else:
                cpk_val = float(s['Cpk'])
                if cpk_val >= 1.33:
                    cpk_class = 'cpk-good'
                elif cpk_val >= 1.0:
                    cpk_class = 'cpk-warning'
                else:
                    cpk_class = 'cpk-bad'
        except:
            cpk_class = ''
        
        html_content += f"""                            <tr>
                                <td>{s['Parameter']}</td>
                                <td>{s['Mean']}</td>
                                <td>{s['Sigma']}</td>
                                <td>{s['LSL']}</td>
                                <td>{s['USL']}</td>
                                <td class="{cpk_class}">{s['Cpk']}</td>
                                <td>{s['n']}</td>
                            </tr>
"""
    
    html_content += """                        </tbody>
                    </table>
                </div>
                
                <h2 class="section-title">📈 Distribution Plots</h2>
                <div class="plots-grid">
"""
    
    for s in stats:
        param_safe = s["Parameter"].replace("/", "_")
        img_file = os.path.join(img_dir, f"{param_safe}.png")
        html_content += f"""                    <div class="plot-card">
                        <div class="plot-header">{s['Parameter']}</div>
                        <div class="plot-body">
                            <img src="{img_file}" alt="{s['Parameter']} Distribution">
                        </div>
                    </div>
"""
    
    html_content += """                </div>
            </div>
            
            <div class="footer">
                <p>Generated by EHM PCBA SPC Analysis Tool | Statistical Process Control Report</p>
            </div>
        </div>
    </body>
    </html>"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML report saved to {output_html}")

    # ------------------- 生成 PDF (高分辨率、专业排版) -------------------
    from matplotlib.patches import FancyBboxPatch
    
    with pdf_backend.PdfPages(output_pdf) as pdf:
        # ====== 第一部分：统计表格 ======
        # 每页显示的行数（优化后的值）
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
                table_data.append([
                    s["Parameter"].replace('_', '_'),  # 保持原样，后续处理
                    s["Mean"],
                    s["Sigma"],
                    s["LSL"],
                    s["USL"],
                    s["Cpk"],
                    str(s["n"])
                ])
            
            columns = ["Parameter", "Mean", "Sigma", "LSL", "USL", "Cpk", "n"]
            
            # 创建坐标轴，留出标题空间
            ax = fig_table.add_axes([0.05, 0.05, 0.90, 0.88])
            ax.axis('off')
            
            # 创建表格
            table = ax.table(
                cellText=table_data,
                colLabels=columns,
                loc='center',
                cellLoc='center',
                colWidths=[0.32, 0.12, 0.12, 0.11, 0.11, 0.11, 0.11]
            )
            
            # 表格整体样式
            table.auto_set_font_size(False)
            table.set_fontsize(7)
            table.scale(1, 1.5)
            
            # 设置表头样式
            for col_idx in range(len(columns)):
                cell = table[0, col_idx]
                cell.set_facecolor('#2c3e50')
                cell.set_text_props(color='white', fontweight='bold', fontsize=7.5)
                cell.set_edgecolor('#34495e')
                cell.set_linewidth(1.5)
            
            # 设置数据行样式
            for row_idx in range(1, actual_rows + 1):
                # 交替行背景色
                if row_idx % 2 == 1:
                    bg_color = '#ffffff'
                else:
                    bg_color = '#f8f9fa'
                
                for col_idx in range(len(columns)):
                    cell = table[row_idx, col_idx]
                    cell.set_facecolor(bg_color)
                    cell.set_edgecolor('#dee2e6')
                    cell.set_linewidth(0.5)
                    
                    # 数据列居中对齐
                    if col_idx > 0:
                        cell.set_text_props(ha='center', va='center')
                
                # Parameter列特殊处理：左对齐 + 长文本换行
                param_cell = table[row_idx, 0]
                param_text = param_cell.get_text().get_text()
                
                # 智能换行处理
                if len(param_text) > 28:
                    words = param_text.split('_')
                    lines = []
                    current_line = ""
                    
                    for word in words:
                        test_line = current_line + ('_' if current_line else '') + word
                        if len(test_line) > 28 and current_line:
                            lines.append(current_line)
                            current_line = word
                        else:
                            current_line = test_line
                    
                    if current_line:
                        lines.append(current_line)
                    
                    wrapped_text = '\n'.join(lines)
                    param_cell.get_text().set_text(wrapped_text)
                    param_cell.set_text_props(ha='left', va='center', fontsize=6.5)
                else:
                    param_cell.set_text_props(ha='left', va='center')
            
            # 添加页面标题
            if total_pages > 1:
                title_text = f"EHM PCBA Statistical Summary (Page {page_idx + 1}/{total_pages})"
            else:
                title_text = "EHM PCBA Statistical Summary"
            
            fig_table.text(0.5, 0.96, title_text, 
                          ha='center', va='top',
                          fontsize=14, fontweight='bold',
                          color='#2c3e50')
            
            # 保存PDF页
            pdf.savefig(fig_table, dpi=300, bbox_inches='tight')
            plt.close(fig_table)
        
        # ====== 第二部分：分布图 ======
        for idx, s in enumerate(stats):
            param = s["Parameter"]
            if param in fig_dict:
                fig = fig_dict[param]
                
                # 添加页脚信息
                fig.text(0.5, 0.02, 
                        f"EHM PCBA Test Report - {param} ({idx + 1}/{len(stats)})",
                        ha='center', va='bottom',
                        fontsize=8, color='#7f8c8d',
                        alpha=0.7)
                
                # 保存到PDF
                pdf.savefig(fig, dpi=300, bbox_inches='tight')
                plt.close(fig)

    print(f"High-resolution PDF report saved to {output_pdf}")


if __name__ == "__main__":
    # ========== 在这里直接指定 CSV 文件路径 ==========
    csv_file = "./Metro_EHM_BFT_301_summary_sort_20260610_174146.csv"  # 请修改为您的实际 CSV 文件名或完整路径
    output_html = "30cyles_verification_after_improved_upper_plate.html"
    output_pdf = "30cyles_verification_after_improved_upper_plate.pdf"
    img_dir = "30cyles_verification_after_improved_upper_plate"
    # ==============================================
    generate_report(csv_file, output_html, output_pdf, img_dir)
