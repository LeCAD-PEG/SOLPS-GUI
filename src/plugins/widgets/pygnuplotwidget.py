#!/usr/bin/env python3
""" A PyQt custom http://www.gnuplot.info/ widget for Qt Designer.
"""

from PyQt5.QtCore import Qt, QProcess, QSize, pyqtSlot, pyqtProperty
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QFrame


class PyGnuplotWidget(QLabel):
    """ PyGnuplotWidget(QWidget)
    
        Provides a custom widget to display a gnuplot with properties and slots
        that can be used to customize its appearance.
    """
    
    def __init__(self, parent=None):
        super(PyGnuplotWidget, self).__init__(parent)
        self._gnuplot_path = "/usr/bin/gnuplot"
        self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumSize(QSize(180, 100))
        self.setText("Gnuplot widget for SOLPS")
        self.process = QProcess()
        self.process.finished.connect(self.show_plot)
        self.process.started.connect(self.started)
        #self.process.stateChanged.connect(self.stateChanged)
        self.process.error.connect(self.show_error)

    def sizeHint(self):
    
        return QSize(320, 200)

    #def paintEvent(self, event):
    #    self.setText("Repaing requested")

    @pyqtSlot()
    def started(self):
        self.setText("Gnuplot process started.")

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
        if self.process.state() != QProcess.NotRunning:
            self.setText("Process still running. Command ignored!")
            self.process.terminate()
            return

        cmd = 'set terminal gif size ' \
            + str(self.width()) + ', ' + str(self.height()) + '\n' \
            + 'plot ' + plot_command.split('#', 1)[0]  + '\nquit\n'
        # print(cmd)
        self.process.start(self._gnuplot_path)
        chars_written = self.process.write(bytearray(cmd, 'utf8'))
        assert(chars_written >= 0)

    @pyqtSlot(QProcess.ProcessError)
    def show_error(self, error):
        errors = ['Failed to Start', 'Crashed', 'Timedout', 'WriteError',
            'ReadError', 'UnknownError']
        msg = 'ProcessError: ' + errors[error]
        print(msg)
        self.setText(msg)

    @pyqtSlot(int)
    def show_plot(self, exit_status):
        if exit_status == 0:
            data = self.process.readAll()
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
        self._gnuplot_path = gnuplot_path

    def getGnuplotPath(self):
        return self._gnuplot_path

    gnuplotPath = pyqtProperty(str, getGnuplotPath, setGnuplotPath)

if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    window = PyGnuplotWidget()
    window.show()
    sys.exit(app.exec_())
