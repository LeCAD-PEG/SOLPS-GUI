import xml.etree.ElementTree as ET
from PySide6.QtGui import  QStandardItemModel, QStandardItem, QIcon
from PySide6.QtWidgets import QTreeView, QApplication
from PySide6.QtCore import (QFile, Qt, QItemSelection, QTextStream, 
            QIODevice, Signal)
from numpy import select
from numpy.core.defchararray import isspace
import pdsicons, designericons

class IconTree(QTreeView):

    icon_path = Signal(str) #: |Signal| emitting icon resource path

    def __init__(self, parent=None) -> None:
        """ Provides selection of icons from PDS and |QD| resources for
            inclusion in ``actor.icon`` for StudyExplorer and |QD| use.
        """
        super().__init__(parent)
        self.setHeaderHidden(True)
        file = QFile(":/iter.org/pds/icons/pdsicons.qrc")
        file.open(QIODevice.ReadOnly | QIODevice.Text)
        infile = QTextStream(file)
        rcc_xml = infile.readAll()
        file.close()
        wb_xml = ET.fromstring(XML_WB)
        pds_xml = ET.fromstring(rcc_xml)
        mdl = QStandardItemModel()
        self.setModel(mdl)
        self.parse_RCC_elementtree(mdl, pds_xml)
        self.parse_widgetbox_elementtree(mdl, wb_xml)
        self.expandAll()

    def parse_widgetbox_elementtree(self, parent, node):
        for element in node:
            item = QStandardItem()
            attribs = ' '.join([f'{key}="{value}"' for key, value in element.attrib.items()])
            if element.text != None and not isspace(element.text): 
                text = element.text
            else:
                text = ""
            name = element.attrib.get('name')
            icon = element.attrib.get('icon')
            if icon: 
                icon = ':/qt-project.org/formeditor/images/' + icon
                item.setIcon(QIcon(icon))
            #item.setData(f"{element.tag} {attribs} {text}" , Qt.DisplayRole)
            item.setData(name, Qt.DisplayRole)
            item.setData(icon, Qt.UserRole)
            self.parse_widgetbox_elementtree(item, element)
            if name:
                parent.appendRow(item)

    def parse_RCC_elementtree(self, parent, node):
        for element in node:
            item = QStandardItem()
            if element.tag == 'qresource':
                name = 'ITER icons'
            else:
                name = element.attrib.get('name')
            if alias := element.attrib.get('alias'):
                icon_path = ':/iter.org/pds/icons/' + alias
                item.setIcon(QIcon(icon_path))
                item.setData(icon_path, Qt.UserRole)

            item.setData(name, Qt.DisplayRole)
            self.parse_RCC_elementtree(item, element)
            if name:
                parent.appendRow(item)

        
    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        size = selected.size()
        if size > 0:
            r=selected.at(0)
            index = selected.indexes()[0]
            item = self.model().itemFromIndex(index)
            data = item.data(Qt.UserRole)
            if (data):
                self.icon_path.emit(data)
            else:
                self.icon_path.emit('')
        return super().selectionChanged(selected, deselected)


