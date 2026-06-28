# -*- encoding: utf-8 -*-
"""
@File    :   spc_config.py
@Time    :   2026/06/17
@Author  :   SimonYuan
@Version :   1.0
@Desc    :   SPC分析配置文件 - 在此定义测试项目和规格限

使用说明:
1. 在 spec_limits 字典中添加/修改测试项目和规格限
2. 格式: "测试项目名称": (LSL下限, USL上限)
3. 运行主程序: python spc_analysis.py
"""

# ===============================================
# EHM PCBA test summary file and limits config
# ===============================================
# CSV_FILE_PATH = "./Metro_EHM_BFT_301_summary_sort_20260617_223411.csv"

# OUTPUT_HTML = "ehm_pcba_test_after_improved_upper_plate.html"
# OUTPUT_PDF = "ehm_pcba_test_after_improved_upper_plate.pdf"
# OUTPUT_IMG_DIR = "ehm_pcba_test_after_improved_upper_plate"

# # fmt: off
# SPEC_LIMITS = {
#     "VBATT_ON_4V2"                                 : (4.1, 4.3),
#     "PP4V2_VSYS_DYNAMO"                            : (4.1, 4.3),
#     "PP4V2_VSYS_SOLAR"                             : (4.1, 4.3),
#     "PP4V2_VSYS_MUX"                               : (4.1, 4.3),
#     "PP5V0_BOOST"                                  : (4.74, 5.17),
#     "PP3V3_SYSTEM"                                 : (3.2, 3.45),
#     "DUT_BQ1_VBat"                                 : (3.4, 3.6),
#     "DUT_BQ2_VBat"                                 : (3.4, 3.6),
#     "Charger_Difference"                           : (-0.1, 0.1),
#     "VBATT_Current_IDLE"                           : (0.038, 0.05),
#     "AccX"                                         : (-0.01, 0.032),
#     "AccY"                                         : (-0.01, 0.04),
#     "AccZ"                                         : (-1.1, -0.9),
#     "ACC_SQRT"                                     : (0.9, 1.1),
#     "GyroX"                                        : (-1.2, 1.2),
#     "GyroY"                                        : (-3, 2),
#     "GyroZ"                                        : (-1.4, 1.4),
#     "PP5V0_T2P_Disabled"                           : (0, 0.2),
#     "PP5V0_T2P_Enabled"                            : (4.74, 5.17),
#     "MCU_TO_T2P_UART_TXD_5V_OUT_HIGH"              : (4.74, 5.17),
#     "MCU_TO_T2P_UART_TXD_5V_OUT_LOW"               : (0, 0.2),
#     "T2P_TO_MCU_UART_RXD_5V_IN_HIGH"               : (1, 1),
#     "T2P_TO_MCU_UART_RXD_5V_IN_HIGH2"              : (4.74, 5.17),
#     "T2P_TO_MCU_UART_RXD_5V_IN_LOW"                : (0, 0),
#     "T2P_TO_MCU_UART_RXD_5V_IN_LOW2"               : (0, 0.2),
#     "PP5V0_T2P_500mA_Load_Voltage"                 : (4.74, 5.17),
#     "PP5V0_T2P_500mA_Load_Current"                 : (0.49, 0.51),
#     "PP5V0_T2P_1000mA_Load_OverCurrent_Volt"       : (0, 0.1),
#     "PP5V0_T2P_Voltage_ELoad_Disabled"             : (0, 0.1),
#     "PP5V0_IMMOB_Disabled"                         : (0, 0.2),
#     "PP5V0_IMMOB_Enabled"                          : (4.74, 5.17),
#     "PP5V0_IMMOB_500mA_Load_Voltage"               : (4.74, 5.17),
#     "PP5V0_IMMOB_500mA_Load_Current"               : (0.49, 0.51),
#     "PP5V0_IMMOB_1000mA_Load_OverCurrent_Volt"     : (0, 0.1),
#     "PP5V0_IMMOB_Voltage_ELoad_Disabled"           : (0, 0.1),
#     "IMMOB_TO_MCU_HALL_5V_IN_HIGH"                 : (1, 1),
#     "IMMOB_TO_MCU_HALL_5V_IN_LOW"                  : (0, 0),
#     "MCU_BI_IMMOB_IO2_5V_OUT_HIGH_PA7"             : (0, 0),
#     "MCU_BI_IMMOB_IO2_5V_OUT_HIGH_Volt"            : (4.74, 5.17),
#     "MCU_BI_IMMOB_IO2_5V_OUT_LOW_PA7"              : (1, 1),
#     "MCU_BI_IMMOB_IO2_5V_OUT_LOW_Volt"             : (0, 0.2),
#     "MCU_BI_IMMOB_IO2_IN_HIGH_PA7"                 : (0, 0),
#     "MCU_BI_IMMOB_IO2_IN_HIGH_PC4"                 : (1, 1),
#     "MCU_BI_IMMOB_IO2_IN_LOW_PA7"                  : (1, 1),
#     "MCU_BI_IMMOB_IO2_IN_LOW_PC4"                  : (0, 0),
#     "Motor_Direction1_Voltage"                     : (4.6, 5.0),
#     "Motor_Direction1_Current"                     : (0.29, 0.35),
#     "Motor_Direction2_Voltage"                     : (-5.0, -4.6),
#     "Motor_Direction2_Current"                     : (0.29, 0.35),
#     "Fake_Wheel_Power_4Hz"                         : (4.75, 5.25),
#     "Motor_Direction2_Halted_Voltage"              : (-0.2, 0.2),
#     "Motor_Direction2_Halted_Current"              : (-0.002, 0.002),
#     "Battery_Simulator_3V5"                        : (3.45, 3.55),
#     "Recovery_Port_NoInput_Detect"                 : (0, 0.2),
#     "PPVAR_VCU_CONN_ADCRead_RP_NoInput"            : (0, 0.2),
#     "Recovery_Power_Apply"                         : (11.5, 12.5),
#     "Recovery_Port_Input_Detect"                   : (1, 1),
#     "PPVAR_VCU_CONN_ADCRead_RP_Input"              : (10.5, 12),
#     "PP12V0_RECOVERY_RVP_ADCRead_RP_Input"         : (10.5, 12),
#     "VBUS1_NTC_Normal_RP"                          : (10.5, 12),
#     "VBAT1_NTC_Normal_RP"                          : (3.75, 3.95),
#     "IBUS1_NTC_Normal_RP"                          : (450, 650),
#     "IBAT1_NTC_Normal_RP"                          : (1200, 1600),
#     "VBUS2_NTC_Normal_RP"                          : (10.5, 12),
#     "VBAT2_NTC_Normal_RP"                          : (3.75, 3.95),
#     "IBUS2_NTC_Normal_RP"                          : (-20, 80),
#     "IBAT2_NTC_Normal_RP"                          : (0, 100),
#     "Battery_Current_RP12V_NTC_Normal"             : (-1.6, -1.2),
#     "VBUS1_NTC_Cold_RP"                            : (11.5, 12.5),
#     "VBAT1_NTC_Cold_RP"                            : (3.45, 3.55),
#     "IBUS1_NTC_Cold_RP"                            : (0, 100),
#     "IBAT1_NTC_Cold_RP"                            : (0, 100),
#     "Battery_Current_RP12V_NTC_Cold"               : (0, 0.005),
#     "VBUS1_NTC_Hot_RP"                             : (11.5, 12.5),
#     "VBAT1_NTC_Hot_RP"                             : (3.45, 3.55),
#     "IBUS1_NTC_Hot_RP"                             : (0, 100),
#     "IBAT1_NTC_Hot_RP"                             : (0, 100),
#     "Battery_Current_RP12V_NTC_Hot"                : (0, 0.005),
#     "HCT_DET_State"                                : (1, 1),
#     "HCT_Power"                                    : (41.5, 42.5),
#     "HCT_Power_Detect_State"                       : (0, 0),
#     "PPVAR_VCU_CONN_ADCRead_HCT_Input"             : (11.5, 12.5),
#     "VBUS2_NTC_Normal_HCT"                         : (11.5, 12.5),
#     "VBAT2_NTC_Normal_HCT"                         : (3.7, 3.85),
#     "IBUS2_NTC_Normal_HCT"                         : (300, 450),
#     "IBAT2_NTC_Normal_HCT"                         : (900, 1200),
#     "Battery_Current_HCT_NTC_Normal"               : (-1.2, -0.9),
#     "VBUS2_NTC_Hot_RP"                             : (11.5, 12.5),
#     "VBAT2_NTC_Hot_RP"                             : (3.45, 3.55),
#     "IBUS2_NTC_Hot_RP"                             : (-20, 90),
#     "IBAT2_NTC_Hot_RP"                             : (0, 100),
#     "Battery_Current_HCT_NTC_Hot"                  : (0, 0.08),
#     "Solar_Power"                                  : (7.75, 8.25),
#     "VBUS1_NTC_Normal_SolarLowCurrent"             : (6, 8),
#     "VBAT1_NTC_Normal_SolarLowCurrent"             : (3.5, 3.65),
#     "IBUS1_NTC_Normal_SolarLowCurrent"             : (150, 300),
#     "IBAT1_NTC_Normal_SolarLowCurrent"             : (200, 450),
#     "Battery_Current_SolarLowCurrent_NTC_Normal"   : (-0.45, -0.2),
#     "Solar_Power_Apply_HighCurrent"                : (7.75, 8.25),
#     "VBUS1_NTC_Normal_SolarHighCurrent"            : (6, 8),
#     "VBAT1_NTC_Normal_SolarHighCurrent"            : (3.7, 4),
#     "IBUS1_NTC_Normal_SolarHighCurrent"            : (500, 900),
#     "IBAT1_NTC_Normal_SolarHighCurrent"            : (900, 1600),
#     "Battery_Current_SolarHighCurrent_NTC_Normal"  : (-1.6, -0.9),
#     "Dynamo_Simulator"                             : (3.5, 4.5),
#     "Dynamo_5mph_Doubler_Voltage"                  : (8, 10.5),
#     "VBUS2_NTC_Normal_Dynamo5mph"                  : (5, 10.5),
#     "VBAT2_NTC_Normal_Dynamo5mph"                  : (3.4, 3.65),
#     "IBUS2_NTC_Normal_Dynamo5mph"                  : (0, 150),
#     "IBAT2_NTC_Normal_Dynamo5mph"                  : (-100, 150),
#     "Battery_Current_Dynamo5mph_NTC_Normal"        : (-0.15, 0.1),
#     "Dynamo_Simulator_15mph"                       : (5.75, 6.25),
#     "Dynamo_15mph_Doubler_Voltage"                 : (12, 16.5),
#     "Dynamo_15mph_Speed_Pulse_Sense"               : (1500, 2500),
#     "VBUS2_NTC_Normal_Dynamo15mph"                 : (9.5, 11.5),
#     "VBAT2_NTC_Normal_Dynamo15mph"                 : (3.4, 3.65),
#     "IBUS2_NTC_Normal_Dynamo15mph"                 : (50, 200),
#     "IBAT2_NTC_Normal_Dynamo15mph"                 : (50, 500),
#     "Battery_Current_Dynamo15mph_NTC_Normal"       : (-0.5, 0.2),
#     "Dynamo_15mph_Doubler_NoLoad"                  : (13, 17),
#     "VBUS2_NTC_Normal_Dynamo15mph_NoLoad"          : (11.5, 12.5),
#     "VBAT2_NTC_Normal_Dynamo15mph_NoLoad"          : (3.45, 3.55),
#     "IBUS2_NTC_Normal_Dynamo15mph_NoLoad"          : (-75, 200),
#     "IBAT2_NTC_Normal_Dynamo15mph_NoLoad"          : (0, 100),
#     "Battery_Current_Dynamo15mph_NTC_Normal_NoLoad": (0, 0.1),
#     "Dynamo_Simulator_40mph"                       : (13.5, 14.5),
#     "Dynamo_40mph_Doubler_Voltage"                 : (35, 42),
#     "Dynamo_40mph_Doubler_ZenerD504_Temp"          : (10, 45),
#     "Dynamo_40mph_Doubler_ZenerD505_Temp"          : (10, 45),
#     "VBUS2_NTC_Normal_Dynamo40mph_NoLoad"          : (11.5, 12.5),
#     "VBAT2_NTC_Normal_Dynamo40mph_NoLoad"          : (3.45, 3.55),
#     "IBUS2_NTC_Normal_Dynamo40mph_NoLoad"          : (-20, 80),
#     "IBAT2_NTC_Normal_Dynamo40mph_NoLoad"          : (0, 100),
#     "Battery_Current_Dynamo40mph_NTC_Normal_NoLoad": (0, 0.1),
#     "PPVAR_VCU_CONN_Power_Input"                   : (11.8, 12.2),
#     "PPVAR_VCU_Voltage_Read"                       : (11, 12.5),
#     "VBUS2_NTC_Normal_VCU"                         : (11, 12.5),
#     "VBAT2_NTC_Normal_VCU"                         : (3.6, 3.9),
#     "IBUS2_NTC_Normal_VCU"                         : (250, 500),
#     "IBAT2_NTC_Normal_VCU"                         : (900, 1200),
#     "Battery_Current_VCU_NTC_Normal"               : (-1.2, -0.9),
#     "PPVAR_VCU_Backup_Voltage_OTG_Disabled"        : (10.5, 11.5),
#     "CableLock_Voltage"                            : (10.5, 11.5),
#     "CableLockConn_ELoad_Voltage"                  : (10, 11.5),
#     "IBAT2_NTC_Normal_OTG"                         : (-1500, -900),
#     "IBUS2_NTC_Normal_OTG"                         : (-500, -200),
#     "TailLight_OTG_Verify"                         : (10, 11.5),
#     "TailLight_Enabled_Out_Voltage"                : (10, 11.5),
#     "TailLight_Enabled_Out_Current"                : (0, 0.1),
#     "TailLight_Disabled_Out_Voltage"               : (0, 0.6),
#     "TailLight_Disabled_Out_Current"               : (0, 0.002),
#     "LowPower_Mode_Current"                        : (0.002, 0.004),
# }
# fmt: on

