# 📊 规格限对比报告

## 基本信息

| 项目 | 值 |
|------|-----|
| CSV 文件 | `20260702105307_PASS_FV2615MEHP2NC0222_Metro_EHM_BFT_301.csv` |
| 项目 ID | `ehm_pcba_test` |
| 对比时间 | 2026-07-02 14:57:18 |

---

## 统计概要

| 统计项 | 数量 |
|--------|------|
| CSV 中测试项总数 | 154 |
| YAML 中测试项总数 | 152 |
| ✅ 完全匹配 | 151 |
| ❌ 存在差异 | 1 |
| ⚠️ 仅在 CSV 中 | 2 |
| ⚠️ 仅在 YAML 中 | 0 |

---

## ❌ 存在差异的测试项 (1 项) - 需要关注!

| TEST_NAME | CSV LSL | YAML LSL | LSL 匹配 | CSV USL | YAML USL | USL 匹配 |
|-----------|---------|----------|----------|---------|----------|----------|
| `LowPower_Mode_Current` | 0.0000 | 0.0020 | ❌ 不一致 | 0.0010 | 0.0040 | ❌ 不一致 |

---

## ⚠️ 仅在 CSV 文件中的测试项 (2 项) - YAML 配置缺失

| TEST_NAME | CSV LSL | CSV USL |
|-----------|---------|---------|
| `HW_Version` | 4.0000 | 4.0000 |
| `SPI_Flash_ID` | 239.0000 | 239.0000 |

---

## ✅ 完全匹配的测试项 (151 项)

<details>
<summary>点击展开完整列表</summary>

