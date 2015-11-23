#!/usr/bin/env python

import socket
import sys
import threading
from datetime import datetime

class SIGStatusServer():
    # wait for clients or not
    retrieve = True
    # dict for storing client's status
    clientsStatus = {}
    
    def __init__(self, inIPaddress, inPort):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind socket to local host and port
        try:
            sock.bind((inIPaddress, inPort))
            
        except socket.error: #, msg:
            print('Bind to '+ inIPaddress +':'+ str(inPort) +'failed.')
            sys.exit()

        print('Listening on ', inIPaddress, ':', inPort)
            
        while self.retrieve:
            # run until 
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            t1 = threading.Thread(target=SIGStatusServer.saveClientStatus,
                                  args=(SIGStatusServer, data, addr))
            t1.start()
            #print( "num active threads:", threading.active_count() )
            #print("1:", self.clientsStatus)

    """
        Save status from received data/string.
    """    
    def saveClientStatus(self, inData, inIPaddr):
        print( "received message: ", inData.decode('utf-8'), " from ", inIPaddr)
        # split data into 3 parts: jobID, status, message
        data = inData.decode('utf-8').split(";")
        #print(data)
        
        if len(data) >= 1 and data[0] == 'quit':
            # quit server
            self.stop(self)

        if len(data) == 3:
            # save data into 
            self.clientsStatus[data[0]] = {'status': data[1],
                                           'last_message': data[2],
                                           'last_change': str(datetime.now()) }
            print("Added status "+ data[1] + " from " + data[0]
                  + ". Cargo: " + data[2])
            #print("2:", self.clientsStatus)

    
    def getClientStatus(self, inClientID):
        """ Return status for client with given ID. If client is not in
        status dictionary, return {'status': 'unknown', 'last_message':
        'client ID not known', 'last_change': '' }
        """
        if inClientID in self.clientsStatus:
            # OK, given client ID exists in array; return status
            return self.clientsStatus[inClientID]
        else:
            # return default values for non-existing (unknown) clients
            return {'status': 'unknown', 'last_message':
                        'client ID not known', 'last_change': '' }
    
    
    def stop(self):
        """ Stop waiting for clients
        """
        self.retrieve = False
        print("E:", self.clientsStatus)
 
 
if __name__ == '__main__':

    # start server and start listening on all network interfaces     
    server = SIGStatusServer('0.0.0.0', 45100)
    sys.exit()