# ===============================================
# EHM module test summary file and limits config
# ===============================================
CSV_FILE_PATH = "./Metro_EHM_Module_302_summary_sort_20260623_144334.csv"

OUTPUT_HTML = "ehm_module_test_after_cycle_time_optimized.html"
OUTPUT_PDF = "ehm_module_test_after_cycle_time_optimized.pdf"
OUTPUT_IMG_DIR = "ehm_module_test_after_cycle_time_optimized"

# fmt: off
SPEC_LIMITS = {
    "EHM_PCB_ID"                                : (3, 3),
    "EHM_ImuAccId"                              : (0, 500),
    "EHM_ImuAccX"                               : (-0.2, 0),
    "EHM_ImuAccY"                               : (-1.1, -0.9),
    "EHM_ImuAccZ"                               : (-0.1, 0.1),
    "EHM_ImuSqrt"                               : (0.9, 1.1),
    "EHM_ImuGyroId"                             : (0, 500),
    "EHM_ImuGyroX"                              : (-4, 3),
    "EHM_ImuGyroY"                              : (-2, 1),
    "EHM_ImuGyroZ"                              : (-4, 4),
    "T2P_Disabled"                              : (0, 0.2),
    "T2P_Enabled"                               : (4.74, 5.17),
    "MCU_TO_T2P_UART_TXD_5V_CONN_H"             : (4.74, 5.17),
    "MCU_TO_T2P_UART_TXD_5V_CONN_L"             : (0, 0.2),
    "MCU_TO_T2P_UART_RXD_5V_CONN_H"             : (1, 1),
    "MCU_TO_T2P_UART_RXD_5V_CONN_L"             : (0, 0),
    "PPVAR_VCU_OTG"                             : (10.8, 11.6),
    "Recovery_Power_Apply"                      : (8.5, 9.5),
    "EHM_Recovery"                              : (1, 1),
    "EHM_Recovery_RVP"                          : (7, 9),
    "EHM_PPVAR_Recovery"                        : (7, 9),
    "EHM_BQ1_VBus"                              : (7, 9),
    "EHM_BQ1_VBat"                              : (3.4, 3.8),
    "EHM_BQ1_IBus"                              : (550, 900),
    "EHM_BQ1_IBat"                              : (1200, 1600),
    "EHM_BQ2_VAC1"                              : (7, 9),
    "EHM_BQ2_VAC2"                              : (7, 9),
    "EHM_BQ2_VBus"                              : (7, 9),
    "EHM_BQ2_VBat"                              : (3.4, 3.8),
    "EHM_BQ2_IBus"                              : (350, 700),
    "EHM_BQ2_IBat"                              : (900, 1200),
    "PPVAR_VCU_CONN_Voltage_Recovery_Input"     : (7, 9),
    "Charger_Difference"                        : (-0.1, 0.1),
    "PPVAR_VCU_LOCK_CONN_Voltage_Recovery_Input": (7, 9),
    "HCT_Power"                                 : (41.5, 42.5),
    "HCT_BQ2_VAC1"                              : (11, 12.5),
    "PPVAR_VCU_HCT"                             : (11, 12.5),
    "HCT_BQ1_VBus"                              : (7, 9),
    "HCT_BQ1_VBat"                              : (3.4, 3.8),
    "HCT_BQ1_IBus"                              : (550, 900),
    "HCT_BQ1_IBat"                              : (1200, 1600),
    "HCT_BQ2_VBus"                              : (11, 12.5),
    "HCT_BQ2_VBat"                              : (3.4, 3.85),
    "HCT_BQ2_VAC1.1"                             : (11.5, 12.5),
    "HCT_BQ2_VAC2"                              : (11.5, 12.5),
    "HCT_BQ2_IBus"                              : (200, 500),
    "HCT_BQ2_IBat"                              : (900, 1200),
    "Solar_Power"                               : (7.5, 8.5),
    "Solar_BQ1_VAC1"                            : (0, 0.5),
    "Solar_BQ1_VAC2"                            : (6.5, 8.5),
    "PPVAR_VCU_Solar"                           : (0, 0.2),
    "Solar_BQ1_VBus"                            : (6.5, 8.5),
    "Solar_BQ1_VBat"                            : (3.4, 3.85),
    "Solar_BQ1_IBus"                            : (600, 900),
    "Solar_BQ1_IBat"                            : (1200, 1600),
    "Dynamo_Simulator"                          : (3.5, 4.5),
    "Dynamo_Doubler_Voltage_5mph"               : (6.5, 10),
    "Dynamo5mph_BQ2_VAC1"                       : (6, 10),
    "Dynamo5mph_BQ2_VAC2"                       : (6, 10),
    "Dynamo5mph_BQ2_VBus"                       : (6, 10),
    "Dynamo5mph_BQ2_VBat"                       : (3.4, 3.85),
    "Dynamo5mph_BQ2_IBus"                       : (10, 200),
    "Dynamo5mph_BQ2_IBat"                       : (-100, 300),
    "Dynamo_Simulator_15mph"                    : (5.5, 6.5),
    "Dynamo_Doubler_Voltage_15mph"              : (10.5, 12.5),
    "Dynamo_Speed_Sense"                        : (20, 40),
    "Dynamo15mph_BQ2_VBus"                      : (10, 11),
    "Dynamo15mph_BQ2_VBat"                      : (3.4, 3.85),
    "Dynamo15mph_BQ2_VAC1"                      : (10, 11),
    "Dynamo15mph_BQ2_VAC2"                      : (10, 11),
    "Dynamo15mph_BQ2_IBus"                      : (50, 300),
    "Dynamo15mph_BQ2_IBat"                      : (200, 300),
}
# fmt: on


