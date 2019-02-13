#! /usr/bin/env python3

import sys
import tarfile
import base64
import os
import logging

from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, pyqtProperty
from PyQt5.QtWidgets import (QDialog, QLineEdit, QPushButton, QGridLayout,
                             QDialogButtonBox, QWidget, QFormLayout)
from PyQt5.QtGui import QIntValidator
import getopt

try:
    import BytesIO
except ImportError as e:
    from io import BytesIO


ENABLED = True
# ERROR used for CLI usage.
ERROR = None # 1 for IMAS module not loaded
             # 2 for no IMAS module
             # 3 for corrupted imas module

if 'IMAS_PREFIX' not in os.environ and 'IMAS_VERSION' not in os.environ:
    ERROR = 1
    ENABLED = False

else:
    try:
        import imas
    except ImportError:
        ERROR = 2
        ENABLED = False
    except FileNotFoundError:
        ERROR = 3
        ENABLED = False

class GetVars:
    names = ['SHOT', 'RUN', 'USER', 'DEVICE', 'VERSION', 'RUNNAME', 'DIRPATH']
    numOfParams = len(names)
    shot, run, user, device, version, runName, dirPath = range(numOfParams)

    defaultValues = {}
    defaultValues[shot] = '1001'
    defaultValues[run] = '1001'
    defaultValues[user] = os.getenv('USER')
    defaultValues[device] = 'solps-iter'
    defaultValues[version] = '3'
    defaultValues[runName] = 'my_run'
    defaultValues[dirPath] = os.path.expanduser('~')


class GetDialog(QDialog):
    """Dialog Demanding the shot, run, name and device for getting the data
    from IDS.
    """

    def __init__(self, parent=None):
        super(GetDialog, self).__init__(parent)

    def prepareWidgets(self, parameters, title='IDS Variables',):

        self.setModal(True)

        self.setWindowTitle(title)

        formLayout = QFormLayout(self)

        self.lineEditContainer = {}

        for i in range(GetVars.numOfParams):
            currLineEdit = QLineEdit()
            currLineEdit.setText(GetVars.names[i])
            self.lineEditContainer[i] = currLineEdit
            if parameters[i]:
                currLineEdit.setText(parameters[i])
            else:
                currLineEdit.setText(GetVars.defaultValues[i])

            formLayout.addRow(GetVars.names[i], currLineEdit)

        # Setting integer validator for run and shot numbers.
        self.lineEditContainer[GetVars.run].setValidator(QIntValidator())
        self.lineEditContainer[GetVars.shot].setValidator(QIntValidator())

        # Adding the Ok and Cancel button.
        dialog_button_box = QDialogButtonBox()
        dialog_button_box.setStandardButtons(QDialogButtonBox.Ok |
                                             QDialogButtonBox.Cancel)
        dialog_button_box.accepted.connect(self.accept)
        dialog_button_box.rejected.connect(self.reject)
        formLayout.addRow(dialog_button_box)

    def getValue(self, Id):
        return self.lineEditContainer[Id].text()

    def on_close(self):
        # Returning a dictionary of values. The values are defined in
        # enumerator class GetVars.

        variables = {}

        for i in range(GetVars.numOfParams):
            variables[i] = self.getValue(i)

        # Checking if validating Integers.
        try:
            variables[GetVars.shot] = int(variables[GetVars.shot])
            variables[GetVars.run] = int(variables[GetVars.run])
        except ValueError as e:
            variables[GetVars.shot] = -1
            variables[GetVars.run] = -1

        return variables


class GetIDS(QWidget):
    """ Push button used for plugin."""
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super(GetIDS, self).__init__(parent)

        self.vars = {}
        for i in range(GetVars.numOfParams):
            # At the begining clear all parameters
            self.vars[i] = ''

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
        self.vars[GetVars.user] = user

    def getUser(self):
        return self.vars[GetVars.user]

    user = pyqtProperty(str, getUser, setUser)

    @pyqtSlot(str)
    def setDevice(self, device):
        self.vars[GetVars.device] = device

    def getDevice(self):
        return self.vars[GetVars.device]

    device = pyqtProperty(str, getDevice, setDevice)

    @pyqtSlot(str)
    def setVersion(self, version):
        self.vars[GetVars.device] = version

    def getVersion(self):
        return self.vars[GetVars.device]

    version = pyqtProperty(str, getVersion, setVersion)

    @pyqtSlot(str)
    def setRun(self, run):
        self.vars[GetVars.run] = run

    def getRun(self):
        return self.vars[GetVars.run]

    runNumber = pyqtProperty(str, getRun, setRun)

    @pyqtSlot(str)
    def setShot(self, shot):
        self.vars[GetVars.shot] = shot

    def getShot(self):
        return self.vars[GetVars.shot]

    shotNumber = pyqtProperty(str, getShot, setShot)

    @pyqtSlot(str)
    def setDirPath(self, savedir):
        self.vars[GetVars.dirPath] = savedir

    def getDirPath(self):
        return self.vars[GetVars.dirPath]

    dirPath = pyqtProperty(str, getDirPath, setDirPath)

    @pyqtSlot(str)
    def setRunName(self, name):
        self.vars[GetVars.runName] = name

    def getRunName(self):
        return self.vars[GetVars.runName]

    runName = pyqtProperty(str, getRunName, setRunName)

    def checkParameters(self):
        state = True
        for key in self.vars:
            if not self.vars[key]:
                state = False
                break
        if state:
            return True

        else:
            # Not all variables are set
            logging.warning('Not all parameters are specified!')
            dialog = GetDialog(self)
            dialog.prepareWidgets(self.vars)
            if dialog.exec_():
                self.vars = dialog.on_close()
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

        self.thread.setParameters(self.vars)
        self.thread.start()

    @pyqtSlot()
    def cleanUp(self):
        for key in self.vars:
            self.vars[key] = ''


