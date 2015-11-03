#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import sys

from PyQt5.QtCore import (QDateTime, pyqtSlot, QModelIndex, Qt, QSettings,
                          pyqtSignal, QThread, QAbstractItemModel, QVariant,
                          QSortFilterProxyModel, QRegExp)

from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QDialog,
                             QFileDialog, QStyle)

from PyQt5.uic import loadUi
from os.path import expanduser
from enum import IntEnum

"Runs columns definition"
class Column(IntEnum):
    name = 0
    path = 1
    date = 2
    status = 3

class RunsSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(RunsSortFilterProxyModel, self).__init__(parent)

    def has_accepted_children(self, source_index):
        item = source_index.internalPointer()
        items = item.childItems.copy()
        while items:
            child = items.pop()
            items.extend(child.childItems)
            data = child.data(Column.path)
            if self.filterRegExp().indexIn(data) >= 0:
                return True
        return False

    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, Column.path, sourceParent)
        data = self.sourceModel().data(index, Qt.DisplayRole)
        if self.filterRegExp().indexIn(data) >= 0:
            return True
        return self.has_accepted_children(index)

class RunSettings(QDialog):
    runDirsChanged = pyqtSignal()

    def __init__(self, parent=None):
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
        self.lineEdit_monitor_interface.setText(
            settings.value("Monitor_interface", "0.0.0.0"))
        self.lineEdit_monitor_port.setText(
            settings.value("Monitor_port", "49406"))
        settings.endGroup()

        self.toolButtonView1.clicked.connect(self.showdir1)
        self.toolButtonView2.clicked.connect(self.showdir2)
        self.toolButtonView3.clicked.connect(self.showdir3)
        self.toolButtonView4.clicked.connect(self.showdir4)
        self.toolButtonView5.clicked.connect(self.showdir5)

    def update_dir(self, line_edit):
        current_dir = line_edit.text()
        if current_dir == "":
            current_dir = expanduser("~")
        new_dir = QFileDialog.getExistingDirectory(self,
                                                   "Select Directory",
                                                   current_dir,
                                                   QFileDialog.ShowDirsOnly)
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
    def showdir1(self):
        self.update_dir(self.lineEdit_rundir1)

    @pyqtSlot()
    def showdir2(self):
        self.update_dir(self.lineEdit_rundir2)

    @pyqtSlot()
    def showdir3(self):
        self.update_dir(self.lineEdit_rundir3)

    @pyqtSlot()
    def showdir4(self):
        self.update_dir(self.lineEdit_rundir4)

    @pyqtSlot()
    def showdir5(self):
        self.update_dir(self.lineEdit_rundir5)

class RunsStatusServer(QThread):
    sock = None
    retrieve = True
    jobStatusChanged = pyqtSignal(str)

    def bind(self, address, port):
        # connect to UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind socket to local host and port
        try:
            self.sock.bind((address, port))
        except socket.error:
            print('Bind to', address, ':', str(port), ' failed.')
            return False
        print('Server on', address, ':', port)
        return True

    def run(self):
        print("RunsStatusServer started")
        while self.retrieve:
            data, addr = self.sock.recvfrom(1024)  # wait for data
            # print("Message", data.decode('utf-8'), "from", addr[0])
            self.jobStatusChanged.emit(data.decode('utf-8'))

class UpdateRunsStatuses(QThread):
    status = pyqtSignal(str)
    progress = pyqtSignal(str)
    statusChanged = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self, runs_model, parent=None):
        super(UpdateRunsStatuses, self).__init__(parent)
        self.model = runs_model
        print("UpdateRunsStatuses model", self.model)

    def run(self):
        self.status.emit("Updating runs statuses...")
        #self.sleep(1)
        i = 0
        for path in self.model.column_index:
            i = i + 1
            if self.isInterruptionRequested():
                print("Status update interrupted!")
                break
            (data, date, status) = self.model.column_index[path]
            data[Column.status] = 'status #{0}'.format(i)
            data[Column.date] = QDateTime().currentDateTime()
            #self.msleep(100)
            self.statusChanged.emit(date, status)
            self.progress.emit(path)
        self.status.emit("Updating runs statuses finished.")