# ===============================================
# FATP 932 test summary file and limits config
# ===============================================
CSV_FILE_PATH = "./Metro_Hybrid_FATP932_302_summary_sort_20260623_144334.csv"

OUTPUT_HTML = "Metro_Hybrid_FATP932.html"
OUTPUT_PDF = "Metro_Hybrid_FATP932.pdf"
OUTPUT_IMG_DIR = "Metro_Hybrid_FATP932"

# fmt: off
SPEC_LIMITS = {
    "EHM_Recovery"              : (1, 1),
    "ALS_Function"              : (3, 30),
    "GNSS_Function"             : (3, 9999),
    "PT_ImuAccId"               : (30, 500),
    "PT_ImuAccX"                : (-0.4, -0.3),
    "PT_ImuAccY"                : (0.35, 0.58),
    "PT_ImuAccZ"                : (-0.9, -0.7),
    "PT_ImuSqrt"                : (0.9, 1.1),
    "EHM_12V_RVP"               : (10, 12.5),
    "EHM_PPVAR_RP12V"           : (10, 12.5),
    "RP_BQ1_VAC1"               : (10, 12.5),
    "RP_BQ1_VAC2"               : (0, 5),
    "RP_BQ1_VBus"               : (10, 12.5),
    "RP_BQ1_VBAT"               : (3.2, 3.8),
    "RP_BQ1_IBAT"               : (1200, 1600),
    "RP_BQ2_VBAT_Compare"       : (3.2, 3.8),
    "Charger_Difference"        : (-0.1, 0.1),
    "BackupBattery_Charging_Off": (0, 50),
    "BackupBattery_Charging"    : (900, 1200),
    "RP_BQ2_VAC1"               : (10, 12.5),
    "RP_BQ2_VAC2"               : (10, 12.5),
    "RP_BQ2_VBus"               : (10, 12.5),
    "RP_BQ2_VBAT"               : (3.2, 3.8),
    "RP_BQ2_IBAT"               : (400, 1400),
    "EHM_HCT_IN"                : (10, 12.5),
    "EHM_Backup_Charging"       : (900, 1200),
    "EHM_Battery_BQ2"           : (0, 50),
    "Solar_BQ1_VAC1"            : (10, 12.5),
    "Solar_BQ1_VAC2"            : (6, 8.5),
    "Solar_BQ1_IBat"            : (1200, 1600),
    "EHM_ImuAccId"              : (0, 500),
    "EHM_ImuAccX"               : (0.9, 1.1),
    "EHM_ImuAccY"               : (-0.7, 0.52),
    "EHM_ImuAccZ"               : (-0.1, 0.1),
    "EHM_ImuSqrt"               : (0.9, 1.1),
    "EHM_ImuGyroId"             : (0, 500),
    "EHM_ImuGyroX"              : (-50, 50),
    "EHM_ImuGyroY"              : (-50, 50),
    "EHM_ImuGyroZ"              : (-50, 50),
}
# fmt: on


