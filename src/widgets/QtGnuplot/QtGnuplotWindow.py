from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QMenu, QAction,
                             QToolButton, QApplication, QDialog, QVBoxLayout,
                             QHBoxLayout, QPushButton, QSpacerItem,
                             QSizePolicy, QCheckBox, QComboBox,
                             QDialogButtonBox, QColorDialog, QFileDialog)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QAbstractPrintDialog
from PyQt5.QtCore import (QDataStream, pyqtSlot, QCoreApplication, QPoint, Qt,
                          QSettings)
from PyQt5.QtGui import QKeyEvent, QCloseEvent, QIcon, QPixmap

from QtGnuplot.QtGnuplotEvent import (QtGnuplotEventReceiver,
                                      QtGnuplotEventHandler)
from QtGnuplot import QtGnuplotWidget
from QtGnuplot.QtGnuplotEvent import (GETitle, GERaise, GESetCtrl, GEPID,
                                      GESetPosition)
from QtGnuplot.mousecmn import GE_keypress, GE_reset


class QtGnuplotSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(QtGnuplotSettingsDialog, self).__init__(parent)
        icon = QIcon()
        icon.addPixmap(QPixmap(':/images/settings'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        verticalLayout = QVBoxLayout(self)
        verticalLayout_1 = QVBoxLayout()
        horizontalLayout_1 = QHBoxLayout()
        self.backgroundButton = QPushButton(self)
        self.backgroundButton.setText("Select background color")
        horizontalLayout_1.addWidget(self.backgroundButton)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding,
                                 QSizePolicy.Minimum)
        horizontalLayout_1.addItem(spacerItem)

        self.sampleColorLabel = QLabel(self)
        self.sampleColorLabel.setText('Sample')
        horizontalLayout_1.addWidget(self.sampleColorLabel)

        verticalLayout_1.addLayout(horizontalLayout_1)

        self.antialiasCheckbox = QCheckBox(self)
        self.antialiasCheckbox.setText('Antialias')
        verticalLayout_1.addWidget(self.antialiasCheckbox)
        self.replotOnResizeCheckBox = QCheckBox(self)
        self.replotOnResizeCheckBox.setText('Replot on resize')
        verticalLayout_1.addWidget(self.replotOnResizeCheckBox)
        self.roundedCheckBox = QCheckBox(self)
        self.roundedCheckBox.setText("Rounded line ends")
        verticalLayout_1.addWidget(self.roundedCheckBox)

        horizontalLayout_2 = QHBoxLayout()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignTrailing |
                                Qt.AlignVCenter)
        self.label.setText("Mouse label")
        horizontalLayout_2.addWidget(self.label)

        self.mouseLabelComboBox = QComboBox(self)
        self.mouseLabelComboBox.addItem("Status bar")
        self.mouseLabelComboBox.addItem("Tool bar")
        self.mouseLabelComboBox.addItem("Above plot")
        self.mouseLabelComboBox.addItem("None")

        horizontalLayout_2.addWidget(self.mouseLabelComboBox)

        verticalLayout_1.addLayout(horizontalLayout_2)

        verticalLayout.addLayout(verticalLayout_1)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel |
                                          QDialogButtonBox.Ok)

        verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)



