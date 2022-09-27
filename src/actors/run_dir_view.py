from PySide6.QtCore import (Qt, QModelIndex, QThread, QSettings, QDateTime,
                          QAbstractItemModel, Signal, Slot, QSize,
                          QRect, QSortFilterProxyModel)
from PySide6.QtWidgets import (QTreeView, QTreeWidgetItem, QStyle, QHeaderView,
                             QStyledItemDelegate, QMessageBox,
                             QStyleOptionViewItem, QAbstractItemView)
from PySide6.QtNetwork import QUdpSocket, QHostAddress, QAbstractSocket
from PySide6.QtGui import QPen, QFontMetrics, QPainter

from solps import Column

from datetime import datetime
import logging
import time
import os
import sys

from typing import Optional

dateFormat = '%d/%m/%Y %I:%m %p'


def exctractValue(line):
    sline = line.split()
    if len(sline) == 1:
        # Maybe it's separated with '='
        sline = line.split('=')
        if len(sline) != 1:
            return sline[-1].strip(" ,'")
        return ''
    else:
        return sline[-1].strip("'")


def timeStamp2Str(timeStamp):
    return datetime.fromtimestamp(timeStamp).strftime(dateFormat)


def readIdentificationParameters(directory):
    """ Reads the identification parameters of the experiment.
    The identification parameters of the experiment are defined inside b2mn.dat
    under the **b2mndr_*id**. In b2md.dat are the switches for the shot and run
    parameters.

    This function scans both files and tries to find these parameters. If they
    are defined inside the b2md.dat or b2mn.dat, these values are then showed
    in the ``run browser`` in SOLPS-GUI.

    Args:
        directory (str): The directory of the experiment input files

    Returns:
        label (str): The string which is labeled as label in b2mn.dat.
        run (str): The string which is labeled as run in b2mn.dat.
        shot (str): The string which is labeled as shot in b2mn.dat.
        user (str): The string which is labeled as user in b2mn.dat
        device (str): The string which is labeled as device in b2mn.dat

    """
    path = os.path.join(directory, 'b2mn.dat')
    label = ''
    run = ''
    shot = ''
    user = ''
    device = ''

    if os.access(path, os.F_OK | os.R_OK):
        with open(path) as file:
            headerLines = file.read(1024).splitlines()
        for i, line in enumerate(headerLines):
            if 'label' in line:
                label = headerLines[i + 1].strip("'")
            elif 'b2mndr_run_number' in line:
                run = exctractValue(line)
            elif 'b2mndr_shot_number' in line:
                shot = exctractValue(line)
            elif 'b2mndr_user' in line:
                user = exctractValue(line)
            elif 'b2mndr_device' in line:
                device = exctractValue(line)
    # logging.info(f'{path}: shot {shot}, run {run}')
    path = os.path.join(directory, 'b2md.dat')

    if (not shot or not run) and os.access(path, os.F_OK | os.R_OK):
        with open(path, 'r') as file:
            for line in file:
                # Remove white spaces
                line = line.strip(' \n')
                if line.startswith('shot='):
                    shot = exctractValue(line)
                elif line.startswith('run='):
                    run = exctractValue(line)

    # logging.info(f'{path}: shot {shot}, run {run}')
    return label, run, shot, user, device


class TreeItem(QTreeWidgetItem):
    def __init__(self, strings=[], parent=None):
        super(TreeItem, self).__init__(parent, strings)

    def children(self):
        return [self.child(i) for i in range(self.childCount())]

    def row(self):
        """Basic concept of QTreeWidget counting.

        To determine the row number of an item, the row is actually the 
        distance of the item from it's parent. The distance is equivalent to 
        the index of the item in the list of the parent's children.

        Additionally, eveything is handled through QModelIndex, which confuses,
        things as they do not posses the absolute position of an item in a 
        tree structure, but it holds a reference to the item in the linked 
        structure and it's row position.

        Hence the calculation of the TreeItem row is actually the index of it
        in it's parent children set.

        For future reference check:
        
        https://doc.qt.io/qt-6/model-view-programming.html#basic-concepts

        """
        # Get the number of level
        row = 0
        parent_item = self.parent()
        if parent_item:
            row = parent_item.indexOfChild(self)
        return row

