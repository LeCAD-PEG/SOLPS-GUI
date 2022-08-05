#! /usr/bin/env python3
# Legend:
#      # .............. variables description, additional (helpful)
#                            information etc.
#      # ............... Commented part of code

# -----------------------------------------------------------------------------
# DESCRIPTION
# This Python script is used to read geometry from b2fgmtry file together with
# electron density, electron temperature and ion temperature scalars from
# b2fstati file. The same data is then written to IDS together by
# creating "Cells" and "Nodes" grid subsets.
#
# Basic environment settings (terminal commands on hpc iter.org)
# $ module load imas/3.7.4/ual/3.4.0
# $ imasdb solps-iter
# -----------------------------------------------------------------------------

from PySide6.QtCore import Slot, QThread, Property, Signal
from PySide6.QtWidgets import (QDialog, QLineEdit, QGridLayout, QDialogButtonBox,
                             QPushButton, QFormLayout)
from PySide6.QtGui import QIntValidator

import sys
import getopt
import logging
import os
import tarfile
import base64

from tcsh_process import TcshProcess

try:
    import BytesIO
except Exception as e:
    from io import BytesIO

ENABLED = True
# ERROR used for CLI usage.
ERROR = None  # 1 for IMAS module not loaded
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

input_files = [
    'input.dat',
    'b2mn.dat',
    'b2ag.dat',
    'b2ah.dat',
    'b2ai.dat',
    'b2ar.dat',
    'b2md.dat',
    'b2.boundary.parameters',
    'b2.neutrals.parameters',
    'b2.numerics.parameters',
    'b2.transport.parameters',
    'b2.wall_save.parameters',
    'b2.feedback_control.parameters',
    'b2.sources.profile',
    'b2.transport.inputfile',
    'b2.user.parameters',
    'b2.atomic_physics_rescale.parameters'
]


class PutVars:
    names = ['SHOT', 'RUN', 'USER', 'DEVICE', 'VERSION', 'RUNDIRPATH']
    numOfParams = len(names)
    shot, run, user, device, version, runDirPath = range(numOfParams)
    defaultValues = {}
    defaultValues[shot] = '1001'
    defaultValues[run] = '1001'
    defaultValues[user] = os.getenv('USER')
    defaultValues[device] = 'solps-iter'
    defaultValues[version] = '3'
    defaultValues[runDirPath] = os.path.expanduser('~')


class PutDialog(QDialog):
    """Dialog Demanding the shot, run, name and device for getting the data
    from IDS.
    """

    def __init__(self, parent=None):
        super(PutDialog, self).__init__(parent)

    def prepareWidgets(self, parameters, title='IDS Variables'):
        self.setModal(True)

        self.setWindowTitle(title)

        formLayout = QFormLayout(self)

        self.lineEditContainer = {}

        for i in range(PutVars.numOfParams):
            currLineEdit = QLineEdit()
            currLineEdit.setText(PutVars.names[i])
            self.lineEditContainer[i] = currLineEdit
            if parameters[i]:
                currLineEdit.setText(parameters[i])
            else:
                currLineEdit.setText(PutVars.defaultValues[i])

            formLayout.addRow(PutVars.names[i], currLineEdit)

        # Setting integer validator for run and shot numbers.
        self.lineEditContainer[PutVars.run].setValidator(QIntValidator())
        self.lineEditContainer[PutVars.shot].setValidator(QIntValidator())

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
        # enumerator class PutVars.

        variables = {}

        for i in range(PutVars.numOfParams):
            variables[i] = self.getValue(i)

        # Checking if validating Integers.
        try:
            variables[PutVars.shot] = int(variables[PutVars.shot])
            variables[PutVars.run] = int(variables[PutVars.run])
        except ValueError as e:
            variables[PutVars.shot] = -1
            variables[PutVars.run] = -1
        return variables


