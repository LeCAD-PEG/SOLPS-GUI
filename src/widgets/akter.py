"""Basic widget for SOLPS gui incorporating signals and a tcsh qprocess
"""
from PyQt5.QtCore import (QProcess, QSize, pyqtSignal, QSettings,
                          pyqtSlot, pyqtProperty, QObject)
from PyQt5.QtWidgets import QPlainTextEdit, QFrame, QWidget
from PyQt5.QtGui import QFont

import logging
import os

class Tcsh(QProcess):
    """A wrapper encompassing QProcess, which starts a TCSH session. The
    session starts with sourcing **SOLPSTOP/setup.csh**.

    The main purpose is to run SOLPS-ITER process commands (Divgeo, Carre,
    gnuplot post-processing commands, etc...) in run directories.

    For maximum control over starting processes, module logging is used to
    send important and informative messages to the SOLPS-GUI log viewer. Other
    processes also require input from the user so additional signals are
    created so that classes inheriting **tcsh** will be able to process and
    write user input back to the TCSH session.
    """

    stdOutput = pyqtSignal(str)
    stdErrOutput = pyqtSignal(str)
    prcStateChanged = pyqtSignal(str)
    prcStarted = pyqtSignal(str)
    prcError = pyqtSignal(str)
    prcFinished = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Tcsh, self).__init__(parent)
        settings = QSettings('ITER', 'solps-gui')
        self.tcshPath = settings.value("tcsh_path", '/bin/path')
        self.solpsTop = None
        self.runDir = None
        self.cwd = None

        self.command = None

        self.started.connect(self.processStarted)
        self.stateChanged.connect(self.processStateChanged)
        self.finished.connect(self.finishedProcess)
        self.error.connect(self.showError)
        self.readyReadStandardError.connect(self.readStdErr)
        self.readyReadStandardOutput.connect(self.readStdOut)

    def setRunDir(self, directory):
        self.runDir = directory

    @pyqtSlot(str)
    def setTcshPath(self, path):
        self.tcshPath = path

    @pyqtSlot()
    def readStdOut(self):
        data = self.readAllStandardOutput()
        text = str(bytearray(data).decode('utf8'))
        self.stdOutput.emit(text)

    @pyqtSlot()
    def readStdErr(self):
        data = self.readAllStandardError()
        text = str(bytearray(data).decode('utf8'))
        self.stdErrOutput.emit(text)

    @pyqtSlot()
    def processStarted(self):
        msg = "Process " + self.program() + " started."
        logging.info(msg)
        self.prcStarted.emit(msg)

    @pyqtSlot(QProcess.ProcessState)
    def processStateChanged(self, newState):
        states = ['Not Running', 'Starting', 'Running']
        msg = 'Process ' + self.program() + ' state changed: ' + \
            states[newState]
        logging.info(msg)
        self.prcStateChanged.emit(msg)

    @pyqtSlot(int, QProcess.ExitStatus)
    def finishedProcess(self, exitCode, exitStatus):
        exits = ["Normal exit", "Crashed exit"]
        msg = 'Process ' + self.program() + ' exited: ' + exits[exitStatus]
        self.prcFinished.emit(msg)

    @pyqtSlot(QProcess.ProcessError)
    def showError(self, error):
        """ Writes an error to the widget in case that the process failed
            to start.
        """
        errors = ['Failed to Start', 'Crashed', 'Timed out', 'WriteError',
                  'ReadError', 'UnknownError']
        msg = 'ProcessError: ' + errors[error] + '\n' + self.errorString()
        logging.error(msg)
        self.prcError.emit(msg)

    def write(self, command):
        if self.state() == QProcess.NotRunning:
            msg = 'Process ' + self.program() + ' is not running!'
            logging.warning(msg)
            return

        msg = bytearray(command, 'utf-8')
        super(Tcsh, self).write(msg)

    def start(self):
        runDirSolpsTop = self.findSolpsTop(self.runDir)
        if not runDirSolpsTop:
            msg = "Could not find readable SOLPSTOP for run."
            logging.error(msg)
            return

        if runDirSolpsTop != self.solpsTop:
            self.kill()
            self.waitForFinished()
            self.solpsTop = runDirSolpsTop

        if self.state() != QProcess.NotRunning:
            logging.info(self.program() + " is already running!")
            return

        self.setArguments(['-l'])
        self.setProgram(self.tcshPath)
        super(Tcsh, self).start()

        if not self.waitForStarted():
            logging.error(self.program() + "not started.")
            return

        logging.info("TCSH started in " + self.solpsTop + ".")
        cmd = "cd " + self.solpsTop + '\nsource setup.csh\necho TCSH READY\n'
        self.cwd = self.solpsTop
        self.write(cmd)

    def findSolpsTop(self, directory):
        """ Searches for setup.csh or SOLPSTOP file in the directory hierarchy.
        Arguments:
            run_directory (str): run_directory

        Returns:
            solps_top(str): if found stup.csh or SOLPSTOP file. Else None
        """
        solpsTop = directory

        while(solpsTop):
            path = solpsTop + '/setup.csh'
            if os.path.exists(path) and os.access(path, os.R_OK):
                return solpsTop
            path = solpsTop + '/SOLPSTOP'
            if os.path.exists(path) and os.access(path, os.R_OK):
                with open(path) as file:
                    return file.readline()
            solpsTop = solpsTop.rsplit('/', 1)[0]
        return None


class Akter(QWidget):
    def __init__(self, parent=None):
        super(Akter, self).__init__(parent)

        self.runDir = None
        self.solpsTop = None

        self.tcshPath = None
        self.tcshCommand = ''
        self.tcshCwd = ''
        self.tcsh = Tcsh(self)

    @pyqtSlot(str)
    def setRunDir(self, newVal):
        self.runDir = newVal

    def getRunDir(self):
        return self.runDir

    run_dir = pyqtProperty(str, getRunDir, setRunDir)

    @pyqtSlot(str)
    def setTcshPath(self, tcshPath):
        self.tcshPath = tcshPath

    def getTcshPath(self):
        return self.tcshPath

    tcsh_path = pyqtProperty(str, getTcshPath, setTcshPath)

    @pyqtSlot(str)
    def setTcshCommand(self, command):
        self.tcshCommand = command

    def getTcshCommand(self):
        return self.tcshCommand

    tcsh_command = pyqtProperty(str, getTcshCommand, setTcshCommand)

    def startTcsh(self):
        self.tcsh.setRunDir(self.runDir)
        self.tcsh.setTcshPath(self.tcshPath)
        self.tcsh.start()

    @pyqtSlot()
    def executeTcshCommand(self):
        self.startTcsh()
        self.tcshCwd = self.tcsh.cwd

        if self.runDir:
            cmd = ''
            if self.runDir != self.tcshCwd:
                self.pwd = self.runDir
                cmd += 'cd ' + self.runDir + '\n'

            if self.tcshCommand:
                cmd += self.tcshCommand + '\n'
            else:
                logging.warning("Empty command for TCSH")
            self.tcsh.write(cmd)
        else:
            logging.warning("No run directory for TCSH")

    @pyqtSlot(str)
    def setTcshCommand(self, command):
        self.tcshCommand = command