| TEST_NAME | LSL | USL |
|-----------|-----|-----|
| `ACC_SQRT` | 0.9000 | 1.1000 |
| `AccX` | -0.2000 | 0.2000 |
| `AccY` | -0.2000 | 0.2000 |
| `AccZ` | -1.1000 | -0.9000 |
| `Battery_Current_Dynamo15mph_NTC_Normal` | -0.5000 | 0.2000 |
| `Battery_Current_Dynamo15mph_NTC_Normal_NoLoad` | 0.0000 | 0.1000 |
| `Battery_Current_Dynamo40mph_NTC_Normal_NoLoad` | 0.0000 | 0.1000 |
| `Battery_Current_Dynamo5mph_NTC_Normal` | -0.1500 | 0.1000 |
| `Battery_Current_HCT_NTC_Hot` | 0.0000 | 0.0800 |
| `Battery_Current_HCT_NTC_Normal` | -1.2000 | -0.9000 |
| `Battery_Current_RP12V_NTC_Cold` | 0.0000 | 0.0050 |
| `Battery_Current_RP12V_NTC_Hot` | 0.0000 | 0.0050 |
| `Battery_Current_RP12V_NTC_Normal` | -1.6000 | -1.2000 |
| `Battery_Current_SolarHighCurrent_NTC_Normal` | -1.6000 | -0.9000 |
| `Battery_Current_SolarLowCurrent_NTC_Normal` | -0.4500 | -0.1000 |
| `Battery_Current_VCU_NTC_Normal` | -1.2000 | -0.9000 |
| `Battery_Simulator_3V5` | 3.4500 | 3.5500 |
| `CableLockConn_ELoad_Voltage` | 10.0000 | 11.5000 |
| `CableLock_Voltage` | 10.5000 | 11.5000 |
| `Charger_Difference` | -0.1000 | 0.1000 |
| `DUT_BQ1_VBat` | 3.4000 | 3.6000 |
| `DUT_BQ2_VBat` | 3.4000 | 3.6000 |
| `Dynamo_15mph_Doubler_NoLoad` | 13.0000 | 17.0000 |
| `Dynamo_15mph_Doubler_Voltage` | 12.0000 | 16.5000 |
| `Dynamo_15mph_Speed_Pulse_Sense` | 1000.0000 | 2000.0000 |
| `Dynamo_40mph_Doubler_Voltage` | 35.0000 | 42.0000 |
| `Dynamo_40mph_Doubler_ZenerD504_Temp` | 10.0000 | 45.0000 |
| `Dynamo_40mph_Doubler_ZenerD505_Temp` | 10.0000 | 45.0000 |
| `Dynamo_5mph_Doubler_Voltage` | 8.0000 | 10.5000 |
| `Dynamo_Simulator` | 3.5000 | 4.5000 |
| `Dynamo_Simulator_15mph` | 5.7500 | 6.2500 |
| `Dynamo_Simulator_40mph` | 13.5000 | 14.5000 |
| `Fake_Wheel_Power_4Hz` | 4.7500 | 5.2500 |
| `GyroX` | -3.0000 | 3.0000 |
| `GyroY` | -3.0000 | 2.0000 |
| `GyroZ` | -1.5000 | 2.0000 |
| `HCT_DET_State` | 1.0000 | 1.0000 |
| `HCT_Power` | 41.5000 | 42.5000 |
| `HCT_Power_Detect_State` | 0.0000 | 0.0000 |
| `IBAT1_NTC_Cold_RP` | 0.0000 | 100.0000 |
| `IBAT1_NTC_Hot_RP` | 0.0000 | 100.0000 |
| `IBAT1_NTC_Normal_RP` | 1200.0000 | 1600.0000 |
| `IBAT1_NTC_Normal_SolarHighCurrent` | 900.0000 | 1600.0000 |
| `IBAT1_NTC_Normal_SolarLowCurrent` | 200.0000 | 450.0000 |
| `IBAT2_NTC_Hot_RP` | 0.0000 | 100.0000 |
| `IBAT2_NTC_Normal_Dynamo15mph` | 50.0000 | 500.0000 |
| `IBAT2_NTC_Normal_Dynamo15mph_NoLoad` | 0.0000 | 100.0000 |
| `IBAT2_NTC_Normal_Dynamo40mph_NoLoad` | 0.0000 | 100.0000 |
| `IBAT2_NTC_Normal_Dynamo5mph` | -100.0000 | 150.0000 |
| `IBAT2_NTC_Normal_HCT` | 900.0000 | 1200.0000 |
| `IBAT2_NTC_Normal_OTG` | -1500.0000 | -900.0000 |
| `IBAT2_NTC_Normal_RP` | 0.0000 | 100.0000 |
| `IBAT2_NTC_Normal_VCU` | 900.0000 | 1200.0000 |
| `IBUS1_NTC_Cold_RP` | 0.0000 | 200.0000 |
| `IBUS1_NTC_Hot_RP` | 0.0000 | 200.0000 |
| `IBUS1_NTC_Normal_RP` | 450.0000 | 650.0000 |
| `IBUS1_NTC_Normal_SolarHighCurrent` | 500.0000 | 900.0000 |
| `IBUS1_NTC_Normal_SolarLowCurrent` | 150.0000 | 300.0000 |
| `IBUS2_NTC_Hot_RP` | 0.0000 | 200.0000 |
| `IBUS2_NTC_Normal_Dynamo15mph` | 10.0000 | 300.0000 |
| `IBUS2_NTC_Normal_Dynamo15mph_NoLoad` | -75.0000 | 200.0000 |
| `IBUS2_NTC_Normal_Dynamo40mph_NoLoad` | 0.0000 | 200.0000 |
| `IBUS2_NTC_Normal_Dynamo5mph` | 0.0000 | 200.0000 |
| `IBUS2_NTC_Normal_HCT` | 240.0000 | 500.0000 |
| `IBUS2_NTC_Normal_OTG` | -500.0000 | -200.0000 |
| `IBUS2_NTC_Normal_RP` | 0.0000 | 200.0000 |
| `IBUS2_NTC_Normal_VCU` | 250.0000 | 500.0000 |
| `IMMOB_TO_MCU_HALL_5V_IN_HIGH` | 1.0000 | 1.0000 |
| `IMMOB_TO_MCU_HALL_5V_IN_LOW` | 0.0000 | 0.0000 |
| `MCU_BI_IMMOB_IO2_5V_OUT_HIGH_PA7` | 0.0000 | 0.0000 |
| `MCU_BI_IMMOB_IO2_5V_OUT_HIGH_Volt` | 4.7400 | 5.1700 |
| `MCU_BI_IMMOB_IO2_5V_OUT_LOW_PA7` | 1.0000 | 1.0000 |
| `MCU_BI_IMMOB_IO2_5V_OUT_LOW_Volt` | 0.0000 | 0.2000 |
| `MCU_BI_IMMOB_IO2_IN_HIGH_PA7` | 0.0000 | 0.0000 |
| `MCU_BI_IMMOB_IO2_IN_HIGH_PC4` | 1.0000 | 1.0000 |
| `MCU_BI_IMMOB_IO2_IN_LOW_PA7` | 1.0000 | 1.0000 |
| `MCU_BI_IMMOB_IO2_IN_LOW_PC4` | 0.0000 | 0.0000 |
| `MCU_TO_T2P_UART_TXD_5V_OUT_HIGH` | 4.7400 | 5.1700 |
| `MCU_TO_T2P_UART_TXD_5V_OUT_LOW` | 0.0000 | 0.2000 |
| `Motor_Direction1_Current` | 0.2900 | 0.3500 |
| `Motor_Direction1_Voltage` | 4.6000 | 5.0000 |
| `Motor_Direction2_Current` | 0.2900 | 0.3500 |
| `Motor_Direction2_Halted_Current` | -0.0030 | 0.0030 |
| `Motor_Direction2_Halted_Voltage` | -0.2000 | 0.2000 |
| `Motor_Direction2_Voltage` | -5.0000 | -4.6000 |
| `PP12V0_RECOVERY_RVP_ADCRead_RP_Input` | 10.5000 | 12.0000 |
| `PP3V3_SYSTEM` | 3.2000 | 3.4500 |
| `PP4V2_VSYS_DYNAMO` | 4.1000 | 4.3000 |
| `PP4V2_VSYS_MUX` | 4.1000 | 4.3000 |
| `PP4V2_VSYS_SOLAR` | 4.1000 | 4.3000 |
| `PP5V0_BOOST` | 4.7400 | 5.1700 |
| `PP5V0_IMMOB_1000mA_Load_OverCurrent_Volt` | 0.0000 | 0.1000 |
| `PP5V0_IMMOB_500mA_Load_Current` | 0.4900 | 0.5100 |
| `PP5V0_IMMOB_500mA_Load_Voltage` | 4.7400 | 5.1700 |
| `PP5V0_IMMOB_Disabled` | 0.0000 | 0.2000 |
| `PP5V0_IMMOB_Enabled` | 4.7400 | 5.1700 |
| `PP5V0_IMMOB_Voltage_ELoad_Disabled` | 0.0000 | 0.1000 |
| `PP5V0_T2P_1000mA_Load_OverCurrent_Volt` | 0.0000 | 0.1000 |
| `PP5V0_T2P_500mA_Load_Current` | 0.4900 | 0.5100 |
| `PP5V0_T2P_500mA_Load_Voltage` | 4.7400 | 5.1700 |
| `PP5V0_T2P_Disabled` | 0.0000 | 0.2000 |
| `PP5V0_T2P_Enabled` | 4.7400 | 5.1700 |
| `PP5V0_T2P_Voltage_ELoad_Disabled` | 0.0000 | 0.1000 |
| `PPVAR_VCU_Backup_Voltage_OTG_Disabled` | 10.5000 | 11.5000 |
| `PPVAR_VCU_CONN_ADCRead_HCT_Input` | 11.5000 | 12.5000 |
| `PPVAR_VCU_CONN_ADCRead_RP_Input` | 10.5000 | 12.0000 |
| `PPVAR_VCU_CONN_ADCRead_RP_NoInput` | 0.0000 | 0.2000 |
| `PPVAR_VCU_CONN_Power_Input` | 11.8000 | 12.2000 |
| `PPVAR_VCU_Voltage_Read` | 11.0000 | 12.5000 |
| `Recovery_Port_Input_Detect` | 1.0000 | 1.0000 |
| `Recovery_Port_NoInput_Detect` | 0.0000 | 0.0000 |
| `Recovery_Power_Apply` | 11.5000 | 12.5000 |
| `Solar_Power` | 7.7500 | 8.2500 |
| `Solar_Power_Apply_HighCurrent` | 7.7500 | 8.2500 |
| `T2P_TO_MCU_UART_RXD_5V_IN_HIGH` | 1.0000 | 1.0000 |
| `T2P_TO_MCU_UART_RXD_5V_IN_HIGH2` | 4.7400 | 5.1700 |
| `T2P_TO_MCU_UART_RXD_5V_IN_LOW` | 0.0000 | 0.0000 |
| `T2P_TO_MCU_UART_RXD_5V_IN_LOW2` | 0.0000 | 0.2000 |
| `TailLight_Disabled_Out_Current` | 0.0000 | 0.0020 |
| `TailLight_Disabled_Out_Voltage` | 0.0000 | 0.6000 |
| `TailLight_Enabled_Out_Current` | 0.0000 | 0.1000 |
| `TailLight_Enabled_Out_Voltage` | 10.0000 | 11.5000 |
| `TailLight_OTG_Verify` | 10.0000 | 11.5000 |
| `VBAT1_NTC_Cold_RP` | 3.4500 | 3.5500 |
| `VBAT1_NTC_Hot_RP` | 3.4500 | 3.5500 |
| `VBAT1_NTC_Normal_RP` | 3.7500 | 3.9500 |
| `VBAT1_NTC_Normal_SolarHighCurrent` | 3.7000 | 4.0000 |
| `VBAT1_NTC_Normal_SolarLowCurrent` | 3.5000 | 3.6500 |
| `VBAT2_NTC_Hot_RP` | 3.4500 | 3.5500 |
| `VBAT2_NTC_Normal_Dynamo15mph` | 3.4000 | 3.6500 |
| `VBAT2_NTC_Normal_Dynamo15mph_NoLoad` | 3.4500 | 3.5500 |
| `VBAT2_NTC_Normal_Dynamo40mph_NoLoad` | 3.4500 | 3.5500 |
| `VBAT2_NTC_Normal_Dynamo5mph` | 3.4000 | 3.6500 |
| `VBAT2_NTC_Normal_HCT` | 3.7000 | 3.8500 |
| `VBAT2_NTC_Normal_RP` | 3.7500 | 3.9500 |
| `VBAT2_NTC_Normal_VCU` | 3.6000 | 3.9000 |
| `VBATT_Current_IDLE` | 0.0380 | 0.0500 |
| `VBATT_ON_4V2` | 4.1000 | 4.3000 |
| `VBUS1_NTC_Cold_RP` | 11.5000 | 12.5000 |
| `VBUS1_NTC_Hot_RP` | 11.5000 | 12.5000 |
| `VBUS1_NTC_Normal_RP` | 10.5000 | 12.0000 |
| `VBUS1_NTC_Normal_SolarHighCurrent` | 6.0000 | 8.0000 |
| `VBUS1_NTC_Normal_SolarLowCurrent` | 6.0000 | 8.0000 |
| `VBUS2_NTC_Hot_RP` | 11.5000 | 12.5000 |
| `VBUS2_NTC_Normal_Dynamo15mph` | 9.5000 | 11.5000 |
| `VBUS2_NTC_Normal_Dynamo15mph_NoLoad` | 11.5000 | 12.5000 |
| `VBUS2_NTC_Normal_Dynamo40mph_NoLoad` | 11.5000 | 12.5000 |
| `VBUS2_NTC_Normal_Dynamo5mph` | 5.0000 | 10.5000 |
| `VBUS2_NTC_Normal_HCT` | 11.5000 | 12.5000 |
| `VBUS2_NTC_Normal_RP` | 10.5000 | 12.0000 |
| `VBUS2_NTC_Normal_VCU` | 11.0000 | 12.5000 |

</details>

---
*报告由规格限对比工具自动生成 — 2026-07-02 14:57:18*
