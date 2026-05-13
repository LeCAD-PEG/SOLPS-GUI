#! /usr/bin/env python3

import sys
import tarfile
import base64
import os
import logging

from PySide6.QtCore import Slot, QThread, Signal, Property
from PySide6.QtWidgets import (QDialog, QLineEdit, QPushButton, QGridLayout,
                             QDialogButtonBox, QWidget, QFormLayout)
from PySide6.QtGui import QIntValidator
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
    finished = Signal()

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

    @Slot(str)
    def setUser(self, user):
        self.vars[GetVars.user] = user

    def getUser(self):
        return self.vars[GetVars.user]

    user = Property(str, getUser, setUser, doc="username or public")

    @Slot(str)
    def setDevice(self, device):
        self.vars[GetVars.device] = device

    def getDevice(self):
        return self.vars[GetVars.device]

    device = Property(str, getDevice, setDevice, doc="Database")

    @Slot(str)
    def setVersion(self, version):
        self.vars[GetVars.device] = version

    def getVersion(self):
        return self.vars[GetVars.device]

    version = Property(str, getVersion, setVersion, doc="DB version")

    @Slot(str)
    def setRun(self, run):
        self.vars[GetVars.run] = run

    def getRun(self):
        return self.vars[GetVars.run]

    runNumber = Property(str, getRun, setRun, doc="Run number")

    @Slot(str)
    def setShot(self, shot):
        self.vars[GetVars.shot] = shot

    def getShot(self):
        return self.vars[GetVars.shot]

    shotNumber = Property(str, getShot, setShot, doc="Pulse ID")

    @Slot(str)
    def setDirPath(self, savedir):
        self.vars[GetVars.dirPath] = savedir

    def getDirPath(self):
        return self.vars[GetVars.dirPath]

    dirPath = Property(str, getDirPath, setDirPath, doc="Rundir")

    @Slot(str)
    def setRunName(self, name):
        self.vars[GetVars.runName] = name

    def getRunName(self):
        return self.vars[GetVars.runName]

    runName = Property(str, getRunName, setRunName, doc="Run name")

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

    @Slot()
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

    @Slot()
    def cleanUp(self):
        for key in self.vars:
            self.vars[key] = ''


class GetIDSQThread(QThread):
    """QThread for getting data from an IDS from a separate thread.
    """
    startFlag = Signal(bool)

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

    @Slot()
    def on_start(self):
        logging.info('Getting IDS...')
        self.startFlag.emit(False)

    @Slot()
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
        self.new_api = False
        self.ids = None
        
        # Try different IMAS API versions
        try:
            # Try new IMAS API with ids_defs (IMAS >= 3.30.0)
            backend = imas.ids_defs.MDSPLUS_BACKEND
            self.ids = imas.DBEntry(backend,
                                    self.vars[GetVars.device],
                                    self.vars[GetVars.shot],
                                    self.vars[GetVars.run],
                                    self.vars[GetVars.user],
                                    data_version=str(self.vars[GetVars.version]))
            self.new_api = True
            logging.info('Using new IMAS API (DBEntry with ids_defs)')
        except (AttributeError, NameError):
            try:
                # Try new IMAS API with imasdef
                backend = imas.imasdef.MDSPLUS_BACKEND
                self.ids = imas.DBEntry(backend,
                                        self.vars[GetVars.device],
                                        self.vars[GetVars.shot],
                                        self.vars[GetVars.run],
                                        self.vars[GetVars.user],
                                        data_version=str(self.vars[GetVars.version]))
                self.new_api = True
                logging.info('Using new IMAS API (DBEntry with imasdef)')
            except (AttributeError, NameError):
                # Fall back to old IMAS API
                try:
                    self.ids = imas.ids(self.vars[GetVars.shot], self.vars[GetVars.run])
                    self.new_api = False
                    logging.info('Using old IMAS API (ids with 2 params)')
                except (AttributeError, TypeError):
                    logging.error('Could not create IMAS connection with any known API!')
                    self.state = False
                    return
        
        self.state = self.openIDS()

    def setParameters(self, parameters):
        for key in parameters:
            self.vars[key] = parameters[key]

    def openIDS(self):
        logging.info('Opening IDS')
        if self.new_api:
            # New API: DBEntry is already connected in constructor
            try:
                self.ids.open()
                logging.info('IDS opened OK!')
                return True
            except Exception as e:
                logging.error(f'IDS open failed: {e}')
                return False
        else:
            # Old API
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
        if self.new_api:
            # New API: use get() method
            edge_profiles = self.ids.get('edge_profiles')
            parameter_string = edge_profiles.code.parameters
        else:
            # Old API: direct access
            self.ids.edge_profiles.get()
            parameter_string = self.ids.edge_profiles.code.parameters
        # print(self.ids.edge_profiles.ggd[0])
        # Convert IDSString0D or similar objects to plain string
        bstring = base64.b64decode(str(parameter_string))
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
                extracted = tar.extractfile(member)
                if extracted is None:
                    logging.warning(f'Skipping {name} (symlink or directory)')
                    continue
                file = extracted.read().decode()
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
            # --- Attach optimization history arrays to ep as a Python attribute for GUI use ---
            try:
                import numpy as np
                ep = getattr(self, 'ep', None)
                if ep is not None:
                    ep.opt_history = {
                        'parm_hist1': np.loadtxt(os.path.join(dir_path, 'parm_hist1.dat')).tolist() if os.path.exists(os.path.join(dir_path, 'parm_hist1.dat')) else None,
                        'parm_hist2': np.loadtxt(os.path.join(dir_path, 'parm_hist2.dat')).tolist() if os.path.exists(os.path.join(dir_path, 'parm_hist2.dat')) else None,
                        'parm_hist3': np.loadtxt(os.path.join(dir_path, 'parm_hist3.dat')).tolist() if os.path.exists(os.path.join(dir_path, 'parm_hist3.dat')) else None,
                        'objval': np.loadtxt(os.path.join(dir_path, 'objval.dat')).tolist() if os.path.exists(os.path.join(dir_path, 'objval.dat')) else None,
                        'grad': np.loadtxt(os.path.join(dir_path, 'grad.dat')).tolist() if os.path.exists(os.path.join(dir_path, 'grad.dat')) else None,
                    }
            except Exception as e:
                logging.warning(f'Could not attach opt_history to ep: {e}')
        except PermissionError:
            logging.error('Warning!, No permission in the current directory!')
        except tarfile.ReadError as e:
            logging.error('Warning empty file!')


if __name__ == '__main__':
    from PySide6.QtCore import QCoreApplication
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
    sys.exit(app.exec())
