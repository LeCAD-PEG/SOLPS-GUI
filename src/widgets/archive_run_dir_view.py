from PyQt5.QtCore import (QSortFilterProxyModel, Qt, QSettings, pyqtSignal,
                          pyqtSlot, QModelIndex)
from PyQt5.QtWidgets import (QTreeView, QStyle, QMessageBox,
                             QStyledItemDelegate, QStyleOptionViewItem)
from PyQt5.QtGui import QPainter

from solps import Column

import logging


class ArchiveSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, archiveDirs, style, parent=None):
        super(ArchiveSortFilterProxyModel, self).__init__(parent)
        self.archiveDirs = archiveDirs
        self.style = style

    def data(self, index, role):
        if role == Qt.DecorationRole:
            if index.column() == Column.name:
                indexDisplay = self.index(index.row(), Column.path,
                                          index.parent())
                path = self.data(indexDisplay, Qt.DisplayRole)
                if path in self.archiveDirs:
                    return self.style.standardIcon(QStyle.SP_DialogOpenButton)
                return None
        return super(ArchiveSortFilterProxyModel, self).data(index, role)

    def hasAcceptedChildren(self, sourceIndex):
        item = sourceIndex.internalPointer()
        items = item.children()
        while items:
            child = items.pop()
            path = child.data(Column.path, Qt.DisplayRole)
            if path in self.archiveDirs:
                return True

            children = child.children()
            if children:
                items += children
        return False

    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, Column.path, sourceParent)
        path = self.sourceModel().data(index, Qt.DisplayRole)
        if path in self.archiveDirs:
            return True
        for dir in self.archiveDirs:
            if path.find(dir) >= 0:
                return True
        return self.hasAcceptedChildren(index)

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

class treeArchiveView(QTreeView):
    archiveDirRemoved = pyqtSignal(str)
    def __init__(self, parent=None, plugin=False):
        super(treeArchiveView, self).__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.leftDelegate = TextElideLeftDelegate(self)
        self.setItemDelegate(self.leftDelegate)
        if plugin:
            # Stop initializing for QDesigner!
            return

        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("TreeViewArchive")
        treeview_archive = settings.value("ColumnWidth")
        if treeview_archive:
            self.header().restoreState(treeview_archive)
        settings.endGroup()

        archiveModel = ArchiveSortFilterProxyModel(self.readArchiveDir(),
                                                        self.style())
        archiveModel.setDynamicSortFilter(True)
        archiveModel.setFilterKeyColumn(Column.path)
        self.setModel(archiveModel)

    def setArchiveSourceModel(self, model):
        """Set the base source model. It is the same as the Runs tree view.
        """
        self.model().setSourceModel(model)

    @pyqtSlot(str)
    def addToArchiveDirs(self, path: str) -> None:
        model = self.model()
        model.archiveDirs.add(path)
        model.invalidateFilter()

    @pyqtSlot()
    def removeFromArchiveDirs(self) -> None:
        index = self.selectionModel().currentIndex()
        model = self.model()
        index_path = model.index(index.row(), Column.path, index.parent())
        path = model.data(index_path, Qt.DisplayRole)

        if path in model.archiveDirs:
            model.archiveDirs.remove(path)
            self.archiveDirRemoved.emit(path)
            model.invalidateFilter()
            self.updateArchiveDirSettings()
        else:
            msg = "Can only remove archived directories marked with icons!"
            QMessageBox.warning(self, 'Invalid action', msg)

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
    from PyQt5.QtWidgets import QApplication
    from run_dir_view import RunsModel
    import sys

    app = QApplication([])

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    archiveView = treeArchiveView()
    sourceModel = RunsModel()
    archiveView.setArchiveSourceModel(sourceModel)

    archiveView.show()


    code = app.exec_()
    sys.exit(code)