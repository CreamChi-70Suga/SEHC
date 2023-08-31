#-*- coding: utf-8 -*-
# =============================================
# FILE		:	scc.py
# DESC		:	단일복합명령 전송
# AUTHOR	:	김동용
# VER		:	220113
# =============================================

import subprocess
import os
import time
import datetime
import serial
import re
import threading
from common import *

# import mgmt


class SerialComm():
    _stop_flag = False

    # =============================================
    # Description	-	SerialComm 클래스 생성자
    # Parameter		-	port : COM 포트
    #					password : root/TASH 비밀번호
    # return		-	X
    # =============================================
    def __init__(self, port, password):
        self._port = port
        self._password = password
        self._baudrate = 0  # Child에서 모듈에 따라 정의 필요

    # =============================================
    # Description	-	로그 저장할 폴더 생성
    # Parameter		-	X
    # return		-	X
    # =============================================
    def make_wifi_log_folder(self):
        par_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))  # ...\Director이 os.getcwd(), 그 상위에 폴더 생성
        par_path += "/06_Wifi_Log"

        if not os.path.exists(par_path):
            os.mkdir(par_path)

        self._folder_path = par_path + "/" + self._get_file_name()  # 현재 시간으로 만들기 때문에 중복될 일 없어서 폴더 존재 체크 필요없음
        os.mkdir(self._folder_path)

    # =============================================
    # Description	-	파일명 생성 후 반환
    # Parameter		-	X
    # return		-	name : 파일명
    # =============================================
    def _get_file_name(self):
        name = str(datetime.datetime.now())[:-7].replace(' ', '_')
        name = name.replace(':', '-')

        return name

    # =============================================
    # Description	-	시리얼포트 열기
    # Parameter		-	X
    # return		-	X
    # =============================================
    def open_serial_port(self):
        try:
            self._serial = serial.Serial(port=self._port, baudrate=self._baudrate, timeout=10)
        except Exception as e:
            print(e)
            Common.print_log('[open_serial_port] Serial port open failure')

    # =============================================
    # Description	-	시리얼포트 닫기
    # Parameter		-	X
    # return		-	X
    # =============================================
    def close_serial_port(self):
        try:
            self._serial.close()
        except Exception as e:
            print(e)
            Common.print_log('[close_serial_port] Serial port close failure')

    # =============================================
    # Description	-	Gửi dữ liệu tới cổng nối tiếp
    # Parameter		-	cmd : yêu cầu
    # return		-	X
    # =============================================
    def write_serial_port(self, cmd):
        time.sleep(1)
        print('[write_serial_port] %s' % cmd)
        self._serial.write((cmd + "\n").encode("utf-8"))

    # =============================================
    # Description	-	문자열에서 ANSI 값 제거
    # Parameter		-	words : 시리얼포트로부터 들어오는 데이터
    # return		-	정제된 데이터
    # =============================================
    def _delete_ansi_code(self, words):
        ansi_escape = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
        return ansi_escape.sub("", words)

    # =============================================
    # Description	-	Thread 돌면서 Log Buffer에 저장
    # Parameter		-	X
    # return		-	X
    # =============================================
    def _write_log_thread(self):
        self._buffer = ""
        t = threading.currentThread()

        start = time.time()

        while True:
            now = time.time()
            elapsed = int(now - start)
            if elapsed > 300:  # 비정상적인 종료로 flag 들어오지 않았을 때, 최대 300초까지만 쓰레드 돌고 정지
                break

            if t.stop == True:
                break

            try:
                log = self._serial.readline().decode("utf-8", errors="ignore")
                log = self._delete_ansi_code(log)
                self._buffer += "[" + str(datetime.datetime.now()) + "]" + log
            except:
                pass

        t.stop = True

    # =============================================
    # Description	-	Wifi Log 저장 시작
    # Parameter		-	X
    # return		-	X
    # =============================================
    def start_wifi_logging(self):
        self._serial.flushInput()
        self._serial.flushOutput()
        self._thread = threading.Thread(target=self._write_log_thread)
        self._thread.stop = False
        self._thread.setDaemon(True)
        self._thread.start()

        self._response_cnt = 0

    # =============================================
    # Description	-	Wifi Log 저장 종료
    # Parameter		-	X
    # return		-	X
    # =============================================
    def stop_wifi_logging(self):
        self._thread.stop = True

        time.sleep(15)  # Thread에서 아직 file write 하고 있을수도 있어서 딜레이 주고 파일 닫아야 함

        path = self._folder_path + "/TC" + "_" + self._get_file_name()

        try:
            p = path + ".log"
            self._file = open(p, mode="w")
        except Exception as e:
            print(e)
            Common.Stop('[stop_wifi_logging] File open failure')

        self._file.write(self._buffer)

        try:
            self._file.close()
        except Exception as e:
            print(e)
            Common.Stop('[close_wifi_log] File Close Failed')

        self._thread.join()


