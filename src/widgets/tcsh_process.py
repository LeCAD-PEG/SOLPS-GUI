"""Basic widget for SOLPS gui incorporating signals and a tcsh qprocess
"""
from PyQt5.QtCore import (QProcess, pyqtSignal, QSettings, pyqtSlot,
                          pyqtProperty)
from PyQt5.QtWidgets import QWidget

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
        self.tcshPath = settings.value("tcsh_path", '/bin/tcsh')
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
        msg = f'Process {self.program()} started.'
        logging.info(msg)
        self.prcStarted.emit(msg)

    @pyqtSlot(QProcess.ProcessState)
    def processStateChanged(self, newState):
        states = ['Not Running', 'Starting', 'Running']

        msg = f'Process {self.program()} state changed: {states[newState]}'
        logging.info(msg)
        self.prcStateChanged.emit(msg)

    @pyqtSlot(int, QProcess.ExitStatus)
    def finishedProcess(self, exitCode, exitStatus):
        exits = ['Normal exit', 'Crashed exit']
        msg = f'Process {self.program()} exited: {exits[exitStatus]}'
        self.prcFinished.emit(msg)

    @pyqtSlot(QProcess.ProcessError)
    def showError(self, error):
        """Writes an error to the widget in case that the process failed
            to start.
        """
        errors = ['Failed to Start', 'Crashed', 'Timed out', 'WriteError',
                  'ReadError', 'UnknownError']
        msg = f'ProcessError: {errors[error]}\n{self.errorString()}'
        logging.error(msg)
        self.prcError.emit(msg)

    def write(self, command):
        if self.state() == QProcess.NotRunning:
            msg = f'Process {self.program()} is not running!'
            logging.warning(msg)
            return

        msg = bytearray(command, 'utf-8')
        super(Tcsh, self).write(msg)

    def start(self):
        runDirSolpsTop = self.findSolpsTop(self.runDir)
        if not runDirSolpsTop:
            msg = 'Could not find readable SOLPSTOP for run.'
            logging.error(msg)
            return

        if runDirSolpsTop != self.solpsTop:
            self.kill()
            self.waitForFinished()
            self.solpsTop = runDirSolpsTop

        if self.state() != QProcess.NotRunning:
            logging.info(f'{self.program()} is already running!')
            return

        self.setProgram(self.tcshPath)
        self.setWorkingDirectory(self.solpsTop)
        self.setArguments(['-l'])
        super(Tcsh, self).start()

        if not self.waitForStarted():
            logging.error(f'{self.program()} not started.')
            return

        logging.info(f'TCSH started in {self.solpsTop}.')
        env = QSettings('ITER', 'solps-gui')
        device = env.value('device_environment', 'iter')
        compiler = env.value('compiler_environment', 'ifort64')
        cmd = f'setenv DEVICE {device}\n'
        cmd += f'source setup.csh {compiler}\necho TCSH READY\n'
        self.cwd = self.solpsTop
        self.write(cmd)

    def findSolpsTop(self, directory):
        """Searches for setup.csh or SOLPSTOP file in the directory hierarchy.

        Args:
            run_directory (str): run_directory

        Returns:
            solps_top(str): if found stup.csh or SOLPSTOP file. Else None
        """
        solpsTop = directory
        while(solpsTop):
            path = os.path.join(solpsTop, 'setup.csh')
            if os.path.exists(path) and os.access(path, os.R_OK):
                return solpsTop
            path = os.path.join(solpsTop, 'SOLPSTOP')
            if os.path.exists(path) and os.access(path, os.R_OK):
                with open(path) as file:
                    return file.readline()
            solpsTop = solpsTop.rsplit('/', 1)[0]
        logging.error(f'No SOLPSTOP found from {directory}. Are you sure that'
                      ' the run is inside of a solps-iter?')
        return None


