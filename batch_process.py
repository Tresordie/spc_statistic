# -*- encoding: utf-8 -*-
"""
@File    :   batch_process.py
@Time    :   2026/06/17
@Author  :   SimonYuan
@Version :   1.0
@Desc    :   批量处理多个CSV文件的示例脚本

使用方法:
1. 修改 csv_files 列表,添加你的CSV文件
2. 运行: python batch_process.py
3. 程序会为每个CSV文件生成独立的报告
"""

import os
import sys

# 导入配置和主程序
from spc_config import SPEC_LIMITS
import spc_analysis

# ========================================
# 批量处理配置
# ========================================

# 方式1: 指定CSV文件列表
csv_files = [
    "./Metro_EHM_BFT_301_summary_sort_20260610_174146.csv",
    "./Metro_EHM_BFT_302_summary_sort_20260611_180000.csv",
    "./Metro_EHM_BFT_303_summary_sort_20260612_190000.csv",
    # 添加更多CSV文件...
]

# 方式2: 自动扫描目录中的所有CSV文件
# import glob
# csv_files = glob.glob("./data/*.csv")

# 输出目录配置
OUTPUT_BASE_DIR = "batch_reports"

# ========================================
# 批量处理函数
# ========================================

def process_single_csv(csv_file, spec_limits):
    """
    处理单个CSV文件,生成报告
    
    参数:
        csv_file: CSV文件路径
        spec_limits: 规格限字典
    """
    print()
    print("=" * 70)
    print(f"📊 Processing: {csv_file}")
    print("=" * 70)
    
    # 生成输出文件名(基于CSV文件名)
    base_name = os.path.basename(csv_file).replace('.csv', '')
    output_html = f"{OUTPUT_BASE_DIR}/{base_name}_report.html"
    output_pdf = f"{OUTPUT_BASE_DIR}/{base_name}_report.pdf"
    output_img_dir = f"{OUTPUT_BASE_DIR}/{base_name}_images"
    
    # 创建输出目录
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    
    # 读取数据
    print(f"📖 Reading data from: {csv_file}")
    try:
        df = spc_analysis.pd.read_csv(
            csv_file,
            keep_default_na=True,
            na_values=["", " ", "null", "NULL"]
        )
        print(f"✅ Loaded {len(df)} rows")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # 处理每个测试项目
    stats = []
    fig_dict = {}
    
    print(f"📊 Processing {len(spec_limits)} test items...")
    
    for param, (lsl, usl) in spec_limits.items():
        if param not in df.columns:
            continue
        
        data = spc_analysis.pd.to_numeric(df[param], errors="coerce").dropna()
        
        if len(data) == 0:
            continue
        
        # 计算统计量
        mean_val = spc_analysis.np.mean(data)
        sigma_val = spc_analysis.np.std(data, ddof=1)
        cpk = spc_analysis.calculate_cpk(data, lsl, usl)
        
        if cpk is not None and not spc_analysis.np.isinf(cpk):
            cpk_display = f"{cpk:.3f}"
        else:
            cpk_display = "inf"
        
        stats.append({
            "Parameter": param,
            "Mean": f"{mean_val:.4f}",
            "Sigma": f"{sigma_val:.4f}",
            "LSL": f"{lsl:.4f}",
            "USL": f"{usl:.4f}",
            "Cpk": cpk_display,
            "n": len(data),
        })
        
        # 绘制图表
        os.makedirs(output_img_dir, exist_ok=True)
        img_file = os.path.join(output_img_dir, f"{param.replace('/', '_')}.png")
        fig = spc_analysis.plot_histogram_with_modern_style(
            data, param, lsl, usl, mean_val, sigma_val, cpk, img_file
        )
        fig_dict[param] = fig
    
    if not stats:
        print("⚠️  No valid data found, skipping report generation")
        return False
    
    print(f"✅ Processed {len(stats)} test items")
    
    # 生成HTML报告
    print(f"🌐 Generating HTML report...")
    spc_analysis.generate_html_report(stats, output_img_dir, output_html)
    
    # 生成PDF报告
    print(f"📄 Generating PDF report...")
    spc_analysis.generate_pdf_report(stats, fig_dict, output_pdf)
    
    print(f"✅ Reports generated:")
    print(f"   - HTML: {output_html}")
    print(f"   - PDF:  {output_pdf}")
    print(f"   - Images: {output_img_dir}/")
    
    return True


def main():
    """主函数:批量处理多个CSV文件"""
    
    print("=" * 70)
    print("🚀 SPC Batch Processing Tool")
    print("=" * 70)
    print(f"📁 Found {len(csv_files)} CSV files to process")
    print()
    
    # 统计处理结果
    success_count = 0
    fail_count = 0
    
    # 处理每个CSV文件
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"⚠️  File not found: {csv_file}")
            fail_count += 1
            continue
        
        try:
            if process_single_csv(csv_file, SPEC_LIMITS):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"❌ Error processing {csv_file}: {e}")
            fail_count += 1
    
    # 输出总结
    print()
    print("=" * 70)
    print("📊 BATCH PROCESSING SUMMARY")
    print("=" * 70)
    print(f"Total Files: {len(csv_files)}")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed:  {fail_count}")
    print(f"📁 Reports saved to: {OUTPUT_BASE_DIR}/")
    print("=" * 70)
    
    if success_count > 0:
        print()
        print("🎉 Batch processing completed successfully!")
    else:
        print()
        print("⚠️  No files were processed successfully.")
    
    print()


if __name__ == "__main__":
    main()
