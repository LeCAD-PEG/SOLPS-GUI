#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" SOLPS GUI aims controlling SOLPS-ITER code suite with a framework
consisting of various tools aiming at improving the user’s experience,
to accelerate and simplify run input set-up, and to increase the scientific
us ability of the B2.5-Eirene  simulation results. GUI allows a large set of
runs  to be scanned, identifying the state they are in, and providing a
framework for in-line analysis and run re-launch, including input file editing
beforehand.

Example:
  Running the GUI requires Python3 and PyQt5 to be installed::

    $ python3 solps.py

  or::

    $ ./solps.py

Notes:
    Listed Runs can receive status updates from network with single line
    UDP message with netcat utility or from the client that can broadcast
    to multiple IP destinations at once.

.. _Google Python Style Guide:
   http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
   http://sphinx-doc.org/ext/example_google.html#example-google
   http://sphinx-doc.org/ext/napoleon.html#module-sphinx.ext.napoleon
   Author: Leon Kos, University of Ljubljana
"""

import getopt
import logging
import os
import shutil
import socket
import sys
import queue
import time




from PyQt5.QtCore import (QDateTime, pyqtSlot, QModelIndex, Qt, QSettings,
                          pyqtSignal, QThread, QAbstractItemModel, QVariant,
                          QSortFilterProxyModel, QRegExp, QObject, QRect,
                          QSize, QProcess)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QDialog,
                             QFileDialog, QStyle, QStyledItemDelegate)
from PyQt5.QtGui import (QStandardItemModel, QFontMetrics, QPen)
from PyQt5.uic import loadUi
from enum import IntEnum

REDIRECT_STDOUT_TO_LOG = False

class Column:
    """Column enumeration for Runs treeview.

        First column `name` cannot be moved and is short name.

    Attributes:
        name : Basename of the directory
        path : Full path to the directory
        date : Last status update of the directory. Uses LC_TIME environment.
        status : Status retrieved from status & log files or via network update
        label : One line description of the run from b2mn.dat
    """
    name, path, date, status, label = range(5)




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


class RunsSettings(QDialog):
    """ Runs settings dialog described in runs.ui configures several
        directories with SOLPS "runs". Each directory may have its own
        SOLPSTOP environment and can also be from other users that one
        wants to explore or monitor.
    """
    runDirsChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(RunsSettings, self).__init__()
        prefix = os.path.dirname(os.path.abspath(__file__))
        loadUi(prefix + '/runs.ui', self)
        # get GUI settings
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("RunDirectories")
        rundir1 = settings.value("runDir1", os.path.expanduser("~"))
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
        settings.endGroup()



        self.toolButtonView1.clicked.connect(self.showdir1)
        self.toolButtonView2.clicked.connect(self.showdir2)
        self.toolButtonView3.clicked.connect(self.showdir3)
        self.toolButtonView4.clicked.connect(self.showdir4)
        self.toolButtonView5.clicked.connect(self.showdir5)

    def update_dir(self, line_edit):
        current_dir = line_edit.text()
        if current_dir == "":
            current_dir = os.path.expanduser("~")
        new_dir = QFileDialog.getExistingDirectory(self,
                                                   "Select Directory",
                                                   current_dir,
                                                   QFileDialog.ShowDirsOnly)
        if new_dir:
            line_edit.setText(new_dir)

    def setRunsSettings(self):
        """ Save Runs directories into settings and emits that the directories
            were changed and are needed to be completely rescanned.
        """
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

class Preferences(QDialog):
    def __init__(self, parent=None):
        super(Preferences, self).__init__()
        prefix = os.path.dirname(os.path.abspath(__file__))
        loadUi(prefix + '/preferences.ui', self)
        # get GUI settings
        settings = QSettings('ITER', 'solps-gui')
        self.lineEdit_monitor_interface.setText(settings.value(
            'SOLPS_GUI_BIND', self.lineEdit_monitor_interface.text()))
        self.lineEdit_monitor_port.setText(settings.value(
            'SOLPS_GUI_PORT', self.lineEdit_monitor_port.text()))
        self.lineEdit_monitor_ip.setText(settings.value(
            'SOLPS_GUI_IP', self.lineEdit_monitor_ip.text()))
        self.lineEdit_tcsh_path.setText(settings.value(
            'tcsh_path', self.lineEdit_tcsh_path.text()))
        self.lineEdit_gnuplot_path.setText(settings.value(
            'gnuplot_path', self.lineEdit_gnuplot_path.text()))
        self.comboBox_log_level.setCurrentIndex(int(settings.value(
            'log_level', self.comboBox_log_level.currentIndex())))
        self.comboBox_submit_script.setCurrentText(settings.value(
            'submit_script', self.comboBox_submit_script.currentText()))
        self.checkBox_use_mpi.setCheckState(int(settings.value(
            'use_mpi', self.checkBox_use_mpi.checkState())))
        self.lineEdit_mpi_options.setText(settings.value(
            'MPI_OPTS', self.lineEdit_mpi_options.text()))
        self.checkBox_use_debugger.setCheckState(int(settings.value(
            'use_debugger', self.checkBox_use_debugger.checkState())))
        self.lineEdit_debugger.setText(settings.value(
            'debugger', self.lineEdit_debugger.text()))
        self.checkBox_compress_log.setCheckState(int(settings.value(
            'compress_log', self.checkBox_compress_log.checkState())))
        self.checkBox_dry_run.setCheckState(int(settings.value(
            'dry_run', self.checkBox_dry_run.checkState())))

    def setPreferences(self):
        s = QSettings('ITER', 'solps-gui')
        s.setValue('SOLPS_GUI_BIND',  self.lineEdit_monitor_interface.text())
        s.setValue('SOLPS_GUI_PORT', self.lineEdit_monitor_port.text())
        s.setValue('SOLPS_GUI_IP', self.lineEdit_monitor_ip.text())
        s.setValue('tcsh_path', self.lineEdit_tcsh_path.text())
        s.setValue('gnuplot_path', self.lineEdit_gnuplot_path.text())
        s.setValue('log_level', str(self.comboBox_log_level.currentIndex()))
        s.setValue('submit_script', self.comboBox_submit_script.currentText())
        s.setValue('use_mpi', self.checkBox_use_mpi.checkState())
        s.setValue('MPI_OPTS', self.lineEdit_mpi_options.text())
        s.setValue('use_debugger', self.checkBox_use_debugger.checkState())
        s.setValue('debugger', self.lineEdit_debugger.text())
        s.setValue('compress_log', self.checkBox_compress_log.checkState())
        s.setValue('dry_run', self.checkBox_dry_run.checkState())
        log_levels = [logging.DEBUG, logging.INFO, logging.WARNING,
                      logging.ERROR, logging.CRITICAL]
        log_level = log_levels[self.comboBox_log_level.currentIndex()]
        logging.getLogger().setLevel(log_level)

class RunsStatusServer(QThread):
    """ Networking UDP listener for receiving job status updates.

    Receives datagrams in single line and emits decoded one line updates sent
    by each job to notify the GUI that status changed.

    Attributes:
        retrieve (Bool) : Gracefully stop the thread on next packet.
    """
    retrieve = True
    jobStatusChanged = pyqtSignal(str)

    def bind(self, address, port):
        # connect to UDP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind socket to local host and port
        try:
            self._sock.bind((address, port))
        except socket.error:
            logging.error('Bind to' + address + ':' + str(port) + ' failed.')
            return False
        logging.info('Server listening on ' + address + ':' + str(port))
        return True

    def run(self):
        logging.info("RunsStatusServer started.")
        while self.retrieve:
            data, addr = self._sock.recvfrom(1024)  # wait for data
            # print("Message", data.decode('utf-8'), "from", addr[0])
            self.jobStatusChanged.emit(data.decode('utf-8').rstrip('\n'))
            # TODO Graceful exit from blocking recvfrom() by setting retrieve
            # TODO and sending UDP packet to ourselves.


class RetrieveRunsFolderInfo(QThread):
    """ Scans filesystem and retrieves state of each run.

    Several status and LOG files are probed and searched to get the state
    and other info for Runs table view.

    Args:
        runs_model (RunsModel): Model that holds Runs

    Attributes:
        status(pyqtSignal(str)): Emits start/stop notices for status bar.
        progress(pyqtSignal(str)): Directory that is being processed
        statusChanged (pyqtSignal(QModelIndex, QModelIndex)) :
            Changed index range for table view update

    """
    status = pyqtSignal(str)
    progress = pyqtSignal(str)
    statusChanged = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self, runs_model, parent=None):
        super(RetrieveRunsFolderInfo, self).__init__(parent)
        self.model = runs_model

    def retrieve_folder_state(self, directory):
        """ Scans directory for existance of status and log files.

        .status and run.log are scanned for status and errors.

        Args:
            directory (str): Directory to scan
        Returns:
            time, status (str, str), static_data : Tuple that is at
                least directory time and empty string. Otherwise it returns
                extracted status string and modification time of the file
                that string was retrieved from and other static data from
                various files.
        """
        # Firstly try to extract label from the beginning of b2mn.dat
        path = directory + '/b2mn.dat'
        label = ''
        if os.path.exists(path):
            try:
                with open(path) as file:
                    lines = file.read(512).splitlines()  # just one sector
                for i, line in enumerate(lines):
                    if 'label' in line:
                        label = lines[i+1].strip("' ")
                        break
            except OSError:
                label = 'b2mn.dat unreadable'

        static_data = label


        # Parse run.log
        path = directory + '/run.log'
        if os.path.exists(path):
            mtime = os.path.getmtime(path)
            qtime = QDateTime.fromTime_t(mtime)  # Qt formatted datetime
            try:
                fsize = os.path.getsize(path)
                with open(path) as f:
                    f.seek(max(fsize-8192, 0), 0)  # Set pos @ last 100 lines
                    lines = f.read().splitlines()  # Read to end
                for line in lines:
                    if 'stopping because' in line \
                            or 'failed' in line \
                            or 'ERROR' in line \
                            or 'UNABLE' in line:
                        return qtime, line, static_data

                # Is there B2 running directory?
                b2mn_exe_dir = directory + '/b2mn.exe.dir'
                if os.path.exists(b2mn_exe_dir):
                    if time.time() - mtime > 60: # Is run.log fresh enough?
                        return qtime, 'CRASHED in b2mn.exe.dir', static_data
                    else:
                        return qtime, 'Running', static_data
                logging.warning("No status found in " + path)
                return qtime, 'run.log without status', static_data
            except OSError:
                return qtime, 'run.log permission denied', static_data

        # Retrieve last line of .status
        path = directory + '/.status'
        if os.path.exists(path):
            mtime = os.path.getmtime(path)
            qtime = QDateTime.fromTime_t(mtime)
            try:
                with open(path) as file:
                    lines = file.read().splitlines()
                last_status_line = lines[-1]
                # detect crashed that 'Started' without run.log present
                if time.time() - mtime > 60 and 'Started' in last_status_line:
                    return qtime, 'CRASHED? ' + last_status_line, static_data
                else:
                    return qtime, last_status_line, static_data
            except OSError:
                return qtime, '.status permission denied', static_data

        # Try to return at least directory date as last status
        try:
            qtime = QDateTime.fromTime_t(os.path.getmtime(directory))
            return qtime, '', static_data
        except OSError:
            return QDateTime().currentDateTime(), 'no access', static_data




    def run(self):
        """ Thread scans each listed directory of the Runs model.
          
        In principle this operation should be thread safe when changing model
        data. However, one should not restart the scan if this thread is
        not finished yet with scan!
        """
        msg = "Updating runs statuses..."
        logging.info(msg)
        self.status.emit(msg)
        i = 0
        for path in self.model.column_index:
            if self.isInterruptionRequested():
                logging.warning("Status update interrupted!")
                break
            (data, date_index, status_index, label_index) = \
                self.model.column_index[path]
            data[Column.date], data[Column.status], static_data = \
                self.retrieve_folder_state(path)
            # Simulate delays with self.msleep(100)
            # Fill in static data into the columns that follow
            data[Column.label] = static_data
            # Emit the range of columns that changed in the model
            self.statusChanged.emit(date_index, label_index)
            self.progress.emit(path)
        msg = "Updating run statuses finished. " \
                + str(len(self.model.column_index)) + " directories scanned."
        logging.info(msg)
        self.status.emit(msg)


class FileSystemScan(QThread):
    """ Creates initial list of directory tree hierarchy of all aliased Runs.

    This is quick scan for of all directories to be quickly shown in the
    tree view and shortly after updated with longer run in separate thread
    with `RetrieveRunsFolderInfo` operation. Nevertheless, this is done in
    a thread to give immediate response (GUI) to the user after its start.
    Tree view is shown empty until this scan finished and model is reset.
    """
    status = pyqtSignal(str)

    def __init__(self, runs_model, parent=None):
        super(FileSystemScan, self).__init__(parent)
        self.model = runs_model

    def setup_model_data(self, rootdir, alias, parent):
        if rootdir is '':
            return
        self.status.emit("Scanning {0}...".format(alias))
        indentations = [len(rootdir.split('/'))]
        parents = [parent]

        for dir, subdirs, files in os.walk(rootdir):
            if dir == rootdir:  # replace name with alias
                date = QDateTime().fromTime_t(os.stat(dir).st_mtime)
                data = [alias, dir, date, None, None]  # TODO number of columns
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
            # TODO Size data to number of columns in use
            data = [os.path.basename(dir), dir, date, None, None]
            parents[-1].appendChild(TreeItem(data, parents[-1]))

    def run(self):
        msg = "Filesystem scanning started..."
        self.status.emit(msg)
        logging.info(msg)
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
        self.setup_model_data(rundir1, alias1, self.model.rootItem)
        self.setup_model_data(rundir2, alias2, self.model.rootItem)
        self.setup_model_data(rundir3, alias3, self.model.rootItem)
        self.setup_model_data(rundir4, alias4, self.model.rootItem)
        self.setup_model_data(rundir5, alias5, self.model.rootItem)

        self.model.create_indices_for_columns()

        msg = "Filesystem scanning finished."
        logging.info(msg)
        self.status.emit(msg)


class TreeItem(object):
    """ Each item in Runs tree view is itemized into parent, data and childs.
    Attributes:
        parentItem (TreeItem) : Pointer to parent.
        itemData (list) : Column data for tree view. First is always name (str)
        childItems (list) : Rows of child items references.
    """
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

class TextElideLeftDelegate(QStyledItemDelegate):
    """ Elide text of the first column to the left (... at start).
    This allows long folder names to be shown right aligned when they are too
    long to fit int the column width as usually the folder name changes at the
    end of the Run name (e.g. with sequence or parameter).
    """
    def __init__(self, parent=None):
        super(TextElideLeftDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        painter.save()
        if index.column() == Column.name:  # Elide text on the left
            painter.setPen(QPen(Qt.black))
            value = index.data(Qt.DisplayRole)
            icon = index.data(Qt.DecorationRole)
            rect_size = QSize(option.rect.width(), option.rect.height())
            icon_width = icon.actualSize(rect_size).width() + 4  # spacer too
            text_width = option.rect.width() - icon_width
            metrics = QFontMetrics(painter.font())
            elided_text = metrics.elidedText(value, 0, text_width, 0)
            if isinstance(value, str):
                icon.paint(painter, option.rect, Qt.AlignLeft)
                x, y, width, height = option.rect.getCoords()
                text_rect = QRect(x + icon_width, y,
                                  width - icon_width, height)
                painter.drawText(text_rect, Qt.AlignLeft, elided_text)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)
        painter.restore()


class RunsModel(QAbstractItemModel):
    """ Model for the Runs and Archive tree views.

    Data in columns that is presents directories in a hierarchical way.

    Args:
        style (QStyle) : Widget decoration style used to retrieve builtin
                         icons.

    Attributes:
        column_index (path : data, date_index, status_index, label_index) :
            Dictionary of data pointer and model indexes for cell update
            with `FileSystemScan` or via network.
            Keys are paths to "unique" directories.
    """
    statusServerThread = None
    scanFileSystemThread = None
    column_index = dict()

    def __init__(self, style, parent=None):
        super(RunsModel, self).__init__(parent)
        self.style = style

        self.startRunsStatusServer()

        self.headerdata = ['Name', 'Path', 'Date', 'Status', 'Label',
                           'Comment', 'Device', 'Shot', 'Run']
        self.columns = len(self.headerdata)
        self.rootItem = TreeItem(self.headerdata)
        self.scanFileSystemThread = FileSystemScan(self)
        self.scanFileSystemThread.finished.connect(self.modelReset.emit)
        self.RetrieveRunsFolderInfoThread = RetrieveRunsFolderInfo(self)
        self.RetrieveRunsFolderInfoThread.statusChanged.connect(
            self.dataChanged.emit)
        self.scanFileSystemThread.finished.connect(
            self.RetrieveRunsFolderInfoThread.start)
        self.RetrieveRunsFolderInfoThread.finished.connect(self.endResetModel)

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
        columns = self.rootItem.columnCount()
        success = parentItem.insertChildren(position, rows, columns)
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

        column = index.column()

        if  column == Column.path or column == Column.date:
            return False

        # disalow changing 'name' except for aliased names (not saved)
        if column == Column.name and self.parent(index) != QModelIndex():
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)
            if column == Column.label:  # set the label in b2mn.dat
                directory = item.data(Column.path)
                path = directory + '/b2mn.dat'
                try:
                    with open(path) as file:
                        lines = file.read().splitlines()  # whole file
                    for i, line in enumerate(lines):
                        if '*label' in line:
                            lines[i+1] = " '" + value + "'"
                            with open(path, 'w') as f:
                                f.write('\n'.join(lines))
                            break
                except OSError:
                    QMessageBox.warning(None, "Permission problem",
                                        "Can't update " + path)
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

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

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
        self.column_index = dict()  # path : (itemData, status, date, label)
        child_items = [self.rootItem.childItems]
        while child_items:
            items = child_items.pop(0)
            for row, childItem in enumerate(items):
                date_index = self.createIndex(row, Column.date, childItem)
                status_index = self.createIndex(row, Column.status, childItem)
                label_index = self.createIndex(row, Column.label, childItem)
                path = childItem.data(Column.path)
                self.column_index[path] = (childItem.itemData,  date_index,
                                           status_index, label_index)
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


    def startRunsStatusServer(self):
        """ Run networking job status server for status updates.

            Status server listens on all (0.0.0.0) or specified network
            interface. UDP messages should be send in format: name path status
        """
        self.statusServerThread = RunsStatusServer()
        settings = QSettings("ITER", "solps-gui")
        default_port = 51966 + os.getuid() % 8192
        try:  # TODO Assign default port number by looking at system UID range
            address = settings.value("SOLPS_GUI_BIND", "0.0.0.0")
            port = int(settings.value("SOLPS_GUI_PORT", str(default_port)))
        except:
            address = "0.0.0.0"
            port = default_port
            settings.setValue('SOLPS_GUI_BIND', address)
            settings.setValue('SOLPS_GUI_PORT', str(port))

        status = self.statusServerThread.bind(address, port)
        if status:
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
        try:
            name, path, status = message.split(maxsplit=2)
            try:
                itemData, date_index, status_index, label_index = \
                    self.column_index[path]
                itemData[Column.status] = status
                itemData[Column.date] = QDateTime().currentDateTime()
                self.dataChanged.emit(date_index, status_index)
                logging.info("Received job status update: " + message)
            except KeyError:  # TODO insert non monitored message anyway
                msg = name + ':' + path + " not monitored "
                msg += 'Skipping "' + status + '" update.'
                logging.warning(msg)
            except ValueError:
                assert(len(self.column_index[path]) == 4)  # indexing changed
        except ValueError as e:
            logging.error(str(e) + " Received essage: '" + message +
                  "' should be in 'name path status' format.")


class LoggingHandler(logging.Handler):
    def __init__(self, stream):
        super(LoggingHandler, self).__init__()
        self.stream = stream

    def emit(self, record):
        msg = self.format(record)
        if record.levelno == logging.DEBUG:
            self.stream.write('<font color="blue">' + msg + '</font>')
        elif record.levelno == logging.INFO:
            self.stream.write('<font color="orange">' + msg + '</font>')
        elif record.levelno == logging.WARNING:
            self.stream.write('<font color="blue">' + msg + '</font>')
        elif record.levelno == logging.ERROR:
            self.stream.write('<font color="red">' + msg + '</font>')
        else:  # logging.CRITICAL
            self.stream.write('<font color="magenta">' + msg + '</font>')


class WriteStream(object):
    """ The new Stream Object which replaces the default stream associated with
    sys.stdout and sys.stderr. This object just puts data in a queue!

    Args:
        queue(queue.Queue) : thread safe queue created for the stream
    """
    def __init__(self, queue):
        self.queue = queue

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, text):
        self.queue.put(text)


class LogReceiver(QObject):
    """ Receives log messages from Logging and sys.stdout.

    A QObject (to be run in a QThread) which sits waiting for data to come
    through a queue.Queue(). It blocks until data is available, and one it
    has got something from the queue, it sends it to the "MainThread"
    by emitting a Qt Signal.
    """
    log_signal = pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    @pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.log_signal.emit(text)


class SOLPS_MainWindow(QMainWindow):
    """Main window of the SOLPS GUI

    Attributes:
        log_thread(QThread) : Thread for Logging facility in Log tab.
        log_receiver(LogReceiver) : Receiving messages from logging thread.
        stdout_thread(QThread) : Redirected sys.stdout to Log tab.
        stdout_receiver(LogReceiver): Receiver for stdout thread.
    """

    runSelected = pyqtSignal(str)

    def __init__(self, *args):
        super(SOLPS_MainWindow, self).__init__(*args)
        prefix = os.path.dirname(os.path.abspath(__file__))
        ui_path = prefix + '/solps.ui'
        try:
            opts, args = getopt.getopt(app.arguments()[1:],
                                       "hu:d",["help","ui=","default"])
        except getopt.GetoptError:
            print ('Supplied option not recognized!')
            print ('For help: solps.py -h / --help')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', "--help"):
                print ('Load default user interface : solps.py')
                print ('Load custom user interface : solps.py '
                       '[-u / --ui] <UIfile.ui>')
                sys.exit(2)
            elif opt in ("-u", "--ui"):
                ui_path =  os.path.abspath(arg)

        if os.path.exists(ui_path):
            ui_filename, ui_extension = os.path.splitext(ui_path)
            if ui_extension == '.ui':
                loadUi(ui_path, self)
            else:
                print(ui_path + ' shoud have .ui extension')
                sys.exit(2)
        else:
            print(ui_path + ' not found')
            sys.exit(2)


        self.main_tcsh = QProcess()  # for job sumbission and scripting
        self.solps_top = None  # Current active ${SOLPSTOP} for tcsh

        self.previous_tab_index = None   # For auto saving of Edit tab
        self.input_tab_index = self.tabWidget.indexOf(self.tab_Input)

        # Create thread-safe Queue and redirect logging it
        log_queue = queue.Queue()
        log_stream = WriteStream(log_queue)
        self.log_thread = QThread()
        self.log_receiver = LogReceiver(log_queue)
        self.log_receiver.log_signal.connect(
            self.plainTextEdit_Log.appendHtml)
        self.log_receiver.moveToThread(self.log_thread)
        self.log_thread.started.connect(self.log_receiver.run)
        self.log_thread.start()
        log_handler = LoggingHandler(log_stream)
        log_format = "%(asctime)s %(levelname)s: %(message)s"
        log_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(log_handler)
        # get GUI settings
        settings = QSettings("ITER", "solps-gui")
        log_levels = [logging.DEBUG, logging.INFO, logging.WARNING,
                      logging.ERROR, logging.CRITICAL]
        log_level = log_levels[int(settings.value('log_level', '1'))]
        logging.getLogger().setLevel(log_level)

        if REDIRECT_STDOUT_TO_LOG:
            # Create thread-safe Queue and redirect sys.stdout to it
            stdout_queue = queue.Queue()
            sys.stdout = WriteStream(stdout_queue)
            self.stdout_thread = QThread()
            self.stdout_receiver = LogReceiver(stdout_queue)
            self.stdout_receiver.log_signal.connect(
                self.plainTextEdit_Log.insertPlainText)
            self.stdout_receiver.moveToThread(self.stdout_thread)
            self.stdout_thread.started.connect(self.stdout_receiver.run)
            self.stdout_thread.start()



        settings.beginGroup("MainWindow")
        geometry = settings.value("Geometry")
        if geometry:
            self.restoreGeometry(geometry)
        state = settings.value("State")
        if state:
            self.restoreState(state)
        settings.endGroup()

        settings.beginGroup("TreeViewRuns")
        treeview = settings.value("ColumnWidth")
        if treeview:
            self.treeViewRuns.header().restoreState(treeview)
        settings.endGroup()

        settings.beginGroup("TreeViewArchive")
        treeview_archive = settings.value("ColumnWidth")
        if treeview_archive:
            self.treeViewArchive.header().restoreState(treeview_archive)
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

        self.comboBoxRunFilterType.addItem("Regular expression",
                                           QRegExp.RegExp)
        self.comboBoxRunFilterType.addItem("Wildcard", QRegExp.Wildcard)
        self.comboBoxRunFilterType.addItem("Fixed string", QRegExp.FixedString)

        self.filterCaseSensitivityCheckBox.setChecked(True)

        self.model = RunsModel(self.style())
        self.model.scanFileSystemThread.status.connect(
            self.statusbar.showMessage)
        self.model.RetrieveRunsFolderInfoThread.status.connect(
            self.statusbar.showMessage)
        self.model.startThreads()

        self.model.RetrieveRunsFolderInfoThread.finished.connect(
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
        self.treeViewRuns.setSortingEnabled(True)

        # Create a delegate for first column to elide text to the left
        elide_left_delegate = TextElideLeftDelegate(self.treeViewRuns)
        self.treeViewRuns.setItemDelegate(elide_left_delegate)

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

        # Setup input tabs
        self.solpsinput.setup_tabs()
        self.tab_Input.setEnabled(False)


        self.actionRuns.triggered.connect(self.show_runs_dialog)
        self.actionPreferences.triggered.connect(self.show_preferences_dialog)
        self.treeViewRuns.selectionModel().selectionChanged.connect(
            self.run_selected)
        self.treeViewArchive.selectionModel().selectionChanged.connect(
            self.enable_restore_button)

        # Configure Dashboard

        #self.gnuplot.plot("sin(3*x)/x")
        #self.runSelected.connect(self.label_7.setText)
        self.runSelected.connect(self.director.setRundir)
        #self.runSelected.connect(self.tcsh.setRundir)
        #self.tcsh.setTcshCommand(self.lineEdit.text())
        #  self.gnuplot.setText("Started")
        #  print(self.gnuplot.process.state())
        #  self.gnuplot1.process.finished.connect(self.gnuplot1.show_plot)

    @pyqtSlot()
    def on_pushButton_Archive_clicked(self):
        """ Selecting directory and pressing Archive will add
        selected directory to filtered set and will not be shown in Runs.
        """
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

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, tab_index):
        """ Signal is received when tab on main window is changed.
            We check if the Edit tab lost its focus and save modified files.

            Arguments:
                 tab_index (int): current tab index selected
        """
        if tab_index != self.input_tab_index \
                and self.previous_tab_index == self.input_tab_index:
            self.solpsinput.save_modified_input_files()
        self.previous_tab_index = tab_index

    @pyqtSlot()
    def on_pushButton_Edit_clicked(self):
        """ For selected run and Edit button pressed Input tab is focused
            with all SOLPS input files modifiable with simple text editor.
        """
        self.tabWidget.setCurrentIndex(self.input_tab_index)
        index = self.treeViewRuns.selectionModel().currentIndex()
        model = self.proxyModel
        index_path = model.index(index.row(), Column.path, index.parent())
        path = model.data(index_path, Qt.DisplayRole)
        self.statusbar.showMessage('Editing ' + path)
        self.solpsinput.setRundir(path)
        self.solpsinput.read_input_files()
        self.tab_Input.setEnabled(True)

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
            for i, directory in enumerate(self.archive_dirs):
                settings.setArrayIndex(i)
                settings.setValue("dir", directory)
            settings.endArray()
            settings.endGroup()
        else:
            msg = "Can only remove archived directories marked with icons!"
            QMessageBox.warning(self, 'Invalid action', msg)

    @pyqtSlot()
    def run_selected(self):
        """ Whenever an item in Runs is selected this function is run.

            Archive button is enabled and directory is emited.
        """
        valid = self.treeViewRuns.selectionModel().currentIndex().isValid()
        self.pushButton_Archive.setEnabled(valid)
        self.pushButton_Continue.setEnabled(valid)
        self.pushButton_Edit.setEnabled(valid)
        self.pushButton_Import.setEnabled(valid)
        self.pushButton_Run.setEnabled(valid)
        self.pushButton_Stop.setEnabled(valid)


        if valid:
            index = self.treeViewRuns.selectionModel().currentIndex()
            model = self.proxyModel
            index_path = model.index(index.row(), Column.path, index.parent())
            path = model.data(index_path, Qt.DisplayRole)
            self.runSelected.emit(path)

    @pyqtSlot()
    def enable_restore_button(self):
        valid = self.treeViewArchive.selectionModel().currentIndex().isValid()
        self.pushButton_Restore.setEnabled(valid)

    def textFilterChanged(self):
        filter_index = self.comboBoxRunFilterType.currentIndex()
        filter_syntax = self.comboBoxRunFilterType.itemData(filter_index)
        syntax = QRegExp.PatternSyntax(filter_syntax)
        case_sense = (self.filterCaseSensitivityCheckBox.isChecked() and
                      Qt.CaseSensitive or Qt.CaseInsensitive)
        regExp = QRegExp(self.lineEditRunFilter.text(), case_sense, syntax)
        self.proxyModel.setFilterRegExp(regExp)

    @pyqtSlot()
    def show_runs_dialog(self):
        dialog = RunsSettings()
        if dialog.exec_():
            dialog.setRunsSettings()
            if self.model.RetrieveRunsFolderInfoThread.isRunning() or \
                    self.model.scanFileSystemThread.isRunning():
                msg = "Runs layout changed in the middle of the update." \
                    "Directories cannot be changed. Try settings later."
                QMessageBox.critical(self, "Restart required", msg)
            else:
                self.model.startThreads()
            # TODO(kosl) self.model.RetrieveRunsFolderInfoThread.quit()
            # self.model.scanFileSystemThread.start()

    @pyqtSlot()
    def show_preferences_dialog(self):
        dialog = Preferences()
        if dialog.exec_():
            dialog.setPreferences()

    def closeEvent(self, event):
        """ Save GUI state at exit.
        Position, size of the main windows and treview columns configuration
        is saved.
        """
        settings = QSettings("ITER", "solps-gui")

        settings.beginGroup("MainWindow")
        settings.setValue("Geometry", self.saveGeometry())
        settings.setValue("State", self.saveState())
        settings.endGroup()

        settings.beginGroup("TreeViewRuns")
        settings.setValue("ColumnWidth",
                          self.treeViewRuns.header().saveState())
        settings.endGroup()

        settings.beginGroup("TreeViewArchive")
        settings.setValue("ColumnWidth",
                          self.treeViewArchive.header().saveState())
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
    def on_pushButton_Filter_clicked(self):
        self.textFilterChanged()

    @pyqtSlot()
    def on_pushButton_Stop_clicked(self):
        """ Signals garceful stop inside b2mn.exe.dir with .quit file.
        """
        index = self.treeViewRuns.selectionModel().currentIndex()
        model = self.proxyModel
        index_path = model.index(index.row(), Column.path, index.parent())
        directory = model.data(index_path, Qt.DisplayRole)
        # Is there B2 running directory?
        try:
            b2mn_exe_dir = directory + '/b2mn.exe.dir'
            if os.path.exists(b2mn_exe_dir):
                path = b2mn_exe_dir + '/.quit'
                msg = "Graceful stop requested on " + time.ctime()
                with open(path, 'w') as f:
                    f.write(msg + '\n')
                index_status = model.index(index.row(), Column.status,
                                           index.parent())
                model.setData(index_status, msg)
            else:
                QMessageBox.warning(None, "Invalid stop request",
                                    "No b2mn.dir.exe for graceful stop!")
        except OSError:
            QMessageBox.warning(None, "Permission problem",
                                        "Can't create " + path)
    @pyqtSlot()
    def on_pushButton_Run_clicked(self):
        """ Submits the selected Run
        """
        index = self.treeViewRuns.selectionModel().currentIndex()
        model = self.proxyModel
        index_path = model.index(index.row(), Column.path, index.parent())
        rundir = model.data(index_path, Qt.DisplayRole)
        self.submit(rundir)  # TODO check b2fstate_OK before you submit

    @pyqtSlot()
    def on_pushButton_Continue_clicked(self):
        """ Continues the run by firstly copying the the plasma state output
            to input (b2fstate->b2fstati)
        """
        if self.treeViewRuns.selectionModel().currentIndex().isValid():
            index = self.treeViewRuns.selectionModel().currentIndex()
            model = self.proxyModel
            index_path = model.index(index.row(), Column.path, index.parent())
            path = model.data(index_path, Qt.DisplayRole)
            try:
                shutil.copyfile(path + '/b2fstate', path + '/b2fstati')
                self.on_pushButton_Run_clicked()
            except IOError:
                QMessageBox.warning(self, 'Problem copying B2 state file!',
                                    path + '/b2fstati' + " read/write error")


    def find_solps_top(self, directory):
        """ Searches for setup.csh or SOLPSTOP file in the directory hierarchy.
            Arguments:
                run_directory (str): run_directory
            Returns:
                solps_top(str): if found setup.csh or SOLPSTOP file. Else None
        """
        solps_top = directory

        while solps_top:
            path = solps_top + '/setup.csh'
            if os.path.exists(path):
                return solps_top
            path = solps_top + '/SOLPSTOP'
            if os.path.exists(path):
                with open(path) as file:
                    return file.readline()
            solps_top = solps_top.rsplit('/', 1)[0]
        return None

    def execute_tcsh_command_in_rundir(self, tcsh_command, rundir):
        """" Executes TCSH comand in run directory (e.g. submit)

            TCSH environment is searched sourced from 'setup.csh' or pointed
            with SOLPSTOP file. SOLPSTOP is probed for runDir changes and
            if necessary resourced within a new shell. The following
            environment variables are injected for use by scripts::

                setenv SOLPS_GUI_IP <IP address of the SOLPS GUI monitor>
                setenv SOLPS_GUI_PORT <listening port>

            Arguments:
                tcsh_command (str) : command or series of commands separated
                    with newline.
                rundir (str): prepared run directory
        """
        settings = QSettings('ITER', 'solps-gui')
        tcsh_path = settings.value("tcsh_path", '/bin/tcsh')
        solps_gui_ip = settings.value('SOLPS_GUI_IP', '127.0.0.1')
        default_port = 51966 + os.getuid() % 8192
        solps_gui_port = settings.value('SOLPS_GUI_PORT', str(default_port))

        rundir_solps_top = self.find_solps_top(rundir)

        if not rundir_solps_top:
            if not rundir:
                logging.error("Empty TCSH runDir! Bailing out.")
            else:
                logging.error("Could not find SOLPSTOP for " + rundir)
            return

        if rundir_solps_top != self.solps_top:  # we have new SOLPSTOP
            self.main_tcsh.kill()
            self.solps_top = rundir_solps_top

        cmd = ''
        if self.main_tcsh.state() != QProcess.Running:
            self.main_tcsh.setWorkingDirectory(self.solps_top)
            self.main_tcsh.start(tcsh_path, ['-l'])  # TODO settings for -l
            logging.info("MAIN TCSH started in " + self.solps_top)
            cmd +=  'cd ' + self.solps_top \
                    + '\nsource setup.csh\necho TCSH READY\n' \
                    + 'setenv SOLPS_GUI_IP ' + solps_gui_ip + '\n' \
                    + 'setenv SOLPS_GUI_PORT ' + solps_gui_port + '\n'
        cmd += 'cd ' + rundir + '\n'
        cmd += tcsh_command + '\n'
        self.main_tcsh.write(bytearray(cmd, 'utf8'))  # TODO flush stdout


    def submit(self, rundir):
        """ Submits the job in the rundir under its $SOLPSTOP environment

        All ``*.prt`` files are removed befor submission command from
        Preferences is issued.

        Arguments:
             rundir (str): prepared run directory
        """
        settings = QSettings('ITER', 'solps-gui')
        submit_command = settings.value("submit_script", 'localsubmit')

        cmd = ''
        if submit_command:
            opts = ''
            if int(settings.value('use_mpi', '0')):
                opts += ' -m "' + settings.value('MPI_OPTS', '-n 16') + '"'
            if int(settings.value('use_debugger', '0')):
                opts += ' -d "' + settings.value('debugger', 'totalview') + '"'
            if int(settings.value('compress_log', '0')):
                opts += ' -z'
            if int(settings.value('dry_run', '0')):
                opts += ' -n'
            cmd +=  'rm -f *.prt\n' + submit_command + opts
            self.execute_tcsh_command_in_rundir(cmd, rundir)
            msg = 'batch ' + rundir + ' ' + submit_command + opts
            logging.info(msg)
            self.model.jobStatusChanged(msg)
        else:
            msg = 'batch ' + rundir + ' Not submitted!'
            msg += "Empty command or no run directory for MAIN TCSH"
            self.model.jobStatusChanged(msg)
            logging.warning(msg)


    @pyqtSlot()
    def on_pushButton_Import_clicked(self):
        """ Imports the run or a tree of runs from somewhere into
            the selected tree position. If baserun is imported
            then 'correct_baserun_timestamps' is run under it.

            We need to rescan the whole model as user could possibly renamed
            or deleted some directories by right-click in file-manager.
        """
        if self.treeViewRuns.selectionModel().currentIndex().isValid():
            index = self.treeViewRuns.selectionModel().currentIndex()
            model = self.proxyModel
            index_path = model.index(index.row(), Column.path, index.parent())
            destination_dir = model.data(index_path, Qt.DisplayRole)
            selected_dir = QFileDialog.getExistingDirectory(self,
                                                    "Select Directory",
                                                    destination_dir,
                                                   QFileDialog.ShowDirsOnly)
            if selected_dir == '':
                return
            destination_dir += '/' + os.path.basename(selected_dir)
            try:
                shutil.copytree(selected_dir, destination_dir, symlinks=True)
            except IOError as error:
                QMessageBox.warning(self, 'Problem copying selected run tree!',
                                    str(error))
                return


            for directory, subdirs, files in os.walk(destination_dir):
                if os.path.exists(directory + '/baserun'):
                    self.execute_tcsh_command_in_rundir(
                        'correct_baserun_timestamps', directory)
                    logging.info("Imported baserun for " + directory)
                if os.path.exists(directory + '/b2fstati') \
                        and os.path.basename(directory) != 'baserun':
                    self.execute_tcsh_command_in_rundir(
                        'setup_baserun_eirene_links\ntouch b2fstati\n',
                        directory)
                    logging.info("B2 and Eirene links set to baserun for "
                                 + directory)




            self.model.scanFileSystemThread.start()


    @pyqtSlot()
    def on_actionAbout_triggered(self):
        msg = "GUI will enable users to monitor multiple simultaneously " \
              "running cases, which requires defining the working directory " \
              "(folder) for each case to be separated from each other. " \
              "Input file builder will depend on it to correctly save input " \
              "files for multiple parameter scan cases."
        QMessageBox.about(self, 'About SOLPS-ITER GUI', msg)

if __name__ == '__main__':
    "  Main method "
    app = QApplication(sys.argv)
    # app.setStyle("windows")
    main_window = SOLPS_MainWindow()
    main_window.show()
    sys.exit(app.exec_())
