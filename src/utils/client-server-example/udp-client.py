#!/usr/bin/env python3


import socket
import sys

class SIGSendStatus():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def __init__(self, msg, inIPaddress, inPort):
        ipAddr = inIPaddress
        port = inPort
        
        # create dgram udp socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('Sending UDP message to', ipAddr, ':', port)
        sock.sendto(bytes(msg, 'utf-8'), (ipAddr, port))

if __name__ == '__main__':

    import sys
    msg = ''
    argc = len(sys.argv)

    if argc == 4:
        # all parameters given; send the message
        address = sys.argv[1]
        port = int(sys.argv[2])
        message = sys.argv[3]
        SIGSendStatus(message, address, port)
    else:
        # ask usr for message
        print("Example command line usage: python3 " + argv[0] +
              " 127.0.0.1 45100 test")

        while (msg != 'quit'):
            msg = input('Enter message to send to 127.0.0.1:45100')           
            SIGSendStatus(msg, '127.0.0.1', 45100)
 
    sys.exit()


