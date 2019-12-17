from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QObject, QDataStream
from QtGnuplot.QtGnuplotWindow import QtGnuplotWindow
from QtGnuplot.QtGnuplotEvent import (QtGnuplotEventReceiver,
                                      QtGnuplotEventHandler,
                                      GESetCurrentWindow, GEInitWindow,
                                      GECloseWindow, GEExit, GEPersist)


class QtGnuplotApplication(QApplication, QtGnuplotEventReceiver):
    def __init__(self, *args, **kwargs):
        QApplication.__init__(self, [])

        self.setQuitOnLastWindowClosed(False)
        self.setWindowIcon(QIcon(':/images/gnuplot'))

        self.m_windows = {}
        self.m_currentWindow = None
        self.m_lastId = 0
        processName = f"qtgnuplot{self.applicationPid()}"
        self.m_eventHandler = QtGnuplotEventHandler(self, processName)
        self.m_eventHandler.connected.connect(self.exitPersistMode)
        self.m_eventHandler.disconnected.connect(self.enterPersistMode)

    def createNewGnuplotWindow(self) -> None:
        pass

    @pyqtSlot(QObject)
    def windowDestroyed(self, obj: QObject = None) -> None:
        _id = -1

        for key in self.m_windows:
            if obj == self.m_windows[key]:
                _id = key
                break

        if self.m_windows.pop(key) == self.m_currentWindow:
            self.m_currentWindow = None

    @pyqtSlot()
    def enterPersistMode(self) -> None:
        self.setQuitOnLastWindowClosed(True)
        if not self.m_windows:
            self.quit()

    @pyqtSlot()
    def exitPersistMode(self) -> None:
        self.setQuitOnLastWindowClosed(False)

    def processEvent(self, type: int, dataStream: QDataStream):
        if type == GESetCurrentWindow:
            self.m_lastId = dataStream.readInt()
            self.m_currentWindow = self.m_windows[self.m_lastId]
        elif type == GEInitWindow and not self.m_currentWindow:
            self.m_currentWindow = QtGnuplotWindow(self.m_lastId,
                self.m_eventHandler)

            self.m_currentWindow.destroyed.connect(self.windowDestroyed)
            self.m_windows[self.m_lastId, self.m_currentWindow]
        elif type == GECloseWindow:
            id_ = dataStream.readInt()
            closeWindow = self.m_windows.pop(id_)
            if closeWindow:
                closeWindow.close()
        elif type == GEExit:
            self.quit()
        elif type == GEPersist:
            self.enterPersistMode()
        elif self.m_currentWindow:
            self.m_currentWindow.processEvent(type, dataStream)
        else:
            self.swallowEvent(type, dataStream)