class TizenRT(SerialComm):
    _scube = {
        'power': {
            'on': {'cluster': 'fe12', 'id': '02', 'len': '01', 'value': '0f'},
            'off': {'cluster': 'fe12', 'id': '02', 'len': '01', 'value': 'f0'}
        },
        'mode': {
            'cool': {'cluster': 'fe12', 'id': '43', 'len': '01', 'value': '12'},
            'dry': {'cluster': 'fe12', 'id': '43', 'len': '01', 'value': '22'},
            'wind': {'cluster': 'fe12', 'id': '43', 'len': '01', 'value': '32'},
            'heat': {'cluster': 'fe12', 'id': '43', 'len': '01', 'value': '42'},
            'auto': {'cluster': 'fe12', 'id': '43', 'len': '01', 'value': 'e2'},
        },
        'temp': {
            '16': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '00a0'},
            '17': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '00aa'},
            '18': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '00b4'},
            '19': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '00be'},
            '20': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '00c8'},
            '21': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '00d2'},
            '22': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '00dc'},
            '23': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '00e6'},
            '24': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '00f0'},
            '25': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '00fa'},
            '26': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '0104'},
            '27': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '010e'},
            '28': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '0118'},
            '29': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '0122'},
            '30': {'cluster': 'fe12', 'id': '5b', 'len': '02', 'value': '012c'}
        },
        'windpower': {
            'auto': {'cluster': 'fe12', 'id': '62', 'len': '01', 'value': '00'},
            'low': {'cluster': 'fe12', 'id': '62', 'len': '01', 'value': '12'},
            'mid': {'cluster': 'fe12', 'id': '62', 'len': '01', 'value': '14'},
            'high': {'cluster': 'fe12', 'id': '62', 'len': '01', 'value': '16'},
            'turbo': {'cluster': 'fe12', 'id': '62', 'len': '01', 'value': '18'}
        },
        'conv': {
            'off': {'cluster': 'fe12', 'id': '44', 'len': '01', 'value': '12'},
            'speed': {'cluster': 'fe12', 'id': '44', 'len': '01', 'value': '22'},
            'smartsaver': {'cluster': 'fe12', 'id': '44', 'len': '01', 'value': '32'},
            'goodsleep': {'cluster': 'fe12', 'id': '44', 'len': '01', 'value': '42'},
            'silent': {'cluster': 'fe12', 'id': '44', 'len': '01', 'value': '52'},
            'nano': {'cluster': 'fe12', 'id': '44', 'len': '01', 'value': 'b2'},
            'nanosleep': {'cluster': 'fe12', 'id': '44', 'len': '01', 'value': 'c2'},
            'direct': {'cluster': 'fe12', 'id': '44', 'len': '01', 'value': 'e1'},
            'indirect': {'cluster': 'fe12', 'id': '44', 'len': '01', 'value': 'e2'}
        },
        'purify': {
            'on': {'cluster': 'fe12', 'id': '45', 'len': '01', 'value': '0f'},
            'off': {'cluster': 'fe12', 'id': '45', 'len': '01', 'value': 'f0'}
        },
        'ai': {
            'on': {'cluster': 'fe12', 'id': '65', 'len': '01', 'value': '0f'},
            'off': {'cluster': 'fe12', 'id': '65', 'len': '01', 'value': 'f0'}
        }
    }
    _baudrate = 115200

    # =============================================
    # Description	-	TizenRT 클래스 생성자
    # Parameter		-	port : COM 포트
    #					password : root/TASH 비밀번호
    # return		-	X
    # =============================================
    def __init__(self, port, password):
        self._com = None
        self._port = port
        self._password = password

    # =============================================
    # Description	-	로그 레벨 설정
    # Parameter		-	X
    # return		-	X
    # =============================================
    def set_log_level(self):
        self._com.input_password()
        self._com.write_serial_port('scube log 1')
        self._com.write_serial_port('setlog 7 6')

    # =============================================
    # Description	-	Wi-Fi 패스워드 입력
    # Parameter		-	X
    # return		-	X
    # =============================================
    def input_password(self):
        self.write_serial_port(self._password)

    # =============================================
    # Description	-	TizenRT 커맨드용 Cluster 변환
    # Parameter		-	c : 클러스터
    # return		-	변환된 클러스터
    # =============================================
    def _get_rt_cluster(self, c):
        t = (
        'fc01', 'fc94', 'fe12', 'fe13', 'fe14', 'fe15', 'fe16', 'fe17', 'fe20', 'fd12', 'fc03', 'fd13', 'fe82', 'fc9f')
        return str(t.index(c))

    # =============================================
    # Description	-	단일명령 전송
    # Parameter		-	attr : 항목
    #					value : 값
    # return		-	X
    # =============================================
    def send_single_command(self, attr, value):
        c = self._scube[attr][value]['cluster']
        i = self._scube[attr][value]['id']
        v = self._scube[attr][value]['value']
        m = '04'
        c = self._get_rt_cluster(c)

        cmd = 'scube 0 ' + '{0} {1} {2} {3}'.format(c, m, i, v)
        self._response_cnt += 1

        for i in range(0, 3):
            cnt = 0

            self._com.write_serial_port(cmd)

            for x in self._buffer.split('\n'):
                if (c + '05') in x:
                    res_data = x
                    cnt += 1

            if self._response_cnt == cnt:
                res_data = res_data.split('fe120501')[1]
                l = int(res_data[2:4])
                feedback = res_data[4: (4 + (l * 2))]

                return feedback
            else:
                print("[send_single_command] Failed to send single command, resend")

        Common.Stop("[send_single_command] Single command transmission failure")


