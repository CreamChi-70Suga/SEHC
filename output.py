# -- coding: utf-8 --
# =============================================
# FILE		:	output.py
# DESC		:
# AUTHOR	:
# VER		:
# =============================================
import time
from library import *
from input import *
from elements import *
from common import *
from input import *
from api_appview import *

class OutputFunctions(BaseDevice):
    platform_model = SMALL_SIZE
    rpm_option = "1"

    def __init__(self, outbug, aircon, source_address, name):
        self._outbug = outbug
        self._aircon = aircon
        self._address = source_address
        self._name = name

    # =============================================
    # Description:  get model size
    # Parameter: model size (MEDIUM_SIZE, SMALL_SIZE)
    # return - None
    # =============================================
    def get_platform_model(self, model):
        self.platform_model = model

    # =============================================
    # Description:  get rpm option table
    # Parameter: option ("0", "1")
    # return - None
    # =============================================
    def get_rpm_option(self, option):
        self.rpm_option = option

    # =============================================
    # Description:  Check status of UV led
    # Parameter: X
    # return - On/Off
    # =============================================
    def get_UV_led_status(self):
        value = self.get(ENUM_OUT_UV_LED)
        Common.print_log("[get_UV_led_status] State: %s " % value)
        return value

    # =============================================
    # Description: Check HPVS ON/OFF, K-filter mode
    # Parameter: X
    # return - Mode, hpvs_state
    # =============================================
    def get_k_filter_mode(self):
        mode = self.get(ENUM_OUT_K_FILTER_MODE)
        hpvs_state = "OFF"
        if mode != "OFF":
            hpvs_state = "ON"

        Common.print_log("[get_k_filter_mode] HPVS state: %s , Mode: %s " % (hpvs_state, mode))
        return mode, hpvs_state

    # =============================================
    # Description: Check operation status (ON/OFF)
    # Parameter: X
    # return - Operation state
    # =============================================
    def check_operation_status(self):
        state = self.get(ENUM_OUT_OPERATION_STATUS)
        if state == OPERATION_OFF or state == OPERATION_ON:
            Common.print_log("[check_operation_status] Operation status: %s" % state)
        else:
            Common.print_log("Unable to check operation status")
        return state

    # =============================================
    # Description: Check gas level ()
    # Parameter: X
    # return - Gas level
    # =============================================
    def check_gas_level(self):
        level = self.get(VAR_IN_GAS_LEVEL)
        if level == GAS_LEVEL1 or level == GAS_LEVEL2 or level == GAS_LEVEL3 or level == GAS_LEVEL4:
            Common.print_log("[check_gas_level] Gas value: %s" % int(level))
        else:
            Common.print_log("Unable to check gas value")
        return level

    # =============================================
    # Description: Check dust level ()
    # Parameter: X
    # return - Dust level
    # =============================================
    def check_dust_level(self):
        PM_10 = int(self.get(VAR_IN_PM_10))

        if PM_10 in range(0, 31):
            Common.print_log("[check_dust_level] 1Lv-Good: %s" % PM_10)
            return 1
        elif PM_10 in range(31, 81):
            Common.print_log("[check_dust_level] 2Lv-Normal: %s" % PM_10)
            return 2
        elif PM_10 in range(81, 151):
            Common.print_log("[check_dust_level] 3Lv-Poor: %s" % PM_10)
            return 3
        elif PM_10 > 150:
            Common.print_log("[check_dust_level] 4Lv-Very poor: %s" % PM_10)
            return 4
        else:
            Common.print_log("[check_dust_level] Can't get dust value")

    # =============================================
    # Description: Get current fan RPM
    # Parameter: X
    # return - RPM values (top fan, middle fan)
    # =============================================
    def get_rpm(self):
        top_rpm = int(self.get(VAR_OUT_FAN_RPM_TOP))
        mid_rpm = int(self.get(VAR_OUT_FAN_RPM_MID))
        Common.print_log("[get_rpm] Top Fan RPM: %s, Mid Fan RPM: %s" % (top_rpm, mid_rpm))
        return top_rpm, mid_rpm

    # =============================================
    # Description: Get target fan RPM
    # Parameter: X
    # return - RPM values (top fan, middle fan)
    # =============================================
    def get_target_rpm(self):
        top_rpm_target = int(self.get(VAR_OUT_TARGET_FAN_RPM_TOP))
        mid_rpm_target = int(self.get(VAR_OUT_TARGET_FAN_RPM_MID))
        Common.print_log("[get_target_rpm] Target Top RPM: %s, Target Mid RPM: %s" % (top_rpm_target, mid_rpm_target))
        return top_rpm_target, mid_rpm_target

    # =============================================
    # Description:  Check SET's mode operation
    # Parameter:    X
    # return:       Mode (SMART_MODE, HIGH_MODE, WINDFREE_MODE, SLEEP_MODE, PET_MODE (depend on model))
    # =============================================
    def get_mode(self):
        mode = self.get(ENUM_OUT_MODE_OPERATION)
        Common.print_log("[get_mode] Mode: %s " % mode)
        return mode

    # =============================================
    # Description: Get absolute value of current fan RPM based on target RPM
    # Parameter:  mode, top_rpm_target, mid_rpm_target
    # return - RPM absolute values (top fan, middle fan)
    # =============================================
    def get_absolute_rpm(self, mode, top_rpm_target, mid_rpm_target):
        abs_top_rpm = 0
        abs_mid_rpm = 0
        Common.print_log("[get_absolute_rpm] Top Target Fan RPM: %s, Mid Target Fan RPM: %s" %
                         (top_rpm_target, mid_rpm_target))

        if mode == SMART_MODE or mode == PET_MODE:
            rpm_range = range(-10, 11)
        else:
            if self.platform_model == SMALL_SIZE:
                rpm_range = range(-60, 121)
            elif self.platform_model == MEDIUM_SIZE:
                rpm_range = range(-60, 61)

        cnt = 0
        time_out = 120
        while cnt < time_out:
            top_rpm, mid_rpm = self.get_rpm()
            top_limit = top_rpm_target - top_rpm
            mid_limit = mid_rpm_target - mid_rpm

            if top_limit in rpm_range and mid_limit in rpm_range:
                abs_top_rpm, abs_mid_rpm = top_rpm_target, mid_rpm_target
                Common.print_log(
                    "[get_absolute_rpm] abs_top_rpm: %s , abs_mid_rpm: %s" % (abs_top_rpm, abs_mid_rpm))
                Common.print_log(
                    "[get_absolute_rpm] Current RPM values are in range: Top: [%s, %s], Mid: [%s, %s]" %
                    (abs_top_rpm + rpm_range[0], abs_top_rpm + (rpm_range[len(rpm_range) - 1]),
                     abs_mid_rpm + rpm_range[0], abs_mid_rpm + (rpm_range[len(rpm_range) - 1])))
                break

            Common.wait(2)
            cnt += 1
        else:
            Common.print_log("[get_absolute_rpm] time out: %s" % cnt)

        return abs_top_rpm, abs_mid_rpm

    # =============================================
    # Description: Get angle front panel
    # Parameter:  None
    # return - Angle
    # =============================================
    def get_angle(self):
        angle = self.get(VAR_OUT_ANGLE)
        Common.print_log("[get_angle] angle: %s " % angle)
        return angle

    # =============================================
    # Description: Get Cumulative Power Consumption
    # Parameter:  None
    # return - cumulative_power
    # =============================================
    def get_cumulative_power_consumption(self):
        cumulative_power = self.get(VAR_OUT_CUMULATIVE_POWER)
        Common.print_log("[get_cumulative_power_consumption] cumulative_power: %s " % cumulative_power)
        return cumulative_power

    # =============================================
    # Description: Check the SET's operation
    # Parameter:  None
    # return - Results (True/False)
    # =============================================
    def check_error(self):
        self.sets(VAR_IN_GAS_LEVEL, GAS_LEVEL3, VAR_IN_PM_10, 151, ENUM_IN_OPERATION_ON_OFF, OPERATION_ON,
                  force_send=False)
        flag = self.compare_value(VAR_IN_GAS_LEVEL, GAS_LEVEL3, VAR_IN_PM_10, 151,
                                  ENUM_OUT_OPERATION_STATUS, OPERATION_ON, 'timeout', 3)

        if flag:
            Common.print_log("[check_error] SET's Normal")
            return True
        else:
            Common.print_log("[check_error] SET's Abnormal")
            return False


