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
from operator import xor


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
                # wait 1s to update value
                Common.wait(timeout)

            return False
        else:
            Common.print_log("[compare_value][Error] Check args again!")
            return False

    # =============================================
    # Description	-   send data to SET
    # Parameter		-	data
    #               ex) send_raw_data("32F1000801018204301841001634")
    # return		-	none
    # =============================================
    def send_raw_data(self, data):
        self._aircon.SendRawData(data)

    # =============================================
    # Description	-   calculate check sum string data by xor operation
    # Parameter		-	data
    #               ex) check_sum_by_xor_operation("32F1000801018204301841001634")
    # return		-	2 end numbers of hexa
    # =============================================
    @staticmethod
    def check_sum_by_xor_operation(data):
        arr = []
        for i in range(0, len(data), 2):
            temp = "0x" + data[i] + data[i+1]
            integer_value = int(temp, 16)
            arr.append(integer_value)

        check_sum_xor = 0
        for x in arr:
            check_sum_xor = xor(check_sum_xor, x)

        hex_check_sum = hex(check_sum_xor).replace("0x", "")
        if len(hex_check_sum) == 1:
            hex_check_sum = "0" + hex_check_sum

        return hex_check_sum

    # =============================================
    # Description	-   inverse number
    # Parameter		-	data1, data2, data3, data4, data5
    #               ex) reversed_data("28", "08", "03", "81", "14")
    # return		-	inverse number
    # =============================================
    @staticmethod
    def reversed_data(data1, data2, data3, data4, data5):

        sd1 = str(data1)[::-1].zfill(2)
        sd2 = str(data2)[::-1].zfill(2)
        sd3 = str(data3)[::-1].zfill(2)
        sd4 = str(data4)[::-1].zfill(2)
        sd5 = str(data5)[::-1].zfill(2)
        ret = sd1 + sd2 + sd3 + sd4 + sd5
        # Common.print_log("%s" % ret)
        return ret

    # =============================================
    # Description	-   writing option remocon
    # Parameter		-	data1, data2, data3, data4, data5
    #               ex) send_option_data(28, 40, 03, 81, 14)
    # return		-	None
    # =============================================
    def send_option_data(self, data1, data2, data3, data4, data5):
        opt_sd = self.reversed_data(data1, data2, data3, data4, data5)
        xor_op = self.check_sum_by_xor_operation("F100080101"+opt_sd)
        opt_raw = "32F100080101" + opt_sd + "00" + xor_op + "34"
        Common.print_log("[send_option_data] %s" % opt_raw)
        self.send_raw_data(opt_raw)
        Common.wait(5)
        self.send_raw_data("32EE00DFAA000000000000009B34")