class TextElideLeftDelegate(QStyledItemDelegate):
    """ Elide text of the first column to the left (... at start).
    This allows long folder names to be shown right aligned when they are too
    long to fit int the column width as usually the folder name changes at the
    end of the Run name (e.g. with sequence or parameter).
    """

    def __init__(self, parent=None):
        super(TextElideLeftDelegate, self).__init__(parent)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem,
              index: QModelIndex):
        # painter.save()
        # if index.column() == Column.name:  # Elide text on the left
        #     painter.setPen(QPen(Qt.black))
        #     text = index.data(Qt.DisplayRole)
        #     icon = index.data(Qt.DecorationRole)
        #     rect_size = QSize(option.rect.width(), option.rect.height())
        #     icon_width = icon.actualSize(rect_size).width() + 4  # spacer too
        #     text_width = option.rect.width() - icon_width
        #     metrics = QFontMetrics(painter.font())
        #     elided_text = metrics.elidedText(text, Qt.ElideLeft,
        #                                      text_width)

        #     if isinstance(text, str):
        #         icon.paint(painter, option.rect, Qt.AlignLeft)
        #         x, y, width, height = option.rect.getCoords()
        #         text_rect = QRect(x + icon_width, y,
        #                           width - icon_width, height)
        #         painter.drawText(text_rect, Qt.AlignLeft, elided_text)
        #         newOption = QStyleOptionViewItem()
        #         newOption.backgroundBrush = option.backgroundBrush
        #         QStyledItemDelegate.paint(self, painter, newOption, index)
        # else:
        #     QStyledItemDelegate.paint(self, painter, option, index)
        # painter.restore()
        if index.column() == Column.name and isinstance(option.text, str):
            option.textElideMode = Qt.ElideLeft
        else:
            option.textElideMode = Qt.ElideRight
        QStyledItemDelegate.paint(self, painter, option, index)


class RetrieveRunsStatus(QThread):
    """Scans the runs directories and retrieves the state of each run.

    Several status and LOG files are probed and searched to get the state
    and other info for Runs table view.

    Args:
    runs_model (RunsModel): Data model that holds run directories

    Attributes:
        status: Emits start/stop notices for status bar.
        currentDir: Current directory that is being processed
        statusChanged: Changed index range for table view update
    """
    progress = Signal(str)
    currentDirectory = Signal(str)

    def __init__(self, model, parent=None):
        super(RetrieveRunsStatus, self).__init__(parent)
        self.model = model

    def readFolderStatus(self, directory):
        """ Scans directory for existance of status and log files.

        .status and run.log are scanned for status and errors.

        Args:
            directory (str): Directory to scan
        Returns:
            time, state (str, str), staticData : Tuple that is at
                least directory time and empty string. Otherwise it returns
                extracted status string and modification time of the file
                that string was retrieved from and other static data from
                various files.
        """
        # Firstly try to extract label from the beginning of b2mn.dat

        # IF there is no SHOT, RUN in b2mn try b2md
        staticData = readIdentificationParameters(directory)
        # logging.info(f"{staticData}")

        # Parse run.log
        path = os.path.join('run.log')

        if os.access(path, os.F_OK | os.R_OK):
            mtime = os.path.getmtime(path)
            mtimeStr = timeStamp2Str(mtime)

            if not os.access(path, os.R_OK):
                return mtimeStr, 'run.log permission denied', staticData

            fsize = os.path.getsize(path)

            with open(path, 'r') as f:
                # Set pos @ last 100 lines
                f.seek(max(fsize - 8192, 0), 0)
                lines = f.read().splitlines()

            for line in lines:
                if any([_ in line for _ in ['stopping because', 'failed',
                                            'ERROR', 'UNABLE']]):
                    return mtimeStr, line, staticData

            b2mn_exe_dir = os.path.join(directory, 'b2mn.exe.dir')
            if os.path.exists(b2mn_exe_dir):
                # Is run.log fresh enough?
                if time.time() - mtime > 60:
                    return mtimeStr, 'CRASHED in b2mn.exe.dir', staticData
                else:
                    return mtimeStr, 'Running', staticData
            logging.warning(f'No status found in {path}')
            return mtimeStr, 'run.log without status', staticData

        # Retrieve last line of .status
        path = os.path.join(directory, '.status')

        if os.path.exists(path):
            mtime = os.path.getmtime(path)
            mtimeStr = timeStamp2Str(mtime)
            if not os.access(path, os.R_OK):
                return timeStamp2Str, '.status permission denied', staticData

            with open(path, 'r') as f:
                lines = f.read().splitlines()

            if lines:
                lastStatus = lines[-1]
                if time.time() - mtime > 60 and 'Started' in lastStatus:
                    return mtimeStr, 'CRASHED?', staticData
                else:
                    return mtimeStr, lastStatus, staticData
            else:
                return mtimeStr, '.status empty', staticData

        # Try to return at least directory date as last status
        if not os.access(directory, os.R_OK):
            return timeStamp2Str(time.time()), 'no access', staticData

        return timeStamp2Str(os.path.getmtime(directory)), '', staticData

    def run(self):
        """ Thread scans each listed directory of the Runs model.

        In principle this operation should be thread safe when changing model
        data. However, one should not restart the scan if this thread is
        not finished yet with scan!
        """

        msg = "Updating runs statuses..."
        logging.info(msg)
        self.progress.emit(msg)

        aliasItems = self.model.rootItem.children()

        childItems = []
        for aliases in aliasItems:
            childItems += aliases.children()
        _c = 0

        while childItems:
            _c += 1
            if self.isInterruptionRequested():
                logging.warning("Status update interrupted")
                break
            item = childItems.pop(0)
            path = item.data(Column.path, Qt.DisplayRole)
            date, status, data = self.readFolderStatus(path)
            item.setData(Column.date, Qt.DisplayRole, date)
            item.setData(Column.status, Qt.DisplayRole, status)
            item.setData(Column.label, Qt.DisplayRole, data[0])
            item.setData(Column.run, Qt.DisplayRole, data[1])
            item.setData(Column.shot, Qt.DisplayRole, data[2])
            item.setData(Column.user, Qt.DisplayRole, data[3])
            item.setData(Column.device, Qt.DisplayRole, data[4])

            children = item.children()
            if children:
                childItems += children

        msg = f"Updating run status finished. {_c} directories scanned."
        logging.info(msg)
        self.progress.emit(msg)


