# =============================================
# FILE		:	input.py
# DESC		:
# AUTHOR	:
# VER		:
# =============================================
import time
import datetime
from library import *
from elements import *
from common import *
from output import *
from FanRPM import *
from api_appview import *


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
            is_success = self.compare_value(ENUM_IN_OPERATION_WIND_DIRECTION, way_mode, 'timeout', 5)
            if is_success:
                Common.print_log("[set_wind_direction] set %s successful " % way_mode)
            else:
                self._result.Stop("[set_wind_direction] Can't set %s " % way_mode)
        else:
            Common.print_log("[set_wind_direction] Blow air: %s " % way_mode)

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
    # Parameter: Operation state (OPERATION_OFF, OPERATION_ON)
    #           ex) set_operation_on_off(OPERATION_OFF)
    # return - None
    # =============================================
    def set_operation_on_off(self, state):
        Common.print_log("[set_operation_on_off] Start set operation state to: %s " % state)
        # Check SET's operation is on or off
        current_state = self._out.check_operation_status()
        if current_state != state:
            self.set(ENUM_IN_OPERATION_ON_OFF, state)
            is_success = self.compare_value(ENUM_OUT_OPERATION_STATUS, state, 'timeout', 3)
            if is_success:
                Common.print_log("[set_operation_on_off] Set operation state sucessfully: %s " % state)
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
        current_level = self._out.check_gas_level()
        if current_level != gas_level:
            if gas_level in GAS_CONFIG:
                self.set(VAR_IN_GAS_LEVEL, gas_level)
            else:
                self._result.Stop("[set_gas_level] can't set %s" % gas_level)

            is_success = self.compare_value(VAR_IN_GAS_LEVEL, gas_level, 'timeout', 3)
            if is_success:
                Common.print_log("[set_gas_level] set %s successfully!" % gas_level)
            else:
                self._result.Stop("[set_gas_level] can't set %s" % gas_level)
        else:
            Common.print_log("[set_gas_level] Current Gas: %s " % current_level)

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
        current_level = self._out.check_dust_level()
        if current_level != level:
            dust_level = DUST_CONFIG[0]

            if 0 < level:
                dust_level = DUST_CONFIG[level]
            else:
                self._result.Stop("[set_dust_level] can't set %s" % dust_level)

            VAL_PM10 = dust_level[0]
            VAL_PM2_5 = dust_level[1]
            VAL_PM1_0 = dust_level[2]

            self.sets(VAR_IN_PM_10, VAL_PM10, VAR_IN_PM_2_5, VAL_PM2_5, VAR_IN_PM_1_0, VAL_PM1_0, force_send=False)

            is_success = self.compare_value(VAR_IN_PM_10, VAL_PM10,
                                                VAR_IN_PM_2_5, VAL_PM2_5,
                                                VAR_IN_PM_1_0, VAL_PM1_0,
                                                'timeout', 3)
            if is_success:
                Common.print_log("[set_dust_level] set %s successfully!" % dust_level)
            else:
                self._result.Stop("[set_dust_level] can't set %s" % dust_level)
        else:
            Common.print_log("[set_dust_level] Current Dust: %s " % current_level)

    # =============================================
    # Description: Set auto windless mode entry conditions
    # Parameter: X
    # return - None
    # =============================================
    def auto_windless_mode_entry(self):
        """
        Precondition
            #1. Set smart mode
            #2. Set not entry to sleep mode - set BRIGHTNESS_LEVEL2
        Proceeding
            #1. Set cleanness level 1
            #2. Wait 10 minutes
        Operation
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
        """Precondition
            #1. Set smart mode
            #2. Set auto sleep mode in SmartThing app
        Proceeding
            #1. Set BRIGHTNESS_LEVEL0
            #2. Wait 30 seconds
        Operation
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
    # Description: Calculate the time between wind level change
    # Parameter: mode, rpm_option, gas_level, dust_level, wind_level
    #            ex)measure_time_change_wind_level(SMART_MODE, "1", GAS_LEVEL2, 2, LOW_WIND)
    # return - elapsed_time
    # =============================================

    def measure_time_change_wind_level(self, mode, rpm_option, gas_level, dust_level, wind_level):

        self.set_gas_level(gas_level)
        self.set_dust_level(dust_level)

        start_time = time.time()
        Common.print_log("[measure_time_change_wins_level] start_time: %s" % datetime.datetime.now())

        self.get_rpm_from_table(mode, self._out.platform_model, rpm_option)
        target_top = 0
        target_mid = 0
        if wind_level == 5:
            target_top = self.rpm_high_top
            target_mid = self.rpm_high_mid
        elif wind_level == 4:
            target_top = self.rpm_mid_top
            target_mid = self.rpm_mid_mid
        elif wind_level == 3:
            target_top = self.rpm_low_top
            target_mid = self.rpm_low_mid
        elif wind_level == 2:
            target_top = self.rpm_windfree_top
            target_mid = self.rpm_windfree_mid
        elif wind_level == 1:
            target_top = self.rpm_sleep_top
            target_mid = self.rpm_sleep_mid

        self._out.get_absolute_rpm(mode, target_top, target_mid)

        elapsed_time = time.time() - start_time
        Common.print_log("[measure_time_change_wins_level] End_time: %s" % datetime.datetime.now())
        Common.print_log("[measure_time_change_wins_level] elapsed_time: %s" % elapsed_time)

        return elapsed_time
     
