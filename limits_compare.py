#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规格限对比工具

功能：
    将 CSV 文件中的 TEST_NAME 对应的 LOWER_LIMIT、UPPER_LIMIT
    与 spc_config.yaml 中相同 project id 下的 spec_limits 进行对比，
    列出对比结果，重点标示出有差别的项。

使用方法:
    python limits_compare.py --file <CSV文件路径> --project <项目ID>
    python limits_compare.py --file <CSV文件路径> --project <项目ID> --config <YAML配置文件路径>

示例:
    python limits_compare.py --file 20260702105307_PASS_FV2615MEHP2NC0222_Metro_EHM_BFT_301.csv --project ehm_pcba_test
"""

import argparse
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

import pandas as pd
import yaml

# Windows 控制台编码设置
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def load_yaml_config(config_path: str) -> Dict:
    """加载 YAML 配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_project_spec_limits(config: Dict, project_id: str) -> Optional[Dict[str, Tuple[float, float]]]:
    """
    从配置中获取指定项目的规格限

    参数:
        config: YAML 配置字典
        project_id: 项目 ID

    返回:
        {参数名: (LSL, USL)} 或 None
    """
    for project in config.get('projects', []):
        if project.get('id') == project_id:
            spec_limits = project.get('spec_limits', {})
            return {k: tuple(v) for k, v in spec_limits.items()}
    return None


def parse_limit_value(value) -> Optional[float]:
    """
    解析规格限值，尝试转换为浮点数

    参数:
        value: 限值（可能是字符串或数字）

    返回:
        浮点数或 None（如果无法转换）
    """
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def compare_limits(
    csv_file: str,
    project_id: str,
    config_path: str = 'spc_config.yaml'
) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
    """
    对比 CSV 文件中的规格限与 YAML 配置中的规格限

    参数:
        csv_file: CSV 文件路径
        project_id: 项目 ID
        config_path: YAML 配置文件路径

    返回:
        (matched, different, csv_only, yaml_only) 四个列表
    """
    # 加载 YAML 配置
    config = load_yaml_config(config_path)
    yaml_limits = get_project_spec_limits(config, project_id)

    if yaml_limits is None:
        print(f"❌ 错误: 在配置文件中找不到项目 ID '{project_id}'")
        sys.exit(1)

    # 加载 CSV 文件
    df = pd.read_csv(csv_file)

    # 检查必要的列
    required_cols = ['TEST_NAME', 'LOWER_LIMIT', 'UPPER_LIMIT']
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        print(f"❌ 错误: CSV 文件缺少必要的列: {missing_cols}")
        sys.exit(1)

    # 提取唯一的测试项及其规格限
    csv_limits = {}
    for _, row in df[required_cols].drop_duplicates(subset=['TEST_NAME']).iterrows():
        test_name = row['TEST_NAME']
        lsl = parse_limit_value(row['LOWER_LIMIT'])
        usl = parse_limit_value(row['UPPER_LIMIT'])
        if lsl is not None and usl is not None:
            csv_limits[test_name] = (lsl, usl)

    # 对比
    matched = []      # 完全匹配
    different = []    # 有差异
    csv_only = []     # 仅在 CSV 中
    yaml_only = []    # 仅在 YAML 中

    # 检查 CSV 中的每一项
    for test_name, (csv_lsl, csv_usl) in csv_limits.items():
        if test_name in yaml_limits:
            yaml_lsl, yaml_usl = yaml_limits[test_name]

            # 比较（允许微小浮点误差）
            lsl_match = abs(csv_lsl - yaml_lsl) < 1e-9
            usl_match = abs(csv_usl - yaml_usl) < 1e-9

            item = {
                'test_name': test_name,
                'csv_lsl': csv_lsl,
                'csv_usl': csv_usl,
                'yaml_lsl': yaml_lsl,
                'yaml_usl': yaml_usl,
                'lsl_match': lsl_match,
                'usl_match': usl_match,
            }

            if lsl_match and usl_match:
                matched.append(item)
            else:
                different.append(item)
        else:
            csv_only.append({
                'test_name': test_name,
                'csv_lsl': csv_lsl,
                'csv_usl': csv_usl,
            })

    # 检查 YAML 中的每一项
    for test_name, (yaml_lsl, yaml_usl) in yaml_limits.items():
        if test_name not in csv_limits:
            yaml_only.append({
                'test_name': test_name,
                'yaml_lsl': yaml_lsl,
                'yaml_usl': yaml_usl,
            })

    return matched, different, csv_only, yaml_only


