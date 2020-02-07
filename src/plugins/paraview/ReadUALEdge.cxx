
/**
*-------------------------------------------------------------------------------
*   @file     ReadUALEdge.cxx
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the main C++ file of the ParaView ReadUALEdge file
*   DESCRIPTION
*   ParaView ReadUALEdge plugin is a tool used to visualize and analyze data,
*   obtained by fusion simulations stored IDS database.
*   The focus of plugin development is on data stored in 'edge_profiles',
*   'edge_sources' and 'edge_transport' IDSs.
*
*   Currently the included data fields are:
*       - grid geometry from any of the above IDSs;
*       - plasma state:
*           ~ edge_profiles:
*               - electrons:
*                   - temperature;
*                   - density;
*                   - density_fast;
*                   - pressure;
*                   - pressure_fast_perpendicular;
*                   - velocity:     @note: only for IMAS version <= 3.15.0
*                       - radial;
*                       - diamagnetic;
*                       - parallel;
*                       - poloidal;
*                       - toroidal;
*                   - distribution_function;
*               - ion:
*                   - temperature;
*                   - density;
*                   - density_fast;
*                   - pressure;
*                   - pressure_fast_perpendicular;
*                   - velocity:     @note: only for IMAS version <= 3.15.0
*                       - radial;
*                       - diamagnetic;
*                       - parallel;
*                       - poloidal;
*                       - toroidal;
*                   - distribution_function;
*           ~ edge_sources:
*               - electrons:
*                   - particles
*                   - energy
*               - ion:
*                   - particles
*                   - energy
*           ~ edge_transport:
*               - electrons:
*                   - particles:
*                       - d
*                       - v
*                       - flux
*                       - flux_limiter
*                   - energy:
*                       - d
*                       - v
*                       - flux
*                       - flux_limiter
*               - ion:
*                   - particles:
*                       - d
*                       - v
*                       - flux
*                       - flux_limiter
*                   - energy:
*                       - d
*                       - v
*                       - flux
*                       - flux_limiter
*           ~ mdh:
*               - TODO
*
*-------------------------------------------------------------------------------
*/

#include "ReadUALEdge.h"
#include <UALClasses.h>
//#include "readGmtryEdge.h"
#include "readGmtryEdge.cxx"
//#include "readPsEdge.h"
#include "readPsEdge.cxx"
#include <vtkCellArray.h>
#include <vtkCellData.h>
#include <vtkDataObject.h>
#include <vtkDoubleArray.h>
#include <vtkFloatArray.h>
#include <vtkInformation.h>
#include <vtkInformationVector.h>
#include <vtkIntArray.h>
#include <vtkLine.h>
#include <vtkMultiBlockDataSet.h>
#include <vtkObjectFactory.h>
#include <vtkOutputWindow.h>
#include <vtkPointData.h>
#include <vtkPoints.h>
#include <vtkPolyData.h>
#include <vtkQuad.h>
#include <vtkSmartPointer.h>
#include <vtkStringArray.h>
#include <vtkTable.h>
#include <vtkUnstructuredGrid.h>
#include <vtkVersion.h>
#include <vtkVertex.h>
#include <vtkTriangle.h>
#include <fstream>
#include <iostream>
#include <string>
#include <sys/stat.h>
#include <tuple>
#include <unistd.h>
#include <vector>

#define IMAS_IDS
#define PLUGIN_IMAS_VERSION_DIGIT IMAS_VERSION_DIGIT

// From $IMAS_PREFIX/include/cpp/coordinate_identifier.h
// TODO: do not define coordtypes again. Use those from coordinate_identifier
//       now that they're available from there
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
    this->Shot = 0;
    this->Run = 0;
    this->User = NULL;
    this->Device = NULL;
    this->Version = NULL;
    this->RefRun = 0;
    this->LoadIDS = NULL;
    this->GridGGDslice = 0;
    this->GGDslice = 0;
    this->EdgeTransportModelID = 0;
    this->EdgeSourcesSourceID = 0;
    this->IDSPlasmaStateSource = NULL;
    this->GridForm = NULL;
    this->SetNumberOfInputPorts(0);
    this->SetNumberOfOutputPorts(1);
    this->DebugOff();
    this->stringArray=vtkSmartPointer<vtkStringArray>::New();
}

