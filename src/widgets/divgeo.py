#!/usr/bin/env python3
""" A PyQt custom DivGeo widget for Qt Designer.
"""

from PyQt5.QtCore import (Qt, QProcess, QSize, pyqtSignal,
                          QSettings, pyqtSlot, pyqtProperty, QPoint, QRect,
                          QTimer)
from PyQt5.QtGui import QImage, QPixmap, QWindow
from PyQt5.QtWidgets import QLabel, QFrame, QWidget, QVBoxLayout, QSizePolicy, QWidgetItem


import logging
import os

import time

class DivGeo(QWidget):
    """ DivGeo(QLabel)

        Provides a custom widget to embed a DivGeo application as a
        Qt widget.

        TODO: Run solps-iter/scripts/dg directly to set environment
              variables such as ``DEVICE, DG_IMPORT_TOPOLOGY_MASK``, ...
    """
    _embedDivGeo = pyqtSignal()

    stderrOutput = pyqtSignal(str)

    def __init__(self, parent=None):
        super(DivGeo, self).__init__(parent)
        # self.setWindowFlags(Qt.SubWindow)
        # self.setAttribute(Qt.WA_NoSystemBackground)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.divgeo_path = None

        self.my_win_id = int(self.winId())
        print('Win id ', self.my_win_id)
        self._container = None
        self._window = None
        self.Layout = QVBoxLayout()
        self.setLayout(self.Layout)
        self._embedDivGeo.connect(self.embedDivGeo)

        # self.my_window = QWindow()
        # self.my_container = QWidget.createWindowContainer(self.my_window)
        # self.my_win_id = int(self.my_window.winId())
        # layout.addWidget(self.my_container)

        #self.my_win_id = 31457602
        """
        self.my_window = QWindow.fromWinId(self.my_win_id)
        self.my_window.setFlags(Qt.FramelessWindowHint)
        self._container = QWidget.createWindowContainer(self.my_window)
        self._container.setParent(self)
        print('Container id', int(self._container.winId()), self._container)
        """
        #self._container.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.divgeo = QProcess(self.parent())
        #self.divgeo = QProcess(self._container)
        self.divgeo.error.connect(self.show_error)

        self.divgeo.readyReadStandardError.connect(self.stderrReady)
        self.divgeo.readyReadStandardOutput.connect(self.stdoutReady)

    def __del__(self):
        if self.divgeo.state(): # state() == 0 means NotRunning
            self.divgeo.kill()
            print("Terminating DivGeo")

    # def sizeHint(self):
    #     return QSize(700, 400)

    # def minimumSizeHint(self):
    #     return QSize(320, 180)

    @pyqtSlot()
    def stderrReady(self):
       error_data = self.divgeo.readAllStandardError()
       error_text = bytearray(error_data).decode('utf8')
       logging.error(error_text)

    @pyqtSlot()
    def stdoutReady(self):
        data = self.divgeo.readAllStandardOutput()
        text = bytearray(data).decode('utf8')

        for line in text.splitlines():
            if "DivGeo WID: " in line:
                DG_ID = int(line.lstrip("DivGeo WID: "))
                self.DivGeoID = DG_ID
                self._embedDivGeo.emit()

        logging.debug(text)

    @pyqtSlot()
    def embedDivGeo(self):
        width, height = self.width(), self.height()
        self.hide()
        self._window = QWindow.fromWinId(self.DivGeoID)
        # self._window.setFlags(Qt.FramelessWindowHint)
        # self._window.setOpacity(1.0)

        self._container = QWidget.createWindowContainer(self._window,
                                                        self.parent(),
                                                        Qt.FramelessWindowHint)
        #self._container.setParent(self)
        # self._container.setGeometry(QRect(0, 0, width, height))
        self._container.show()
        self.Layout.addWidget(self._container)
        self.show()
        #self._timer.timeout.disconnect()

    @pyqtSlot()
    def startDivGeo(self):
        """ Starts divgeo process inside the widget
        """
        if self.divgeo.state():
            self.divgeo.kill()
            return
        if self.layout():
            self.clearLayout()

        if self.divgeo_path is None:
            settings = QSettings('ITER', 'solps-gui')
            self.divgeo_path = settings.value('divgeo_path',
                                              os.path.expanduser("~")
                + '/solps-iter/modules/DivGeo/builds/ITER.ifort64/dg.exe')
        #        + '/solps-iter/modules/DivGeo/builds/default.gcc/dg.exe')
        geometry = '{}x{}'.format(self.width(), self.height())
        global_pos = self.mapToGlobal(QPoint(0, 0))
        if global_pos.x():
           geometry += '+{}+{}'.format(global_pos.x()-6, global_pos.y()-24)

        options = [
                   "-xrm", 'DivGeo.geometry: ' + geometry,
                   # "-wid", str(int(self.winId()))
                  ]

        # options = ["-into", self.my_win_id]
        # print(options)
        # print(os.environ.keys())
        # env = self.divgeo.processEnvironment()
        # print(env.keys())
        # for key in env.keys():
        #     print(key, env.value(key))

        # for key in os.environ.keys():
        #     env.insert(key, os.environ[key])
        # self.divgeo.setProcessEnvironment(env)
        # self.divgeo.setWorkingDirectory(os.path.expanduser('~'))
        self.divgeo.start(self.divgeo_path, options)
        if not self.divgeo.waitForStarted():
            logging.error(self.divgeo.program() + " not started")
            return
        # print(self.divgeo.program(), self.divgeo.arguments())
        # if not self._container.isVisible():
        #     self._container.setVisible(True)

    @pyqtSlot(QProcess.ProcessError)
    def show_error(self, error):
        """ Writes an error to the widget in case that the process failed
            to start.
        """
        errors = ['Failed to Start', 'Crashed', 'Timedout', 'WriteError',
            'ReadError', 'UnknownError']
        msg = 'DivGeo process: ' + errors[error]
        print(msg)
        logging.error(msg)
        #self.setText(msg)

    @pyqtSlot(int)
    def setDivGeoPath(self, divgeo_path):
        """ Executable requires absolute path. No ${PATH} possible!
        """
        self.divgeo_path = divgeo_path

    def getDivGeoPath(self):
        return self.divgeo_path

    divgeoPath = pyqtProperty(str, getDivGeoPath, setDivGeoPath)

    @pyqtSlot(str)
    def setRundir(self, directory):
        """
        Args:
             directory (str): Absolute path to SOLPS directory with run data.

        """
        self.rundir = directory

    # def dropEvent(self, e):
    #     print("Container", self._container)
    #     if self._container:
    #         self._container.show()
    #         self._container.setGeometry(QRect(0, 0, self.width(), self.height()))
    #         print("Resizing container")
    #     else:
    #         print("No container to resize")

    #     self.resize(self.width(), self.height())
    #     super(DivGeo, self).dropEvent(e)

    def clearLayout(self):
        for i in reversed(range(self.layout().count())):
            item = self.layout().itemAt(i)
            if isinstance(item, QWidgetItem):
                item.widget().close()
            self.layout().removeItem(item)

