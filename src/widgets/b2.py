
from PyQt5.QtCore import QRegExp, QEvent, Qt, pyqtSlot, QSize
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QToolTip
from PyQt5.QtGui import (QSyntaxHighlighter, QTextCursor, QTextCharFormat,
                         QFont, QBrush)
import logging
import b2_tooltips
import textwrap



def dedent(description):
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

    wrap = 70 if len(description) < 800 else 150
    for line in lines:
        if line.startswith('\t'):
            output += '\n     '.join(textwrap.wrap(line[1:], wrap)) + '\n'
        else:
            output += textwrap.fill(line, wrap) + '\n'
    return output[0:-1] # remove last newline

class HighlightingRule():
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format = format


class B2PlainTextEdit(QPlainTextEdit):
    """This is the QPlainTextEdit that contains the text, activates highlights 
    and tooltips for all the switches and parameters that have description,
    category, default values and other notes.
    """

    def __init__(self, parent=None, rules=list()):
        super(B2PlainTextEdit, self).__init__(parent)
        font = QFont()
        font.setFamily('Monospace')
        font.setPixelSize(12)
        self.setFont(font)
        self.tooltips = dict()
        self.old_text = ''

        for key in rules:
            category, param_type, description, default_value = rules[key]
            tooltip = '<font color=blue><b>' + key \
                      + '</b> Category: <b>' + category + '</b>,' \
                      + 'Type: <b>' + param_type + '</b>,'\
                      + 'Default: <b>' + default_value + '</b></font>' \
                      + '<pre>' + dedent(description) + '</pre>'

            self.tooltips[key.lower()] = tooltip

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            textCursor = self.cursorForPosition(event.pos())
            textCursor.select(QTextCursor.WordUnderCursor)
            word = textCursor.selectedText().lower()
            if word in self.tooltips:
                QToolTip.showText(event.globalPos(), self.tooltips[word])
            else:
                QToolTip.hideText()
        return super(B2PlainTextEdit, self).event(event)

    def setPlainText(self, text):
        result = super(B2PlainTextEdit, self).setPlainText(text)
        self.old_text = self.toPlainText()
        return result

    def insert_line(self, line):
        self.moveCursor(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
        self.insertPlainText(line+'\n')

    def sizeHint(self):
        return QSize(600, 400)

class B2Highlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super(B2Highlighter, self).__init__(parent)
        self.highlightingRules = []
        self.keyword = QTextCharFormat()
        self.keyword.setForeground(Qt.darkBlue)
        self.keyword.setFontWeight(QFont.Bold)

        comment = QTextCharFormat()
        brush = QBrush(Qt.darkGreen, Qt.SolidPattern)
        pattern = QRegExp("^\*[^\n]*")
        comment.setForeground(brush)
        rule = HighlightingRule(pattern, comment)
        self.highlightingRules.append(rule)

    def prepare_rules(self, tooltip):
        keywords = []
        for key in tooltip:
            keywords.append(key)
        # Setting prefixes, so words inside quotes, other words do not get
        # highlighted, thus getting partially highlighted words
        prefix = '^(\'| ||\*)'
        for word in keywords:
            pattern = QRegExp(prefix + word, Qt.CaseInsensitive)
            rule = HighlightingRule(pattern, self.keyword)
            self.highlightingRules.append(rule)

    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QRegExp(rule.pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = text.find(str(expression), index + length)
        self.setCurrentBlockState(0)


class B2Handler:
    def __init__(self, parent, display_widget):
        self.parent = parent
        self.display_widget = display_widget
        self.highlighter = B2Highlighter(self.display_widget.document())
        return

    def readInput(self, path):
        if os.path.exists(path):
            try:
                with open(path) as file:
                    self.filename = path
                    self.text = file.read()
                    self.setPlainText()
            except PermissionError as error:
                logging.error(str(error))
        else:
            msg = path + " does not exist"
            logging.error(msg)
        return

    def setPlainText(self, text=None):
        if text is None:
            self.display_widget.setPlainText(self.text)
        else:
            self.display_widget.setPlainText(text)

    def toPlainText(self):
        return self.display_widget.toPlainText()

    def isModified(self):
        old_text = self.display_widget.old_text
        last_text = self.display_widget.toPlainText()
        if last_text and old_text != last_text:
            return True
        return False

class B2Edit(QWidget):
    """This is the editor for all input files that are part of B2. If the input
    file has any tool-tips, that describes the switch or parameter, they will
    be applied. Otherwise it acts as a normal editor.

    If there is a .stencil provided in the run folder or in the ../baserun 
    folder, it can be loaded by using the F2 key.
    """

    def __init__(self, parent=None, filename=''):
        super(B2Edit, self).__init__(parent)
        self.path = ''

        if filename == 'b2mn.dat':
            tooltips = dict()
            [tooltips.update(b2_tooltips.tooltips[d]) for d in 
             b2_tooltips.tooltips]
        elif filename == 'b2ar.dat':
            tooltips = b2_tooltips.tooltips['b2mn.dat']
        elif filename in b2_tooltips.tooltips:
            tooltips = b2_tooltips.tooltips[filename]
        else:
            tooltips = {}

        # for switch_name in b2_tooltips.tooltips['b2mn.dat']:
        #     if switch_name not in tooltips and \
        #         switch_name[:4] == filename[:4]:
        #         tooltips[switch_name] = \
        #             b2_tooltips.tooltips['b2mn.dat'][switch_name]
        self.display_widget = B2PlainTextEdit(self, tooltips)
        self.text_handler = B2Handler(self, self.display_widget)
        self.text_handler.highlighter.prepare_rules(tooltips)
        layout = QVBoxLayout()
        layout.addWidget(self.display_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F2: 
            if self.path:
                # No checks are required since the solpsinput.py have
                # checked if stensils exist
                with open(self.path, 'r') as f:
                    self.display_widget.setPlainText(f.read())
                    self.path = ''

    def setPlainText(self, text):
        self.text_handler.setPlainText(text)

    def toPlainText(self):
        return self.display_widget.toPlainText()

    def setReadOnly(self, state):
        return

    def setPlaceholderText(self, text):
        self.display_widget.setPlaceholderText(text)

    def document(self):
        return self.text_handler

if __name__ == '__main__':
    import sys
    import os
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu,)
    from PyQt5.QtCore import pyqtSignal, QRect
    import functools

    app = QApplication(sys.argv)

    # Add menu functionality
    add_menu_functionality = 1
    try:
        import b2menu
    except ImportError:
        add_menu_functionality = 0
        prtin('No add menu functionality!')

    class AddMenu(QMenu):
        """ AddMenu(QMenu)
        
            Provides a custom widget for inserting B2mn parameters into editor.
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

                for parameter in b2menu.b2mn_menu[category][1:]:
                    ( name, param_type, data, description ) = parameter
                    if param_type == 'switchgroup':
                        switchgroup = QMenu(category_menu)
                        switchgroup.setTitle(name)
                        action = category_menu.addAction(\
                                                    switchgroup.menuAction())
                        for parameter in data:
                            (name, param_type, default, short_desc) = parameter
                            action = switchgroup.addAction(name)
                            sd_formatted= self.dedent(short_desc)
                            if len(sd_formatted):
                                sd_formatted = '<br/><b>'+sd_formatted+'</b>'
                            tooltip = '<pre><font color=blue><b>'+name+'</b>'\
                                      + 'Type: <b>' + param_type + '</b>, '\
                                      + 'Default: <b>'+default+'</b></font>'\
                                      + '<br/>' + self.dedent(description)\
                                      + sd_formatted + '</pre>'
                            action.setToolTip(tooltip)
                            line = "'" + name + "'       '" + default + "'"
                            pfn = functools.partial(self.handleMenuTriggered, 
                                                    line)
                            action.triggered.connect(pfn)

                    else:
                        action = category_menu.addAction(name)
                        tooltip = '<pre><font color=blue><b>' + name + '</b> '\
                                  + 'Type: <b>' + param_type + '</b>, ' \
                                  + 'Default: <b>' + data + '</b></font><br/>'\
                                  + self.dedent(description) + '</pre>'
                        action.setToolTip(tooltip)
                        line = "'" + name + "'       '" + data + "'"
                        pfn = functools.partial(self.handleMenuTriggered, line)
                        action.triggered.connect(pfn)

        def handleMenuHovered(self, action):
            """ Instead of showing tooltip on hover we rather setup a new 
                tool-tip to the parent and wait to be shown.
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

            wrap = 70 if len(description) < 800 else 150
            for line in lines:
                if line.startswith('\t'):
                    output += '\n     '.join(textwrap.wrap(line[1:], wrap)) + '\n'
                else:
                    output += textwrap.fill(line, wrap) + '\n'
            return output[0:-1] # remove last newline

        @pyqtSlot(str)
        def editorChanged(self, filename):
            if filename == 'b2mn.dat':
                for action in self.actions():
                    if action.text().startswith('b2'):
                        action.setEnabled(False)
                    else:
                        action.setEnabled(True)
            elif filename == 'input.dat':
                [action.setEnabled(False) for action in self.actions()]
            elif filename == 'b2ar.dat':
                # Find action with name 'Atomic Physics'
                for action in self.actions():
                    if action.text() == 'Atomic Physics':
                        action.setEnabled(True)
                        for a in action.menu().actions():
                            if a.text().startswith('b2ar'):
                                a.setEnabled(True)
                            else:
                                a.setEnabled(False)
                    else:
                        action.setEnabled(False)
            else:
                actions = self.actions()
                for action in actions:
                    if filename[:-4] in action.text():
                        action.setEnabled(True)
                    else:
                        action.setEnabled(False)


    class Standalone(QMainWindow):
        editorChanged = pyqtSignal(str)
        def __init__(self, parent=None):
            super(Standalone, self).__init__(parent)

        def read_and_set_text(self, path):
            self.path = path
            if os.path.isfile(path):
                filename = path.split('/')[-1] # For unix
                with open(path, 'r') as f:
                    text = f.read()
                self.editor = B2Edit(self, filename)
                self.setCentralWidget(self.editor.display_widget)
                self.editor.setPlainText(text)
                if add_menu_functionality:
                    menu_bar = QMenuBar(self)
                    addMenu = AddMenu(menu_bar)
                    addMenu.output.connect(\
                                        self.editor.display_widget.insert_line)
                    self.editorChanged.connect(addMenu.editorChanged)
                    self.editorChanged.emit(filename)
                    self.setMenuBar(menu_bar)
            else:
                print('File does not exist')

        def closeEvent(self, e):
            self.documentSave()
            return super(Standalone, self).closeEvent(e)

        def documentSave(self):
            if self.editor.text_handler.isModified():
                if os.path.exists(self.path):
                    try:
                        with open(self.path, 'w') as f:
                            f.write(self.editor.display_widget.toPlainText())
                    except PermissionError as e:
                        print('Permission error.')
                else:
                    print('The path to file does not exist!')



    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
        mainwindow = Standalone()
        title_name = input_filename.split('/')[-1]
        mainwindow.setWindowTitle(title_name)
        mainwindow.read_and_set_text(input_filename)
        mainwindow.show()
        sys.exit(app.exec_())
        
    else:
        print("Provide path to B2 input file.")
        sys.exit()