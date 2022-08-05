#!/usr/bin/env python3

"""
divgeoplugin.py

A divgeo http://www.divgeo.info/ custom widget plugin for Qt Designer.

"""

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import QRect

from divgeo import DivGeo


class DivGeoPlugin(QDesignerCustomWidgetInterface):
    """DivGeoPlugin(QDesignerCustomWidgetInterface)

    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin via a PyQt-specific custom plugin class.
    """

    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):

        super(DivGeoPlugin, self).__init__(parent)

        self.initialized = False

    # The initialize() and isInitialized() methods allow the plugin to set up
    # any required resources, ensuring that this can only happen once for each
    # plugin.
    def initialize(self, core):

        if self.initialized:
            return

        self.initialized = True

    def isInitialized(self):

        return self.initialized

    # This factory method creates new instances of our custom widget with the
    # appropriate parent.
    def createWidget(self, parent):
        x = DivGeo(parent)
        x.labelContainer.setFrameStyle(QFrame.StyledPanel)
        return x

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "DivGeo"

    # Returns the name of the group in Qt Designer's widget box that this
    # widget belongs to.
    def group(self):
        return "SOLPS"

    # Returns the icon used to represent the custom widget in Qt Designer's
    # widget box.
    def icon(self):
        return QIcon(_logo_pixmap)

    # Returns a short description of the custom widget for use in a tool tip.
    def toolTip(self):
        return "DivGeo plugin with TCSH for SOLPS plots"

    # Returns a short description of the custom widget for use in a "What's
    # This?" help message for the widget.
    def whatsThis(self):
        return "DivGeo plugin with TCSH for SOLPS plots"

    # Returns True if the custom widget acts as a container for other widgets;
    # otherwise returns False. Note that plugins for custom containers also
    # need to provide an implementation of the QDesignerContainerExtension
    # interface if they need to add custom editing support to Qt Designer.
    def isContainer(self):
        return False

    # Returns an XML description of a custom widget instance that describes
    # default values for its properties. Each custom widget created by this
    # plugin will be configured using this description.
    def domXml(self):
        return '<ui language="c++" displayname="DivGeo">\n' \
               ' <widget class="DivGeo" name="divgeo" >\n' \
               ' </widget>\n' \
               '</ui>'


    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "divgeo"


# Define the image used for the icon.
_logo_16x16_xpm = [
"16 16 17 1",
"       c None",
".      c #000100",
"+      c #5F53C8",
"@      c #5A60C6",
"#      c #867BD3",
"$      c #229AD8",
"%      c #7C88D5",
"&      c #A3A0DA",
"*      c #63BAB4",
"=      c #80B8DD",
"-      c #A9BCD5",
";      c #C4C2EC",
">      c #C5C8E5",
",      c #DEDAEC",
"'      c #E9EAF9",
")      c #FAFBFF",
"!      c #FDFFFC",
"!!!!)!!!!!!!!!!!",
"!!!,&>!)!......!",
"!!'#++;.........",
"!!&#!!...!!!!!!.",
"!)#'))..!!!!!!!!",
"!,#!)..'>!!!!!!!",
"!>&!!..)>!!.....",
"!;&!!..)>!!.....",
"!;&!!..)>!!!!!..",
"!>&!)..;'!!!!!..",
"!'%))!..!!!!!!..",
"!)%;!'...!!!!!..",
"!)=+#@,........!",
"!))$@;!!!.....!!",
"!!-*=;!!!!!!!!!!",
"!!!!))!!!!!!!!!!"]

_logo_pixmap = QPixmap(_logo_16x16_xpm)