class DirectoryScan(QThread):
    """Creates initial list of directory tree hierarchy of all aliased Runs.

    This is quick scan for of all directories to be quickly shown in the
    tree view and shortly after updated with longer run in separate thread
    with `RetrieveRunsFolderInfo` operation. Nevertheless, this is done in
    a thread to give immediate response (GUI) to the user after its start.
    Tree view is shown empty until this scan finished and model is reset.
    """

    status = Signal(str)

    def __init__(self, parentModel, parent=None):
        super(DirectoryScan, self).__init__(parent)
        self.model = parentModel

    def setupModelData(self, rootDir, alias, parent):
        if rootDir == '':
            return
        self.status.emit(f'Scanning {alias}...')

        indentations = [len(rootDir.split(os.sep))]
        parents = [parent]
        for dir, subdirs, files in os.walk(rootDir):
            if dir == rootDir:
                mtime = os.stat(dir).st_mtime
                date = timeStamp2Str(mtime)
                data = [alias, dir, date, *[''] * 7]
                treeItem = TreeItem(data, parent)
                parents[0].addChild(treeItem)
                self.model.path2item[dir] = treeItem
                continue
            position = len(dir.split(os.sep))
            if position > indentations[-1]:
                if parents[-1].childCount() > 0:
                    # So basically to the parent list append the previous 
                    # 1 level higher directory.
                    parents.append(
                        parents[-1].child(parents[-1].childCount() - 1))
                    indentations.append(position)
            else:
                while position < indentations[-1] and len(parents) > 0:
                    parents.pop()
                    indentations.pop()

            date = timeStamp2Str(os.path.getmtime(dir))
            data = [os.path.basename(dir), dir, date, *[''] * 7]
            treeItem = TreeItem(data, parents[-1])
            self.model.path2item[dir] = treeItem
            parents[-1].addChild(treeItem)

        self.model.rootItem = parent

    def run(self):
        msg = "Directory scanning started..."
        self.status.emit(msg)
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("RunDirectories")
        rundirs = []
        aliases = []
        for i in range(1, 6):
            rundirs.append(settings.value(f'runDir{i}', ''))
            aliases.append(settings.value(f'Alias{i}', f'local_{i}'))
        settings.endGroup()
        # self.model.rootItem = TreeItem(Column.headerData)
        rootItem = TreeItem(Column.headerData)
        [self.setupModelData(rundirs[i], aliases[i], rootItem) for
            i in range(5) if rundirs[i] != '']
        msg = "Filesystem scanning finished."
        logging.info(msg)
        self.status.emit(msg)

