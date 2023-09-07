# =============================================
# FILE		:	output.py
# DESC		:
# AUTHOR	:
# VER		:
# =============================================

import time
from library import *
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


