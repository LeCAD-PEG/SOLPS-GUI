#! /usr/bin/env python
#Python 3.5
#> Legend:
#>      #> .............. variables description, additional (helpful)
#>                            information etc.
#>      # ............... Commented part of code  

#> -----------------------------------------------------------------------------
#> DESCRIPTION
#> This Python script is used to read geometry from b2fgmtry file together with
#> electron density, electron temperature and ion temperature scalars from 
#> b2fstati file. The same data is then written to IDS together by 
#> creating "Cells" and "Nodes" grid subsets.
#>
#> Basic environment settings (terminal commands on hpc iter.org)
#> $ module load imas/3.7.4/ual/3.4.0
#> $ imasdb solps-iter
#> -----------------------------------------------------------------------------

try:
    import BytesIO
except:
    from io import BytesIO

import getopt
import sys
import os
import tarfile

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


def tarInputFiles(dir_path):
    tf = BytesIO()
    tar = tarfile.TarFile(mode='w', fileobj=tf)
    for filename in input_files:
        name = getB2path(dir_path, filename)
        if name:
            os.chdir(dir_path)
            tar.add(name)

    bstring = tf.getvalue()
    bstring = bstring.replace(b'\x00', b'\x01')
    return bstring.decode()

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
    #> Read geometry from file b2fgmtry (x and y coordinates of nodes)
    #> and insert them into array for later use

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
            code_paramaters):
    # Writing previously found data in b2fgmtry and b2fstati to IDS database
    print('Writing IDS: ')
    time = 1
    interp = 1

    # --Creating IDS database--
    imas_obj = imas.ids(shot, run, shot, run)

    # imas_obj.create()  # Create the data entry
    imas_obj.create_env(user, device, version)

    if imas_obj.isConnected():
        print('Creation of data entry OK!')
    else:
        print('Creation of data entry FAILED!')
        return 0

    # --Basic IDS space allocation--
    imas_obj.edge_profiles.profiles_1d.resize(1)
    imas_obj.edge_profiles.ggd.resize(1)
    imas_obj.edge_profiles.putNonTimed()
    imas_obj.edge_profiles.ggd[0].grid.space.resize(1)
    imas_obj.edge_profiles.ggd[0].grid.space[0].objects_per_dimension.resize(3)
    imas_obj.edge_profiles.ids_properties.homogeneous_time = 1 # !
    #

    # Writing code parameters
    imas_obj.edge_profiles.code.parameters = code_parameters
    # Homogeneous time: Synchronised data over same time array

    num_coord = len(xc) + len(yc)  # Number of all available coordinates
    num_subgrids = 2  # Number of subgrid to write (Cells and Nodes)

    imas_obj.edge_profiles.time.resize(num_coord)
    imas_obj.edge_profiles.ggd[0].grid.space[0].coordinates_type.resize(1)

    imas_obj.edge_profiles.ggd[0].grid.grid_subset.resize(num_subgrids)

    ## --WRITING DATA FOR SUBGRID "Nodes"
    # (subgrid base id : 2, subgrid class : 1) --
    # Note that writing of all data in form of indices is done in Fortran index
    # counting (starting with 1), not in C++/python index counting
    # (starts with 0)!
    # But we must have in mind, that currently we're working with Python
    # ( Python_Index == Fortran_Index -1)!
    num_nodes = int(num_coord / 2)  # We have 2D coordinates, P(x,y)
    subgrid_base_index = 2  # Subgrid index of subgrid Nodes
                        # (Indexing of subgrids is as in shot: 1, run:1,
                        # device:iter; and shot:16151, run:1000; device:aug
    subgrid_name = "Nodes"
    subgrid_class = 1   # Subgrid Nodes consists of points -> subgrid class 1
                        # (edges -> class 2; cells -> class 3)
    obj_class_1_id = 1  # Index used to identify between the subgrids under the
                        # same subgrid-class group

    # Writing base subgrid data/parameters
    subgridBaseData = \
        imas_obj.edge_profiles.ggd[0].grid.grid_subset[subgrid_base_index-1]
    subgridGeoData = imas_obj.edge_profiles.ggd[0].grid.space[0] \
        .objects_per_dimension[subgrid_class - 1]

    subgridGeoData.object.resize(1)

    subgridBaseData.identifier.name = subgrid_name
    subgridBaseData.identifier.index = subgrid_base_index
    subgridBaseData.element.resize(1)
    subgridBaseData.element[0].object.resize(1)
    subgridBaseData.element[0].object[0].space = 0 + 1
    subgridBaseData.element[0].object[0].dimension = subgrid_class

    # --Allocating space and writing to IDS:
    # Geometry and Nodes for class 1 -> Nodes -- #
    subgridGeoData.object.resize(1)
    subgridBaseData.element[0].object[0].index = obj_class_1_id
    subgridGeoData.object[obj_class_1_id - 1].geometry.resize(num_coord)
    subgridGeoData.object[obj_class_1_id - 1].nodes.resize(num_nodes)

    for n in range(num_nodes):
        # There are num_nodes geometry entries.
        # [x1, x2, ... xn, y1, y2, ...yn] -> Fortran notation
        subgridGeoData.object[obj_class_1_id - 1].geometry[n] = xc[n]
        subgridGeoData.object[obj_class_1_id - 1].geometry[num_nodes + n]=yc[n]
        subgridGeoData.object[obj_class_1_id - 1].nodes[n] = n + 1
        imas_obj.edge_profiles.time[n] = time

    ## --WRITING DATA FOR SUBGRID "Cells" (base subgrid id = 1; subgrid class 3)
    numCellsX = nx + 2
    numCellsY = ny + 2
    num_cells = numCellsX * numCellsY
    subgrid_base_index = 1
    subgrid_name = "Cells"
    subgrid_class = 3
    obj_class_3_id = 1

    # setting subgridDaseData and subgridGeoData for Cells subgrid
    subgridBaseData = \
        imas_obj.edge_profiles.ggd[0].grid.grid_subset[subgrid_base_index - 1]
    subgridGeoData = imas_obj.edge_profiles.ggd[0].grid.space[0] \
        .objects_per_dimension[subgrid_class - 1]

    subgridBaseData.identifier.name = subgrid_name
    subgridBaseData.identifier.index = subgrid_base_index
    subgridBaseData.element.resize(1)
    subgridBaseData.element[0].object.resize(1)
    subgridBaseData.element[0].object[0].space = 0 + 1
    subgridBaseData.element[0].object[0].dimension = subgrid_class

    subgridGeoData.object.resize(1)
    subgridBaseData.element[0].object[0].index = obj_class_3_id
    subgridGeoData.object[obj_class_3_id - 1].nodes.resize(
        num_cells * 4)  # each cell consists of 4 nodes

    # Writing cells geometry for Cells subgrid
    cellId  = 0
    for j in range(numCellsY):
        for i in range(numCellsX):
            subgridGeoData.object[obj_class_3_id - 1].nodes[
                cellId+0*numCellsX*numCellsY] = cellId+0*numCellsX*numCellsY+1
            subgridGeoData.object[obj_class_3_id - 1].nodes[
                cellId+1*numCellsX*numCellsY] = cellId+1*numCellsX*numCellsY+1
            subgridGeoData.object[obj_class_3_id - 1].nodes[
                cellId+3*numCellsX*numCellsY] = cellId+2*numCellsX*numCellsY+1
            subgridGeoData.object[obj_class_3_id - 1].nodes[
                cellId+2*numCellsX*numCellsY] = cellId+3*numCellsX*numCellsY+1
            cellId += 1

    #> Set (IDS substructure shortcut variable) subgridDaseData for 
    #> Cells grid subset
    gridSubsetBaseData = \
        imas_obj.edge_profiles.ggd[0].grid.grid_subset[gridSubset_index - 1]
    #> Put base grid subset data/parameters (name, index)
    gridSubsetBaseData.identifier.name = gridSubset_name
    gridSubsetBaseData.identifier.index = gridSubset_index
    #> Put grid subset element and element object data
    gridSubsetBaseData.element.resize(num_obj_2D)
    for i in range(num_obj_2D):
        gridSubsetBaseData.element[i].object.resize(1)
        gridSubsetBaseData.element[i].object[0].space = 0 + 1
        gridSubsetBaseData.element[i].object[0].dimension = gridSubset_dim_index
        gridSubsetBaseData.element[i].object[0].index = i + 1

    #> PUT VALUES (ne, te, ti) for "Cells" grid subset
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
    #> Ion specie is linked with the ion density of each ion charge,
    #> as ion temperature is taken as the same for all ion charges.
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

