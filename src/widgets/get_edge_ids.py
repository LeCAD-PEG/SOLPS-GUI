# Python 3.5

import getopt
import sys
import tarfile
import base64
import os

from PyQt5.QtCore import pyqtSlot, Qt, QSize, QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit,
                             QGridLayout, QLabel, QDialogButtonBox, )
from PyQt5.QtGui import QIntValidator

try:
    import BytesIO
except ImportError as e:
    from io import BytesIO

try:
    import imas
except ImportError as e:
    if __name__ == '__main__':
        print('There is no imas module... Exiting.')
        sys.exit()
    else:
        pass

class GetDialog(QDialog):
    """Dialog Demanding the shot, run, name and device for getting the data
    from IDS.
    """

    def __init__(self, parent=None, shot='1001', run='1001',
                 user=os.getenv('USER'), device='solps-iter', version='3',
                 runName='new_run', dirpath=os.path.expanduser('~')):
        super(GetDialog, self).__init__(parent)
        self.setModal(True)
        self.main_layout = QGridLayout(self)
        self.setWindowTitle('Get IDS')

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
        self.main_layout.addWidget(QLineEdit(dirpath), 6, 1, Qt.AlignCenter)

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


class GetIDS(QThread):
    """QThread for getting data from an IDS from a separate thread.
    """
    emitMessage = pyqtSignal(str)
    startFlag = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(GetIDS, self).__init__(parent)
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

    def setStatusBar(self, status_bar):
        self.status_bar = status_bar

    def setPushButton(self, push_button):
        self.push_button = push_button

    def setParameters(self, shot='', run='', user='', device='', version='',
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


    def checkParameters(self):
        """Function that checks if all parameter are defined to open an ids."""

        if self.shot and self.runNumber and self.user and self.device and \
           self.version:
            return True
        else:
            self.emitMessage.emit("Not all parameters are specified!")
            print("Not all parameters are specified!")
            dialog = GetDialog(self.parent, self.shot, self.runNumber,
                               self.user, self.device, self.version,
                               self.runName, self.dirpath)
            if dialog.exec_():
                self.shot, self.runNumber, self.user, self.device, \
                  self.version, self.runName, self.dirpath = dialog.on_close()
                return self.checkParameters()
            else:
                self.emitMessage.emit("Dialog canceled, not enough "
                                      "parameters.")
                print("Dialog canceled, not enough parameters.")
                return False

    def run(self):
        ids = GetIDSWrapper(int(self.shot), int(self.runNumber), self.user,
                            self.device, self.version, self.dirpath,
                            self.runName)
        # Data is saved if the self.dirpath and self.runName were provided.
        ids.saveData()

    @pyqtSlot()
    def on_start(self):
        print('Getting IDS...')
        self.emitMessage.emit('Getting IDS...')
        self.startFlag.emit(False)

    @pyqtSlot()
    def on_finish(self):
        print('Finished')
        self.startFlag.emit(True)
        self.emitMessage.emit('Finished.')


class GetIDSWrapper:
    """This class gets the data from an IDS and save it to a directory.

    You provide the necessary id parameters so the IDS can be accessed, then
    the data is written to the directory you specify.
    """
    def __init__(self, shot='', run='', user='', machine='', version='',
                 dirpath='', runName=''):

        self.shot = shot
        self.run = run
        self.user = user
        self.machine = machine
        self.version = version

        self.dirpath = dirpath
        self.runName = runName

        self.ids = imas.ids(shot, run)
        self.state = self.openIDS()

    def openIDS(self):
        print('Opening IDS')
        self.ids.open_env(self.user, self.machine, self.version)
        if self.ids.isConnected():
            print('IDS opened OK!')
            return True
        else:
            print('IDS open failed!')
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
        if self.dirpath == '' and self.runName == '':
            print('No location specified, saving stopped')
            return

        dir_path = self.dirpath + '/' + self.runName

        if os.path.exists(dir_path):
            print('Directory already exists... Canceling!')
            return

        try:
            tar = self.extractFiles()
            for member in tar:
                name = member.name
                file = tar.extractfile(member).read().decode()
                print("Writing to ", dir_path + '/' + name)
                abs_path = dir_path + '/' + name

                # The reason for the following lines is that some input files
                # are located in the ${TOP}/../baserun directory, hence there
                # is a check for each file if the directory exists.

                if not os.path.exists(os.path.dirname(abs_path)):
                    try:
                        os.makedirs(os.path.dirname(abs_path))
                    except OSError:
                        print("Warning! Cannot create directory, permission "
                              "denied")
                        continue
                with open(abs_path, 'w') as f:
                    f.write(file)
        except PermissionError:
            print('Warning!, No permission in the current directory!')

if __name__ == '__main__':
    """
    python3.5 put_edge_ids.py --dirpath=/home/ITER/simicg/RUNS/demo/2171/baserun\
    <--user=simicg --run=1001 --shot=1001 --device=solps-iter --version=3
    """

    # user = "simicg"
    # run = 1005dir_path
    # shot = 1005
    # machine = "solps-iter"
    # version = "3"
    # x = GetIDS(shot, run, user, machine, version)
    # if x.state == 'False':
    #     sys.exit()
    # string = x.readCodeParameters()
    # print(string)
    # print(x.ids.edge_profiles)


    # For launching python script directly from treminal with python command
    try:
        opts, args = getopt.getopt(sys.argv[1:], "srutvh", ["dirpath=",
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
                print("In order to run b2read file path, shot, run, user,"
                    "device and version variables must be defined."
                    "Example (terminal): "
                    "python3.5 put_edge_ids.py "
                    "baserun "
                    "--shot=1000 --run=1 --user=tomsicp --device=solps-iter "
                    "--version=3")
                sys.exit()

    except Exception:
        print ('Supplied option not recognized!')
        print ('For help: b2read -h / --help')
        sys.exit(2)

    # few paths to example files for testing
    # /home/ITER/tomsicp/solps-iter/runs/AUG_16151_D/baserun
    # /home/ITER/tomsicp/solps-iter-devel/runs/ITER_535_D+He+Ar/baserun
    # run: "imasdb solps-iter"
    # Example command:
    """
python3.5 get_edge_ids.py --dirpath=/home/ITER/simicg/RUNS/demo/2171/baserun --user=simicg --run=1001 --shot=1001 --device=solps-iter --version=3
    """
    app = QApplication(sys.argv)
    t = GetIDS()
    t.setParameters(shot=shot, run=run, user=user, device=device,
                    version=version)
    t.finished.connect(app.exit)
    t.start()
    sys.exit(app.exec_())