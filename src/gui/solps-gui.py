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
from PyQt5.QtGui import QStandardItemModel
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
    def __init__(self, archive_dirs, parent=None):
        super(RunsSortFilterProxyModel, self).__init__(parent)
        self.archive_dirs = archive_dirs

    " Parent of accepted children needs to be accepted too for treeviews. "
    def has_accepted_children(self, source_index):
        item = source_index.internalPointer()
        items = item.childItems.copy()
        while items:
            child = items.pop()
            items.extend(child.childItems)
            path = child.data(Column.path)
            if self.filterRegExp().indexIn(path) >= 0 \
                    and path not in self.archive_dirs:
                return True
        return False

    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, Column.path, sourceParent)
        path = self.sourceModel().data(index, Qt.DisplayRole)
        if path in self.archive_dirs:
            return False
        if self.filterRegExp().indexIn(path) >= 0:
            return True
        return self.has_accepted_children(index)

class ArchiveSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, archive_dirs, style, parent=None):
        super(ArchiveSortFilterProxyModel, self).__init__(parent)
        self.archive_dirs = archive_dirs
        self.style = style

    def data(self, index, role):
        if role == Qt.DecorationRole:
            if index.column() == Column.name:
                index_display = self.index(index.row(),
                                           Column.path, index.parent())
                path = self.data(index_display, Qt.DisplayRole)
                if path in self.archive_dirs:
                        return self.style.standardIcon(
                            QStyle.SP_DialogOpenButton)
                return None
        return super(ArchiveSortFilterProxyModel, self).data(index, role)

    " Parent of accepted children needs to be accepted too for treeviews. "
    def has_accepted_children(self, source_index):
        item = source_index.internalPointer()
        items = item.childItems.copy()
        while items:
            child = items.pop()
            items.extend(child.childItems)
            path = child.data(Column.path)
            if path in self.archive_dirs:
                return True
        return False

    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, Column.path, sourceParent)
        path = self.sourceModel().data(index, Qt.DisplayRole)
        if path in self.archive_dirs:
            return True
        for dir in self.archive_dirs:
            if path.find(dir) >= 0:
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

    def retrieve_folder_stats(self, dir):
        path = dir + '/.status'
        if os.path.exists(path):
            mtime = QDateTime.fromTime_t(os.path.getmtime(path))
            try:
                with open(path) as file:
                    lines = file.read().splitlines()
                    file.close()
                #print(path, lines[-1])
                return mtime, lines[-1]
            except OSError:
                return mtime, '.status unknown'
        return QDateTime().currentDateTime(), ''

    def run(self):
        self.status.emit("Updating runs statuses...")
        #self.sleep(1)
        i = 0
        for path in self.model.column_index:
            i = i + 1
            if self.isInterruptionRequested():
                print("Status update interrupted!")
                break
            (data, date_index, status_index) = self.model.column_index[path]
            data[Column.date], data[Column.status] = \
                self.retrieve_folder_stats(path)
            #self.msleep(100)
            self.statusChanged.emit(date_index, status_index)
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
        self.model.create_indices_for_columns()
        self.status.emit("Filesystem scanning finished.")


