   #!/usr/bin/env python3
""" A PyQt custom Menu widget that adds input parameters
"""

from PyQt5.QtCore import (QSize, pyqtSignal, QSettings,
                          pyqtSlot, pyqtProperty)
from PyQt5.QtWidgets import QMenu, QToolTip
from PyQt5.QtGui import QCursor

import logging
import os
import textwrap

from tooltips import b2mn_tooltips

class AddMenu(QMenu):
    """ Script(QPlainTextEdit)
    
        Provides a custom widget to display a gnuplot with properties and slots
        that can be used to customize its appearance.
    """

    output = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(AddMenu, self).__init__(parent)
        #self.setAlignment(Qt.AlignCenter)
        #self.menuAdd = QMenu(parent)
        #self.menuAdd.setTitle("Add")
        self.setTitle("Add")

        self.menuPhysics = QMenu(self)
        self.menuPhysics.setTitle("Physics")
        self.addAction(self.menuPhysics.menuAction())
        # self.menuPhysics.setToolTip("Physics switches")
        parent.addAction(self.menuAction())
        self.menuPhysics.hovered.connect(self.handleMenuHovered)

        b2mntooltips = dict()
        for parameter in sorted(b2mn_tooltips):
            category, param_type, default, description = b2mn_tooltips[parameter]
            if category == 'Physics':
                b2mntooltips[parameter] = parameter
                # menu = QMenu(self.menuPhysics)
                # menu.setTitle(parameter)
                action = self.menuPhysics.addAction(parameter)
                tooltip = '<pre><font color=blue><b>' + parameter + '</b> ' \
                          + 'Type: <b>' + param_type + '</b>, ' \
                          + 'Default: <b>' + default + '</b></font><br/>' \
                          + self.dedent(description) + '</pre>'
                action.setToolTip(tooltip)

    def dedent(self, description):
        """ Removes first empty line from description and any leading tabs
            from the next line before the description and any following lines.
            First lines are wrapped to 70 characters.

        :param description(string): from the XML generated tooltips dictionary
        :return: formatted output for the tooltip
        """
        trim_start = 0  # Remove any leading newline that affects dedent
        while trim_start < len(description) and description[trim_start] == '\n':
            trim_start += 1
        description = textwrap.dedent(description[trim_start : ])
        lines = description.splitlines()
        output = ''
        for line in lines:
            output += textwrap.fill(line, 70) + '\n'
        return output[0:-1] # remove last newline


    def handleMenuHovered(self, action):
       QToolTip.showText(QCursor.pos(), action.toolTip(),
                         self, self.parent().actionGeometry(action))

if __name__ == "__main__":

    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar
    from PyQt5.QtCore import QRect
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    menubar = QMenuBar(main_window)
    menubar.setGeometry(QRect(0, 0, 800, 19))
    menu = AddMenu(menubar)
    main_window.show()
    sys.exit(app.exec_())
