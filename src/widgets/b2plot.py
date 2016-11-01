#!/usr/bin/env python3
""" A PyQt custom B2plot widget for Qt Designer.
"""

from PyQt5.QtCore import (Qt, QProcess, QProcessEnvironment, QSize, pyqtSignal,
                          QSettings, pyqtSlot, pyqtProperty)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QFrame


import logging
import os
import tempfile

class B2plot(QLabel):
    """ B2plot(QWidget)
    
        Provides a custom widget to display a b2plot with properties and slots
        that can be used to customize its appearance.

        Emits *convertFinished()* when b2plot conversion is finished
        and it is safe to start another B2plot widget in a chain to the
        *executeB2plotCommand()*.
    """

    stderrOutput = pyqtSignal(str)

    convertFinished = pyqtSignal()
    
    def __init__(self, parent=None):
        super(B2plot, self).__init__(parent)
        settings = QSettings('ITER', 'solps-gui')
        self.tcsh_path = settings.value('tcsh_path', '/bin/tcsh')
        self.convert_path = settings.value('convert_path', '/usr/bin/convert')
        self.solps_top = None
        self.solps_top_changed = False
        self.rundir = None
        self.b2plot_command = None

        self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumSize(QSize(180, 100))
        self.setText("B2plot widget for SOLPS")

        self.convert = QProcess()
        self.tcsh = QProcess()

        self.convert.finished.connect(self.show_plot)
        self.convert.error.connect(self.show_error)
        self.tcsh.readyReadStandardOutput.connect(self.read_tcsh_stdout)
        self.tcsh.readyReadStandardError.connect(self.print_tcsh_stderr)

    def sizeHint(self):
        return QSize(320, 200)

    @pyqtSlot(QProcess.ProcessError)
    def show_error(self, error):
        """ Writes an error to the widget in case that the process failed
            to start.
        """
        errors = ['Failed to Start', 'Crashed', 'Timedout', 'WriteError',
            'ReadError', 'UnknownError']
        msg = 'B2plot process: ' + errors[error]
        logging.error(msg)
        self.setText(msg)

    @pyqtSlot(int)
    def show_plot(self, exit_status):
        if exit_status == 0:
            data = self.convert.readAll()
            image = QImage()
            image.loadFromData(data)
            self.setPixmap(QPixmap.fromImage(image))
        else:
            msg = 'Process finished unexpectedly!\nExit status = '
            if exit_status == 1:
                msg += ' 1 [EXIT_FAILURE]'
            else:
                msg += str(exit_status)
            self.setText(msg)

    @pyqtSlot(int)
    def setConvertPath(self, convert_path):
        """ Executable requires absolute path. No ${PATH} possible!
        """
        self.convert_path = convert_path

    def getConvertPath(self):
        return self.convert_path

    convertPath = pyqtProperty(str, getConvertPath, setConvertPath)

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
    def setB2plotCommand(self, command):
        self.b2plot_command = command

    def getB2plot_pltcmd(self):
        return self.b2plot_command

    b2PlotCommand = pyqtProperty(str, getB2plot_pltcmd, setB2plotCommand)

    @pyqtSlot()
    def print_tcsh_stderr(self):
        error_data=self.tcsh.readAllStandardError()
        error_text=bytearray(error_data).decode('utf8')
        self.stderrOutput.emit(str(error_text))

    @pyqtSlot()
    def read_tcsh_stdout(self):
        data = self.tcsh.readAll()
        text = str(bytearray(data).decode('utf8'))
        if 'B2PLOT FINISHED' in text:
            self.convert.setWorkingDirectory(self.rundir)
            self.convert_args =  ['-resize',
                                  str(self.width()) + 'x' + str(self.height()),
                                  'b2plot.ps', 'gif:-']
            self.convert.start(self.convert_path, self.convert_args)

    def find_solps_top(self, directory):
        """ Searches for setup.csh or SOLPSTOP file in the directory hierarchy.
            Arguments:
                run_directory (str): run_directory
            Returns:
                solps_top(str): if found setup.csh or SOLPSTOP file. Else None
        """
        solps_top = directory

        while(solps_top):
            path = solps_top + '/setup.csh'
            if os.path.exists(path) and os.access(path, os.R_OK):
                return solps_top
            path = solps_top + '/SOLPSTOP'
            if os.path.exists(path) and os.access(path, os.R_OK):
                with open(path) as file:
                    return file.readline()
            solps_top = solps_top.rsplit('/', 1)[0]
        return None

    @pyqtSlot()
    def executeB2plotCommand(self):
        """ Opens TCSH login shell and runs B2plot command
            previously defined and under the runsDir.

            TCSH enviromnent is searched sourced from 'setup.csh' or pointed
            with SOLPSTOP file. SOLPSTOP is probed for runDir changes and
            if necessary resourced within a new shell.

            b2plot is executed in B2PLOT_DEV="ps" mode.

            TODO: b2plot error handling when resulting b2plot.ps file
                  is empty or nonexistent.
        """
        rundir_solps_top = self.find_solps_top(self.rundir)
        if not rundir_solps_top:
            if not self.rundir:
                msg = "Empty B2plot runDir! Bailing out."
                logging.error(msg)
            else:
                msg = "Could not find readable SOLPSTOP for run"
                logging.error(msg)
            self.setText(msg)
            return

        if rundir_solps_top != self.solps_top:  # we have a new SOLPSTOP
            self.tcsh.kill()
            self.solps_top = rundir_solps_top

        cmd = ''
        if self.tcsh.state() != QProcess.Running:
            self.tcsh.setWorkingDirectory(self.solps_top)
            env = QProcessEnvironment.systemEnvironment()
            self.tcsh.setProcessEnvironment(env)
            self.tcsh.start(self.tcsh_path, ['-l'])
            logging.info("B2plot TCSH started in " + self.solps_top)
            cmd += 'cd ' + self.solps_top + '\n'
            cmd += '\source setup.csh\necho TCSH READY\n'
            cmd += 'setenv B2PLOT_DEV "ps"\n'
        if self.b2plot_command and self.rundir:
            cmd += 'cd ' + self.rundir + '\n'
            cmd += self.b2plot_command + '\n'
            cmd += 'echo B2PLOT FINISHED\n'
            self.tcsh.write(bytearray(cmd, 'utf8'))
        else:
            logging.warning("No B2plot command or run directory")


if __name__ == "__main__":

    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = B2plot()
    window.show()
    rundir = "~/solps-iter-devel/runs/ITER_535_D+He+Ar/my_new_run" 
    window.setRundir(os.path.expanduser(rundir))
    window.setB2plotCommand("echo phys a4p ti te m/ surf | b2plot")
    window.executeB2plotCommand()
    sys.exit(app.exec_())
