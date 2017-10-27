#!/usr/bin/env python3
""" A PyQt custom DivGeo widget for Qt Designer.
"""

from PyQt5.QtCore import (Qt, QProcess, QSize, pyqtSignal,
                          QSettings, pyqtSlot, pyqtProperty, QPoint)
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QWidgetItem


import logging
import os

import time

class DivGeo(QWidget):
    """
        Important notice: DivGeo git branch origin/feature/embedxwin
        required for this to work.

        DivGeo(QWidget)

        Provides a custom widget to embed a DivGeo application as a
        Qt widget.

        With the use of QtGui.QWindow and QWidget.createWindowContainer, DivGeo
        is embedded inside the QWindow and then we control the drawings with
        the help of window Container (QWidget.createWindowContainer), which is
        a QWidget object.

        In Qt5 there is no official x11 support, because it was dropped and 
        so far this is the only way to achieve embedding of external 
        applications.

        Furthermore, if we wish to embed an external application we need to get
        it's Window ID. It is used in the function QWindow.fromWinId(int WinId)

        .. note::

           Embedding DivGeo is not always successful. It's hard to figure what
           is causing problems (Either QProcess or x11 window manager?).

        TODO: Run solps-iter/scripts/dg directly to set environment
              variables such as ``DEVICE, DG_IMPORT_TOPOLOGY_MASK``, ...


        Attributes:
            _embedDivGeo (pyqtSignal): Signal used to run the function for
                embedding DivGeo.
            stderrOutput (pyqtSignal): Signal which emits error output from
                QProcess.
    """
    _embedDivGeo = pyqtSignal()

    stderrOutput = pyqtSignal(str)

    def __init__(self, parent=None):
        """Initialize variables. Create an empty layout so that it's created
        before trying to embed DivGeo, to avoid drawing problems.

        Creating QProcess and connecting the Std. Output and Error to slots.
        It is important to specify which object should be parent to the 
        QProcess. In this case we provide the parent of DivGeo(QWidget). Reason
        is, it provides stability when it comes to embedding. Or at least in 
        tests.

        What is important to provide the parent of QWidget DivGeo to the 
        QProcess self.divgeo.

        Attributes:
            _container : Variable that holds the QWidget window container.
            _window : Variable that holds the QWindow for embedding DivGeo.
            Layout (QVBoxLayout): Layout for DivGeo widget.
            divgeo (QProcess): QProcess that will start DivGeo and then provide
                the Window ID so QWidget DivGeo can embed it.
        """

        super(DivGeo, self).__init__(parent)
        self.divgeo_path = None

        self._container = None
        self._window = None
        self.Layout = QVBoxLayout()
        self.setLayout(self.Layout)
        self._embedDivGeo.connect(self.embedDivGeo)

        self.divgeo = QProcess(self.parent())
        self.divgeo.error.connect(self.show_error)

        self.divgeo.readyReadStandardError.connect(self.stderrReady)
        self.divgeo.readyReadStandardOutput.connect(self.stdoutReady)

    def __del__(self):
        if self.divgeo.state(): # state() == 0 means NotRunning
            self.divgeo.kill()
            print("Terminating DivGeo")

    @pyqtSlot()
    def stderrReady(self):
       error_data = self.divgeo.readAllStandardError()
       error_text = bytearray(error_data).decode('utf8')
       logging.error(error_text)

    @pyqtSlot()
    def stdoutReady(self):
        """We read the standard output of QProcess self.divgeo and start to 
        embed the external DivGeo when we get it's Window ID.

        When the Window ID is received the signal _embedDivGeo emits to start
        the embedding function.
        """
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
        """Function that will try to embed the DivGeo started from QProcess 
        self.divgeo. Notice the try, since there are some problems with 
        embedding. The way it works:

        .. code-block:: python

           # We have the Window ID so first we create the QWindow
           window = QWindow.fromWinId(WinID)
           # Now we create the container which will control the resizing and 
           # other geometrical functions
           container = QWidget.createWindowContainer(window,
                                                     parent.parent(),
                                                     QtFramelessWindowHint)
           # It's important to specify the parent to the container. The parent
           # is the widget which holds the widget that is embedding the 
           # external application. If it is confusing:
           # QMainwindow -> DivGeo(QWidget) -> container
           # Provide the QMainwindow as the parent to the container or in this 
           # case DivGeo's parent.

           # Now we just put the container in the parents layout and show it.
           parent.layout().addWidget(container)
           parent.show()
           # It isn't always successful.

        Because I wrote in so many places the same block of code, I decided to
        create a function and then just call it.
        """
        width, height = self.width(), self.height()
        self.hide()
        self._window = QWindow.fromWinId(self.DivGeoID)

        self._container = QWidget.createWindowContainer(self._window,
                                                        self.parent(),
                                                        Qt.FramelessWindowHint)
        self._container.show()
        self.Layout.addWidget(self._container)
        self.show()

    @pyqtSlot()
    def startDivGeo(self):
        """ Starts divgeo process inside the qwidget. We provide geometry 
        coordinates, width and height for starting divgeo.
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
        geometry = '{}x{}'.format(self.width(), self.height())
        global_pos = self.mapToGlobal(QPoint(0, 0))
        if global_pos.x():
           geometry += '+{}+{}'.format(global_pos.x()-6, global_pos.y()-24)

        options = [
                   "-xrm", 'DivGeo.geometry: ' + geometry,
                  ]

        self.divgeo.start(self.divgeo_path, options)
        if not self.divgeo.waitForStarted():
            logging.error(self.divgeo.program() + " not started")
            return

    @pyqtSlot(QProcess.ProcessError)
    def show_error(self, error):
        """ Writes an error to the widget in case that the process failed
            to start.
        """
        errors = ['Failed to Start', 'Crashed', 'Timedout', 'WriteError',
            'ReadError', 'UnknownError']
        msg = 'DivGeo process: ' + errors[error]
        logging.error(msg)

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

    def clearLayout(self):
        """Clearing the layout of widgets.
        """
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