def print_comparison_results(
    matched: List[Dict],
    different: List[Dict],
    csv_only: List[Dict],
    yaml_only: List[Dict],
    project_id: str,
    csv_file: str
):
    """打印对比结果"""

    print("\n" + "=" * 80)
    print(f"📊 规格限对比报告")
    print("=" * 80)
    print(f"📁 CSV 文件: {os.path.basename(csv_file)}")
    print(f"📋 项目 ID:  {project_id}")
    print("-" * 80)

    # 统计
    total_csv = len(matched) + len(different) + len(csv_only)
    total_yaml = len(matched) + len(different) + len(yaml_only)

    print(f"\n📈 统计概要:")
    print(f"   CSV 中测试项总数: {total_csv}")
    print(f"   YAML 中测试项总数: {total_yaml}")
    print(f"   ✅ 完全匹配: {len(matched)}")
    print(f"   ❌ 存在差异: {len(different)}")
    print(f"   ⚠️  仅在 CSV 中: {len(csv_only)}")
    print(f"   ⚠️  仅在 YAML 中: {len(yaml_only)}")

    # 有差异的项（重点显示）
    if different:
        print(f"\n{'=' * 80}")
        print(f"❌ 存在差异的测试项 ({len(different)} 项) - 需要关注!")
        print("=" * 80)
        print(f"{'TEST_NAME':<45} {'CSV LSL':>10} {'YAML LSL':>10} {'CSV USL':>10} {'YAML USL':>10}")
        print("-" * 80)
        for item in sorted(different, key=lambda x: x['test_name']):
            lsl_mark = "  " if item['lsl_match'] else "❌"
            usl_mark = "  " if item['usl_match'] else "❌"
            print(f"{item['test_name']:<45} {lsl_mark}{item['csv_lsl']:>9.4f} {item['yaml_lsl']:>10.4f} {usl_mark}{item['csv_usl']:>9.4f} {item['yaml_usl']:>10.4f}")

    # 完全匹配的项
    if matched:
        print(f"\n{'=' * 80}")
        print(f"✅ 完全匹配的测试项 ({len(matched)} 项)")
        print("=" * 80)
        print(f"{'TEST_NAME':<45} {'LSL':>10} {'USL':>10}")
        print("-" * 80)
        for item in sorted(matched, key=lambda x: x['test_name'])[:20]:  # 只显示前20个
            print(f"{item['test_name']:<45} {item['csv_lsl']:>10.4f} {item['csv_usl']:>10.4f}")
        if len(matched) > 20:
            print(f"   ... 还有 {len(matched) - 20} 项（省略）")

    # 仅在 CSV 中的项
    if csv_only:
        print(f"\n{'=' * 80}")
        print(f"⚠️  仅在 CSV 文件中的测试项 ({len(csv_only)} 项) - YAML 配置缺失")
        print("=" * 80)
        print(f"{'TEST_NAME':<45} {'CSV LSL':>10} {'CSV USL':>10}")
        print("-" * 80)
        for item in sorted(csv_only, key=lambda x: x['test_name']):
            print(f"{item['test_name']:<45} {item['csv_lsl']:>10.4f} {item['csv_usl']:>10.4f}")

    # 仅在 YAML 中的项
    if yaml_only:
        print(f"\n{'=' * 80}")
        print(f"⚠️  仅在 YAML 配置中的测试项 ({len(yaml_only)} 项) - CSV 文件缺失")
        print("=" * 80)
        print(f"{'TEST_NAME':<45} {'YAML LSL':>10} {'YAML USL':>10}")
        print("-" * 80)
        for item in sorted(yaml_only, key=lambda x: x['test_name']):
            print(f"{item['test_name']:<45} {item['yaml_lsl']:>10.4f} {item['yaml_usl']:>10.4f}")

    print(f"\n{'=' * 80}")
    print("对比完成!")
    print("=" * 80 + "\n")


