#!/usr/bin/env python3

import os
import socket
import sys
from PyQt5.QtCore import (pyqtSlot, QDir, QModelIndex, Qt, QSettings,
                          QByteArray, pyqtSignal, QThread, QAbstractItemModel)

from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QFileSystemModel, QDialog, QFileDialog)
from PyQt5.uic import loadUi
from os import environ
from os.path import expanduser

class RunStatusServer(QThread):
    sock = None
    retrieve = True
    jobStatusChange = pyqtSignal(str)

    def bind(self, address, port):
        # connect to UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind socket to local host and port
        try:
            self.sock.bind((address, port))
        except socket.error: #, msg:
            print('Bind to', address, ':', str(port), ' failed.')
            sys.exit()
        print('Server on', address, ':', port)
    def run(self):
        print("RunStatusServer started")
        while self.retrieve:
            data, addr = self.sock.recvfrom(1024) # wait for data
            print("Received packet from", addr[0], "data=", data.decode('utf-8'))
            self.jobStatusChange.emit(data.decode('utf-8'))

# Settings->Job list

class RunSettings(QDialog):

    def __init__(self):
        super(RunSettings, self).__init__()
        loadUi('runs.ui', self)
        self.setWindowTitle("Monitored runs folder")

        # get GUI settings
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("RunDirectories")
        rundir1 = settings.value("runDir1", expanduser("~"))
        self.lineEdit_rundir1.setText(rundir1)
        rundir2 = settings.value("runDir2", "")
        self.lineEdit_rundir2.setText(rundir2)
        rundir3 = settings.value("runDir3", "")
        self.lineEdit_rundir3.setText(rundir3)
        rundir4 = settings.value("runDir4", "")
        self.lineEdit_rundir4.setText(rundir4)
        rundir5 = settings.value("runDir5", "")
        self.lineEdit_rundir5.setText(rundir5)
        settings.endGroup()
        
        self.toolButtonView1.clicked.connect(self.showdir1)
        self.toolButtonView2.clicked.connect(self.showdir2)
        self.toolButtonView3.clicked.connect(self.showdir3)
        self.toolButtonView4.clicked.connect(self.showdir4)
        self.toolButtonView5.clicked.connect(self.showdir5)

    # save GUI settings
    @pyqtSlot()
    def on_pushButton_OK_clicked(self):
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("RunDirectories")
        settings.setValue("runDir1", self.lineEdit_rundir1.text())
        settings.setValue("runDir2", self.lineEdit_rundir2.text())
        settings.setValue("runDir3", self.lineEdit_rundir3.text())
        settings.setValue("runDir4", self.lineEdit_rundir4.text())
        settings.setValue("runDir5", self.lineEdit_rundir5.text())
        
        settings.endGroup()

    def update_dir(self, line_edit):
        current_dir = line_edit.text()
        if current_dir == "": current_dir = expanduser("~")
        new_dir = QFileDialog.getExistingDirectory(self,
          "Select Directory", current_dir, QFileDialog.ShowDirsOnly)
        if new_dir: line_edit.setText(new_dir)
 
    # Choose run directory
    @pyqtSlot()
    def showdir1(self): self.update_dir(self.lineEdit_rundir1)

    @pyqtSlot()
    def showdir2(self): self.update_dir(self.lineEdit_rundir2)
                
    @pyqtSlot()
    def showdir3(self): self.update_dir(self.lineEdit_rundir3)

    @pyqtSlot()
    def showdir4(self): self.update_dir(self.lineEdit_rundir4)

    @pyqtSlot()
    def showdir5(self): self.update_dir(self.lineEdit_rundir5)

class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

class RunsModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super(RunsModel, self).__init__(parent)

        self.rootItem = TreeItem(("Title", "Summary"))
        #self.setupModelData(data.split('\n'), self.rootItem)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())
                
class RUNSystemModel(QFileSystemModel):
    jobStatusServer = None
    monitorThread = None
    
    def __init__(self):
        super(RUNSystemModel, self).__init__()
        self.runJobStatusServer()

    def columnCount(self, parent = QModelIndex()):
        return super(RUNSystemModel, self).columnCount()+1

    def data(self, index, role=None):
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

    def headerData(self, section, orientation, role=None):
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
        return super(RUNSystemModel, self).headerData(section,
                                                      orientation, role)

    """ Run job server """
    def runJobStatusServer(self):
        self.monitorThread = RunStatusServer()
        self.monitorThread.bind('0.0.0.0', 49406)
        #self.monitorThread.finished.connect(self.deleteLater) # TODO
        self.monitorThread.jobStatusChange.connect(self.jobStatusChanged)
        self.monitorThread.start()

    """
        Register method as slot (receiver) of signal when job status signal
        is emitted.
        Method calls method to retrieve job status and other data from server.
    """
    @pyqtSlot(str)
    def jobStatusChanged(self, message):
        # get new data about job ID from server: new status, last change date,
        # etc.
        #newData = self.jobStatusServer.getClientStatus(inJobID)
        
        print("Status of job changed: ", message)
        #print(newData)


class SolpsImpl(QMainWindow):
    model = None
    
    def __init__(self, *args):
        super(SolpsImpl, self).__init__(*args)
        loadUi('solps-gui.ui', self)
        self.actionAbout_Qt.triggered.connect(QApplication.instance().aboutQt)
        self.checkBoxParameterScan.toggled.connect(
            self.plainTextEditScript.setEnabled)
        
        self.model = RunsModel()
       # self.model.setRootPath('') # Disable folder watch for now
        self.treeViewRuns.setModel(self.model)
        #self.treeViewRuns.setRootIndex(self.model.index(os.environ.get("HOME")))
        #self.model.setFilter(QDir.Dirs|QDir.NoDotAndDotDot)
        #self.model.setNameFilterDisables(0)

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

        self.actionJob_list.triggered.connect(self.showdialog)

    def showdialog(self):
        dialog = RunSettings()
        dialog.show()
        dialog.exec_()

        
    def closeEvent(self, event):
        # save settings
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
