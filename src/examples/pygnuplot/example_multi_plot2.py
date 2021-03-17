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
        self.gp = [QtGnuplotInstance() for i in range(4)]
        self.phi = 0
        self.timer = QTimer()
        self.mainWindow = mainWindow

        for i in range(4):
            self.widgets[i] = QtGnuplotWidget()
            # self.widgets[i].statusTextChanged.connect(self.statusText)
            # self.widgets[i].setFixedSize(400, 250)
            self.gp[i].setWidget(self.widgets[i])
            layout.addWidget(self.widgets[i], i//2, i % 2)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout)

        self.outputFrame = QPlainTextEdit(self)
        self.outputFrame.setReadOnly(True)
        layout.addWidget(self.outputFrame)
        self.setLayout(mainLayout)
        # [self.gp[i].gnuplotOutput.connect(self.gnuplotOutput) for i in range(4)]

        # Force new resize to refresh gnuplot?
        [self.widgets[i].resize(self.widgets[i].sizeHint()) for i in range(4)]

    def plot(self):
        # self.gp[0].setWidget(self.widgets[0])
        self.gp[0] << 'plot x w l lt 3\n'
        self.gp[0] << 'print pi\n'

        # self.gp.setWidget(self.widgets[1])
        self.gp[1] << 'plot sin(x) lw 3 lt rgb "red", cos(x) lt rgb "blue"\n'

        points = []
        for i in range(100):
            points.append(QPointF(random(), random()))
        self.gp[2] << "plot '-'\n"
        self.gp[2] << points

        # self.gp.setWidget(self.widgets[3])
        # self.gp << 'test\n'

        self.gp[3] << 'unset grid\n'
        self.phi = 0
        self.gp[3] << f'plot sin(x + {self.phi:.1f})\n'
        self.gp[3] << f'print pi, {self.phi}\n'
        self.timer.timeout.connect(self.tick)
        # self.timer.start(500)

    @pyqtSlot()
    def tick(self):
        self.gp[3] << f'plot sin(x + {self.phi:.1f})\n'
        self.gp[3] << f'print pi, {self.phi}\n'
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
