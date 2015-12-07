#!/usr/bin/env python3
""" A PyQt custom TCSH widget.
"""

from PyQt5.QtCore import (Qt, QProcess, QProcessEnvironment, QSize, pyqtSignal,
                          pyqtSlot, pyqtProperty)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QFrame


class TcshWidget(QLabel):
    """ TcshWidget(QWidget)
    
        Provides a custom widget to display a gnuplot with properties and slots
        that can be used to customize its appearance.
    """
    
    def __init__(self, parent=None):
        super(TcshWidget, self).__init__(parent)
        self.gnuplot_path = "/usr/bin/gnuplot"
        self.tcsh_path = '/bin/tcsh'
        self.solps_top = None
        self.tcsh_plot_command = None

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
        msg = 'ProcessError: ' + errors[error]
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
    def setTcshPlotCommand(self, command):
        self.tcsh_plot_command = command

    def get_tcsh_pltcmd(self):
        return self.tcsh_plot_command

    tcshPlotCommand = pyqtProperty(str, get_tcsh_pltcmd, setTcshPlotCommand)

    @pyqtSlot()
    def executeTcshPlotCommand(self):
        if self.tcsh.state() != QProcess.Running:
            self.tcsh.start(self.tcsh_path)
            self.tcsh.setWorkingDirectory(self.solps_top)
            cmd = "cd " + self.solps_top \
                  + '\nsource setup.csh\necho TCSH READY\n'
            env = QProcessEnvironment.systemEnvironment()
            env.insert('GNUPLOT_BATCH', 'true')
            self.tcsh.setProcessEnvironment(env)


            self.tcsh_plot_command_executed = False


if __name__ == "__main__":

    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = TcshWidget()
    window.show()
    sys.exit(app.exec_())
