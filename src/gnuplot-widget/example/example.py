from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from pyQtGnuplot import gnuplotWidget
import sys


class CmdInput(QLineEdit):
    sendCmd = pyqtSignal(str)
    def __init__(self, parent=None):
        super(CmdInput, self).__init__(parent)
        self.returnPressed.connect(self.sendCommand)

    @pyqtSlot()
    def sendCommand(self):
        text = self.text()
        self.sendCmd.emit(text)
        self.clear()

class Output(QPlainTextEdit):
    def __init__(self, parent=None):
        super(Output, self).__init__(parent)

    @pyqtSlot(str)
    def updateLog(self, str):
        self.appendPlainText(str)


app = QApplication(sys.argv)

main = QMainWindow()
main.setAttribute(Qt.WA_DeleteOnClose)
inputWidget = CmdInput()
gpw = gnuplotWidget()
gpw.setWindowTitle('Window title')
output = Output()
inputWidget.sendCmd.connect(gpw.cmd)
inputWidget.sendCmd.connect(output.updateLog)
gpw.gnuplotOutput.connect(output.updateLog)
layout = QVBoxLayout()


layout.addWidget(gpw)
layout.addWidget(inputWidget)
layout.addWidget(output)
window = QWidget()
window.setLayout(layout)
main.setCentralWidget(window)
main.show()
app.exec_()

