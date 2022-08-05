#!/usr/bin/env python3

"""
gnuplotplugin.py

A gnuplot http://www.gnuplot.info/ custom widget plugin for Qt Designer.

"""

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtDesigner import (QDesignerCustomWidgetInterface,
                              QPyDesignerTaskMenuExtension,
                              QExtensionFactory,
                              QDesignerFormWindowInterface,
                              QDesignerTaskMenuExtension)
from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QSpinBox,
                             QLabel, QGridLayout)
from PySide6.QtCore import QVariantAnimation

from gnuplot import Gnuplot


class GnuplotDialog(QDialog):
    def __init__(self, widget, parent=None):
        super(GnuplotDialog, self).__init__(parent)

        self.widget = widget

        buttonBox = QDialogButtonBox()
        okButton = buttonBox.addButton(buttonBox.Ok)
        cancelButton = buttonBox.addButton(buttonBox.Cancel)

        self.rowSpin = QSpinBox()
        self.rowSpin.setMinimum(1)

        self.columnSpin = QSpinBox()
        self.columnSpin.setMinimum(1)

        okButton.clicked.connect(self.updateProperties)
        cancelButton.clicked.connect(self.reject)

        layout = QGridLayout()

        layout.addWidget(QLabel(self.tr('# of Rows:')), 0, 0)
        layout.addWidget(self.rowSpin, 0, 1)
        layout.addWidget(QLabel(self.tr('# of Columns:')), 1, 0)
        layout.addWidget(self.columnSpin, 1, 1)
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(layout)
        self.setWindowTitle(self.tr("Update row and column properties"))

    def updateProperties(self):
        formWindow = QDesignerFormWindowInterface.findFormWindow(self.widget)

        if formWindow:
            formWindow.cursor().setProperty("numberOfRows",
                                            self.rowSpin.value())
            formWindow.cursor().setProperty("numberOfColumns",
                                            self.columnSpin.value())

        self.accept()


class GnuplotMenuEntry(QPyDesignerTaskMenuExtension):

    def __init__(self, widget, parent):
        super(GnuplotMenuEntry, self).__init__(parent)
        self.widget = widget
        self.editNumOfWidgets = QAction(self.tr("# of Gnuplots..."), self)
        self.editNumOfWidgets.triggered.connect(self.changeNumberOfPlots)

    def preferredEditAction(self):
        return self.editNumOfWidgets

    def taskActions(self):
        return [self.editNumOfWidgets]

    def changeNumberOfPlots(self):
        dialog = GnuplotDialog(self.widget)
        dialog.exec_()


class GnuplotTaskMenuFactory(QExtensionFactory):

    def __init__(self, parent=None):
        super(GnuplotTaskMenuFactory, self).__init__(parent)

    def createExtension(self, obj, ID, parent):
        if ID != "solps.TaskMenu":
            return None

        if isinstance(obj, Gnuplot):
            print('instanced')
            return GnuplotMenuEntry(obj, parent)

        return None


class GnuplotPlugin(QDesignerCustomWidgetInterface):
    """GnuplotPlugin(QDesignerCustomWidgetInterface)

    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin via a PyQt-specific custom plugin class.
    """

    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):

        super(GnuplotPlugin, self).__init__(parent)

        self.initialized = False

    # The initialize() and isInitialized() methods allow the plugin to set up
    # any required resources, ensuring that this can only happen once for each
    # plugin.
    def initialize(self, formEditor):

        if self.initialized:
            return
        manager = formEditor.extensionManager()
        if manager:
            self.factory = GnuplotTaskMenuFactory(manager)
            manager.registerExtensions(self.factory,
                                       "solps.TaskMenu")
        self.initialized = True

    def isInitialized(self):

        return self.initialized

    # This factory method creates new instances of our custom widget with the
    # appropriate parent.
    def createWidget(self, parent):
        return Gnuplot(parent)

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "Gnuplot"

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
        return "Gnuplot plugin with TCSH for SOLPS plots"

    # Returns a short description of the custom widget for use in a "What's
    # This?" help message for the widget.
    def whatsThis(self):
        return "Gnuplot plugin with TCSH for SOLPS plots"

    # Returns True if the custom widget acts as a container for other widgets;
    # otherwise returns False. Note that plugins for custom containers also
    # need to provide an implementation of the QDesignerContainerExtension
    # interface if they need to add custom editing support to Qt Designer.
    def isContainer(self):
        return True

    # Returns an XML description of a custom widget instance that describes
    # default values for its properties. Each custom widget created by this
    # plugin will be configured using this description.
    def domXml(self):
        return '<ui language="c++" displayname="Gnuplot">\n' \
               ' <widget class="Gnuplot" name="gnuplot">\n' \
               '  <property name="toolTip" >\n' \
               '   <string>Gnuplot plugin with TCSH for SOLPS plots</string>\n' \
               '  </property>\n' \
               '  <property name="whatsThis" >\n' \
               '   <string>Gnuplot plugin with TCSH for SOLPS plots</string>' \
               '  </property>\n' \
               '  <property name="text"><string>Gnuplot</string></property>' \
               ' </widget>\n' \
               '</ui>'

    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "gnuplot"


# Define the image used for the icon.
_logo_16x16_xpm = [
    "16 16 16 1",
    "       c #000100",
    ".      c #4C56A4",
    "+      c #66757B",
    "@      c #32AD88",
    "#      c #A0A55D",
    "$      c #D083EF",
    "%      c #B7B8B7",
    "&      c #ABCE69",
    "*      c #CBAED3",
    "=      c #DFBBF0",
    "-      c #B4E2D2",
    ";      c #E8D3D6",
    ">      c #DEDFDA",
    ",      c #FFEC8D",
    "'      c #EBECEA",
    ")      c #FDFFFB",
    "))))))))))))))))",
    "  )) )))) ))   )",
    " ) ) ))) ) )) ))",
    " ) ) ))) ) )) ))",
    "  )) ))) ) )) ))",
    " )))   )) ))) ))",
    "'>'>'>'>'>'>'>'>",
    ")'';>;>%>;>))))'",
    "''-''''''-)))))'",
    ">')>'>'''@)))))'",
    ")';'''''-@'))))'",
    "''))))))-@-,)))'",
    "''))))''@@&,,))'",
    "'');=$$$.+#,,,)'",
    ");=====*%*%*;>>'",
    "%%%%%%%%%%%%%%%%"]

_logo_pixmap = QPixmap(_logo_16x16_xpm)
