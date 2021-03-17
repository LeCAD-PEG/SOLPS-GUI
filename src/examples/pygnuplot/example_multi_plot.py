from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, QVBoxLayout,
                             QPlainTextEdit)
from PyQt5.QtCore import QPointF, QTimer, pyqtSlot
from QtGnuplot import QtGnuplotWidget, QtGnuplotInstance
from random import random


class GnuplotWidget(QWidget):
    def __init__(self, parent=None, mainWindow=None):
        super(GnuplotWidget, self).__init__(parent)

        layout = QGridLayout()
        self.widgets = [None for i in range(4)]
        self.gp = QtGnuplotInstance()
        self.phi = 0
        self.timer = QTimer()
        self.mainWindow = mainWindow

        for i in range(4):
            self.widgets[i] = QtGnuplotWidget()
            self.widgets[i].statusTextChanged.connect(self.statusText)
            # self.widgets[i].setFixedSize(400, 250)
            layout.addWidget(self.widgets[i], i//2, i % 2)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout)

        self.outputFrame = QPlainTextEdit(self)
        self.outputFrame.setReadOnly(True)
        layout.addWidget(self.outputFrame)
        self.setLayout(mainLayout)
        self.gp.gnuplotOutput.connect(self.gnuplotOutput)

    def plot(self):
        self.gp.setWidget(self.widgets[0])
        self.gp << 'plot x w l lt 3\n'
        self.gp << 'print pi\n'

        self.gp.setWidget(self.widgets[1])

        self.gp << 'plot sin(x) lw 3 lt rgb "red", cos(x) lt rgb "blue"\n'

        self.gp.setWidget(self.widgets[2])
        points = []
        for i in range(100):
            points.append(QPointF(random(), random()))
        self.gp << "plot '-'\n"
        self.gp << points

        self.gp.setWidget(self.widgets[3])
        # self.gp << 'test\n'

        self.gp << 'unset grid\n'
        self.phi = 0
        self.gp << f'plot sin(x + {self.phi:.1f})\n'
        self.gp << f'print pi, {self.phi}\n'
        self.timer.timeout.connect(self.tick)
        self.timer.start(50)

    @pyqtSlot()
    def tick(self):
        self.gp << f'plot sin(x + {self.phi:.1f})\n'
        self.gp << f'print pi, {self.phi}\n'
        self.phi += 0.3

    def statusText(self, status: str) -> None:
        self.mainWindow.statusBar().showMessage(status)

    def gnuplotOutput(self, output: str) -> None:
        self.outputFrame.appendPlainText(output)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    import logging

    logging.basicConfig(level=logging.DEBUG)
    logging._srcfile = None
    logging.logThreads = 0
    logging.logProcesses = 0
    app = QApplication([])
    mainWindow = QMainWindow()

    widget = GnuplotWidget(parent=None, mainWindow=mainWindow)
    mainWindow.setCentralWidget(widget)
    mainWindow.statusBar().showMessage('Qt Gnuplot widgets embedding example')
    mainWindow.show()
    widget.plot()
    c = app.exec_()
    sys.exit(c)
