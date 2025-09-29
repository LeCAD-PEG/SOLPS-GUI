from PySide6.QtCore import  QSize, Property, Slot, Signal
from PySide6.QtWidgets import QVBoxLayout, QPushButton
from iplotlib.qt.gui.iplotCanvasToolbar import IplotQtCanvasToolbar
from iplotlib.qt.gui.iplotQtPreferencesWindow import QWidget
from PySide6.QtGui import QShowEvent
 
 



class IPlotToolbar(IplotQtCanvasToolbar):

    icon = ":/iter.org/pds/icons/menu.png"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._toolbar_emit = False

    def minimumSizeHint(self):
        return QSize(400, 16)

    def sizeHint(self):
        return QSize(560, 20)
        
    def showEvent(self, event: QShowEvent) -> None:
        if not self._toolbar_emit: # one-shot emit
            self.toolbar.emit(self)
            self._toolbar_emit = True
        return super().showEvent(event)

    toolbar = Signal(QWidget)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtUiTools import loadUiType

    uiclass, baseclass = loadUiType("../designer/iplottoolbar.ui")

    class MainWindow(uiclass, baseclass):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

    # from actor import Actor

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())