#!/usr/bin/env python3
""" A PyQt custom http://www.gnuplot.info/ widget for Qt Designer.
"""

from PyQt5.QtCore import (Qt, QProcess, QProcessEnvironment, QSize, pyqtSignal,
                          QSettings, pyqtSlot, pyqtProperty)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QWidget

import logging
import os
import tempfile

try:
    from pyQtGnuplot import gnuplotWidget
    GNUPLOT_WIDGET = True
except ImportError as e:
    GNUPLOT_WIDGET = False

class Gnuplot(QWidget):
    """Gnuplot(QWidget)
    Provides a custom widget to display a gnuplot with properties and slots
    that can be used to customize its appearance.
    """

    stderrOutput = pyqtSignal(str)
    TERMINAL = 'gif'
    if GNUPLOT_WIDGET:
        send_command = pyqtSignal(str)
        TERMINAL = 'qt'

    def __init__(self, parent=None):
        super(Gnuplot, self).__init__(parent)
        settings = QSettings('ITER', 'solps-gui')
        self.tcsh_path = settings.value('tcsh_path', '/bin/tcsh')
        self.gnuplot_path = settings.value('gnuplot_path', '/usr/bin/gnuplot')
        self.solps_top = None
        self.solps_top_changed = False
        self.rundir = None
        self.solps_plot_command = None
        self.gnuplot_cmdfile = None
        self.gnuplot_datafile = None

        layout = QVBoxLayout()

        if GNUPLOT_WIDGET:
            self.gnuplot = gnuplotWidget(self)
            print(self.gnuplot)
            self.send_command.connect(self.gnuplot.cmd)
            layout.addWidget(self.gnuplot)
        else:

            self.gnuplot = QProcess()

            self.gnuplot.finished.connect(self.show_plot)
            self.gnuplot.started.connect(self.write_commands_to_gnuplot)
            self.gnuplot.error.connect(self.show_error)

            self.label = QLabel()
            layout.addWidget(self.label)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setFrameStyle(QFrame.StyledPanel)
            self.label.setMinimumSize(QSize(180, 100))
            self.label.setText("Gnuplot widget for SOLPS")

        self.setLayout(layout)

        self.tcsh = QProcess()
        self.tcsh.readyReadStandardOutput.connect(self.read_tcsh_stdout)
        self.tcsh.readyReadStandardError.connect(self.print_tcsh_stderr)

    def sizeHint(self):
        return QSize(320, 200)

    @pyqtSlot(str)
    def plot(self, plot_command):
        """ Starts gnuplot process and sends plot commands through the
        standard input. Everything after # is truncated
        """

        if not GNUPLOT_WIDGET and self.gnuplot.state() != QProcess.NotRunning:
            logging.warning("Gnuplot process still running. Command ignored!")
            #  self.process.terminate()
            return

        self.gnuplot_cmd = 'set terminal ' + self.TERMINAL + ' size ' \
            + str(self.width()) + ', ' + str(self.height()) + '\n' \
            + 'plot ' + plot_command.split('#', 1)[0]
        # print(self.gnuplot_cmd)

        if GNUPLOT_WIDGET:
            self.send_command.emit(self.gnuplot_cmd)
        else:
            self.gnuplot_cmd += '\nquit\n'
            self.gnuplot.start(self.gnuplot_path)
            if not self.gnuplot.waitForStarted():
                logging.error(self.gnuplot.program() + " not started")
                return

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
        logging.error(msg)
        self.label.setText(msg)

    @pyqtSlot(int)
    def show_plot(self, exit_status):
        if GNUPLOT_WIDGET:
            pass
        else:
            if exit_status == 0:
                data = self.gnuplot.readAll()
                image = QImage()
                image.loadFromData(data)
                self.label.setPixmap(QPixmap.fromImage(image))
            else:
                msg = 'Process finished unexpectedly!\nExit status = '
                if exit_status == 1:
                    msg += ' 1 [EXIT_FAILURE]'
                else:
                    msg += str(exit_status)
                self.label.setText(msg)
        # Tempfiles cleanup
        if self.gnuplot_cmdfile and os.path.exists(self.gnuplot_cmdfile):
            os.unlink(self.gnuplot_cmdfile)
        if self.gnuplot_datafile and os.path.exists(self.gnuplot_datafile):
            os.unlink(self.gnuplot_datafile)

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
        error_data = self.tcsh.readAllStandardError()
        error_text = bytearray(error_data).decode('utf8')
        self.stderrOutput.emit(str(error_text))

    @pyqtSlot()
    def read_tcsh_stdout(self):
        data = self.tcsh.readAll()
        text = str(bytearray(data).decode('utf8'))
        if 'PLOT FINISHED' in text:
            self.gnuplot_cmd = 'cd "' + self.runDir + '"\n' \
                'set terminal ' + self.TERMINAL + ' size ' \
                + str(self.width()) + ', ' + str(self.height()) + '\n' \
                + 'load "' + self.gnuplot_cmdfile
            # print(self.gnuplot_cmd)
            if GNUPLOT_WIDGET:
                print(self.gnuplot_cmd)
                self.send_command.emit(self.gnuplot_cmd)
            else:
                self.gnuplot_cmd += '\nquit\n'
                self.gnuplot.start(self.gnuplot_path)

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

            SOLPS plot is executed in GNUPLOT_BATCH mode.
        """
        rundir_solps_top = self.find_solps_top(self.rundir)
        if not rundir_solps_top:
            if not self.rundir:
                msg = "Empty Gnuplot runDir! Bailing out."
                logging.error(msg)
            else:
                msg = "Could not find readable SOLPSTOP for run"
                logging.error(msg)
            self.setText(msg)
            return

        if rundir_solps_top != self.solps_top:  # we have new SOLPSTOP
            self.tcsh.kill()
            self.tcsh.waitForFinished()
            self.solps_top = rundir_solps_top

        cmd = ''
        if self.tcsh.state() != QProcess.Running:
            env = QProcessEnvironment.systemEnvironment()
            env.insert('GNUPLOT_BATCH', 'true')
            self.tcsh.setProcessEnvironment(env)
            self.tcsh.start(self.tcsh_path, ['-l'])
            if not self.tcsh.waitForStarted():
                logging.error(self.tcsh.program() + " not started")
                return
            logging.info("Gnuplot TCSH started in " + self.solps_top)
            cmd += "cd " + self.solps_top \
                   + '\nsource setup.csh\necho TCSH READY\n'
        if self.solps_plot_command and self.rundir:
            fd, self.gnuplot_cmdfile = tempfile.mkstemp('.cmd', 'gnuplot')
            os.close(fd)
            fd, self.gnuplot_datafile = tempfile.mkstemp('.dat', 'gnuplot')
            os.close(fd)
            cmd += 'cd ' + self.rundir + '\n'
            cmd += 'setenv GNUPLOT_CMD ' + self.gnuplot_cmdfile + '\n'
            cmd += 'setenv GNUPLOT_DATA ' + self.gnuplot_datafile + '\n'
            cmd += self.solps_plot_command + '\n'
            cmd += 'echo PLOT FINISHED\n'
            self.tcsh.write(bytearray(cmd, 'utf8'))
        else:
            logging.warning("No plot command or run directory")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit

    class CmdInput(QLineEdit):
        sendCmd = pyqtSignal(str)
        def __init__(self, parent=None):
            super(CmdInput, self).__init__(parent)
            self.returnPressed.connect(self.sendCommand)

        @pyqtSlot()
        def sendCommand(self):
            text = self.text()
            self.sendCmd.emit(text)
            self.clear()



    app = QApplication(sys.argv)
    main = QMainWindow()
    widget = QWidget()
    layout = QVBoxLayout()

    window = Gnuplot()
    input_w = CmdInput()
    input_w.sendCmd.connect(window.plot)

    layout.addWidget(window)
    layout.addWidget(input_w)

    if GNUPLOT_WIDGET:
        from PyQt5.QtWidgets import QPlainTextEdit
        class Output(QPlainTextEdit):
            def __init__(self, parent=None):
                super(Output, self).__init__(parent)

            @pyqtSlot(str)
            def updateLog(self, str):
                self.appendPlainText(str)


        output = Output()
        layout.addWidget(output)
        window.gnuplot.gnuplotOutput.connect(output.updateLog)
    widget.setLayout(layout)
    main.setCentralWidget(widget)
    main.show()
    sys.exit(app.exec_())
