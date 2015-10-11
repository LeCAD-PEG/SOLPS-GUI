#!/usr/bin/env python3


import socket
import sys

class SIGSendStatus():
#    ipAddr = ''
#    port = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def __init__(self, msg, inIPaddress, inPort):
        ipAddr = inIPaddress
        port = inPort
        
        # create dgram udp socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('Connected to ', ipAddr, ':', port)
        sock.sendto(bytes(msg, 'utf-8'), (ipAddr, port))

if __name__ == '__main__':

    import sys
    msg = ''
    num = len(sys.argv)
    print("num: ", num)

    if num >= 4:
        # all parameters given; send the message
        SIGSendStatus(sys.argv[num-3], sys.argv[num-2], int(sys.argv[num-1]))
    else:
        # ask usr for message
        while (msg != 'quit'):
            msg = input('Enter message to send :')           
            SIGSendStatus(msg, '127.0.0.1', 45100)
 
    sys.exit()


