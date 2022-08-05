#!/usr/bin/env python3
""" A PyQt custom B2plot widget for Qt Designer.
"""

from PySide6.QtCore import (Qt, QProcess, QProcessEnvironment, QSize, Signal,
                          QSettings, Slot, Property)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout


import logging
import os

from tcsh import TcshProcess


class B2plot(TcshProcess):
    """ B2plot(QWidget)

        Provides a custom widget to display a b2plot with properties and slots
        that can be used to customize its appearance.

        Emits *convertFinished()* when b2plot conversion is finished
        and it is safe to start another B2plot widget in a chain to the
        *executeB2plotCommand()*.
    """

    stderrOutput = Signal(str)

    convertFinished = Signal()

    def __init__(self, parent=None):
        super(B2plot, self).__init__(parent)
        settings = QSettings('ITER', 'solps-gui')
        self.tcshPath = settings.value('tcsh_path', '/bin/tcsh')
        self.convert_path = settings.value('convert_path', '/usr/bin/convert')

        self.b2plot_command = None
        self.b2plot_page = 0

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFrameStyle(QFrame.StyledPanel)
        self.label.setMinimumSize(QSize(180, 100))
        self.label.setText("B2plot widget for SOLPS")
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.convert = QProcess()

        self.convert.finished.connect(self.show_plot)
       # self.convert.error.connect(self.show_error)
        self.tcsh.stdOutput.connect(self.read_tcsh_stdout)
        self.tcsh.stdErrOutput.connect(self.print_tcsh_stderr)

    def sizeHint(self):
        return QSize(320, 200)

    @Slot(QProcess.ProcessError)
    def show_error(self, error):
        """ Writes an error to the widget in case that the process failed
            to start.
        """
        errors = ['Failed to Start', 'Crashed', 'Timedout', 'WriteError',
            'ReadError', 'UnknownError']
        msg = 'B2plot process: ' + errors[error]
        logging.error(msg)
        self.setText(msg)

    @Slot(int)
    def show_plot(self, exit_status):
        self.convertFinished.emit()
        if exit_status == 0:
            data = self.convert.readAll()
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

    @Slot(int)
    def setConvertPath(self, convert_path):
        """ Executable requires absolute path. No ${PATH} possible!
        """
        self.convert_path = convert_path

    def getConvertPath(self):
        return self.convert_path

    convertPath = Property(str, getConvertPath, setConvertPath)

    @Slot(str)
    def setB2plotCommand(self, command):
        """ Sets b2plot command for later execution.

            Args:
                command (str): Command in usual b2plot style.
                                ``echo "b2plot commands" | b2plot``
        """
        self.b2plot_command = command

    def getB2plot_pltcmd(self):
        return self.b2plot_command

    b2plotCommand = Property(str, getB2plot_pltcmd, setB2plotCommand)

    def setB2plotPage(self, page):
        """ Sets the page for conversion into final image.

            Args:
                page (int): page number. First page is 0 and it is default.
        """
        self.b2plot_page = page

    def getB2plotPage(self):
        return self.b2plot_page

    b2plotPage = Property(int, getB2plotPage, setB2plotPage)

    @Slot(str)
    def print_tcsh_stderr(self, error_text):
        self.stderrOutput.emit(error_text)

    @Slot(str)
    def read_tcsh_stdout(self, text):
        if 'B2PLOT FINISHED' in text:
            b2plot_ps_file = self.runDir + '/b2plot.ps'
            if os.path.exists(b2plot_ps_file):
                self.convert_args =  ['+antialias', '-resize', str(self.width())
                                      + 'x' + str(self.height()), 'b2plot.ps[' +
                                      str(self.b2plot_page) + ']', 'png:-']
                self.convert.setWorkingDirectory(self.runDir)
                self.convert.start(self.convert_path, self.convert_args)
            else:
                msg ="b2plot.ps file not created from " + self.b2plot_command
                logging.error(msg)
                self.label.setText(msg)
                self.convertFinished.emit()

    @Slot()
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
        cmd = ''
        if not self.tcsh.state():
            # cmd += 'module load libpng\n'
            cmd += 'setenv B2PLOT_DEV "ps"\n'

        self.startTcsh()

        if self.b2plot_command and self.runDir:
            cmd += 'cd ' + self.runDir + '\n'
            cmd += self.b2plot_command + '\n'
            cmd += 'echo B2PLOT FINISHED\n'
            self.tcsh.write(cmd)
        else:
            logging.warning("No B2plot command or run directory")

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication
    import logging

    logging.getLogger().setLevel(logging.DEBUG)
    app = QApplication(sys.argv)
    window = B2plot()
    window.show()
    rundir = '/solps-iter/runs/examples/ITER_2298_Honly_20MW/baserun'
    window.setRunDir(os.path.expanduser(rundir))
    window.setB2plotCommand("echo phys a4p ti te m/ surf | b2plot")
    window.executeB2plotCommand()
    sys.exit(app.exec())
