/**
*-------------------------------------------------------------------------------
*   @file     ReadUALEdge.cxx
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the main C++ file of the ParaView ReadUALEdge file
*   DESCRIPTION
*   ParaView ReadUALEdge plugin is a tool used to visualize and analyze data,
*   obtained by fusion simulations (electron temperature/density, ion
*   temperature/density) stored in CPO and/or IDS database.
*   The focus of plugin development is on data stored in IDS "edge_profiles".
*-------------------------------------------------------------------------------
*/

#include <iostream>
#include <fstream>
#include <string>
#include <tuple>
#include "vtkVersion.h"
#include "vtkSmartPointer.h"
#include "vtkTable.h"
#include "vtkFloatArray.h"
#include "vtkIntArray.h"
#include "vtkCellArray.h"
#include "vtkPointData.h"
#include "ReadUALEdge.h"
#include "vtkUnstructuredGrid.h"
#include "vtkMultiBlockDataSet.h"
#include "vtkObjectFactory.h"
#include "vtkInformationVector.h"
#include "vtkInformation.h"
#include "vtkDataObject.h"
#include "vtkDoubleArray.h"
#include "vtkCellData.h"
#include "vtkPoints.h"
#include "vtkPolyData.h"
#include "vtkQuad.h"
#include "vtkTriangle.h"
#include "UALClasses.h"
#include <vtkLine.h>
#include <vtkVertex.h>
#include <vtkStringArray.h>
#include <dirent.h>
#include <vector>
#include <sys/stat.h>
#include <unistd.h>

#define IMAS_IDS

// Set macro to take:
// - strName, name (string data type) of the plasma state quantity,
// - vtkUGtarget, vtkUnstructuredGrid target, and
// - IDStarget, a grid_generic_scalar IDS data structure target.
// Those two arguments are then used with the
// 'fVal2UnstrGrid_GenericGridScalar' function to read the target plasma state
// quantities.
// Example:
//    readValues_GenericGridScalar(   "Electron Density",
//                                    electrons.density );
#define readValues_GenericGridScalar(strName, vtkUGtarget, IDStarget) \
    num_IDStarget_gridSubsets = ggd.IDStarget.extent(0); \
    for (int n = 0; n < num_IDStarget_gridSubsets; n++) \
    { \
        fVal2UnstrGrid_GenericGridScalar( \
            strName, \
            vtkUGtarget, \
            ggd.IDStarget(n), \
            gridSubset_index, \
            num_gridSubset_el); \
    }

// Set macro to take:
// - std::string stdName, the name of the plasma state quantity,
// - vtkUGtarget, vtkUnstructuredGrid target,
// - IDStarget, a grid_generic_vector_components IDS data structure target, and
// - std::string strComponent, the name of the component.
// Those two arguments are then used with the
// 'fVal2UnstrGrid_GenericGridScalar' function to read the target plasma state
// quantities.
// Example:
//    readValues_GenericGridVectorComponents(
//        "Electron Velocity - Radial",
//        electrons.velocity,
//        "radial" );
#define readValues_GenericGridVectorComponents(strName, vtkUGtarget, IDStarget, strComponent) \
    num_IDStarget_gridSubsets = ggd.IDStarget.extent(0); \
    for (int n = 0; n < num_IDStarget_gridSubsets; n++) \
    { \
        fVal2UnstrGrid_GenericGridVectorComponents( \
            strName, \
            vtkUGtarget, \
            ggd.IDStarget(n), \
            strComponent, \
            gridSubset_index, \
            num_gridSubset_el); \
    }

// From ggd/f90/src/service/ids_grid_common.f90
// First cartesian coordinate in the horizontal plane [m]
#define COORDTYPE_X              1
// Second cartesian coordinate in the horizontal plane [m]
#define COORDTYPE_Y              2
// Major radius [m]
#define COORDTYPE_R              4
// Vertical position Z [m]
#define COORDTYPE_Z              5
// Toroidal angle [rad]
#define COORDTYPE_PHI            6
// Poloidal magnetic flux [T*m^2]
#define COORDTYPE_PSI            7
// Geometrical poloidal angle
#define COORDTYPE_THETA          8

#define SSTR( x ) dynamic_cast< std::ostringstream & >(                 \
    ( std::ostringstream() << std::dec << x ) ).str()


vtkStandardNewMacro(ReadUALEdge);

ReadUALEdge::ReadUALEdge()
{
    this->User = NULL;
    this->Device = NULL;
    this->Version = NULL;
    this->RefRun = 0;
    this->SetNumberOfInputPorts(0);
    this->SetNumberOfOutputPorts(1);
    this->DebugOff();
    this->stringArray=vtkSmartPointer<vtkStringArray>::New();
}

/**
*   Function used to read directory holding the IDSs and put
*   the found shot/runs into vector for later use
*/
std::vector<std::string> findShotRun(   std::string userIMASShotRunDir,
                                        std::string user)
{
    DIR *pDIR = NULL;
    struct dirent *entry = NULL;
    std::string dirPath = userIMASShotRunDir;
    std::vector<std::string> availableShotRun;
    std::string d_name_str;
    int digitInStrCount = 0;
    std::string stripShot;
    std::string stripRun;

    struct stat sb;
    if(string(user) == "")
    {
        char *loginUserName = getlogin();
        user = string(loginUserName);
    }
    // Check if the directory exists
    if (stat(dirPath.c_str(), &sb) == 0 && S_ISDIR(sb.st_mode))
    {
        std::clog <<"IDS directory from user " << user <<
            " found. Reading available IDS shot/runs." << std::endl;
        if( pDIR=opendir(dirPath.c_str()))
        {
            while(entry = readdir(pDIR))
            {
                if( strcmp(entry->d_name, ".") != 0 &&
                    strcmp(entry->d_name, "..") != 0 )
                {
                    // Read all files in directory
                    d_name_str = std::string(entry->d_name);
                    int d_name_str_len = d_name_str.length();
                    if(d_name_str.substr( d_name_str_len - 5 ) == ".tree")
                    {
                        // Work only with .tree files
                        for(int i = 0; i < d_name_str.length(); i++)
                        {
                            if(isdigit(d_name_str[i]))
                                digitInStrCount++;
                        }
                        int numExtCh = 5;   // 5 is for ".tree" == 5 characters
                        int numRunMax = 4;  // Run consists of max 4 characters
                                            // (from 0000 to 9999).
                        stripShot = d_name_str.substr(
                            d_name_str_len-numExtCh - digitInStrCount,
                            digitInStrCount-numRunMax);
                        stripRun = d_name_str.substr(
                            d_name_str_len-numExtCh - numRunMax,numRunMax);
                        // Get rid of excess zeros in Run number
                        // (example 0011->11).
                        int stripRunStartLen = stripRun.length();
                        int eraseCount = 0;
                        while(stripRun[0] == '0' &&
                              eraseCount < stripRunStartLen-1)
                        {
                            stripRun.erase(0,1);
                            eraseCount++;
                        }
                        // Set stripShot and stripRun in proper form
                        availableShotRun.push_back(stripShot);
                        availableShotRun.push_back(stripRun);
                        digitInStrCount = 0;
                    }
                }
            }
            closedir(pDIR);
        }
    }
    return availableShotRun;
}