if __name__ == "__main__":
    @pyqtSlot()
    def cbresize(self):
        divgeo.resize(550, 400)

    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
    from PyQt5.QtCore import QRect
    import logging

    logging.getLogger().setLevel(logging.DEBUG)

    app = QApplication(sys.argv)
    main_window = QMainWindow()

    main_window.resize(600, 400)
    layout = QVBoxLayout()

    divgeo = DivGeo(main_window)
    # divgeo.setGeometry(QRect(70, 30, 501, 411))
    # divgeo.resize(500,500)
    # divgeo.setDivGeoPath("dg")

    pushButton = QPushButton()
    #pushButton.setGeometry(QRect(30, 450, 81, 22))
    pushButton.setText("Start")

    pushButtonR = QPushButton()
    #pushButtonR.setGeometry(QRect(130, 450, 81, 22))
    pushButtonR.setText("Resize")

    # main_window.setCentralWidget(divgeo)
    pushButton.clicked.connect(divgeo.startDivGeo)
    pushButtonR.clicked.connect(cbresize)

    layout.addWidget(divgeo)
    layout.addWidget(pushButton)
    layout.addWidget(pushButtonR)
    w = QWidget(main_window)
    w.setLayout(layout)
    main_window.setCentralWidget(w)
    main_window.show()
    divgeo.show()
    sys.exit(app.exec_())
