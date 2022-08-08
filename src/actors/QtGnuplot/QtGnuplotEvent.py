from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtCore import QObject, Signal, Slot, QDataStream, QPoint
import logging
import sys
import struct

GESetCurrentWindow, GEInitWindow, GECloseWindow, GEExit, GEPersist, \
    GEStatusText, GETitle, GESetCtrl, GESetPosition, GEPID, \
    GESetWidgetSize, GECursor, GEPenColor, GEBackgroundColor, GEBrushStyle, \
    GEPenStyle, GEPointSize, GELineWidth, GEFillBox, GEPutText, \
    GEFilledPolygon, GETextAngle, GETextAlignment, GEPoint, GEClear, \
    GEZoomStart, GEZoomStop, GERuler, GECopyClipboard, GEMove, GEVector, \
    GELineTo, GESetFont, GEEnhancedFlush, GEEnhancedFinish, GEImage, \
    GESetSceneSize, GERaise, GEWrapCursor, GEScale, GEActivate, GEDesactivate,\
    GELayer, GEPlotNumber, GEHypertext, GETextBox, GEModPlots, GEAfterPlot, \
    GEFontMetricRequest, GEDashPattern, GEDone = range(1000, 1051)

QTMODPLOTS_SET_VISIBLE, QTMODPLOTS_SET_INVISIBLE, \
    QTMODPLOTS_INVERT_VISIBILITIES = range(3)

QTLAYER_BEGIN_KEYSAMPLE, QTLAYER_END_KEYSAMPLE, QTLAYER_BEFORE_ZOOM = range(3)

GE_buttonrelease = 2  # mousecmn


class QtGnuplotEventReceiver(object):
    def __init__(self, parent=None):
        self.m_eventHandler = None

    def processEvent(self, type, dataStream) -> None:
        # Virtual Void
        return 0

    def swallowEvent(self, type, dataStream) -> None:
        logging.debug(f"Swallowing {type}")
        point = QPoint()
        if type == GESetCurrentWindow:
            dataStream.readInt32()
        elif type == GEInitWindow:
            pass
        elif type == GECloseWindow:
            dataStream.readInt32()
        elif type == GEExit:
            pass
        elif type == GEPersist:
            pass
        elif type == GEStatusText:
            dataStream.readQString()
        elif type == GETitle:
            dataStream.readQString()
        elif type == GESetCtrl:
            dataStream.readBool()
        elif type == GECursor:
            dataStream.readInt32()
        elif type == GEZoomStart:
            dataStream.readQString()
        elif type == GEZoomStop:
            dataStream.readQString()
        elif type == GERaise:
            pass
        elif type == GEDesactivate:
            pass
        elif type == GESetPosition:
            dataStream >> point
        else:
            logging.debug(f"Event not swallowed: {type}!")

    def serverName(self) -> str:
        if self.m_eventHandler:
            return self.m_eventHandler.serverName()
        return ''


class QtGnuplotEventHandler(QObject):
    connected = Signal()
    disconnected = Signal()

    def __init__(self, parent=None, socket: str = "") -> None:
        super(QtGnuplotEventHandler, self).__init__(parent)
        self.m_socket = 0
        self.m_blockSize = 0
        self.m_server = QLocalServer(self)
        if not self.m_server.listen(socket):
            logging.debug("QtGnuplotApplication error: cannot open server")
        self.m_server.newConnection.connect(self.newConnection)

    def init(self, inSocket: str) -> None:
        pass

    def postTermEvent(self, type: int, mx: int, my: int, par1: int, par2: int,
                      widget) -> bool:
        if self.m_socket == 0 or \
           self.m_socket.state() != QLocalSocket.ConnectedState:
            return False

        if widget and not widget.isActive():
            if type == GE_buttonrelease:
                logging.debug("Rescued buttonrelease event")
            else:
                logging.debug("Event lost because widget is not active")
                return False

        #  event_t = gp_event_t(type=type, mx=mx, my=my, par1=par1, par2=par2,
        #               winid=0) # We don't forward any window id to gnuplot
        logging.debug(f"QtGnuplotEvent::postTermEvent {type} {mx} "
                      f"{my} {par1} {par2}")
        gp_event_t = struct.pack("6i", type, mx, my, par1, par2, 0)
        self.m_socket.write(gp_event_t)
        return True

    def serverName(self) -> str:
        return self.m_server.serverName()

    @Slot()
    def newConnection(self) -> None:
        self.m_socket = self.m_server.nextPendingConnection()
        self.m_socket.readyRead.connect(self.readEvent)
        self.m_socket.disconnected.connect(self.connectionClosed)
        self.connected.emit()

    @Slot()
    def readEvent(self) -> None:
        dataStream = QDataStream(self.m_socket)
        dataStream.setVersion(QDataStream.Qt_4_4)

        receiver = self.parent()
        if not receiver:
            logging.debug("QtGnuplotEventHandler.readEvent -- No receiver!")
            return
        while not dataStream.atEnd():
            if self.m_blockSize == 0:
                if self.m_socket.bytesAvailable() < sys.getsizeof(int()):
                    return
                self.m_blockSize = dataStream.readUInt32()

            if self.m_socket.bytesAvailable() < self.m_blockSize:
                # Break if the message is not entirelly received yet
                logging.debug(f"Packet size {self.m_socket.bytesAvailable()}")
                return

            remaining = self.m_socket.bytesAvailable() - self.m_blockSize
            while self.m_socket.bytesAvailable() > remaining:
                eventType = dataStream.readInt32()
                if eventType < 1000 or eventType > GEDone:
                    logging.debug(f"Error event type: {eventType}")
                    logging.debug("qt_gnuplot exiting on read error")
                    sys.exit(0)
                logging.debug(f"\tProcessing: {eventType}")
                receiver.processEvent(eventType, dataStream)

            self.m_blockSize = 0

    @Slot()
    def connectionClosed(self) -> None:
        self.disconnected.emit()
