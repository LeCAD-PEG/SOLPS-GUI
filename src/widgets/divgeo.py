#!/usr/bin/env python3
""" A PyQt custom DivGeo widget for Qt Designer.
"""

from PyQt5.QtCore import (Qt, QProcess, QProcessEnvironment, QSize, pyqtSignal,
                          QSettings, pyqtSlot, pyqtProperty, QPoint, QRect)
from PyQt5.QtGui import QImage, QPixmap, QWindow
from PyQt5.QtWidgets import QLabel, QFrame, QWidget


import logging
import os
import tempfile

class DivGeo(QLabel):
    """ DivGeo(QLabel)
    
        Provides a custom widget to embed a DivGeo application as a
        Qt widget.

        TODO: Run solps-iter/scripts/dg directly to set environment
              variables such as ``DEVICE, DG_IMPORT_TOPOLOGY_MASK``, ...
    """

    stderrOutput = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(DivGeo, self).__init__(parent)
        self.divgeo_path = None
        self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setText("DivGeo 2.11a widget for SOLPS")
        self.my_win_id = int(self.winId())
        self.my_window = QWindow.fromWinId(self.my_win_id)
        self.container = QWidget.createWindowContainer(self.my_window, self)
        self.container.setGeometry(QRect(0, 0, self.width(), self.height()))
        self.divgeo = QProcess(self.container)
        self.divgeo.error.connect(self.show_error)
        self.divgeo.readyReadStandardError.connect(self.stderrReady)

    def __del__(self):
        if self.divgeo.state() != QProcess.NotRunning:
            self.divgeo.kill()
            print("Terminating DivGeo")

    def sizeHint(self):
        return QSize(700, 400)

    def minimumSizeHint(self):
        return QSize(320, 180)

    @pyqtSlot()
    def stderrReady(self):
       error_data = self.divgeo.readAllStandardError()
       error_text = bytearray(error_data).decode('utf8')
       logging.error(error_text)

    @pyqtSlot()
    def startDivGeo(self):
        """ Starts divgeo process inside the widget
        """
        if self.divgeo_path is None:
            settings = QSettings('ITER', 'solps-gui')
            self.divgeo_path = settings.value('divgeo_path',
                                              os.path.expanduser("~")
                + '/solps-iter/modules/DivGeo/builds/default.gcc/dg.exe')

        geometry = '{}x{}'.format(self.width(), self.height())
        global_pos = self.mapToGlobal(QPoint(0,0))
        if global_pos.x():
           geometry += '+{}+{}'.format(global_pos.x()-6, global_pos.y()-24)
        options = ["-wid", str(self.my_win_id),
                   "-xrm", "DivGeo.geometry: " + geometry ]
        self.divgeo.start(self.divgeo_path, options)
        if not self.divgeo.waitForStarted():
            logging.error(self.divgeo.program() + " not started")
            return
        if not self.container.isVisible():
            self.container.setVisible(True)

    @pyqtSlot(QProcess.ProcessError)
    def show_error(self, error):
        """ Writes an error to the widget in case that the process failed
            to start.
        """
        errors = ['Failed to Start', 'Crashed', 'Timedout', 'WriteError',
            'ReadError', 'UnknownError']
        msg = 'DivGeo process: ' + errors[error]
        logging.error(msg)
        self.setText(msg)

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


if __name__ == "__main__":
    @pyqtSlot()
    def cbresize(self):
        divgeo.resize(550,400)

    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
    from PyQt5.QtCore import QRect
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.resize(648, 520)
    centralwidget = QWidget(main_window)

    divgeo = DivGeo(centralwidget)
    divgeo.setGeometry(QRect(70, 30, 501, 411))
    #divgeo.setDivGeoPath("dg")

    pushButton = QPushButton(centralwidget)
    pushButton.setGeometry(QRect(30, 450, 81, 22))
    pushButton.setText("Start")

    pushButtonR = QPushButton(centralwidget)
    pushButtonR.setGeometry(QRect(130, 450, 81, 22))
    pushButtonR.setText("Resize")

    main_window.setCentralWidget(centralwidget)
    pushButton.clicked.connect(divgeo.startDivGeo)
    pushButtonR.clicked.connect(cbresize)
    main_window.show()
    sys.exit(app.exec_())
