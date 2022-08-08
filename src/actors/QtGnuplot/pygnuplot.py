#!/usr/bin/env python3
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

from PySide6.QtCore import Qt, QProcess, Slot, QByteArray
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel

class PyGnuplot(QLabel):
    def __init__(self, parent = None):
        super(PyGnuplot, self).__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.process = QProcess()
        self.process.finished.connect(self.show_plot)
        self.process.errorOccurred.connect(self.show_error)

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
        # msg = bytes(cmd, 'utf8')
        msg = cmd
        size = len(msg)
        self.process.writeData(msg, size)

    @Slot(QProcess.ProcessError)
    def show_error(self, error):
        msg = ['Failed to Start', 'Crashed', 'Timedout', 'WriteError',
            'ReadError', 'UnknownError']
        self.setText('ProcessError: ' + msg[error])

    @Slot(int)
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
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    gnuplot = PyGnuplot()
    gnuplot.resize(451, 322)
    gnuplot.plot('plot sin(2*x)/x')
    gnuplot.setText("Waiting for gnuplot to finish...")
    gnuplot.show()
    sys.exit(app.exec())