def generate_markdown_report(
    matched: List[Dict],
    different: List[Dict],
    csv_only: List[Dict],
    yaml_only: List[Dict],
    project_id: str,
    csv_file: str,
    output_dir: str = '.'
) -> str:
    """
    生成 Markdown 格式的对比报告

    参数:
        matched: 完全匹配的测试项列表
        different: 存在差异的测试项列表
        csv_only: 仅在 CSV 中的测试项列表
        yaml_only: 仅在 YAML 中的测试项列表
        project_id: 项目 ID
        csv_file: CSV 文件路径
        output_dir: 输出目录

    返回:
        生成的 Markdown 文件路径
    """
    # 生成文件名: {datetime}_{project_id}_limits_compare.markdown
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{project_id}_limits_compare.markdown"
    output_path = os.path.join(output_dir, filename)

    # 统计
    total_csv = len(matched) + len(different) + len(csv_only)
    total_yaml = len(matched) + len(different) + len(yaml_only)

    lines = [
        f"# 📊 规格限对比报告\n",
        f"## 基本信息\n",
        f"| 项目 | 值 |",
        f"|------|-----|",
        f"| CSV 文件 | `{os.path.basename(csv_file)}` |",
        f"| 项目 ID | `{project_id}` |",
        f"| 对比时间 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |\n",
        f"---\n",
        f"## 统计概要\n",
        f"| 统计项 | 数量 |",
        f"|--------|------|",
        f"| CSV 中测试项总数 | {total_csv} |",
        f"| YAML 中测试项总数 | {total_yaml} |",
        f"| ✅ 完全匹配 | {len(matched)} |",
        f"| ❌ 存在差异 | {len(different)} |",
        f"| ⚠️ 仅在 CSV 中 | {len(csv_only)} |",
        f"| ⚠️ 仅在 YAML 中 | {len(yaml_only)} |\n",
    ]

    # 存在差异的项（重点显示）
    if different:
        lines.extend([
            f"---\n",
            f"## ❌ 存在差异的测试项 ({len(different)} 项) - 需要关注!\n",
            f"| TEST_NAME | CSV LSL | YAML LSL | LSL 匹配 | CSV USL | YAML USL | USL 匹配 |",
            f"|-----------|---------|----------|----------|---------|----------|----------|",
        ])
        for item in sorted(different, key=lambda x: x['test_name']):
            lsl_mark = "✅" if item['lsl_match'] else "❌ 不一致"
            usl_mark = "✅" if item['usl_match'] else "❌ 不一致"
            lines.append(
                f"| `{item['test_name']}` | {item['csv_lsl']:.4f} | {item['yaml_lsl']:.4f} | {lsl_mark} | "
                f"{item['csv_usl']:.4f} | {item['yaml_usl']:.4f} | {usl_mark} |"
            )
        lines.append("")

    # 仅在 CSV 中的项
    if csv_only:
        lines.extend([
            f"---\n",
            f"## ⚠️ 仅在 CSV 文件中的测试项 ({len(csv_only)} 项) - YAML 配置缺失\n",
            f"| TEST_NAME | CSV LSL | CSV USL |",
            f"|-----------|---------|---------|",
        ])
        for item in sorted(csv_only, key=lambda x: x['test_name']):
            lines.append(f"| `{item['test_name']}` | {item['csv_lsl']:.4f} | {item['csv_usl']:.4f} |")
        lines.append("")

    # 仅在 YAML 中的项
    if yaml_only:
        lines.extend([
            f"---\n",
            f"## ⚠️ 仅在 YAML 配置中的测试项 ({len(yaml_only)} 项) - CSV 文件缺失\n",
            f"| TEST_NAME | YAML LSL | YAML USL |",
            f"|-----------|----------|----------|",
        ])
        for item in sorted(yaml_only, key=lambda x: x['test_name']):
            lines.append(f"| `{item['test_name']}` | {item['yaml_lsl']:.4f} | {item['yaml_usl']:.4f} |")
        lines.append("")

    # 完全匹配的项（折叠显示，避免报告过长）
    if matched:
        lines.extend([
            f"---\n",
            f"## ✅ 完全匹配的测试项 ({len(matched)} 项)\n",
            f"<details>",
            f"<summary>点击展开完整列表</summary>\n",
            f"| TEST_NAME | LSL | USL |",
            f"|-----------|-----|-----|",
        ])
        for item in sorted(matched, key=lambda x: x['test_name']):
            lines.append(f"| `{item['test_name']}` | {item['csv_lsl']:.4f} | {item['csv_usl']:.4f} |")
        lines.extend(["", "</details>", ""])

    lines.append(f"---\n*报告由规格限对比工具自动生成 — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    # 写入文件
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='对比 CSV 文件中的规格限与 YAML 配置中的规格限',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python limits_compare.py --file data.csv --project ehm_pcba_test
  python limits_compare.py --file data.csv --project ehm_pcba_test --config my_config.yaml
        """
    )

    parser.add_argument("--file", "-f", required=True,
                        help="CSV 数据文件路径 (包含 TEST_NAME, LOWER_LIMIT, UPPER_LIMIT 列)")
    parser.add_argument("--project", "-p", required=True,
                        help="YAML 配置文件中的项目 ID")
    parser.add_argument("--config", "-c", default="spc_config.yaml",
                        help="YAML 配置文件路径 (默认: spc_config.yaml)")
    parser.add_argument("--output", "-o", default=".",
                        help="Markdown 报告输出目录 (默认: 当前目录)")

    args = parser.parse_args()

    # 检查文件是否存在
    if not os.path.exists(args.file):
        print(f"❌ 错误: 找不到文件 '{args.file}'")
        sys.exit(1)

    if not os.path.exists(args.config):
        print(f"❌ 错误: 找不到配置文件 '{args.config}'")
        sys.exit(1)

    # 执行对比
    matched, different, csv_only, yaml_only = compare_limits(
        args.file, args.project, args.config
    )

    # 打印结果
    print_comparison_results(
        matched, different, csv_only, yaml_only,
        args.project, args.file
    )

    # 生成 Markdown 报告
    md_path = generate_markdown_report(
        matched, different, csv_only, yaml_only,
        args.project, args.file, args.output
    )
    print(f"📝 Markdown 报告已生成: {md_path}")

    # 如果有差异，返回非零退出码（可用于 CI/CD）
    if different or csv_only or yaml_only:
        sys.exit(2)  # 表示有差异
    sys.exit(0)


if __name__ == "__main__":
    main()
