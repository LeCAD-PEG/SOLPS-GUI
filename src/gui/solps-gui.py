#!/usr/bin/env python3

import os
import socket
import sys
from PyQt5.QtCore import (pyqtSlot, QModelIndex, Qt, QSettings,
                          pyqtSignal, QThread, QAbstractItemModel, QVariant)

from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QDialog,
                             QFileDialog)
from PyQt5.uic import loadUi
from os.path import expanduser

class RunSettings(QDialog):

    runDirsChanged = pyqtSignal()

    def __init__(self, runs_model):
        super(RunSettings, self).__init__()
        loadUi('runs.ui', self)
        self.setWindowTitle("Monitored runs folder")
        self.runDirsChanged.connect(runs_model.refresh_dirs)

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
        self.lineEdit_alias1.setText(settings.value("Alias1", "local_1"))
        self.lineEdit_alias2.setText(settings.value("Alias2", "local_2"))
        self.lineEdit_alias3.setText(settings.value("Alias3", "local_3"))
        self.lineEdit_alias4.setText(settings.value("Alias4", "local_4"))
        self.lineEdit_alias5.setText(settings.value("Alias5", "local_5"))
        self.lineEdit_monitor_interface.setText(
            settings.value("Monitor_interface", "interface #"))
        self.lineEdit_monitor_port.setText(
            settings.value("Monitor_port", "port #"))
        settings.endGroup()
        
        self.toolButtonView1.clicked.connect(self.showdir1)
        self.toolButtonView2.clicked.connect(self.showdir2)
        self.toolButtonView3.clicked.connect(self.showdir3)
        self.toolButtonView4.clicked.connect(self.showdir4)
        self.toolButtonView5.clicked.connect(self.showdir5)


    def update_dir(self, line_edit):
        current_dir = line_edit.text()
        if current_dir == "": current_dir = expanduser("~")
        new_dir = QFileDialog.getExistingDirectory(self,
          "Select Directory", current_dir, QFileDialog.ShowDirsOnly)
        if new_dir: line_edit.setText(new_dir)

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
        settings.setValue("Alias1", self.lineEdit_alias1.text())
        settings.setValue("Alias2", self.lineEdit_alias2.text())
        settings.setValue("Alias3", self.lineEdit_alias3.text())
        settings.setValue("Alias4", self.lineEdit_alias4.text())
        settings.setValue("Alias5", self.lineEdit_alias5.text())
        settings.setValue("Monitor_interface",
                          self.lineEdit_monitor_interface.text())
        settings.setValue("Monitor_port", self.lineEdit_monitor_port.text())
        settings.endGroup()
        self.runDirsChanged.emit()

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

class RunStatusServer(QThread):
    sock = None
    retrieve = True
    jobStatusChanged = pyqtSignal(str)

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
            self.jobStatusChanged.emit(data.decode('utf-8'))


class RunFileSystemScan(QThread):

    completed = pyqtSignal()
    scanStatus = pyqtSignal(str)

    def __init__(self, runs_model, parent=None):
        super(RunFileSystemScan, self).__init__(parent)
        self.model = runs_model

    def run(self):
        self.scanStatus.emit(u"Filesystem scanning started...")
        print("FileSystemScan started")
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("RunDirectories")
        rundir1 = settings.value("runDir1", "")
        alias1 = settings.value("Alias1", "local_1") #TODO threaded
        settings.endGroup()

        self.model.rootItem = TreeItem(self.model.headerdata)
        self.model.setupModelData(rundir1, self.model.rootItem)
        self.completed.emit()
        self.scanStatus.emit(u'Ready')

class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.basename = os.path.basename(data[0])
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
            if column == 0:
                return self.basename
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

    monitorThread = None
    scanFileSystemThread = None

    def __init__(self, parent=None):
        super(RunsModel, self).__init__(parent)
        self.runJobStatusServer()
        self.headerdata = ["Run Directory", "Status", "Comment", "Last update",
                        "User", "Device", "Shot number", "Run number"]
        self.columns = 8
        self.rootItem = TreeItem(self.headerdata)

        self.scanFileSystemThread = RunFileSystemScan(self)
        self.scanFileSystemThread.completed.connect(self.tree_available)
        self.scanFileSystemThread.start()

    @pyqtSlot()
    def tree_available(self):
        self.modelReset.emit()

    @pyqtSlot()
    def refresh_dirs(self):
        self.scanFileSystemThread.start()

    def dirTraverse(self, alias, rundir):
        data_string = alias + 6 * " *" + "\n"
        rootDir = rundir
        path_b = rootDir.split("/")
        for dir, subdirs, files in os.walk(rootDir):
            path = dir.split('/')
            r = len(path)-len(path_b)
            data_string += " %s%s\n" % ( r*" ", os.path.basename(dir))
        return data_string

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()
    #    return self.columns
    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role = None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[section])
        if role == Qt.TextAlignmentRole:
           # return Qt.AlignHCenter
            return self.rootItem.data(section)
        return super(RunsModel, self).headerData(section, orientation, role)

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem is None: #or parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModelData(self, rootdir, parent):
        parents = [parent]
        rootdir_len = len(rootdir)
        for dir, subdirs, files in os.walk(rootdir):
            dir_len = len(dir)
            if dir_len > rootdir_len:
                parents.append(parents[-1].child(parents[-1].childCount() - 1))
                rootdir = dir
                rootdir_len = len(rootdir)
            elif dir_len < rootdir_len:
                parents.pop()
                rootdir = dir
                rootdir_len = len(rootdir)
            parents[-1].appendChild(TreeItem([dir, dir], parents[-1]))

    """ Run job server """
    def runJobStatusServer(self):
        self.monitorThread = RunStatusServer()
        self.monitorThread.bind('0.0.0.0', 49406)
        #self.monitorThread.finished.connect(self.deleteLater) # TODO
        self.monitorThread.jobStatusChanged.connect(self.jobStatusChanged)
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
    def __init__(self, *args):
        super(SolpsImpl, self).__init__(*args)
        loadUi('solps-gui.ui', self)
        self.actionAbout_Qt.triggered.connect(QApplication.instance().aboutQt)
        self.checkBoxParameterScan.toggled.connect(self.plainTextEditScript.setEnabled)

        self.model = RunsModel()
        self.treeViewRuns.setModel(self.model)

        # get GUI settings
        settings = QSettings("ITER", "solps-gui")
        
        settings.beginGroup("MainWindow")
        geometry = settings.value("Geometry")
        if geometry :  self.restoreGeometry(geometry)
        state = settings.value("State")
        if state : self.restoreState(state)
        settings.endGroup()

        settings.beginGroup("TreeViewRuns")
        treeview = settings.value("ColumnWidth")
        if treeview : self.treeViewRuns.header().restoreState(treeview)
        settings.endGroup()

        self.actionJob_list.triggered.connect(self.showdialog)
        self.model.scanFileSystemThread.scanStatus.connect(self.statusbar.showMessage)
        self.statusbar.showMessage("Preparing Runs tree ...")

    def showdialog(self):
        dialog = RunSettings(self.model)
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

    def expanded(self):
        for column in range(self.model().columnCount(QModelIndex())):
            self.resizeColumnToContents(column)

    def change(self, topLeftIndex, bottomRightIndex):
        self.update(topLeftIndex)
        self.expandAll()
        self.expanded()
        
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
    Main method
"""
app = QApplication(sys.argv)
# app.setStyle("motif")
widget = SolpsImpl()
widget.show()
sys.exit(app.exec_())
