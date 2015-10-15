#!/usr/bin/env python3

import os
import socket
import sys
from PyQt5.QtCore import (pyqtSlot, QDir, QModelIndex, Qt, QSettings,
                          QByteArray, pyqtSignal, QThread)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QFileSystemModel, QDialog, QFileDialog)
from PyQt5.uic import loadUi
from os import environ

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

class RunSettings(QDialog):
    file = None
    file2 = None
    file3 = None
    def __init__(self):
        super(RunSettings, self).__init__()
        loadUi('runs.ui', self)
        self.setWindowTitle("Monitored runs folder")

        self.toolButtonView.clicked.connect(self.showdir)
        self.toolButtonView2.clicked.connect(self.showdir2)
        self.toolButtonView3.clicked.connect(self.showdir3)

        self.pushButton_OK.clicked.connect(self.rundir_save)

        # get GUI settings
        settings = QSettings("ITER", "solps-gui")

        settings.beginGroup("RunDirectories")

        rundir1 = settings.value("runDir1")
        if rundir1 : self.lineEdit_rundir.setText(rundir1)
        rundir2 = settings.value("runDir2")
        if rundir2 :  self.lineEdit_rundir2.setText(rundir2)
        rundir3 = settings.value("runDir3")
        if rundir3 :  self.lineEdit_rundir3.setText(rundir3)

        settings.endGroup()

    def rundir_save(self):

        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("RunDirectories")
        if self.file : settings.setValue("runDir1",self.file)
        if self.file2 : settings.setValue("runDir2",self.file2)
        if self.file3 : settings.setValue("runDir3",self.file3)
        settings.endGroup()

    def showdir(self):
        self.file = QFileDialog.getExistingDirectory\
            (self, "Select Directory",'/work/projects/solps-iter',
             QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks)
        self.lineEdit_rundir.setText(self.file)

    def showdir2(self):
        self.file2 = QFileDialog.getExistingDirectory\
            (self, "Select Directory",'/work/projects/solps-iter',
             QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks)
        self.lineEdit_rundir2.setText(self.file2)

    def showdir3(self):
        self.file3 = QFileDialog.getExistingDirectory\
            (self, "Select Directory",'/work/projects/solps-iter',
             QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks)
        self.lineEdit_rundir3.setText(self.file3)


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
        
        self.model = RUNSystemModel()
        self.model.setRootPath('') # Disable folder watch for now
        self.treeViewRuns.setModel(self.model)
        self.treeViewRuns.setRootIndex(self.model.index(os.environ.get("HOME")))
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