/**
*   Function used to get the geometry/coordinates of all 0D objects/points
*   P[R, Z] forming this grid
*/
vtkSmartPointer<vtkPoints> fSetVtkPoints(
    class IdsNs::IDS::edge_profiles::ggd::grid::space& space)
{
    class IdsNs::IDS::edge_profiles::ggd::grid::space::objects_per_dimension&
        dim_obj_0D = space.objects_per_dimension(0);
    // Get number of 0D objects / points
    int num_obj_0D = dim_obj_0D.object.extent(0);
    vtkSmartPointer<vtkPoints> pointsArray =
        vtkSmartPointer<vtkPoints>::New();
    for(int i=0; i < num_obj_0D; ++i){
    pointsArray->InsertNextPoint(
        dim_obj_0D.object(i).geometry(0),
        dim_obj_0D.object(i).geometry(1),
        0.0);
    }
    return pointsArray;
}

/**
*   Function used to set vtkDoubleArray size and label
*/
vtkSmartPointer<vtkDoubleArray> fSetValuesArrayBase(
    int ndarray_num_tuples,
    std::string ndarray_label)
{
    vtkSmartPointer<vtkDoubleArray> newDoubleArray =
        vtkSmartPointer<vtkDoubleArray>::New();
    newDoubleArray->SetNumberOfComponents(1);
    newDoubleArray->SetNumberOfTuples(ndarray_num_tuples);
    std::string set_name = ndarray_label;
    newDoubleArray->SetName(set_name.c_str());
    return newDoubleArray;
}

/**
*   Function used to fill predefined (size, label...) vtkDoubleArray with
*   quantity values stored in generic_grid_scalar IDS data structure
*   and assign it to vtkUnstructuredGrid.
*   (after each full vtkDoubleArray definition process is required
*   to assign it to vtkUnstructuredGrid)
*   @param loc_quantity     \b grid_generic_scalar IDS data structure
*/
template <typename LQ1>
void fVal2UnstrGrid_GenericGridScalar(
    std::string values_array_label,
    vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
    LQ1 const& loc_quantity,
    int gridSubset_index,
    int num_gridSubset_el)
{
// Skip if the node structure is empty, otherwise continue
    int quantity_gridSubset_index = loc_quantity.grid_subset_index;
    int num_values = loc_quantity.values.extent(0);
    if (gridSubset_index == quantity_gridSubset_index &&
        num_gridSubset_el == num_values)
    {
        // Define vtkDoubleArray and set its label and size
        vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
            fSetValuesArrayBase(    num_gridSubset_el,
                                    values_array_label);
        // In correctly written IDS the number of grid subset
        // objects and grid subset values (scalars) is equal
        newVtkDoubleArray->
            SetNumberOfValues(num_gridSubset_el);
        for (int j = 0; j < num_gridSubset_el; j++)
        {
            newVtkDoubleArray->SetComponent(
                j,0, loc_quantity.values(j));
        }
        // Set new vtkDoubleArray, containing data field,
        // to vtkUnstructuredGrid
        inputVtkUnstructuredGrid->GetCellData()->AddArray(
            newVtkDoubleArray);
        return;
    }
}

/**
*   Function used to fill predefined (size, label...) vtkDoubleArray with
*   quantity values stored in generic_grid_vector_components IDS data structure
*   and assign it to vtkUnstructuredGrid.
*   (after each full vtkDoubleArray definition process is required
*   to assign it to vtkUnstructuredGrid)
*   @param loc_quantity     \b grid_generic_vector_components IDS data structure
*/
template <typename LQ2>
void fVal2UnstrGrid_GenericGridVectorComponents(
    std::string values_array_label,
    vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
    LQ2 const& loc_quantity,
    std::string component_label,
    int gridSubset_index,
    int num_gridSubset_el)
{
    int quantity_gridSubset_index = loc_quantity.grid_subset_index;
    // Set component_label_ID integer to be used in switch statement
    // (as C++ cannot directly use strings in switch statements)
    int component_label_ID = 0;
    if ( component_label == "radial") component_label_ID = 1;
    if ( component_label == "diamagnetic") component_label_ID = 2;
    if ( component_label == "parallel") component_label_ID = 3;
    if ( component_label == "poloidal") component_label_ID = 4;
    if ( component_label == "toroidal") component_label_ID = 5;

    // Read defined component and set it to vtkDoubleArray
    switch( component_label_ID )
    {
        case 1:
        {
            int num_values = loc_quantity.radial.extent(0);
            if (gridSubset_index == quantity_gridSubset_index &&
                num_gridSubset_el == num_values)
            {
                // Define vtkDoubleArray and set its label and size
                vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
                    fSetValuesArrayBase(    num_gridSubset_el,
                                            values_array_label);
                // In correctly written IDS the number of grid subset
                // objects and grid subset values (scalars) is equal
                newVtkDoubleArray->
                    SetNumberOfValues(num_gridSubset_el);
                for (int j = 0; j < num_gridSubset_el; j++)
                {
                    newVtkDoubleArray->SetComponent(
                        j,0, loc_quantity.radial(j));
                }
                // Set new vtkDoubleArray, containing data field,
                // to vtkUnstructuredGrid
                inputVtkUnstructuredGrid->GetCellData()->AddArray(
                    newVtkDoubleArray);
                return;
            }
        }
        case 2:
        {
            int num_values = loc_quantity.diamagnetic.extent(0);
            if (gridSubset_index == quantity_gridSubset_index &&
                num_gridSubset_el == num_values)
            {
                // Define vtkDoubleArray and set its label and size
                vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
                    fSetValuesArrayBase(    num_gridSubset_el,
                                            values_array_label);
                // In correctly written IDS the number of grid subset
                // objects and grid subset values (scalars) is equal
                newVtkDoubleArray->
                    SetNumberOfValues(num_gridSubset_el);
                for (int j = 0; j < num_gridSubset_el; j++)
                {
                    newVtkDoubleArray->SetComponent(
                        j,0, loc_quantity.diamagnetic(j));
                }
                // Set new vtkDoubleArray, containing data field,
                // to vtkUnstructuredGrid
                inputVtkUnstructuredGrid->GetCellData()->AddArray(
                    newVtkDoubleArray);
                return;
            }
        }
        case 3:
        {
            int num_values = loc_quantity.parallel.extent(0);
            if (gridSubset_index == quantity_gridSubset_index &&
                num_gridSubset_el == num_values)
            {
                // Define vtkDoubleArray and set its label and size
                vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
                    fSetValuesArrayBase(    num_gridSubset_el,
                                            values_array_label);
                // In correctly written IDS the number of grid subset
                // objects and grid subset values (scalars) is equal
                newVtkDoubleArray->
                    SetNumberOfValues(num_gridSubset_el);
                for (int j = 0; j < num_gridSubset_el; j++)
                {
                    newVtkDoubleArray->SetComponent(
                        j,0, loc_quantity.parallel(j));
                }
                // Set new vtkDoubleArray, containing data field,
                // to vtkUnstructuredGrid
                inputVtkUnstructuredGrid->GetCellData()->AddArray(
                    newVtkDoubleArray);
                return;
            }
        }
        case 4:
        {
            int num_values = loc_quantity.poloidal.extent(0);
            if (gridSubset_index == quantity_gridSubset_index &&
                num_gridSubset_el == num_values)
            {
                // Define vtkDoubleArray and set its label and size
                vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
                    fSetValuesArrayBase(    num_gridSubset_el,
                                            values_array_label);
                // In correctly written IDS the number of grid subset
                // objects and grid subset values (scalars) is equal
                newVtkDoubleArray->
                    SetNumberOfValues(num_gridSubset_el);
                for (int j = 0; j < num_gridSubset_el; j++)
                {
                    newVtkDoubleArray->SetComponent(
                        j,0, loc_quantity.poloidal(j));
                }
                // Set new vtkDoubleArray, containing data field,
                // to vtkUnstructuredGrid
                inputVtkUnstructuredGrid->GetCellData()->AddArray(
                    newVtkDoubleArray);
                return;
            }
        }
        case 5:
        {
            int num_values = loc_quantity.toroidal.extent(0);
            if (gridSubset_index == quantity_gridSubset_index &&
                num_gridSubset_el == num_values)
            {
                // Define vtkDoubleArray and set its label and size
                vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
                    fSetValuesArrayBase(    num_gridSubset_el,
                                            values_array_label);
                // In correctly written IDS the number of grid subset
                // objects and grid subset values (scalars) is equal
                newVtkDoubleArray->
                    SetNumberOfValues(num_gridSubset_el);
                for (int j = 0; j < num_gridSubset_el; j++)
                {
                    newVtkDoubleArray->SetComponent(
                        j,0, loc_quantity.toroidal(j));
                }
                // Set new vtkDoubleArray, containing data field,
                // to vtkUnstructuredGrid
                inputVtkUnstructuredGrid->GetCellData()->AddArray(
                    newVtkDoubleArray);
                return;
            }
        }
    }
}

