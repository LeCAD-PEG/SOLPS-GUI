#!/usr/bin/env python3
""" A PyQt custom TCSH widget.
"""

from PyQt5.QtCore import (QProcess, QSize, pyqtSignal, QSettings,
                          pyqtSlot, pyqtProperty)
from PyQt5.QtWidgets import QPlainTextEdit, QFrame, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont

import logging
import os

from akter import Akter

class TcshEdit(Akter):
    """ Tcsh(QWidget)

        Provides a custom widget to display TCSH with properties and slots
        that can be used to customize its appearance.
    """

    solpsTopChanged = pyqtSignal(str)
    runChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TcshEdit, self).__init__(parent)
        settings = QSettings('ITER', 'solps-gui')
        self.tcsh_path = settings.value('tcsh_path', '/bin/tcsh')
        self.plainTextEdit = QPlainTextEdit(parent)
        layout = QVBoxLayout()
        layout.addWidget(self.plainTextEdit)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        #self.setAlignment(Qt.AlignCenter)
        self.plainTextEdit.setFrameStyle(QFrame.StyledPanel)
        self.plainTextEdit.setMinimumSize(QSize(180, 50))
        self.plainTextEdit.setPlaceholderText("TCSH widget for SOLPS")
        font = QFont()
        font.setFamily('Monospace')
        self.plainTextEdit.setFont(font)

        self.tcsh.stdOutput.connect(self.updateText)
        self.tcsh.stdErrOutput.connect(self.showError)
        self.tcsh.prcStateChanged.connect(self.updateText)
        self.tcsh.setTcshPath(self.tcsh_path)

    def sizeHint(self):
        return QSize(320, 100)

    @pyqtSlot(str)
    def setAndExecuteTcshCommand(self, command):
        """ Immediately executes provided command in TCSH.
        """
        self.tcshCommand = command
        self.executeTcshCommand()

    @pyqtSlot(str)
    def updateText(self, msg):
        self.plainTextEdit.appendPlainText(msg)

    @pyqtSlot(str)
    def showError(self, msg):
        self.plainTextEdit.appendHtml('<b>' + msg + '</b>')


if __name__ == "__main__":

    import sys
    from PyQt5.QtWidgets import QApplication

    logging.getLogger().setLevel(logging.DEBUG)
    layout = QVBoxLayout()
    app = QApplication(sys.argv)
    tcsh_widget = TcshEdit()
    tcsh_widget.activateDebugging()

    tcsh_widget.show()
    tcsh_widget.setTcshPath('/bin/tcsh')
    tcsh_widget.setRunDir(os.path.expanduser("~") +
                          '/solps-iter/runs/examples/AUG_16151_D+C+He')
    tcsh_widget.setTcshCommand('ls')
    tcsh_widget.executeTcshCommand()
    tcsh_widget.setTcshCommand('ls -l')
    tcsh_widget.executeTcshCommand()

    sys.exit(app.exec_())
