#!/usr/bin/env python3
""" A PyQt widget for Carre process.
"""

from PyQt5.QtWidgets import QPlainTextEdit, QLineEdit, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QProcess, QSettings
import logging

from akter import Akter

class Carre(Akter):

    def __init__(self, parent=None):
        super(Carre, self).__init__(parent)

        # Creating QPlainTextEdit

        self.textDisplay = QPlainTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.textDisplay)
        self.setLayout(layout)

        self.tcsh.stdOutput.connect(self.readStdOutput)
        self.tcsh.stdErrOutput.connect(self.readStdErrOutput)

    @pyqtSlot()
    def startCarre(self):
        """Start tcsh in the set rundir and then run Carre.
        """
        if not self.runDir:
            logging.error("No run directory set!")
            return

        self.startTcsh()
        cmd = "cd " + self.runDir + "\n"
        cmd += "carre -"
        self.write(cmd)

    @pyqtSlot(str)
    def readStdOutput(self, text):
        """Read the output given from carre, and when input is expected, spawn
        input dialogs to get input from the user and then pass it back to
        Carre.
        """
        pass

    @pyqtSlot(str)
    def readStdErrOutput(self, text):
        pass
