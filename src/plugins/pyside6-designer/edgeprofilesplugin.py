#!/usr/bin/env python3

"""

A SOLPS 'Plot edge_profiles GGD' widget for Qt designer.

"""

from edgeprofiles import EdgeProfiles

from PySide6.QtGui import QAction
from PySide6.QtDesigner import (QExtensionManager, QExtensionFactory, 
    QPyDesignerTaskMenuExtension, QDesignerFormWindowInterface)
from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtUiTools import loadUiType 
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtDesigner import (QExtensionManager,
    QDesignerCustomWidgetInterface)


class EdgeProfilesPlugin(QDesignerCustomWidgetInterface):
    def __init__(self, parent=None):
        super(EdgeProfilesPlugin, self).__init__(parent)

    def createWidget(self, parent):
        t = EdgeProfiles(parent)
        return t

    def name(self):
        return 'EdgeProfiles'    

    def group(self):
        return 'SOLPS'

    def icon(self):
        return QIcon(_logo_pixmap)

    def toolTip(self):
        return 'Draws various edge profiles from SOLPS'

    def whatsThis(self):
        return 'This actor is part of SOLPS-ITER GUI'
        #return self.toolTip()

    def isContainer(self):
        return False

    def domXml(self):
        return '<ui language="c++" displayname="Edge Profiles">\n' \
               ' <widget class="EdgeProfiles" name="edgeprofiles">\n' \
               '        <property name="geometry">\n' \
               '        <rect>\n' \
               '             <x>0</x>\n' \
               '             <y>0</y>\n' \
               '             <width>300</width>\n' \
               '             <height>200</height>\n' \
               '         </rect>\n' \
               '     </property>\n' \
               '     <property name="pulse">\n' \
               '         <string notr="true" comment="(shot, run, usename, database, backend)"\n' \
               '         extracomment="Tuple of IDS parameters">(130012, 2, "public", "ITER", 12)</string>\n' \
               '     </property>\n' \
               '  <property name="toolTip" >\n' \
               '   <string>Draws various edge profiles from SOLPS</string>\n' \
               '  </property>\n' \
               '  <property name="whatsThis" >\n' \
               '   <string>This actor is part of SOLPS-ITER GUI</string>'\
               '  </property>\n' \
               '  <property name="text"><string>EdgeProfiles</string></property>' \
               ' </widget>\n' \
               '</ui>'    

    def includeFile(self):
        return 'edgeprofiles'

# Define the image used for the icon.
_logo_16x16_xpm = [
 "16 16 16 1",
" 	c #000100",
".	c #5F53C8",
"+	c #5A60C6",
"@	c #867BD3",
"#	c #229AD8",
"$	c #7C88D5",
"%	c #A3A0DA",
"&	c #63BAB4",
"*	c #80B8DD",
"=	c #A9BCD5",
"-	c #C4C2EC",
";	c #C5C8E5",
">	c #DEDAEC",
",	c #E9EAF9",
"'	c #FAFBFF",
")	c #FDFFFC",
"))))')))))) ) ))",
")))>%;)')))) ) )",
")),@..-)')))))))",
"))%@))$>)))) )))",
")'@,'')%))) ) ))",
")>@)')',;))    )",
");%)))'';)))))))",
")-%)))'';))))) )",
")-%)))'';))    )",
");%)'))-,)))))))",
"),$''),%))))  ))",
")'$-),$)')) )) )",
")'*.@+>'))))  ))",
")''#+-))))))))))",
"))=&*-))))) ) ))",
"))))'')))))) ) )"]

_logo_pixmap = QPixmap(_logo_16x16_xpm)
    