class PutIDS(TcshProcess):
    """Widget representation of the PutIDS functionality. A normal QPushButton
    that encapsulates the PutIDS QThread that does the putting data to the IDS.
    """

    def __init__(self, parent=None):
        super(PutIDS, self).__init__(parent)
        self.cleanupFlag = False
        self.vars = {}
        for i in range(PutVars.numOfParams):
            self.vars[i] = ''

        self.thread = PutIDSQThread(self)
        self.thread.finished.connect(self.cleanUp)

        # Because of mix STD and ERR output from the thread, both channels
        # has to be parsed.
        self.tcsh.stdOutput.connect(self.processTcshOutput)
        self.tcsh.stdErrOutput.connect(self.processTcshOutput)

        self.pushButton = QPushButton(self)
        self.pushButton.setText("Put IDS")
        self.pushButton.clicked.connect(self.putToIDS)
        self.pushButton.setEnabled(ENABLED)

        self.thread.startFlag.connect(self.pushButton.setEnabled)
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.pushButton)
        self.setLayout(layout)

    @Slot(str)
    def setRunDir(self, runDir):
        self.vars[PutVars.runDirPath] = runDir
        super(PutIDS, self).setRunDir(runDir)

    @Slot(str)
    def setUser(self, user):
        self.vars[PutVars.user] = user

    def getUser(self):
        return self.vars[PutVars.user]

    user = Property(str, getUser, setUser)

    @Slot(str)
    def setDevice(self, device):
        self.vars[PutVars.device] = device

    def getDevice(self):
        return self.vars[PutVars.device]

    device = Property(str, getDevice, setDevice)

    @Slot(str)
    def setVersion(self, version):
        self.vars[PutVars.version] = version

    def getVersion(self):
        return self.vars[PutVars.version]

    version = Property(str, getVersion, setVersion)

    @Slot(str)
    def setRun(self, run):
        self.vars[PutVars.run] = run

    def getRun(self):
        return self.vars[PutVars.run]

    runNumber = Property(str, getRun, setRun)

    @Slot(str)
    def setShot(self, shot):
        self.vars[PutVars.shot] = shot

    def getShot(self):
        return self.vars[PutVars.shot]

    shotNumber = Property(str, getShot, setShot)

    def checkParameters(self):
        """Function that checks if all parameter are defined to open an IDS.
        If not all parameters are provided, a QDialog will open and asking for
        other parameters, necessary to open an IDS.

        If you use the GetIDS from a CLI this usually doesn't happen, but if it
        is implemented in a GUI, usually a user will expect some sort of dialog
        to provide the parameters."""

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
            dialog = PutDialog(self)
            dialog.prepareWidgets(self.vars)
            if dialog.exec_():
                self.vars = dialog.on_close()
                return self.checkParameters()
            else:
                # Canceled!
                return False

    @Slot()
    def putToIDS(self):
        if not self.checkParameters():
            self.cleanUp()
            return
        self.pushButton.setEnabled(False)

        # Start the :attr:`tcsh` in the run directory
        self.startTcsh()  # Tcsh started in run directory
        if not self.tcsh.state():
            # Failed to start
            self.cleanUp()

        if not os.access(self.getRunDir() + '/b2mn.dat', os.F_OK | os.R_OK):
            logging.error('No b2mn.dat in this directory!')

        logging.info('Figuring out if the run is coupled or stand alone?')
        # Checking if inpud.dat is in run directory

        if os.access(self.getRunDir() + '/input.dat', os.F_OK):
            COUPLED = True
        else:
            COUPLED = False

        self.tcsh.write('cd %s\n' % self.getRunDir())
        self.tcsh.write('imasdb solps-iter\n')

        cmd = 'b2run '

        if not COUPLED:
            logging.info('Run is standalone')
            cmd += '-s '
        else:
            logging.info('Run is coupled')

        cmd += 'b2_ual_write\n'
        logging.info('Starting %s in %s' % (cmd, self.getRunDir()))
        cmd += 'echo "Cleanup"\n'

        self.tcsh.write(cmd)

    def processTcshOutput(self, msg):
        """First run ``b2_mod_ual_writer``
        """
        if 'IDS write finished' in msg:
            logging.info('b2_ual_write complete.')
            self.cleanupFlag = True

        if 'Cleanup' in msg:
            if not self.cleanupFlag:
                # B2 ual write failed
                logging.error('b2_ual_write failed in %s', self.getRunDir())
                self.pushButton.setEnabled(True)
                self.cleanUp()
            else:
                logging.info('b2_ual_write finished.')
                self.thread.setParameters(self.vars)
                self.thread.start()

    @Slot()
    def cleanUp(self):
        for key in self.vars:
            self.vars[key] = ''


def tarInputFiles(dir_path):
    """Input files for a SOLPS run (B2 and Eirene) are tarballed into a
    tar-string and then encoded with base64 to avoid null terminators.

    Parameters:
        dir_path (str): Path to a SOLPS run from where it collects the input
            files.
    """
    tf = BytesIO()
    tar = tarfile.TarFile(mode='w', fileobj=tf)
    for filename in input_files:
        name = getB2path(dir_path, filename)
        if name:
            os.chdir(dir_path)
            tar.add(name)

    bstring = tf.getvalue()
    bstring = base64.b64encode(bstring).decode()
    return bstring


def getB2path(dir_path, file_name):
    """Returns a path for an input file if it resides in the run directory or
    in the base directory.
    """
    filepath = dir_path + '/' + file_name
    filepath_base = dir_path + '/../baserun/' + file_name
    if os.path.isfile(filepath):
        return file_name

    elif os.path.isfile(filepath_base):
        return '../baserun/' + file_name

    else:
        return ''