class FileSytemScan(QThread):
    status = pyqtSignal(str)

    def __init__(self, runs_model, parent=None):
        super(FileSytemScan, self).__init__(parent)
        self.model = runs_model

    def setupModelData(self, rootdir, alias, parent):
        if rootdir is '':
            return
        self.status.emit("Scanning {0}...".format(alias))
        indentations = [len(rootdir.split('/'))]
        parents = [parent]

        for dir, subdirs, files in os.walk(rootdir):
            if dir == rootdir:  # replace name with alias
                date = QDateTime().fromTime_t(os.stat(dir).st_mtime)
                data = [alias, dir, date, None]
                parents[0].appendChild(TreeItem(data, parent))
                continue

            position = len(dir.split('/'))

            if position > indentations[-1]:
                # The last child of the current parent is now the new
                # parent unless the current parent has no children.

                if parents[-1].childCount() > 0:
                    parents.append(
                        parents[-1].child(parents[-1].childCount() - 1))
                    indentations.append(position)

            else:
                while position < indentations[-1] and len(parents) > 0:
                    parents.pop()
                    indentations.pop()
            # Append a new item to the current parent's list of children.
            date = QDateTime().fromTime_t(os.stat(dir).st_mtime)
            data = [os.path.basename(dir), dir, date, None]
            parents[-1].appendChild(TreeItem(data, parents[-1]))

    def run(self):
        self.status.emit("Filesystem scanning started...")
        print("FileSystemScan started")
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("RunDirectories")
        rundir1 = settings.value("runDir1", "")
        alias1 = settings.value("Alias1", "local_1")
        rundir2 = settings.value("runDir2", "")
        alias2 = settings.value("Alias2", "local_2")
        rundir3 = settings.value("runDir3", "")
        alias3 = settings.value("Alias3", "local_3")
        rundir4 = settings.value("runDir4", "")
        alias4 = settings.value("Alias4", "local_4")
        rundir5 = settings.value("runDir5", "")
        alias5 = settings.value("Alias5", "local_5")
        settings.endGroup()

        self.model.rootItem = TreeItem(self.model.headerdata)
        self.setupModelData(rundir1, alias1, self.model.rootItem)
        self.setupModelData(rundir2, alias2, self.model.rootItem)
        self.setupModelData(rundir3, alias3, self.model.rootItem)
        self.setupModelData(rundir4, alias4, self.model.rootItem)
        self.setupModelData(rundir5, alias5, self.model.rootItem)
        self.model.create_indexes_for_columns()
        self.status.emit("Filesystem scanning finished.")


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
    statusServerThread = None
    scanFileSystemThread = None
    column_index = dict()

    def __init__(self, style, parent=None):
        super(RunsModel, self).__init__(parent)
        self.style = style
        self.startRunsStatusServer()
        self.headerdata = ["Name", "Path", "Date", "Status", "Comment",
                           "Device", "Shot number", "Run number"]
        self.columns = len(self.headerdata)
        self.rootItem = TreeItem(self.headerdata)

        self.scanFileSystemThread = FileSytemScan(self)
        self.scanFileSystemThread.finished.connect(self.modelReset.emit)

        self.updateRunsStatusesThread = UpdateRunsStatuses(self)
        self.updateRunsStatusesThread.statusChanged.connect(
            self.dataChanged.emit)
        self.scanFileSystemThread.finished.connect(
            self.updateRunsStatusesThread.start)
        self.updateRunsStatusesThread.finished.connect(self.endResetModel)

    def startThreads(self):
        self.beginResetModel()
        self.scanFileSystemThread.start()

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    # return self.columns
    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DecorationRole:
            if index.column() == 0:
                if self.parent(index) == QModelIndex():
                    return self.style.standardIcon(QStyle.SP_DialogOpenButton)
                else:
                    return self.style.standardIcon(QStyle.SP_DirHomeIcon)

            if index.column() == 1:
                return self.style.standardIcon(QStyle.SP_DirIcon)

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[section])
        if role == Qt.TextAlignmentRole:
            return Qt.AlignHCenter
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

        if parentItem == self.rootItem or parentItem is None:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def create_indexes_for_columns(self):
        "Create hashed dictionary for updating columns specified by path"
        self.column_index = dict()  # path : (itemData, status, date)
        child_items = [self.rootItem.childItems]
        while child_items:
            items = child_items.pop(0)
            for row, childItem in enumerate(items):
                date_index = self.createIndex(row, Column.date, childItem)
                status_index = self.createIndex(row, Column.status, childItem)
                path = childItem.data(Column.path)
                self.column_index[path] = (childItem.itemData,
                                           date_index, status_index)
                if childItem.childItems:
                    child_items.append(childItem.childItems)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    " Run job status server"
    def startRunsStatusServer(self):
        self.statusServerThread = RunsStatusServer()
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("RunDirectories")
        try:
            address = settings.value("Monitor_interface", "0.0.0.0")
            port = int(settings.value("Monitor_port", "49406"))
        except :
            address = "0.0.0.0"
            port = 49406
        settings.endGroup()

        status = self.statusServerThread.bind(address, port)
        if status :
            self.statusServerThread.start()
        else:
            msg = "Failed to bind interface {0} to port {1}. " \
                  "Job monitoring will not start unless you " \
                  "setup free port and restart! " \
                  "GUI will exit if you press Cancel.".format(address, port)
            ret = QMessageBox.warning(None, "SOLPS-GUI Status server", msg,
                                      QMessageBox.Cancel | QMessageBox.Ok)
            if ret == QMessageBox.Cancel:
                sys.exit(1)
        self.statusServerThread.jobStatusChanged.connect(self.jobStatusChanged)

    @pyqtSlot(str)
    def jobStatusChanged(self, message):
        print("Received job status update: ", message)
        try:
            name, path, status = message.split()
            try:
                (itemData, date_index, status_index) = self.column_index[path]
                itemData[Column.status] = status
                itemData[Column.date] = QDateTime().currentDateTime()
                self.dataChanged.emit(date_index, status_index)
            except KeyError:  # TODO insert non monitored message anyway
                print(path, "not monitored. Skipping status update.")
        except ValueError:
            print("Received invalid message:", message,
                  "Message should be in <name> <path> <status> format.")


