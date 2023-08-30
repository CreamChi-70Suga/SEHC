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

    def __init__(self, outbug, aircon, source_address, name):
        self._outbug = outbug
        self._aircon = aircon
        self._address = source_address
        self._name = name

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