class PutIDSQThread(QThread):
    """QThread for storing data to IDS. Note that it gets the attributes
    necessary to open an IDS and create a data entry, from PutIDS instances.

    The threading is required since it takes sometime for everything to be
    written to an IDS so in order avoid from freezing the GUI, QThread is used.
    """

    startFlag = Signal(bool)

    def __init__(self, parent=None):
        super(PutIDSQThread, self).__init__(parent)
        self.vars = {}
        for i in range(PutVars.numOfParams):
            self.vars[i] = None

        self.started.connect(self.on_start)
        self.finished.connect(self.on_finish)

    def setParameters(self, parameters):
        """Function that sets the parameters necessary for accessing IDS.
        """
        for key in parameters:
            self.vars[key] = parameters[key]

    def run(self):
        """Threaded run function that writes the data of the B2 output files
        and input files to the given IDS entry.
        """
        logging.info('Reading files...')
        runDir = self.vars[PutVars.runDirPath]
        code_parameters = tarInputFiles(runDir)
        logging.info('Code parameters read.')
        logging.info('Creating IDS object.')
        ids = PutIDSwrapper(self.vars)
        logging.info('IDS object created.')
        if not ids.connected():
            logging.info('Failed to create IDS entry. Canceling.')
            return
        ids.writeCodeParameters(code_parameters)
        logging.info('Code parameters added.')

        logging.info('Now saving data entry.')
        ids.save()

    @Slot()
    def on_start(self):
        logging.info('Putting to IDS...')
        self.startFlag.emit(False)

    @Slot()
    def on_finish(self):
        logging.info('Finished writing data to IDS.')
        self.startFlag.emit(True)
        # Clear Parameters


class PutIDSwrapper:
    """ A python wrapper that eases the saving of data to an IDS. It is used
    for creating or opening an IDS data entry and then storing data to it. The
    data right now are the electron and ion temperatures, electron density and
    the plasma coordinates.

    Each set of data has its own function on how to write to the IDS.

    Note that for now the function **imas.ids.create_env** is very CPU
    intensive, so first we check whether an IDS with the same address already
    exists. If it does, then the write finishes quickly, otherwise the creation
    of a new entry will take some time.
    """

    def __init__(self, variables):
        """ The constructor creates the IDS database object and then creates
        the data entry."""

        self.vars = variables
        shot = self.vars[PutVars.shot]
        run = self.vars[PutVars.run]
        user = self.vars[PutVars.user]
        device = self.vars[PutVars.device]
        version = self.vars[PutVars.version]

        # Create the IDS database
        self.imas_obj = imas.ids(shot, run, shot, run)

        # See if the entry is already existing
        try:
            self.imas_obj.open_env(user, device, version)
        except Exception as e:
            logging.info('IDS does not exist... Creating IDS')
            # Create data entry
            self.imas_obj.create_env(user, device, version)
        self.state = self.connected()

        if self.state:
            logging.info('Created IDS data entry.')
        else:
            logging.error('Failed to create data entry.')

    def connected(self):
        """Checks whether the data entry has been created."""
        return self.imas_obj.isConnected()

    def writeCodeParameters(self, code_parameters):
        """ Writing code parameters, which is basically tar-balled input files
        for SOLPS run and then encoded with base64 to avoid null terminations.
        """
        logging.info('Writing code parameters.')
        self.imas_obj.edge_profiles.code.parameters = code_parameters

    def save(self):
        """Saves changes to IDS.edge_profiles with the put function.
        """

        if self.state:
            # A data entry has been opened
            # Saving to IDS
            self.imas_obj.edge_profiles.put()
            # Closing the IDS
            self.imas_obj.close()


if __name__ == "__main__":
    from PySide6.QtCore import QCoreApplication

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    root.addHandler(ch)

    Vars = {}

    Help = """
This is used for testing for writing data to IDS. By default the data \
from a run directory will be stored to an IDS with the ID variables you \
provide via CLI.

In order to run put_edge run directory path, shot, run, user, device and \
version must be defined: Example (terminal):

python3 put_edge_ids.py \
--dirpath=/home/ITER/simicg/solps-iter/runs/examples/ITER_2298_Honly_20MW+C+He\
/16151_1.6MW_2.0e19_D=0.4_chi=1.6_standalone \
--shot=1001 --run=1001 --user=%s --device=solps-iter --version=3"""

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "srudvh",
                                   ["dirpath=", "shot=", "run=", "user=",
                                    "device=", "version=", "help"])
        for opt, arg in opts:
            # print opt, arg
            if opt in ("-fp", "--dirpath"):
                Vars[PutVars.runDirPath] = arg
            elif opt in ("-s", "--shot"):
                Vars[PutVars.shot] = int(arg)
            elif opt in ("-r", "--run"):
                Vars[PutVars.run] = int(arg)
            elif opt in ("-u", "--user"):
                Vars[PutVars.user] = arg
            elif opt in ("-t", "--device"):
                Vars[PutVars.device] = arg
            elif opt in ("-v", "--version"):
                Vars[PutVars.version] = arg

            elif opt in ("-h", "--help"):
                logging.info(Help % os.environ['USER'])
                sys.exit()

    except Exception:
        print('Supplied option not recognized!')
        print('For help: -h / --help')
        sys.exit(2)

    if len(Vars) < PutVars.numOfParams:
        print('Not enough variables defined!')
        print('For help: -h / --help')
        sys.exit(2)
    elif len(Vars) > PutVars.numOfParams:
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
    t = PutIDSQThread()
    t.setParameters(Vars)
    t.finished.connect(app.exit)
    t.start()
    sys.exit(app.exec())