class Tizen(SerialComm):
    _tizen_cmd = 'launch_app com.samsung.ac.hac-main cmdType scube device 0 target to data '
    _baudrate = 115200
    _response_cnt = 0

    # =============================================
    # Description	-	Tizen 클래스 생성자
    # Parameter		-	port : COM 포트
    #					password : root/TASH 비밀번호
    # return		-	X
    # =============================================
    def __init__(self, port, password):
        self._port = port
        self._password = password

    # =============================================
    # Description	-	로그 레벨 설정
    # Parameter		-	X
    # return		-	X
    # =============================================
    def set_log_level(self):
        self._com.input_password()

        self._com.write_serial_port('dlogutil -c')  # R18은 로그 입력 시 이전 로그까지 올라오기 때문에 클리어 필요
        self._com.write_serial_port('pkill dlogutil')
        self._com.write_serial_port('dlogutil hac-main ocfd.ses&')

    # =============================================
    # Description	-	Wi-Fi 패스워드 입력
    # Parameter		-	X
    # return		-	X
    # =============================================
    def input_password(self):
        self.write_serial_port("root")
        self.write_serial_port(self._password)

    # =============================================
    # Description	-	단일명령 전송
    # Parameter		-	attr : 항목
    #					value : 값
    # return		-	X
    # =============================================
    def send_single_command(self, attr, value):
        for key, val in d.items():
            if val == '-':
                continue

            c = self._env[key][val]['cluster']
            i = self._env[key][val]['id']
            l = self._env[key][val]['len']
            v = self._env[key][val]['value']
            m = '04'
            s = str(int(l) + 2).zfill(2)

            cmd = self._tizen_cmd + '{0}{1}{2}{3}{4}{5}'.format(c, m, s, i, l, v)

            time.sleep(5)
            self._com.write_serial_port(cmd)
