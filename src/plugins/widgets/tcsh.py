#!/usr/bin/env python3
""" A PyQt custom TCSH widget.
"""

from PyQt5.QtCore import (Qt, QProcess, QProcessEnvironment, QSize, pyqtSignal,
                          pyqtSlot, pyqtProperty, QByteArray)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QPlainTextEdit, QFrame


class Tcsh(QPlainTextEdit):
    """ Tcsh(QWidget)
    
        Provides a custom widget to display a gnuplot with properties and slots
        that can be used to customize its appearance.
    """

    solpsTopChanged = pyqtSignal(str)
    runChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(Tcsh, self).__init__(parent)
        self.tcsh_path = '/bin/tcsh'
        self.solps_top = None
        self.tcsh_command = None

        #self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumSize(QSize(180, 50))
        self.setPlaceholderText("TCSH widget for SOLPS")
        #self.setEnabled(False)

        self.tcsh = QProcess()
        self.tcsh.readyReadStandardOutput.connect(self.print_stdout)
        self.tcsh.readyReadStandardError.connect(self.print_stderr)

        #self.gnuplot.finished.connect(self.show_plot)
        #self.gnuplot.started.connect(self.write_commands_to_gnuplot)
        #self.gnuplot.stateChanged.connect(self.stateChanged)
        #self.gnuplot.error.connect(self.show_error)

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
    def setSolpsTop(self, directory):
        """
        Args:
             directory (str): Absolute path to SOLPS directory where setup.csh
                              should reside. (Re)starts the TCSH environment
        """
        self.solps_top = directory


    def getSolpsTop(self):
        return self.solps_top

    solpsTop = pyqtProperty(str, getSolpsTop, setSolpsTop)

    @pyqtSlot(str)
    def setTcshCommand(self, command):
        self.tcsh_command = command

    def get_tcsh_command(self):
        return self.tcsh_command

    tcshPlotCommand = pyqtProperty(str, get_tcsh_command, setTcshCommand)

    @pyqtSlot()
    def executeTcshCommand(self):
        if self.tcsh.state() != QProcess.Running:
            self.tcsh.setWorkingDirectory(self.solps_top)
            self.tcsh.start(self.tcsh_path, ['-l'])
            cmd = "cd " + self.solps_top \
                  + '\nsource setup.csh\necho TCSH READY\n'
            env = QProcessEnvironment.systemEnvironment()
            self.tcsh.setProcessEnvironment(env)
            self.tcsh.write(bytearray(cmd, 'utf8'))
            self.solpsTopChanged.emit(self.solps_top)


        self.tcsh.write(bytearray(self.tcsh_command+'\n', 'utf8'))



if __name__ == "__main__":

    import sys, os
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    tcsh_widget = Tcsh()
    tcsh_widget.show()
    tcsh_widget.setSolpsTop(os.path.expanduser("~")+'/solps-iter')
    tcsh_widget.setTcshCommand('ls')
    tcsh_widget.executeTcshCommand()
    tcsh_widget.setTcshCommand('ls -l')
    tcsh_widget.executeTcshCommand()
    sys.exit(app.exec_())
