#!/usr/bin/env python

import socket
import sys

class Receiver():
    def __init__(self,inIPaddress, inPort):
        receive = True;
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind socket to local host and port
        try:
            sock.bind((inIPaddress, inPort))
            
        except socket.error: #, msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        print('Waiting on ', inIPaddress, ':', inPort)
            
        while receive:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            print( "received message: ", data.decode('utf-8'), " from ", addr)

            if data == 'quit':
                receive = False
 
if __name__ == '__main__':

    import sys

#    app = QApplication(sys.argv)
    receiver = Receiver('127.0.0.1', 45100)
#    receiver.show()
    sys.exit(receiver.exec_())


