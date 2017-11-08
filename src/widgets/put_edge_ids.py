#! /usr/bin/env python
#Python 3.5
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

try:
    import BytesIO
except Exception as e:
    from io import BytesIO

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


import getopt
import logging
import os
import tarfile
import base64

from PyQt5.QtCore import (pyqtSlot, Qt, QSize, QThread, pyqtProperty,
                          pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit,
                             QGridLayout, QLabel, QDialogButtonBox,
                             QPushButton, QWidget)
from PyQt5.QtGui import QIntValidator


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


class PutIDS(QWidget):
    """Widget representation of the PutIDS functionality. A normal QPushButton
    that encapsulates the PutIDS QThread that does the putting data to the IDS.
    """

    emitMessage = pyqtSignal(str)
    def __init__(self, parent=None):
        super(PutIDS, self).__init__(parent)
        self._rundir = ''
        self._user = ''
        self._shot = ''
        self._device = ''
        self._version = ''
        self._run = ''

        self.thread = PutIDSQThread(self)
        self.thread.finished.connect(self.cleanUp)

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


    @pyqtSlot(str)
    def setRunDir(self, rundir):
        self._rundir = rundir

    def getRunDir(self):
        return self._rundir

    runDir = pyqtProperty(str, getRunDir, setRunDir)

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

    def checkParameters(self):
        """Function that checks if all parameter are defined to open an IDS.
        If not all parameters are provided, a QDialog will open and asking for
        other parameters, necessary to open an IDS.

        If you use the GetIDS from a CLI this usually doesn't happen, but if it
        is implemented in a GUI, usually a user will expect some sort of dialog
        to provide the parameters."""

        if self._shot and self._run and self._user and self._device and \
           self._version and self._rundir:
            return True
        else:
            logging.warning("Not all parameters are specified!")
            dialog = PutDialog(self)
            dialog.prepareWidgets(shot=self._shot, run=self._run,
                                  user=self._user, device=self._device,
                                  version=self._version, path=self._rundir)

            if dialog.exec_():
                self._shot, self._run, self._user, self._device, \
                  self._version, self._rundir = dialog.on_close()
                return self.checkParameters()
            else:
                logging.warning("Dialog canceled, not enough parameters.")
                return False

    @pyqtSlot()
    def putToIDS(self):
        if not self.checkParameters():
            self.cleanUp()
            return

        self.thread.setParameters(self._rundir, int(self._run),
                                  int(self._shot), self._device, self._version,
                                  self._user)
        self.thread.start()

    @pyqtSlot()
    def cleanUp(self):
        self._rundir = ''
        self._user = ''
        self._shot = ''
        self._device = ''
        self._version = ''
        self._run = ''


class PutDialog(QDialog):
    """Dialog Demanding the shot, run, name and device for getting the data
    from IDS.
    """

    def __init__(self, parent=None):
        super(PutDialog, self).__init__(parent)

    def prepareWidgets(self, shot='1001', run='1001', user=os.getenv('USER'),
                       device='solps-iter', version='3',
                       title='Put IDS', path=os.path.expanduser('~')):
        self.main_layout = QGridLayout(self)
        self.setWindowTitle(title)

        self.main_layout.addWidget(QLabel('SHOT'), 0, 0, Qt.AlignLeft)
        shot = QLineEdit(shot)
        shot.setValidator(QIntValidator())
        self.main_layout.addWidget(shot, 0, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('RUN'), 1, 0, Qt.AlignLeft)
        run = QLineEdit(run)
        run.setValidator(QIntValidator())
        self.main_layout.addWidget(run, 1, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('USER'), 2, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit(os.getenv('USER')), 2, 1,
                                   Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('DEVICE'), 3, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit('solps-iter'),
                                   3, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('VERSION'), 4, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit('3'), 4, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('RUN PATH'), 5, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit(path), 5, 1, Qt.AlignCenter)

        # Adding the Ok and Cancel button.
        dialog_button_box = QDialogButtonBox()
        dialog_button_box.setStandardButtons(QDialogButtonBox.Ok |
                                             QDialogButtonBox.Cancel)
        dialog_button_box.accepted.connect(self.accept)
        dialog_button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(dialog_button_box, 6, 1)

    def sizeHint(self):
        return QSize(100, 100)

    def on_close(self):
        """ If the ``OK`` button was clicked then this function should be
        called to process the input widgets and return it's values.

        Note that there is a run number and a **run**. The run number is a
        number but a **run** specifies a SOLPS case.

        Returns:
            SHOT (int): The shot number for a SOLPS case.
            RUN (int): The run number for a SOLPS case.
            USER (str): The user name for a SOLPS case.
            DEVICE (str): The device name for a SOLPS case.
            VERSION (str): The version of IMAS.
        """
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
        PATH = self.main_layout.itemAt(11).widget().text()

        return SHOT, RUN, USER, DEVICE, VERSION, PATH


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