/* Function used to display complex message in ParaView 'Output Message'
* window with the use of stringstream
* @param msg        Message text to display
* @param ms_type    message type (info/error/warning)
*/
void msgToOutputWindow( std::stringstream& msg, std::string msg_type = "info" )
{
    const std::string msg_str = msg.str();
    const char* msg_cstr = msg_str.c_str();

    if (msg_type == "info" || msg_type == "i")
    {
        vtkOutputWindowDisplayText(msg_cstr);
    }
    else if (msg_type == "error" || msg_type == "e")
    {
        vtkOutputWindowDisplayErrorText(msg_cstr);
    }
    else if (msg_type == "warning" || msg_type == "w")
    {
        vtkOutputWindowDisplayWarningText(msg_cstr);
    }
    else
    {
        vtkOutputWindowDisplayWarningText("Warning: Output Window message type "
            "not found!");
    }
    // Clean stringstream
    msg.str(std::string());
}

/**
*   Function to add unstructured grid to main VTK multiblock
*   @param  MB  Main VTK MultiBlock Data Set object
*   @param  UG  VTK Unstructured Grid to add as bloc to MultiBlock
*   @param  gridSubset_name     Block label
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
    // Get the info object
    vtkInformation *outInfo = outputVector->GetInformationObject(0);

    // If PromptUser is set to true then each time a line of text is displayed,
    // the user is asked if they want to keep getting messages.
    vtkOutputWindow::GetInstance()->PromptUserOff();
    // Set stringstream to be used for displaying more complex messages to
    // ParaView 'Output messages' window
    std::stringstream msg;

#ifdef IMAS_IDS
    using namespace IdsNs;

#if IMAS_VERSION_DIGIT <= 3151
    msgToOutputWindow("This plugin was compiled using ancient version of IMAS "
        "which shouldn't be used anymore (3.15.0 or older)! Due for this reason"
        "this plugin does not support those versions of IMAS (and DD) anymore",
        "warning" );
#endif


    // Check IMAS and UAL version
    std::string load_IV = getenv("IMAS_VERSION");
    std::string load_UV = getenv("UAL_VERSION");

    // Get IMAS version digit, used to compile the plugin, as a string
    // (e.g. 3150 -> 3.15.0)
    std::string plugin_IV = std::to_string(PLUGIN_IMAS_VERSION_DIGIT);
    int load_IV_DIGIT = 0;
    std::string load_IV_str;
    if( plugin_IV.length() == 3 )
    {
        plugin_IV = std::string() + plugin_IV[0] + "." + plugin_IV[1] + "." +
            plugin_IV[2];
        // Get currently loaded IMAS version as an integer (e.g. 3.5.0 -> 350)
        load_IV_str = std::string() + load_IV[0] + load_IV[2] + load_IV [4];
        load_IV_DIGIT = std::stoi( load_IV_str );
    }
    else if( plugin_IV.length() == 4 )
    {
        plugin_IV = std::string() + plugin_IV[0] + "." + plugin_IV[1] +
            plugin_IV [2] + "." + plugin_IV[3];
        // Get currently loaded IMAS version as an integer (e.g. 3.15.0 -> 3150)
        load_IV_str = std::string() + load_IV[0] + load_IV[2] + load_IV[3]
            + load_IV[5];
        load_IV_DIGIT = std::stoi( load_IV_str );
    }
    // Latest IMAS version, for which it is confirmed the ReadUALEdgeplugin is
    // compatible with ( in single integer form )
    std::string IV_latest_string = "3.26.0";
    int IV_latest_DIGIT = 3260;

    // Display IMAS and UAL versions
    vtkOutputWindowDisplayText(std::string("LOADED IMAS VERSION: " + load_IV +
        "\n").c_str());
    vtkOutputWindowDisplayText(std::string("LOADED UAL VERSION: " + load_UV +
        "\n").c_str());
    vtkOutputWindowDisplayText(std::string("PLUGIN IMAS VERSION: " + plugin_IV +
        "\n\n").c_str());

    // IMAS version checks
    if( load_IV_DIGIT < IV_latest_DIGIT )
    {
        vtkOutputWindowDisplayWarningText("WARNING! This IMAS (and "
            "consequently Data Dictionary) is outdated! ReadUALEdge plugin "
            "might not be fully compatible with the currently loaded Data "
            "Dictionary! The latest IMAS module, confirmed to be compatible "
            "with the ReadUALEdge plugin, is IMAS/3.26.0/UAL/4.4.0 while the "
            "oldest is IMAS/3.17.0/UAL/3.8.0. Using the last confirmed "
            "compatible IMAS version is recommended. \n\n");
    }
    if( load_IV_DIGIT != PLUGIN_IMAS_VERSION_DIGIT )
    {
        vtkOutputWindowDisplayWarningText("WARNING! For best practice it is "
            "recommended that the same IMAS/DD version is used for writing "
            "the IDSs, compiling the ReadUALEdge plugin and then for loading "
            "the plugin within the ParaView application. \n\n");
    }
    if( PLUGIN_IMAS_VERSION_DIGIT < IV_latest_DIGIT)
    {
        vtkOutputWindowDisplayWarningText("WARNING! The IMAS version (and "
            "consequently Data Dictionary), used to compile the ReadUALEdge "
            "plugin, is outdated! The latest IMAS module, confirmed to be "
            "compatible with the ReadUALEdge, is IMAS/3.26.0/UAL/4.4.0 while "
            "the oldest is IMAS/3.17.0/UAL/3.8.0. Using the last confirmed "
            "compatible IMAS version is recommended.\n\n");
    }

    vtkOutputWindowDisplayText("Reading IDS \n");

    // Set IDSs shot and run
    IDS db(this->Shot, this->Run, this->Shot, this->RefRun);
    if (!this->Version)
        this->Version = strdup("3");
    // Open IDS
    db.openEnv(this->User, this->Device, this->Version);

    // Print IDS info
    msg  << "IDS parameters:" << "\n" <<
        " - Loaded IDS: " << this->LoadIDS << "\n" <<
        " - Shot:       " << this->Shot    << "\n" <<
        " - Run:        " << this->Run     << "\n" <<
        " - RefRun:     " << this->RefRun  << "\n" <<
        " - User:       " << this->User    << "\n" <<
        " - Device:     " << this->Device  << "\n" <<
        " - Version:    " << this->Version << "\n\n";
    msgToOutputWindow( msg );

    // Set default variable to hold the IDS source for plasma state data fields
    // (can be specified by the IDSPlasmaDataSource advanced option)
    std::string IDS_plasmaStateSource = "edge_profiles";

    if( std::string(this->IDSPlasmaStateSource) == "Same as 'Read from IDS'")
    {
        IDS_plasmaStateSource = std::string(this->LoadIDS);
    }
    else
    {
        IDS_plasmaStateSource = std::string(this->IDSPlasmaStateSource);
    }

    // Get GRID GGD structure array index to internal variable
    int grid_ggd_slice_index = this->GridGGDslice;
    // Get GGD structure array index to internal variable
    int ggd_slice_index = this->GGDslice;
    // Get edge_sources.source(:) structure array index to internal variable
    int source_index = this->EdgeSourcesSourceID;
    // Get edge_transport.model(:) structure array index to internal variable
    int model_index = this->EdgeTransportModelID;

    // Set default number of GRID_GGD slices
    int num_gridggd_slices = 0;
    // Set default number of grid subsets
    int num_gridSubset = 0;
    // Set default number of GGD slices
    int num_ggd_slices = 0;

    if( std::string(this->LoadIDS).find("edge_profiles") != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_profiles IDS. \n");
        db._edge_profiles.get();
        num_gridggd_slices = db._edge_profiles.grid_ggd.extent(0);
        // Get number of grid subsets in the selected IDS
        num_gridSubset = db._edge_profiles.
            grid_ggd(grid_ggd_slice_index).grid_subset.extent(0);
        // Get number of GGD slices
        num_ggd_slices = db._edge_profiles.ggd.extent(0);

    }
    else if( std::string(this->LoadIDS).find("edge_sources")
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_sources IDS. \n");
        db._edge_sources.get();
        num_gridggd_slices = db._edge_sources.grid_ggd.extent(0);
        // Get number of grid subsets in the selected IDS
        num_gridSubset = db._edge_sources.grid_ggd(grid_ggd_slice_index).
            grid_subset.extent(0);
        // Get number of GGD slices
        num_ggd_slices = db._edge_sources.source(source_index).ggd.extent(0);
    }
    else if( std::string(this->LoadIDS).find("edge_transport")
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_transport IDS. \n");
        db._edge_transport.get();
        num_gridggd_slices = db._edge_transport.grid_ggd.extent(0);
        // Get number of grid subsets in the selected IDS
        num_gridSubset = db._edge_transport.grid_ggd(grid_ggd_slice_index).
            grid_subset.extent(0);
        // Get number of GGD slices
        num_ggd_slices = db._edge_transport.model(model_index).ggd.extent(0);

    }
    else if( std::string(this->LoadIDS).find("mhd")
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading mhd IDS. \n");
        db._mhd.get();
        num_gridggd_slices = db._mhd.grid_ggd.extent(0);
        // Get number of grid subsets in the selected IDS
        num_gridSubset = db._mhd.grid_ggd(grid_ggd_slice_index).
            grid_subset.extent(0);
        // Get number of GGD slices
        num_ggd_slices = db._mhd.ggd.extent(0);
    }

    // Get plasma state from one of the IDSs
    if( std::string(LoadIDS).find("edge_profiles")
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("GGD check: edge_profiles IDS. \n");
        // db._edge_profiles.get();
    }
    else if( std::string(LoadIDS).find( "edge_sources" )
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("GGD check: edge_sources IDS. \n");
        // db._edge_sources.get();
    }
    else if( std::string(LoadIDS).find( "edge_transport" )
        != std::string::npos )
    {
        vtkOutputWindowDisplayText(std::string("GGD check: edge_transport IDS "
            "(not yet implemented). \n").c_str());
        // db._edge_transport.get();
    }
    else if( std::string(LoadIDS).find( "mhd" )
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("GGD check: mhd IDS. \n");
        // db._mhd.get();
    }

    // Set object to readGmtryEdge class
    readGmtryEdge gmtrye_obj;
    //
    gmtrye_obj.ggdCheck(db, IDS_plasmaStateSource, grid_ggd_slice_index,
                        ggd_slice_index);

    // Get the geometry/coordinates of all nodes/points N[R, Z]
    // forming this grid using routine 'setVtkPoints'
    vtkSmartPointer<vtkPoints> obj_0D_vtkPointsArray = gmtrye_obj.setVtkPoints(
        db,
        std::string(this->LoadIDS),
        grid_ggd_slice_index,
        this->EdgeSourcesSourceID,
        this->EdgeTransportModelID);

    // Object declaration for readPsEdge routines
    readPsEdge pse_obj;

    // Represent grid as grid subsets or as a single unstructured grid
    if( std::string(GridForm).find("Grid subsets") != std::string::npos)
    {
        vtkOutputWindowDisplayText("Representation as 'Grid subsets' selected.");

        vtkSmartPointer<vtkMultiBlockDataSet> mainMB =
            vtkSmartPointer<vtkMultiBlockDataSet>::New();

        // Print total number of grid subsets
        vtkOutputWindowDisplayText(std::string("Total number of grid subsets: " +
            std::to_string(num_gridSubset) + "\n").c_str());

        // Set a list of grid subset index, to follow which one were already set
        vector<int> list_gs_indices;

        // Loop through all grid subsets and extract data for each
        for(int i = 0; i < num_gridSubset; i++)
        {
            std::string gridSubset_name;
            int gridSubset_index;

            // Current grid subset index
            vtkOutputWindowDisplayText(std::string("-----Grid subset No " +
                std::to_string(i+1) + " ----- \n").c_str());

            if( std::string(LoadIDS).find("mhd") != std::string::npos )
            {
                gridSubset_name = db._mhd.
                    grid_ggd(grid_ggd_slice_index).grid_subset(i).identifier.name;
                gridSubset_index= db._mhd.
                    grid_ggd(grid_ggd_slice_index).grid_subset(i).identifier.index;

            }else if( std::string(LoadIDS).find("edge_sources") != std::string::npos )
            {
                gridSubset_name = db._edge_sources.
                    grid_ggd(grid_ggd_slice_index).grid_subset(i).identifier.name;
                gridSubset_index= db._edge_sources.
                    grid_ggd(grid_ggd_slice_index).grid_subset(i).identifier.index;
            }else
            {
                gridSubset_name = db._edge_profiles.
                    grid_ggd(grid_ggd_slice_index).grid_subset(i).identifier.name;
                gridSubset_index= db._edge_profiles.
                    grid_ggd(grid_ggd_slice_index).grid_subset(i).identifier.index;
            }

            // Print grid subset info
            vtkOutputWindowDisplayText(std::string(" - Index: " +
                std::to_string(gridSubset_index) + "\n").c_str());
            vtkOutputWindowDisplayText(std::string(" - Name: " + gridSubset_name +
                "\n").c_str());

            // Grid subset index check
            if (std::find(list_gs_indices.begin(),
                list_gs_indices.end(), gridSubset_index) != list_gs_indices.end())
            {
                // If a grid subset with the same grid_subset_index
                // was already set, skip the 'duplicate' grid subset
                vtkOutputWindowDisplayWarningText(std::string(
                    "WARNING: A grid subset with the same associated "
                    "grid_subset_index (" + std::to_string(gridSubset_index) +
                    "as the current grid subset was already set. Two grid subsets "
                    "SHOULD NOT share the same grid_subset_index! "
                    "Skipping current grid subset. \n").c_str());

                continue;
            }
            else if (gridSubset_index == 0)
            {
                vtkOutputWindowDisplayWarningText(
                    "WARNING: A grid subset with index 0 was found. 0 is invalid "
                    "index was found (first index must start with 1). "
                    "Skipping the 'duplicate' grid subset. \n");
                // exit(0);
                continue;
            }
            else
            {
                list_gs_indices.push_back(gridSubset_index);
            }

            // Get size/number of elements forming current grid subset
            int num_gridSubset_el;
            if( std::string(LoadIDS).find("mhd") != std::string::npos )
            {
                num_gridSubset_el = db._mhd.grid_ggd(grid_ggd_slice_index).
                    grid_subset(i).element.extent(0);
            }else if( std::string(LoadIDS).find("edge_sources") != std::string::npos )
            {
                num_gridSubset_el = db._edge_sources.grid_ggd(grid_ggd_slice_index).
                    grid_subset(i).element.extent(0);
            }else
            {
                num_gridSubset_el = db._edge_profiles.grid_ggd(grid_ggd_slice_index).
                    grid_subset(i).element.extent(0);
            }

            // Check if there are any elements in grid_subset
            if (num_gridSubset_el == 0)
            {
                vtkOutputWindowDisplayWarningText(std::string(
                    "WARNING: Current grid subset does not contain any elements! "
                    "Skipping current grid subset. \n").c_str());

                continue;
            }

            // Get dimension of the objects forming this grid subset
            int gridSubset_obj_cls;
            if( std::string(LoadIDS).find("mhd") != std::string::npos )
            {
                gridSubset_obj_cls = db._mhd.grid_ggd(grid_ggd_slice_index).
                        grid_subset(i).element(0).object(0).dimension;
            }
            else if( std::string(LoadIDS).find("edge_sources") != std::string::npos )
            {
                gridSubset_obj_cls = db._edge_sources.grid_ggd(grid_ggd_slice_index).
                        grid_subset(i).element(0).object(0).dimension;
            }else
            {
                gridSubset_obj_cls = db._edge_profiles.grid_ggd(grid_ggd_slice_index).
                    grid_subset(i).element(0).object(0).dimension;
            }
            int gridSubset_obj_dim;
            gridSubset_obj_dim = gridSubset_obj_cls - 1;

            // Print grid subset info
            vtkOutputWindowDisplayText(std::string(" - Class: " +
                std::to_string(gridSubset_obj_cls) + "\n").c_str());
            vtkOutputWindowDisplayText(std::string(" - Dimension: " +
                std::to_string(gridSubset_obj_dim) + "\n").c_str());
            vtkOutputWindowDisplayText(std::string(" - Number of elements: " +
                std::to_string(num_gridSubset_el) + "\n").c_str());

            // ------ SET POINTS/NODES -----
            if (gridSubset_obj_cls == 1)
            {
                // Set vtkUnstructuredGrid dataset for grid subset, containing
                // only 0D objects
                vtkSmartPointer<vtkUnstructuredGrid> gridSubsetPointsUnstructuredGrid =
                    vtkSmartPointer<vtkUnstructuredGrid>::New();

                // Set grid subset 0D geometry to vtkUnstructuredGrid
                gmtrye_obj.setGridSubset0DGeometry2UnstructuredGrid(
                    std::string(this->LoadIDS),
                    db,
                    gridSubsetPointsUnstructuredGrid,
                    obj_0D_vtkPointsArray,
                    grid_ggd_slice_index,
                    i);

                if (num_ggd_slices > 0)
                {
                    // Set data fields to vtkunstructuredGrid for selected IDS with the
                    // help of 'setUnstructuredGridDataFields' routine
                    pse_obj.setUnstructuredGridDataFields(
                        gridSubsetPointsUnstructuredGrid,
                        db,
                        gridSubset_index,
                        num_gridSubset_el,
                        IDS_plasmaStateSource,
                        ggd_slice_index,
                        this->EdgeSourcesSourceID,
                        this->EdgeTransportModelID);
                }

                // Add unstructured grid to main block
                fAddBlock2MultiBlock( mainMB, gridSubsetPointsUnstructuredGrid,
                    gridSubset_name );
            }
            // ------ SET LINES -----
            else if (gridSubset_obj_cls == 2)
            {
                vtkSmartPointer<vtkUnstructuredGrid> gridSubsetLinesUnstructuredGrid =
                    vtkSmartPointer<vtkUnstructuredGrid>::New();

                // Set grid subset 1D geometry to vtkUnstructuredGrid
                gmtrye_obj.setGridSubset1DGeometry2UnstructuredGrid(
                    std::string(this->LoadIDS),
                    db,
                    gridSubsetLinesUnstructuredGrid,
                    obj_0D_vtkPointsArray,
                    ggd_slice_index,
                    i);

                // Add unstructured grid to main block
                fAddBlock2MultiBlock(mainMB, gridSubsetLinesUnstructuredGrid,
                    gridSubset_name );
            }
            //------ SET 2D CELLS -----
            else if (gridSubset_obj_cls == 3)
            {
                // Set vtk array for 2D cells
                vtkSmartPointer<vtkUnstructuredGrid> gridSubsetCellsUnstructuredGrid =
                    vtkSmartPointer<vtkUnstructuredGrid>::New();

                // Set grid subset 2D geometry to vtkUnstructuredGrid
                gmtrye_obj.setGridSubset2DGeometry2UnstructuredGrid(
                    std::string(this->LoadIDS),
                    db,
                    gridSubsetCellsUnstructuredGrid,
                    obj_0D_vtkPointsArray,
                    grid_ggd_slice_index,
                    i,
                    gridSubset_obj_cls);

                if (num_ggd_slices > 0)
                {

                    // Set data fields to vtkunstructuredGrid for selected IDS with the
                    // help of 'setUnstructuredGridDataFields' routine
                    pse_obj.setUnstructuredGridDataFields(
                        gridSubsetCellsUnstructuredGrid,
                        db,
                        gridSubset_index,
                        num_gridSubset_el,
                        IDS_plasmaStateSource,
                        ggd_slice_index,
                        this->EdgeSourcesSourceID,
                        this->EdgeTransportModelID);
                }

                // Add unstructured grid to main block
                fAddBlock2MultiBlock(mainMB, gridSubsetCellsUnstructuredGrid,
                    gridSubset_name );
            }

            vtkOutputWindowDisplayText(std::string("Setting grid subset No " +
                std::to_string(i+1) + " completed \n").c_str());
        }

        // Set the output format
        vtkMultiBlockDataSet *outputMB = vtkMultiBlockDataSet::SafeDownCast(
            outInfo->Get(vtkMultiBlockDataSet::DATA_OBJECT()));
        // Make shallow copy of the output (passes it to ParaView)
        outputMB->ShallowCopy(mainMB);

    }else if( std::string(GridForm).find("Single grid") != std::string::npos){
        vtkOutputWindowDisplayText("Representation as a 'Single grid' selected.");

        // Get dimension of the grid (up to 3D)
        // Note: Looking only in the first space (grid_ggd(:).space(0))
        int max_dim = 4; // HARDCODED!
        int num_nD_obj[4];
        int num_0D_obj = 0;
        int num_1D_obj = 0;
        int num_2D_obj = 0;
        int num_3D_obj = 0;

        if( std::string(LoadIDS).find("mhd") != std::string::npos )
        {
            class IdsNs::IDS::mhd::grid_ggd & GRID_GGD =
                db._mhd.grid_ggd(grid_ggd_slice_index);
            // auto GRID_GGD = db._mhd.grid_ggd(grid_ggd_slice_index);
            gmtrye_obj.getNumberOfNDimObjects(GRID_GGD, num_nD_obj);
        }
        else if( std::string(LoadIDS).find("edge_profiles") != std::string::npos )
        {
            class IdsNs::IDS::edge_profiles::grid_ggd & GRID_GGD =
                db._edge_profiles.grid_ggd(grid_ggd_slice_index);
            // auto GRID_GGD = db._edge_profiles.grid_ggd(grid_ggd_slice_index);
            gmtrye_obj.getNumberOfNDimObjects(GRID_GGD, num_nD_obj);
        }
        else if( std::string(LoadIDS).find("edge_sources") != std::string::npos )
        {
            class IdsNs::IDS::edge_sources::grid_ggd & GRID_GGD =
                db._edge_sources.grid_ggd(grid_ggd_slice_index);
            gmtrye_obj.getNumberOfNDimObjects(GRID_GGD, num_nD_obj);
        }else{
            vtkOutputWindowDisplayWarningText(std::string(
                "WARNING: Unknown IDS provided.").c_str());
        }

        num_0D_obj = num_nD_obj[0];
        num_1D_obj = num_nD_obj[1];
        num_2D_obj = num_nD_obj[2];
        num_3D_obj = num_nD_obj[3];

        vtkOutputWindowDisplayText(std::string(" - Dimension: "
            + std::to_string(max_dim-1) + "D\n").c_str());
        vtkOutputWindowDisplayText(std::string(" - Number of 0D objects: "
            + std::to_string(num_0D_obj) + "\n").c_str());
        vtkOutputWindowDisplayText(std::string(" - Number of 1D objects: "
            + std::to_string(num_1D_obj) + "\n").c_str());
        vtkOutputWindowDisplayText(std::string(" - Number of 2D objects: "
            + std::to_string(num_2D_obj) + "\n").c_str());
        vtkOutputWindowDisplayText(std::string(" - Number of 3D objects: "
            + std::to_string(num_3D_obj) + "\n").c_str());

        // NOTE: UnstructuredGrid cannot be set as the output, as in the
        //       C++ header file the vtkMultiBlockDataSetAlgorithm is being set
        //       (plugin CANNOT USE both vtkMultiBlockDataSetAlgorithm and
        //       vtkUnstructuredGridAlgorithm AT THE SAME TIME!)
        //       Due to that a single full unstructured grid will be passed as
        //       a block to multiblock dataset.
        vtkSmartPointer<vtkMultiBlockDataSet> mainMB =
            vtkSmartPointer<vtkMultiBlockDataSet>::New();

        vtkSmartPointer<vtkUnstructuredGrid> UG =
             vtkSmartPointer<vtkUnstructuredGrid>::New();

        // Points are mandatory. Set points (but not vertices) and PointData
        if (max_dim > 0)
        {
            int dim = 0;
            // Set vtkVertex vtk data type
            vtkSmartPointer<vtkVertex> vertex =
                vtkSmartPointer<vtkVertex>::New();

            // Set points
            UG->SetPoints(obj_0D_vtkPointsArray);

            // gmtrye_obj.insertVTKCells2UnstructuredGrid(dim, vertex,
            //     db._edge_profiles.grid_ggd(grid_ggd_slice_index), UG);

            if (num_ggd_slices > 0)
            {

                // Set data fields to vtkunstructuredGrid for selected IDS with
                // the help of 'setUnstructuredGridDataFields' routine
                // NOTE: grid_subsetIndex = 0 is being used to use this routine
                //       in an alternative way - not checking grid subsets, but
                //       the grid_ggd(:).space(:).objects_per_dimension(:)...
                //       directly (intended for meshes that don't use/have
                //       grid subsets)
                pse_obj.setUnstructuredGridDataFields(
                    UG,
                    db,
                    0,
                    num_0D_obj,
                    IDS_plasmaStateSource,
                    ggd_slice_index,
                    this->EdgeSourcesSourceID,
                    this->EdgeTransportModelID);
            }
        }

        if( std::string(LoadIDS).find("edge_profiles") != std::string::npos )
        {

            if (max_dim-1 == 1)
            {
                int dim = 1;
                // Set vtkLine vtk data type
                vtkSmartPointer<vtkLine> line = vtkSmartPointer<vtkLine>::New();
                gmtrye_obj.insertVTKCells2UnstructuredGrid(dim, line,
                    db._edge_profiles.grid_ggd(grid_ggd_slice_index), UG);

            }
            if (max_dim-1 >= 2)
            {
                // NOTE: Max 2D supported!
                int dim = 2;
                // Get number of nodes per object (to determine to use either
                // vtkTriangle (3 nodes) or vtkQuad (4 nodes))
                int num_obj_nodes =
                    db._edge_profiles.grid_ggd(grid_ggd_slice_index).space(0).
                    objects_per_dimension(dim).object(0).nodes.extent(0);

                if (num_obj_nodes == 3)
                {
                // Set vtkTriangle vtk data type
                vtkSmartPointer<vtkTriangle> triangle =
                    vtkSmartPointer<vtkTriangle>::New();
                gmtrye_obj.insertVTKCells2UnstructuredGrid(dim, triangle,
                    db._edge_profiles.grid_ggd(grid_ggd_slice_index), UG);

                }else if (num_obj_nodes == 4)
                {
                // Set vtkQuad vtk data type
                vtkSmartPointer<vtkQuad> quad = vtkSmartPointer<vtkQuad>::New();
                gmtrye_obj.insertVTKCells2UnstructuredGrid(dim, quad,
                    db._edge_profiles.grid_ggd(grid_ggd_slice_index), UG);
                }
            }
        }else if( std::string(LoadIDS).find("mhd") != std::string::npos )
        {

            if (max_dim-1 == 1)
            {
                int dim = 1;
                // Set vtkLine vtk data type
                vtkSmartPointer<vtkLine> line = vtkSmartPointer<vtkLine>::New();
                gmtrye_obj.insertVTKCells2UnstructuredGrid(dim, line,
                    db._mhd.grid_ggd(grid_ggd_slice_index), UG);

            }
            if (max_dim-1 >= 2)
            {
                // NOTE: Max 2D supported!
                int dim = 2;
                // Get number of nodes per object (to determine to use either
                // vtkTriangle (3 nodes) or vtkQuad (4 nodes))
                int num_obj_nodes =
                    db._mhd.grid_ggd(grid_ggd_slice_index).space(0).
                    objects_per_dimension(dim).object(0).nodes.extent(0);

                if (num_obj_nodes == 3)
                {
                // Set vtkTriangle vtk data type
                vtkSmartPointer<vtkTriangle> triangle =
                    vtkSmartPointer<vtkTriangle>::New();
                gmtrye_obj.insertVTKCells2UnstructuredGrid(dim, triangle,
                    db._mhd.grid_ggd(grid_ggd_slice_index), UG);

                }else if (num_obj_nodes == 4)
                {
                // Set vtkQuad vtk data type
                vtkSmartPointer<vtkQuad> quad = vtkSmartPointer<vtkQuad>::New();
                gmtrye_obj.insertVTKCells2UnstructuredGrid(dim, quad,
                    db._mhd.grid_ggd(grid_ggd_slice_index), UG);
                }
            }
        }else{
            vtkOutputWindowDisplayWarningText(std::string(
                "WARNING: Trying to read IDS with empty/unsupported GRID_GGD."
                ).c_str());
        }

        // Add unstructured grid to main block
        fAddBlock2MultiBlock(mainMB, UG, "Full Unstructured Grid" );

        // Set the output format
        vtkMultiBlockDataSet *outputMB = vtkMultiBlockDataSet::SafeDownCast(
            outInfo->Get(vtkMultiBlockDataSet::DATA_OBJECT()));
        // Make shallow copy of the output (passes it to ParaView)
        outputMB->ShallowCopy(mainMB);

    }else{
        vtkOutputWindowDisplayText("Neither grid representation as grid subsets"
            " or as a single unstructured grid was initiated. NOTHING WAS "
            " PASSED TO PARAVIEW!");
    }

    // Close IMAS database
    db.close();

#else
    msgToOutputWindow("This plugin supports only IMAS and IDSs. There is no "
        "CPO support.", "warning" );

#endif // IMAS_IDS
    return 1;
}

void  ReadUALEdge::PrintSelf(ostream& os, vtkIndent indent)
{
    this->Superclass::PrintSelf(os, indent);
}

