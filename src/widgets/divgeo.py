#!/usr/bin/env python3
""" A PyQt custom DivGeo widget for Qt Designer.
"""

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSettings
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QWidgetItem, QLabel


import logging
import os
import signal
from akter import Akter



class DivGeo(Akter):
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
        self.labelContainer = None
        self.DivGeoID = None
        self.Layout = QVBoxLayout()
        self.setLayout(self.Layout)

        self.tcsh.stdOutput.connect(self.readStdOutput)

    def __del__(self):
        if self.tcsh.state():  # state() == 0 means NotRunning
            self.tcsh.kill()
            print("Terminating DivGeo")

    @pyqtSlot(str)
    def readStdOutput(self, text):
        """We read the standard output of QProcess self.divgeo and start to
        embed the external DivGeo when we get it's Window ID.

        When the Window ID is received the signal _embedDivGeo emits to start
        the embedding function.
        """

        for line in text.splitlines():
            if "DivGeo WID: " in line:
                DG_ID = int(line.lstrip("DivGeo WID: "))
                self.DivGeoID = DG_ID

            if "DivGeo PID: " in line:
                self.DivGeoPID = int(line.lstrip("DivGeo PID: "))

        if 'STARTING DIVGEO' in text:
            self.labelContainer.setText("DivGeo running.")

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

        # Clean the layout first!
        if not self.DivGeoID:
            return

        self.clearLayout()

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
        if self.layout():
            self.clearLayout()
        self.labelContainer = QLabel()
        self.labelContainer.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.labelContainer)

        if not self.getRunDir():
            self.labelContainer.setText("No run dir selected!")
            return

        self.labelContainer.setText("Started TCSH. (sourcing setup.csh, "
                                    "please wait...)")

        DivGeo = 'dg'

        self.startTcsh()
        env = QSettings('ITER', 'solps-gui')
        device = env.value('device_environment', 'iter')
        cmd = 'cd ' + self.getRunDir() + '\n'
        cmd += 'setenv DEVICE ' + device + '\n'
        cmd += 'echo setting DEVICE as ${DEVICE}\n'
        cmd += 'echo STARTING DIVGEO\n'
        cmd += DivGeo + ' -wid ' + str(int(self.winId())) + '\n'

        self.tcsh.write(cmd)

    @pyqtSlot()
    def stopDivGeo(self):
        if not self.labelContainer:
            self.labelContainer = QLabel()
            self.labelContainer.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.labelContainer)

        if self.DivGeoPID:
            os.kill(self.DivGeoPID, signal.SIGUSR1)
        else:
            self.labelContainer.setText("No DivGeo PID!")
            return

        if self.tcsh.waitForFinished():
            self.tcsh.close()
            self.clearLayout()
            self.labelContainer.setText("Terminated DivGeo.")

        else:
            self.labelContainer.setText("DivGeo not running.")


    def clearLayout(self):
        """Clearing the layout of widgets.
        """
        for i in reversed(range(self.layout().count())):
            item = self.layout().itemAt(i)
            if isinstance(item, QWidgetItem):
                item.widget().close()
            self.layout().removeItem(item)
            del item


if __name__ == "__main__":
    @pyqtSlot()
    def cbresize(self):
        divgeo.resize(550, 400)

    import sys
    import os
    from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

    logging.getLogger().setLevel(logging.DEBUG)

    app = QApplication(sys.argv)
    main_window = QMainWindow()

    main_window.resize(600, 400)
    layout = QVBoxLayout()

    divgeo = DivGeo(main_window)
    divgeo.activateDebugging()
    RunDirPath = os.path.expanduser('~/solps-iter/runs/examples')
    print(RunDirPath)
    divgeo.setRunDir(RunDirPath)
    # divgeo.setGeometry(QRect(70, 30, 501, 411))
    # divgeo.resize(500,500)

    pushButton = QPushButton()
    # pushButton.setGeometry(QRect(30, 450, 81, 22))
    pushButton.setText("Start/Stop")

    pushButtonR = QPushButton()
    # pushButtonR.setGeometry(QRect(130, 450, 81, 22))
    pushButtonR.setText("Resize")

    pushButtonE = QPushButton()
    pushButtonE.setText("Embed DivGeo")

    # main_window.setCentralWidget(divgeo)
    pushButton.clicked.connect(divgeo.startDivGeo)
    pushButtonR.clicked.connect(cbresize)
    pushButtonE.clicked.connect(divgeo.embedDivGeo)

    layout.addWidget(divgeo)
    layout.addWidget(pushButton)
    layout.addWidget(pushButtonR)
    layout.addWidget(pushButtonE)

    w = QWidget(main_window)
    w.setLayout(layout)
    main_window.setCentralWidget(w)
    main_window.show()
    divgeo.show()
    sys.exit(app.exec_())