# ===============================================
# FATP 933 test summary file and limits config
# ===============================================
CSV_FILE_PATH = "./Metro_Hybrid_FATP932_302_summary_sort_20260623_144334.csv"

OUTPUT_HTML = "Metro_Hybrid_FATP933.html"
OUTPUT_PDF = "Metro_Hybrid_FATP933.pdf"
OUTPUT_IMG_DIR = "Metro_Hybrid_FATP933"

# fmt: off
SPEC_LIMITS = {
    "Motor_CalibratedUnlockPosition"   : (646, 1200),
    "Motor_CalibratedAutolockPosition" : (1159, 2152),
    "Motor_CalibratedSuperlockPosition": (2430, 4050),
    "CL_Pin_RawX"                      : (-9999, -5000),
    "CL_Pin_RawY"                      : (-9999, -9999),
    "CL_Pin_RawZ"                      : (-9999, -9999),
    "CL_Pin_CalibMinX"                 : (-9999, -9999),
    "CL_Pin_CalibMaxX"                 : (-9999, -9999),
    "CL_Pin_CalibMinY"                 : (-9999, -9999),
    "CL_Pin_CalibMaxY"                 : (-9999, -9999),
    "CL_Pin_CalibMinZ"                 : (-9999, -9999),
    "CL_Pin_CalibMaxZ"                 : (-9999, -9999),
    "CL_Pin_CalibTemp"                 : (20, 35),
    "CL_Pin_CalibConfigGain"           : (0, 0),
    "CL_Pin_CalibConfigResX"           : (0, 0),
    "CL_Pin_CalibConfigResY"           : (0, 0),
    "CL_Pin_CalibConfigResZ"           : (0, 0),
    "Holster_RawX"                     : (500, 3216),
    "CL_Holster_CalibMinX"             : (-9999, -9999),
    "CL_Holster_CalibMaxX"             : (-9999, -9999),
    "CL_Holster_CalibMinY"             : (-9999, -9999),
    "CL_Holster_CalibMaxY"             : (-9999, -9999),
    "CL_Holster_CalibMinZ"             : (-9999, -9999),
    "CL_Holster_CalibMaxZ"             : (-9999, -9999),
    "CL_Holster_CalibTemp"             : (20, 35),
    "CL_Holster_CalibConfigGain"       : (1, 1),
    "CL_Holster_CalibConfigResX"       : (0, 0),
    "CL_Holster_CalibConfigResY"       : (0, 0),
    "CL_Holster_CalibConfigResZ"       : (0, 0),
    "Brake_Front_Min"                  : (0.16, 0.222),
    "Brake_Front_Max"                  : (0.36, 0.55),
    "Brake_Rear_Min"                   : (0.16, 0.222),
    "Brake_Rear_Max"                   : (0.36, 0.55),
    "BrakeAdcDataFront_Max"            : (0, 1000),
    "BrakeAdcDataRear_Min"             : (0, 1000),
    "BrakeAdcDataFront_Min"            : (0, 1000),
    "BrakeAdcDataRear_Max"             : (0, 1000),
    "EHM_RP_Input"                     : (8.5, 9.5),
    "RP_BQ1_VBus"                      : (7.5, 8.5),
    "EHM_BQ1_VBat"                     : (3.2, 3.8),
    "EHM_BQ1_IBat"                     : (1200, 1600),
    "EHM_BQ2_VAC1"                     : (7.5, 8.5),
    "EHM_RP_Current"                   : (1.2, 1.8),
    "BackupBattery_Charging"           : (900, 1200),
    "Dynamo_Doubler_Voltage"           : (15, 35),
    "Dynamo_BQ2_VAC1"                  : (6.5, 12),
    "Dynamo_BQ2_VAC2"                  : (6.5, 12),
    "Dynamo_BQ2_VBus"                  : (6.5, 12),
    "Dynamo_BQ2_VBat"                  : (3.2, 3.8),
    "Dynamo_BQ2_IBat"                  : (250, 1200),
    "Dynamo_RP_Current"                : (0.5, 1),
    "IMMO_Lock_PreventLockCount"       : (0, 200),
}
# fmt: on

