#!/usr/bin/python3

"""

A SOLPS putIDS plugin for Qt designer.

"""

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from put_edge_ids import PutIDS

class putIDSplugin(QPyDesignerCustomWidgetPlugin):
    """Plugin for put_edge_ids functionality.
    """
    def __init__(self, parent=None):
        super(putIDSplugin, self).__init__(parent)

    def createWidget(self, parent):
        return PutIDS(parent)

    def name(self):
        return "PutIDS"

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
        return '<widget class="PutIDS" name="put_edge_ids">\n</widget>'

    def includeFile(self):
        return "put_edge_ids"

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