<<<<<<< HEAD
    imas_obj.edge_profiles.put()
=======
    #> Write all put data do IDS
    imas_obj.edge_profiles.putSlice()
>>>>>>> abfe7f44f60da7c10f5963f5cf91e36a865ff2ed

    #> Close IDS
    imas_obj.close()
<<<<<<< HEAD
    print("Closing IDS.")
    return 1
=======
    print("IDS write finished")
    print("IDS closed")
>>>>>>> abfe7f44f60da7c10f5963f5cf91e36a865ff2ed

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

<<<<<<< HEAD
    except Exception:
=======
        dirpath, shot, run, user, device, version
    except getopt.GetoptError:
>>>>>>> abfe7f44f60da7c10f5963f5cf91e36a865ff2ed
        print ('Supplied option not recognized!')
        print ('For help: b2read -h / --help')
        sys.exit(2)

    # few paths to example files for testing
    # /home/ITER/tomsicp/solps-iter/runs/AUG_16151_D/baserun
    # /home/ITER/tomsicp/solps-iter-devel/runs/ITER_535_D+He+Ar/baserun
<<<<<<< HEAD
    # run: "imasdb solps-iter"
    # Example command:
    """
python3.5 put_edge_ids.py --dirpath=/home/ITER/simicg/RUNS/demo/2171/baserun --user=simicg --run=1001 --shot=1001 --device=solps-iter --version=3
    """
    xc, yc, nx, ny = readB2fgmtry(filepath)
    ne, te, ti = readB2fstati(filepath)
    code_parameters = tarInputFiles(filepath)
    # code_parameters = r'test\x00test'
    print(code_parameters[:50])
    B2toIDS(shot, run, user, device, version, xc, yc, nx, ny, ne, te, ti, code_parameters)
=======

    xc, yc, nx, ny = readB2fgmtry(dirpath)
    ne, te, ti = readB2fstati(dirpath)

    B2toIDS(shot, run, user, device, version, xc, yc, nx, ny, ne, te, ti)
>>>>>>> abfe7f44f60da7c10f5963f5cf91e36a865ff2ed

