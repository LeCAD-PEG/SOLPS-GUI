   #!/usr/bin/env python3
""" A PyQt custom Script widget.
"""

from PyQt5.QtCore import (QProcess, QSize, pyqtSignal, QSettings,
                          pyqtSlot, pyqtProperty)
from PyQt5.QtWidgets import QPlainTextEdit, QFrame
from PyQt5.QtGui import QFont

import logging
import os

class Script(QPlainTextEdit):
    """ Script(QPlainTextEdit)
    
        Provides a custom widget to display a gnuplot with properties and slots
        that can be used to customize its appearance.
    """

    output = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(Script, self).__init__(parent)
        #self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumSize(QSize(180, 50))
        self.setPlaceholderText("Python script widget. "
                                "Use self.output.emit(command) to signal.")
        font = QFont()
        font.setFamily('Monospace')
        self.setFont(font)

    def sizeHint(self):
        return QSize(320, 100)

    @pyqtSlot()
    def run(self):
        script = self.toPlainText()
        exec(script)

    @pyqtSlot(str)
    def setScript(self, script):
        self.setPlainText(script)

    def getScript(self):
        return self.toPlainText()

    script = pyqtProperty(str, getScript, setScript)
if __name__ == "__main__":

    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget = Script()
    script = """self.output.emit('pwd')
for i in range(10):
   cmd = "install -d run{0:02d}".format(i)
   print(cmd)
   self.output.emit(cmd)
    """
    widget.setPlainText(script)
    widget.show()
    widget.run()
    sys.exit(app.exec_())
