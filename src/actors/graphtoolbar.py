from PySide6.QtCore import  QSize, Property, Slot, Signal, Qt, QEvent, QRect
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QPlainTextEdit, 
                                QFrame, QLabel, QLineEdit)
from PySide6.QtGui import QPalette, QBrush, QColor, QDoubleValidator
import xml.etree.ElementTree as ET

from PySide6.QtWidgets import QWidget


class GraphToolbar(QWidget):
    """ Graphical actor
    """

    icon = ':/qt-project.org/formeditor/images/widgets/toolbutton.png'
    toolbarData = Signal(list) #: Signal(list): |Signal| for emitting toolbar data containing (_activeButton, _x, _y).
    _activeButton = 0 # 0=Select, 1=Move, 2=Add, 3=Delete
    _x = 0
    _y = 0
    #_running_state = 0 # 0=not started, 1=started, 2=finished

    def __init__(self, parent=None):
        """Default constructor.
        """
        super().__init__(parent)
        self._layout = QHBoxLayout(self) #: Sample horizontal layout 
       
        self._pushButton1 = QPushButton("Sel.")
        self._pushButton2 = QPushButton("Move")
        self._pushButton3 = QPushButton("Add")
        self._pushButton4 = QPushButton("Del.")
        self._pushButton1.setMaximumWidth(50)
        self._pushButton2.setMaximumWidth(50)
        self._pushButton3.setMaximumWidth(50)
        self._pushButton4.setMaximumWidth(50)
        self._layout.addWidget(self._pushButton1)
        self._layout.addWidget(self._pushButton2)
        self._layout.addWidget(self._pushButton3)
        self._layout.addWidget(self._pushButton4)

        self._labelx = QLabel()
        self._labelx.setText("   x:")
        self._layout.addWidget(self._labelx)

        self._lineEditx = QLineEdit()
        self._lineEditx.setValidator(QDoubleValidator())
        self._lineEditx.editingFinished.connect(self.update_valuex)
        self._lineEditx.returnPressed.connect(self.update_valuex)
        self._layout.addWidget(self._lineEditx)
        
        self._labely = QLabel()        
        self._labely.setText("   y:")        
        self._layout.addWidget(self._labely)        
        
        self._lineEdity = QLineEdit()
        self._lineEdity.setValidator(QDoubleValidator())
        self._lineEdity.editingFinished.connect(self.update_valuey)
        self._lineEdity.returnPressed.connect(self.update_valuey)
        self._layout.addWidget(self._lineEdity)

        # self._start_button = QPushButton("Start")
        # self._layout.addWidget(self._start_button)
                
        self._pushButton1.clicked.connect(self.buttonClicked)
        self._pushButton2.clicked.connect(self.buttonClicked)
        self._pushButton3.clicked.connect(self.buttonClicked)
        self._pushButton4.clicked.connect(self.buttonClicked)

        self._palette = QPalette()
        brush = QBrush(QColor(239, 239, 239, 0))
        brush.setStyle(Qt.SolidPattern)
        self._palette.setBrush(QPalette.Active, QPalette.Button, brush)
        self._palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        self._palette.setBrush(QPalette.Disabled, QPalette.Button, brush)

        self._paletteGreen = QPalette()
        brush = QBrush(QColor(100, 255, 100, 0))
        brush.setStyle(Qt.SolidPattern)
        self._paletteGreen.setBrush(QPalette.Active, QPalette.Button, brush)
        self._paletteGreen.setBrush(QPalette.Inactive, QPalette.Button, brush)
        self._paletteGreen.setBrush(QPalette.Disabled, QPalette.Button, brush)
        
        self._pushButton1.setPalette(self._paletteGreen)

        #self._lineEditx.update
        


    def minimumSizeHint(self):
        """This property holds the recommended minimum size for the widget.
        """
        return QSize(200, 200)

    def sizeHint(self):
        """This property holds the recommended size for the widget.
        """
        return QSize(200, 200)


    def get_state(self) -> ET.Element:
        """ Gets the current state of the widget, e.g. for saving the state 
            into the study file.
        """
        _state = ET.Element({})
        _state.tag = self.objectName()
        _state.text = ""
        return _state

    def set_state(self, _state: ET.Element):
        """ Sets the state of the widget, e.g. after loading the state 
            from the study file.

            Args:
                state(Element): |XML| study file.
        """  
        state = _state.text

    @Slot()
    def buttonClicked(self):
        match self.sender():
            case self._pushButton1:
                self._activeButton = 1
                self._pushButton1.setPalette(self._paletteGreen)
                self._pushButton2.setPalette(self._palette)
                self._pushButton3.setEnabled(True)
                self._pushButton4.setEnabled(True)
            case self._pushButton2:
                self._activeButton = 2
                self._pushButton1.setPalette(self._palette)
                self._pushButton2.setPalette(self._paletteGreen)
                self._pushButton3.setEnabled(False)
                self._pushButton4.setEnabled(False)
            case self._pushButton3:
                self._activeButton = 3
            case self._pushButton4:
                self._activeButton = 4
            case _:
                self._activeButton = -1
        
        self.toolbarData.emit([self._activeButton,self._x,self._y])

    def update_valuex(self):   
        txt = self._lineEditx.text()
        if not txt:
            self._x = 0
        else:
            self._x = float(txt)

    def update_valuey(self):        
        txt = self._lineEdity.text()
        if not txt:
            self._y = 0
        else:
            self._y = float(txt)


    # def _pause(self):
    #     """ Pause or continue self.
    #     """
    #     pass

    # def _stop(self):
    #     """ Stop self.
    #     """
    #     pass

    def _show_or_hide(self, dynamic_property_name: str, widget: QWidget) -> bool:
        """ Depending on the dynamic_property_name the widget is shown or
            hiden.

            Args:
            dynamic_property_name: name of the dynamic property
            widget: widget to be shown or hiddenn
        """
        property = self.property(dynamic_property_name)
        if property is None:
            return None
        if property:
            widget.show()
            return True
        else:
            widget.hide()
        return False


    # def event(self, received : QEvent) -> bool:
    #     if received.type() == QEvent.DynamicPropertyChange:
    #         name = bytes(received.propertyName()).decode()
    #         if name == 'title':
    #             self._title.setText(self.property('title'))
    #             return True
    #         if name == 'button':
    #             self._start_button.setText(self.property('button'))
    #             return True
    #         if name == 'show_button':
    #             self._show_or_hide('show_button', self._start_button)
    #             return True
    #         if name == 'show_log':
    #             self._show_or_hide('show_log', self._log)
    #             return True
    #         if name == 'show_title':
    #             self._show_or_hide('show_title', self._title)
    #             return True
    #     return super().event(received)

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtUiTools import loadUiType

    uiclass, baseclass = loadUiType("../designer/graphtoolbar.ui")

    class MainWindow(uiclass, baseclass):
        def __init__(self):
            super().__init__()
            self.setupUi(self)

    # from actor import Actor

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())