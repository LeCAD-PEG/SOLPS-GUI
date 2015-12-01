#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel

class PyGnuplot(QLabel):
    def __init__(self, parent = None):
        super(PyGnuplot, self).__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        
    def plot(self, plot_command):
        self.gnuplot = QProcess()
        cmd = 'set terminal gif size ' \
            + str(self.width()) + ', ' + str(self.height()) + '; ' \
            + 'pause 3; ' + plot_command
        self.gnuplot.start("gnuplot", ['-e', cmd])
        if not self.gnuplot.waitForStarted():
            self.setText("Error: gnuplot not started!")
            return False
        if not self.gnuplot.waitForFinished():
            self.setText("Error: gnuplot not finished")
            return False
        data = self.gnuplot.readAll()
        image = QImage()
        image.loadFromData(data)
        self.setPixmap(QPixmap.fromImage(image))
        return True



if __name__ == '__main__':

    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    gnuplot = PyGnuplot()
    gnuplot.resize(451, 322)
    gnuplot.plot('plot sin(2*x)/x')
    gnuplot.show()
    sys.exit(app.exec_())
