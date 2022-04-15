
from PySide6.QtCore import (QEvent, Qt, Slot, QSize, QRegularExpression,
                          Signal)
from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QToolTip
from PySide6.QtGui import (QSyntaxHighlighter, QTextCursor, QTextCharFormat,
                         QFont, QBrush)
import logging
import b2_tooltips
import textwrap
import re



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

        self.keywordGreen = QTextCharFormat()
        self.keywordGreen.setForeground(Qt.green)
        self.keywordGreen.setFontWeight(QFont.Bold)

        self.keywordRed = QTextCharFormat()
        self.keywordRed.setForeground(Qt.red)
        self.keywordRed.setFontWeight(QFont.Bold)

        self.highlightingSwitches = []

        self.commentPattern = QRegularExpression("^\*[^\n]*")
        self.keywordComment = QTextCharFormat()
        brush = QBrush(Qt.darkGreen, Qt.SolidPattern)
        self.keywordComment.setForeground(brush)
        self.keywordComment.setFontWeight(QFont.Bold)

    def prepare_rules(self, tooltip):
        keywords = []
        self.counter = {}
        for key in tooltip:
            keywords.append(key)
        # Setting prefixes, so words inside quotes, other words do not get
        # highlighted, thus getting partially highlighted words
        prefix = '^(\'| ||\*)'
        for word in keywords:
            pattern = QRegularExpression(prefix + word)
            pattern.setPatternOptions(pattern.patternOptions() |
                                      QRegularExpression.CaseInsensitiveOption)
            self.highlightingSwitches.append((pattern, word))

    def highlightBlock(self, text):
        whole_text = self.document().toPlainText()
        position = self.currentBlock().position()
        #print(position, text)
        match = self.commentPattern.match(text)
        if match.hasMatch():
            index = match.capturedStart()
            length = match.capturedLength()
            self.setFormat(index, length, self.keywordComment)

        for p, word in self.highlightingSwitches:
            match = p.match(text)
            if match.hasMatch():
                index = match.capturedStart()
                length = match.capturedLength()
                p.setPattern(word + '(\'|\s)')
                if p.match(whole_text[position + length:]).hasMatch():
                    match = p.match(whole_text[position + length:])
                    #print(match.capturedStart(), match.capturedLength())
                    #print(index, length)
                    highlight_format = self.keywordRed
                elif p.match(whole_text[:position]).hasMatch():
                    highlight_format = self.keywordGreen
                else:
                    highlight_format = self.keyword
                self.setFormat(index, length, highlight_format)

        # self.setCurrentBlockState(0)


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
        self.plainTextWidget = B2PlainTextEdit(self, tooltips)
        self.highlighter = B2Highlighter(self.plainTextWidget.document())
        self.highlighter.prepare_rules(tooltips)

        layout = QVBoxLayout()
        layout.addWidget(self.plainTextWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F2:
            if self.path.endswith('.stencil') or 'baserun' in self.path:
                # No checks are required since the solpsinput.py have
                # checked if stencils exist
                with open(self.path, 'r') as f:
                    self.plainTextWidget.setPlainText(f.read())
                    self.plainTextWidget.document().setModified(True)
                    self.path = ''
        elif event.key() == Qt.Key_F5:
            # Refresh the highlighter
            self.highlighter.rehighlight()

    def setPlainText(self, text):
        self.plainTextWidget.setPlainText(text)

    def toPlainText(self):
        return self.plainTextWidget.toPlainText()

    def setReadOnly(self, state):
        return

    def setPlaceholderText(self, text):
        self.plainTextWidget.setPlaceholderText(text)

    def document(self):
        return self.plainTextWidget.document()

if __name__ == '__main__':
    import sys
    import os
    from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu,)
    import functools

    app = QApplication(sys.argv)

    # Add menu functionality
    add_menu_functionality = 1
    try:
        import b2menu
    except ImportError:
        add_menu_functionality = 0
        print('No add menu functionality!')

    class AddMenu(QMenu):
        """ AddMenu(QMenu)

            Provides a custom widget for inserting B2mn parameters into editor.
        """

        output = Signal(str)

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

        @Slot(str)
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
        editorChanged = Signal(str)

        def __init__(self, parent=None):
            super(Standalone, self).__init__(parent)

        def read_and_set_text(self, path):
            self.path = path
            if os.path.isfile(path):
                filename = path.split('/')[-1] # For unix
                with open(path, 'r') as f:
                    text = f.read()
                self.editor = B2Edit(self, filename)
                self.setCentralWidget(self.editor)
                self.editor.setPlainText(text)
                if add_menu_functionality:
                    menu_bar = QMenuBar(self)
                    addMenu = AddMenu(menu_bar)
                    addMenu.output.connect(\
                                    self.editor.plainTextWidget.insert_line)
                    self.editorChanged.connect(addMenu.editorChanged)
                    self.editorChanged.emit(filename)
                    self.setMenuBar(menu_bar)
            else:
                logging.warning("Path " + path + " does not exist")

        def closeEvent(self, e):
            self.documentSave()
            return super(Standalone, self).closeEvent(e)

        def documentSave(self):
            if self.editor.document().isModified():
                if os.path.exists(self.path):
                    try:
                        with open(self.path, 'w') as f:
                            f.write(self.editor.plainTextWidget.toPlainText())
                        logging.info('File', self.path, 'saved.')
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
