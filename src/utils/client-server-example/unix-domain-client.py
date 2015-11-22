# -*- coding: utf-8 -*-
import socket
import os
 
print("Connecting...")
if os.path.exists(os.path.expanduser("~/.python_unix_sockets_example")):
  client = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
  client.connect(os.path.expanduser("~/.python_unix_sockets_example"))
  print("Ready.")
  print("Ctrl-C to quit.")
  print("Sending 'DONE' shuts down the server and quits.")
  while True:
    try:
      x = input( "> " )
      if "" != x:
        print("SEND:", x)
        client.send(bytes(x, 'utf-8'))
        if "DONE" == x:
          print("Shutting down.")
          break
    except KeyboardInterrupt as k:
      print("Shutting down.")
  client.close()
else:
  print("Couldn't Connect!")
print("Done")
