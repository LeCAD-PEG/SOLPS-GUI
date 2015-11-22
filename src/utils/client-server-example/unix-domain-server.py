# -*- coding: utf-8 -*-
import socket
import os
import time
 
if os.path.exists(os.path.expanduser("~/.python_unix_sockets_example")):
  os.remove(os.path.expanduser("~/.python_unix_sockets_example"))
 
print("Opening socket...")
server = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
server.bind(os.path.expanduser("~/.python_unix_sockets_example"))
 
print("Listening...")
while True:
  datagram = server.recv( 1024 )
  if not datagram:
    break
  else:
    print("-" * 20)
    print(datagram.decode('utf-8'))
    if "DONE" == datagram.decode('utf-8'):
      break
print("-" * 20)
print("Shutting down...")
server.close()
os.remove(os.path.expanduser("~/.python_unix_sockets_example"))
print("Done")
