from PySide6.QtCore import  QSize, Property, Slot, Signal, Qt, QEvent
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QPlainTextEdit, QFrame, QLabel
import xml.etree.ElementTree as ET
{% if base_class == 'QtMatplotlibCanvas' %}
from iplotlib.impl.matplotlib.qt.qtMatplotlibCanvas import QtMatplotlibCanvas
{% elif base_class in ['QWidget', 'QPlainTextEdit' ] %}
from PySide6.QtWidgets import {{ base_class }}
{% elif base_class == 'PlotWidget' %}
from pyqtgraph import PlotWidget
{% elif base_class == 'FigureCanvasQTAgg' %}
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
{% endif %}

class {{ class_name }}({{ base_class }}):
    """ Graphical actor
    """

    icon = '{{ icon_path }}'
    finished = Signal()
    _running_state = 0 # 0=not started, 1=started, 2=finished

    def __init__(self, parent=None):
        """Default constructor.
        """
        super().__init__(parent)
        self._layout = QVBoxLayout(self) #: Sample vertical layout
        self._layout.setSpacing(2) 
        self._title = QLabel()
        self._title.setFrameStyle(QFrame.Box|QFrame.Sunken)
        self._title.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self._title) 
        self._log = QPlainTextEdit()
        self._log.setPlaceholderText("This is {{ class_name }} log.")
        self._layout.addWidget(self._log)
        self._start_button = QPushButton("Start")
        self._layout.addWidget(self._start_button)
        self._start_button.clicked.connect(self.compute)    

{% if size_hints %}
    def minimumSizeHint(self):
        """This property holds the recommended minimum size for the widget
        """
        return QSize(200, 200)

    def sizeHint(self):
        """This property holds the recommended size for the widget
        """
        return QSize(200, 200)
{% endif %}
{% if state %}
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
        """  
        state = _state.text
{% endif %}
    @Slot()
    def compute(self):
        self._running_state = 1
        self.finished.emit()
        self._running_state = 2

    def _pause(self):
        """ Pause or continue self.
        """
        pass

    def _stop(self):
        """ Stop self.
        """
        pass

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


    def event(self, received : QEvent) -> bool:
        if received.type() == QEvent.DynamicPropertyChange:
            name = bytes(received.propertyName()).decode()
            if name == 'title':
                self._title.setText(self.property('title'))
                return True
            if name == 'button':
                self._start_button.setText(self.property('button'))
                return True
            if name == 'show_button':
                self._show_or_hide('show_button', self._start_button)
                return True
            if name == 'show_log':
                self._show_or_hide('show_log', self._log)
                return True
            if name == 'show_title':
                self._show_or_hide('show_title', self._title)
                return True
        return super().event(received)

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtUiTools import loadUiType

    uiclass, baseclass = loadUiType("{{ designer_localPath }}/{{ name }}.ui")

    class MainWindow(uiclass, baseclass):
        def __init__(self):
            super().__init__()
            self.setupUi(self)

    # from actor import Actor

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())