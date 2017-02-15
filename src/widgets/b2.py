
from PyQt5.QtCore import QRegExp, QEvent, Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QToolTip
from PyQt5.QtGui import (QSyntaxHighlighter, QTextCursor, QTextCharFormat,
                         QFont, QBrush)
import logging
import b2_tooltips

b2_tooltips = {'b2mn': b2_tooltips.b2mn_tooltips,
               'b2ag': b2_tooltips.b2ag_tooltips,
               'b2ah': b2_tooltips.b2ah_tooltips,
               'b2ar': b2_tooltips.b2ar_tooltips,
               'b2ai': b2_tooltips.b2ai_tooltips,
               }


class HighlightingRule():
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format = format


class B2PlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None, rules=list()):
        super(B2PlainTextEdit, self).__init__(parent)
        self.tooltips = dict()
        self.old_text = None
        self.modified = False
        for key in rules:
            category, param_type, description, default_value = rules[key]
            tooltip = '<font color=blue><b>' + key \
                      + '</b> Category: <b>' + category + '</b>, ' \
                      + 'Type: <b>' + param_type + '</b>, '\
                      + 'Default: <b>' + default_value + '</b></font><br>' \
                      + description
            self.tooltips[key] = tooltip
    def event(self, event):
        if event.type() == QEvent.ToolTip:
            textCursor = self.cursorForPosition(event.pos())
            textCursor.select(QTextCursor.WordUnderCursor)
            word = textCursor.selectedText()
            if word in self.tooltips:
                QToolTip.showText(event.globalPos(), self.tooltips[word])
            else:
                QToolTip.hideText()
        return super(B2PlainTextEdit, self).event(event)

    def setPlainText(self, text):
        if self.old_text is None:
            self.old_text = text
        elif self.old_text != text:
            self.modified = True
        return super(B2PlainTextEdit, self).setPlainText(text)

    def insert_line(self, line):
        self.insertPlainText(line)


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

        for word in keywords:
            pattern = QRegExp(word)
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
        return self.display_widget.modified

class B2Edit(QWidget):
    def __init__(self, parent=None, filename=''):
        super(B2Edit, self).__init__(parent)

        if filename[:4] not in b2_tooltips:
            tooltips = {}
        else:
            tooltips = b2_tooltips[filename[:4]]
        self.display_widget = B2PlainTextEdit(self, tooltips)
        self.text_handler = B2Handler(self, self.display_widget)
        self.text_handler.highlighter.prepare_rules(tooltips)
        layout = QVBoxLayout()
        layout.addWidget(self.display_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def setPlainText(self, text):
        self.text_handler.setPlainText(text)

    def toPlainText(self):
        return self.display_widget.toPlainText()

    def setReadOnly(self, state):
        return

    def setPlaceholderText(self, text):
        self.text_handler.setPlainText(text)

    def document(self):
        return self.text_handler

if __name__ == '__main__':
    import sys
    import os
    from PyQt5.QtWidgets import (QApplication, QMainWindow)

    app = QApplication(sys.argv)

    class Standalone(QMainWindow):
        def __init__(self, parent=None):
            super(Standalone, self).__init__(parent)
            self.editor = B2Edit(self)
            self.plaintextedit = B2PlainTextEdit(self)
            self.setCentralWidget(self.b2)

    mainwindow = Standalone()
    mainwindow.b2.document().readInput('/home/simicg/Documents\
                                        /eirene-gui/b2ag.dat')
    mainwindow.b2.setPlainText
    mainwindow.show()
    sys.exit(app.exec_())