class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False

        for row in range(count):
            self.childItems.pop(position)

        return True

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

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childItems):
            return False

        for row in range(count):
            data = [None for v in range(columns)]
            item = TreeItem(data, self)
            self.childItems.insert(position, item)

        return True

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        self.itemData[column] = value

        return True

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

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def insertColumns(self, position, columns, parent=QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeColumns(self, position, columns, parent=QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result

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

    def create_indices_for_columns(self):
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

        settings.beginGroup("TreeViewArchive")
        treeview_archive = settings.value("ColumnWidth")
        if treeview_archive: self.treeViewArchive.header().restoreState(
            treeview_archive)
        settings.endGroup()

        settings.beginGroup("Archive")
        size = settings.beginReadArray("dirs")
        self.archive_dirs = set()
        for i in range(size):
            settings.setArrayIndex(i)
            dir = settings.value("dir")
            self.archive_dirs.add(dir)
        settings.endArray()
        settings.endGroup()

        self.actionAbout_Qt.triggered.connect(QApplication.instance().aboutQt)
        self.checkBoxParameterScan.toggled.connect(
            self.plainTextEditScript.setEnabled)

        self.comboBoxRunFilterType.addItem("Regular expression", QRegExp.RegExp)
        self.comboBoxRunFilterType.addItem("Wildcard", QRegExp.Wildcard)
        self.comboBoxRunFilterType.addItem("Fixed string", QRegExp.FixedString)

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
            self.proxyModel = RunsSortFilterProxyModel(self.archive_dirs)
            self.proxyModel.setDynamicSortFilter(True)
            self.proxyModel.setFilterKeyColumn(Column.path)
            self.proxyModel.setSourceModel(self.model)
            self.treeViewRuns.setModel(self.proxyModel)
        else:
            self.treeViewRuns.setModel(self.model)

        self.treeViewRuns.setRootIsDecorated(True)
        self.treeViewRuns.setAlternatingRowColors(True)
        self.treeViewRuns.setSortingEnabled(True)


        self.lineEditRunFilter.returnPressed.connect(self.textFilterChanged)

        # Tree view for archived run directories

        self.archiveProxyModel = \
            ArchiveSortFilterProxyModel(self.archive_dirs, self.style())
        self.archiveProxyModel.setDynamicSortFilter(True)
        self.archiveProxyModel.setFilterKeyColumn(Column.path)
        self.archiveProxyModel.setSourceModel(self.model)
        self.treeViewArchive.setModel(self.archiveProxyModel)
        self.treeViewArchive.setAlternatingRowColors(True)
        self.treeViewArchive.setSortingEnabled(True)

        self.actionJob_list.triggered.connect(self.showdialog)
        self.treeViewRuns.selectionModel().selectionChanged.connect(
            self.enable_archive_button)
        self.treeViewArchive.selectionModel().selectionChanged.connect(
            self.enable_restore_button)


    @pyqtSlot()
    def on_pushButton_Archive_clicked(self):
        index = self.treeViewRuns.selectionModel().currentIndex()
        model = self.proxyModel
        index_path = model.index(index.row(), Column.path, index.parent())
        path = model.data(index_path, Qt.DisplayRole)

        self.archive_dirs.add(path)
        self.proxyModel.invalidateFilter()
        self.archiveProxyModel.invalidateFilter()

        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("Archive")
        settings.beginWriteArray("dirs")
        for i, dir in enumerate(self.archive_dirs):
            settings.setArrayIndex(i)
            settings.setValue("dir", dir)
        settings.endArray()
        settings.endGroup()

    @pyqtSlot()
    def on_pushButton_Restore_clicked(self):
        index = self.treeViewArchive.selectionModel().currentIndex()
        model = self.archiveProxyModel
        index_path = model.index(index.row(), Column.path, index.parent())
        path = model.data(index_path, Qt.DisplayRole)

        if path in self.archive_dirs:
            self.archive_dirs.remove(path)
            self.proxyModel.invalidateFilter()
            self.archiveProxyModel.invalidateFilter()

            settings = QSettings("ITER", "solps-gui")
            settings.beginGroup("Archive")
            settings.beginWriteArray("dirs")
            for i, dir in enumerate(self.archive_dirs):
                settings.setArrayIndex(i)
                settings.setValue("dir", dir)
            settings.endArray()
            settings.endGroup()
        else:
            msg = "Can only remove archived directories marked with icons!"
            QMessageBox.warning(self, 'Invalid action', msg)

    @pyqtSlot()
    def enable_archive_button(self):
        valid = self.treeViewRuns.selectionModel().currentIndex().isValid()
        self.pushButton_Archive.setEnabled(valid)

    @pyqtSlot()
    def enable_restore_button(self):
        valid = self.treeViewArchive.selectionModel().currentIndex().isValid()
        self.pushButton_Restore.setEnabled(valid)

    def create_model(self):
        model = QStandardItemModel()
        self.headerdata = ["Name", "Path", "Date", "Status", "Comment",
                           "Device", "Shot number", "Run number"]
        self.columns = len(self.headerdata)
        self.rootItem = TreeItem(self.headerdata)
        return model

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
        # save GUI settings
        settings = QSettings("ITER", "solps-gui")

        settings.beginGroup("MainWindow")
        settings.setValue("Geometry", self.saveGeometry())
        settings.setValue("State", self.saveState())
        settings.endGroup()

        settings.beginGroup("TreeViewRuns")
        settings.setValue("ColumnWidth", self.treeViewRuns.header().saveState())
        settings.endGroup()

        settings.beginGroup("TreeViewArchive")
        settings.setValue("ColumnWidth", self.treeViewArchive.header().saveState())
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
#app.setStyle("windows")
widget = SOLPS_MainWindow()
widget.show()
sys.exit(app.exec_())
