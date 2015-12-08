#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QProcess, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel

class PyGnuplot(QLabel):
    def __init__(self, parent = None):
        super(PyGnuplot, self).__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.process = QProcess()
        self.process.finished.connect(self.show_plot)
        self.process.error.connect(self.show_error)

    def plot(self, plot_command):
        """ Start gnuplot and write commands in standard input.
            Executable requires absolute path. No ${PATH} possible!
            Pause command demonstrates artificial processing and
            can be removed for production.
        """
        cmd = 'set terminal gif size ' \
            + str(self.width()) + ', ' + str(self.height()) + '; ' \
            + plot_command  + '; pause 3; quit;\n' 
        print(cmd)
        self.process.start("/usr/bin/gnuplot")  # Check this path
        self.process.writeData(bytearray(cmd, 'utf8'))

    @pyqtSlot(QProcess.ProcessError)
    def show_error(self, error):
        msg = ['Failed to Start', 'Crashed', 'Timedout', 'WriteError',
            'ReadError', 'UnknownError']
        self.setText('ProcessError: ' + msg[error])

    @pyqtSlot(int)
    def show_plot(self, exit_status):
        if exit_status == 0:
            data = self.process.readAll()
            image = QImage()
            image.loadFromData(data)
            self.setPixmap(QPixmap.fromImage(image))
        else:
            self.setText('exit status = ' + str(exit_status))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    gnuplot = PyGnuplot()
    gnuplot.resize(451, 322)
    gnuplot.plot('plot sin(2*x)/x')
    gnuplot.setText("Waiting for gnuplot to finish...")
    gnuplot.show()
    sys.exit(app.exec_())
