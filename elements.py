# =============================================
# FILE		:	elements.py
# DESC		:	Define elements actor
# AUTHOR	:	thingoc.dang
# VER		:	230821
# =============================================
from library import *

ENUM_IN_OPERATION_MODE = "Mode Setting"
ENUM_IN_OPERATION_ON_OFF = "Operation On Off Setting"
ENUM_IN_OPERATION_WIND_DIRECTION = "Wind Direction"
VAR_IN_PM_10 = "PM10"
VAR_IN_PM_2_5 = "PM2.5"
VAR_IN_PM_1_0 = "PM1.0"
VAR_IN_GAS_LEVEL = "Gas"
VAR_IN_FILTER = "Filter usage count"
VAR_IN_ILLUMINANCE = "Illuminance sensor"
VAR_IN_Fan_RPM_TOP = "FanRpmTop Setting"
VAR_IN_Fan_RPM_MID = "FanRpmMid Setting"

ENUM_OUT_UV_LED = "UV Led State"
ENUM_OUT_K_FILTER_MODE = "K Filter Mode"
ENUM_OUT_MODE_OPERATION = "Mode Operation"
VAR_OUT_FAN_RPM_TOP = "vFanRpmTop"
VAR_OUT_FAN_RPM_MID = "vFanRpmMid"
VAR_OUT_TARGET_FAN_RPM_TOP = "targetTop"
VAR_OUT_TARGET_FAN_RPM_MID = "targetMid"
ENUM_OUT_OPERATION_STATUS = "Operation Status"


SMART_MODE = "Smart"
HIGH_MODE = "High"
WIND_FREE_MODE = "WindFree"
SLEEP_MODE = "Sleep"
PET_MODE = "Pet"

ONE_WAY = "1WAY"
THREE_WAYS = "3WAYS"

OPERATION_OFF = "OFF"
OPERATION_ON = "ON"


LIST_MODE_OPERATION = [SMART_MODE, HIGH_MODE, WIND_FREE_MODE, SLEEP_MODE, PET_MODE]

DUST_CONFIG = [
    [],  # None
    [PM10_LEVEL1, PM2_5_LEVEL1, PM1_0_LEVEL1],  # Level 1
    [PM10_LEVEL2, PM2_5_LEVEL2, PM1_0_LEVEL2],  # Level 2
    [PM10_LEVEL3, PM2_5_LEVEL3, PM1_0_LEVEL3],  # Level 3
    [PM10_LEVEL4, PM2_5_LEVEL4, PM1_0_LEVEL4]   # Level 4
]

GAS_CONFIG = [GAS_LEVEL1, GAS_LEVEL2, GAS_LEVEL3, GAS_LEVEL4]

ILLUMINANCE_CONFIG = [BRIGHTNESS_LEVEL0, BRIGHTNESS_LEVEL1, BRIGHTNESS_LEVEL2]

VIRTUAL_ELEMENT_TABLE = {

}