"""
class RunsStatusServer(QThread):
    Networking UDP listener for receiving job status updates.

    Receives datagrams in single line and emits decoded one line updates sent
    by each job to notify the GUI that status changed.

    Attributes:
        retrieve (Bool) : Gracefully stop the thread on next packet.

    retrieve = True
    jobStatusChanged = Signal(str)
    address = None
    port = None

    def bind(self, address, port):
        # connect to UDP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind socket to local host and port
        try:
            self._sock.bind((address, port))
            self.address = address
            self.port = port
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
            msg = data.decode('utf-8').rstrip('\n')
            if msg[0:4] == 'STOP':
                break
            self.jobStatusChanged.emit(msg)
            # TODO Graceful exit from blocking recvfrom() by setting retrieve
            # TODO and sending UDP packet to ourselves.
        logging.info("RunsStatusServer run() finished.")
        self._sock.close()

    def stop(self):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_sock.sendto(bytes('STOP', 'utf-8'), (self.address, self.port))
        client_sock.close()
        self.wait()
        self.exit(0)
        logging.info("RunsStatusServer stopped.")
"""
class RunsStatusServer(QUdpSocket):
    """ Networking UDP listener for receiving job status updates.

    Receives datagrams in single line and emits decoded one line updates sent
    by each job to notify the GUI that status changed.

    Attributes:
        retrieve (Bool) : Gracefully stop the thread on next packet.
    """

    retrieve = True
    jobStatusChanged = Signal(str)
    address = None
    port = None

    def __init__(self, parent=None):
        super(RunsStatusServer, self).__init__(parent)
        self.readyRead.connect(self.readPendingDatagrams)

    @Slot()
    def readPendingDatagrams(self):
        logging.info(f'RunsStatusServer reading data.')
        while self.hasPendingDatagrams():
            datagram = self.receiveDatagram()
            data = str(datagram.data(), "utf-8")
            logging.debug(f'Received datagram: {data}')
            self.jobStatusChanged.emit(data)

    def stop(self) -> None:
        if self.state() == QUdpSocket.BindMode:
            self.writeData(b"STOP")
            self.close()
            # self.waitForDisconnected()
            logging.info("RunsStatusServer stopped.")