# ===============================================
# monolith solar left door test summary file and limits config
# ===============================================
CSV_FILE_PATH = "./Metro_Hybrid_FATP932_302_summary_sort_20260623_144334.csv"

OUTPUT_HTML = "Monolith_Solar_Left_Door.html"
OUTPUT_PDF = "Monolith_Solar_Left_Door.pdf"
OUTPUT_IMG_DIR = "Monolith_Solar_Left_Door"

# fmt: off
SPEC_LIMITS = {
    "Test_voltage": (6.902, 8.33),
    "Test_first_temp_1": (20, 30),
    "Test_first_temp_2": (20, 30),
    "Test_Current": (0.0945, 0.147),
    "Test_Count_Power": (0.652, 1.176),
    "Test_second_temp_1": (20, 30),
    "Test_second_temp_2": (20, 30),
}
# fmt: on

# ===============================================
# monolith solar right door test summary file and limits config
# ===============================================
CSV_FILE_PATH = "./Metro_Hybrid_FATP932_302_summary_sort_20260623_144334.csv"

OUTPUT_HTML = "Monolith_Solar_Right_Door.html"
OUTPUT_PDF = "Monolith_Solar_Right_Door.pdf"
OUTPUT_IMG_DIR = "Monolith_Solar_Right_Door"

