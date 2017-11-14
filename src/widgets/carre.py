#!/usr/bin/env python3
""" A PyQt widget for Carre process.
"""

from PyQt5.QtWidgets import (QPlainTextEdit, QLineEdit, QVBoxLayout,
                             QInputDialog)
from PyQt5.QtCore import (pyqtSlot, pyqtSignal, QProcess, QSettings,
                          pyqtProperty, Qt)
from tcsh_process import tcshProcess


class Carre(tcshProcess):

    def __init__(self, parent=None):
        super(Carre, self).__init__(parent)

        # Creating QPlainTextEdit

        self.textDisplay = QPlainTextEdit()
        self.textDisplay.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.textDisplay)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.tcsh.prcStateChanged.connect(self.updateText)
        self.tcsh.prcFinished.connect(self.updateText)
        self.tcsh.prcError.connect(self.updateError)
        self.tcsh.stdOutput.connect(self.updateText)
        self.tcsh.stdErrOutput.connect(self.updateError)

    def setDeviceVar(self, device):
        self.device = device

    def getDeviceVar(self):
        return self.device

    Device = pyqtProperty(str, getDeviceVar, setDeviceVar)

    @pyqtSlot(str)
    def updateText(self, text):
        """Read the output given from carre, and when input is expected, spawn
        input dialogs to get input from the user and then pass it back to
        Carre.
        """
        self.textDisplay.appendPlainText(text)

        if 'http' in text:
            return
        if '?' in text:
            # Carre expects an input
            lines = text.splitlines()
            for line in lines:
                if '?' in line:
                    break

            userInput = QInputDialog.getText(self,
                                             "Carre input dialog",
                                             line)
            self.tcsh.write(userInput)





    @pyqtSlot(str)
    def updateError(self, text):
        color_pref = '<font color=red>'
        color_post = '</font>'
        self.textDisplay.appendHtml('<b>' + color_pref + text + color_post +
                                    '</b>')
        pass

    @pyqtSlot()
    def startCarre(self):
        pass


if __name__ == '__main__':

    import sys
    import os
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                                 QWidget)
    from PyQt5.QtCore import QRect

    app = QApplication(sys.argv)
    main = QMainWindow()
    carreM = Carre()
    carreM.activateDebugging()
    # carreM.activateDebugging()
    carreM.setTcshPath('/bin/tcsh')
    path = os.path.expanduser('~/solps-iter/runs/test_run/baserun')
    carreM.setRunDir(path)
    carreM.setTcshCommand('carre -')

    carrePush = QPushButton()
    carrePush.setText('Start Carre')
    carrePush.clicked.connect(carreM.executeTcshCommand)

    carreRunDir = QLineEdit('Set rundir')
    carreRunDir.textChanged.connect(carreM.setRunDir)
    carreRunDir.setText(path)



    layout = QVBoxLayout()
    layout.addWidget(carreM)
    layout.addWidget(carreRunDir)
    layout.addWidget(carrePush)

    window = QWidget()
    window.setLayout(layout)

    main.setCentralWidget(window)
    main.show()



    res = app.exec_()
    app.quit()
    sys.exit(res)