/**
*   Function used to fill predefined (size, label...) vtkCellArray.
*/
template <typename V>
vtkSmartPointer<vtkCellArray> fSetCellArray(
    V const& el_data_type,
    class IdsNs::IDS::edge_profiles::ggd::grid::grid_subset& loc_gridSubset,
    class IdsNs::IDS::edge_profiles::ggd::grid& grid)
{
    vtkSmartPointer<vtkCellArray> newCellArray =
        vtkSmartPointer<vtkCellArray>::New();

    // Get size/number of elements forming current grid subset
    // Currently ReadUALEdge works only with elements containing one object
    // (one scalar value is provided per element).
    int num_gridSubset_el = loc_gridSubset.element.extent(0);

    // Get dimension of the objects forming this grid subset
    // NOTE :  Each grid subset is formed with objects of the same
    //         dimension
    //         (either only 0D nodes, 1D edges, 2D cells...).
    //         So in that case is enough to read only the dimension of
    //         the first object forming the grid subset.
    int obj_dimension = loc_gridSubset.element(0).object(0).dimension;

    for (int j = 0; j < num_gridSubset_el; j++)
    {
        // Get objects space index, dimension and index
        // Note that in IDS indices are written in Fortran notation
        // (1,2,3,...) while C++ notation starts with 0 (0,1,2,...)
        // so c++_index = fortran_index - 1

        // Get space index of the object
        int obj_space = loc_gridSubset.element(j).object(0).space;

        // Get object index of the object
        int obj_index = loc_gridSubset.element(j).object(0).index;

        // Get number of nodes/points forming the object
        int num_obj_nodes = grid.space(obj_space - 1).
            objects_per_dimension(obj_dimension - 1).
            object(obj_index - 1).nodes.extent(0);

        // Fill the el_data_type (it must be either vtkVertex,
        // vtkLine, vtkTriangle or vtkQuad data type)
        for(int k = 0; k < num_obj_nodes; k++)
        {
            int node_ind = grid.space(obj_space - 1).
                objects_per_dimension(obj_dimension - 1).
                object(obj_index - 1).nodes(k);
            el_data_type->GetPointIds()->
                SetId(k, node_ind - 1);
        }
        // Assign the <el_data_type> list of data types to vtkCellArray
        newCellArray->InsertNextCell(el_data_type);
    }
    return newCellArray;
}

/**
*   Function to add unstructured grid to main multiblock
*/
void fAddBlock2MultiBlock(  vtkSmartPointer<vtkMultiBlockDataSet> MB,
                            vtkSmartPointer<vtkUnstructuredGrid>  UG,
                            std::string gridSubset_name)
{
    int num_blocks = MB->GetNumberOfBlocks();
    MB->SetBlock(num_blocks, UG);
    MB->GetMetaData((unsigned int) num_blocks)->Set(
        vtkCompositeDataSet::NAME(), gridSubset_name.c_str());
}

/*
*   Set Ion specie data field label.
*   @param   is  Ion specie index
*   @param   ic  Ion charge
*/
std::string fSetIonQuantityLabel(   std::string quantity_name, int is,
                                    std::string ic )
{
    stringstream ion_species_num2str;
    ion_species_num2str << is + 1;
    std::string is_string = ion_species_num2str.str();
    std::string ion_array_label;
    if (is < 9)
    {
        ion_array_label = "Ion " + quantity_name + " 0" + is_string + ic;
    } else
    {
        ion_array_label = "Ion " + quantity_name + " " + is_string + ic;
    }
    return ion_array_label;
}