# fmt: off
SPEC_LIMITS = {
    "Test_voltage": (6.902, 8.33),
    "Test_first_temp_1": (20, 30),
    "Test_first_temp_2": (20, 30),
    "Test_Current": (0.0945, 0.147),
    "Test_Count_Power": (0.652, 1.176),
    "Test_second_temp_1": (20, 30),
    "Test_second_temp_2": (20, 30),
}
# fmt: on


# ===============================================
# cosmo vcu101 test summary file and limits config
# ===============================================
CSV_FILE_PATH = "./Metro_Hybrid_FATP932_302_summary_sort_20260623_144334.csv"

OUTPUT_HTML = "Cosmo_VCU101_PCBA.html"
OUTPUT_PDF = "Cosmo_VCU101_PCBA.pdf"
OUTPUT_IMG_DIR = "Cosmo_VCU101_PCBA"

# fmt: off
SPEC_LIMITS = {
    "PP59V0_VEHICLE_CONN_Ohm"     : (3000, 10000),
    "PP14V8_VEHICLE_BOOST_OUT_Ohm": (3000, 10000),
    "PP3V3_SYSTEM_BUCK_Ohm"       : (10000, 500000),
    "PP12V0_VEHICLE_Ohm"          : (30000, 60000),
    "PP1V8_SYSTEM_LDO_Ohm"        : (15000, 35000),
    "PP5V0_BOOST_Ohm"             : (15000, 50000),
    "PP3V3_WIFI_Ohm"              : (10000, 500000),
    "PP1V8_EG21_VDD_EXT_Ohm"      : (10000, 50000),
    "PP4V2_BATT_VCC_Ohm"          : (1500, 10000),
    "PP14V8_VEHICLE_BOOST_OUT_V"  : (0, 0.1),
    "PP59V0_VEHICLE_IN_CONN_V"    : (14.7, 15.3),
    "PP12V0_VEHICLE_V"            : (11.56, 12.04),
    "PP4V2_BATT_VCC_V"            : (3.58, 3.73),
    "PP3V3_SYSTEM_BUCK_V"         : (3.1, 3.5),
    "PP1V8_SYSTEM_LDO_V"          : (1.72, 1.89),
    "PP5V0_BOOST_V"               : (4.9, 5.1),
    "PP3V3_WIFI_V"                : (3.13, 3.46),
    "PP1V8_EG21_VDD_EXT_V"        : (1.76, 1.84),
    "Input_Current"               : (63.51, 105.85),
}
# fmt: on


