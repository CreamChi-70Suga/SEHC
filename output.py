# =============================================
# FILE		:	output.py
# DESC		:
# AUTHOR	:
# VER		:
# =============================================
from library import *
import input
from elements import *
from common import *


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

        Common.print_log("[ENUM_OUT_K_FILTER_MODE] HPVS state: %s , Mode: %s " % (hpvs_state, mode))
        return mode, hpvs_state

    # =============================================
    # Description: Check operation status (ON/OFF)
    # Parameter: X
    # return - Operation state
    # =============================================
    def check_operation_status(self):
        state = self.get(ENUM_OUT_OPERATION_STATUS)
        if state == OPERATION_OFF or state == OPERATION_ON:
            Common.print_log("[ENUM_OUT_OPERATION_STATUS] Operation status: %s" % state)
        else:
            Common.print_log("Unable to check operation status")
        return state

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
    # Description: Check SET's mode operation
    # Parameter: X
    # return - Mode (SMART_MODE, HIGH_MODE, WINDFREE_MODE, SLEEP_MODE, PET_MODE (depend on model))
    # =============================================
    def get_mode(self):
        mode = self.get(ENUM_OUT_MODE_OPERATION)
        Common.print_log("[get_mode] Mode: %s " % mode)
        return mode

    def get_absolute_rpm(self, mode, platform):
        abs_top_rpm = 0
        abs_mid_rpm = 0

        for retry in range(0, 3):
            if mode == SMART_MODE or mode == PET_MODE:
                rpm_range = range(-10, 11)
            else:
                if platform == "SMALL":
                    rpm_range = range(-60, 121)
                elif platform == "MEDIUM":
                    rpm_range = range(-60, 61)

            top_rpm, mid_rpm = self.get_rpm()
            top_rpm_target, mid_rpm_target = self.get_target_rpm()
            top_limit = top_rpm_target - top_rpm
            mid_limit = mid_rpm_target - mid_rpm
            Common.wait(30)
            if top_limit in rpm_range and mid_limit in rpm_range:
                abs_top_rpm, abs_mid_rpm = top_rpm_target, mid_rpm_target
                Common.print_log("[get_absolute_rpm] Target RPM's range: Top: [%s, %s], Mid: [%s, %s]" %
                                 (abs_top_rpm + rpm_range[0], abs_top_rpm + (rpm_range[len(rpm_range) - 1]),
                                  abs_mid_rpm + rpm_range[0], abs_mid_rpm + (rpm_range[len(rpm_range) - 1])))
                break
            else:
                Common.print_log("[get_absolute_rpm] RPM value is not in target RPM range")

            # Common.wait(30)
            Common.print_log("[get_absolute_rpm] [Retry]: %s"
                             "\n\t   [get_rpm] Top Fan RPM: %s, Mid Fan RPM: %s"
                             "\n\t   [get_target_rpm] Top Fan RPM: %s, Mid Fan RPM: %s" % (
                                 (retry + 1), top_rpm, mid_rpm, top_rpm_target, mid_rpm_target))
        return abs_top_rpm, abs_mid_rpm

    # =============================================
    # Description: Get absolute value of current fan RPM based on target RPM
    # Parameter: Mode (SMART_MODE or PET_MODE),
    #            Platform type (SMALL_SIZE, MEDIUM_SIZE)
    # return - RPM absolute values (top fan, middle fan)
    # =============================================
    def get_current_rpm(self, mode, platform):
        abs_top_rpm = 0
        abs_mid_rpm = 0

        if mode == SMART_MODE or mode == PET_MODE:
            rpm_range = range(-10, 11)
        else:
            if platform == "SMALL":
                rpm_range = range(-60, 121)
            elif platform == "MEDIUM":
                rpm_range = range(-60, 61)

        for retry in range(0, 30):
            Common.wait(3)
            top_rpm, mid_rpm = self.get_rpm()
            top_rpm_target, mid_rpm_target = self.get_target_rpm()
            top_limit = top_rpm_target - top_rpm
            mid_limit = mid_rpm_target - mid_rpm

            if top_limit in rpm_range and mid_limit in rpm_range:
                abs_top_rpm, abs_mid_rpm = top_rpm_target, mid_rpm_target
                Common.print_log("[get_current_rpm] Current RPM values are in range: Top: [%s, %s], Mid: [%s, %s]" %
                                 (abs_top_rpm + rpm_range[0], abs_top_rpm + (rpm_range[len(rpm_range) - 1]),
                                  abs_mid_rpm + rpm_range[0], abs_mid_rpm + (rpm_range[len(rpm_range) - 1])))
                break
            else:
                Common.print_log("[get_current_rpm] RPM value is not in target RPM range")

            Common.print_log("[get_current_rpm] [Retry]: %s" % (retry + 1))
        return abs_top_rpm, abs_mid_rpm