class RunsModel(QAbstractItemModel):
    # statusServerThread = None
    # scanDirectoriesThread: Optional[DirectoryScan] = None
    columnIndex = {}

    def __init__(self, style=None, parent=None):
        super(RunsModel, self).__init__(parent)
        self.style = style
        # Root widget item, basically the header
        self.rootItem = TreeItem(Column.headerData)
        # Path to widget item, using directory as hash and widget item as the
        # value.
        self.path2item = {}

        self.scanDirectoriesThread = DirectoryScan(self)
        self.scanDirectoriesThread.finished.connect(self.modelReset.emit)
        # self.modelReset.connect(self.scanDirectoriesThread.start)
        self.scanDirectoriesThread.start()

        self.retRunsFolderInfoThread = RetrieveRunsStatus(self)
        self.scanDirectoriesThread.finished.connect(
            self.retRunsFolderInfoThread.start)
        self.retRunsFolderInfoThread.finished.connect(self.endResetModel)

        self.startRunsStatusServer()

    def startThreads(self):
        self.beginResetModel()
        self.scanDirectoriesThread.start()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section, role)
        if role == Qt.TextAlignmentRole:
            return Qt.AlignHCenter
        return super(RunsModel, self).headerData(section, orientation, role)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def rowCount(self, index: QModelIndex):
        """Return the number of children for a given item.
        """
        if index.column() > 0:
            # Do not return the row number when selected index has a column
            # value higher than 0.
            return 0
        if not index.isValid():
            parentItem = self.rootItem
        else:
            parentItem = index.internalPointer()
        item_row = parentItem.childCount()
        return item_row
    def getItem(self, index: QModelIndex) -> TreeItem:
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def index(self, row: int, column: int, parentIndex: QModelIndex):
        if not self.hasIndex(row, column, parentIndex):
            return QModelIndex()

        if not parentIndex.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parentIndex.internalPointer()

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

        return item.data(index.column(), role)

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def setData(self, index: QModelIndex, value: str,
                role: int = Qt.EditRole) -> bool:
        """This is the overloaded function for QAbstractItemModel. When the
        user change certain columns in the RunsTreeView, these parameters will
        be saved to the b2mn.dat file, if able, in the form of identification
        switches.

        Otherwise, if some columns were to be changed, i.e. the part to the
        run directories etc... the changes will be rejected.
        """
        logging.debug('SetData called')
        row = index.row()

        # Accept only edits and display changes
        logging.debug(role != Qt.EditRole and role != Qt.DisplayRole)
        if role != Qt.EditRole and role != Qt.DisplayRole:
            return False

        column = index.column()
        logging.debug(f"setData row: {row} column: {column} value: {value}")

        # Disallow changing date by hand
        if role == Qt.EditRole and column == Column.date:
            return False

        # if column == Column.path or column == Column.date:
        if column == Column.path:
            return False

        # disallow changing 'name' except for aliased names (not saved)
        if column == Column.name and self.parent(index) != QModelIndex():
            return False

        item = self.getItem(index)
        # The QTreeWidgetItem setData is void by default.
        item.setData(column, role, value)
        # DATA changed does NOT help. I.e., to actually refresh view
        # a repaint has to be called or moving the mouse... But still
        # it has to be called so maybe that the QSortFilterProxy model
        # does it magic.
        self.dataChanged.emit(index, index)

        if column == Column.run:
            switch_name = 'b2mndr_run_number'
        elif column == Column.shot:
            switch_name = 'b2mndr_shot_number'
        elif column == Column.user:
            switch_name = 'b2mndr_user'
        elif column == Column.device:
            switch_name = 'b2mndr_device'
        elif column == Column.label:
            switch_name = 'label'
        else:
            switch_name = ''

        # LABEL to b2mn, USER, SHOT, RUN to b2md

        if value and switch_name:
            directory = item.data(Column.path, Qt.DisplayRole)
            path = os.path.join(directory, 'b2mn.dat')
            try:
                with open(path) as file:
                    lines = file.read()  # whole file
                if switch_name in lines:
                    lines = lines.split('\n')
                    for i, line in enumerate(lines):
                        if switch_name in line:
                            if column == Column.label:
                                lines[i + 1] = " '" + value + "'"
                            else:
                                value_to_replace =\
                                    lines[i].split()[-1].strip("'")
                                lines[i] = \
                                lines[i].replace(value_to_replace, value)
                            with open(path, 'w') as f:
                                f.write('\n'.join(lines))
                                logging.debug(f'Written to {path}')
                            break
                else:
                    lines = lines.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith('*endphy'):
                            new_line = f"'{switch_name}'     {value}"
                            lines.insert(i + 1, new_line)
                            with open(path, 'w') as f:
                                f.write('\n'.join(lines))
                                logging.debug(f'Written to {path}')

            except OSError:
                QMessageBox.warning(None, "Permission problem",
                                    "Can't update " + path)
        return True

    def startRunsStatusServer(self) -> None:
        self.statusServerThread = RunsStatusServer(self)
        settings = QSettings("ITER", "solps-gui")
        defaultPort = 0xCAFE + os.getuid() % 13566
        address = settings.value("SOLPS_GUI_BIND", "0.0.0.0")
        port = int(settings.value("SOLPS_GUI_PORT", defaultPort))

        settings.setValue("SOLPS_GUI_BIND", address)
        settings.setValue("SOLPS_GUI_PORT", port)
        address = QHostAddress(address)
        if address.isNull():
            ok = False
        else:
            ok = self.statusServerThread.bind(address, port)
        # self.statusServerThread.connectToHost(QHostAddress(address), port)
        if not ok:
            msg = f'Failed to bind interface {address.toString()}'
            msg += f' to port {port}. '
            msg += 'Job monitoring will not start unless you setup a free'
            msg += ' port and restart! GUI will exit if you press Cancel.'
            ret = QMessageBox.warning(None, 'SOLPS-GUI Status server', msg,
                                      QMessageBox.Cancel | QMessageBox.Ok)
            if ret == QMessageBox.Cancel:
                sys.exit(1)
        self.statusServerThread.jobStatusChanged.connect(self.jobStatusChanged)

    @Slot(str)
    def jobStatusChanged(self, message: str) -> None:
        """
        Change the status column fields of the row, whose run was submitted.

        Args:
            index (QModelIndex): Row with the submitted run.
            message (str): Message containing information of the run.
        """

        try:
            name, path, status = message.split(maxsplit=2)
            status = status.rstrip() # Remove the newline.
            try:
                # dateIndex = self.index(index.row(), Column.date, QModelIndex())
                item = self.path2item[path]
                item_row = item.row()
                dateIndex = self.createIndex(item_row, Column.date, item)
                statusIndex = self.createIndex(item_row, Column.status, item)
                # Sets the data. Sadly it does not trigger a repaint.
                self.setData(dateIndex, timeStamp2Str(time.time()),
                             Qt.DisplayRole)
                self.setData(statusIndex, status, Qt.DisplayRole)

            except KeyError:  # TODO insert non monitored message anyway
                msg = name + ':' + path + " not monitored "
                msg += 'Skipping "' + status + '" update.'
                logging.warning(msg)
            except ValueError:
                pass
                # assert(len(self.column_index[path]) == 4)  # indexing changed
        except ValueError as e:
            logging.error(str(e) + " Received essage: '" + message +
                          "' should be in 'name path status' format.")