# MOBILE ==================

class OutputFunctionsMobile(UserAPIAppView):

    def __init__(self, mobile, outbug):
        self.mobile = mobile
        self.outbug = outbug

    # =============================================
    # Description: Check toggle status of a function's toggle button
    # Parameter: Function name's text of toggle
    # ex) ai_cleaning_txt = "AI purify, Enable air purifying-related features when the indoor air quality is bad."
    #               get_toggle_status(ai_cleaning_txt)
    # Return - State (True/False)
    # =============================================
    def get_toggle_status(self,toggle_txt):
        self.wait(2)

        if toggle_txt == welcome_care_txt or toggle_txt == ai_cleaning_txt:
            self.user_touch_object(text=toggle_txt)
        #  Enter Smart Sleep Mode page
        elif toggle_txt:
            welcome_care_pc = self.user_get_pointcenter(text=welcome_care_txt)
            self.mobile.Touch(welcome_care_pc[0][0], welcome_care_pc[0][1] + 228, duration=0, recording=False)

        self.wait(2)

        off_state = self.mobile.HasTextAND(btn_switch_off_txt)
        if off_state:
            Common.print_log("[get_toggle_status] Toggle is OFF")
            return False
        elif off_state is False:
            Common.print_log("[get_toggle_status] Toggle is ON")
            return True
        else:
            Common.print_log("[get_toggle_status] Can't get toggle's state!")
            self.Stop(ERROR_NOTIF)

    # =============================================
    # Description: Check SET's mode operation
    # Parameter: X
    #           ex) get_mode_STA()
    # return - Mode (smart_mode_txt, max_mode_txt, windfree_mode_txt, sleep_mode_txt, pet_mode_txt (depend on model))
    # =============================================
    def get_mode_STA(self):
        self.wait(3)
        noti_log_mode = "[get_mode_STA] Mode: "
        if self.user_text_exits(smart_mode_txt):
            Common.print_log(noti_log_mode + SMART_MODE)
            return smart_mode_txt
        elif self.user_text_exits(max_mode_txt):
            Common.print_log(noti_log_mode + HIGH_MODE)
            return max_mode_txt
        elif self.user_text_exits(windfree_mode_txt):
            Common.print_log(noti_log_mode + WIND_FREE_MODE)
            return windfree_mode_txt
        elif self.user_text_exits(sleep_mode_txt):
            Common.print_log(noti_log_mode + SLEEP_MODE)
            return sleep_mode_txt
        elif self.user_text_exits(pet_mode_txt):
            Common.print_log(noti_log_mode + PET_MODE)
            return pet_mode_txt

    # =============================================
    # Description: Check SET's operation status
    # Parameter: X
    #           ex) get_operation_status_STA()
    # return - State (btn_power_on_txt, btn_power_off_txt)
    # =============================================
    def get_operation_status_STA(self):
        self.wait(3)
        noti_log_operation = "[get_operation_status_STA] Operation status: "
        if self.user_text_exits(btn_power_on_txt):
            Common.print_log(noti_log_operation + OPERATION_ON)
            return btn_power_on_txt
        elif self.user_text_exits(btn_power_off_txt):
            Common.print_log(noti_log_operation + OPERATION_OFF)
            return btn_power_off_txt

    # =============================================
    # Description:  get sensor level in SmartThings App
    # Parameter:    cleanness_name (VAR_IN_PM_10 / VAR_IN_PM_2_5 / VAR_IN_PM_1_0 / VAR_IN_GAS_LEVEL)
    #               Eg) get_cleanness_sensor_indicate(VAR_IN_GAS_LEVEL)
    # Return:       Indicate and state of dust and gas
    # =============================================
    def get_cleanness_sensor_indicate(self, cleanness_name):
        list_objects = self.user_get_object(class_attr="android.widget.TextView")
        cleanness_indicate = ''
        cleanness_state = ''
        cleanness_x1 = 0
        cleanness_y1 = 0
        if list_objects is None:
            self.print_log("[get_dust_sensor_indicate] Couldn't find object")
            return cleanness_indicate, cleanness_state

        for obj in list_objects:
            name_txt = obj['text']
            if name_txt == cleanness_name:
                cleanness_x1 = obj['bounds'][0]
                cleanness_y1 = obj['bounds'][1]

        for obj in list_objects:
            x1 = obj['bounds'][0]
            y1 = obj['bounds'][1]
            if x1 == cleanness_x1 and cleanness_y1 < y1 < cleanness_y1 + 250:
                txt_tmp = obj['text']
                pos = txt_tmp.find('㎍/㎥')
                pos_gas = txt_tmp.find("Lv")
                if pos != -1 or pos_gas != -1:
                    cleanness_indicate = txt_tmp
                elif txt_tmp in STATE_AIR:
                    cleanness_state = txt_tmp
                Common.print_log("[get_cleanness_sensor_indicate] %s: %s %s"
                                 % (cleanness_name, cleanness_indicate, cleanness_state))
        return cleanness_indicate, cleanness_state
