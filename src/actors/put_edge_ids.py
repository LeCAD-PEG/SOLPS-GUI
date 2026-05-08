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

from PySide6.QtCore import Slot, QThread, Property, Signal, QProcess
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

# Optimization output files (added when they exist)
optimization_output_files = [
    'objval.dat',
    'grad.dat',
    'parm_hist1.dat',
    'parm_hist2.dat',
    'parm_hist3.dat',
    'parm_hist4.dat',
    'parm_hist5.dat',
    'cf2.dat',
    'cf3.dat',
    'cf4.dat',
    'cf5.dat',
    'cf6.dat',
    'cf7.dat',
    'cf8.dat',
    'cf9.dat',
    'PETSC-TAO.OUT',
    'b2.optimization.parameters'
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

    user = Property(str, getUser, setUser,
        doc="Database user (can be public)")

    @Slot(str)
    def setDevice(self, device):
        self.vars[PutVars.device] = device

    def getDevice(self):
        return self.vars[PutVars.device]

    device = Property(str, getDevice, setDevice, doc="Database")

    @Slot(str)
    def setVersion(self, version):
        self.vars[PutVars.version] = version

    def getVersion(self):
        return self.vars[PutVars.version]

    version = Property(str, getVersion, setVersion, 
        doc="DB version")

    @Slot(str)
    def setRun(self, run):
        self.vars[PutVars.run] = run

    def getRun(self):
        return self.vars[PutVars.run]

    runNumber = Property(str, getRun, setRun, doc="Pulse")

    @Slot(str)
    def setShot(self, shot):
        self.vars[PutVars.shot] = shot

    def getShot(self):
        return self.vars[PutVars.shot]

    shotNumber = Property(str, getShot, setShot, doc="Shot")

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

        if not os.access(self.getRunDir() + '/b2mn.dat', os.F_OK | os.R_OK):
            logging.error('No b2mn.dat in this directory!')
            self.cleanUp()
            return

        self.pushButton.setEnabled(False)

        logging.info('Starting Python IDS writer directly.')
        self.thread.setParameters(self.vars)
        self.thread.start()

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


def tarInputFiles(dir_path, shot=None, run=None, user=None, device=None):
    """Input files for a SOLPS run (B2 and Eirene) are tarballed into a
    tar-string and then encoded with base64 to avoid null terminators.
    
    This function also includes optimization output files if they exist in 
    the run directory (objval.dat, grad.dat, parm_hist*.dat, cf*.dat, etc.)
    
    If IDS metadata is provided, it updates b2mndr_shot_number, b2mndr_run_number,
    b2mndr_user, and b2mndr_device parameters in b2mn.dat.

    Parameters:
        dir_path (str): Path to a SOLPS run from where it collects the input files.
        shot (int): IDS shot number (optional)
        run (int): IDS run number (optional)
        user (str): IDS user (optional)
        device (str): IDS device (optional)
    """
    tf = BytesIO()
    tar = tarfile.TarFile(mode='w', fileobj=tf, dereference=True)
    
    os.chdir(dir_path)
    
    # Add standard input files
    for filename in input_files:
        name = getB2path(dir_path, filename)
        if name:
            # Special handling for b2mn.dat to add/update IDS metadata parameters
            if filename == 'b2mn.dat' and shot is not None and run is not None:
                import tempfile
                
                logging.info(f'Processing b2mn.dat: shot={shot}, run={run}, user={user}, device={device}')
                temp_fd, temp_path = tempfile.mkstemp(suffix='.dat', text=True)
                try:
                    with os.fdopen(temp_fd, 'w') as temp_file:
                        # Read original b2mn.dat
                        with open(name, 'r') as orig_file:
                            lines = orig_file.readlines()
                        
                        logging.info(f'Read {len(lines)} lines from b2mn.dat')
                        
                        # Track which parameters we've updated
                        updated_shot = False
                        updated_run = False
                        updated_user = False
                        updated_device = False
                        label_line_idx = None
                        
                        # Update existing parameters or track where to insert new ones
                        for i, line in enumerate(lines):
                            if "'b2mndr_shot_number'" in line or '"b2mndr_shot_number"' in line:
                                lines[i] = f"'b2mndr_shot_number'              '{shot}'\n"
                                updated_shot = True
                            elif "'b2mndr_run_number'" in line or '"b2mndr_run_number"' in line:
                                lines[i] = f"'b2mndr_run_number'               '{run}'\n"
                                updated_run = True
                            elif "'b2mndr_user'" in line or '"b2mndr_user"' in line:
                                if user:
                                    lines[i] = f"'b2mndr_user'                    '{user}'\n"
                                updated_user = True
                            elif "'b2mndr_device'" in line or '"b2mndr_device"' in line:
                                if device:
                                    lines[i] = f"'b2mndr_device'                  '{device}'\n"
                                updated_device = True
                            elif '*label' in line.lower() and label_line_idx is None:
                                label_line_idx = i + 1  # Insert after the label value line
                        
                        # If parameters weren't found, add them after the label section
                        logging.info(f'Updated flags: shot={updated_shot}, run={updated_run}, user={updated_user}, device={updated_device}')
                        logging.info(f'Label line index: {label_line_idx}')
                        
                        if not (updated_shot and updated_run and updated_user and updated_device):
                            if label_line_idx is not None:
                                insert_idx = label_line_idx + 1
                                logging.info(f'Inserting IDS parameters at line {insert_idx} (after label)')
                            else:
                                insert_idx = 0
                                logging.warning('Could not find *label in b2mn.dat, inserting at beginning')
                            
                            new_lines = []
                            if not updated_shot:
                                new_lines.append(f"'b2mndr_shot_number'              '{shot}'\n")
                            if not updated_run:
                                new_lines.append(f"'b2mndr_run_number'               '{run}'\n")
                            if not updated_user and user:
                                new_lines.append(f"'b2mndr_user'                    '{user}'\n")
                            if not updated_device and device:
                                new_lines.append(f"'b2mndr_device'                  '{device}'\n")
                            
                            if new_lines:
                                logging.info(f'Adding {len(new_lines)} new IDS parameter lines to b2mn.dat')
                                lines = lines[:insert_idx] + new_lines + lines[insert_idx:]
                            else:
                                logging.info('All IDS parameters already exist or not provided')
                        else:
                            logging.info('All IDS parameters were already present and updated')
                        
                        # Write modified content
                        temp_file.writelines(lines)
                        logging.info(f'Wrote {len(lines)} lines to temporary b2mn.dat')
                    
                    # Add the modified file to tarball
                    tar.add(temp_path, arcname=filename)
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            else:
                tar.add(name)
    
    # Add optimization output files if they exist
    for filename in optimization_output_files:
        if os.path.isfile(filename):
            logging.info(f'Adding optimization file: {filename}')
            tar.add(filename)

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


def readB2output(file_path, file_name, variables):
    """Read the B2 output file and return values for the requested variables.

    Each line starting with ``*cf`` indicates a variable type and name.
    The user provides the variable names to read; results are returned as a
    dictionary keyed by variable name.

    Arguments:
        file_path (str): Run directory path.
        file_name (str): B2 output file name (e.g. ``b2fgmtry``, ``b2fstati``).
        variables (list): Variable names to extract.

    Returns:
        dict: Dictionary mapping variable name to list of float values.
    """
    arrays = {el: [] for el in variables}
    with open(file_path + '/' + file_name, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.startswith('*cf'):
                stripLine = line.strip()
                lastWord = stripLine.split()[-1]
                if lastWord in arrays:
                    splitLine = stripLine.split()
                    ar = arrays[splitLine[-1]]
                    N = int(splitLine[-2])
                    counter = 0
                    while counter < N:
                        line = f.readline().split()
                        counter += len(line)
                        ar += [float(el) for el in line]
    return arrays


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

        # Extract IDS metadata to add to b2mn.dat
        shot = self.vars.get(PutVars.shot)
        run = self.vars.get(PutVars.run)
        user = self.vars.get(PutVars.user)
        device = self.vars.get(PutVars.device)

        logging.info(f'IDS parameters for tarInputFiles: shot={shot}, run={run}, user={user}, device={device}')

        # Check if b2 output files are available for GGD geometry/physics
        b2out = False
        b2statiAr = {}
        b2plasmfAr = {}
        if os.path.exists(runDir + '/b2fgmtry') and \
           (os.path.exists(runDir + '/b2fstati') or
            os.path.exists(runDir + '/b2fplasmf')):
            try:
                coorAr = readB2output(runDir, 'b2fgmtry',
                                      variables=['nx,ny,nncut', 'vxX', 'vxY',
                                                 'cvVx', 'nCi,nCg,nCv,nFc,nVx,nFs,nFt',
                                                 'cvX', 'cvY', 'fcLbl', 'fcCv'])
                logging.info('b2fgmtry read.')
                if os.path.exists(runDir + '/b2fstati'):
                    b2statiAr = readB2output(runDir, 'b2fstati',
                                             variables=['ne', 'te', 'ti'])
                    logging.info('b2fstati read.')
                if os.path.exists(runDir + '/b2fplasmf'):
                    b2plasmfAr = readB2output(runDir, 'b2fplasmf',
                                              variables=['ne', 'te', 'ti',
                                                         'dna0', 'hce0', 'hci0'])
                    logging.info('b2fplasmf read.')
                # Reference case from reference_reg/b2fplasmf
                b2refAr = {}
                refDir = os.path.normpath(os.path.join(runDir, '..', 'reference_reg'))
                if os.path.exists(refDir + '/b2fplasmf'):
                    b2refAr = readB2output(refDir, 'b2fplasmf',
                                           variables=['ne', 'te', 'dna0', 'hce0'])
                    logging.info(f'Reference b2fplasmf read from {refDir}.')
                else:
                    logging.info(f'No reference_reg/b2fplasmf found at {refDir}.')
                b2out = True
            except Exception as e:
                import traceback
                logging.warning(f'Failed to read b2 output files: {e}\n{traceback.format_exc()}')
        else:
            logging.info('No b2 output files found; skipping GGD geometry/physics write.')

        code_parameters = tarInputFiles(runDir, shot=shot, run=run, user=user, device=device)
        logging.info('Code parameters read.')
        logging.info('Creating IDS object.')
        ids = PutIDSwrapper(self.vars)
        logging.info('IDS object created.')
        if not ids.connected():
            logging.info('Failed to create IDS entry. Canceling.')
            return
        ids.writeCodeParameters(code_parameters, run_dir=runDir)
        logging.info('Code parameters added.')

        if b2out:
            try:
                nCi = int(coorAr['nCi,nCg,nCv,nFc,nVx,nFs,nFt'][0])
                nCv = int(coorAr['nCi,nCg,nCv,nFc,nVx,nFs,nFt'][2])
                ids.writeCoordinates(coorAr['vxX'], coorAr['vxY'],
                                     int(coorAr['nx,ny,nncut'][0]),
                                     int(coorAr['nx,ny,nncut'][1]),
                                     [int(x) for x in coorAr['cvVx']])
                logging.info('GGD coordinates written.')
                # ggd[0] <- b2fstati quantities (always attempt first)
                if b2statiAr:
                    ids.writeTe(b2statiAr['te'][:nCv], ggd_index=0)
                    ids.writeTi(b2statiAr['ti'][:nCv], ggd_index=0)
                    ids.writeNe(b2statiAr['ne'][:nCv], ggd_index=0)
                    logging.info('b2fstati: Te, Ti, Ne written to ggd[0].')
                # 1D profiles are read directly from disk by plotProfiles1D (not stored in IDS)
            except Exception as e:
                import traceback
                logging.warning(f'Failed to write GGD data: {e}\n{traceback.format_exc()}')

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

        # Create the IDS database - support both old and new IMAS APIs
        self.new_api = False
        self.imas_obj = None
        
        # Try different IMAS API versions
        try:
            # Try new IMAS API with ids_defs (IMAS >= 3.30.0)
            backend = imas.ids_defs.MDSPLUS_BACKEND
            self.imas_obj = imas.DBEntry(backend, device, shot, run, user)
            self.new_api = True
            logging.info('Using new IMAS API (DBEntry with ids_defs)')
            
            # Try to open existing entry
            try:
                self.imas_obj.open()
                logging.info('Opened existing IDS entry')
            except:
                logging.info('IDS does not exist... Creating IDS')
                self.imas_obj.create()
                
        except (AttributeError, NameError):
            try:
                # Try new IMAS API with imasdef - pass data_version so MDS+
                # looks in the correct versioned directory (e.g. solps-iter/4/)
                backend = imas.imasdef.MDSPLUS_BACKEND
                self.imas_obj = imas.DBEntry(backend, device, shot, run,
                                             user, data_version=version)
                self.new_api = True
                logging.info('Using new IMAS API (DBEntry with imasdef)')
                
                # Try to open existing entry; AL may print errors without
                # raising, so check the return status explicitly
                try:
                    ret = self.imas_obj.open()
                    # Some AL versions return a status tuple (status, ...)
                    status = ret[0] if isinstance(ret, (tuple, list)) else ret
                    if status is not None and status != 0:
                        raise RuntimeError(f'open() returned status {status}')
                    logging.info('Opened existing IDS entry')
                except Exception as e:
                    logging.info(f'IDS does not exist or open failed ({e})... Creating IDS')
                    self.imas_obj.create()
                    
            except (AttributeError, NameError):
                # Fall back to old IMAS API
                try:
                    self.imas_obj = imas.ids(shot, run, shot, run)
                    self.new_api = False
                    logging.info('Using old IMAS API (ids with 4 params)')
                    
                    # See if the entry is already existing
                    try:
                        self.imas_obj.open_env(user, device, version)
                        logging.info('Opened existing IDS entry')
                    except Exception as e:
                        logging.info('IDS does not exist... Creating IDS')
                        # Create data entry
                        self.imas_obj.create_env(user, device, version)
                        
                except (AttributeError, TypeError):
                    # Try old API with 2 params
                    self.imas_obj = imas.ids(shot, run)
                    self.new_api = False
                    logging.info('Using old IMAS API (ids with 2 params)')
                    
                    # See if the entry is already existing
                    try:
                        self.imas_obj.open_env(user, device, version)
                        logging.info('Opened existing IDS entry')
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
        if self.new_api:
            # New API doesn't have isConnected, check if object exists
            return self.imas_obj is not None
        else:
            return self.imas_obj.isConnected()

    def writeCodeParameters(self, code_parameters, run_dir=None):
        """ Writing code parameters, which is basically tar-balled input files
        for SOLPS run and then encoded with base64 to avoid null terminations.
        """
        logging.info('Writing code parameters.')
        
        if self.new_api:
            # New API: create or get IDS
            try:
                # Try to get existing edge_profiles
                edge_profiles = self.imas_obj.get('edge_profiles')
                logging.info('Retrieved existing edge_profiles from IDS')
            except Exception as e:
                # IDS is empty or not writable – create a fresh object
                logging.info(f'Creating new edge_profiles (get failed: {e})')
                edge_profiles = imas.IDSFactory().edge_profiles()
                # Set required ids_properties fields
                edge_profiles.ids_properties.homogeneous_time = 1
                edge_profiles.ids_properties.comment = 'SOLPS-ITER run data'
                logging.info('Initialized ids_properties for new edge_profiles')
            
            edge_profiles.code.parameters = code_parameters
            if run_dir:
                edge_profiles.ids_properties.comment = run_dir  # store runDir for plotProfiles1D
            self.edge_profiles = edge_profiles
        else:
            # Old API: direct access
            self.imas_obj.edge_profiles.code.parameters = code_parameters

    def _get_ep(self):
        """Return the edge_profiles object for modification (new or old API)."""
        if self.new_api:
            return self.edge_profiles
        else:
            return self.imas_obj.edge_profiles

    def writeCoordinates(self, rC, zC, dimR, dimZ, cvVx):
        """Write R, Z coordinates (nodes and cells) to the IDS GGD grid.

        In this IMAS version, grid_ggd[i] directly has ``space`` and
        ``grid_subset`` (no intermediate ``.grid`` sub-object).

        Arguments:
            rC (list): Flattened R-coordinates of nodes (vxX).
            zC (list): Flattened Z-coordinates of nodes (vxY).
            dimR (int): Number of cells in the R direction (nx).
            dimZ (int): Number of cells in the Z direction (ny).
            cvVx (list): Flat cell-to-vertex connectivity list from b2fgmtry
                         (cvVx), 4 entries per cell, 1-based Fortran indices.
        """
        logging.info('Writing GGD coordinates.')
        ep = self._get_ep()

        logging.info(f'edge_profiles grid_ggd length: {len(ep.grid_ggd)}')
        logging.info(f'edge_profiles ggd length: {len(ep.ggd)}')
        logging.info(f'edge_profiles time length: {len(ep.time)}')

        if self.new_api:
            if len(ep.grid_ggd) == 0:
                ep.grid_ggd.resize(1)
            if len(ep.ggd) < 1:
                ep.ggd.resize(1)  # ggd[0] = all physics data
            if len(ep.time) == 0:
                ep.time.resize(1)
                ep.time[0] = 1.0
            ep.ids_properties.homogeneous_time = 1
        else:
            ep.profiles_1d.resize(1)
            ep.ggd.resize(1)
            ep.putNonTimed()
            ep.time.resize(1)
            ep.time[0] = 1.0
            ep.ids_properties.homogeneous_time = 1

        logging.info(f'After resize - grid_ggd length: {len(ep.grid_ggd)}, ggd length: {len(ep.ggd)}')

        # In this IMAS version grid_ggd[i] IS the grid (no .grid sub-object)
        ggrid = ep.grid_ggd[0]
        ggrid.space.resize(1)
        space0 = ggrid.space[0]
        space0.objects_per_dimension.resize(3)

        space0.coordinates_type.resize(2)
        space0.coordinates_type[0] = 4  # R
        space0.coordinates_type[1] = 5  # Z

        num_gridSubsets = 2  # Cells (index 1) and Nodes (index 2)
        ggrid.grid_subset.resize(num_gridSubsets)

        self._writeNodes(ep, rC, zC)
        self._writeCells(ep, dimR, dimZ, cvVx)

    def _writeNodes(self, ep, rC, zC):
        """Write 0D node objects and the Nodes grid subset."""
        ggrid = ep.grid_ggd[0]
        space0 = ggrid.space[0]

        gridSubset_index = 2
        gridSubset_name = 'Nodes'
        gridSubset_dim_index = 1

        num_obj_0D = len(rC)
        dim0 = space0.objects_per_dimension[gridSubset_dim_index - 1]
        dim0.object.resize(num_obj_0D)
        for i in range(num_obj_0D):
            dim0.object[i].nodes.resize(1)
            dim0.object[i].nodes[0] = i
            dim0.object[i].geometry.resize(2)
            dim0.object[i].geometry[0] = rC[i]
            dim0.object[i].geometry[1] = zC[i]

        gsData = ggrid.grid_subset[gridSubset_index - 1]
        gsData.identifier.name = gridSubset_name
        gsData.identifier.index = gridSubset_index
        gsData.element.resize(num_obj_0D)
        for i in range(num_obj_0D):
            gsData.element[i].object.resize(1)
            gsData.element[i].object[0].space = 1
            gsData.element[i].object[0].dimension = gridSubset_dim_index
            gsData.element[i].object[0].index = i + 1

    def _writeCells(self, ep, dimR, dimZ, cvVx):
        """Write 2D cell objects and the Cells grid subset using actual
        cell-to-vertex connectivity read from b2fgmtry (cvVx).

        Arguments:
            ep: edge_profiles IDS object.
            dimR (int): nx — number of cells in radial direction.
            dimZ (int): ny — number of cells in poloidal direction.
            cvVx (list): Flat 1-based cell-to-vertex connectivity (4 per cell).
        """
        ggrid = ep.grid_ggd[0]
        space0 = ggrid.space[0]

        # Total number of cells including guard cells = (nx+2)*(ny+2)
        numCellsX = dimR + 2
        numCellsY = dimZ + 2
        num_obj_2D = numCellsX * numCellsY
        gridSubset_index = 1
        gridSubset_name = 'Cells'
        gridSubset_dim_index = 3

        # cvVx has 4 node indices per cell (Fortran 1-based)
        nodes_per_cell = 4
        if len(cvVx) != num_obj_2D * nodes_per_cell:
            logging.warning(
                f'cvVx length {len(cvVx)} != {num_obj_2D}*{nodes_per_cell}='
                f'{num_obj_2D * nodes_per_cell}; using available data.')
            num_obj_2D = len(cvVx) // nodes_per_cell

        dim2 = space0.objects_per_dimension[gridSubset_dim_index - 1]
        dim2.object.resize(num_obj_2D)
        for i in range(num_obj_2D):
            dim2.object[i].nodes.resize(nodes_per_cell)
            base = i * nodes_per_cell
            for k in range(nodes_per_cell):
                # cvVx is 1-based; store as-is (IDS uses 1-based node indices)
                dim2.object[i].nodes[k] = cvVx[base + k]

        gsData = ggrid.grid_subset[gridSubset_index - 1]
        gsData.identifier.name = gridSubset_name
        gsData.identifier.index = gridSubset_index
        gsData.element.resize(num_obj_2D)
        for i in range(num_obj_2D):
            gsData.element[i].object.resize(1)
            gsData.element[i].object[0].space = 1
            gsData.element[i].object[0].dimension = gridSubset_dim_index
            gsData.element[i].object[0].index = i + 1

    def writeTe(self, te, ggd_index=0):
        """Write electron temperature (Te) to the IDS GGD (Cells grid subset).

        Values are converted from J to eV.
        """
        ep = self._get_ep()
        num_te_values = len(te)
        el = ep.ggd[ggd_index].electrons
        el.temperature.resize(1)
        tePath = el.temperature[0]
        tePath.grid_subset_index = 1  # Cells
        tePath.values.resize(num_te_values)
        for n in range(num_te_values):
            tePath.values[n] = te[n] * 6.242e18  # J -> eV

    def writeTi(self, ti, ggd_index=0):
        """Write ion temperature (Ti) to the IDS GGD (Cells grid subset).

        Values are converted from J to eV.
        """
        ep = self._get_ep()
        num_ti_values = len(ti)
        ion = ep.ggd[ggd_index].ion
        ion.resize(1)
        ion[0].temperature.resize(1)
        tiPath = ion[0].temperature[0]
        tiPath.grid_subset_index = 1  # Cells
        tiPath.values.resize(num_ti_values)
        for n in range(num_ti_values):
            tiPath.values[n] = ti[n] * 6.242e18  # J -> eV

    def writeNe(self, ne, ggd_index=0):
        """Write electron density (Ne) to the IDS GGD (Cells grid subset)."""
        ep = self._get_ep()
        num_ne_values = len(ne)
        elDensity = ep.ggd[ggd_index].electrons.density
        elDensity.resize(1)
        nePath = elDensity[0]
        nePath.grid_subset_index = 1  # Cells
        nePath.values.resize(num_ne_values)
        for n in range(num_ne_values):
            nePath.values[n] = ne[n]

    def writeDperp(self, dna0, nCv, ggd_index=0):
        """Write perpendicular particle diffusion D_perp (dna0) from b2fplasmf.

        Stored in ion[1].density (ion slot 1 is reserved for D_perp).
        """
        ep = self._get_ep()
        ion = ep.ggd[ggd_index].ion
        if len(ion) < 2:
            ion.resize(2)
        ion[1].density.resize(1)
        d = ion[1].density[0]
        d.grid_subset_index = 1  # Cells
        d.values.resize(nCv)
        for n in range(nCv):
            d.values[n] = dna0[n]

    def writeChiE(self, hce0, nCv, ggd_index=0):
        """Write electron heat diffusivity chi_e (hce0) from b2fplasmf.

        Stored in electrons.pressure as a proxy field.
        """
        ep = self._get_ep()
        el = ep.ggd[ggd_index].electrons
        el.pressure.resize(1)
        p = el.pressure[0]
        p.grid_subset_index = 1  # Cells
        p.values.resize(nCv)
        for n in range(nCv):
            p.values[n] = hce0[n]

    def writeChiI(self, hci0, nCv, ggd_index=0):
        """Write ion heat diffusivity chi_i (hci0) from b2fplasmf.

        Stored in ion[0].pressure.
        """
        ep = self._get_ep()
        ion = ep.ggd[ggd_index].ion
        if len(ion) < 1:
            ion.resize(1)
        ion[0].pressure.resize(1)
        p = ion[0].pressure[0]
        p.grid_subset_index = 1  # Cells
        p.values.resize(nCv)
        for n in range(nCv):
            p.values[n] = hci0[n]

    def writeProfiles1D(self, b2plasmfAr, b2statiAr, b2refAr,
                        cvX, cvY, fcLbl, fcCv,
                        nx, ny, nCv, nCi, nFc):
        """Write 1D radial profiles matching MATLAB plot_regression_estimation.m.

        profiles_1d slots:
            [0] optimized OMP   : ne, te, D_perp (ion[0].density), chi_e (electrons.pressure)
            [1] optimized target: ne, te
            [2] reference OMP   : ne, te, D_perp, chi_e
            [3] reference target: ne, te
        """
        ep = self._get_ep()
        ev = 6.242e18  # J -> eV

        # ------------------------------------------------------------------ #
        # 1. OMP cells — mimics cv_intersections(rzomp=[R_in R_out;0 0], gmtry)
        # ------------------------------------------------------------------ #
        # For each iy: outer half (R > mid-R) → min|Z|. Then two post-filters:
        # 1) drop rings with |Z| >> median (guard/wall rings at wrong Z)
        # 2) drop rings with spatial step >> median step (disconnected guards)
        omp_raw = []
        for iy in range(1, ny + 1):
            cells_iy = []
            for ix in range(1, nx + 1):
                flat = ix + (nx + 2) * iy
                if flat < len(cvX):
                    cells_iy.append((flat, cvX[flat], cvY[flat]))
            if not cells_iy:
                continue
            R_vals = [c[1] for c in cells_iy]
            R_mid = (max(R_vals) + min(R_vals)) / 2.0
            outer = [c for c in cells_iy if c[1] > R_mid] or cells_iy
            best = min(outer, key=lambda c: abs(c[2]))
            omp_raw.append((iy, best[0], best[1], best[2]))
        if omp_raw:
            absZ_vals = sorted(abs(r[3]) for r in omp_raw)
            median_absZ = absZ_vals[len(absZ_vals) // 2]
            threshold_Z = max(median_absZ * 10.0, 0.05)
            omp_raw = [r for r in omp_raw if abs(r[3]) <= threshold_Z]
        if len(omp_raw) > 2:
            import math as _math
            steps = [_math.sqrt((omp_raw[k][2]-omp_raw[k-1][2])**2 +
                                (omp_raw[k][3]-omp_raw[k-1][3])**2)
                     for k in range(1, len(omp_raw))]
            med_step = sorted(steps)[len(steps) // 2]
            thresh_step = max(med_step * 4.0, 0.005)
            filtered = [omp_raw[0]]
            for k in range(1, len(omp_raw)):
                if steps[k-1] <= thresh_step:
                    filtered.append(omp_raw[k])
            omp_raw = filtered
        omp_idx = [r[1] for r in omp_raw]
        n_omp = len(omp_idx)
        if n_omp == 0:
            logging.warning('No OMP cells found — skipping profiles_1d.')
            return

        icsep = min(ny // 2, n_omp - 1)   # 0-based; ny//2 is a machine-generic midpoint

        def calc_dist(idx_list, icsep_idx, nc=None):
            """Arc length along ordered cell centres, zeroed at icsep_idx.

            Mimics MATLAB calc_dist(gmtry, cv_list, nc, icsep) exactly:
              - loops over first nc cells (if nc given, else all)
              - reference = midpoint of arc[icsep_idx-1] and arc[icsep_idx]
                (MATLAB: dsref = (ds(iref)+ds(iref-1))/2, iref=icsep 1-based)
            Returns list of distances [mm] with length nc (or len(idx_list)).
            """
            import math
            if nc is None:
                nc = len(idx_list)
            nc = min(nc, len(idx_list))
            arc = [0.0] * nc
            for k in range(1, nc):
                i_prev = idx_list[k - 1]
                i_curr = idx_list[k]
                dR = cvX[i_curr] - cvX[i_prev]
                dZ = cvY[i_curr] - cvY[i_prev]
                arc[k] = arc[k - 1] + math.sqrt(dR*dR + dZ*dZ)
            # MATLAB midpoint reference between icsep_idx-1 and icsep_idx
            if icsep_idx > 0:
                sep_arc = (arc[icsep_idx] + arc[icsep_idx - 1]) / 2.0
            else:
                sep_arc = arc[0]
            return [(a - sep_arc) * 1e3 for a in arc]  # [mm]

        ds_omp = calc_dist(omp_idx, icsep)
        logging.info(f'OMP: {n_omp} cells, icsep={icsep}, ds=[{ds_omp[0]:.2f},{ds_omp[-1]:.2f}] mm')

        # ------------------------------------------------------------------ #
        # 2. Outer target cells — mimics MATLAB fcLbl==-34 loop
        # ------------------------------------------------------------------ #
        # Only include faces where |raw1-raw2|==1 (ix-adjacent = real outer
        # plate cells).  Without this filter, ghost/corner faces appear.
        trg_idx = []
        ds_trg  = []
        if fcLbl and fcCv and nFc > 0:
            seen_trg = set()
            for iFc in range(nFc):
                if int(fcLbl[iFc]) == -34:
                    raw1 = int(fcCv[2 * iFc])
                    raw2 = int(fcCv[2 * iFc + 1])
                    if abs(raw1 - raw2) != 1:   # skip non-ix-adjacent faces
                        continue
                    ic1 = max(raw1, raw2) - 1   # 0-based: max picks the plasma cell (not guard)
                    if ic1 < nCi and ic1 not in seen_trg:
                        seen_trg.add(ic1)
                        trg_idx.append(ic1)
            trg_idx = sorted(trg_idx,
                             key=lambda i: cvX[i] if i < len(cvX) else 0)
            # Find separatrix in target: first SOL cell above omp_sep_iy
            omp_sep_iy = omp_idx[icsep] // (nx + 2)
            trg_stride = nx + 2
            trg_icsep = min(range(len(trg_idx)),
                            key=lambda k: abs(trg_idx[k] // trg_stride - omp_sep_iy - 0.5))
            ds_trg = calc_dist(trg_idx, trg_icsep) if trg_idx else []
            logging.info(f'Outer target: {len(trg_idx)} cells, trg_icsep={trg_icsep}')

        # ------------------------------------------------------------------ #
        # 3. Helper — write one profiles_1d slot
        # ------------------------------------------------------------------ #
        # profiles_1d is time-indexed in IMAS: resize time to 4 slots.
        # Use dummy time values 0.0, 1.0, 2.0, 3.0 (one per slot).
        n_slots = 4
        ep.profiles_1d.resize(n_slots)
        if len(ep.time) < n_slots:
            ep.time.resize(n_slots)
            for t in range(n_slots):
                ep.time[t] = float(t)

        def _write_slot(slot, src, cell_idx, xvals, is_omp):
            if not src or not cell_idx:
                return
            n = len(cell_idx)
            p = ep.profiles_1d[slot]

            # x coordinate [mm from separatrix] stored in rho_pol_norm
            p.grid.rho_pol_norm.resize(n)
            for k, x in enumerate(xvals):
                p.grid.rho_pol_norm[k] = x

            ne_src = src.get('ne', [])
            te_src = src.get('te', [])

            # ne
            if ne_src and max(cell_idx) < len(ne_src):
                p.electrons.density.resize(n)
                for k, i in enumerate(cell_idx):
                    p.electrons.density[k] = ne_src[i]

            # te [eV]
            if te_src and max(cell_idx) < len(te_src):
                p.electrons.temperature.resize(n)
                for k, i in enumerate(cell_idx):
                    p.electrons.temperature[k] = te_src[i] * ev

            if is_omp:
                # D_perp = dna0 species 1 (second block of nCv values)
                dna0 = src.get('dna0', [])
                if dna0 and len(dna0) >= 2 * nCv:
                    dna0_s1 = dna0[nCv:]
                    if max(cell_idx) < len(dna0_s1):
                        if len(p.ion) < 1:
                            p.ion.resize(1)
                        p.ion[0].density.resize(n)
                        for k, i in enumerate(cell_idx):
                            p.ion[0].density[k] = dna0_s1[i]

                # chi_e = hce0 / ne_raw
                # matches MATLAB: hce0 ./ ne ./ 1e19 where ne = ne_raw/1e19
                # => hce0 / (ne_raw/1e19) / 1e19 = hce0 / ne_raw
                hce0 = src.get('hce0', [])
                if hce0 and ne_src and max(cell_idx) < len(hce0):
                    p.electrons.pressure.resize(n)
                    for k, i in enumerate(cell_idx):
                        ne_v = ne_src[i]
                        p.electrons.pressure[k] = (hce0[i] / ne_v
                                                    if ne_v != 0 else 0.0)

            logging.info(f'profiles_1d[{slot}] written ({n} cells)')

        optimized = b2plasmfAr if b2plasmfAr else b2statiAr

        _write_slot(0, optimized, omp_idx, ds_omp, True)   # optimized OMP
        _write_slot(1, optimized, trg_idx, ds_trg, False)  # optimized target
        _write_slot(2, b2refAr,  omp_idx, ds_omp, True)   # reference OMP
        _write_slot(3, b2refAr,  trg_idx, ds_trg, False)  # reference target

    def save(self):
        """Saves changes to IDS.edge_profiles with the put function.
        """

        if self.state:
            if self.new_api:
                try:
                    self.imas_obj.put(self.edge_profiles)
                    logging.info('edge_profiles saved with put().')
                except Exception as e:
                    # put() deletes existing data first; if the MDS+ tree was
                    # created by b2_ual_write without ids_properties, delete
                    # fails with "Node Not Found". Close and recreate the entry
                    # so we get a clean tree, then put again.
                    logging.warning(f'put() failed ({e}). Recreating entry and retrying.')
                    try:
                        self.imas_obj.close()
                    except Exception:
                        pass
                    try:
                        self.imas_obj.create()
                        self.imas_obj.put(self.edge_profiles)
                        logging.info('edge_profiles saved after recreating entry.')
                    except Exception as e2:
                        logging.error(f'put() after recreate also failed: {e2}')
                if hasattr(self.imas_obj, 'close'):
                    try:
                        self.imas_obj.close()
                    except Exception:
                        pass
            else:
                self.imas_obj.edge_profiles.put()
                if hasattr(self.imas_obj, 'close'):
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
        logging.info(f'Command line arguments: {sys.argv[1:]}')
        opts, args = getopt.getopt(sys.argv[1:],
                                   "srudvh",
                                   ["dirpath=", "shot=", "run=", "user=",
                                    "device=", "version=", "help"])
        logging.info(f'Parsed options: {opts}')
        for opt, arg in opts:
            # print opt, arg
            logging.info(f'Processing option: {opt} = {arg}')
            if opt in ("-fp", "--dirpath"):
                Vars[PutVars.runDirPath] = arg
                logging.info(f'Set runDirPath = {arg}')
            elif opt in ("-s", "--shot"):
                Vars[PutVars.shot] = int(arg)
                logging.info(f'Set shot = {arg}')
            elif opt in ("-r", "--run"):
                Vars[PutVars.run] = int(arg)
                logging.info(f'Set run = {arg}')
            elif opt in ("-u", "--user"):
                Vars[PutVars.user] = arg
                logging.info(f'Set user = {arg}')
            elif opt in ("-d", "-t", "--device"):  # Fixed: use -d not -t
                Vars[PutVars.device] = arg
                logging.info(f'Set device = {arg}')
            elif opt in ("-v", "--version"):
                Vars[PutVars.version] = arg
                logging.info(f'Set version = {arg}')

            elif opt in ("-h", "--help"):
                logging.info(Help % os.environ['USER'])
                sys.exit()

    except Exception as e:
        print(f'Supplied option not recognized: {e}')
        print('For help: -h / --help')
        sys.exit(2)

    logging.info(f'Collected {len(Vars)} variables: {Vars}')
    logging.info(f'Required: {PutVars.numOfParams} parameters')
    
    if len(Vars) < PutVars.numOfParams:
        print(f'Not enough variables defined! Got {len(Vars)}, need {PutVars.numOfParams}')
        print(f'Missing variables: {[PutVars.names[i] for i in range(PutVars.numOfParams) if i not in Vars]}')
        print('For help: -h / --help')
        sys.exit(2)
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
