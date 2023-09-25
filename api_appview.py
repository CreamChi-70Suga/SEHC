import time
from datetime import datetime
from common import *
from library import *


class UserAPIAppView(Common):

    # =============================================
    # Description - Init mobile instance
    # # Parameter -	mobile
    # # return		-	X
    # =============================================
    def __init__(self, mobile, outbug):
        self.mobile = mobile
        self.outbug = outbug

    # =============================================
    # Description - Get objects corresponding to attribute values
    # # Parameter -	attribute (text, index, resource-id,...)
    # #             ex)user_get_object(text='Air purifier')
    # #                user_get_object(text='Air purifier', index=1)
    # # return		-	all corresponding objects (list[dict])
    # =============================================
    def user_get_object(self, **kwargs):
        attribute = {}
        for key, value in kwargs.items():
            if key == "resource":
                attribute.update({'resource-id': value})
            elif key == "content-desc":
                attribute.update({'content-desc': value})
            else:
                attribute.update({key: value})  # update element

        try:
            attributes = self.mobile.GetObject(attribute, random=False, regex=False)
            self.print_log("[user_get_object] attributes: %s " % attributes)
            if attributes:
                return attributes
        except Exception:
            msg = ERROR_NOTIF + " Couldn't get object %s" % attribute
            self.Stop(msg)

    # =============================================
    # Description - Get text corresponding to attribute values
    # # Parameter -	attribute (index, resource-id,..)
    # #             ex) user_get_text(resource="com.sec.android.app.launcher:id/home_icon")
    # # return	  - txt(list)
    # =============================================
    def user_get_text(self, **kwargs):
        attributes = self.user_get_object(**kwargs)
        # create a list txt has the same attribute value
        list_txt = []
        if attributes:
            for x in attributes:
                txt = x['text']
                list_txt.append(txt)
            self.print_log("[user_get_text] list_txt: %s " % list_txt)
            return list_txt
        else:
            self.print_log("[user_get_text] Couldn't find the element {%s}." % kwargs)
            self.Stop(ERROR_NOTIF)

    # =============================================
    # Description - Get bounds corresponding to attribute values
    # # Parameter -	attribute (index, resource-id,..)
    # #             ex)user_get_bounds(resource="com.sec.android.app.launcher:id/home_icon")
    # # return	  - bounds(x1,y1,x2,y2)(list)
    # =============================================
    def user_get_bounds(self, **kwargs):
        attributes = self.user_get_object(**kwargs)
        # create a list bounds has the same attribute value
        if attributes:
            list_bounds = []
            for x in attributes:
                bounds = x['bounds']
                list_bounds.append(bounds)
            self.print_log("[user_get_bounds] list_bounds: %s " % list_bounds)
            return list_bounds
        else:
            self.print_log("[user_get_bounds] Couldn't find the element.")
            self.Stop(ERROR_NOTIF)
    # =============================================
    # Description - Get bounds corresponding to attribute values
    # # Parameter -	attribute (index, resource-id,..)
    # #             ex)user_get_pointcenter(resource="com.sec.android.app.launcher:id/home_icon")
    # # return	  - point-center(x,y)(list)
    # =============================================
    def user_get_pointcenter(self, **kwargs):
        attributes = self.user_get_object(**kwargs)
        # create a list of point center has the same attribute value
        if attributes:
            list_pointcenter = []
            for x in attributes:
                pointcenter = x['point-center']
                list_pointcenter.append(pointcenter)
            self.print_log("[user_get_pointcenter] list_pointcenter: %s " % list_pointcenter)
            return list_pointcenter
        else:
            self.print_log("[user_get_pointcenter] Couldn't find the element.")
            self.Stop(ERROR_NOTIF)
    # =============================================
    # Description - Get coordinates(X,Y) corresponding to attribute values
    # # Parameter -	attribute (index, resource-id,..)
    # #             ex)
    # # return	  - coordinates(X, Y) (list)
    # =============================================
    def user_get_XY(self, **kwargs):
        attributes = self.user_get_object(**kwargs)
        if attributes:
            coordinate = attributes[0]['point-center']
            X = coordinate[0]
            Y = coordinate[1]
            self.print_log("[user_get_XY] X: %s, Y: %s" % (X, Y))
            return X, Y
        else:
            self.print_log("[user_get_XY] Couldn't find the element.")
            self.Stop(ERROR_NOTIF)

    # =============================================
    # Description - Click to object corresponding to attribute values
    # # Parameter -	attribute (index, resource-id,..)
    # #             ex)
    # # return	  -
    # =============================================
    def user_touch_object(self, **kwargs):
        attribute = {}
        for key, value in kwargs.items():
            if key == "resource":
                attribute.update({'resource-id': value})
            elif key == "content-desc":
                attribute.update({'content-desc': value})
            else:
                attribute.update({key: value})  # update element
        try:
            self.mobile.TouchObject(attribute, random = False, regex = False)
        except Exception:
            self.print_log("[user_touch_object] Couldn't touch the element.")
            self.Stop(ERROR_NOTIF)

    # =============================================
    # Description - Long Click to object corresponding to attribute values
    # # Parameter -	attribute (duration, index, resource-id,..)
    # #             ex)user_long_touch_object(text="SmartThings", duration=5)
    # # return	  - None
    # =============================================
    def user_long_touch_object(self, **kwargs):
        attribute = {}
        duration = 2
        for key, value in kwargs.items():
            if key == "resource":
                attribute.update({'resource-id': value})
            elif key == "content":
                attribute.update({'content-desc': value})
            elif key == "duration":
                duration = value
            else:
                attribute.update({key: value})  # update element
        try:
            self.mobile.TouchObject(attribute, duration, random=False, regex=False)
        except Exception:
            self.print_log("[user_long_touch_object] Couldn't touch the element.")
            self.Stop(ERROR_NOTIF)

    # =============================================
    # Description - Enter text to box
    # # Parameter -	txt
    # #             ex)user_input_text('12345')
    # # return	  - None
    # =============================================
    def user_input_text(self, txt):
        self.print_log("[user_input_text] %s " % txt)
        try:
            self.mobile.InputText(txt)
            self.wait(2)
            self.print_log("[user_input_text] Input text '%s' complete." % txt)
        except Exception:
            self.print_log("[user_input_text] Couldn't write txt {%s}." % txt)
            self.Stop(ERROR_NOTIF)

    # =============================================
    # Description - check if text is exits
    # # Parameter -	txt
    # #             ex)user_text_exits('12345')
    # # return	  - True/False
    # =============================================
    def user_text_exits(self, txt):
        try:
            result = self.mobile.HasTextAND(txt)
            if result:
                self.print_log("[user_text_exits] Found text '%s'." % txt)
                return True
            else:
                self.print_log("[user_text_exits] Text '%s' is not exist." % txt)
                return False
        except Exception:
            self.print_log("[user_text_exits] Wrong format." % txt)
            self.Stop(ERROR_NOTIF)

    # =============================================
    # Description - Wait for text occur in time out
    # # Parameter -	txt
    # #             ex)user_wait_text_occur('12345')
    # # return	  - True/False
    # =============================================
    def user_wait_text_occur(self, txt, timeout):
        cnt = 0
        while self.user_text_exits(txt) is not True:
            cnt += 1
            self.wait(1)
            if cnt > timeout:
                self.print_log("[user_wait_text_occur] TIME OUT: '%s'" % txt)
                return False
        return True
    # =============================================
    # Description - Swipe up and down until text is found
    # # Parameter - txt
    # #             ex)user_swipe_to_find_text('12345')
    # # return	  - True/False
    # =============================================
    def user_swipe_to_find_text(self, txt):
        for roll in range(2):
            for swipe in range(6):
                txt_object = self.user_get_object(text=txt)
                if not txt_object and roll == 0:
                    self.user_swipe_up()
                elif not txt_object and roll == 1:
                    self.user_swipe_down()
                else:
                    self.print_log("[user_swipe_to_find_text] Found text '%s'." % txt)
                    return True

    # =============================================
    # Description - Swipe up on current page
    # # Parameter -	X
    # # return	  - None
    # =============================================
    def user_swipe_up(self):
        self.mobile.Swipe(swipe_up_bound[0], swipe_up_bound[1], swipe_up_bound[2], swipe_up_bound[3], swipe_up_bound[4])
        self.print_log("[swipe_up] Swipe up")

    # =============================================
    # Description - Swipe down on current page
    # # Parameter -	X
    # # return	  - None
    # =============================================
    def user_swipe_down(self):
        self.mobile.Swipe(swipe_down_bound[0], swipe_down_bound[1], swipe_down_bound[2], swipe_down_bound[3], swipe_down_bound[4])
        self.print_log("[swipe_down] Swipe down")

























