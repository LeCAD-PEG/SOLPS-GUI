from PyQt5.QtWidgets import (QWidget, QGraphicsView, QVBoxLayout, QApplication,
                             QLabel)
from PyQt5.QtCore import (QSize, pyqtSignal, pyqtSlot, pyqtProperty, QSettings,
                          Qt, QCoreApplication, QPoint, QRect, QDataStream,
                          QSizeF)
from PyQt5.QtGui import QPainter, QColor, QResizeEvent, QPixmap, QCursor
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtSvg import QSvgGenerator

from QtGnuplot.QtGnuplotEvent import (QtGnuplotEventHandler,
                                      QtGnuplotEventReceiver, GEDone,
                                      GESetWidgetSize, GEStatusText,
                                      GECopyClipboard, GECursor,
                                      GEWrapCursor, GEActivate, GEDesactivate)
from QtGnuplot.QtGnuplotScene import QtGnuplotScene
import logging

GE_fontprops = 11
GE_replot = 9


class QtGnuplotWidget(QWidget, QtGnuplotEventReceiver):
    plotDone = pyqtSignal()
    statusTextChanged = pyqtSignal(str)

    m_widgetUid = 1

    def __init__(self, id: int = 0,
                 eventHandler: QtGnuplotEventHandler = 0, parent=None):

        QWidget.__init__(self, parent=parent)
        self.m_id = id
        self.m_eventHandler = eventHandler

        self.m_active = False
        self.m_lastSizeRequest = QSize(-1, -1)
        self._m_rounded = True
        self._m_backgroundColor = Qt.white
        self._m_antialias = True
        self._m_replotOnResize = True
        self._m_statusLabelActive = False
        self.m_skipResize = False

        if eventHandler == 0:
            self.m_eventHandler = QtGnuplotEventHandler(self,
                f"qtgnuplot{QCoreApplication.applicationPid()}-"
                f"{self.m_widgetUid}")
            QtGnuplotWidget.m_widgetUid += 1

        self.m_scene = QtGnuplotScene(self)
        self.m_view = QGraphicsView(self.m_scene)
        self.m_scene.resetItems()
        self.m_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.m_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.m_view)
        self.setLayout(layout)
        self.setViewMatrix()

        self.m_statusLabel = QLabel(self.m_view.viewport())
        self.m_statusLabel.setStyleSheet("QLabel { background-color :  rgba(230, 212, 166, 150) }")
        self.m_statusLabel.setMargin(1)
        self.m_statusLabel.setVisible(False)
        self.m_sizeHint = QSize(600, 400)

        # self.tmp_painter = None  # Store painter device
        # self.tmp_printer = None

    def antialias(self) -> bool:
        return self._m_antialias

    def setAntialias(self, value: bool) -> None:
        self._m_antialias = value
        self.m_view.setRenderHints(self.renderHints())

    m_antialias = pyqtProperty(bool, antialias, setAntialias)

    def rounded(self) -> bool:
        return self._m_rounded

    def setRounded(self, value: bool) -> None:
        self._m_rounded = value

    m_rounded = pyqtProperty(bool, rounded, setRounded)

    def replotOnResize(self) -> bool:
        return self._m_replotOnResize

    def setReplotOnResize(self, value: bool) -> None:
        self._m_replotOnResize = value

    m_replotOnResize = pyqtProperty(bool, replotOnResize, setReplotOnResize)

    def backgroundColor(self) -> QColor:
        return self._m_backgroundColor

    def setBackgroundColor(self, color: QColor) -> None:
        self._m_backgroundColor = color
        self.m_view.setBackgroundBrush(self._m_backgroundColor)

    m_backgroundColor = pyqtProperty(QColor, backgroundColor, setBackgroundColor)

    def statusLabelActive(self) -> bool:
        return self._m_statusLabelActive

    def setStatusLabelActive(self, value: bool) -> None:
        self._m_statusLabelActive = value
        if not value:
            self.m_statusLabel.setVisible(False)

    m_statusLabelActive = pyqtProperty(bool, statusLabelActive, setStatusLabelActive)

    def isActive(self) -> bool:
        return self.m_active

    def setStatusText(self, status: str) -> None:
        if isinstance(status, bytes):
            status = status.decode()
        if self.m_statusLabelActive:
            self.m_statusLabel.setText(status)
            self.m_statusLabel.adjustSize()
            self.m_statusLabel.move(self.m_view.viewport().width() -
                                    self.m_statusLabel.width(), 0)
            self.m_statusLabel.setVisible(True)
        self.statusTextChanged.emit(status)

    def plotAreaSize(self) -> QSize:
        return self.m_view.viewport().size()

    def sizeHint(self) -> QSize:
        return self.m_sizeHint

    def processEvent(self, type: int, dataStream: QDataStream) -> None:
        # logging.debug(f"GnuplotWidget processEvent type {type}")
        if type == GEDone:
            self.plotDone.emit()
            self.m_scene.processEvent(type, dataStream)
            return

        if type == GESetWidgetSize:

            # Qt has no reliable mechanism to set the size of widget while
            # having it resizable. So we heuristically use the resize function
            # to set the size of the plotting area when the plot window is
            # already displayed. When the window is not yet displayed, this
            # does not work because the window messes up with its content sizes
            # before showing up. In this case, we use the sizeHint mechanism
            # to tell the window which size we  prefer for the plotting area.
            # On MacOS, it looks like QMainWindow forgets the status bar area
            # when it layouts its contents. This makes the plot area 14 pixels
            # too small in the vertical direction when the plot window is first
            # displayed.

            s = QSize()
            dataStream >> s
            self.m_lastSizeRequest = s
            # self.m_view.resetTransform()  # resetMatrix()
            # self.m_view.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.m_view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            viewport = self.m_view.viewport()

            logging.debug('QtGnuplitWidget::GESetWidgetSize')
            logging.debug(f'Widget size: {s.width()} x {s.height()}')

            logging.debug(f'View size: {self.m_view.size().width()} x '
                          f'{self.m_view.size().height()}')
            logging.debug(f'Viewport size: {viewport.size().width()} x '
                          f'{self.m_view.size().height()}')

            parent = self.parentWidget()
            if s != viewport.size() or (parent and not parent.isVisible()):
                logging.debug('Resizing')
                if parent:
                    # The parent is not visible : resize via the sizeHint
                    # mechanism because the "resize" function is not active
                    if not parent.isVisible():
                        logging.debug('Resizing parent')
                        self.m_skipResize = True
                        self.m_sizeHint = s + \
                            QSize(2 * self.m_view.frameWidth(),
                                  2 * self.m_view.frameWidth())
                        parent.updateGeometry()
                        parent.show()
                        self.m_skipResize = False
                    parent.resize(s + parent.size() - viewport.size())
                    # Force an update to geometry, otherwise other widgets
                    # will be moved around due to reising
                    parent.updateGeometry()
                viewport.resize(s)

        elif type == GEStatusText:
            logging.debug("GnuplotWidget::GEStatusText")
            text = dataStream.readQString()
            logging.debug(f"Text: {text}")
            self.setStatusText(text)
        elif type == GECopyClipboard:
            logging.debug("GnuplotWidget::GECopyClipboard")
            QApplication.clipboard().setText(dataStream.readQString())
        elif type == GECursor:
            logging.debug("GnuplotWidget::GECursor")
            cursorType = dataStream.readInt32()
            self.m_view.setCursor(Qt.CursorShape(cursorType))
        elif type == GEWrapCursor:
            logging.debug("GnuplotWidget::GEWrapCursor")
            point = QPoint(dataStream.readInt32(), dataStream.readInt32())
            QCursor.setPos(self.mapToGlobal(point))
        elif type == GEActivate:
            logging.debug("GnuplotWidget::GEActivate")
            self.m_active = True
        elif type == GEDesactivate:
            logging.debug("GnuplotWidget::GEDesactivate")
            self.m_active = False
        else:
            self.m_scene.processEvent(type, dataStream)

    def loadSettings(self, settings: QSettings) -> None:
        self.setAntialias(bool(settings.value('antialias', True)))
        self.setRounded(bool(settings.value('rounded', True)))
        self.setBackgroundColor(settings.value('backgroundColor',
                                               QColor(Qt.white)))
        self.setReplotOnResize(bool(settings.value('replotOnResize', True)))
        self.setStatusLabelActive(bool(settings.value('statusLabelActive',
                                                      False)))

    def saveSettings(self, settings: QSettings) -> None:
        settings.setValue('antialias', self.m_antialias)
        settings.setValue('rounded', self.m_rounded)
        settings.setValue('backgroundColor', self.m_backgroundColor)
        settings.setValue('replotOnResize', self.m_replotOnResize)
        settings.setValue('statusLabelActive', self.m_statusLabelActive)

    @pyqtSlot()
    def copyToClipboard(self) -> None:
        QApplication.clipboard().setPixmap(self.createPixmap())

    @pyqtSlot()
    def print(self, printer: QPrinter) -> None:
        painter = QPainter(printer)
        painter.setRenderHints(self.renderHints())
        self.m_scene.render(painter)

    @pyqtSlot()
    def exportToPdf(self, fileName: str) -> None:
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(fileName)
        printer.setPaperSize(QSizeF(self.m_scene.width(),
                                    self.m_scene.height()), QPrinter.Point)
        printer.setPageMargins(0, 0, 0, 0, QPrinter.Point)
        painter = QPainter(printer)
        painter.setRenderHints(self.renderHints())
        # self.tmp_painter = painter
        # self.tmp_printer = printer
        self.m_scene.render(painter)
        painter.end()

    @pyqtSlot()
    def exportToEps(self) -> None:
        pass

    @pyqtSlot()
    def exportToImage(self, fileName: str) -> None:
        self.createPixmap().save(fileName)

    @pyqtSlot()
    def exportToSvg(self, fileName: str) -> None:
        svg = QSvgGenerator()
        svg.setFileName(fileName)
        svg.setSize(QSize(self.m_view.width(), self.m_view.height()))
        svg.setViewBox(QRect(0, 0, self.m_view.width(), self.m_view.height()))
        painter = QPainter(svg)
        # self.tmp_painter = painter
        self.m_scene.render(painter)
        painter.end()


    def resizeEvent(self, event: QResizeEvent) -> None:
        viewport = self.m_view.viewport()
        self.m_statusLabel.move(viewport.width() - self.m_statusLabel.width(),
                                0)
        logging.debug('QtGnuplotWidget::resizeEvent')
        logging.debug(f'event.size(): {event.size()}')
        logging.debug(f'event.oldSize(): {event.oldSize()}')
        logging.debug(f'widget size: {self.size()}')
        logging.debug(f'view size: {self.m_view.size()}')
        logging.debug(f'viewport size: {viewport.size()}')
        logging.debug(f'last size req.: {self.m_lastSizeRequest}')

        if viewport.size() != self.m_lastSizeRequest and \
           self.m_lastSizeRequest != QSize(-1, -1) and not self.m_skipResize:
            logging.debug('Sending event')
            self.m_eventHandler.postTermEvent(GE_fontprops,
                                              viewport.size().width(),
                                              viewport.size().height(),
                                              0, 0, self)

            if self.m_replotOnResize and self.isActive():
                self.m_eventHandler.postTermEvent(GE_replot, 0, 0, 0, 0, self)
            else:
                self.m_view.fitInView(self.m_scene.sceneRect(),
                                      Qt.KeepAspectRatio)

        super(QtGnuplotWidget, self).resizeEvent(event)

    def setViewMatrix(self) -> None:
        # self.m_view.resetMatrix()
        # self.m_view.resetTransform()
        # self.m_view.setTransformationAnchor(QGraphicsView.NoAnchor)
        # self.m_view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        pass

    def createPixmap(self) -> QPixmap:
        pixmap = QPixmap(self.m_scene.width(), self.m_scene.height())
        pixmap.fill()
        painter = QPainter(pixmap)
        painter.translate(0.5, 0.5)
        painter.setRenderHints(self.renderHints())
        self.m_scene.render(painter)
        return pixmap

    def renderHints(self) -> QPainter.RenderHints:
        hint = QPainter.RenderHint(QPainter.TextAntialiasing)
        if self.m_antialias:
            hint |= QPainter.Antialiasing
        return hint