XML_WB='''
<!--
// Copyright (C) 2016 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
-->
<WB>
<widgetbox name="Widget Box icons" version="4.2">
    <category name="Layout">
        <categoryentry name="Vertical Layout" icon="win/editvlayout.png"/>
        <categoryentry name="Horizontal Layout" icon="win/edithlayout.png"/>
        <categoryentry name="Grid Layout" icon="win/editgrid.png"/>
        <categoryentry name="Form Layout" icon="win/editform.png"/>
    </category>
    <category name="Spacers">
       <categoryentry name="Horizontal Spacer" icon="widgets/spacer.png"/>
       <categoryentry  name="Vertical Spacer" icon="widgets/vspacer.png"/>
    </category>
    <category name="Buttons">
        <categoryentry name="Push Button" icon="widgets/pushbutton.png"/>
        <categoryentry name="Tool Button" icon="widgets/toolbutton.png"/>
        <categoryentry name="Radio Button" icon="widgets/radiobutton.png"/>
        <categoryentry name="Check Box" icon="widgets/checkbox.png"/>
        <categoryentry name="Command Link Button" icon="widgets/commandlinkbutton.png"/>
        <categoryentry name="Dialog Button Box" icon="widgets/dialogbuttonbox.png"/>
    </category>
    <category name="Item Views (Model-Based)">
        <categoryentry name="List View" icon="widgets/listbox.png"/>
        <categoryentry name="Tree View" icon="widgets/listview.png"/>
        <categoryentry name="Table View" icon="widgets/table.png"/>
        <categoryentry name="Column View" icon="widgets/columnview.png"/>
        <categoryentry name="Undo View" icon="widgets/listbox.png"/>
    </category>
    <category name="Item Widgets (Item-Based)">
        <categoryentry name="List Widget" icon="widgets/listbox.png"/>
        <categoryentry name="Tree Widget" icon="widgets/listview.png"/>
        <categoryentry name="Table Widget" icon="widgets/table.png"/>
    </category>
    <category name="Containers">
        <categoryentry name="Group Box" icon="widgets/groupbox.png"/>
        <categoryentry icon="widgets/scrollarea.png"  type="default" name="Scroll Area"/>
        <categoryentry name="Tool Box" icon="widgets/toolbox.png"/>
        <categoryentry name="Tab Widget" icon="widgets/tabwidget.png"/>
        <categoryentry name="Stacked Widget" icon="widgets/widgetstack.png"/>
        <categoryentry name="Frame" icon="widgets/frame.png"/>
        <categoryentry name="Widget" icon="widgets/widget.png"/>
        <categoryentry name="MDI Area" icon="widgets/mdiarea.png"/>
        <categoryentry name="Dock Widget" icon="widgets/dockwidget.png"/>
    </category>
    <category name="Input Widgets">
        <categoryentry name="Combo Box" icon="widgets/combobox.png"/>
        <categoryentry  name="Font Combo Box" icon="widgets/fontcombobox.png"/>
        <categoryentry name="Line Edit" icon="widgets/lineedit.png"/>
        <categoryentry name="Text Edit" icon="widgets/textedit.png"/>
        <categoryentry name="Plain Text Edit" icon="widgets/plaintextedit.png"/>
        <categoryentry name="Spin Box" icon="widgets/spinbox.png"/>
        <categoryentry name="Double Spin Box" icon="widgets/doublespinbox.png"/>
        <categoryentry name="Time Edit" icon="widgets/timeedit.png"/>
        <categoryentry name="Date Edit" icon="widgets/dateedit.png"/>
        <categoryentry name="Date/Time Edit" icon="widgets/datetimeedit.png"/>
        <categoryentry name="Dial" icon="widgets/dial.png"/>
        <categoryentry name="Horizontal Scroll Bar" icon="widgets/hscrollbar.png"/>
        <categoryentry name="Vertical Scroll Bar" icon="widgets/vscrollbar.png"/>
        <categoryentry name="Horizontal Slider" icon="widgets/hslider.png"/>
        <categoryentry name="Vertical Slider" icon="widgets/vslider.png"/>
        <categoryentry name="Key Sequence Edit" icon="widgets/lineedit.png"/>
    </category>
    <category name="Display Widgets">
        <categoryentry name="Label" icon="widgets/label.png"/>
        <categoryentry name="Text Browser" icon="widgets/textedit.png"/>
        <categoryentry name="Graphics View" icon="widgets/graphicsview.png"/>
        <categoryentry name="Calendar Widget" icon="widgets/calendarwidget.png"/>
        <categoryentry name="LCD Number" icon="widgets/lcdnumber.png"/>
        <categoryentry name="Progress Bar" icon="widgets/progress.png"/>
        <categoryentry name="Horizontal Line" icon="widgets/line.png"/>
        <categoryentry name="Vertical Line" icon="widgets/vline.png"/>
        <categoryentry name="OpenGL Widget" icon="widgets/widget.png"/>
    </category>
</widgetbox>
</WB>
'''

 
if __name__ == '__main__':
    app = QApplication([])
    win = IconTree()
    win.show()
    app.exec()
