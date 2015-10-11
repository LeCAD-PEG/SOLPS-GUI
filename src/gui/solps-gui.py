#!/usr/bin/env python3
import sys

from PyQt5.QtCore import pyqtSlot, QDir, QModelIndex, Qt, QSettings, QByteArray
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeView, QFileSystemModel
from PyQt5.uic import loadUi
import jobStatusServer
from src.gui.jobStatusServer.server import SIGjobStatusServer

class RUNSystemModel(QFileSystemModel):

    def __init__(self):
        super(RUNSystemModel, self).__init__()
        # run job status server
        self.jobStatusServer = SIGjobStatusServer('127.0.0.1', 45100)
        
        #self.jobStatusServer.
        
    def columnCount(self, parent = QModelIndex()):
        return super(RUNSystemModel, self).columnCount()+1

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
        return super(RUNSystemModel, self).data(index, role)

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
        return super(RUNSystemModel, self).headerData(section, orientation, role)


    """
        Register method as slot (receiver) of signal when job status signal is emitted.
        Method calls method to retrieve job status and other data from server.
    """
    @pyqtSlot(str, name='jobStatusChanged')
    def jobStatusChanged(self, inJobID):
        # get new data about job ID from server: new status, last change date, etc.
        newData = self.jobStatusServer.getClientStatus(inJobID)
        
        printf("Status of job " + inJobID + " changed: " )
        printf(newData)


class SolpsImpl(QMainWindow):
    model = None
    def __init__(self, *args):
        super(SolpsImpl, self).__init__(*args)
        loadUi('solps-gui.ui', self)
        self.actionAbout_Qt.triggered.connect(QApplication.instance().aboutQt)
        self.checkBoxParameterScan.toggled.connect(self.plainTextEditScript.setEnabled)
        
        self.model = RUNSystemModel()
        self.model.setRootPath('')
        self.treeViewRuns.setModel(self.model)
        self.model.setFilter(QDir.Dirs|QDir.NoDotAndDotDot)
        self.model.setNameFilterDisables(0)

        # get GUI settings
        settings = QSettings("ITER", "solps-gui")
        
        settings.beginGroup("MainWindow")
        geometry = settings.value("Geometry")
        if geometry :  self.restoreGeometry(geometry)
        state = settings.value("State")
        if state : self.restoreState(state)
        settings.endGroup()

        column_array = QByteArray()

        settings.beginGroup("TreeViewRuns")
        treeview = settings.value("ColumnWidth")
        if treeview : self.treeViewRuns.header().restoreState(treeview)
        settings.endGroup()

        
    def closeEvent(self, event):
        settings = QSettings("ITER", "solps-gui")
        
        settings.beginGroup("MainWindow")
        settings.setValue("Geometry", self.saveGeometry())
        settings.setValue("State", self.saveState())
        settings.endGroup()

        settings.beginGroup("TreeViewRuns")
        settings.setValue("ColumnWidth", self.treeViewRuns.header().saveState())
        settings.endGroup()
        
        QMainWindow.closeEvent(self, event)

    
    @pyqtSlot()
    def on_initializeRuns_clicked(self):
        if self.plainTextEditScript.isEnabled():
            script = self.plainTextEditScript.toPlainText()
            exec(script)
        else:
            print("Creating %s" % self.lineEditSequenceName.text())

    @pyqtSlot()
    def on_pushButtonRunFilter_clicked(self):
        self.model.setNameFilters([self.lineEditRunFilter.text()])

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        QMessageBox.about(self, "About SOLPS-ITER GUI",
         "GUI will enable users to monitor multiple simultaneously running "
         "cases, which requires defining the working directory (folder) for "
         "each case to be separated from each other. "
         "Input file builder will depend on it to correctly save input files "
         " for multiple parameter scan cases.")


"""
    Main method.
"""
app = QApplication(sys.argv)
app.setStyle("motif")
widget = SolpsImpl()

widget.show()
sys.exit(app.exec_())
