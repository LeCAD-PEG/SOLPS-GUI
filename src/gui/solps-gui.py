#!/usr/bin/env python3
import sys

#from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QDir, QModelIndex, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeView, QFileSystemModel
from PyQt5.uic import loadUi

class ITERSystemModel(QFileSystemModel):

    def columnCount(self, parent = QModelIndex()):
        return super(ITERSystemModel, self).columnCount()+1

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == Qt.DisplayRole:
                return "YourText" + str(index.row())
            if role == Qt.TextAlignmentRole:
                return Qt.AlignLeft
        if index.column() == 1:
            if role == Qt.DisplayRole:
                return "running"
            if role == Qt.TextAlignmentRole:
                return Qt.AlignHCenter
        return super(ITERSystemModel, self).data(index, role)

    def headerData(self, section, orientation, role):
        if section == 1:
            if role == Qt.DisplayRole:
                return "Status"
            if role == Qt.TextAlignmentRole:
                return Qt.AlignHCenter
        if section == self.columnCount() - 1:
            if role == Qt.DisplayRole:
                 return "Comment"     
            if role == Qt.TextAlignmentRole:
                return Qt.AlignLeft
        return super(ITERSystemModel, self).headerData(section, orientation, role)


class SolpsImpl(QMainWindow):
    model = None
    def __init__(self, *args):
        super(SolpsImpl, self).__init__(*args)
        loadUi('solps-gui.ui', self)
        self.actionAbout_Qt.triggered.connect(QApplication.instance().aboutQt)
        self.checkBoxParameterScan.toggled.connect(
            self.plainTextEditScript.setEnabled)
        self.model = ITERSystemModel()
        self.model.setRootPath('')
        self.treeViewRuns.setModel(self.model)
        self.model.setFilter(QDir.Dirs|QDir.NoDotAndDotDot)
        self.model.setNameFilters(["b*"])
        self.model.setNameFilterDisables(0)
    
    @pyqtSlot()
    def on_initializeRuns_clicked(self):
        if self.plainTextEditScript.isEnabled():
            script = self.plainTextEditScript.toPlainText()
            exec(script)
        else:
            print("Creating %s" % self.lineEditSequenceName.text())

    @pyqtSlot()
    def on_pushButtonRunFilter_clicked(self):
        print(self.lineEditRunFilter.text())
        self.model.setNameFilters([self.lineEditRunFilter.text()])

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        QMessageBox.about(self, "About SOLPS-ITER GUI",
         "GUI will enable users to monitor multiple simultaneously running "
         "cases, which requires defining the working directory (folder) for "
         "each case to be separated from each other. "
         "Input file builder will depend on it to correctly save input files "
         " for multiple parameter scan cases.")

app = QApplication(sys.argv)
app.setStyle("motif")
widget = SolpsImpl()
widget.show()
sys.exit(app.exec_())
