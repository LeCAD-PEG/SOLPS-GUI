#!/usr/bin/env python3

"""
pygnuplotwidget.py

A PyQt custom widget example for Qt Designer.

"""

from PyQt5.QtCore import Qt, QProcess, QSize, pyqtSlot, pyqtProperty
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QFrame


class PyGnuplotWidget(QLabel):
    """PyGnuplotWidget(QWidget)
    
    Provides a custom widget to display a gnuplot with properties and slots
    that can be used to customize its appearance.
    """
    
    def __init__(self, parent=None):
    
        super(PyGnuplotWidget, self).__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumSize(QSize(180, 100))
        self.setText("Gnuplot widget for SOLPS")
        self.process = QProcess()
        self.process.finished.connect(self.show_plot)
        self.process.started.connect(self.started)
        self.process.error.connect(self.show_error)



    def sizeHint(self):
    
        return QSize(320, 200)

    #def paintEvent(self, event):
    #    self.setText("Repaing requested")

    @pyqtSlot()
    def started(self):
        self.setText("Gnuplot process started.")

    def plot(self, plot_command):
        """ Start gnuplot and write commands in standard input.
            Executable requires absolute path. No ${PATH} possible!
            Pause command demonstrates artificial processing and
            can be removed for production.
        """
        cmd = 'set terminal gif size ' \
            + str(self.width()) + ', ' + str(self.height()) + '; ' \
            + plot_command  + '; quit;\n'
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
        print("Plot finished")
        if exit_status == 0:
            data = self.process.readAll()
            image = QImage()
            image.loadFromData(data)
            self.setPixmap(QPixmap.fromImage(image))
        else:
            self.setText('exit status = ' + str(exit_status))



    # The setAngle() setter method is also a slot.
    @pyqtSlot(int)
    def setAngle(self, angle):
        self._angle = min(max(0, angle), 360)
        self.update()
    
    #angle = pyqtProperty(int, getAngle, setAngle)

    """
    # The innerRadius property is implemented using the getInnerRadius() and
    # setInnerRadius() methods.

    # The setInnerRadius() setter method is also a slot.
    @pyqtSlot(int)
    def setInnerRadius(self, radius):
        self._innerRadius = radius
        self.createPath()
        self.createGradient()
        self.update()
    
    innerRadius = pyqtProperty(int, getInnerRadius, setInnerRadius)
    
    # The outerRadius property is implemented using the getOuterRadius() and
    # setOuterRadius() methods.
    
    def getOuterRadius(self):
        return self._outerRadius
    
    # The setOuterRadius() setter method is also a slot.
    @pyqtSlot(int)
    def setOuterRadius(self, radius):
        self._outerRadius = radius
        self.createPath()
        self.createGradient()
        self.update()
    
    outerRadius = pyqtProperty(int, getOuterRadius, setOuterRadius)
    
    # The numberOfSides property is implemented using the getNumberOfSides()
    # and setNumberOfSides() methods.
    
    def getNumberOfSides(self):
        return self._sides
    
    # The setNumberOfSides() setter method is also a slot.
    @pyqtSlot(int)
    def setNumberOfSides(self, sides):
        self._sides = max(3, sides)
        self.createPath()
        self.update()
    
    numberOfSides = pyqtProperty(int, getNumberOfSides, setNumberOfSides)
    
    # The innerColor property is implemented using the getInnerColor() and
    # setInnerColor() methods.
    
    def getInnerColor(self):
        return self._innerColor
    
    def setInnerColor(self, color):
        self._innerColor = max(3, color)
        self.createGradient()
        self.update()
    
    innerColor = pyqtProperty(QColor, getInnerColor, setInnerColor)
    
    # The outerColor property is implemented using the getOuterColor() and
    # setOuterColor() methods.
    
    def getOuterColor(self):
        return self._outerColor
    
    def setOuterColor(self, color):
        self._outerColor = color
        self.createGradient()
        self.update()
    
    outerColor = pyqtProperty(QColor, getOuterColor, setOuterColor)
    """

if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    window = PyGnuplotWidget()
    window.show()
    sys.exit(app.exec_())
