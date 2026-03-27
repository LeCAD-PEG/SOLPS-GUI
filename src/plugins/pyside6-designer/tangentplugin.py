#!/usr/bin/env python3

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from tangent import TangentActor


class TangentPlugin(QDesignerCustomWidgetInterface):

    def __init__(self, parent=None):
        super(TangentPlugin, self).__init__(parent)
        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return TangentActor(parent)

    def name(self):
        return "TangentActor"

    def group(self):
        return "SOLPS"

    def icon(self):
        return QIcon(_logo_pixmap)

    def toolTip(self):
        return "SOLPS tangent compile/run workflow."

    def whatsThis(self):
        return "SOLPS tangent compile/run workflow."

    def isContainer(self):
        return False

    def domXml(self):
        return (
            '<ui language="c++" displayname="Tangent">\n'
            ' <widget class="TangentActor" name="tangentActor">\n'
            '  <property name="toolTip">\n'
            '   <string>SOLPS tangent compile/run workflow.</string>\n'
            '  </property>\n'
            '  <property name="whatsThis">\n'
            '   <string>SOLPS tangent compile/run workflow.</string>\n'
            '  </property>\n'
            ' </widget>\n'
            '</ui>\n'
        )

    def includeFile(self):
        return "tangent"


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
"!!!!))!!!!!!!!!!"
]

_logo_pixmap = QPixmap(_logo_16x16_xpm)