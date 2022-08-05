#!/usr/bin/env python3

"""

A SOLPS getIDS plugin for Qt designer.

"""

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from get_edge_ids import GetIDS

class getIDSplugin(QDesignerCustomWidgetInterface):
    """Plugin for put_edge_ids functionality.
    """
    def __init__(self, parent=None):
        super(getIDSplugin, self).__init__(parent)

    def createWidget(self, parent):
        return GetIDS(parent)

    def name(self):
        return "GetIDS"

    def group(self):
        return "SOLPS"

    def icon(self):
        return QIcon(_logo_pixmap)

    def toolTip(self):
        return "Push button for putting data to IDS data entry."

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def domXml(self):
        return '<ui language="c++" displayname="GetIDS">\n' \
               ' <widget class="GetIDS" name="get_edge_ids">\n' \
               '  <property name="toolTip" >\n' \
               '   <string>Push button for putting data to IDS data entry</string>\n' \
               '  </property>\n' \
               '  <property name="whatsThis" >\n' \
               '   <string>Push button for putting data to IDS data entry</string>' \
               '  </property>\n' \
               '  <property name="text"><string>GetIDS</string></property>' \
               ' </widget>\n' \
               '</ui>'

    def includeFile(self):
        return "get_edge_ids"

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