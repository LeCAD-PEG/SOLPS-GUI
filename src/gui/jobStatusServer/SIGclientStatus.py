#!/usr/bin/env python3

import socket
import sys
from datetime import datetime
from PyQt5.QtCore import pyqtSlot, Qt, QObject, pyqtSignal

"""
Class for storing client (job) status and various supporting methods
"""
class SIGclientStatus(QObject):
    # This defines a signal called 'jobStatusChanged' that takes one string (jobID) arguments.
    jobStatusChange = pyqtSignal(str, name='jobStatusChanged')
    
    def __init__(self):
        super(SIGclientStatus, self).__init__()
        # init values
        self.status = ''
        self.last_message = ''
        self.last_change = str(datetime.now())


    """
    Set client status and last message.
    """
    def setStatus(self, inStatus, inLastMessage):
        self.status = inStatus
        self.last_lessage = inLastMessage
        self.last_change = str(datetime.now())
        

    """
    Return client status as dict/
    """
    def getStatusDict(self):
        return {'status': self.status, 'last_message': self.last_message, 'last_change': self.last_change }