def readB2output(file_path, file_name, variables):
    """This function reads the B2 output file and according to input variables
    it returns values for those variables.

    The way the file is written is that every line that starts with **\*cf**,
    tells us two things, the type of the variable and the name of the variable.

    Therefore instead of writing numerous functions for reading specific
    variables, the user needs only provide which variables needs to be read
    from the output file and the result comes in the form of a dictionary, with
    the variable names being the keys for arrays.

    Arguments:
        file_path (str): Run directory.
        file_name (str): b2output file name.
        variables (array): Array of variables to read from the b2output file.

    Returns:
        arrays (dict): A dictionary containing the values read from the
          b2output file for each variable in the array variables.
    """

    arrays = {el: [] for el in variables}
    with open(file_path + '/' + file_name, 'r') as f:

        while 1:
            line = f.readline()
            if not line:
                break

            if line.startswith('*cf'):
                stripLine = line.strip()

                if any([stripLine.endswith(key) for key in arrays]):
                    splitLine = stripLine.split()
                    ar = arrays[splitLine[-1]]

                    N = int(splitLine[-2])

                    counter = 0
                    while counter < N:
                        line = f.readline().split()
                        counter += len(line)
                        ar += [float(el) for el in line]
                else:
                    continue

    return arrays


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

    def __init__(self, user, device, shot, run, version):
        """ The constructor creates the IDS database object and then creates
        the data entry."""

        self.run = run
        self.shot = shot
        self.user = user
        self.device = device
        self.version = version
        # Create the IDS database
        self.imas_obj = imas.ids(shot, run, shot, run)

        # See if the entry is already existing
        self.imas_obj.open_env(user, device, version)
        if not self.connected():
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

    def basicInit(self):
        """ Basic IDS space allocation.
        """
        self.imas_obj.edge_profiles.profiles_1d.resize(1)
        self.imas_obj.edge_profiles.ggd.resize(1)
        self.imas_obj.edge_profiles.putNonTimed()
        self.imas_obj.edge_profiles.time.resize(1)
        self.imas_obj.edge_profiles.time[0] = 1
        self.imas_obj.edge_profiles.ids_properties.homogeneous_time = 1

    def writeDescription(self, msg=''):
        """Writing simple description to IDS."""

        grid_description = "IDS:" + " shot=" + str(self.shot) + " run=" + \
                           str(self.run) + " user=" + str(self.user) + \
                           " device=" + str(self.device) + \
                           " version=" + str(self.version) + msg
        # Put IDS grid description
        self.imas_obj.edge_profiles.ggd[0].grid.identifier.description = \
            grid_description

    def writeCodeParameters(self, code_parameters):
        """ Writing code parameters, which is basically tar-balled input files
        for SOLPS run and then encoded with base64 to avoid null terminations.
        """
        logging.info('Writing code parameters.')
        self.imas_obj.edge_profiles.code.parameters = code_parameters

    def writeCoordinates(self, rC, zC, dimR, dimZ):
        """ Writing R, Z coordinates to IDS. ``Coordinates`` are stored in
        **Nodes** and the ``cells`` are storred in **Cells**.
        The functions used for this are **writeNodes** and **writeCells**.
        """
        logging.info('Writing coordinates.')
        grid = self.imas_obj.edge_profiles.ggd[0].grid
        grid.space.resize(1)
        # Set (IDS substructure shortcut variable) space0
        space0 = grid.space[0]
        space0.objects_per_dimension.resize(3)  # Allocation

        num_gridSubsets = 2 # Number of grid subsets to write (Cells and Nodes)

        space0.coordinates_type.resize(2)
        space0.coordinates_type[0] = 4  # R
        space0.coordinates_type[1] = 5  # Z

        # Allocating grid subsets. 2 are allocated for Nodes and Cells
        grid.grid_subset.resize(num_gridSubsets)

        self.writeNodes(rC, zC)
        self.writeCells(dimR, dimZ)

    def writeNodes(self, rC, zC):
        """Writes points (0D elements) to Nodes inside the IDS.
        """
        logging.info('Writing nodes.')
        # -- Put DATA FOR GRID SUBSET "Nodes" --
        # (grid subset index: 2, objects forming the grid subset: nodes, 0D)
        # Note:  All indices must be put in Fortran index notation
        # (starting with 1), not in C++/python index notation(starts with 0)!
        # So in our case: Python_Index == Fortran_Index -1 !

        gridSubset_index = 2    # grid subset index of grid subset Nodes
                                # (Indexing of grid subsets follows the ITM CPO
                                # edge examples :
                                # shot: 1, run:1, # device: iter; and
                                # shot: 16151, run: 1000; device: aug
        gridSubset_name = "Nodes"
        gridSubset_dim_index = 1 # Grid subset Nodes consists of
                                 # points -> 0D objects -> dimension index = 1
                                 # (edges -> 1D objects -> dimension index = 2
                                 # cells  -> 2D objects -> dimension index = 3)
        grid = self.imas_obj.edge_profiles.ggd[0].grid
        space0 = grid.space[0]
        num_obj_0D = len(rC)  # Number of nodes (len(rC) == len(zC))
                              # have 2D coordinates, P(x,y)
        # Write all available 0D objects (all of them form the grid subset
        # Nodes
        # Set (IDS substructure shortcut variable) dim0
        dim0 = space0.objects_per_dimension[gridSubset_dim_index - 1]
        dim0.object.resize(num_obj_0D)
        for i in range(num_obj_0D):
            dim0.object[i].nodes.resize(1)
            dim0.object[i].nodes[0] = i
            dim0.object[i].geometry.resize(2)
            dim0.object[i].geometry[0] = rC[i]
            dim0.object[i].geometry[1] = zC[i]

        # Set(IDS substructure shortcut variable) gridSubsetBaseData
        gridSubsetBaseData = grid.grid_subset[gridSubset_index - 1]
        # Put base grid subset data/parameters (name, index)
        gridSubsetBaseData.identifier.name = gridSubset_name
        gridSubsetBaseData.identifier.index = gridSubset_index
        # Put grid subset element and element object data

        # Providing index to elements that point into a Node.
        gridSubsetBaseData.element.resize(num_obj_0D)
        for i in range(num_obj_0D):
            gridSubsetBaseData.element[i].object.resize(1)
            gridSubsetBaseData.element[i].object[0].space = 0 + 1
            gridSubsetBaseData.element[i].object[0].dimension = \
                gridSubset_dim_index
            gridSubsetBaseData.element[i].object[0].index = i + 1

    def writeCells(self, dimR, dimZ):
        """Writes cells (2D elements) to Cells inside the IDS.
        """
        logging.info('Writing cells.')
        # -- Put DATA FOR GRUD SUBSET "Cells"
        # (grid subset index: 1, objects forming the grid subset: cells, 2D)
        grid = self.imas_obj.edge_profiles.ggd[0].grid
        space0 = grid.space[0]
        numCellsX = dimR + 2
        numCellsY = dimZ + 2
        num_cells = numCellsX * numCellsY
        num_obj_2D = num_cells
        gridSubset_index = 1
        gridSubset_name = "Cells"
        gridSubset_dim_index = 3

        # Write all available 2D objects (all of them form the grid subset
        # Cells
        dim2 = space0.objects_per_dimension[gridSubset_dim_index - 1]
        dim2.object.resize(num_obj_2D)
        for i in range(num_obj_2D):
            dim2.object[i].nodes.resize(4)
        Id = 1  # Cell ID.
        for j in range(numCellsY):
            for i in range(numCellsX):
                dim2.object[Id - 1].nodes[0] = Id + 0 * numCellsX * numCellsY
                dim2.object[Id - 1].nodes[1] = Id + 1 * numCellsX * numCellsY
                dim2.object[Id - 1].nodes[2] = Id + 3 * numCellsX * numCellsY
                dim2.object[Id - 1].nodes[3] = Id + 2 * numCellsX * numCellsY
                Id += 1

        # Set (IDS substructure shortcut variable) subgridDaseData for
        # Cells grid subset
        gridSubsetBaseData = grid.grid_subset[gridSubset_index - 1]
        # Put base grid subset data/parameters (name, index)
        gridSubsetBaseData.identifier.name = gridSubset_name
        gridSubsetBaseData.identifier.index = gridSubset_index
        # Put grid subset element and element object data
        gridSubsetBaseData.element.resize(num_obj_2D)
        for i in range(num_obj_2D):
            element = gridSubsetBaseData.element[i]
            element.object.resize(1)
            element.object[0].space = 0 + 1
            element.object[0].dimension = gridSubset_dim_index
            element.object[0].index = i + 1

    def writeTe(self, te):
        """Writes the electron temperature to the IDS. These values colors the
        cells.
        """
        num_te_gridSubset = 1
        num_te_values = len(te)
        el = self.imas_obj.edge_profiles.ggd[0].electrons
        el.temperature.resize(num_te_gridSubset)
        tePath = el.temperature[num_te_gridSubset - 1]
        tePath.grid_subset_index = 1  # gridSubset_index for Cells.
        tePath.values.resize(num_te_values)
        for n in range(num_te_values):
            # convert to eV (1 J = 6.242e18 eV)
            tePath.values[n] = te[n] *(6.242e18)

    def writeTi(self, ti):
        """Writes the ion temperature to the IDS. These values colors the the
        cells.
        """
        num_ti_gridSubset = 1
        num_ti_values = len(ti)
        num_ti_species = 1  # Number of ion species, as in
                            # number of different ion charges.
        ion_specie = 1
        # Ion specie is linked with the ion density of each ion charge,
        # as ion temperature is taken as the same for all ion charges.
        ion = self.imas_obj.edge_profiles.ggd[0].ion
        ion.resize(num_ti_species)
        ion[ion_specie - 1].temperature.resize(num_ti_gridSubset)
        tiPath = ion[ion_specie - 1].temperature[num_ti_gridSubset - 1]
        tiPath.grid_subset_index = 1  # gridSubset_index for Cells.
        tiPath.values.resize(num_ti_values)
        for n in range(num_ti_values):
            # convert to eV (1 J = 6.242e18 eV)
            tiPath.values[n] = ti[n] * (6.242e18)

    def writeNe(self, ne):
        """Writes electron density to the IDS.
        """
        # PUT VALUES for "Cells" grid subset
        # Put ne (electron density)
        num_ne_gridSubset = 1
        num_ne_values = len(ne)
        elDensity = self.imas_obj.edge_profiles.ggd[0].electrons.density
        elDensity.resize(num_ne_gridSubset)
        nePath = elDensity[num_ne_gridSubset - 1]
        nePath.grid_subset_index = 1  # gridSubset_index for Cells.
        nePath.values.resize(num_ne_values)
        for n in range(num_ne_values):
            nePath.values[n] = ne[n]

    def save(self):
        """Saves changes to IDS.edge_profiles with the put function.
        """

        if self.state:
            # A data entry has been opened
            # Saving to IDS
            self.imas_obj.edge_profiles.put()
            # Closing the IDS
            self.imas_obj.close()


