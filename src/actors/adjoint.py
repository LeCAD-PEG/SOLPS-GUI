#!/usr/bin/env python3

from PySide6.QtCore import Slot, QProcess
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (QGridLayout, QGroupBox, QPushButton, QPlainTextEdit,
                                QVBoxLayout, QSpacerItem, QSizePolicy, QInputDialog, QLabel, QMessageBox,)

from tcsh_process import TcshProcess
import os


class AdjointActor(TcshProcess):
    icon = ''

    def __init__(self, parent=None):
        super().__init__(parent)

        self.prepareUserInterface()

        self.tcsh.stdOutput.connect(self.updateText)
        self.tcsh.stdErrOutput.connect(self.updateText)
        self.tcsh.prcStateChanged.connect(self.showProcessState)
        self.tcsh.prcError.connect(self.showProcessState)

    def prepareUserInterface(self):
        mainLayout = QGridLayout(self)

        commandBox = QGroupBox('Commands', self)
        commandLayout = QVBoxLayout(commandBox)

        self.compileButton = QPushButton('Compile adjoint', commandBox)
        self.compileButton.clicked.connect(self.compileAdjoint)
        commandLayout.addWidget(self.compileButton)

        self.runButton = QPushButton('Run adjoint', commandBox)
        self.runButton.clicked.connect(self.runAdjoint)
        commandLayout.addWidget(self.runButton)

        self.removePrtButton = QPushButton('rm b2mn.prt', commandBox)
        self.removePrtButton.clicked.connect(self.removeB2mnPrt)
        commandLayout.addWidget(self.removePrtButton)

        self.stopButton = QPushButton('Stop run', commandBox)
        self.stopButton.clicked.connect(self.stopRun)
        commandLayout.addWidget(self.stopButton)
        
        commandLayout.addItem(
            QSpacerItem(
                20,
                20,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            )
        )

        logBox = QGroupBox('Log window', self)
        logLayout = QGridLayout(logBox)

        self.textDisplay = QPlainTextEdit(logBox)
        self.textDisplay.setReadOnly(True)
        self.textDisplay.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.textDisplay.setPlaceholderText(
            'SOLPS B25 adjoint output will appear here.'
        )
        logLayout.addWidget(self.textDisplay, 0, 0, 1, 2)

        self.manualButton = QPushButton('Terminal input', logBox)
        self.manualButton.clicked.connect(self.manualInput)
        logLayout.addWidget(self.manualButton, 1, 0)

        self.clearButton = QPushButton('Clear log', logBox)
        self.clearButton.clicked.connect(self.clearLog)
        logLayout.addWidget(self.clearButton, 1, 1)

        mainLayout.addWidget(commandBox, 0, 0)
        mainLayout.addWidget(logBox, 0, 1)
        mainLayout.setColumnStretch(1, 1)

    @Slot(str)
    def setRunDir(self, rundir):
        self.runDir = rundir
        self.textDisplay.appendPlainText(f'Selected run directory:  {rundir}')

    def _ensureTcshReady(self):
        if not self.runDir:
            self.textDisplay.appendPlainText('No run directory selected.')
            return False

        self.tcsh.setRunDir(self.runDir)
        self.tcsh.setTcshPath(self.getTcshPath())

        if self.tcsh.state() == QProcess.ProcessState.NotRunning:
            self.tcsh.start()

        return self.tcsh.state() != QProcess.ProcessState.NotRunning

    def _executeCommand(self, command: str):
        if not self._ensureTcshReady():
            self.textDisplay.appendPlainText('Failed to start tcsh process.')
            return

        self.textDisplay.appendPlainText(f'$ {command}')
        if self.runDir != self.tcsh.cwd:
            self.tcsh.write(f'cd {self.runDir}\n')
        self.tcsh.write(command + '\n')

    @Slot()
    def compileAdjoint(self):
        self._executeCommand('gmake b25adj')

    @Slot()
    def runAdjoint(self):
        self._executeCommand('b2run -adj b2mn')

    @Slot()
    def stopRun(self):
        if self.tcsh.state() != QProcess.ProcessState.NotRunning:
            self.textDisplay.appendPlainText('$ kill current process')
        self.tcsh.close_process()

    @Slot()
    def removeB2mnPrt(self):
        self._executeCommand('rm b2mn.prt')

    @Slot()
    def clearLog(self):
        self.textDisplay.clear()
        
    def appendOutput(self, text):
        """Append external output text to the actor log window."""
        self.textDisplay.appendPlainText(text.rstrip())

    def clearOutput(self):
        """Clear external output text from the actor log window."""
        self.textDisplay.clear()

    @Slot()
    def manualInput(self):
        if not self._ensureTcshReady():
            return

        text, ok = QInputDialog.getText(self, 'Terminal input', 'Command:')
        if ok and text.strip():
            command = text.strip()
            self.textDisplay.appendPlainText(f'$ {command}')
            self.tcsh.write(command + '\n')

    @Slot(str)
    def updateText(self, text):
        if not text:
            return
        filtered = '\n'.join(
            line for line in text.splitlines()
            if 'no access to tty' not in line
            and 'Inappropriate ioctl for device' not in line
            and 'Thus no job control in this shell' not in line
        )
        if not filtered.strip():
            return
        cursor = self.textDisplay.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.textDisplay.setTextCursor(cursor)
        self.textDisplay.insertPlainText(filtered + '\n' if not filtered.endswith('\n') else filtered)
        self.textDisplay.ensureCursorVisible()

    @Slot(str)
    def showProcessState(self, message):
        if message:
            self.textDisplay.appendPlainText(message)

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = AdjointActor()
    widget.resize(531, 821)
    widget.show()
    sys.exit(app.exec())