class RunsSortFilterProxyModel(QSortFilterProxyModel):
    # archiveDirSet is a signal for archive Proxy model
    def __init__(self, archiveDirs, parent=None):
        super(RunsSortFilterProxyModel, self).__init__(parent)
        self.archiveDirs = archiveDirs

    # Parent of accepted children needs to be accepted too for treeviews.
    def hasAcceptedChildren(self, sourceIndex):
        item = sourceIndex.internalPointer()
        items = item.children()
        while items:
            child = items.pop()

            path = child.data(Column.path, Qt.DisplayRole)
            match = self.filterRegularExpression().match(path)
            if match.hasMatch() and path not in self.archiveDirs:
                return True

            children = child.children()
            if children:
                items += children
        return False


    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, Column.path, sourceParent)
        path = self.sourceModel().data(index, Qt.DisplayRole)
        if path in self.archiveDirs:
            return False
        match = self.filterRegularExpression().match(path)
        if match.hasMatch():
            # Row with string returns true
            return True
        # Row with child that has the string in itself ralso returns true,
        flag = self.hasAcceptedChildren(index)
        return flag


class RunDirView(QTreeView):
    archiveDirSet = Signal(str)

    def __init__(self, parent=None, plugin=False):
        super(RunDirView, self).__init__(parent)
        # self.header().setStretchLastSection(False)
        # self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.leftDelegate = TextElideLeftDelegate(self)
        self.setItemDelegate(self.leftDelegate)
        if plugin:
            # Stop initializing for QDesigner!
            return

        # Get settings
        settings = QSettings("ITER", "solps-gui")

        settings.beginGroup("TreeViewRuns")
        treeViewColumnWidget = settings.value("ColumnWidgh")
        if treeViewColumnWidget:
            self.header().restoreState(treeViewColumnWidget)
        expandedPaths = settings.value("ExpandedPaths")
        settings.endGroup()

        # Default model
        self._model = RunsModel(self.style())
        self._model.retRunsFolderInfoThread.finished.connect(self.update)

        # if True: # use filter if True
        proxyModel = RunsSortFilterProxyModel(self.readArchiveDir())
        proxyModel.setDynamicSortFilter(True)
        proxyModel.setFilterKeyColumn(Column.path)
        proxyModel.setSourceModel(self._model)

        self.setModel(proxyModel)
        # else:
            # self.setModel(self.model)

        self.setRootIsDecorated(True)
        self.setSortingEnabled(True)

    @Slot()
    def addToArchiveDirs(self) -> None:
        index = self.selectionModel().currentIndex()
        model = self.model()
        index_path = model.index(index.row(), Column.path, index.parent())
        path = model.data(index_path, Qt.DisplayRole)

        model.archiveDirs.add(path)
        self.archiveDirSet.emit(path)
        model.invalidateFilter()

        self.updateArchiveDirSettings()

    @Slot(str)
    def removeFromArchiveDirs(self, path: str) -> None:
        model = self.model()
        if path in model.archiveDirs:
            model.archiveDirs.remove(path)

            # Invalidate filter does not refresh the current view by itself.
            model.invalidateFilter()

            # The following collapses everything...
            # model.beginResetModel()
            # model.endResetModel()

            # This then actually forces the view to be updated...
            model.layoutAboutToBeChanged.emit()
            model.layoutChanged.emit()

    def updateArchiveDirSettings(self) -> None:
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("Archive")
        settings.beginWriteArray("dirs")
        for i, directory in enumerate(self.model().archiveDirs):
            settings.setArrayIndex(i)
            settings.setValue("dir", directory)
        settings.endArray()
        settings.endGroup()

    def readArchiveDir(self) -> set:
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("Archive")
        size = settings.beginReadArray("dirs")
        archiveDirs = set()
        for i in range(size):
            settings.setArrayIndex(i)
            dir = settings.value("dir")
            archiveDirs.add(dir)
        settings.endArray()
        settings.endGroup()
        return archiveDirs

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    app = QApplication(sys.argv)

    view = RunDirView()

    view.show()
    code = app.exec()
    import resource
    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    sys.exit(code)
