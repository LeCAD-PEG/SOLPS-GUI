from graph import Graph
#from graphtaskmenu import GraphTaskMenuFactory

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtDesigner import (QExtensionManager,
    QDesignerCustomWidgetInterface)

# Dynamic properties
DOM_XML = """
<ui language='c++'>
    <widget class='Graph' name='graph'>
        <property name='geometry'>
            <rect>
                <x>0</x>
                <y>0</y>
                <width>380</width>
                <height>120</height>
            </rect>
        </property>
    </widget>
</ui>
"""


class GraphPlugin(QDesignerCustomWidgetInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._form_editor = None

    def createWidget(self, parent):
        t = Graph(parent)
        return t

    def domXml(self):
        return DOM_XML

    def group(self):
        return 'IMAS Plot'

    def icon(self):
        return QIcon(_logo_pixmap)

    def includeFile(self):
        return 'graph'

    def initialize(self, form_editor):
        self._form_editor = form_editor
        #manager = form_editor.extensionManager()
        #iid = GraphTaskMenuFactory.task_menu_iid()
        #manager.registerExtensions(GraphTaskMenuFgraphy(manager), iid)

    def isContainer(self):
        return False

    def isInitialized(self):
        return self._form_editor is not None

    def name(self):
        return 'Graph'

    def toolTip(self):
        return 'Graphing for Transmak time dependent plots'

    def whatsThis(self):
        return self.toolTip()

# Define the image used for the icon.
_logo_16x16_xpm = [
    "16 16 12 1",
    "  c gray100",
    ". c #FF3333",
    "X c #CCFFFF",
    "o c #99CCFF",
    "O c #66CCFF",
    "+ c #CCCCFF",
    "@ c #CCFF33",
    "# c #99FFFF",
    "$ c #CCFFCC",
    "% c #99CCCC",
    "& c #FFCC66",
    "* c #66CCCC",
    "   XX      . .  ",
    "  OOoOX     . . ",
    " Xo   oX        ",
    " O     o    .   ",
    " o      X  . .  ",
    " o      X  .... ",
    " o      X       ",
    " o      X     . ",
    " o      X  .... ",
    " o     X        ",
    " X+    X    ..  ",
    "  O   o    .  . ",
    "  O++oX     ..  ",
    "  #*o%          ",
    "  $@&      . .  ",
    "            . . "]

_logo_pixmap = QPixmap(_logo_16x16_xpm)
    