/**
*   Main ReadUALEdge function. It reads grid geometry, grid subset and plasma
*   state data out of the IDSs and combines this data into display ready
*   visualized data.
*
*/
int ReadUALEdge::RequestData(   vtkInformation *vtkNotUsed(request),
                                vtkInformationVector **vtkNotUsed(inputVector),
                                vtkInformationVector *outputVector)
{
    // get the info object
    vtkInformation *outInfo = outputVector->GetInformationObject(0);
    // get the output
    vtkMultiBlockDataSet *output = vtkMultiBlockDataSet::SafeDownCast(
        outInfo->Get(vtkMultiBlockDataSet::DATA_OBJECT()));

    std::clog << "Shot:" << this->Shot << " Run:" << this->Run << std::endl;

#ifdef IMAS_IDS
    using namespace IdsNs;

    // Check IMAS and DD version
    std::string imas_version = getenv("IMAS_VERSION");
    std::clog << "IMAS VERSION: " << imas_version << std::endl;
    if (imas_version != "3.15.0")
    {
        std::clog << "WARNING! This IMAS module version (and consequently \
                      Data Dictionary) is outdated! ReadUALEdge plugin might \
                      not be fully compatible with the currently used Data \
                      Dictionary! The latest IMAS module, confirmed to be \
                      compatible with the ReadUALEdge, is \
                      imas/3.15.0/ual/3.6.4" << std::endl;
    }

    std::clog << "Reading IDS" << std::endl;
    // Set IDSs shot and run
    IDS db(this->Shot, this->Run, this->Shot, this->RefRun);
    if (!this->Version)
        this->Version = strdup("3");
    // Open IDS
    db.openEnv(this->User, this->Device, this->Version);
    std::clog << "User: "<<this->User<<" Device: "<<this->Device<< std::endl;
    // Get IDS data
    db._edge_profiles.get();

    int num_ggd_slices = db._edge_profiles.ggd.extent(0);
    std::clog << "Number of GGD slices:" << num_ggd_slices << std::endl;

    if (num_ggd_slices == 0)
    {
        std::clog << "ERROR! Either selected database doesn't exist \
                      or it's empty!" << std::endl;
        vtkErrorMacro(<<"ERROR! Either selected database doesn't exist \
                         or it's empty!");
        return 0;
    }

    // Set class shortcuts for IDS substructures
    class IDS::edge_profiles & edge = db._edge_profiles;
    class IDS::edge_profiles::ggd & ggd = edge.ggd(0);
    class IDS::edge_profiles::ggd::grid & grid = ggd.grid;
    class IDS::edge_profiles::ggd::grid::space & space = grid.space(0);
    // objects_per_dimensions(0) holds every 0D object (nodes/vertices)
    class IDS::edge_profiles::ggd::grid::space::objects_per_dimension &
        dim_obj_0D = space.objects_per_dimension(0);
    // objects_per_dimensions(1) holds every 1D object (edges)
    class IDS::edge_profiles::ggd::grid::space::objects_per_dimension &
        dim_obj_1D = space.objects_per_dimension(1);
    // objects_per_dimensions(2) holds every 2D object (faces/2D cells)
    class IDS::edge_profiles::ggd::grid::space::objects_per_dimension &
        dim_obj_2D = space.objects_per_dimension(2);

    int num_obj_0D = 0; // Node/Point/vertice == 0D object
    int num_obj_1D = 0; // Edge    == 1D object
    int num_obj_2D = 0; // 2D Cell == 2D object

    // Check for nodes, edges and cells data in current IDS database and
    // get number of objects for each dimension
    num_obj_0D = dim_obj_0D.object.extent(0);
    num_obj_1D = dim_obj_1D.object.extent(0);
    num_obj_2D = dim_obj_2D.object.extent(0);

    std::clog << "num_obj_0D: " << num_obj_0D << std::endl;
    std::clog << "num_obj_1D: " << num_obj_1D << std::endl;
    std::clog << "num_obj_2D: " << num_obj_2D << std::endl;

    vtkSmartPointer<vtkMultiBlockDataSet> mainMB =
        vtkSmartPointer<vtkMultiBlockDataSet>::New();

    // Get the geometry/coordinates of all nodes/points N[R, Z]
    // forming this grid
    vtkSmartPointer<vtkPoints> obj_0D_vtkPointsArray = fSetVtkPoints(space);

    // Get number of grid subsets
    int num_gridSubset = grid.grid_subset.extent(0);
    int num_ne_gri = grid.grid_subset.extent(0);

    // Set array of plasma state (ion) quantity names (Density,
    // etc. Temperature )
    std::string edge_quantity_names[12];
    edge_quantity_names[0] = "Temperature";
    edge_quantity_names[1] = "Density";
    edge_quantity_names[2] = "Density_Fast";
    edge_quantity_names[3] = "Pressure";
    edge_quantity_names[4] = "Pressure_Fast_Perpendicular";
    edge_quantity_names[5] = "Pressure_Fast_Parallel";
    edge_quantity_names[6] = "Velocity - Radial";
    edge_quantity_names[7] = "Velocity - Diamagnetic";
    edge_quantity_names[8] = "Velocity - Parallel";
    edge_quantity_names[9] = "Velocity - Poloidal";
    edge_quantity_names[10] = "Velocity - Toroidal";
    edge_quantity_names[11] = "Energy Density Kinetic";

    // Loop through all grid subsets and extract data for each
    for(int i = 0; i < num_gridSubset; i++){
        class IDS::edge_profiles::ggd::grid::grid_subset & grid_subset =
            grid.grid_subset(i);
        std::string gridSubset_name = grid_subset.identifier.name;
        int gridSubset_index = grid_subset.identifier.index;

        // Get size/number of elements forming current grid subset
        int num_gridSubset_el = grid_subset.element.extent(0);

        std::clog << "num_gridSubset_el: " << num_gridSubset_el <<
            " gridSubset_name: "<< gridSubset_name << std::endl;

        // Get dimension of the objects forming this grid subset
        int gridSubset_obj_dim = grid_subset.element(0).object(0).dimension;
        int ne_gridSubsets_num = ggd.electrons.density.extent(0);

        // ------ SET POINTS/NODES -----
        if (gridSubset_obj_dim == 1)
        {
            // Set vtkUnstructuredGrid dataset
            vtkSmartPointer<vtkUnstructuredGrid> gridSubsetPointsUnstructuredGrid =
                vtkSmartPointer<vtkUnstructuredGrid>::New();

            vtkSmartPointer<vtkVertex> gridSubsetVertex =
                vtkSmartPointer<vtkVertex>::New();

            // Set vtkCellArray for nodes/points
            vtkSmartPointer<vtkCellArray> gridSubsetVertices =
                vtkSmartPointer<vtkCellArray>::New();
            gridSubsetVertices = fSetCellArray(gridSubsetVertex, grid_subset, grid);

            // Assign vtkCellArray to vtkUnstructuredGrid
            gridSubsetPointsUnstructuredGrid->SetPoints(obj_0D_vtkPointsArray);
            gridSubsetPointsUnstructuredGrid->SetCells(
                VTK_VERTEX, gridSubsetVertices);

            // Set integer to be later used in the readValues_GenericGridScalar
            // macro
            int num_IDStarget_gridSubsets = 0;

            // Assigning values (vertices) - Electrons

            // Assign values found in Electron Temperature substructure to
            // grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Temperature",
                gridSubsetPointsUnstructuredGrid,
                electrons.temperature );
            // Assign values found in Electron Density substructure to
            // grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Density",
                gridSubsetPointsUnstructuredGrid,
                electrons.density );
            // Assign values found in Electron Density_Fast substructure to
            // grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Density_Fast",
                gridSubsetPointsUnstructuredGrid,
                electrons.density_fast );
            // Assign values found in Electron Pressure substructure to
            // grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Pressure",
                gridSubsetPointsUnstructuredGrid,
                electrons.pressure );
            // Assign values found in Electron Pressure_Fast_Perpendicular
            // substructure to grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Pressure_Fast_Perpendicular",
                gridSubsetPointsUnstructuredGrid,
                electrons.pressure_fast_perpendicular );
            // Assign values found in Electron Pressure_Fast_Parallel
            // substructure to grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Pressure_Fast_Parallel",
                gridSubsetPointsUnstructuredGrid,
                electrons.pressure_fast_parallel );
            // Assign values found in Electron Velocity - Radial
            // substructure to grid subsets objects (vertices)
            readValues_GenericGridVectorComponents(
                "Electron Velocity - Radial",
                gridSubsetPointsUnstructuredGrid,
                electrons.velocity,
                "radial" );
            // Assign values found in Electron Velocity - Diamagnetic
            // substructure to grid subsets objects (vertices)
            readValues_GenericGridVectorComponents(
                "Electron Velocity - Diamagnetic",
                gridSubsetPointsUnstructuredGrid,
                electrons.velocity,
                "diamagnetic" );
            // Assign values found in Electron Velocity - Parallel
            // substructure to grid subsets objects (vertices)
            readValues_GenericGridVectorComponents(
                "Electron Velocity - Parallel",
                gridSubsetPointsUnstructuredGrid,
                electrons.velocity,
                "parallel" );
            // Assign values found in Electron Velocity - Poloidal
            // substructure to grid subsets objects (vertices)
            readValues_GenericGridVectorComponents(
                "Electron Velocity - Poloidal",
                gridSubsetPointsUnstructuredGrid,
                electrons.velocity,
                "poloidal" );
            // Assign values found in Electron Velocity - Toroidal
            // substructure to grid subsets objects (vertices)
            readValues_GenericGridVectorComponents(
                "Electron Velocity - Toroidal",
                gridSubsetPointsUnstructuredGrid,
                electrons.velocity,
                "toroidal" );
            // Assign values found in Electron Distribution Function
            // substructure to grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Distribution Function",
                gridSubsetPointsUnstructuredGrid,
                electrons.distribution_function );


            // Assigning values (vertices) - Ion species

            // Assign values to grid subsets objects (vertices) using scalars
            // found in Ion substructure
            int num_ion_species = ggd.ion.extent(0);
            for( int k = 0; k < num_ion_species; k++)
            {
                // Assign values found in ion Temperature substructure to
                // grid subsets objects (vertices)
                readValues_GenericGridScalar(
                    "Ion Temperature" + k,
                    gridSubsetPointsUnstructuredGrid,
                ion(k).temperature );

                /// Set ion specie label
                std::string ion_charge= ggd.ion(k).label;
                /// Set data field name
                std::string array_label;
                // Assign values found in Ion Density substructure to grid
                // subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[1],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetPointsUnstructuredGrid,
                    ion(k).density );
                // Assign values found in Ion Density_Fast substructure to grid
                // subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[2],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetPointsUnstructuredGrid,
                    ion(k).density_fast );
                // Assign values found in Ion Pressure substructure to grid
                // subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[3],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetPointsUnstructuredGrid,
                    ion(k).pressure );
                // Assign values found in Ion Pressure_Fast_Perpendicular
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[4],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetPointsUnstructuredGrid,
                    ion(k).pressure_fast_perpendicular );
                // Assign values found in Ion Pressure_Fast_Parallel
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[5],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetPointsUnstructuredGrid,
                    ion(k).pressure_fast_parallel );
                // Assign values found in Ion Velocity - Radial
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[6],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridVectorComponents(
                    array_label,
                    gridSubsetPointsUnstructuredGrid,
                    ion(k).velocity,
                    "radial" );
                // Assign values found in Ion Velocity - Diamagnetic
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[7],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridVectorComponents(
                    array_label,
                    gridSubsetPointsUnstructuredGrid,
                    ion(k).velocity,
                    "diamagnetic" );
                // Assign values found in Ion Velocity - Parallel
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[8],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridVectorComponents(
                    array_label,
                    gridSubsetPointsUnstructuredGrid,
                    ion(k).velocity,
                    "parallel" );
                // Assign values found in Ion Velocity - Poloidal
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[9],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridVectorComponents(
                    array_label,
                    gridSubsetPointsUnstructuredGrid,
                    ion(k).velocity,
                    "poloidal" );
                // Assign values found in Ion Velocity - Toroidal
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[10],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridVectorComponents(
                    array_label,
                    gridSubsetPointsUnstructuredGrid,
                    ion(k).velocity,
                    "toroidal" );
                // Assign values found in Ion Energy_Density_Kinetic
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[11],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetPointsUnstructuredGrid,
                    ion(k).energy_density_kinetic );
        }

            // Add unstructured grid to main block
            fAddBlock2MultiBlock(mainMB, gridSubsetPointsUnstructuredGrid,
                gridSubset_name );
        }
        // ------ SET LINES -----
        else if (gridSubset_obj_dim == 2)
        {
            vtkSmartPointer<vtkUnstructuredGrid> gridSubsetLinesUnstructuredGrid =
                vtkSmartPointer<vtkUnstructuredGrid>::New();

            // Set vtkCellArray for edges
            vtkSmartPointer<vtkCellArray> gridSubsetLinesArray =
                vtkSmartPointer<vtkCellArray>::New();
            vtkSmartPointer<vtkLine> gridSubsetLine =
                vtkSmartPointer<vtkLine>::New();
            gridSubsetLinesArray = fSetCellArray(gridSubsetLine, grid_subset, grid);

            // Assign vtkCellArray to vtkUnstructuredGrid
            gridSubsetLinesUnstructuredGrid->SetPoints(obj_0D_vtkPointsArray);
            gridSubsetLinesUnstructuredGrid->SetCells(
                VTK_LINE, gridSubsetLinesArray);

            // Add unstructured grid to main block
            fAddBlock2MultiBlock(mainMB, gridSubsetLinesUnstructuredGrid,
                gridSubset_name );
        }
        // ------ SET 2D CELLS -----
        else if (gridSubset_obj_dim == 3)
        {
            // Set vtk array for 2D cells
            vtkSmartPointer<vtkUnstructuredGrid> gridSubsetCellsUnstructuredGrid =
                vtkSmartPointer<vtkUnstructuredGrid>::New();
            vtkSmartPointer<vtkQuad> gridSubsetQuad =
                vtkSmartPointer<vtkQuad>::New();
            vtkSmartPointer<vtkTriangle> gridSubsetTriangle =
                vtkSmartPointer<vtkTriangle>::New();
            vtkSmartPointer<vtkCellArray> gridSubsetCellArray =
                vtkSmartPointer<vtkCellArray>::New();

            // Get number of nodes of the first 2D cell in order to find out
            // whether they are triangles or quad (all other 2D cells of the
            // same grid should be of the same type for now)
            int num_obj_nodes_first =
                grid.space(0).objects_per_dimension(gridSubset_obj_dim - 1).
                object(0).nodes.extent(0);
            // Cells-Triangles
            if (num_obj_nodes_first == 3)
            {
                gridSubsetCellArray = fSetCellArray(gridSubsetTriangle, grid_subset, grid);

                // Assign vtkCellArray to vtkUnstructuredGrid
                gridSubsetCellsUnstructuredGrid->SetPoints(obj_0D_vtkPointsArray);
                gridSubsetCellsUnstructuredGrid->SetCells(
                    VTK_TRIANGLE, gridSubsetCellArray);
            }
            // Cells-Quad
            else if (num_obj_nodes_first == 4)
            {
                gridSubsetCellArray = fSetCellArray(gridSubsetQuad, grid_subset, grid);

                // Assign vtkCellArray to vtkUnstructuredGrid
                gridSubsetCellsUnstructuredGrid->SetPoints(obj_0D_vtkPointsArray);
                gridSubsetCellsUnstructuredGrid->SetCells(
                    VTK_QUAD, gridSubsetCellArray);
            }

            // Set integer to be later used in the readValues_GenericGridScalar
            // macro
            int num_IDStarget_gridSubsets = 0;

            // Assigning values (2D cells) - Electrons

            // Assign values found in Electron Temperature substructure to
            // grid subsets objects (2D cells)
            readValues_GenericGridScalar(
                "Electron Temperature",
                gridSubsetCellsUnstructuredGrid,
                electrons.temperature );
            // Assign values found in Electron Density substructure to grid
            // subsets objects (2D cells)
            readValues_GenericGridScalar(
                "Electron Density",
                gridSubsetCellsUnstructuredGrid,
                electrons.density );
            // Assign values found in Electron Density_Fast substructure to
            // grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Density_Fast",
                gridSubsetCellsUnstructuredGrid,
                electrons.density_fast );
            // Assign values found in Electron Pressure substructure to
            // grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Pressure",
                gridSubsetCellsUnstructuredGrid,
                electrons.pressure );
            // Assign values found in Electron Pressure_Fast_Perpendicular
            // substructure to grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Pressure_Fast_Perpendicular",
                gridSubsetCellsUnstructuredGrid,
                electrons.pressure_fast_perpendicular );
            // Assign values found in Electron Pressure_Fast_Parallel
            // substructure to grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Pressure_Fast_Parallel",
                gridSubsetCellsUnstructuredGrid,
                electrons.pressure_fast_parallel );
            // Assign values found in Electron Distribution Function
            // substructure to grid subsets objects (vertices)
            readValues_GenericGridScalar(
                "Electron Distribution Function",
                gridSubsetCellsUnstructuredGrid,
                electrons.distribution_function );

            //** Assigning values (2D cells) - Ion species

            // Assign values found in Ion substructure to grid subsets
            // objects (2D cells)
            int num_ion_species = ggd.ion.extent(0);
            for( int k = 0; k < num_ion_species; k++)
            {

                //* Assign values found in ion Temperature substructure to
                //* grid subsets objects (2D cells)
                readValues_GenericGridScalar(
                    "Ion Temperature" + k,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).temperature );

                /// Set ion specie label
                std::string ion_charge= ggd.ion(k).label;
                /// Set data field name
                std::string array_label;
                // Assign values found in Ion Density substructure to grid
                // subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[1],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).density );
                // Assign values found in Ion Density_Fast substructure to grid
                // subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[2],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).density_fast );
                // Assign values found in Ion Pressure substructure to grid
                // subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[3],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).pressure );
                // Assign values found in Ion Pressure_Fast_Perpendicular
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[4],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).pressure_fast_perpendicular );
                // Assign values found in Ion Pressure_Fast_Parallel
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[5],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).pressure_fast_parallel );
                // Assign values found in Ion Velocity - Radial
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[6],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridVectorComponents(
                    array_label,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).velocity,
                    "radial" );
                // Assign values found in Ion Velocity - Diamagnetic
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[7],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridVectorComponents(
                    array_label,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).velocity,
                    "diamagnetic" );
                // Assign values found in Ion Velocity - Parallel
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[8],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridVectorComponents(
                    array_label,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).velocity,
                    "parallel" );
                // Assign values found in Ion Velocity - Poloidal
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[9],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridVectorComponents(
                    array_label,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).velocity,
                    "poloidal" );
                // Assign values found in Ion Velocity - Toroidal
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[10],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridVectorComponents(
                    array_label,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).velocity,
                    "toroidal" );
                // Assign values found in Ion Energy_Density_Kinetic
                // substructure to grid subsets objects (2D cells)
                array_label = fSetIonQuantityLabel( edge_quantity_names[11],
                    k, ion_charge );
                /// Assign values
                readValues_GenericGridScalar(
                    array_label,
                    gridSubsetCellsUnstructuredGrid,
                    ion(k).energy_density_kinetic );
            }

            // Add unstructured grid to main block
            fAddBlock2MultiBlock(mainMB, gridSubsetCellsUnstructuredGrid,
                gridSubset_name );
        }
    }

    output->ShallowCopy(mainMB);
    db.close();

