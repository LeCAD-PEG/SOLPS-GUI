#!/usr/bin/env python3
""" A PyQt custom http://www.gnuplot.info/ widget for Qt Designer.
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
    """

    stderrOutput = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(B2plot, self).__init__(parent)
        settings = QSettings('ITER', 'solps-gui')
        self.tcsh_path = settings.value('tcsh_path', '/bin/tcsh')
        self.b2plot_path = settings.value('b2plot_path', '/usr/bin/gnuplot')
        self.solps_top = None
        self.solps_top_changed = False
        self.rundir = None
        self.solps_plot_command = None
        self.b2plot_cmdfile = None
        self.b2plot_datafile = None

        self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumSize(QSize(180, 100))
        self.setText("B2plot widget for SOLPS")

        self.b2plot = QProcess()
        self.tcsh = QProcess()

        self.b2plot.finished.connect(self.show_plot)
        self.b2plot.started.connect(self.write_commands_to_b2plot)
        self.b2plot.error.connect(self.show_error)
        self.tcsh.readyReadStandardOutput.connect(self.read_tcsh_stdout)
        self.tcsh.readyReadStandardError.connect(self.print_tcsh_stderr)

    def sizeHint(self):
        return QSize(320, 200)

    @pyqtSlot(str)
    def plot(self, plot_command):
        """ Starts b2plot process and sends plot commands through the
            standard input. Everything after # is truncated
        """
        if self.b2plot.state() != QProcess.NotRunning:
            logging.warning("B2plot process still running. Command ignored!")
            #  self.process.terminate()
            return

        self.b2plot_cmd = 'set terminal gif size ' \
            + str(self.width()) + ', ' + str(self.height()) + '\n' \
            + 'plot ' + plot_command.split('#', 1)[0]  + '\nquit\n'
        # print(self.b2plot_cmd)
        self.b2plot.start(self.b2plot_path)

    @pyqtSlot()
    def write_commands_to_b2plot(self):
        """ After b2plot process has started send the commands to the pipe.
            We rather wait to start than immediately write the pipe.
        """
        # print("B2plot process started.")
        chars = self.b2plot.write(bytearray(self.b2plot_cmd, 'utf8'))
        assert(chars >= 0)

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
            data = self.b2plot.readAll()
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
        # Tempfiles cleanup
        if self.b2plot_cmdfile and os.path.exists(self.b2plot_cmdfile):
            os.unlink(self.b2plot_cmdfile)
        if self.b2plot_datafile and os.path.exists(self.b2plot_datafile):
            os.unlink(self.b2plot_datafile)

    @pyqtSlot(int)
    def setB2plotPath(self, b2plot_path):
        """ Executable requires absolute path. No ${PATH} possible!
        """
        self.b2plot_path = b2plot_path

    def getB2plotPath(self):
        return self.b2plot_path

    b2plotPath = pyqtProperty(str, getB2plotPath, setB2plotPath)

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
    def setSolpsPlotCommand(self, command):
        self.solps_plot_command = command

    def get_solps_pltcmd(self):
        return self.solps_plot_command

    solpsPlotCommand = pyqtProperty(str, get_solps_pltcmd, setSolpsPlotCommand)

    @pyqtSlot()
    def print_tcsh_stderr(self):
        error_data=self.tcsh.readAllStandardError()
        error_text=bytearray(error_data).decode('utf8')
        self.stderrOutput.emit(str(error_text))

    @pyqtSlot()
    def read_tcsh_stdout(self):
        data = self.tcsh.readAll()
        text = str(bytearray(data).decode('utf8'))
        if 'PLOT FINISHED' in text:
            self.b2plot_cmd = 'cd "' + self.runDir + '"\n' \
                'set terminal gif size ' \
                + str(self.width()) + ', ' + str(self.height()) + '\n' \
                + 'load "' + self.b2plot_cmdfile + '"\nquit\n'
            #print(self.b2plot_cmd)
            self.b2plot.start(self.b2plot_path)

    def find_solps_top(self, directory):
        """ Searches for setup.csh or SOLPSTOP file in the directory hierarchy.
            Arguments:
                run_directory (str): run_directory
            Returns:
                solps_top(str): if found stup.csh or SOLPSTOP file. Else None
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
    def executeSolpsPlotCommand(self):
        """ Opens TCSH login shell and runs SOLPS plot command
            previously defined and under the runsDir.

            TCSH enviromnent is searched sourced from 'setup.csh' or pointed
            with SOLPSTOP file. SOLPSTOP is probed for runDir changes and
            if necessary resourced within a new shell.

            SOLPS plot is executed in B2PLOT_BATCH mode.
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

        if rundir_solps_top != self.solps_top:  # we have new SOLPSTOP
            self.tcsh.kill()
            self.solps_top = rundir_solps_top

        cmd = ''
        if self.tcsh.state() != QProcess.Running:
            self.tcsh.setWorkingDirectory(self.solps_top)
            env = QProcessEnvironment.systemEnvironment()
            env.insert('B2PLOT_BATCH', 'true')
            self.tcsh.setProcessEnvironment(env)
            self.tcsh.start(self.tcsh_path, ['-l'])
            logging.info("B2plot TCSH started in " + self.solps_top)
            cmd += "cd " + self.solps_top \
                  + '\nsource setup.csh\necho TCSH READY\n'
        if self.solps_plot_command and self.rundir:
            fd, self.b2plot_cmdfile = tempfile.mkstemp('.cmd', 'b2plot')
            os.close(fd)
            fd, self.b2plot_datafile = tempfile.mkstemp('.dat', 'b2plot')
            os.close(fd)
            cmd += 'cd ' + self.rundir + '\n'
            cmd += 'setenv B2PLOT_CMD ' + self.b2plot_cmdfile + '\n'
            cmd += 'setenv B2PLOT_DATA ' + self.b2plot_datafile + '\n'
            cmd += self.solps_plot_command + '\n'
            cmd += 'echo PLOT FINISHED\n'
            self.tcsh.write(bytearray(cmd, 'utf8'))
        else:
            logging.warning("No plot command or run directory")


if __name__ == "__main__":

    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = B2plot()
    window.show()
    window.plot('sin(x)')
    sys.exit(app.exec_())
