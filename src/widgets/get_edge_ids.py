#!/usr/bin/python3

import sys

ENABLED = True

try:
    import imas
except ImportError as e:
    if __name__ == '__main__':
        print('There is no imas module... Exiting.')
        sys.exit()
    else:
        ENABLED = False
        pass

import tarfile
import base64
import os
import logging

from PyQt5.QtCore import pyqtSlot, Qt, QSize, QThread, pyqtSignal, pyqtProperty
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton,
                             QGridLayout, QLabel, QDialogButtonBox, QWidget)
from PyQt5.QtGui import QIntValidator
import getopt

try:
    import BytesIO
except ImportError as e:
    from io import BytesIO

class GetDialog(QDialog):
    """Dialog Demanding the shot, run, name and device for getting the data
    from IDS.
    """
    def __init__(self, parent=None):
        super(GetDialog, self).__init__(parent)

    def prepareWidgets(self, shot='1001', run='1001', title='Get IDS',
                       user=os.getenv('USER'), device='solps-iter',
                       version='3', runName='new_run',
                       path=os.path.expanduser('~')):

        self.setModal(True)
        self.main_layout = QGridLayout(self)
        self.setWindowTitle(title)

        self.main_layout.addWidget(QLabel('SHOT'), 0, 0, Qt.AlignLeft)
        shot = QLineEdit(str(shot))
        shot.setValidator(QIntValidator())
        self.main_layout.addWidget(shot, 0, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('RUN'), 1, 0, Qt.AlignLeft)
        run = QLineEdit(str(run))
        run.setValidator(QIntValidator())
        self.main_layout.addWidget(run, 1, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('USER'), 2, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit(user), 2, 1,
                                   Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('DEVICE'), 3, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit(device),
                                   3, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('VERSION'), 4, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit(version), 4, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('RUN NAME'), 5, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit(runName), 5, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('DIR PATH'), 6, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit(path), 6, 1, Qt.AlignCenter)

        # Adding the Ok and Cancel button.
        dialog_button_box = QDialogButtonBox()
        dialog_button_box.setStandardButtons(QDialogButtonBox.Ok |
                                             QDialogButtonBox.Cancel)
        dialog_button_box.accepted.connect(self.accept)
        dialog_button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(dialog_button_box, 7, 1)

    def sizeHint(self):
        return QSize(100, 100)

    def on_close(self):
        # Returning the values
        # SHOT, RUN, USER, DEVICE, VERSION, run_name exclusively.
        try:
            SHOT = int(self.main_layout.itemAt(1).widget().text())
            RUN = int(self.main_layout.itemAt(3).widget().text())
        except ValueError as e:
            SHOT = -1
            RUN = -1

        USER = self.main_layout.itemAt(5).widget().text()
        DEVICE = self.main_layout.itemAt(7).widget().text()
        VERSION = self.main_layout.itemAt(9).widget().text()
        RUN_NAME = self.main_layout.itemAt(11).widget().text()
        DIR_PATH = self.main_layout.itemAt(13).widget().text()

        return SHOT, RUN, USER, DEVICE, VERSION, RUN_NAME, DIR_PATH

