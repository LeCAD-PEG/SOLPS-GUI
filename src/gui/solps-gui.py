#!/usr/bin/env python3

import os
import socket
import sys
from PyQt5.QtCore import (pyqtSlot, QModelIndex, Qt, QSettings,
                          pyqtSignal, QThread, QAbstractItemModel, QVariant)

from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QFileSystemModel, QDialog, QFileDialog)
from PyQt5.uic import loadUi
from os import environ
from os.path import expanduser

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
        self.lineEdit_alias1.setText(settings.value("Alias1", "local_1"))
        self.lineEdit_alias2.setText(settings.value("Alias2", "local_2"))
        self.lineEdit_alias3.setText(settings.value("Alias3", "local_3"))
        self.lineEdit_alias4.setText(settings.value("Alias4", "local_4"))
        self.lineEdit_alias5.setText(settings.value("Alias5", "local_5"))
        self.lineEdit_monitor_interface.setText(settings.value("Monitor_interface", "interface #"))
        self.lineEdit_monitor_port.setText(settings.value("Monitor_port", "port #"))        
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
        settings.setValue("Alias1", self.lineEdit_alias1.text())
        settings.setValue("Alias2", self.lineEdit_alias2.text())
        settings.setValue("Alias3", self.lineEdit_alias3.text())
        settings.setValue("Alias4", self.lineEdit_alias4.text())
        settings.setValue("Alias5", self.lineEdit_alias5.text())
        settings.setValue("Monitor_interface", self.lineEdit_monitor_interface.text())
        settings.setValue("Monitor_port", self.lineEdit_monitor_port.text())
        settings.endGroup()

        file = open("Data.txt","r")
        data = file.readlines()
        travers_model = RunsModel(data)
        travers_model.dirTraverse(settings.value("Alias1"), settings.value("runDir1", expanduser("~")))

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
    monitorThread = None

    def __init__(self, data, parent=None):
        super(RunsModel, self).__init__(parent)
        self.runJobStatusServer()
        self.headerdata = ["Run Directory", "Status", "Comment", "Last update",
                        "User", "Device", "Shot number", "Run number"]
        self.columns = 8

        self.rootItem = TreeItem(self.headerdata)
        self.setupModelData(data, self.rootItem)
       # self.setupModelData(data.split("\n"), self.rootItem)
        
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("RunDirectories")
        rundir1 = settings.value("runDir1", "/home/ITER/telentm/test")
        alias1 = settings.value("Alias1")
        settings.endGroup()
       # self.file = open("Data.txt","w")
       # self.file.write("%s * * * * * *\n" % alias1)
        self.dirTraverse(alias1, rundir1)
       # self.file.close()
        
    def dirTraverse(self, alias, rundir):
        self.file = open("Data.txt","w")
        self.file.write("%s * * * * * *\n" % alias)
        rootDir = rundir
        path_b = rootDir.split("/")
       # b'C\xc3N'.decode('utf8','replace')
        for dir, subdirs, files in os.walk(rootDir):
            path = dir.split('/')
            r = len(path)-len(path_b)
            #self.file.write(" %s%s\n" % ( r*" ", os.path.basename(dir)))
        self.file.close()

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

        if parentItem == self.rootItem:
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

    def setupModelData(self, lines, parent):
        parents = [parent]
        indentations = [0]

        number = 0

        while number < len(lines):
            position = 0
            while position < len(lines[number]):
                if lines[number][position] != ' ':
                    break
                position += 1

            lineData = lines[number][position:].strip()

            if lineData:
                # Read the column data from the rest of the line.
                columnData = [s for s in lineData.split(' ') if s]

                if position > indentations[-1]:
                    # The last child of the current parent is now the new
                    # parent unless the current parent has no children.

                    if parents[-1].childCount() > 0:
                        parents.append(parents[-1].child(parents[-1].childCount() - 1))
                        indentations.append(position)

                else:
                    while position < indentations[-1] and len(parents) > 0:
                        parents.pop()
                        indentations.pop()

                # Append a new item to the current parent's list of children.
                parents[-1].appendChild(TreeItem(columnData, parents[-1]))

            number += 1

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
    model = None
    data1 = """AUG_16151_D machine * * * * * *
    baserun ready comment1 1.1.2000 telentm ITER 1 10
    run1 on-going comment2 2.1.1980 kosl Asdex-U 2 8
    16151_1.6MW_2.0e19_D=0.4 finished/not_yet_converged comment3 5.5.2005 telentm ITER 3 6
    run_after_conversion finished/not_yet_converged_not_doing_well comment4 2.5.2001 bonninx Textor 5 6
 Tutorial machine * * * * * *
    baserun ready comment5 1.1.2000 telentm ITER 1 10
    tut1 on-going comment6 2.1.1980 kosl Asdex-U 2 8
    tut2 finished/converged comment7 2.5.2001 bonninx Textor 5 6
    remeshed finished/crashed comment8 5.5.2005 kosl ITER 3 4
         baserun not_ready comment9 1.1.2000 telentm ITER 1 10
    """
    file = open("Data.txt","r")
    data = file.readlines()
    
    def __init__(self, *args):
        super(SolpsImpl, self).__init__(*args)
        loadUi('solps-gui.ui', self)
        self.actionAbout_Qt.triggered.connect(QApplication.instance().aboutQt)
        self.checkBoxParameterScan.toggled.connect(
            self.plainTextEditScript.setEnabled)

        self.model = RunsModel(self.data)
        
        # self.model.setRootPath('') # Disable folder watch for now
        self.treeViewRuns.setModel(self.model)
        #self.treeViewRuns.setRootIndex(self.model.index(expanduser("~")))
        # self.model.setFilter(QDir.Dirs|QDir.NoDotAndDotDot)
        # self.model.setNameFilterDisables(0)

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
    Main method.
"""
app = QApplication(sys.argv)
app.setStyle("motif")
widget = SolpsImpl()

widget.show()
sys.exit(app.exec_())
