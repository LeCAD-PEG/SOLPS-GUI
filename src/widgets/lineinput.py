#!/usr/bin/env python3

"""

A PyQt custom widget with Line edit capabilities and input triggering.

"""

from PyQt5.QtCore import (Qt, QProcess, QSize, pyqtProperty,
                          pyqtSignal, pyqtSlot)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QComboBox


class LineInput(QComboBox):
    """LineInput(QComboBox)
    
    Provides a custom widget that allows several commands to be
    combinined for Line input.
    """

    returnPressed = pyqtSignal()
    
    def __init__(self, parent=None):
        super(LineInput, self).__init__(parent)

        self.process = QProcess()
        self.setEditable(True)

    @pyqtSlot()
    def triggerTextChanged(self):
        """ Connector that receives a signal and re-emits the current text.
        """
        current_text = self.currentText()
        self.editTextChanged.emit(current_text)
        self.currentTextChanged.emit(current_text)

    def keyPressEvent(self, event):
        """ Catch each key and emit plot command when Return is pressed.
        """
        super(LineInput, self).keyPressEvent(event)
        if event.key() == Qt.Key_Return:
            self.returnPressed.emit()


if __name__ == "__main__":

    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = LineInput()
    window.show()
    sys.exit(app.exec_())