#else  // CPO
       // Note: The development is focused on IDSs. Following that the
       //       plugin support for the CPO is not being developed at the time.
    ItmNs::Itm itm(this->Shot,this->Run,this->Shot,this->RefRun);

    if (!this->Version)
        this->Version = strdup("4.10a");
    itm.openEnv(this->User, this->Device, this->Version); //Open the database
    std::clog << "User: "<<this->User<<" Device:"<<this->Device<< std::endl;

    itm._edgeArray.get();

    int num_slices = itm._edgeArray.extent(0);
    if (num_slices == 0)
    {
        std::clog << "ERROR! Either selected database doesn't exist"
            "or it's empty!" << std::endl;
        return 0;
    }

    class ItmNs::Itm::edge & edge = itm._edgeArray[0];
    class ItmNs::Itm::edge::grid & grid = edge.grid;
    class ItmNs::Itm::edge::grid::spaces & space = grid.spaces(0);
    class ItmNs::Itm::edge::grid::spaces::objects & nodes = space.objects(0);
    class ItmNs::Itm::edge::grid::spaces::objects & edges = space.objects(1);
    class ItmNs::Itm::edge::grid::spaces::objects & cells = space.objects(2);

    std::clog << "grid id: " << grid.id << std::endl;

    int num_spaces = grid.spaces.extent(0);
    std::clog << "num_spaces: " << num_spaces << std::endl;
    grid.spaces.extent(0);

    int num_coordtypes =  space.coordtype.extent(0);

    if (num_spaces != 1 && num_coordtypes != 2)
    {
        std::clog << "Unhandled space configuration!" << std::endl;
        return 0;
    }

    // Assure we are reading SOLPS grid
    assert(space.coordtype(0,0) == COORDTYPE_R);
    assert(space.coordtype(1,0) == COORDTYPE_Z);
    // assert(space.objects.extent(0) == 1);

    int num_objects = space.objects.extent(0);
    std::clog << "num_objects: " << num_objects << std::endl;

    int num_nodes = nodes.geo.extent(0);
    std::clog << "num_nodes: " << num_nodes << std::endl;

    vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();

    for(int i=0; i < num_nodes; ++i)
    {
        points->InsertNextPoint(nodes.geo(i, 0), nodes.geo(i, 1), 0.0);
    }

    // 2D cells in GGD are defined by edges. Edges have indices to nodes.

    int num_edges = edges.boundary.extent(0);
    int num_cells = cells.boundary.extent(0);

    std::clog << "num_cells :" << num_cells << std::endl;

    vtkSmartPointer<vtkQuad> subgridQuad =  vtkSmartPointer<vtkQuad>::New();
    vtkSmartPointer<vtkCellArray> cellArray =
        vtkSmartPointer<vtkCellArray>::New();
    vtkSmartPointer<vtkMultiBlockDataSet> mainMB =
        vtkSmartPointer<vtkMultiBlockDataSet>::New();

    double all_cells[num_cells][4];
    for (int i = 0; i < num_cells; ++i)
    {
        int node_idx[4];    // Resulting node indices for a cell
        int free_edge[3];   // list of edges that are free to search for node
        int last_idx;       // last node index
        int edge_idx = cells.boundary(i, 0) - 1;
        free_edge[0] = cells.boundary(i, 1) - 1;
        free_edge[1] = cells.boundary(i, 2) - 1;
        free_edge[2] = cells.boundary(i, 3) - 1;
        node_idx[0] = edges.boundary(edge_idx, 0) - 1;
        node_idx[last_idx=1] = edges.boundary(edge_idx, 1) - 1;
        for(int loop_count = 0; last_idx < 3 && loop_count < 4; ++loop_count)
        {
            for(int j = 0; j < 3 ; ++j)
            {
                // free_edge
                edge_idx = free_edge[j];
                if(edge_idx < 0)
                continue;
                int node1 =  edges.boundary(edge_idx, 0) - 1;
                int node2 =  edges.boundary(edge_idx, 1) - 1;
                if (node_idx[last_idx] == node1)
                {
                    free_edge[j] = -1;
                    node_idx[++last_idx] = node2;
                    break;
                }
                if (node_idx[last_idx] == node2)
                {
                    free_edge[j] = -1;
                    node_idx[++last_idx] = node1;
                    break;
                }
            }
            assert(loop_count < 3);
        }
        all_cells[i][0] = node_idx[0];
        all_cells[i][1] = node_idx[1];
        all_cells[i][2] = node_idx[2];
        all_cells[i][3] = node_idx[3];
    }

    // Check contents under po (electric potential)
    class ItmNs::Itm::edge::fluid::po & po = edge.fluid.po;
    std::clog << std::left << setw(35) << "po.value(0).extent(0): _______" <<
        edge.fluid.po.value.extent(0) << std::endl;
    std::clog << std::left << setw(35) << "po.value(0).scalar.extent(0): ___" <<
        edge.fluid.po.value(0).scalar.extent(0) << std::endl;

    int num_ni_species = edge.fluid.ni.extent(0);
    std::clog << "Number of Ion Density species:" << num_ni_species <<
        std::endl;
    int num_ti_species = edge.fluid.ti.extent(0);
    std::clog << "Number of Ion Temperature species:" << num_ti_species <<
        std::endl;

    int num_subgrids = grid.subgrids.extent(0);
    std:: subgridName[num_subgrids];
    std::clog << "num_subgrids: "<< num_subgrids << std::endl;
    std::clog << "Setting scalars" << std::endl;
    for(int i = 0; i < num_subgrids; i++)
    {
        int subgrid_class = grid.subgrids(i).list(0).cls(0);
        int ind_num = grid.subgrids(i).list(0).ind.extent(0);
        subgridName[i] = grid.subgrids(i).id;
        int indset_found = grid.subgrids(i).list(0).indset.extent(0);
        // grid.subgrids(i).list(0).indset contains range for certain subgrid.
        // If indset is not found then also there is no range for that subgrid.
        std::clog << std::left << "Subgrid id number: " << setw(2) << i+1 <<
        " Subgrid name: " << setw(18) << subgridName[i] << " Subgrid class: " <<
        setw(1) << subgrid_class << " ";
        int range0 = 0;
        int range1 = 0;
        int range_found;
        int start_index;
        int end_index;
        int jIndex = 0;
        int array_size;
        if(indset_found > 0)
        {
            int range_size = grid.subgrids(i).list(0).indset(0).range.extent(0);
            if(range_size > 1)
            {
                range_found = 1;
                range0 = grid.subgrids(i).list(0).indset(0).range(0) - 1;
                range1 = grid.subgrids(i).list(0).indset(0).range(1);
                start_index = range0;
                end_index = range1;
                std::clog << std::left << " range: " << setw(4) << range0+1 <<
                " - " << setw(4) << range1;
                array_size = end_index - start_index;
            } else
            {
                std::clog << "Range is either EMPTY or it doesn't exist" <<
                std::endl;
            }
        } else
        {
            range_found = 0;
            start_index = grid.subgrids(i).list(0).ind(0,0) - 1;
            end_index = grid.subgrids(i).list(0).ind(ind_num-1,0) - 1;
            std::clog << std::left << setw(19) << "range: not found";
            array_size = ind_num;
        }
        int index_array[array_size];
        std::clog << "  index_Array size: " <<
            sizeof(index_array)/sizeof(*index_array) << std::endl;
        if(range_found == 1)
        {
            for(int j = start_index; j < end_index; j++)
            {
                index_array[j-start_index] = j;
            }
        } else
        {
            for(int j = 0; j < ind_num; j++)
            {
                jIndex = grid.subgrids(i).list(0).ind(j,0) - 1;
                index_array[j] = jIndex;
            }
        }

        int size = (sizeof(index_array)/sizeof(*index_array));

        vtkSmartPointer<vtkCellArray> subgridCellArray =
            vtkSmartPointer<vtkCellArray>::New();

        // ELECTRON TEMPERATURE creating array
        vtkSmartPointer<vtkDoubleArray> electronTemperatureArray =
            fSetValuesArrayBase(size, "Electron Temperature");

        // ELECTRON DENSITY creating array
        vtkSmartPointer<vtkDoubleArray> electronDensityArray =
            fSetValuesArrayBase(size, "Electron Density");

        // ELECTRIC POTENTIAL creating array
        vtkSmartPointer<vtkDoubleArray> electricPotentialArray =
            fSetValuesArrayBase(size, "Electric Potential");

        if(subgrid_class == 0)
        {
            // POINTS/NODES
            vtkSmartPointer<vtkUnstructuredGrid> subgridPointsUnstructuredGrid =
                 vtkSmartPointer<vtkUnstructuredGrid>::New();
            // Getting vertex colored by reading scalars from electron density
            // subgrids (nodes)
            int ne_subgrid_num = edge.fluid.ne.value.extent(0);
            for(int n = 0; n < ne_subgrid_num; n++)
            {
                int ne_subgrid_ind = edge.fluid.ne.value(n).subgrid;
                if(i+1 == edge.fluid.ne.value(n).subgrid)
                // +1 because in CPO index starts with 1 and not with 0
                // as in C++
                {
                    vtkSmartPointer<vtkCellArray> subgridVertices =
                        vtkSmartPointer<vtkCellArray>::New();
                    vtkSmartPointer<vtkVertex> subgridVertex =
                        vtkSmartPointer<vtkVertex>::New();

                    electronDensityArray->SetNumberOfValues(size);
                    for(int j = 0; j < size; j++)
                    {
                        points->InsertNextPoint(nodes.geo(index_array[j], 0),
                            nodes.geo(index_array[j], 1), 0.0);
                        subgridVertex->GetPointIds()->SetId(0, j);
                        subgridVertices->InsertNextCell(subgridVertex);
                        electronDensityArray->SetComponent(j, 0,
                            edge.fluid.ne.value(n).scalar(j));
                    }
                    // To add new array Electron Density (Cells) as unstructuredGrid
                    subgridPointsUnstructuredGrid->SetPoints(points);
                    subgridPointsUnstructuredGrid->SetCells(
                        VTK_VERTEX, subgridVertices);
                    subgridPointsUnstructuredGrid->GetCellData()->AddArray(
                        electronDensityArray);
                }
            }

            // Getting vertex colored by reading scalars from electron
            // temperature subgrids (nodes)
            int te_subgrid_num = edge.fluid.te.value.extent(0);
            for(int n = 0; n < te_subgrid_num; n++)
            {
                int te_subgrid_ind = edge.fluid.te.value(n).subgrid;
                if(i+1 == edge.fluid.te.value(n).subgrid)
                // +1 because in CPO index starts with 1 and not with 0
                // as in C++
                {
                    vtkSmartPointer<vtkCellArray> subgridVertices =
                        vtkSmartPointer<vtkCellArray>::New();
                    vtkSmartPointer<vtkVertex> subgridVertex =
                        vtkSmartPointer<vtkVertex>::New();
                    electronTemperatureArray->SetNumberOfValues(size);
                    for(int j = 0; j < size; j++)
                    {
                        points->InsertNextPoint(nodes.geo(index_array[j], 0),
                            nodes.geo(index_array[j], 1), 0.0);
                        subgridVertex->GetPointIds()->SetId(0, j);
                        subgridVertices->InsertNextCell(subgridVertex);
                        electronTemperatureArray->SetComponent(j, 0,
                            edge.fluid.te.value(n).scalar(j));
                    }

                    // To add new array Electron Temperature (Cells) as
                    // unstructuredGrid
                    subgridPointsUnstructuredGrid->SetPoints(points);
                    subgridPointsUnstructuredGrid->SetCells(
                        VTK_VERTEX, subgridVertices);
                    subgridPointsUnstructuredGrid->GetCellData()->AddArray(
                        electronTemperatureArray);
                }
            }
            // Getting vertex colored by reading scalars from ion density
            // subgrids (nodes)
            for(int k = 0; k < num_ni_species; k++)
            {
                std::string ion_charge = edge.species(k).label;
                stringstream ni_species_num2str;
                ni_species_num2str << k+1;
                string ni_species_num_str = ni_species_num2str.str();
                std::string ni_array_label;
                if (k < 9)
                {
                    ni_array_label = "Ion Density 0" + ni_species_num_str +
                        ion_charge;
                } else
                {
                    ni_array_label = "Ion Density " + ni_species_num_str +
                        ion_charge;
                }
                vtkSmartPointer<vtkDoubleArray> ionDensityArray =
                    fSetValuesArrayBase(size, ni_array_label);
                int ni_subgrid_num = edge.fluid.ni(k).value.extent(0);
                for(int n = 0; n < ni_subgrid_num; n++)
                {
                    int ni_subgrid_ind = edge.fluid.ni(k).value(n).subgrid;
                    if(i+1 == edge.fluid.ni(k).value(n).subgrid)
                    // +1 because in CPO index starts with 1 and not with 0
                    // as in C++
                    {
                        vtkSmartPointer<vtkCellArray> subgridVertices =
                            vtkSmartPointer<vtkCellArray>::New();
                        vtkSmartPointer<vtkVertex> subgridVertex =
                            vtkSmartPointer<vtkVertex>::New();
                        ionDensityArray->SetNumberOfValues(size);
                        for(int j = 0; j < size; j++)
                        {
                            points->InsertNextPoint(nodes.geo(index_array[j], 0),
                                nodes.geo(index_array[j], 1), 0.0);
                            subgridVertex->GetPointIds()->SetId(0, j);
                            subgridVertices->InsertNextCell(subgridVertex);
                            ionDensityArray->SetComponent(j, 0, edge.fluid.
                                ni(k).value(n).scalar(j));
                        }

                        // To add new array Electron Density (Cells) as unstructuredGrid
                        subgridPointsUnstructuredGrid->SetPoints(points);
                        subgridPointsUnstructuredGrid->SetCells(
                            VTK_VERTEX, subgridVertices);
                        subgridPointsUnstructuredGrid->GetCellData()->AddArray(
                            ionDensityArray);
                    }
                }
            }

            // Getting vertex colored by reading scalars from ion Temperature
            // subgrids (nodes)
            for(int k = 0; k < num_ti_species; k++)
            {
                vtkSmartPointer<vtkDoubleArray> ionTemperatureArray =
                    fSetValuesArrayBase(size, "Ion Temperature");
                int ti_subgrid_num = edge.fluid.ti(k).value.extent(0);
                for(int n = 0; n < ti_subgrid_num; n++)
                {
                    int ti_subgrid_ind = edge.fluid.ti(k).value(n).subgrid;
                    if(i+1 == edge.fluid.ti(k).value(n).subgrid)
                    // +1 because in CPO index starts with 1 and not with 0
                    // as in C++
                    {
                        vtkSmartPointer<vtkCellArray> subgridVertices =
                            vtkSmartPointer<vtkCellArray>::New();
                        vtkSmartPointer<vtkVertex> subgridVertex =
                            vtkSmartPointer<vtkVertex>::New();
                        ionTemperatureArray->SetNumberOfValues(size);
                        for(int j = 0; j < size; j++)
                        {
                            points->InsertNextPoint(
                                nodes.geo(index_array[j], 0),
                                nodes.geo(index_array[j], 1), 0.0);
                            subgridVertex->GetPointIds()->SetId(0, j);
                            subgridVertices->InsertNextCell(subgridVertex);
                            ionTemperatureArray->SetComponent(j, 0,
                                edge.fluid.ti(k).value(n).scalar(j));
                        }

                        // To add new array Electron Temperature (Cells)
                        // as unstructuredGrid
                        subgridPointsUnstructuredGrid->SetPoints(points);
                        subgridPointsUnstructuredGrid->SetCells(
                            VTK_VERTEX, subgridVertices);
                        subgridPointsUnstructuredGrid->GetCellData()->AddArray(
                            ionTemperatureArray);
                    }
                }
            }

            // Getting vertex colored by reading scalars from electric potential
            // subgrids (nodes): There is no data for electric potential nodes.
            int num_blocks = mainMB->GetNumberOfBlocks();
            mainMB->SetBlock(num_blocks, subgridPointsUnstructuredGrid);
            mainMB->GetMetaData((unsigned int) num_blocks)->Set(
                vtkCompositeDataSet::NAME(), subgridName[i].c_str());
        }
        else if(subgrid_class == 1) //LINES
        {
            vtkSmartPointer<vtkUnstructuredGrid> subgridLinesUnstructuredGrid =
                vtkSmartPointer<vtkUnstructuredGrid>::New();
            vtkSmartPointer<vtkCellArray> subgridLinesArray =
                vtkSmartPointer<vtkCellArray>::New();
            for(int j = 0; j < size; j++)
            {
                vtkSmartPointer<vtkLine> subgridLine =
                    vtkSmartPointer<vtkLine>::New();

                int line_ind_0 = edges.boundary(index_array[j],0) -1;
                int line_ind_1 = edges.boundary(index_array[j],1) -1;

                subgridLine ->GetPointIds()->SetId(0, line_ind_0);
                subgridLine ->GetPointIds()->SetId(1, line_ind_1);
                subgridLinesArray->InsertNextCell(subgridLine);
            }
            subgridLinesUnstructuredGrid->SetPoints(points);
            subgridLinesUnstructuredGrid->SetCells(VTK_LINE, subgridLinesArray);

            // Getting all subgrids to main block
            int num_blocks = mainMB->GetNumberOfBlocks();
            mainMB->SetBlock(num_blocks, subgridLinesUnstructuredGrid);
            mainMB->GetMetaData((unsigned int) num_blocks)->
                Set(vtkCompositeDataSet::NAME(), subgridName[i].c_str());
        }
        else if(subgrid_class == 2) //CELLS
        {
            for(int j = 0; j < size; j++)
            {
                subgridQuad->GetPointIds()->
                    SetId(0,all_cells[index_array[j]][0]);
                subgridQuad->GetPointIds()->
                    SetId(1,all_cells[index_array[j]][1]);
                subgridQuad->GetPointIds()->
                    SetId(2,all_cells[index_array[j]][2]);
                subgridQuad->GetPointIds()->
                    SetId(3,all_cells[index_array[j]][3]);
                subgridCellArray->InsertNextCell(subgridQuad);

                // ELECTRON DENSITY and ELECTRON TEMPERATURE
                electronDensityArray->SetComponent(j, 0,
                    edge.fluid.ne.value(0).scalar(index_array[j]));
                electronTemperatureArray->SetComponent(j, 0,
                    edge.fluid.te.value(0).scalar(index_array[j]));
                electricPotentialArray->SetComponent(j, 0,
                    edge.fluid.po.value(0).scalar(index_array[j]));
            }
            vtkSmartPointer<vtkUnstructuredGrid> subgridCellsUnstructuredGrid =
                vtkSmartPointer<vtkUnstructuredGrid>::New();

            subgridCellsUnstructuredGrid->SetPoints(points);
            subgridCellsUnstructuredGrid->SetCells(VTK_QUAD, subgridCellArray);

            // Setting Electron Density and Electron Temperature to
            // UnstructuredGrid
            subgridCellsUnstructuredGrid->GetCellData()->AddArray(
                electronTemperatureArray);
            subgridCellsUnstructuredGrid->GetCellData()->AddArray(
                electronDensityArray);
            subgridCellsUnstructuredGrid->GetCellData()->AddArray(
                electricPotentialArray);

            // ION DENSITY
            for(int k = 0; k < num_ni_species; k++)
            {
                std::string ion_charge = edge.species(k).label;
                stringstream ni_species_num2str;
                ni_species_num2str << k+1;
                string ni_species_num_str = ni_species_num2str.str();
                std::string ni_array_label;
                if (k < 9)
                {
                    ni_array_label = "Ion Density 0" + ni_species_num_str +
                        ion_charge;
                } else
                {
                    ni_array_label = "Ion Density " + ni_species_num_str +
                        ion_charge;
                }
                vtkSmartPointer<vtkDoubleArray> ionDensityArray =
                    fSetValuesArrayBase(size, ni_array_label);
                for(int j =0; j < size; j++)
                {
                    ionDensityArray->SetComponent(j, 0,
                        edge.fluid.ni(k).value(0).scalar(index_array[j]));
                }
                    subgridCellsUnstructuredGrid->GetCellData()->AddArray(
                        ionDensityArray);
            }

            // ION TEMPERATURE
            for(int k = 0; k < num_ti_species; k++)
            {
                vtkSmartPointer<vtkDoubleArray> ionTemperatureArray =
                    fSetValuesArrayBase(size, "Ion Temperature");
                for(int j =0; j < size; j++)
                {
                    ionTemperatureArray->SetComponent(j, 0,
                        edge.fluid.ti(k).value(0).scalar(index_array[j]));
                }
                subgridCellsUnstructuredGrid->GetCellData()->AddArray(
                    ionTemperatureArray);
            }

            // Getting all subgrids to main multiblockdataset block
            int num_blocks = mainMB->GetNumberOfBlocks();
            mainMB->SetBlock(num_blocks, subgridCellsUnstructuredGrid);
            mainMB->GetMetaData((unsigned int) num_blocks)->Set(
                vtkCompositeDataSet::NAME(), subgridName[i].c_str());
        }
    }
    output->ShallowCopy(mainMB);
    itm.close();
#endif // IMAS_IDS
    return 1;
}

void  ReadUALEdge::PrintSelf(ostream& os, vtkIndent indent)
{
    this->Superclass::PrintSelf(os, indent);
}