class TcshProcess(QWidget):
    """QWidget for creating custom widgets that requires TCSH terminal for
    starting programs and starting scripts from SOLPS-ITER.

    Also because the widgets will be used as Qt's Designer plugins it is easier
    if they have a template to avoid creating a mess (i.e. with signals) in
    QDesigner.
    """
    def __init__(self, parent=None):
        """The important variables are:


        """
        super(TcshProcess, self).__init__(parent)

        self.runDir = None
        self.solpsTop = None
        settings = QSettings('ITER', 'solps-gui')
        self.tcshPath = settings.value("tcsh_path", '/bin/tcsh')
        self.tcshCommand = ''
        self.tcshCwd = ''
        self.tcsh = Tcsh(self)
        self.destroyed.connect(self.tcsh.close)
        self.activateDebugging()

    def activateDebugging(self):
        """Function that activates printing of all the output from the
        tcsh (TCSH terminal) variable.
        """
        self.tcsh.prcError.connect(self.debugError)
        self.tcsh.prcFinished.connect(self.debugState)
        self.tcsh.prcStarted.connect(self.debugState)
        self.tcsh.stdOutput.connect(self.debugStd)
        self.tcsh.stdErrOutput.connect(self.debugError)

    @pyqtSlot(str)
    def debugError(self, message):
        """Prints std error message. Used for debugging.
        """
        logging.info('Error: ' + message)

    @pyqtSlot(str)
    def debugState(self, message):
        """Prints QProcess state. Used for debugging.
        """
        logging.info('Changed State: ' + message)

    @pyqtSlot(str)
    def debugStd(self, message):
        """Prints std output message. Used for debugging.
        """
        logging.info('STD: ' + message)

    @pyqtSlot(str)
    def setRunDir(self, newVal):
        """Setter function for variable runDir.

        The main widget that passes the current run directory path is the
        widget Director.

        The directory should be inside a SOLPS-ITER project as it is necessary
        for starting the TCSH terminal with the correct SOLPS environment.

        Args:
            newVal (str): The new directory.
        """
        self.runDir = newVal

    def getRunDir(self):
        """Getter function for variable runDir.
        """
        return self.runDir

    run_dir = pyqtProperty(str, getRunDir, setRunDir)

    @pyqtSlot(str)
    def setTcshPath(self, tcshPath):
        """Setter for variable tcshPath.

        The path should be an absolute path i.e. /usr/bin/tcsh.

        Args:
            tcshPath (str): Absolute path to TCSH.
        """
        self.tcshPath = tcshPath

    def getTcshPath(self):
        """Getter for variable tcshPath.
        """
        return self.tcshPath

    tcsh_path = pyqtProperty(str, getTcshPath, setTcshPath)

    @pyqtSlot(str)
    def setTcshCommand(self, command):
        """Setter for variable tcshCommand.

        Args:
            command (command): Command for TCSH terminal.
        """
        self.tcshCommand = command

    def getTcshCommand(self):
        return self.tcshCommand

    tcsh_command = pyqtProperty(str, getTcshCommand, setTcshCommand)

    def startTcsh(self):
        """Starts the TCSH terminal by first setting the run directory variable
        runDir, so the correct SOLPS-ITER is used for setting the TCSH
        environment.

        You can run it as many times as you want, since it always check if it
        is running.
        """
        self.tcsh.setRunDir(self.runDir)
        self.tcsh.setTcshPath(self.getTcshPath())
        self.tcsh.start()

    @pyqtSlot()
    def executeTcshCommand(self):
        """Executes the TCSH command storred in variable tcshCommand by passing
        it to the TCSH terminal.

        It is not needed to first start TCSH with
        :meth:`TcshProcess.startTcsh` as it is run with
        :meth:`TcshProcess.executeTcshCommand`

        Examples:
            tcsh_process.setTcshCommand(command)
            tcsh_process.executeTcshCommnad()
            # is
            tcsh_process.setTcshCommand(command)

        """
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
