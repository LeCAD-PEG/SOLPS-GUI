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
except:
    from io import BytesIO

try:
    import imas
except ImportError as e:
    pass


import getopt
import sys
import os
import tarfile
import base64

from PyQt5.QtCore import pyqtSlot, Qt, QSize, QThread
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QLineEdit,
                             QGridLayout, QLabel, QDialogButtonBox,
                             QPushButton)
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


class PutDialog(QDialog):
    """Dialog Demanding the shot, run, name and device for getting the data
    from IDS.
    """

    def __init__(self, parent=None, title='Get IDS'):
        super(PutDialog, self).__init__(parent)

    def prepareWidgets(self, shot='1001', run='1001', user=os.getenv('USER'),
                       machine='solps-iter', version='3',
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

        self.main_layout.addWidget(QLabel('MACHINE'), 3, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit('solps-iter'),
                                   3, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('VERSION'), 4, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit('3'), 4, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('PATH'), 4, 0, Qt.AlignLeft)
        self.main_layout.addWidget(path, 4, 1, Qt.AlignCenter)

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
        # Returning the values
        # SHOT, RUN, USER, MACINE, VERSION, run_name exclusively.
        try:
            SHOT = int(self.main_layout.itemAt(1).widget().text())
            RUN = int(self.main_layout.itemAt(3).widget().text())
        except ValueError as e:
            SHOT = -1
            RUN = -1

        USER = self.main_layout.itemAt(5).widget().text()
        MACHINE = self.main_layout.itemAt(7).widget().text()
        VERSION = self.main_layout.itemAt(9).widget().text()
        RUN_NAME = self.main_layout.itemAt(11).widget().text()

        return SHOT, RUN, USER, MACHINE, VERSION, RUN_NAME


class PutIDS(QThread):

    def __init__(self, parent=None):
        super(PutIDS, self).__init__(parent)
        self.prepare_input()

    def prepare_input(self):
        parent = self.parent()
        self.dialog = PutDialog(parent)

    def start(self):
        if self.dialog.exec_(self):
            SHOT, RUN, USER, MACHINE, VERSION, RUN_NAME = \
                self.dialog.on_close()


def tarInputFiles(dir_path):
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
    filepath = dir_path + '/' + file_name
    filepath_base = dir_path + '/../baserun/' + file_name
    if os.path.isfile(filepath):
        return file_name

    elif os.path.isfile(filepath_base):
        return '../baserun/' + file_name

    else:
        return ''

def readB2fgmtry(file_path):
    # Read geometry from file b2fgmtry (x and y coordinates of nodes)
    # and insert them into array for later use
    if file_path == '':
        return [], [], [], []

    crx = []
    cry = []

    found_nxyx  = 0
    found_crx   = 0
    found_cry   = 0
    with open(file_path + "/b2fgmtry", 'r') as infile:
        for line in infile:
            lineSplit = line.split()    #line split in form
                                        # ['*cf:', 'int', '2', 'nx,ny']
            if len(lineSplit) >= 4:
                if lineSplit[3] == "nx,ny":
                    found_nxyx = 1
                    continue
            if (found_nxyx == 1):
                nx = int(lineSplit[0])
                ny = int(lineSplit[1])
                found_nxyx = 0

            if (found_crx == 1 and found_cry == 0):
            #start writing coorindates between 'crx' and next 'cf*:' to crx array
                for j in range(len(lineSplit)):
                    if lineSplit[j] == "*cf:":
                        found_crx = 0
                        found_cry = 0
                        break
                    else:
                        crx.append(float(lineSplit[j].split('E')[0]) * \
                                   pow(10, int(lineSplit[j].split('E')[1])))
            if (found_crx == 0 and found_cry == 1):
            #start writing coorindates between 'cry' and next 'cf*:' to cry array
                for j in range(len(lineSplit)):
                    if lineSplit[j] == "*cf:":
                        found_crx = 0
                        found_cry = 0
                        break
                    else:
                        cry.append(float(lineSplit[j].split('E')[0]) * \
                                   pow(10, int(lineSplit[j].split('E')[1])))
            for i in range(len(lineSplit)):
                if lineSplit[i] == "crx":
                    found_crx = 1
                    found_cry = 0
                    break
                if lineSplit[i] == "cry":
                    found_crx = 0
                    found_cry = 1
                    break
    print("nx: %d | ny: %d" % (nx,ny))

    return crx, cry, nx, ny

def readB2fstati(file_path):
    # Reading values from file b2fstati
    # (electron density (ne), electron temperature(te), ion temperature(ti))
    # and inserting them into array for later use

    ne = []
    te = []
    ti = []

    if file_path == '':
        return ne, te, ti

    found_ne = 0
    found_te = 0
    found_ti = 0

    with open(file_path + "/b2fstati", 'r') as infile:
        for line in infile:
            lineSplit = line.split()    #line split in form
                                        # ['*cf:', 'int', '2', 'nx,ny']
            if (found_ne == 1 and found_te == 0 and found_ti == 0):
            #start writing coorindates between 'ne' and next 'cf*:' to ne array
                for j in range(len(lineSplit)):
                    if lineSplit[j] == "*cf:":
                        found_ne = 0
                        found_te = 0
                        found_ti = 0
                        break
                    else:
                        ne.append(float(lineSplit[j].split('E')[0]) * \
                                  pow(10, int(lineSplit[j].split('E')[1])))
            if (found_ne == 0 and found_te == 1 and found_ti == 0):
            #start writing coorindates between 'te' and next 'cf*:' to te array
                for j in range(len(lineSplit)):
                    if lineSplit[j] == "*cf:":
                        found_ne = 0
                        found_te = 0
                        found_ti = 0
                        break
                    else:
                        te.append(float(lineSplit[j].split('E')[0]) * \
                                  pow(10, int(lineSplit[j].split('E')[1])))
            if (found_ne == 0 and found_te == 0 and found_ti == 1):
            # Write coorindates between 'ti' and next 'cf*:' to ti array
                for j in range(len(lineSplit)):
                    if lineSplit[j] == "*cf:":
                        found_ne = 0
                        found_te = 0
                        found_ti = 0
                        break
                    else:
                        ti.append(float(lineSplit[j].split('E')[0]) * \
                                  pow(10, int(lineSplit[j].split('E')[1])))
            for i in range(len(lineSplit)):
                if lineSplit[i] == "ne":
                    found_ne = 1
                    found_te = 0
                    found_ti = 0
                    break
                if lineSplit[i] == "te":
                    found_ne = 0
                    found_te = 1
                    found_ti = 0
                    break
                if lineSplit[i] == "ti":
                    found_ne = 0
                    found_te = 0
                    found_ti = 1
                    break
    return ne, te, ti

def B2toIDS(shot, run, user, device, version, xc, yc, nx, ny, ne, te, ti,
            code_paramaters, dirpath):
    # Write previously found data in b2fgmtry and b2fstati to IDS database
    print('Writing IDS: ')
    time = 1
    interp = 1

    # --Create IDS database--
    imas_obj = imas.ids(shot, run, shot, run)

    # imas_obj.create()  # Create the data entry
    imas_obj.create_env(user, device, version)

    if imas_obj.isConnected():
        print('Creation of data entry OK!')
    else:
        print('Creation of data entry FAILED!')
        sys.exit()

    # --Basic IDS space allocation--
    imas_obj.edge_profiles.profiles_1d.resize(1)
    imas_obj.edge_profiles.ggd.resize(1)
    imas_obj.edge_profiles.putNonTimed()
    imas_obj.edge_profiles.time.resize(1)
    imas_obj.edge_profiles.time[0] = 1
    imas_obj.edge_profiles.ids_properties.homogeneous_time = 1

    # Writing code parameters
    imas_obj.edge_profiles.code.parameters = code_paramaters
    # Homogeneous time: Synchronised data over same time array
    if xc and yc and nx and ny and ne and te and ti:
        # Set IDS grid description
        grid_description = "This is IDS" + \
            " shot=" + str(shot) + " run=" + str(run) + " user=" + str(user) + \
            " device=" + str(device) + " version=" + str(version) + \
            " written by put_edge_ids using b2fgmtry and b2fstati files found " +\
            "in directory" + dirpath + "."
        # Put IDS grid description
        imas_obj.edge_profiles.ggd[0].grid.identifier.description = grid_description
        imas_obj.edge_profiles.ggd[0].grid.space.resize(1)
        # Set (IDS substructure shortcut variable) space0
        space0 = imas_obj.edge_profiles.ggd[0].grid.space[0]
        space0.objects_per_dimension.resize(3)

        num_obj_0D = len(xc) # Number of nodes (len(xc) == len(yc))
                            # # have 2D coordinates, P(x,y)
        num_coord = len(xc) + len(yc)  # Number of all available coordinates
        num_gridSubsets = 2  # Number of grid subsets to write (Cells and Nodes)

        space0.coordinates_type.resize(2)
        space0.coordinates_type[0] = 1 # X
        space0.coordinates_type[1] = 2 # Y

        imas_obj.edge_profiles.ggd[0].grid.grid_subset.resize(num_gridSubsets)

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


        # Write all available 0D objects (all of them form the grid subset
        # Nodes
        # Set (IDS substructure shortcut variable) dim0
        dim0 = space0.objects_per_dimension[gridSubset_dim_index - 1]
        dim0.object.resize(num_obj_0D)
        for i in range(num_obj_0D):
            dim0.object[i].nodes.resize(1)
            dim0.object[i].nodes[0] = i
            dim0.object[i].geometry.resize(2)
            dim0.object[i].geometry[0] = xc[i]
            dim0.object[i].geometry[1] = yc[i]

        # Set(IDS substructure shortcut variable) gridSubsetBaseData
        gridSubsetBaseData = \
            imas_obj.edge_profiles.ggd[0].grid.grid_subset[gridSubset_index-1]
        # Put base grid subset data/parameters (name, index)
        gridSubsetBaseData.identifier.name = gridSubset_name
        gridSubsetBaseData.identifier.index = gridSubset_index
        # Put grid subset element and element object data
        gridSubsetBaseData.element.resize(num_obj_0D)
        for i in range(num_obj_0D):
            gridSubsetBaseData.element[i].object.resize(1)
            gridSubsetBaseData.element[i].object[0].space = 0 + 1
            gridSubsetBaseData.element[i].object[0].dimension = gridSubset_dim_index
            gridSubsetBaseData.element[i].object[0].index = i + 1

        # -- Put DATA FOR GRUD SUBSET "Cells"
        # (grid subset index: 1, objects forming the grid subset: cells, 2D)

        numCellsX = nx + 2
        numCellsY = ny + 2
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
        cellId  = 1
        for j in range(numCellsY):
            for i in range(numCellsX):
                dim2.object[cellId - 1].nodes[0] = cellId+0*numCellsX*numCellsY
                dim2.object[cellId - 1].nodes[1] = cellId+1*numCellsX*numCellsY
                dim2.object[cellId - 1].nodes[2] = cellId+3*numCellsX*numCellsY
                dim2.object[cellId - 1].nodes[3] = cellId+2*numCellsX*numCellsY
                cellId += 1

        # Set (IDS substructure shortcut variable) subgridDaseData for
        # Cells grid subset
        gridSubsetBaseData = \
            imas_obj.edge_profiles.ggd[0].grid.grid_subset[gridSubset_index - 1]
        # Put base grid subset data/parameters (name, index)
        gridSubsetBaseData.identifier.name = gridSubset_name
        gridSubsetBaseData.identifier.index = gridSubset_index
        # Put grid subset element and element object data
        gridSubsetBaseData.element.resize(num_obj_2D)
        for i in range(num_obj_2D):
            gridSubsetBaseData.element[i].object.resize(1)
            gridSubsetBaseData.element[i].object[0].space = 0 + 1
            gridSubsetBaseData.element[i].object[0].dimension = gridSubset_dim_index
            gridSubsetBaseData.element[i].object[0].index = i + 1

        # PUT VALUES (ne, te, ti) for "Cells" grid subset
        # Put ne (electron density)
        num_ne_gridSubset = 1
        num_ne_values = len(ne)
        imas_obj.edge_profiles.ggd[0].electrons.density.resize(num_ne_gridSubset)
        nePath = \
            imas_obj.edge_profiles.ggd[0].electrons.density[num_ne_gridSubset - 1]
        nePath.grid_subset_index = gridSubset_index
        nePath.values.resize(num_ne_values)
        for n in range(num_ne_values):
            nePath.values[n] = ne[n]

        # Put te (electron temperature)
        num_te_gridSubset = 1
        num_te_values = len(te)
        imas_obj.edge_profiles.ggd[0].electrons.temperature.resize(num_te_gridSubset)
        tePath = \
            imas_obj.edge_profiles.ggd[0].electrons.temperature[num_te_gridSubset - 1]
        tePath.grid_subset_index = gridSubset_index
        tePath.values.resize(num_te_values)
        for n in range(num_te_values):
            # convert to eV (1 J = 6.242e18 eV)
            tePath.values[n] = te[n] *(6.242e18)

        # Put ti (ion temperature)
        num_ti_gridSubset = 1
        num_ti_values = len(ti)
        num_ti_species = 1  # Number of ion species, as in
                            # number of different ion charges.
        ion_specie = 1
        # Ion specie is linked with the ion density of each ion charge,
        # as ion temperature is taken as the same for all ion charges.
        imas_obj.edge_profiles.ggd[0].ion.resize(num_ti_species)
        imas_obj.edge_profiles.ggd[0].ion[ion_specie - 1].temperature.\
            resize(num_ti_gridSubset)
        tiPath = imas_obj.edge_profiles.ggd[0].ion[ion_specie - 1]. \
            temperature[num_ti_gridSubset - 1]
        tiPath.grid_subset_index = gridSubset_index
        tiPath.values.resize(num_ti_values)
        for n in range(num_ti_values):
            # convert to eV (1 J = 6.242e18 eV)
            tiPath.values[n] = ti[n] * (6.242e18)

    # Write all put data do IDS
    imas_obj.edge_profiles.put()

    # Close IDS
    imas_obj.close()
    print("IDS write finished")
    print("IDS closed")

if __name__ == "__main__":
    try:
        import imas
    except Exception as e:
        print("Required IMAS support library not available on this system.")
        sys.exit()
    # For launching python script directly from treminal with python command
    try:
        opts, args = getopt.getopt(sys.argv[1:], "srutvh", ["dirpath=",
                                                            "shot=", "run=",
                                                            "user=", "device=",
                                                            "version=", "help"])
        for opt, arg in opts:
            #print opt, arg
            if opt in ("-fp", "--dirpath"):
                filepath = arg
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

            if opt in ("-h", "--help"):
                print("In order to run b2read file path, shot, run, user,"
                    "device and version variables must be defined."
                    "Example (terminal): "
                    "python3.5 put_edge_ids.py "
                    "--dirpath=/home/ITER/penkod/solps-iter/runs/AUG_16151_D/"
                    "baserun "
                    "--shot=1000 --run=1 --user=penkod --device=solps-iter "
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
python3.5 put_edge_ids.py --dirpath=/home/ITER/simicg/RUNS/demo/2171/baserun --user=simicg --run=1001 --shot=1001 --device=solps-iter --version=3
    """
    xc, yc, nx, ny = readB2fgmtry(filepath)
    ne, te, ti = readB2fstati(filepath)
    code_parameters = tarInputFiles(filepath)
    #code_parameters = 'test\x00test'
    print(code_parameters[:10])
    B2toIDS(shot, run, user, device, version, xc, yc, nx, ny, ne, te, ti, code_parameters, filepath)
