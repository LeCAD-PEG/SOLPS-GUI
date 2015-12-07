#!/usr/bin/env python3
""" A PyQt custom http://www.gnuplot.info/ widget for Qt Designer.
"""

from PyQt5.QtCore import (Qt, QProcess, QProcessEnvironment, QSize, pyqtSignal,
                          pyqtSlot, pyqtProperty)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QFrame

import os
import logging


class Gnuplot(QLabel):
    """ Gnuplot(QWidget)
    
        Provides a custom widget to display a gnuplot with properties and slots
        that can be used to customize its appearance.
    """
    
    def __init__(self, parent=None):
        super(Gnuplot, self).__init__(parent)
        self.gnuplot_path = "/usr/bin/gnuplot"
        self.tcsh_path = '/bin/tcsh'
        self.solps_top = None
        self.solps_top_changed = False
        self.rundir = None
        self.solps_plot_command = None

        self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumSize(QSize(180, 100))
        self.setText("Gnuplot widget for SOLPS")

        self.gnuplot = QProcess()
        self.tcsh = QProcess()

        self.gnuplot.finished.connect(self.show_plot)
        self.gnuplot.started.connect(self.write_commands_to_gnuplot)
        #self.gnuplot.stateChanged.connect(self.stateChanged)
        self.gnuplot.error.connect(self.show_error)
        self.tcsh.readyReadStandardOutput.connect(self.read_tcsh_stdout)
        self.tcsh.readyReadStandardError.connect(self.print_tcsh_stderr)

    def sizeHint(self):
        return QSize(320, 200)

    @pyqtSlot(QProcess.ProcessState)
    def stateChanged(self, newState):
        states = ['Not Running', 'Starting', 'Running']
        msg = 'Process state changed: ' + states[newState]
        print(msg)
        self.setText(msg)

    @pyqtSlot(str)
    def plot(self, plot_command):
        """ Starts gnuplot process and sends plot commands through the
            standard input. Everything after # is truncated
        """
        if self.gnuplot.state() != QProcess.NotRunning:
            print("Gnuplot process still running. Command ignored!")
            #  self.process.terminate()
            return

        self.gnuplot_cmd = 'set terminal gif size ' \
            + str(self.width()) + ', ' + str(self.height()) + '\n' \
            + 'plot ' + plot_command.split('#', 1)[0]  + '\nquit\n'
        #  print(self.gnuplot_cmd)
        self.gnuplot.start(self.gnuplot_path)

    @pyqtSlot()
    def write_commands_to_gnuplot(self):
        """ After gnuplot process has started send the commands to the pipe.
            We rather wait to start than immediately write the pipe.
        """
        # print("Gnuplot process started.")
        chars = self.gnuplot.write(bytearray(self.gnuplot_cmd, 'utf8'))
        assert(chars >= 0)

    @pyqtSlot(QProcess.ProcessError)
    def show_error(self, error):
        """ Writes an error to the widget in case that the process failed
            to start.
        """
        errors = ['Failed to Start', 'Crashed', 'Timedout', 'WriteError',
            'ReadError', 'UnknownError']
        msg = 'Gnuplot process: ' + errors[error]
        print(msg)
        self.setText(msg)

    @pyqtSlot(int)
    def show_plot(self, exit_status):
        if exit_status == 0:
            data = self.gnuplot.readAll()
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
    def setGnuplotPath(self, gnuplot_path):
        """ Executable requires absolute path. No ${PATH} possible!
        """
        self.gnuplot_path = gnuplot_path

    def getGnuplotPath(self):
        return self.gnuplot_path

    gnuplotPath = pyqtProperty(str, getGnuplotPath, setGnuplotPath)

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
        self.gnuplot.setText(str(error_text))

    @pyqtSlot()
    def read_tcsh_stdout(self):
        data = self.tcsh.readAll()
        text = str(bytearray(data).decode('utf8'))
        if 'PLOT FINISHED' in text:
            print("TODO Gnuplot should plot this")
            self.plot('load')

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
            if os.path.exists(path):
                return solps_top
            path = solps_top + '/SOLPSTOP'
            if os.path.exists(path):
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

            SOLPS plot is executed in GNUPLOT_BATCH mode.
        """
        rundir_solps_top = self.find_solps_top(self.rundir)
        if not rundir_solps_top:
            if not self.rundir:
                logging.error("Empty Gnuplot runDir! Bailing out.")
            else:
                logging.error("Could not find SOLPSTOP for " + self.rundir)
            return

        if rundir_solps_top != self.solps_top:  # we have new SOLPSTOP
            self.tcsh.kill()
            self.solps_top = rundir_solps_top

        cmd = ''
        if self.tcsh.state() != QProcess.Running:
            self.tcsh.setWorkingDirectory(self.solps_top)
            env = QProcessEnvironment.systemEnvironment()
            env.insert('GNUPLOT_BATCH', 'true')
            self.tcsh.setProcessEnvironment(env)
            self.tcsh.start(self.tcsh_path)
            logging.info("Guplot TCSH started in " + self.solps_top)
            cmd += "cd " + self.solps_top \
                  + '\nsource setup.csh\necho TCSH READY\n'
        if self.solps_plot_command and self.rundir:
            cmd += 'cd ' + self.rundir + '\n'
            cmd += self.solps_plot_command + '\n'
            cmd += 'echo PLOT FINISHED\n'
            self.tcsh.write(bytearray(cmd, 'utf8'))
        else:
            logging.warning("No plot command or run directory")


if __name__ == "__main__":

    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = Gnuplot()
    window.show()
    window.plot('sin(x)')
    sys.exit(app.exec_())
