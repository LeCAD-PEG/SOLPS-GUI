#!/usr/bin/env python3
""" A PyQt custom http://www.gnuplot.info/ widget for Qt Designer.
"""

from PySide6.QtCore import (Qt, QProcess, QSize, Signal,
                          QSettings, Slot, Property, QTemporaryDir,
                          QProcessEnvironment)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout, QWidget, QGridLayout
from tcsh_process import TcshProcess

import logging
import os
import tempfile

try:
    from QtGnuplot import QtGnuplotInstance, QtGnuplotWidget, QtGnuplotBar
    GNUPLOT_WIDGET = True
except ImportError as e:
    GNUPLOT_WIDGET = False


def cleanTempFiles(*files):
    for file in files:
        if file and os.path.exists(file):
            os.unlink(file)

class Gnuplot(TcshProcess):
    """Gnuplot(QWidget)
    Provides a custom widget to display a gnuplot with properties and slots
    that can be used to customize its appearance.

    The gnuplot can be either the embedded Qt5 widget from
    ``solps-gui/src/gnuplot-widget``, built with
    ``solps-gui/build-gnuplot-widget.sh`` (read more in ``README.md``) or
    the system gnuplot.

    The difference is that the embedded version also has interactivity, meaning
    zooming, resizing, etc... while the system version is a static picture,
    that does not resize or zoom.
    """

    TERMINAL = 'gif'
    if GNUPLOT_WIDGET:
        send_command = Signal(str)
        TERMINAL = 'qt'

    def __init__(self, parent=None):
        super(Gnuplot, self).__init__(parent)
        settings = QSettings('ITER', 'solps-gui')
        self.tcsh_path = settings.value('tcsh_path', '/bin/tcsh')
        self.gnuplot_path = settings.value('gnuplot_path', 'gnuplot')
        self.solps_plot_command = None
        self.gnuplot_cmdfile = None
        self.gnuplot_datafile = None

        self.previous_event = None

        # Creating temporary folder.
        self.temp_dir = QTemporaryDir('/tmp/gnuplot')
        self.destroyed.connect(self.temp_dir.remove)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(1, 1, 1, 1)

        if GNUPLOT_WIDGET:
            self.gp = QtGnuplotInstance(parent=self)
            self.gnuplot = QtGnuplotWidget(parent=self)
            self.gp.setWidget(self.gnuplot)
            self.gnuplotBar = QtGnuplotBar(self, m_widget=self.gnuplot)
            # self.send_command.connect(self.gnuplot.cmd)
            self.gnuplot.plotDone.connect(self.showPlot)
            layout.addWidget(self.gnuplot, 0, 0)
            layout.addWidget(self.gnuplotBar, 1, 0)
        else:

            self.gnuplot = QProcess(self)
            # self.gnuplot.setWorkingDirectory(self.temp_dir.path())

            self.gnuplot.finished.connect(self.showPlot)
            self.gnuplot.started.connect(self.writeCommandsToGnuplot)
            self.gnuplot.errorOccurred.connect(self.showError)

            self.label = QLabel(self)

            self.label.setAlignment(Qt.AlignCenter)
            self.label.setFrameStyle(QFrame.StyledPanel)
            self.label.setMinimumSize(QSize(180, 100))
            self.label.setText("Gnuplot widget for SOLPS")
            layout.addWidget(self.label, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.tcsh.stdOutput.connect(self.readTcshStdOut)

    @Slot(str)
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

        if GNUPLOT_WIDGET:
            self.gnuplot_cmd = plot_command.split('#', 1)[0]
            # self.send_command.emit(self.gnuplot_cmd)
            self.gp << self.gnuplot_cmd + '\n'
        else:
            self.gnuplot_cmd += 'plot ' + plot_command.split('#', 1)[0]
            self.gnuplot_cmd += '\nquit\n'
            self.gnuplot.start(self.gnuplot_path)
            if not self.gnuplot.waitForStarted():
                logging.error(self.gnuplot.program() + " not started")
                return

    @Slot()
    def writeCommandsToGnuplot(self):
        """ After gnuplot process has started send the commands to the pipe.
        We rather wait to start than immediately write the pipe.
        """
        chars = self.gnuplot.write(bytearray(self.gnuplot_cmd, 'utf8'))
        assert(chars >= 0)

    @Slot(QProcess.ProcessError)
    def showError(self, error):
        """ Writes an error to the widget in case that the process failed
            to start.
        """
        errors = ['Failed to Start', 'Crashed', 'Timedout', 'WriteError',
                  'ReadError', 'UnknownError']
        msg = 'Gnuplot process: ' + errors[error]
        logging.error(msg)
        self.label.setText(msg)

    @Slot(int)
    @Slot()
    def showPlot(self, exit_status=0):
        if GNUPLOT_WIDGET:
            # Do not remove the temporary files, since gnuplot needs it for
            # interactivity!
            if self.solps_plot_command:
                logging.info("Gnuplot command: " + self.solps_plot_command +
                             " finished.")
            return
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
        cleanTempFiles(self.gnuplot_cmdfile, self.gnuplot_datafile)

    @Slot(str)
    def setGnuplotPath(self, gnuplot_path):
        """ Executable requires absolute path. No ${PATH} possible!
        """
        self.gnuplot_path = gnuplot_path

    def getGnuplotPath(self):
        return self.gnuplot_path

    gnuplotPath = Property(str, getGnuplotPath, setGnuplotPath)

    @Slot(str)
    def setSolpsPlotCommand(self, command):
        self.solps_plot_command = command

    def getSolpsPlotCommand(self):
        return self.solps_plot_command

    solpsPlotCommand = Property(str, getSolpsPlotCommand,
                                    setSolpsPlotCommand)

    @Slot()
    def print_tcsh_stderr(self, error_text):
        self.stderrOutput.emit(error_text)

    @Slot(str)
    def readTcshStdOut(self, text):
        if 'PLOT FINISHED' in text:
            self.gnuplot_cmd = f'cd "{self.runDir}"\n'
            self.gnuplot_cmd += f'load "{self.gnuplot_cmdfile}"\n'
            if GNUPLOT_WIDGET:
                # self.send_command.emit(self.gnuplot_cmd)
                self.gp << self.gnuplot_cmd
            else:
                self.gnuplot_cmd += '\nquit\n'
                self.gnuplot.start(self.gnuplot_path)

    @Slot()
    def executeSolpsPlotCommand(self):
        """ Opens TCSH login shell and runs SOLPS plot command
        previously defined and under the runsDir.

        TCSH enviromnent is searched sourced from 'setup.csh' or pointed
        with SOLPSTOP file. SOLPSTOP is probed for runDir changes and
        ff necessary resourced within a new shell.

            SOLPS plot is executed in GNUPLOT_BATCH mode.
        """
        env = QProcessEnvironment.systemEnvironment()
        env.insert('GNUPLOT_BATCH', 'True')
        self.tcsh.setProcessEnvironment(env)
        self.startTcsh()
        cleanTempFiles(self.gnuplot_cmdfile, self.gnuplot_datafile)

        if self.solps_plot_command and self.runDir:
            fd, self.gnuplot_cmdfile = tempfile.mkstemp(prefix='gnuplot',
                                                        suffix='.cmd',
                                                      dir=self.temp_dir.path())
            os.close(fd)
            fd, self.gnuplot_datafile = tempfile.mkstemp(prefix='gnuplot',
                                                         suffix='.dat',
                                                      dir=self.temp_dir.path())
            os.close(fd)
            cmd = f'cd {self.runDir}\n'
            cmd_file = self.gnuplot_cmdfile.split('/')[-1]
            dat_file = self.gnuplot_datafile.split('/')[-1]
            cmd += f'setenv GNUPLOT_CMD {cmd_file}\n'
            cmd += f'setenv GNUPLOT_DATA {dat_file}\n'
            cmd += f'setenv GNUPLOT_TMP {self.temp_dir.path()}\n'
            cmd += f'{self.solps_plot_command}\n'
            cmd += 'echo PLOT FINISHED\n'

            logging.info(f'Running command:')
            [logging.info(_) for _ in cmd.split('\n')]
            self.tcsh.write(cmd)
        else:
            logging.warning("No plot command or run directory")


if __name__ == "__main__":
    import sys


    class CmdInput(QLineEdit):
        sendCmd = Signal(str)

        def __init__(self, parent=None):
            super(CmdInput, self).__init__(parent)
            self.returnPressed.connect(self.sendCommand)

        @Slot()
        def sendCommand(self):
            text = self.text()
            self.sendCmd.emit(text)
            self.clear()

    app = QApplication(sys.argv)
    main = QMainWindow()
    main.setAttribute(Qt.WA_DeleteOnClose)
    widget = QWidget()
    layout = QVBoxLayout()

    window = Gnuplot()
    window.activateDebugging()
    input_w = CmdInput()
    input_w.sendCmd.connect(window.plot)

    layout.addWidget(window)
    layout.addWidget(input_w)

    if GNUPLOT_WIDGET:
        from PySide6.QtWidgets import QPlainTextEdit

        class Output(QPlainTextEdit):
            def __init__(self, parent=None):
                super(Output, self).__init__(parent)

            @Slot()
            @Slot(str)
            def updateLog(self, text='PLOT_DONE'):
                if text != "PLOT_DONE":
                    self.appendPlainText(text)
                else:
                    self.appendPlainText(text)

        output = Output()
        layout.addWidget(output)
        # window.gnuplot.gnuplotOutput.connect(output.updateLog)
        window.gnuplot.plotDone.connect(output.updateLog)
    widget.setLayout(layout)
    main.setCentralWidget(widget)
    main.show()
    code = app.exec()
    app.quit()
    sys.exit(code)
