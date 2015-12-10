   #!/usr/bin/env python3
""" A PyQt custom TCSH widget.
"""

from PyQt5.QtCore import (QProcess, QSize, pyqtSignal, QSettings,
                          pyqtSlot, pyqtProperty)
from PyQt5.QtWidgets import QPlainTextEdit, QFrame

import logging
import os

class Tcsh(QPlainTextEdit):
    """ Tcsh(QWidget)
    
        Provides a custom widget to display a gnuplot with properties and slots
        that can be used to customize its appearance.
    """

    solpsTopChanged = pyqtSignal(str)
    runChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(Tcsh, self).__init__(parent)
        settings = QSettings('ITER', 'solps-gui')
        self.tcsh_path = settings.value("tcsh_path", '/bin/tcsh')
        self.solps_top = None
        self.rundir = None
        self.tcsh_command = None

        #self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumSize(QSize(180, 50))
        self.setPlaceholderText("TCSH widget for SOLPS")
        #self.setEnabled(False)

        self.tcsh = QProcess()
        self.tcsh.readyReadStandardOutput.connect(self.print_stdout)
        self.tcsh.readyReadStandardError.connect(self.print_stderr)

    def sizeHint(self):
        return QSize(320, 100)

    @pyqtSlot(QProcess.ProcessState)
    def stateChanged(self, newState):
        states = ['Not Running', 'Starting', 'Running']
        msg = 'Process state changed: ' + states[newState]
        print(msg)
        self.setText(msg)

    @pyqtSlot()
    def print_stdout(self):
        data = self.tcsh.readAll()
        text = bytearray(data).decode('utf8')
        self.appendPlainText(str(text))


    @pyqtSlot()
    def print_stderr(self):
        error_data=self.tcsh.readAllStandardError()
        error_text=bytearray(error_data).decode('utf8')
        self.appendHtml('<b>' + str(error_text) + '</b>')


    @pyqtSlot(QProcess.ProcessError)
    def show_error(self, error):
        """ Writes an error to the widget in case that the process failed
            to start.
        """
        errors = ['Failed to Start', 'Crashed', 'Timedout', 'WriteError',
            'ReadError', 'UnknownError']
        msg = 'ProcessError: ' + errors[error]
        print(msg)
        self.setText(msg)

    @pyqtSlot(int)
    def setTcshPath(self, tcsh_path):
        """ Executable requires absolute path. No ${PATH} possible!
        """
        self.tch_path = tcsh_path

    def getTcshPath(self):
        return self.tcsh_path

    tcshPath = pyqtProperty(str, getTcshPath, setTcshPath)

    @pyqtSlot(str)
    def setRundir(self, directory):
        """
        Args:
             directory (str): Absolute path to SOLPS directory with run data.

        """
        self.rundir = directory

    def getRundir(self):
        return self.rundir

    runDir = pyqtProperty(str, getRundir, setRundir)

    @pyqtSlot(str)
    def setTcshCommand(self, command):
        self.tcsh_command = command

    def get_tcsh_command(self):
        return self.tcsh_command

    tcshCommand = pyqtProperty(str, get_tcsh_command, setTcshCommand)

    def find_solps_top(self, directory):
        """ Searches for setup.csh or SOLPSTOP file in the directory hierarchy.
            Arguments:
                run_directory (str): run_directory
            Returns:
                solps_top(str): if found setup.csh or SOLPSTOP file. Else None
        """
        solps_top = directory

        while solps_top:
            path = solps_top + '/setup.csh'
            if os.path.exists(path):
                return solps_top
            path = solps_top + '/SOLPSTOP'
            if os.path.exists(path):
                with open(path) as file:
                    return file.readline()
            solps_top = solps_top.rsplit('/', 1)[0]
        return None

    @pyqtSlot()
    def executeTcshCommand(self):
        """ Opens TCSH login shell and runs SOLPS plot command
            previously defined and under the runsDir.

            TCSH environment is searched sourced from 'setup.csh' or pointed
            with SOLPSTOP file. SOLPSTOP is probed for runDir changes and
            if necessary resourced within a new shell.
        """
        rundir_solps_top = self.find_solps_top(self.rundir)
        if not rundir_solps_top:
            if not self.rundir:
                logging.error("Empty TCSH runDir! Bailing out.")
            else:
                logging.error("Could not find SOLPSTOP for " + self.rundir)
            return

        if rundir_solps_top != self.solps_top:  # we have new SOLPSTOP
            self.tcsh.kill()
            self.solps_top = rundir_solps_top

        cmd = ''
        if self.tcsh.state() != QProcess.Running:
            self.tcsh.setWorkingDirectory(self.solps_top)
            self.tcsh.start(self.tcsh_path, ['-l'])
            logging.info("TCSH started in " + self.solps_top)
            cmd +=  'cd ' + self.solps_top \
                    + '\nsource setup.csh\necho TCSH READY\n' \
                    + 'cd ' + self.rundir + '\n'

        if self.tcsh_command and self.rundir:
            cmd += self.tcsh_command + '\n'
            self.tcsh.write(bytearray(cmd, 'utf8'))
        else:
            logging.warning("Empty command or no run directory for TCSH")



if __name__ == "__main__":

    import sys, os
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    tcsh_widget = Tcsh()
    tcsh_widget.show()
    tcsh_widget.setRundir(os.path.expanduser("~")+
                          '/solps-iter/runs/AUG_16151_D/run1')
    tcsh_widget.setTcshCommand('ls')
    tcsh_widget.executeTcshCommand()
    tcsh_widget.setTcshCommand('ls -l')
    tcsh_widget.executeTcshCommand()
    sys.exit(app.exec_())
