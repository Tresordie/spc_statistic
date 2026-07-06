# 📊 规格限对比报告

## 基本信息

| 项目 | 值 |
|------|-----|
| CSV 文件 | `20260702144115_PASS_FV2615MEHM2000038_Metro_EHM_Module_302.csv` |
| 项目 ID | `ehm_module_test` |
| 对比时间 | 2026-07-02 17:54:25 |

---

## 统计概要

| 统计项 | 数量 |
|--------|------|
| CSV 中测试项总数 | 71 |
| YAML 中测试项总数 | 72 |
| ✅ 完全匹配 | 71 |
| ❌ 存在差异 | 0 |
| ⚠️ 仅在 CSV 中 | 0 |
| ⚠️ 仅在 YAML 中 | 1 |

---

## ⚠️ 仅在 YAML 配置中的测试项 (1 项) - CSV 文件缺失

| TEST_NAME | YAML LSL | YAML USL |
|-----------|----------|----------|
| `HCT_BQ2_VAC1.1` | 11.5000 | 12.5000 |

---

## ✅ 完全匹配的测试项 (71 项)

<details>
<summary>点击展开完整列表</summary>

| TEST_NAME | LSL | USL |
|-----------|-----|-----|
| `Charger_Difference` | -0.1000 | 0.1000 |
| `Dynamo15mph_BQ2_IBat` | 200.0000 | 300.0000 |
| `Dynamo15mph_BQ2_IBus` | 50.0000 | 300.0000 |
| `Dynamo15mph_BQ2_VAC1` | 10.0000 | 11.0000 |
| `Dynamo15mph_BQ2_VAC2` | 10.0000 | 11.0000 |
| `Dynamo15mph_BQ2_VBat` | 3.4000 | 3.8500 |
| `Dynamo15mph_BQ2_VBus` | 10.0000 | 11.0000 |
| `Dynamo5mph_BQ2_IBat` | -100.0000 | 300.0000 |
| `Dynamo5mph_BQ2_IBus` | 10.0000 | 200.0000 |
| `Dynamo5mph_BQ2_VAC1` | 6.0000 | 10.0000 |
| `Dynamo5mph_BQ2_VAC2` | 6.0000 | 10.0000 |
| `Dynamo5mph_BQ2_VBat` | 3.4000 | 3.8500 |
| `Dynamo5mph_BQ2_VBus` | 6.0000 | 10.0000 |
| `Dynamo_Doubler_Voltage_15mph` | 10.5000 | 12.5000 |
| `Dynamo_Doubler_Voltage_5mph` | 6.5000 | 10.0000 |
| `Dynamo_Simulator` | 3.5000 | 4.5000 |
| `Dynamo_Simulator_15mph` | 5.5000 | 6.5000 |
| `Dynamo_Speed_Sense` | 20.0000 | 40.0000 |
| `EHM_BQ1_IBat` | 1200.0000 | 1600.0000 |
| `EHM_BQ1_IBus` | 550.0000 | 900.0000 |
| `EHM_BQ1_VBat` | 3.4000 | 3.8000 |
| `EHM_BQ1_VBus` | 7.0000 | 9.0000 |
| `EHM_BQ2_IBat` | 900.0000 | 1200.0000 |
| `EHM_BQ2_IBus` | 350.0000 | 700.0000 |
| `EHM_BQ2_VAC1` | 7.0000 | 9.0000 |
| `EHM_BQ2_VAC2` | 7.0000 | 9.0000 |
| `EHM_BQ2_VBat` | 3.4000 | 3.8000 |
| `EHM_BQ2_VBus` | 7.0000 | 9.0000 |
| `EHM_ImuAccId` | 0.0000 | 500.0000 |
| `EHM_ImuAccX` | -0.2000 | 0.0000 |
| `EHM_ImuAccY` | -1.1000 | -0.9000 |
| `EHM_ImuAccZ` | -0.1000 | 0.1000 |
| `EHM_ImuGyroId` | 0.0000 | 500.0000 |
| `EHM_ImuGyroX` | -4.0000 | 3.0000 |
| `EHM_ImuGyroY` | -2.0000 | 1.0000 |
| `EHM_ImuGyroZ` | -4.0000 | 4.0000 |
| `EHM_ImuSqrt` | 0.9000 | 1.1000 |
| `EHM_PCB_ID` | 4.0000 | 4.0000 |
| `EHM_PPVAR_Recovery` | 7.0000 | 9.0000 |
| `EHM_Recovery` | 1.0000 | 1.0000 |
| `EHM_Recovery_RVP` | 7.0000 | 9.0000 |
| `HCT_BQ1_IBat` | 1200.0000 | 1600.0000 |
| `HCT_BQ1_IBus` | 550.0000 | 900.0000 |
| `HCT_BQ1_VBat` | 3.4000 | 3.8000 |
| `HCT_BQ1_VBus` | 7.0000 | 9.0000 |
| `HCT_BQ2_IBat` | 900.0000 | 1200.0000 |
| `HCT_BQ2_IBus` | 200.0000 | 500.0000 |
| `HCT_BQ2_VAC1` | 11.0000 | 12.5000 |
| `HCT_BQ2_VAC2` | 11.5000 | 12.5000 |
| `HCT_BQ2_VBat` | 3.4000 | 3.8500 |
| `HCT_BQ2_VBus` | 11.0000 | 12.5000 |
| `HCT_Power` | 41.5000 | 42.5000 |
| `MCU_TO_T2P_UART_RXD_5V_CONN_H` | 1.0000 | 1.0000 |
| `MCU_TO_T2P_UART_RXD_5V_CONN_L` | 0.0000 | 0.0000 |
| `MCU_TO_T2P_UART_TXD_5V_CONN_H` | 4.7400 | 5.1700 |
| `MCU_TO_T2P_UART_TXD_5V_CONN_L` | 0.0000 | 0.2000 |
| `PPVAR_VCU_CONN_Voltage_Recovery_Input` | 7.0000 | 9.0000 |
| `PPVAR_VCU_HCT` | 11.0000 | 12.5000 |
| `PPVAR_VCU_LOCK_CONN_Voltage_Recovery_Input` | 7.0000 | 9.0000 |
| `PPVAR_VCU_OTG` | 10.8000 | 11.6000 |
| `PPVAR_VCU_Solar` | 0.0000 | 0.2000 |
| `Recovery_Power_Apply` | 8.5000 | 9.5000 |
| `Solar_BQ1_IBat` | 1200.0000 | 1600.0000 |
| `Solar_BQ1_IBus` | 600.0000 | 900.0000 |
| `Solar_BQ1_VAC1` | 0.0000 | 0.5000 |
| `Solar_BQ1_VAC2` | 6.5000 | 8.5000 |
| `Solar_BQ1_VBat` | 3.4000 | 3.8500 |
| `Solar_BQ1_VBus` | 6.5000 | 8.5000 |
| `Solar_Power` | 7.5000 | 8.5000 |
| `T2P_Disabled` | 0.0000 | 0.2000 |
| `T2P_Enabled` | 4.7400 | 5.1700 |

</details>

---
*报告由规格限对比工具自动生成 — 2026-07-02 17:54:25*
