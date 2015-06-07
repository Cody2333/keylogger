# -*- coding: utf-8 -*-
import socket
import time  
# Ŀ���ַIP/URL���˿�
target_host = "59.78.26.99"
target_port = 8080
  
# ����һ��socket����
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  
# ��������
client.connect((target_host,target_port))
  
# �������
client.send("GET / HTTP/1.1\r\nHOST:127.0.0.1\r\n\r\n")
for i in range(10):
    time.sleep(1.5)
    client.send("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")  
# ������Ӧ
#response = client.recv(4096)
  
#print response