class GetIDS(QWidget):
    """ Push button used for plugin."""
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super(GetIDS, self).__init__(parent)

        self._user = ''
        self._shot = ''
        self._device = ''
        self._version = ''
        self._run = ''
        self._runName = ''
        self._dirPath = ''

        self.thread = GetIDSQThread(self)
        self.thread.finished.connect(self.cleanUp)

        self.pushButton = QPushButton(self)
        self.pushButton.setText("Get IDS")
        self.pushButton.clicked.connect(self.getFromIDS)
        self.pushButton.setEnabled(ENABLED)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.pushButton)
        self.setLayout(layout)

        self.thread.startFlag.connect(self.pushButton.setEnabled)
        self.thread.finished.connect(self.finished)

    @pyqtSlot(str)
    def setUser(self, user):
        self._user = user

    def getUser(self):
        return self._user

    user = pyqtProperty(str, getUser, setUser)

    @pyqtSlot(str)
    def setDevice(self, device):
        self._device = device

    def getDevice(self):
        return self._device

    device = pyqtProperty(str, getDevice, setDevice)

    @pyqtSlot(str)
    def setVersion(self, version):
        self._version = version

    def getVersion(self):
        return self._version

    version = pyqtProperty(str, getVersion, setVersion)

    @pyqtSlot(str)
    def setRun(self, run):
        self._run = run

    def getRun(self):
        return self._run

    runNumber = pyqtProperty(str, getRun, setRun)

    @pyqtSlot(str)
    def setShot(self, shot):
        self._shot = shot

    def getShot(self):
        return self._shot

    shotNumber = pyqtProperty(str, getShot, setShot)

    @pyqtSlot(str)
    def setDirPath(self, savedir):
        self._dirPath = savedir

    def getDirPath(self):
        return self._dirPath

    dirPath = pyqtProperty(str, getDirPath, setDirPath)

    @pyqtSlot(str)
    def setRunName(self, name):
        self._runName = name

    def getRunName(self):
        return self._runName

    runName = pyqtProperty(str, getRunName, setRunName)

    def checkParameters(self):
        if self._runName and self._shot and self._user and self._version and \
           self._device and self._run and self._dirPath:
            return True

        else:
            # Not all variables are set
            dialog = GetDialog(self)
            dialog.prepareWidgets(shot=self._shot, run=self._run,
                                  user=self._user, device=self._device,
                                  version=self._version, path=self._dirPath)
            if dialog.exec_():
                self._shot, self._run, self._user, self._device, \
                self._version, self._runName, self._dirPath = dialog.on_close()
                return self.checkParameters()
            else:
                # Canceled!
                return False

    def checkDestination(self):
        if self.dirpath == '' and self.runName == '':
            logging.warning('No location specified, saving stopped!')
            return False

        dir_path = self.dirpath + '/' + self.runName

        if os.path.exists(dir_path):
            logging.error('Directory already exists... Canceling!')
            return False

        return True

    @pyqtSlot()
    def getFromIDS(self):
        if not self.checkParameters():
            logging.warning('Not all parameters are set! Canceling.')
            self.cleanUp()
            return
        else:
            logging.info('All parameters set. Continuing.')

        if not self.checkDestination:
            return

        self.thread.setParameters(dirpath=self._dirPath, run=int(self._run),
                                  shot=int(self._shot), device=self._device,
                                  version=self._version, user=self._user,
                                  runName=self._runName)
        self.thread.start()

    @pyqtSlot()
    def cleanUp(self):
        self._user = ''
        self._shot = ''
        self._device = ''
        self._version = ''
        self._run = ''
        self._runName = ''
        self._dirPath = ''

class GetIDSQThread(QThread):
    """QThread for getting data from an IDS from a separate thread.
    """
    startFlag = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(GetIDSQThread, self).__init__(parent)
        self.parent = parent
        self.shot = None
        self.runNumber = None
        self.user = None
        self.device = None
        self.version = None

        self.dirpath = None
        self.runName = None

        self.status_bar = None

        self.finished.connect(self.on_finish)
        self.started.connect(self.on_start)

    def setParameters(self, shot=0, run=0, user='', device='', version='',
                      dirpath='', runName=''):
        """Function that sets the parameters.
        """
        self.shot = shot
        self.runNumber = run
        self.user = user
        self.device = device
        self.version = version
        self.dirpath = dirpath
        self.runName = runName



    def run(self):
        ids = GetIDSWrapper(int(self.shot), int(self.runNumber), self.user,
                            self.device, self.version, self.dirpath,
                            self.runName)
        # Data is saved if the self.dirpath and self.runName were provided.
        if ids.state:
            ids.saveData()
        else:
            logging.warning('IDS did not open correctly.')

    @pyqtSlot()
    def on_start(self):
        logging.info('Getting IDS...')
        self.startFlag.emit(False)

    @pyqtSlot()
    def on_finish(self):
        logging.info('Finished reading from IDS.')
        self.startFlag.emit(True)


