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
from FanRPM import *


class InputFunctions(BaseDevice, FanRpm):

    def __init__(self, outbug, aircon, source_address, name):
        self._outbug = outbug
        self._aircon = aircon
        self._address = source_address
        self._name = name

        self._result = Common(outbug, aircon)
        self._out = OutputFunctions(outbug, aircon, source_address, name)

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
    def set_wind_level(self, wind_level):
        state = self._out.check_operation_status()
        if state == OPERATION_OFF:
            Common.print_log("[set_wind_level] wait for turn on ")
            self.set_operation_on_off(OPERATION_ON)
            Common.wait(15)

        self.set_mode(SMART_MODE)
        self.set_gas_level(GAS_LEVEL1)
        if wind_level == HIGH_WIND:
            self.set_dust_level(4)
        elif wind_level == MEDIUM_WIND:
            self.set_dust_level(3)
        elif wind_level == LOW_WIND:
            self.set_dust_level(2)
        elif wind_level == WIND_FREE_WIND:
            self.set_mode(WIND_FREE_MODE)
        elif wind_level == SLEEP_WIND:
            self.set_mode(SLEEP_MODE)

        Common.wait(TIME_ONE_MIN * 1)
        target_rpm_top, target_rpm_bottom = self._out.get_target_rpm()
        Common.print_log("[set_wind_level] target_rpm_top: %s, "
                         "target_rpm_bottom: %s" % (target_rpm_top, target_rpm_bottom))
        self.get_rpm_from_table(SMART_MODE, self._out.platform_model, self._out.rpm_option)
        wind_cur = self.get_wind_level(target_rpm_top, target_rpm_bottom)
        Common.print_log("[set_wind_level] Current wind level: %s!" % wind_cur)
        if wind_cur == wind_level:
            Common.print_log("[set_wind_level] Set level %s successfully!" % wind_level)
        else:
            self._result.Stop("[set_wind_level] Set level %s fail!" % wind_level)

    # =============================================
    # Description: Set operation status
    # Parameter: Operation state (ON, OFF)
    # return - None
    # =============================================
    # Description: Set operation status
    # Parameter: Operation state (OPERATION_OFF, OPERATION_ON)
    #           ex) set_operation_on_off(OPERATION_OFF)
    # return - None
    # =============================================
    def set_operation_on_off(self, state):
        Common.print_log("[set_operation_on_off] Start set operation state to: %s " % state)
        # Check SETs is on or off
        current_state = self._out.check_operation_status()
        if current_state != state:
            self.set(ENUM_IN_OPERATION_ON_OFF, state)
            is_success = self.compare_value(ENUM_OUT_OPERATION_STATUS, state, 'timeout', 3)
            if is_success:
                Common.print_log("[set_operation_on_off] Set operation state successfully: %s " % state)
            else:
                self._result.Stop("[set_operation_on_off] Fail to set operation state: %s " % state)
        else:
            Common.print_log("[set_operation_on_off] Current operation: %s " % current_state)

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

    # =============================================
    # Description: Set auto windless mode entry conditions
    # Parameter: X
    # return - None
    # =============================================
    def auto_windless_mode_entry(self):
        """
        #precondition
            #1. Set smart mode
            #2. Set not entry to sleep mode - set BRIGHTNESS_LEVEL2
        #proceeding
            #1. Set cleanness level 1
            #2. Wait 10 minutes
        #Operation
            #1. RPM = 480
            #2. Close door
        """

        self.set_mode(SMART_MODE)
        self.set_illu_sensor(BRIGHTNESS_LEVEL2)
        Common.wait(TIME_ONE_SEC * 10)
        self.set_gas_level(GAS_LEVEL1)
        self.set_dust_level(1)

        Common.wait(TIME_ONE_MIN * 10)

        windless_entry = self.compare_value(VAR_OUT_TARGET_FAN_RPM_TOP, 480, 'timeout', 5)
        if windless_entry:
            Common.print_log("[auto_windless_mode_entry] Entry WindFree mode successfully!")
        else:
            self._result.Stop("[auto_windless_mode_entry] Entry WindFree mode Fail!")

    # =============================================
    # Description: Set auto sleep mode entry conditions
    # Parameter: X
    # return - None
    # =============================================
    def auto_sleep_mode_entry(self):
        """
        #precondition
            #1. Set smart mode
            #2. Set auto sleep mode in SmartThing app
        #proceeding
            #1. Set BRIGHTNESS_LEVEL0
            #2. Wait 30 seconds
        #Operation
            #1. RPM = 400
            #2. LCD, Led: off
            #3. Ambient Lighting: White color.
        """

        self.set_mode(SMART_MODE)
        # 2. Set auto sleep mode in SmartThing app (Wait library from Appview)

        self.set_illu_sensor(BRIGHTNESS_LEVEL0)
        Common.wait(TIME_ONE_SEC * 30)

        sleep_entry = self.compare_value(VAR_OUT_TARGET_FAN_RPM_TOP, 400, 'timeout', 5)
        if sleep_entry:
            Common.print_log("[auto_windless_mode_entry] Entry sleep mode successfully!")
        else:
            self._result.Stop("[auto_windless_mode_entry] Entry sleep mode Fail!")

    # =============================================
    # Description: Calculate the time between two changed sensor level
    # Parameter: sensor_level (1,2,3,4)
    # return - None
    # =============================================
       def measure_time(self, sensor_level):
        """
        default: operation On, Smart mode
        =========================================================
        1. Pre-condition:
            operation: On
            mode: Smart / Pet
            => input initial sensor value : set any level
        =========================================================
        2. Conditions:
            total = 0
            start = int(time.time())
            => sensor value is changed: set any level
            if set_level in range [set_level]
                end = int(time.time())
                total = end-start
                if total > 60:
                    print("[PASS] %s" total)
                else:
                    print("[ERROR] %s" total)
        3. Expected:
            - total > 60 seconds
        =========================================================

        """
        #precondition
        self.set_operation_on_off(OPERATION_ON)
        self.set_mode(SMART_MODE)
        self.set_gas_level(GAS_LEVEL2)
        self.set_dust_level(4)
        Common.wait(60)

        #Procedure
        self.set_gas_level(GAS_LEVEL2)
        self.set_dust_level(2)
        start_time = time.time()
        cur_rpm = 0
        while cur_rpm not in range(549, 571):
            cur_rpm = self.get(VAR_OUT_FAN_RPM_TOP)
            print("cur_rpm : %s" % cur_rpm)
            Common.wait(1)

        eslap_time_1 = time.time() - start_time
        print("eslap_time_1: %s" % eslap_time_1)

        Common.wait(10)
        self.set_dust_level(3)
        start_time = time.time()
        cur_rpm = 0
        while cur_rpm not in range(869, 891):
            cur_rpm = self.get(VAR_OUT_FAN_RPM_TOP)
            print("cur_rpm : %s" % cur_rpm)
            Common.wait(1)

        eslap_time_2 = time.time() - start_time
        print("eslap_time_2: %s" % eslap_time_2)

 


