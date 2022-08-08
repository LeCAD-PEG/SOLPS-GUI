from PySide6.QtWidgets import (QToolBar, QFileDialog, QMenu, QDialog,
                             QCheckBox, QVBoxLayout, QHBoxLayout, QPushButton,
                             QSpacerItem, QSizePolicy, QLabel, QComboBox,
                             QDialogButtonBox, QToolButton, QColorDialog)
from PySide6.QtCore import Slot, Qt, QSettings
from PySide6.QtGui import QIcon, QPixmap, QAction
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QAbstractPrintDialog

from QtGnuplot.QtGnuplotWidget import QtGnuplotWidget
from QtGnuplot.mousecmn import GE_keypress


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


class QtGnuplotBar(QToolBar):
    def __init__(self, parent, m_widget: QtGnuplotWidget):
        super(QtGnuplotBar, self).__init__(parent)
        self.m_widget = m_widget
        self.m_ui = QtGnuplotSettingsDialog(self)
        self.setupUi()

    def setGnuplotWidget(self, m_widget: QtGnuplotWidget) -> None:
        self.m_widget = m_widget

    def setupUi(self) -> None:

        copyToClipboardAction = QAction(QIcon(':/images/clipboard'),
                                               'Copy to clipboard', self)
        printAction = QAction(QIcon(':/images/print'), 'Print', self)
        exportAction = QAction(QIcon(':/images/export'), 'Export', self)
        exportPdfAction = QAction(QIcon(':/images/exportPDF'), 'Export to PDF',
                                  self)
        # exportEpsAction = QAction(QIcon(':/images/exportVector'),
        #                           'Export to EPS', self)
        exportSvgAction = QAction(QIcon(':/images/exportVector'),
                                  'Export to SVG', self)
        exportPngAction = QAction(QIcon(':/images/exportRaster'),
                                  'Export to image', self)
        settingsAction = QAction(QIcon(':/images/settings'), 'Settings', self)

        # copyToClipboard.triggered.connect(self.m_widget.copyToClipboard)
        printAction.triggered.connect(self.print)
        exportPdfAction.triggered.connect(self.exportToPdf)
        # exportEpsAction.triggered.connect(self.m_widget.exportToEps)
        exportSvgAction.triggered.connect(self.exportToSvg)
        exportPngAction.triggered.connect(self.exportToImage)
        settingsAction.triggered.connect(self.showSettingsDialog)

        exportMenu = QMenu(self)
        exportMenu.addAction(copyToClipboardAction)
        exportMenu.addAction(printAction)
        exportMenu.addAction(exportPdfAction)
        # exportMenu.addAction(exportEpsAction)
        exportMenu.addAction(exportSvgAction)
        exportMenu.addAction(exportPdfAction)

        self.addAction(exportAction)
        exportWidget = self.widgetForAction(exportAction)
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

        self.addAction(settingsAction)
        self.loadSettings()

    def createAction(self, name: str, key: str, icon: str) -> None:
        action = QAction(QIcon(icon), name, self)
        action.triggered.connect(self.on_keyAction)
        action.setData(key)
        self.addAction(action)

    @Slot()
    def on_keyAction(self) -> None:
        action = self.sender()
        handler = self.m_widget.m_eventHandler
        handler.postTermEvent(GE_keypress, 0, 0, ord(action.data()), 0,
                              self.m_widget)

    def print(self) -> None:
        printer = QPrinter()
        printer.setDocName("gnuplot-qt graph")
        dialog = QPrintDialog(printer, self)
        dialog.setOption(QAbstractPrintDialog.PrintPageRange, False)

        c = dialog.exec()
        if c == QPrintDialog.Accepted:
            self.m_widget.print(printer)

    def exportToPdf(self) -> None:
        fileName, ok = QFileDialog.getSaveFileName(self, "Export to PDF",
                                                   "", "PDF files (*.pdf)")
        if not ok:
            return

        if not fileName.lower().endswith(".pdf"):
            fileName += ".pdf"

        self.m_widget.exportToPdf(fileName)

    def exportToImage(self) -> None:
        fileName, ok = QFileDialog.getSaveFileName(self, "Export to Image",
                                                   "",
                                                   "Image files (*.png *.bmp)")
        if not ok:
            return
        l_filename = fileName.lower()
        if not l_filename.endswith(".png") and not l_filename.endswith(".bml"):
            fileName += ".png"

        self.m_widget.exportToImage(fileName)

    def exportToSvg(self) -> None:
        fileName, ok = QFileDialog.getSaveFileName(self, "Export to Image",
                                                   "", "SVG files (*.svg)")
        if not ok:
            return

        if not fileName.lower().endswith(".svg"):
            fileName += ".svg"

        self.m_widget.exportToSvg(fileName)

    def loadSettings(self) -> None:
        settings = QSettings('gnuplot', 'qtterminal')
        settings.beginGroup('view')
        self.m_widget.loadSettings(settings)
        self.m_statusBarActive = bool(settings.value("statusBarActive", True))

    def saveSettings(self) -> None:
        settings = QSettings('gnuplot', 'qtterminal')
        settings.beginGroup('view')
        self.m_widget.saveSettings(settings)
        settings.setValue('statusBarActive', self.m_statusBarActive)

    def showSettingsDialog(self) -> None:
        self.m_ui.antialiasCheckbox.setCheckState(2 if self.m_widget.antialias() else 0)
        self.m_ui.roundedCheckBox.setCheckState(2 if self.m_widget.rounded() else 0)
        self.m_ui.replotOnResizeCheckBox.setCheckState(2 if self.m_widget.replotOnResize() else 0)

        if self.m_widget.statusLabelActive:
            self.m_ui.mouseLabelComboBox.setCurrentIndex(0)
        else:
            self.m_ui.mouseLabelComboBox.setCurrentIndex(1)

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
            self.m_widget.setStatusLabelActive(statusIndex == 1)
            self.saveSettings()

    @Slot()
    def settingsSelectBackgroundColor(self) -> None:
        self.m_chosenBackgroundColor = QColorDialog.getColor(
            self.m_chosenBackgroundColor, self)

        samplePixmap = QPixmap(self.m_ui.sampleColorLabel.size())
        samplePixmap.fill(self.m_chosenBackgroundColor)
        self.m_ui.sampleColorLabel.setPixmap(samplePixmap)