class InputFunctionsMobile(UserAPIAppView, Common):

    def __init__(self, mobile, outbug):
        self.mobile = mobile
        self.outbug = outbug

        self._out = OutputFunctionsMobile(mobile, outbug)

    # =============================================
    # Description: Go to "Devices" tab, find device's plugin name and enter device plugin
    # Parameter: Device's plugin name
    #           ex) enter_device_plugin("Air Purifier 81V")
    # return - None
    # =============================================
    def enter_device_plugin(self, plugin_name):
        try:
            ENTER_PLUGIN = "[enter_device_plugin] "
            self.print_log(ENTER_PLUGIN + "Close all the running app")
            self.mobile.CloseAllApp()
            self.wait(3)

            self.print_log(ENTER_PLUGIN + "Enter SmartThings App")
            self.mobile.OpenApp('com.samsung.android.oneconnect')
            self.wait(3)

            self.user_touch_object(text='Devices')
            self.wait(2)

            self.print_log(ENTER_PLUGIN + "Enter device's plugin: %s" % plugin_name)
            has_text = self.user_text_exits(plugin_name)
            if has_text:
                self.user_touch_object(text=plugin_name)
                has_text_ = self.user_wait_text_occur(plugin_name, 60)
                self.wait(4)
                if has_text_:
                    print(ENTER_PLUGIN + "Enter device's plugin: %s successfully" % plugin_name)
                else:
                    self.Stop(ERROR_NOTIF + " Couldn't enter device's plugin: %s" % plugin_name)
            else:
                self.Stop(ERROR_NOTIF + " Check current existing plugin name again: %s" % plugin_name)
        except Exception:
            self.Stop(ERROR_NOTIF + " Error while go to device's plugin: %s" % plugin_name)

    # =============================================
    # Description: Enable/disable a feature's toggle's status
    # Parameter: Target state text, toggle's name text
    # ex) btn_ai_cleaning_off_txt = "Off, AI purify , Switch"
    # ai_cleaning_txt = "AI purify, Enable air purifying-related features when the indoor air quality is bad."
    # enable_disable_toggle(btn_ai_cleaning_off_txt, ai_cleaning_txt)
    # return - None
    # =============================================
    def enable_disable_toggle(self, state, toggle_name_txt):
        if toggle_name_txt == welcome_care_txt:
            btn_off_txt = btn_welcome_care_off_txt
            btn_on_txt = btn_welcome_care_on_txt
            toggle_txt = welcome_care_txt
        elif toggle_name_txt == ai_cleaning_txt:
            btn_off_txt = btn_ai_cleaning_off_txt
            btn_on_txt = btn_ai_cleaning_on_txt
            toggle_txt = ai_cleaning_txt
        else:
            btn_off_txt = btn_smart_sleep_off_txt
            btn_on_txt = btn_smart_sleep_on_txt
            toggle_txt = smart_sleep_off_txt

        off_state = self.mobile.HasTextAND(btn_off_txt)
        if off_state is True:
            if state == btn_on_txt:
                self.user_touch_object(text=btn_off_txt)
                self.user_wait_text_occur(btn_on_txt, 4)
                cur_state = self._out.get_toggle_status(toggle_txt)
                if cur_state:
                    Common.print_log("[enable_disable_toggle] Enable toggle successfully.")
                else:
                    Common.print_log("[enable_disable_toggle] Unable to Enable toggle!")
            elif state == btn_off_txt:
                self._out.get_toggle_status(toggle_txt)
                Common.print_log("[enable_disable_toggle] Toggle is already OFF!")

        elif off_state is False:
            if state == btn_on_txt:
                self._out.get_toggle_status(toggle_txt)
                Common.print_log("[enable_disable_toggle] Toggle is already ON!")
            elif state == btn_off_txt:
                self.user_touch_object(text=btn_on_txt)
                self.user_wait_text_occur(btn_off_txt, 4)
                cur_state = self._out.get_toggle_status(toggle_txt)
                if cur_state is False:
                    Common.print_log("[enable_disable_toggle] Disable toggle successfully.")
                else:
                    Common.print_log("[enable_disable_toggle] Unable to disable toggle!")
        else:
            Common.print_log("[enable_disable_toggle] Can't switch toggle!")

    # =============================================
    # Description: Enable/Disable AI Cleaning On/Off status
    # Parameter:  Toggle's state (btn_ai_cleaning_on_txt, btn_ai_cleaning_off_txt)
    #           ex) btn_ai_cleaning_off_txt = "Off, AI purify , Switch"
    #               enable_disable_AICleaning(btn_ai_cleaning_off_txt)
    # Return - None
    # =============================================
    def enable_disable_AICleaning(self, state):
        Common.print_log("[enable_disable_AICleaning]")
        self.enable_disable_toggle(state, ai_cleaning_txt)

    # =============================================
    # Description: Enable/disable Welcome air care toggle's state
    # Parameter: Toggle's state (btn_welcome_care_on_txt, btn_welcome_care_off_txt)
    #           ex) btn_welcome_care_on_txt = "On, Welcome air care , Switch"
    #               enable_disable_WelcomCare(btn_welcome_care_on_txt)
    # return - None
    # =============================================
    def enable_disable_WelcomCare(self, state):
        Common.print_log("[enable_disable_WelcomCare]")
        self.enable_disable_toggle(state, welcome_care_txt)

    # =============================================
    # Description: Enable/disable Smart Sleep Mode toggle's state
    # Parameter: Toggle's state (btn_smart_sleep_on_txt, btn_smart_sleep_off_txt)
    #           ex) btn_smart_sleep_on_txt = "On, Smart Sleep Mode , Switch"
    #               enable_disable_SmartSleep(btn_smart_sleep_on_txt)
    # return - None
    # =============================================
    def enable_disable_SmartSleep(self, state):
        Common.print_log("[enable_disable_SmartSleep]")
        self.enable_disable_toggle(state, smart_sleep_off_txt)

    # =============================================
    # Description: Set SET's mode operation
    # Parameter: Mode (smart_mode_txt, max_mode_txt, windfree_mode_txt, sleep_mode_txt, pet_mode_txt)
    #           ex) pet_mode_txt = "Mode, Pet"
    #               set_mode_STA(pet_mode_txt)
    # return - None
    # =============================================
    def set_mode_STA(self, mode):
        if mode in list_mode_operation:
            current_mode = self._out.get_mode_STA()
            text_mode = mode.split(", ")[1]
            if current_mode != mode:
                self.user_touch_object(text=current_mode)
                self.wait(1)
                self.user_touch_object(text=text_mode)
                self.wait(4)
            elif current_mode == mode:
                Common.print_log("[set_mode_STA] Current mode already is %s." % text_mode)

            is_success = self.user_text_exits(mode)
            if is_success:
                Common.print_log("[set_mode_STA] Set %s mode successfully." % text_mode)
            else:
                self.Stop(ERROR_NOTIF + " Couldn't set mode: %s" % text_mode)
        else:
            self.Stop(ERROR_NOTIF + " Check target mode text again!")

    # =============================================
    # Description: Set SET's operation state
    # Parameter: state (btn_power_off_txt, btn_power_on_txt)
    #           ex) set_operation_on_off_STA(btn_power_off_txt)
    # return - None
    # =============================================
    def set_operation_on_off_STA(self, state):
        current_state = self.mobile.HasTextAND(btn_power_off_txt)
        if current_state is True:
            if state == btn_power_on_txt:
                self.user_touch_object(text=btn_power_off_txt)
                self.user_wait_text_occur(btn_power_on_txt, 3)
                Common.print_log("[set_operation_on_off_STA] Operation On")
            elif state == btn_power_off_txt:
                Common.print_log("[set_operation_on_off_STA] Operation Off")
        elif current_state is False:
            if state == btn_power_on_txt:
                Common.print_log("[set_operation_on_off_STA] Operation On")
            elif state == btn_power_off_txt:
                self.user_touch_object(text=btn_power_on_txt)
                self.user_wait_text_occur(btn_power_off_txt, 3)
                Common.print_log("[set_operation_on_off_STA] Operation Off")
            else:
                Common.print_log("[set_operation_on_off_STA] Can't set operation!")