class GetIDSQThread(QThread):
    """QThread for getting data from an IDS from a separate thread.
    """
    startFlag = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(GetIDSQThread, self).__init__(parent)
        self.parent = parent
        self.vars = {}
        for i in range(GetVars.numOfParams):
            self.vars[i] = None
        self.finished.connect(self.on_finish)
        self.started.connect(self.on_start)

    def setParameters(self, parameters):
        """Function that sets the parameters necessary for accessing IDS.
        """
        for key in parameters:
            self.vars[key] = parameters[key]

    def run(self):
        ids = GetIDSWrapper(self.vars)
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

    def __init__(self, parameters):
        self.vars = {}
        self.setParameters(parameters)
        self.ids = imas.ids(self.vars[GetVars.shot], self.vars[GetVars.run])
        self.state = self.openIDS()

    def setParameters(self, parameters):
        for key in parameters:
            self.vars[key] = parameters[key]

    def openIDS(self):
        logging.info('Opening IDS')
        self.ids.open_env(self.vars[GetVars.user],
                          self.vars[GetVars.device],
                          self.vars[GetVars.version])
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
        dir_path = self.vars[GetVars.dirPath] + '/' + \
                   self.vars[GetVars.runName]

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
    from PyQt5.QtCore import QCoreApplication
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    root.addHandler(ch)

    # For launching python script directly from treminal with python command
    Vars = {}
    Help = """
This is used for testing the importing data from an IDS. By default the data \
from an IDS will be saved in $HOME/my_run directory.

In order to run get_edge path, shot, run, user, device, version and  \
target-directory variables must be defined. Example (terminal):

python3 get_edge_ids.py --shot=1001 --run=1001 --user=%s \
--device=solps-iter --version=3 --targetDir=%s --runName=my_run
"""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "srudvh", ["dirpath=",
                                                            "shot=", "run=",
                                                            "user=", "device=",
                                                           "version=",
                                                           "targetDir=",
                                                           "runName=", "help"])
        for opt, arg in opts:
            #print opt, arg
            if opt in ("-s", "--shot"):
                Vars[GetVars.shot] = int(arg)
            elif opt in ("-r", "--run"):
                Vars[GetVars.run] = int(arg)
            elif opt in ("-u", "--user"):
                Vars[GetVars.user] = arg
            elif opt in ("-t", "--device"):
                Vars[GetVars.device] = arg
            elif opt in ("-v", "--version"):
                Vars[GetVars.version] = arg
            elif opt in ("-D", "--targetDir"):
                Vars[GetVars.dirPath] = arg
            elif opt in ("-R", "--runName"):
                Vars[GetVars.runName] = arg

            if opt in ("-h", "--help"):
                print(Help % (os.environ['USER'], os.path.expanduser('~')))
                sys.exit()

    except Exception:
        print('Supplied option not recognized!')
        print('For help: -h / --help')
        sys.exit(2)

    if len(Vars) < GetVars.numOfParams:
        print('Not enough variables defined!')
        print('For help: -h / --help')
        sys.exit(2)
    elif len(Vars) > GetVars.numOfParams:
        print('Too many variables defined!')
        print('For help: -h / --help')
        sys.exit(2)

    if ERROR:
        if ERROR == 1:
            print('IMAS module is not loaded.')
        elif ERROR == 2:
            print('There is no IMAS module... Exiting.')
        elif ERROR == 3:
            print(__name__, 'Corrupted IMAS module!')
        else:
            print('Unknown error with IMAS')
        sys.exit(2)

    app = QCoreApplication(sys.argv)
    t = GetIDSQThread()
    t.setParameters(Vars)
    t.finished.connect(app.exit)
    t.start()
    sys.exit(app.exec_())
