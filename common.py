# =============================================
# FILE		:	common.py
# DESC		:	set, get value from actor
# AUTHOR	:	thingoc.dang
# VER		:	230821
# =============================================

import time
import datetime
import os
import sys
import subprocess


class Common:

    def __init__(self, outbug, aircon):
        self.outbug = outbug
        self.aircon = aircon

    # ==============================================
    # Description - Log Output
    # Parameter - msg : Message
    # # return - X
    # ==============================================
    @staticmethod
    def print_log(message):
        print("%s %s" % (datetime.datetime.now().strftime("%H:%M:%S"), message))

    # =============================================
    # Description - Waiting for time
    # Parameter - t : Time to wait (in seconds)
    # debug: message output status
    # # return - X
    # ==============================================
    @staticmethod
    def wait(t, debug=True):
        if debug:
            current = datetime.datetime.now()
            target = current + datetime.timedelta(seconds=t)

            msg_current = "{:%H:%M:%S}".format(current)
            msg_target = "{:%H:%M:%S}".format(target)

            h = t / 3600
            m = (t % 3600) / 60
            s = (t % 3600) % 60

            Common.print_log(
                "[wait] Wait %d hours %d minutes %d seconds ==> %s ~ %s" % (h, m, s, msg_current, msg_target))

        time.sleep(t)

    def Pass(self):
        self.print_log("[Debug] PASS")
        self.outbug.Pass()

    def Fail(self):
        self.print_log("[Debug] FAIL")
        self.outbug.Fail()

    def Stop(self, msg):
        self.print_log("[Debug] STOP")
        self.outbug.Stop(msg)

    def Exempt(self, msg):
        self.print_log("[Debug] Exempt")
        self.outbug.Exempt(msg)


class BaseDevice:
    _str_cmd = "Command"
    _get_cmd = 0xA01200
    _set_cmd = 0xA01100
    _sender_address = 0x00

    # =============================================
    # Description	-   Base device class constructor
    # Parameter		-	outbug : Outbug instance
    #					aircon : Aircon instance
    #					address : Device address
    #					name : the device name to be used in Debug message
    # return		-	X
    # =============================================
    def __init__(self, outbug, aircon, address, name):
        self._outbug = outbug
        self._aircon = aircon
        self._address = address
        self._name = name

    # =============================================
    # Description	-   Get value from actor
    # Parameter		-	element : Name of element
    #               ex) get("PM10")
    # return		-	Element value
    # =============================================
    def get(self, element):
        value = self._aircon.GetValue(self._sender_address, element)

        if str(type(value)) == "<type 'Array[Byte]'>":
            str_list = list(value)
            hex_data = ''.join('%02x' % byte for byte in str_list)
            return hex_data
        else:
            return value

    # =============================================
    # Description	-   Get values from actor
    # Parameter		-	element : Name of elements
    #               ex) get("PM10", "PM2.5")
    # return		-	Element value
    # =============================================
    def gets(self, *elements):
        if len(elements) == 1 and isinstance(elements[0], list):
            return self._aircon.GetValues(elements[0], self._sender_address)
        else:
            return self._aircon.GetValues(list(elements), self._sender_address)

    # =============================================
    # Description	-   Set a value to SET
    # Parameter		-	element : Name of element
    #               ex) set("PM10", 100)
    # return		-	Element value
    # =============================================
    def set(self, name, value, force_send=True):
        if force_send:
            self._aircon.SetForceValue(self._address, self._sender_address, name, value, self._str_cmd, self._get_cmd)
        else:
            self._aircon.SetValue(self._address, self._sender_address, name, value, self._str_cmd, self._get_cmd)

    # =============================================
    # Description	-   Set values to SET
    # Parameter		-	element : Name of elements
    #               ex) sets("PM10", 100, "PM2.5", 30)
    # return		-	Element value
    # =============================================
    def sets(self, *args, **kargs):
        len_args = len(args)

        if len_args <= 1:
            Common.print_log("check the number of elements")
        else:
            force_send = kargs['force_send'] if 'force_send' in kargs.keys() else True
            if force_send:
                self._aircon.SetForceValues(list(args), self._address, self._sender_address,
                                            self._str_cmd, self._get_cmd)
            else:
                self._aircon.SetValues(list(args), self._address, self._sender_address,
                                       self._str_cmd, self._get_cmd)

    # =============================================
    # Description	-   Check whether the element is set successfully for timeout
    # Parameter		-	args : Name of elements, value element, 'timeout', time
    #               ex) compare_value("PM10", 100, "PM2.5", 30, 'timeout', 4)
    # return		-	true/false
    # =============================================
    def compare_value(self, *args):
        len_args = len(args)
        timeout = args[len_args-1] if "timeout" in args else 5
        len_args = len(args) - 2 if "timeout" in args else len_args
        print(timeout, len_args)

        if len_args % 2 == 0:
            for retry in range(0, 10):
                Common.print_log("[compare_value] [retry: %s] check whether the element is written successfully?"
                                 % (retry + 1))
                flag = True
                for i in range(0, len_args, 2):
                    element = args[i]
                    target = args[i + 1]
                    current = self.get(element)
                    Common.print_log("[compare_value] %s = Target(%s) : Current(%s)" % (element, target, current))
                    if target != current:
                        flag = False

                if flag:
                    return True
                #wait 1s to update value
                Common.wait(timeout)

            return False
        else:
            Common.print_log("[compare_value][Error] Check args again!")
            return False
