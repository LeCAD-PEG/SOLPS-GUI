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
import functools

import b2menu

class AddMenu(QMenu):
    """ Script(QPlainTextEdit)
    
        Provides a custom widget to display a gnuplot with properties and slots
        that can be used to customize its appearance.
    """

    output = pyqtSignal(str)
    
    def __init__(self, parent=None):
        '''
        Toooltips work on QMenu as a whole but not on actions!
        For this reason we connect action's hover and set the tooltip
        to the menu.
        '''
        super(AddMenu, self).__init__(parent)
        self.setTitle("Add")
        parent.addAction(self.menuAction())
        self.hovered.connect(self.handleMenuHovered)
        #self.setEnabled(False)

        for category in sorted(b2menu.b2mn_menu):
            category_menu = QMenu(self)
            category_menu.setTitle(category)
            self.addAction(category_menu.menuAction())

            for parameter in b2menu.b2mn_menu[category]:
                ( name, param_type, data, description ) = parameter
                if param_type == 'paramgroup':
                    paramgroup = QMenu(category_menu)
                    paramgroup.setTitle(name)
                    action = category_menu.addAction(paramgroup.menuAction())
                    for parameter in data:
                        (name, param_type, default, short_desc) = parameter
                        action = paramgroup.addAction(name)
                        sd_formatted= self.dedent(short_desc)
                        if len(sd_formatted):
                            sd_formatted = '<br/><b>' + sd_formatted +'</b>'
                        tooltip = '<pre><font color=blue><b>' + name + '</b> ' \
                                  + 'Type: <b>' + param_type + '</b>, ' \
                                  + 'Default: <b>' + default + '</b></font>' \
                                  + '<br/>' + self.dedent(description)  \
                                  + sd_formatted + '</pre>'
                        action.setToolTip(tooltip)
                        line = "'" + name + "'       '" + default + "'"
                        pfn = functools.partial(self.handleMenuTriggered, line)
                        action.triggered.connect(pfn)

                else:
                    action = category_menu.addAction(name)
                    tooltip = '<pre><font color=blue><b>' + name + '</b> ' \
                              + 'Type: <b>' + param_type + '</b>, ' \
                              + 'Default: <b>' + data + '</b></font><br/>' \
                              + self.dedent(description) + '</pre>'
                    action.setToolTip(tooltip)
                    line = "'" + name + "'       '" + data + "'"
                    pfn = functools.partial(self.handleMenuTriggered, line)
                    action.triggered.connect(pfn)

    def handleMenuHovered(self, action):
        """ Instead of showing tooltip on hover we rather setup a new tooltip
            to the parent and wait to be shown.
        """
        action.parent().setToolTip(action.toolTip())

    def handleMenuTriggered(self, line):
        #action.parent().setToolTip(action.toolTip())
        print("Emmiting: " + line)
        self.output.emit(line)


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
            output += textwrap.fill(line, 80) + '\n'
        return output[0:-1] # remove last newline




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