class PutIDSQThread(QThread):
    """QThread for storing data to IDS. Note that it gets the attributes
    necessary to open an IDS and create a data entry, from PutIDS instances.

    The threading is required since it takes sometime for everything to be
    written to an IDS so in order avoid from freezing the GUI, QThread is used.

    The `push_button` is a widget that is passed to the thread, for when the
    thread is working that the button should be disabled and then enabled after
    it's done.

    The `status_bar` is a StatusBar widget, part of the QMainWindow and is used
    to send messages about the state of Putting IDS.
    """

    startFlag = pyqtSignal(bool)

    def __init__(self, dirpath='', run='', shot='', device='', version='',
                 user='', parent=None):
        super(PutIDSQThread, self).__init__(parent)
        self.setParameters(dirpath, run, shot, device, version, user)
        self.started.connect(self.on_start)
        self.finished.connect(self.on_finish)

        self.push_button = None
        self.status_bar = None

    def setParameters(self, dirpath, run, shot, device, version, user):
        """ Setting the parameters for the IDS data entry.
        """
        self.rundir = dirpath
        self.runNumber = run
        self.shot = shot
        self.device = device
        self.version = version
        self.user = user

    def run(self):
        """Threaded run function that writes the data of the B2 output files
        and input files to the given IDS entry.
        """
        logging.info('Reading files...')
        b2out = False
        if os.path.exists(self.rundir + '/' + 'b2fgmtry') and \
           os.path.exists(self.rundir + '/' + 'b2fstati'):
            coorAr = readB2output(self.rundir, 'b2fgmtry',
                                  variables=['nx,ny', 'crx', 'cry'])
            logging.info('B2fmtry read.')
            tempAr = readB2output(self.rundir, 'b2fstati',
                                  variables=['ne', 'te', 'ti'])
            logging.info('B2fstati read.')
            b2out = True
        else:
            logging.info('No b2ouput files found, skipping writing'
                                  ' output files to IDS.')

        code_parameters = tarInputFiles(self.rundir)
        logging.info('Code parameters read.')
        logging.info('Creating IDS object.')
        ids = PutIDSwrapper(self.user, self.device, self.shot, self.runNumber,
                            self.version)
        logging.info('IDS object created.')
        if not ids.connected():
            logging.info('Failed to create IDS entry. Canceling.')
            return
        ids.basicInit()
        logging.info('Basic IDS initialization done.')
        ids.writeDescription(' directory: ' + self.rundir)
        logging.info('Description added.')
        ids.writeCodeParameters(code_parameters)
        logging.info('Code parameters added.')

        if b2out:
            ids.writeCoordinates(coorAr['crx'], coorAr['cry'],
                                 int(coorAr['nx,ny'][0]),
                                 int(coorAr['nx,ny'][1]))
            logging.info('Coordinates written added.')
            ids.writeTe(tempAr['te'])
            ids.writeTi(tempAr['ti'])
            ids.writeNe(tempAr['ne'])
            logging.info('Te, Ti and Ne written.')
        logging.info('Now saving data entry.')
        ids.save()

    @pyqtSlot()
    def on_start(self):
        logging.info('Putting to IDS...')
        self.startFlag.emit(False)

    @pyqtSlot()
    def on_finish(self):
        logging.info('Finished writing data to IDS.')
        self.startFlag.emit(True)
        # Clear Parameters



