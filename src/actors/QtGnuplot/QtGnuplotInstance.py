from PySide6.QtCore import QObject, Signal, Slot, QProcess
from QtGnuplot import QtGnuplotWidget

import os
import logging


class QtGnuplotInstance(QObject):
    gnuplotOutput = Signal(str)

    def __init__(self, widget: QtGnuplotWidget = None,
                 gnuplotPath: str = "gnuplot"):
        super(QtGnuplotInstance, self).__init__(None)

        self.m_widget = widget
        self.m_gnuplot = QProcess()

        self.m_gnuplot.setProcessChannelMode(QProcess.MergedChannels)
        self.m_gnuplot.start(gnuplotPath)
        self.m_gnuplot.waitForStarted()

        self.m_gnuplot.readyReadStandardOutput.connect(self.gnuplotDataReady)
        if self.m_gnuplot.state() == QProcess.NotRunning:
            logging.error(f'Error starting gnuplot with command {gnuplotPath}')

        self.setWidget(widget)

    @Slot()
    def deleteLater(self):
        self.m_gnuplot.close()

        # Remove the created socket in tmp
        sock = os.path.join('tmp', self.m_widget.serverName())
        if os.path.exists(sock):
            os.unlink(sock)

    def setWidget(self, widget: QtGnuplotWidget) -> None:
        self.m_widget = widget

        if self.m_widget:
            plotAreaSize = self.m_widget.plotAreaSize()
            command = f'set term qt widget "{self.m_widget.serverName()}" ' + \
                      f'size {plotAreaSize.width()},{plotAreaSize.height()}\n'
            logging.debug(command)
            self.exec(command)

    def widget(self) -> QtGnuplotWidget:
        return self.m_widget

    @Slot()
    def gnuplotDataReady(self) -> None:
        result = self.m_gnuplot.readAllStandardOutput()
        self.gnuplotOutput.emit(result.data().decode())

    def exec(self, command: str) -> None:
        if self.m_gnuplot.state() == QProcess.Running:
            self.m_gnuplot.write(command.encode())
        else:
            logging.debug('Process gnuplot not running')

    def execAndRead(self, command: str, msecs: int = 30000) -> str:
        self.m_gnuplot.waitForReadyRead(0)

        while 1:
            trailing = self.m_gnuplot.readAllStandardOutput()
            if not trailing:
                break
            self.gnuplotOutput.emit(trailing)

        self.m_gnuplot.readyReadStandardOutput.disconnect()
        self.exec(command)
        self.m_gnuplot.waitForReadyRead(msecs)
        answer = self.m_gnuplot.readAllStandardOutput()
        self.m_gnuplot.readyReadStandardOutput.connect(self.gnuplotDataReady)
        return answer

    def __lshift__(self, data):
        if isinstance(data, str):
            self.exec(data)
            return self
        elif isinstance(data, list):
            # El in list are QPointF
            command = ""
            for pointF in data:
                command += f"{pointF.x()} {pointF.y()}\n"

            command += 'e\n'
            self.exec(command)
            return self
        else:
            logging.error(f'Not implemented for data: {data}')
        return self
