# =============================================
# FILE		:	input.py
# DESC		:
# AUTHOR	:
# VER		:
# =============================================

import time
from library import *
from elements import *
from common import *
from output import *


class InputFunctions(BaseDevice):

    def __init__(self, outbug, aircon, source_address, name):
        self._outbug = outbug
        self._aircon = aircon
        self._address = source_address
        self._name = name

        self._result = Common(outbug, aircon)

    # =============================================
    # Description - Set power on/off use USB switch tool
    # # Parameter -	po
    # # return		-	X
    # =============================================
    @staticmethod
    def set_power_on_off(power=True):
        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        path += r"\05_Utility"
        Common.print_log("Path: %s" % path)

        if not os.path.exists(path):
            Common.print_log("Path: %s is not exist." % path)
            return
        if power:
            Common.print_log("[set_power_on_off] - set on")
            subprocess.Popen(path + r"\USBswitchCmd.exe 1", shell=True)
        else:
            Common.print_log("[set_power_on_off] - set off")
            subprocess.Popen(path + r"\USBswitchCmd.exe 0", shell=True)

        Common.wait(30, debug=True)

    # =============================================
    # Description - reset power use USB switch tool
    # # Parameter -	X
    # # return		-	X
    # =============================================
    @staticmethod
    def power_reset():
        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        path += r"\05_Utility"
        Common.print_log("Path: %s" % path)

        if not os.path.exists(path):
            Common.print_log("Path: %s is not exist." % path)
            return

        Common.print_log("[power_reset] Off")
        subprocess.Popen(path + r"\USBswitchCmd.exe 0", shell=True)

        Common.wait(10, debug=False)

        Common.print_log("[power_reset] On ")
        subprocess.Popen(path + r"\USBswitchCmd.exe 1", shell=True)

    # =============================================
    # Description: Setting operation mode
    # Parameter: Mode (SMART_MODE, HIGH_MODE, WIND_FREE_MODE, SLEEP_MODE, PET_MODE (depend on model))
    # return - X
    # =============================================
    def set_mode(self, mode):
        if mode in LIST_MODE_OPERATION:
            self.set(ENUM_IN_OPERATION_MODE, mode)
        else:
            self._result.Stop("[set_mode] %s mode is not exist." % mode)

        is_success = self.compare_value(ENUM_OUT_MODE_OPERATION, mode, 'timeout', 5)
        if is_success:
            Common.print_log("[set_mode] set %s mode successful " % mode)
        else:
            self._result.Stop("[set_mode] Can't set %s mode" % mode)

    # =============================================
    # Description: Set wind direction.
    # Parameter: Wind direction (1Way, 3Ways)
    # return - None
    # =============================================
    def set_wind_direction(self, way_mode):
        way_tmp = self.get(ENUM_IN_OPERATION_WIND_DIRECTION)
        Common.wait(3, debug=False)
        Common.print_log("[set_wind_direction] [Before setting] Blow air: %s " % way_tmp)
        if way_mode != way_tmp:
            self.set(ENUM_IN_OPERATION_WIND_DIRECTION, way_mode)
        else:
            Common.print_log("[set_wind_direction] Blow air: %s " % way_mode)

        is_success = self.compare_value(ENUM_IN_OPERATION_WIND_DIRECTION, way_mode, 'timeout', 5)
        if is_success:
            Common.print_log("[set_wind_direction] set %s successful " % way_mode)
        else:
            self._result.Stop("[set_wind_direction] Can't set %s " % way_mode)

    # =============================================
    # Description: Set a value from actor element
    # Parameter: Wind volume level (HIGH_WIND, MEDIUM_WIND, LOW_WIND, WIND_FREE, SLEEP)
    # return - None
    # =============================================
    def set_wind(self, wind_level):
        pass

    # =============================================
    # Description: Set gas value from actor element
    # Parameter: Gas level (GAS_LEVEL1, GAS_LEVEL2, GAS_LEVEL3, GAS_LEVEL4)
    # return - None
    # =============================================
    def set_gas_level(self, gas_level):
        if gas_level in GAS_CONFIG:
            self.set(VAR_IN_GAS_LEVEL, gas_level)
        else:
            self._result.Stop("[set_gas_level] can't set %s" % gas_level)

        is_success = self.compare_value(VAR_IN_GAS_LEVEL, gas_level)
        if is_success:
            Common.print_log("[set_gas_level] set %s successfully!" % gas_level)
        else:
            self._result.Stop("[set_gas_level] can't set %s" % gas_level)

    # =============================================
    # Description: Set illuminance value from actor element
    # Parameter: Illuminance level (BRIGHTNESS_LEVEL0, BRIGHTNESS_LEVEL1, BRIGHTNESS_LEVEL2)
    # return - None
    # =============================================
    def set_illu_sensor(self, bright_level):
        if bright_level in ILLUMINANCE_CONFIG:
            self.set(VAR_IN_ILLUMINANCE, bright_level)
            Common.print_log("[set_illu_sensor] set %s successfully!" % bright_level)
        else:
            self._result.Stop("[set_illu_sensor] can't set %s" % bright_level)


    # =============================================
    # Description: Set dust value from actor element
    # Parameter: Dust level (1, 2, 3, 4)
    # return - None
    # =============================================
    def set_dust_level(self, level):
        dust_level = DUST_CONFIG[0]

        if 0 < level:
            dust_level = DUST_CONFIG[level]
        else:
            self._result.Stop("[set_dust_level] can't set %s" % dust_level)

        VAL_PM10 = dust_level[0]
        VAL_PM2_5 = dust_level[1]
        VAL_PM1_0 = dust_level[2]

        self.sets(VAR_IN_PM_10, VAL_PM10, VAR_IN_PM_2_5, VAL_PM2_5, VAR_IN_PM_1_0, VAL_PM1_0, force_send=False)

        is_success = self.compare_value(VAR_IN_PM_10, VAL_PM10, VAR_IN_PM_2_5, VAL_PM2_5, VAR_IN_PM_1_0, VAL_PM1_0)
        if is_success:
            Common.print_log("[set_dust_level] set %s successfully!" % dust_level)
        else:
            self._result.Stop("[set_dust_level] can't set %s" % dust_level)