if __name__ == "__main__":
    # For launching python script directly from treminal with python command
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "srudvh",
                                   ["dirpath=", "shot=", "run=", "user=",
                                    "device=", "version=", "help"])
        for opt, arg in opts:
            #print opt, arg
            if opt in ("-fp", "--dirpath"):
                dirpath = arg
            elif opt in ("-s", "--shot"):
                shot = int(arg)
            elif opt in ("-r", "--run"):
                run = int(arg)
            elif opt in ("-u", "--user"):
                user = arg
            elif opt in ("-t", "--device"):
                device = arg
            elif opt in ("-v", "--version"):
                version = arg

            elif opt in ("-h", "--help"):
                print("In order to run put_edge file path, shot, run, user,"
                      "device and version variables must be defined."
                      "Example (terminal): "
                      "python3 put_edge_ids.py "
                      "--dirpath=/home/ITER/simicg/RUNS/demo/2171/baserun "
                      "--shot=1001 --run=1001 --user=simicg "
                      "--device=solps-iter "
                      "--version=3")
                sys.exit()

    except Exception:
        print('Supplied option not recognized!')
        print('For help: -h / --help')
        sys.exit(2)

    app = QApplication(sys.argv)
    t = PutIDSQThread(dirpath, run, shot, device, version, user)
    t.finished.connect(app.exit)
    t.start()
    sys.exit(app.exec_())
