#!/usr/bin/env python3
""" A PyQt custom Python Script widget.
"""

from PySide6.QtCore import QSize, Signal, Slot, Property
from PySide6.QtWidgets import QPlainTextEdit, QFrame
from PySide6.QtGui import QFont


class Script(QPlainTextEdit):
    """ Script(QPlainTextEdit)

        Provides a custom widget to display a box where Python script
        can be entered and run.
    """

    output = Signal(str)

    def __init__(self, parent=None):
        super(Script, self).__init__(parent)
        # self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMinimumSize(QSize(180, 50))
        self.setPlaceholderText("Python script widget. "
                                "Use self.output.emit(command) to signal.")
        font = QFont()
        font.setFamily('Monospace')
        self.setFont(font)

    def sizeHint(self):
        return QSize(320, 100)

    @Slot()
    def run(self):
        script = self.toPlainText()
        exec(script)

    @Slot(str)
    def setScript(self, script):
        self.setPlainText(script)

    def getScript(self):
        return self.toPlainText()

    script = Property(str, getScript, setScript)


if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication
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
    sys.exit(app.exec())