class QtGnuplotWindow(QMainWindow, QtGnuplotEventReceiver):
    def __init__(self, id_: int, eventHandler: QtGnuplotEventHandler = 0,
                 parent: QWidget = None):
        QMainWindow.__init__(self)
        self.m_ctrl = False
        self.m_eventHandler = eventHandler
        self.m_id = id_
        self.m_pid = 0

        self.setWindowIcon(QIcon(":/images/gnuplot"))

        if self.m_eventHandler == 0:
            appId = f"gnuplot{QCoreApplication.applicationPid()}"
            self.m_eventHandler = QtGnuplotEventHandler(self, appId)

        self.m_widget = QtGnuplotWidget(self.m_id, self.m_eventHandler, self)
        self.m_widget.statusTextChanged.connect(self.on_setStatusText)
        self.setCentralWidget(self.m_widget)

        self.m_toolBar = self.addToolBar("Main tool bar")

        self.m_mouseToolBar = self.addToolBar("Mouse tool bar")
        self.m_mouseToolBarLabel = QLabel()
        self.m_mouseToolBar.addWidget(self.m_mouseToolBarLabel)

        self.m_statusBar = self.statusBar()

        copyToClipboardAction = QAction(QIcon(':/images/clipboard'),
                                        'Copy to clipboard', self)
        printAction = QAction(QIcon(':/images/print'), 'Print', self)
        exportAction = QAction(QIcon(':/images/export'), 'Export', self)
        exportPdfAction = QAction(QIcon(':/images/exportPDF'), 'Export to PDF',
                                  self)
        exportEpsAction = QAction(QIcon(':/images/exportVector'),
                                  'Export to EPS', self)
        exportSvgAction = QAction(QIcon(':/images/exportVector'),
                                  'Export to SVG', self)
        exportPngAction = QAction(QIcon(':/images/exportRaster'),
                                  'Export to image', self)
        settingsAction = QAction(QIcon(':/images/settings'), 'Settings', self)

        copyToClipboardAction.triggered.connect(self.m_widget.copyToClipboard)
        printAction.triggered.connect(self.print)
        exportPdfAction.triggered.connect(self.exportToPdf)
        exportEpsAction.triggered.connect(self.m_widget.exportToEps)
        exportSvgAction.triggered.connect(self.exportToSvg)
        exportPngAction.triggered.connect(self.exportToImage)
        settingsAction.triggered.connect(self.showSettingsDialog)

        exportMenu = QMenu(self)
        exportMenu.addAction(copyToClipboardAction)
        exportMenu.addAction(printAction)
        exportMenu.addAction(exportPdfAction)
        # exportMenu.addAction(exportEpsAction)
        exportMenu.addAction(exportSvgAction)
        exportMenu.addAction(exportPngAction)

        # exportAction.setMenu(exportMenu)
        self.m_toolBar.addAction(exportAction)

        exportWidget = self.m_toolBar.widgetForAction(exportAction)
        exportButton = QToolButton(exportWidget)
        if exportButton:
            exportButton.setMenu(exportMenu)
            exportAction.triggered.connect(exportButton.showMenu)
            exportButton.setVisible(False)
        self.createAction('Replot', 'e', ':/images/replot')
        self.createAction('Show grid', 'g', ':/images/grid')
        self.createAction('Previous zoom', 'p', ':/images/zoomPrevious')
        self.createAction('Next zoom', 'n', ':/images/zoomNext')
        self.createAction('Autoscale', 'a', ':/images/autoscale')
        self.m_toolBar.addAction(settingsAction)

        self.m_ui = QtGnuplotSettingsDialog(self)

        self.loadSettings()

    def createAction(self, name: str, key: str, icon: str) -> None:
        action = QAction(QIcon(icon), name, self)
        action.triggered.connect(self.on_keyAction)
        action.setData(key)
        self.m_toolBar.addAction(action)

    @pyqtSlot(str)
    def on_setStatusText(self, status: str) -> None:
        if self.m_mouseToolBar.toggleViewAction().isChecked():
            self.m_mouseToolBarLabel.setText(status)
        if self.m_statusBar.isVisible():
            self.m_statusBar.showMessage(status)

    @pyqtSlot()
    def on_keyAction(self) -> None:
        action = self.sender()
        self.m_eventHandler.postTermEvent(GE_keypress, 0, 0,
                                          ord(action.data()), 0, self.m_widget)

    def print(self) -> None:
        printer = QPrinter()
        printer.setDocName('gnuplot-qt graph')
        dialog = QPrintDialog(printer, self)
        dialog.setOption(QAbstractPrintDialog.PrintPageRange, False)

        c = dialog.exec()
        if c == QPrintDialog.Accepted:
            self.m_widget.print(printer)

    def exportToPdf(self) -> None:
        fileName, ok = QFileDialog.getSaveFileName(self, 'Export to PDF',
                                                   '', 'PDF files (*.pdf)')
        if not ok:
            return

        if not fileName.lower().endswith('.pdf'):
            fileName += '.pdf'

        self.m_widget.exportToPdf(fileName)

    def exportToImage(self) -> None:
        fileName, ok = QFileDialog.getSaveFileName(self, 'Export to Image',
                                                   '',
                                                   'Image files (*.png *.bmp)')
        if not ok:
            return
        l_filename = fileName.lower()
        if not l_filename.endswith('.png') and not l_filename.endswith('.bml'):
            fileName += '.png'

        self.m_widget.exportToImage(fileName)

    def exportToSvg(self) -> None:
        fileName, ok = QFileDialog.getSaveFileName(self, 'Export to Image',
                                                   '', 'SVG files (*.svg)')
        if not ok:
            return

        if not fileName.lower().endswith('.svg'):
            fileName += '.svg'

        self.m_widget.exportToSvg(fileName)

    def loadSettings(self) -> None:
        settings = QSettings('gnuplot', 'qtterminal')
        settings.beginGroup('view')
        self.m_widget.loadSettings(settings)
        self.m_statusBarActive = bool(settings.value("statusBarActive", True))
        self.m_statusBar.setVisible(self.m_statusBarActive)
        mouseToolBarActive = bool(settings.value('mouseToolBarActive', False))
        self.m_mouseToolBar.toggleViewAction().setChecked(mouseToolBarActive)
        self.m_mouseToolBar.setVisible(mouseToolBarActive)

    def saveSettings(self) -> None:
        settings = QSettings('gnuplot', 'qtterminal')
        settings.beginGroup('view')
        self.m_widget.saveSettings(settings)
        settings.setValue('statusBarActive', self.m_statusBarActive)
        settings.setValue('mouseToolBarActive',
                          self.m_mouseToolBar.toggleViewAction().isChecked())

    def showSettingsDialog(self) -> None:
        self.m_ui.antialiasCheckbox.setCheckState(2 if
                                                  self.m_widget.antialias()
                                                  else 0)
        self.m_ui.roundedCheckBox.setCheckState(2 if self.m_widget.rounded()
                                                else 0)
        self.m_ui.replotOnResizeCheckBox.setCheckState(2 if
                                                self.m_widget.replotOnResize()
                                                else 0)

        if self.m_statusBar.isVisible():
            self.m_ui.mouseLabelComboBox.setCurrentIndex(0)
        elif self.m_mouseToolBar.toggleViewAction().isChecked():
            self.m_ui.mouseLabelComboBox.setCurrentIndex(1)
        elif self.m_widget.statusLabelActive:
            self.m_ui.mouseLabelComboBox.setCurrentIndex(2)
        else:
            self.m_ui.mouseLabelComboBox.setCurrentIndex(3)

        samplePixmap = QPixmap(self.m_ui.sampleColorLabel.size())
        samplePixmap.fill(self.m_widget.backgroundColor())
        self.m_ui.sampleColorLabel.setPixmap(samplePixmap)
        self.m_chosenBackgroundColor = self.m_widget.backgroundColor()
        self.m_ui.backgroundButton.clicked.connect(
            self.settingsSelectBackgroundColor)
        self.m_ui.exec_()

        if self.m_ui.result() == QDialog.Accepted:
            self.m_widget.setBackgroundColor(self.m_chosenBackgroundColor)
            self.m_widget.setAntialias(bool(self.m_ui.antialiasCheckbox.isChecked()))
            self.m_widget.setRounded(bool(self.m_ui.roundedCheckBox.isChecked()))
            self.m_widget.setReplotOnResize(
                bool(self.m_ui.replotOnResizeCheckBox.isChecked()))

            statusIndex = self.m_ui.mouseLabelComboBox.currentIndex()
            self.m_statusBarActive = statusIndex == 0
            self.m_statusBar.setVisible(self.m_statusBarActive)
            self.m_mouseToolBar.toggleViewAction().setChecked(statusIndex == 1)
            self.m_mouseToolBar.setVisible(statusIndex == 1)
            self.m_widget.setStatusLabelActive(statusIndex == 2)
            self.saveSettings()

    @pyqtSlot()
    def settingsSelectBackgroundColor(self) -> None:
        self.m_chosenBackgroundColor = QColorDialog.getColor(
            self.m_chosenBackgroundColor, self)

        samplePixmap = QPixmap(self.m_ui.sampleColorLabel.size())
        samplePixmap.fill(self.m_chosenBackgroundColor)
        self.m_ui.sampleColorLabel.setPixmap(samplePixmap)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.m_eventHandler.postTermEvent(GE_reset, 0, 0, 0, 0, self.m_widget)
        event.accept()

    def processEvent(self, type: int, dataStream: QDataStream) ->None:
        if type == GETitle:
            title = dataStream.readQString()
            if not title:
                title = f"Gnuplot window {self.m_id}"
            self.setWindowTitle(title)
        elif type == GERaise:
            if self.isMinimized():
                self.showNormal()
            self.raise_()
        elif type == GESetCtrl:
            self.m_ctrl = dataStream.readBool()
        elif type == GESetPosition:
            pos = QPoint()
            dataStream >> pos
            self.move(pos)
        elif type == GEPID:
            self.m_pid = dataStream.readUInt32()
        else:
            self.m_widget.processEvent(type, dataStream)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        modifiers = QApplication.keyboardModifiers() & Qt.ControlModifier
        if event.key() == 'Q' and (not self.m_ctrl or modifiers):
            self.close()

        # Something about windows keys_space for GE_raise.

        QMainWindow.keyPressEvent(self, event)
