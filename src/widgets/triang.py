#!/usr/bin/env python3
""" A PyQt widget for Triang process.
"""

from PyQt5.QtWidgets import (QPlainTextEdit, QVBoxLayout, QLabel, QGridLayout,
                             QInputDialog, QSpacerItem, QSizePolicy, QFrame,
                             QMessageBox, QPushButton)
from PyQt5.QtCore import pyqtSlot, QSettings
from PyQt5.QtGui import QTextCursor
from tcsh_process import TcshProcess
import logging
import os
import sys


class TriangState:
    notRunning, running = range(2)


class Triang(TcshProcess):

    def __init__(self, parent=None):
        super(Triang, self).__init__(parent)

        # Creating QPlainTextEdit

        self.textDisplay = QPlainTextEdit()
        self.textDisplay.setReadOnly(True)

        self.startTriangPush = QPushButton('Start Triang')
        self.startTriangPush.clicked.connect(self.startCarre)

        self.baserunLabel = QLabel(self.runDir)

        self.writeCommandPush = QPushButton('Write command')
        self.writeCommandPush.clicked.connect(self.manualInput)


        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.textDisplay, 0, 0, 1, -1)

        labelBaserun = QLabel('Baserun: ')
        labelBaserun.setFrameStyle(QFrame.Box | QFrame.Raised)

        layout.addWidget(self.startTriangPush, 1, 0)
        layout.addWidget(self.writeCommandPush, 1, 1)

        layout.addItem(QSpacerItem(20, 20, hPolicy=QSizePolicy.Expanding),
                       1, 2)

        layout.addWidget(labelBaserun, 1, 3)
        layout.addWidget(self.baserunLabel, 1, 4)
        layout.addItem(QSpacerItem(20, 20, ), 1, 5)



        self.setLayout(layout)

        self.tcsh.readyReadStandardOutput.connect(self.tcsh.readStdOut)
        settings = QSettings('ITER', 'solps-gui')
        self.tcsh.setTcshPath(settings.value('tcsh_path', '/usr/bin/tcsh'))
        self.tcsh.prcStateChanged.connect(self.updateText)
        self.tcsh.prcFinished.connect(self.updateText)
        self.tcsh.prcError.connect(self.updateError)
        self.tcsh.stdOutput.connect(self.updateText)
        self.tcsh.stdErrOutput.connect(self.updateError)

        self.currentRunDir = ''
        self.STATE = TriangState.notRunning

    @pyqtSlot()
    def manualInput(self):
        if not self.tcsh.state():
            return

        msg, ok = QInputDialog.getMultiLineText(self, 'Input dialog',
                                                'Command:')
        if ok:
            self.tcsh.write(msg + '\n')
            self.insertTextAtBottom(msg)

    def insertTextAtBottom(self, msg):
        self.textDisplay.moveCursor(QTextCursor.End)
        if msg.endswith('\n'):
            msg = msg[:-1]
        self.textDisplay.insertPlainText('\n' + msg)
        self.textDisplay.moveCursor(QTextCursor.End)

    # Overloaded
    @pyqtSlot(str)
    def setRunDir(self, runDir):
        if runDir:
            self.baserunLabel.setText(runDir)
        super(Triang, self).setRunDir(runDir)

    def processText(self, text):
        if 'http' in text:
            return
        if 'y/n' in text or 'y / n' in text:
            ok = QMessageBox.question(self,'Triang input dialog', text)
            if ok == QMessageBox.Yes:
                msg = 'y\n'
            else:
                msg = 'n\n'
            self.tcsh.write(msg)
            self.insertTextAtBottom(msg)
            return

        if 'Type \"end\" to stop.' in text:
            userInput, ok = QInputDialog.getMultiLineText(self, "Triang input "
                                                          "dialog", text)
            if ok:
                self.tcsh.write(userInput + '\n')
                self.insertTextAtBottom(userInput + '\n')
            return

        if '?' in text:
            # Carre expects an input
            ok = False
            userInput, ok = QInputDialog.getText(self,
                                                 "Triang input dialog",
                                                 text)
            if ok:
                # self.tcsh.write(userInput)
                self.tcsh.write(userInput + '\n')
                self.insertTextAtBottom(userInput)
                if userInput in 'qQquit':
                    self.STATE = TriangState.notRunning

    @pyqtSlot(str)
    def updateText(self, text):
        """Read the output given from carre, and when input is expected, spawn
        input dialogs to get input from the user and then pass it back to
        Carre.
        """
        self.insertTextAtBottom(text)
        # self.processText(text)  # Triang script outputs via StdError...

    @pyqtSlot(str)
    def updateError(self, text):
        # color_pref = '<font color=red>'
        # color_post = '</font>'
        # self.textDisplay.appendHtml('<b>' + color_pref + text + color_post +
        #                             '</b>')
        self.insertTextAtBottom(text)
        self.processText(text)

    @pyqtSlot()
    def startCarre(self):
        if not self.getRunDir():
            logging.error('No baserun selected.')
            return

        runDir = self.getRunDir()
        if self.getRunDir() != self.currentRunDir:
            msg = 'Baserun changed'
            if self.STATE == TriangState.running:
                msg += '. But current triang run hasn\'t finished yet!'
                logging.warning(msg)
                self.insertTextAtBottom(msg)
                return

            msg += '. Running triang in directory ' + self.currentRunDir + '.'
            logging.info(msg)
            self.currentRunDir = runDir

        if not self.tcsh.state():
            # Get DG model from combo box

            self.startTcsh()
            self.tcsh.waitForStarted()

            env = QSettings('ITER', 'solps-gui')
            device = env.value('device_environment', 'iter')
            cmd = 'setenv DEVICE ' + device + '\n'
            cmd += 'cd ' + runDir + '\n'
            self.tcsh.write(cmd)
        else:
            logging.info('TCSH for triang is aready running.')

        Triang = 'triang\n'
        cmd = Triang + '\n'
        # self.tcsh.write(cmd)
        self.tcsh.write(cmd)


if __name__ == '__main__':
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget)
    env = QSettings('ITER', 'solps-gui')
    env.setValue('device_environment', 'cmod')
    app = QApplication(sys.argv)
    main = QMainWindow()
    carreM = Triang()
    # carreM.activateDebugging()
    carreM.setTcshPath('/bin/tcsh')
    path = os.path.expanduser('~/solps-iter/runs/test_run/baserun')
    carreM.setRunDir(path)

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(carreM)

    window = QWidget()
    window.setLayout(layout)

    main.setCentralWidget(window)
    main.show()

    res = app.exec_()
    app.quit()
    sys.exit(res)
