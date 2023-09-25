# =============================================
# FILE		: FanRPM.py
# DESC		: Fan RPM get set
# AUTHOR	: thingoc.dang
# VER		:
# =============================================

import common
from elements import *
from library import *

rpm_dict = {
    PET_MODE: {
        MEDIUM_SIZE: {
            "0": {
                "HIGH": {"TOP": 1240,
                         "MID": 1140},
                "MID": {"TOP": 950,
                        "MID": 850},
                "LOW": {"TOP": 640,
                        "MID": 500},
                "WINDFREE": {"TOP": None,
                             "MID": None},
                "SLEEP": {"TOP": None,
                          "MID": None}},
            "1": None},
        SMALL_SIZE: {
            "0": {
                "HIGH": {"TOP": 1240,
                         "MID": 0},
                "MID": {"TOP": 880,
                        "MID": 0},
                "LOW": {"TOP": 610,
                        "MID": 0},
                "WINDFREE": {"TOP": None,
                             "MID": None},
                "SLEEP": {"TOP": None,
                          "MID": None}},
            "1": {
                "HIGH": {"TOP": 1290,
                         "MID": 0},
                "MID": {"TOP": 880,
                        "MID": 0},
                "LOW": {"TOP": 610,
                        "MID": 0},
                "WINDFREE": {"TOP": None,
                             "MID": None},
                "SLEEP": {"TOP": None,
                          "MID": None}}}},
    SMART_MODE: {
        MEDIUM_SIZE: {
            "0": {
                "HIGH": {"TOP": 1240,
                         "MID": 1140},
                "MID": {"TOP": 950,
                        "MID": 850},
                "LOW": {"TOP": 560,
                        "MID": 420},
                "WINDFREE": {"TOP": 530,
                             "MID": 410},
                "SLEEP": {"TOP": 420,
                          "MID": 320}},
            "1": None},
        SMALL_SIZE: {
            "0": {
                "HIGH": {"TOP": 1240,
                         "MID": 0},
                "MID": {"TOP": 880,
                        "MID": 0},
                "LOW": {"TOP": 560,
                        "MID": 0},
                "WINDFREE": {"TOP": 480,
                             "MID": 0},
                "SLEEP": {"TOP": 400,
                          "MID": 0}},
            "1": {
                "HIGH": {"TOP": 1290,
                         "MID": 0},
                "MID": {"TOP": 880,
                        "MID": 0},
                "LOW": {"TOP": 560,
                        "MID": 0},
                "WINDFREE": {"TOP": 480,
                             "MID": 0},
                "SLEEP": {"TOP": 400,
                          "MID": 0}
            }
        }
    },
    HIGH_MODE: {
        MEDIUM_SIZE: {
            "0": {
                "HIGH": {"TOP": 1240,
                         "MID": 1140},
                "MID": {"TOP": None,
                        "MID": None},
                "LOW": {"TOP": None,
                        "MID": None},
                "WINDFREE": {"TOP": None,
                             "MID": None},
                "SLEEP": {"TOP": None,
                          "MID": None}},
            "1": None},
        SMALL_SIZE: {
            "0": {
                "HIGH": {"TOP": 1240,
                         "MID": 0},
                "MID": {"TOP": None,
                        "MID": None},
                "LOW": {"TOP": None,
                        "MID": None},
                "WINDFREE": {"TOP": None,
                             "MID": None},
                "SLEEP": {"TOP": None,
                          "MID": None}},
            "1": {
                "HIGH": {"TOP": 1290,
                         "MID": 0},
                "MID": {"TOP": None,
                        "MID": None},
                "LOW": {"TOP": None,
                        "MID": None},
                "WINDFREE": {"TOP": None,
                             "MID": None},
                "SLEEP": {"TOP": None,
                          "MID": None}
            }
        }
    },
    WIND_FREE_MODE: {
        MEDIUM_SIZE: {
            "0": {
                "HIGH": {"TOP": None,
                         "MID": None},
                "MID": {"TOP": None,
                        "MID": None},
                "LOW": {"TOP": None,
                        "MID": None},
                "WINDFREE": {"TOP": 530,
                             "MID": 410},
                "SLEEP": {"TOP": None,
                          "MID": None}},
            "1": None},
        SMALL_SIZE: {
            "0": {
                "HIGH": {"TOP": None,
                         "MID": None},
                "MID": {"TOP": None,
                        "MID": None},
                "LOW": {"TOP": None,
                        "MID": None},
                "WINDFREE": {"TOP": 480,
                             "MID": 0},
                "SLEEP": {"TOP": None,
                          "MID": None}},
            "1": {
                "HIGH": {"TOP": None,
                         "MID": None},
                "MID": {"TOP": None,
                        "MID": None},
                "LOW": {"TOP": None,
                        "MID": None},
                "WINDFREE": {"TOP": 480,
                             "MID": 0},
                "SLEEP": {"TOP": None,
                          "MID": None}
            }
        }
    },
    SLEEP_MODE: {
        MEDIUM_SIZE: {
            "0": {
                "HIGH": {"TOP": None,
                         "MID": None},
                "MID": {"TOP": None,
                        "MID": None},
                "LOW": {"TOP": None,
                        "MID": None},
                "WINDFREE": {"TOP": None,
                             "MID": None},
                "SLEEP": {"TOP": 420,
                          "MID": 320}},
            "1": None},
        SMALL_SIZE: {
            "0": {
                "HIGH": {"TOP": None,
                         "MID": None},
                "MID": {"TOP": None,
                        "MID": None},
                "LOW": {"TOP": None,
                        "MID": None},
                "WINDFREE": {"TOP": None,
                             "MID": None},
                "SLEEP": {"TOP": 400,
                          "MID": 0}},
            "1": {
                "HIGH": {"TOP": None,
                         "MID": None},
                "MID": {"TOP": None,
                        "MID": None},
                "LOW": {"TOP": None,
                        "MID": None},
                "WINDFREE": {"TOP": None,
                             "MID": None},
                "SLEEP": {"TOP": 400,
                          "MID": 0}
            }
        }}
}


