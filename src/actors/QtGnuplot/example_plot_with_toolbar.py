from PySide6.QtWidgets import (QMainWindow, QWidget, QGridLayout, QLineEdit)
from PySide6.QtCore import QTimer
from QtGnuplot import QtGnuplotWidget, QtGnuplotInstance, QtGnuplotBar


exampleScript = """set title "Simple Plots" font ",20"
set key left box
set samples 50
set style data points

plot [-10:10] sin(x),atan(x),cos(atan(x))
"""


class GnuplotWidget(QWidget):
    def __init__(self, parent=None, mainWindow=None):
        super(GnuplotWidget, self).__init__(parent)

        self.widgets = None
        self.gp = QtGnuplotInstance()
        self.phi = 0
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.mainWindow = mainWindow

        layout = QGridLayout()

        self.widget = QtGnuplotWidget(self)
        self.widget.statusTextChanged.connect(self.statusText)
        self.gp.setWidget(self.widget)
        layout.addWidget(self.widget, 0, 0)

        self.toolBar = QtGnuplotBar(parent=self, m_widget=self.widget)
        layout.addWidget(self.toolBar, 1, 0)

        self.lineInput = QLineEdit()
        self.lineInput.returnPressed.connect(self.gnuplotInput)

        layout.addWidget(self.lineInput, 2, 0)


        # self.outputFrame = QPlainTextEdit(self)
        # self.outputFrame.setReadOnly(True)
        # layout.addWidget(self.outputFrame)
        self.setLayout(layout)
        # self.gp.gnuplotOutput.connect(self.gnuplotOutput)

    def statusText(self, status: str) -> None:
        self.mainWindow.statusBar().showMessage(status)

    def gnuplotOutput(self, output: str) -> None:
        self.outputFrame.appendPlainText(output)

    def gnuplotInput(self):
        text = self.lineInput.text()
        if text:
            if text == "script":
                self.gp << exampleScript
            else:
                self.gp << f'{text}\n'
            self.lineInput.clear()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QIcon
    import sys
    import logging

    logging.basicConfig(level=logging.DEBUG)
    logging._srcfile = None
    logging.logThreads = 0
    logging.logProcesses = 0
    app = QApplication([])
    print("")
    mainWindow = QMainWindow()
    mainWindow.setWindowTitle("Gnuplot with toolbar")
    mainWindow.setWindowIcon(QIcon(":/images/gnuplot"))

    widget = GnuplotWidget(parent=None, mainWindow=mainWindow)
    mainWindow.setCentralWidget(widget)
    mainWindow.statusBar().showMessage('Qt Gnuplot widgets embedding example')
    mainWindow.show()
    # widget.plot()
    c = app.exec_()
    sys.exit(c)