class SOLPS_MainWindow(QMainWindow):
    def __init__(self, *args):
        super(SOLPS_MainWindow, self).__init__(*args)
        loadUi('solps-gui.ui', self)
        self.actionAbout_Qt.triggered.connect(QApplication.instance().aboutQt)
        self.checkBoxParameterScan.toggled.connect(
            self.plainTextEditScript.setEnabled)

        self.comboBoxRunFilerType.addItem("Regular expression", QRegExp.RegExp)
        self.comboBoxRunFilerType.addItem("Wildcard", QRegExp.Wildcard)
        self.comboBoxRunFilerType.addItem("Fixed string", QRegExp.FixedString)

        self.filterCaseSensitivityCheckBox.setChecked(True)

        self.model = RunsModel(self.style())
        self.model.scanFileSystemThread.status.connect(
            self.statusbar.showMessage)
        self.model.updateRunsStatusesThread.status.connect(
            self.statusbar.showMessage)
        self.model.startThreads()

        self.model.updateRunsStatusesThread.finished.connect(
            self.treeViewRuns.update)
        if True:  # use Filter if True
            self.proxyModel = RunsSortFilterProxyModel()
            self.proxyModel.setDynamicSortFilter(True)
            self.proxyModel.setFilterKeyColumn(Column.path)
            self.proxyModel.setSourceModel(self.model)
            self.treeViewRuns.setModel(self.proxyModel)
        else:
            self.treeViewRuns.setModel(self.model)

        self.treeViewRuns.setRootIsDecorated(True)
        self.treeViewRuns.setAlternatingRowColors(True)
        self.treeViewRuns.setSortingEnabled(True)
        #self.treeViewRuns.sortByColumn(Column.date, Qt.AscendingOrder)

        self.lineEditRunFilter.returnPressed.connect(self.textFilterChanged)


        # get GUI settings
        settings = QSettings("ITER", "solps-gui")

        settings.beginGroup("MainWindow")
        geometry = settings.value("Geometry")
        if geometry:  self.restoreGeometry(geometry)
        state = settings.value("State")
        if state: self.restoreState(state)
        settings.endGroup()

        settings.beginGroup("TreeViewRuns")
        treeview = settings.value("ColumnWidth")
        if treeview: self.treeViewRuns.header().restoreState(treeview)
        settings.endGroup()


        self.actionJob_list.triggered.connect(self.showdialog)

    def textFilterChanged(self):
        filter_index = self.comboBoxRunFilerType.currentIndex()
        filter_syntax = self.comboBoxRunFilerType.itemData(filter_index)
        syntax = QRegExp.PatternSyntax(filter_syntax)
        caseSensitivity = (self.filterCaseSensitivityCheckBox.isChecked()
            and Qt.CaseSensitive or Qt.CaseInsensitive)
        regExp = QRegExp(self.lineEditRunFilter.text(), caseSensitivity, syntax)
        self.proxyModel.setFilterRegExp(regExp)

    def showdialog(self):
        dialog = RunSettings()
        response = dialog.exec_()
        if response:
            if self.model.updateRunsStatusesThread.isRunning() or \
                    self.model.scanFileSystemThread.isRunning():
                msg = "Runs layout changed in the middle of the update." \
                    "Directories cannot be changed. Try settings later."
                QMessageBox.critical(self, "Restart required", msg)
            else:
                self.model.startThreads()
            #self.model.updateRunsStatusesThread.quit()
            #self.model.scanFileSystemThread.start()


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
        self.textFilterChanged()

    @pyqtSlot()
    def on_pushButton_8_clicked(self):  # Testing only
        settings = QSettings('ITER', 'solps-gui')
        settings.beginGroup('RunDirectories')
        path = settings.value('runDir2', '')
        settings.endGroup()
        (data, date, status) = self.model.column_index[path]
        data[Column.status] = 'running'
        data[Column.date] = QDateTime().currentDateTime()
        self.model.dataChanged.emit(date, status)

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        msg = "GUI will enable users to monitor multiple simultaneously " \
              "running cases, which requires defining the working directory " \
              "(folder) for each case to be separated from each other. " \
              "Input file builder will depend on it to correctly save input " \
              "files for multiple parameter scan cases."
        QMessageBox.about(self, 'About SOLPS-ITER GUI', msg)


"  Main method "
app = QApplication(sys.argv)
# app.setStyle("motif")
widget = SOLPS_MainWindow()
widget.show()
sys.exit(app.exec_())