# ===============================================
# cosmo vcu103 test summary file and limits config
# ===============================================
CSV_FILE_PATH = "./Metro_Hybrid_FATP932_302_summary_sort_20260623_144334.csv"

OUTPUT_HTML = "Cosmo_VCU103_PCBA.html"
OUTPUT_PDF = "Cosmo_VCU103_PCBA.pdf"
OUTPUT_IMG_DIR = "Cosmo_VCU103_PCBA"

# fmt: off
SPEC_LIMITS = {
    "PP59V0_VEHICLE_CONN_V_Value"                 : (46.00, 51.00),
    "PP4V2_BATT_VCC_V_Value"                      : (3.99, 4.41),
    "PT_MCU_IMU_9axes_1_Value"                    : (-18000.00, 580.00),
    "PT_MCU_IMU_9axes_2_Value"                    : (-400.00, 580.00),
    "PT_MCU_IMU_9axes_3_Value"                    : (-18500.00, -800.00),
    "PT_MCU_IMU_9axes_4_Value"                    : (-100.00, 100.00),
    "PT_MCU_IMU_9axes_5_Value"                    : (-100.00, 100.00),
    "PT_MCU_IMU_9axes_6_Value"                    : (-100.00, 100.00),
    "PT_MCU_IMU_9axes_7_Value"                    : (-90000.00, 90000.00),
    "PT_MCU_IMU_9axes_8_Value"                    : (-90000.00, 90000.00),
    "PT_MCU_IMU_9axes_9_Value"                    : (-90000.00, 90000.00),
    "PT_MCU_BOARD_REV_ADC_Value"                  : (0.38, 0.88),
    "PT_MCU_59Vsense_ADC_Value"                   : (1.29, 1.42),
    "PT_MCU_5VBoost_Sense_ADC_Value"              : (2.60, 2.90),
    "PT_MCU_5VHandlebar_Switch_ADC_Value"         : (2.60, 2.90),
    "PT_PP5V0_HB_SW_RIGHT_CONN_V_Value"           : (4.90, 5.10),
    "PT_PP5V0_HB_SW_LEFT_CONN_V_Value"            : (4.90, 5.10),
    "PT_Copilot_SwitchIOs_00_Value"               : (0, 0),
    "PP4V2_BEACON_SW_CONN_V_Value"                : (0.00, 0.10),
    "PP4V2_BEACON_SW_CONN_EN_V_Value"             : (3.99, 4.41),
    "Beacon_PP4V2_BATT_VCC_Value"                 : (3.99, 4.41),
    "PP12V0_HEADLIGHT_OUT_CONN_Value"             : (0, 0.1),
    "PP12V0_HEADLIGHT_OUT_CONN_EN_Value"          : (5.40, 12.24),
    "MCU_HeadlightI_SNS_ADC_Value"                : (0.25, 0.55),
    "BATT_Volt_over_I2C_V_Value"                  : (3.40, 3.85),
    "BATT_Discharge_Curr_mA_Value"                : (131.00, 327.00),
    "BATT_Charge_Curr_mA_Value"                   : (630.00, 1305.00),
    "BB_PP59V0_VEHICLE_IN_CONN_V_Value"           : (0, 0.1),
    "BB_VEHICLE_BOOST_TO_MCU_ILIM_ADC_Value"      : (0, 15),
    "BB_PP59V0_VEHICLE_IN_CONN_EN_V_Value"        : (14, 15.3),
    "BB_PP12V0_VEHICLE_BUCK_OUT_V_Value"          : (-0.7, 0.5),
    "BB_VEHICLE_BOOST_TO_MCU_ILIM_100mA_ADC_Value": (88.00, 133.00),
    "BB_PP59V0_VEHICLE_IN_CONN_Re2A_V_Value"      : (14.47, 15.07),
    "BB_PP59V0_VEHICLE_IN_CONN_48V_V_Value"       : (47.04, 48.96),
    "BB_PP14V8_VEHICLE_BOOST_OUT_V_Value"         : (14.50, 15.10),
    "IPD_PP12V0_VEHICLE_BUCK_OUT_Value"           : (11.40, 12.24),
    "IPD_PP12V0_VEHICLE_BUCK_OUT_DIS_Value"       : (-0.50, 0.50),
    "IPD_BATT_Output_Curr_mA_Value"               : (-0.50, 0.50),
    "MCU_BRAKE_SNS_ADC_Value"                     : (0.95, 1.05),
    "MCU_BRAKE_SNS2_ADC_Value"                    : (0.95, 1.05),
    "MCU_THROTTLE_SNS_ADC_Value"                  : (0.80, 1.00),
    "MCU_THROTTLE_SNS2_ADC_Value"                 : (0.80, 1.00),
    "MCU_BRAKE_SNS_ADC_0V5_Value"                 : (0.41, 0.45),
    "MCU_BRAKE_SNS2_ADC_0V5_Value"                : (0.41, 0.45),
    "MCU_THROTTLE_SNS_ADC_0V5_Value"              : (0.26, 0.30),
    "MCU_THROTTLE_SNS2_ADC_0V5_Value"             : (0.26, 0.30),
    "MCU_BRAKE_SNS_ADC_4V5_Value"                 : (2.30, 2.60),
    "MCU_BRAKE_SNS2_ADC_4V5_Value"                : (2.30, 2.60),
    "MCU_THROTTLE_SNS_ADC_4V5_Value"              : (2.32, 2.58),
    "MCU_THROTTLE_SNS2_ADC_4V5_Value"             : (2.32, 2.58),
    "PP5V0_HB_SW_LEFT_CONN_CURR_mA_Value"         : (77.00, 116.00),
    "MCU_5V_HB_Switch_ADC_toG_Value"              : (0.00, 0.35),
    "MCU_5V_HB_Switch_ADC_Value"                  : (2.60, 2.90),
    "PP2V3_GNSS_OUT_CONN_Value"                   : (-0.1, 0.1),
    "PP2V3_GNSS_OUT_CONN_EN_Value"                : (2.23, 2.37),
    "MCU_TO_GNSS_AP_REQ_CONN_HIGH_Value"          : (1.15, 1.84),
    "MCU_TO_GNSS_AP_REQ_CONN_LOW_Value"           : (-0.10, 0.10),
    "GNSS_STANDBY_L_HIGH_Value"                   : (-0.10, 0.20),
    "GNSS_STANDBY_L_LOW_Value"                    : (2.10, 2.40),
    "PP4V2_BATT_VCC_NFC_CONN_Value"               : (3.99, 4.41),
    "PP3V3_NFC_CONN_Value"                        : (3.08, 3.41),
    "MCU_TO_NFC_RESET_L_HIGH_V_Value"             : (3.00, 3.50),
    "MCU_TO_NFC_RESET_L_LOW_V_Value"              : (-0.10, 0.10),
    "PP5V0_DISPLAY_V_Value"                       : (-0.50, 0.50),
    "PP5V0_DISPLAY_EN_V_Value"                    : (4.80, 5.30),
    "Display_LED_Curr_EN_mA_Value"                : (10.00, 48.00),
    "Display_LED_Curr_DIS_mA_Value"               : (-0.1, 0.1),
    "DAC_ID_I2C_Value"                            : (18, 18),
    "Speaker_Play_Sound_Value"                    : (-60.00, -15.00),
    "BTLE_RSSI_Value"                             : (-65.00, -35.00),
}
# fmt: on


# ========================================
# 使用说明
# ========================================
"""
如何添加新的测试项目:

1. 在 SPEC_LIMITS 字典中添加新行
2. 格式: "测试项目名称": (下限值, 上限值)
3. 示例:
   "My_New_Test": (1.0, 2.0)  # 下限1.0, 上限2.0

注意事项:
- 测试项目名称必须与CSV文件中的列名完全一致
- 规格限必须是数值(整数或浮点数)
- 如果只有单边规格,可以设置另一侧为None(需要在主程序中处理)
- 使用 # 添加注释说明测试项目的含义

如何修改CSV文件路径:
- 修改 CSV_FILE_PATH 变量的值
- 可以使用相对路径或绝对路径

如何修改输出文件名:
- 修改 OUTPUT_HTML 和 OUTPUT_PDF 变量
- 输出图片目录: OUTPUT_IMG_DIR
"""