class FanRpm:

    def __init__(self):

        self.rpm_sleep_mid = None
        self.rpm_sleep_top = None
        self.rpm_windfree_mid = None
        self.rpm_windfree_top = None
        self.rpm_low_top = None
        self.rpm_low_mid = None
        self.rpm_mid_mid = None
        self.rpm_mid_top = None
        self.rpm_high_mid = None
        self.rpm_high_top = None

    # =============================================
    # Description: get rpm value from table
    # Parameter: mode, platform, rpm_option
    #            ex)  get_rpm_from_table(SMART_MODE, MEDIUM_SIZE, "0")
    # return - None
    # =============================================
    def get_rpm_from_table(self, mode, platform, rpm_option):

        self.rpm_high_top = rpm_dict[mode][platform][rpm_option]["HIGH"]["TOP"]
        self.rpm_high_mid = rpm_dict[mode][platform][rpm_option]["HIGH"]["MID"]

        self.rpm_mid_top = rpm_dict[mode][platform][rpm_option]["MID"]["TOP"]
        self.rpm_mid_mid = rpm_dict[mode][platform][rpm_option]["MID"]["MID"]

        self.rpm_low_top = rpm_dict[mode][platform][rpm_option]["LOW"]["TOP"]
        self.rpm_low_mid = rpm_dict[mode][platform][rpm_option]["LOW"]["MID"]

        self.rpm_windfree_top = rpm_dict[mode][platform][rpm_option]["WINDFREE"]["TOP"]
        self.rpm_windfree_mid = rpm_dict[mode][platform][rpm_option]["WINDFREE"]["MID"]

        self.rpm_sleep_top = rpm_dict[mode][platform][rpm_option]["SLEEP"]["TOP"]
        self.rpm_sleep_mid = rpm_dict[mode][platform][rpm_option]["SLEEP"]["MID"]
        
        print("\t  [get_rpm_from_table]:")
        print("\t  rpm_high_top: %s, rpm_high_mid: %s" % (self.rpm_high_top, self.rpm_high_mid))
        print("\t  rpm_mid_top: %s, rpm_mid_mid: %s" % (self.rpm_mid_top, self.rpm_mid_mid))
        print("\t  rpm_low_top: %s, rpm_low_mid: %s" % (self.rpm_low_top, self.rpm_low_mid))
        print("\t  rpm_windfree_top: %s, rpm_windfree_mid: %s" % (self.rpm_windfree_top, self.rpm_windfree_mid))
        print("\t  rpm_sleep_top: %s, rpm_sleep_mid: %s" % (self.rpm_sleep_top, self.rpm_sleep_mid))

    # =============================================
    # Description: get wind level depend on current rpm
    # Parameter: top_rpm, mid_rpm
    #            ex)  get_wind_level(1240, 0)
    # return - wind level(HIGH_WIND, MEDIUM_WIND, ..)
    # =============================================
    def get_wind_level(self, top_rpm, mid_rpm):
        if top_rpm == self.rpm_high_top and mid_rpm == self.rpm_high_mid:
            return HIGH_WIND
        elif top_rpm == self.rpm_mid_top and mid_rpm == self.rpm_mid_mid:
            return MEDIUM_WIND
        elif top_rpm == self.rpm_low_top and mid_rpm == self.rpm_low_mid:
            return LOW_WIND
        elif top_rpm == self.rpm_windfree_top and mid_rpm == self.rpm_windfree_mid:
            return WIND_FREE_WIND
        elif top_rpm == self.rpm_sleep_top and mid_rpm == self.rpm_sleep_mid:
            return SLEEP_WIND
        else:
            return None