class GetIDSWrapper:
    """This class gets the data from an IDS and save it to a directory.

    You provide the necessary id parameters so the IDS can be accessed, then
    the data is written to the directory you specify.

    Attributes:

    """
    def __init__(self, shot='', run='', user='', machine='', version='',
                 dirpath='', runName=''):

        self.setParameters(shot, run, user, machine, version, dirpath, runName)
        self.ids = imas.ids(shot, run)
        self.state = self.openIDS()

    def setParameters(self, shot, run, user, machine, version, dirpath,
                      runName):
        self.shot = shot
        self.run = run
        self.user = user
        self.machine = machine
        self.version = version

        self.dirpath = dirpath
        self.runName = runName

    def openIDS(self):
        logging.info('Opening IDS')
        self.ids.open_env(self.user, self.machine, self.version)
        if self.ids.isConnected():
            logging.info('IDS opened OK!')
            return True
        else:
            logging.error('IDS open failed!')
            return False

    def readCodeParameters(self):
        self.ids.edge_profiles.get()
        parameter_string = self.ids.edge_profiles.code.parameters
        # print(self.ids.edge_profiles.ggd[0])
        bstring = base64.b64decode(parameter_string)
        return bstring

    def extractFiles(self):
        bstring = self.readCodeParameters()

        tf = BytesIO(bstring)
        tar = tarfile.TarFile(mode='r', fileobj=tf)
        return tar

    def saveData(self):
        """Saves data in the directory with the name ``runName``. The directory
        is located in the ``dirpath``.
        """
        dir_path = self.dirpath + '/' + self.runName

        try:
            tar = self.extractFiles()
            for member in tar:
                name = member.name
                file = tar.extractfile(member).read().decode()
                logging.info("Writing to " + dir_path + '/' + name)
                abs_path = dir_path + '/' + name

                # The reason for the following lines is that some input files
                # are located in the ${TOP}/../baserun directory, hence there
                # is a check for each file if the directory exists.

                if not os.path.exists(os.path.dirname(abs_path)):
                    try:
                        os.makedirs(os.path.dirname(abs_path))
                    except OSError:
                        logging.warning("Warning! Cannot create directory, "
                                        " permission denied")
                        continue
                with open(abs_path, 'w') as f:
                    f.write(file)
        except PermissionError:
            logging.error('Warning!, No permission in the current directory!')
        except tarfile.ReadError as e:
            logging.error('Warning empty file!')

if __name__ == '__main__':

    # For launching python script directly from treminal with python command
    try:
        opts, args = getopt.getopt(sys.argv[1:], "srudvh", ["dirpath=",
                                                            "shot=", "run=",
                                                            "user=", "device=",
                                                           "version=", "help"])
        for opt, arg in opts:
            #print opt, arg
            if opt in ("-s", "--shot"):
                shot = int(arg)
            elif opt in ("-r", "--run"):
                run = int(arg)
            elif opt in ("-u", "--user"):
                user = arg
            elif opt in ("-t", "--device"):
                device = arg
            elif opt in ("-v", "--version"):
                version = arg

            if opt in ("-h", "--help"):
                print("In order to run get_edge file path, shot, run, user,"
                    "device and version variables must be defined."
                    "Example (terminal):\n"
                    "python3.5 get_edge_ids.py "
                    "--shot=1001 --run=1001 --user=simicg "
                    "--device=solps-iter --version=3")
                sys.exit()

    except Exception:
        print ('Supplied option not recognized!')
        print ('For help: -h / --help')
        sys.exit(2)

    app = QApplication(sys.argv)
    t = GetIDSQThread()
    t.setParameters(shot=shot, run=run, user=user, device=device,
                    version=version)
    t.finished.connect(app.exit)
    t.start()
    sys.exit(app.exec_())
