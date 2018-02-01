
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
*   Currently the plugin allows to display:
*       - grid geometry from any of the above IDSs;
*       - plasma state:
*           ~ edge_profiles:
*               - electrons:
*                   - temperature;
*                   - density;
*                   - density_fast;
*                   - pressure;
*                   - pressure_fast_perpendicular;
*                   - velocity:
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
*                   - velocity:
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
*                   - particles - flux
*                   - energy - flux
*               - ion:
*                   - particles - flux
*                   - energy - flux
*
*-------------------------------------------------------------------------------
*/

#include "ReadUALEdge.h"
#include <UALClasses.h>
#include "read_gmtry_edge.h"
#include "read_gmtry_edge.cxx"
#include "read_ps_edge.h"
#include "read_ps_edge.cxx"
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
    this->Shot = 0;
    this->Run = 0;
    this->User = NULL;
    this->Device = NULL;
    this->Version = NULL;
    this->RefRun = 0;
    this->LoadIDS = NULL;
    this->GGDslice = 0;
    this->EdgeTransportModelID = 0;
    this->EdgeSourcesSourceID = 0;
    this->IDSGridSource = NULL;
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
    // Get the output
    vtkMultiBlockDataSet *output = vtkMultiBlockDataSet::SafeDownCast(
        outInfo->Get(vtkMultiBlockDataSet::DATA_OBJECT()));

    // If PromptUser is set to true then each time a line of text is displayed,
    // the user is asked if they want to keep getting messages.
    vtkOutputWindow::GetInstance()->PromptUserOff();
    // Set stringstream to be used for displaying more complex messages to
    // ParaView 'Output messages' window
    std::stringstream msg;

#ifdef IMAS_IDS
    using namespace IdsNs;

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
    std::string IV_latest_string = "3.15.0";
    int IV_latest_DIGIT = 3150;

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
            "with the ReadUALEdge plugin, is imas/3.15.0/ual/3.6.4 while the "
            "oldest is imas/3.8.0/ual/3.5.0. \n\n");
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
            "compatible with the ReadUALEdge, is imas/3.15.0/ual/3.6.4 while "
            "the oldest is imas/3.8.0/ual/3.5.0. \n\n");
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

    // Get all three IDS databases
    db._edge_profiles.get();
    db._edge_sources.get();
    db._edge_transport.get();

    // Get GGD structure array index to internal variable
    int ggd_slice_index = this->GGDslice;
    // Get edge_sources.source(:) structure array index to internal variable
    int source_index = this->EdgeSourcesSourceID;
    // Get edge_transport.model(:) structure array index to internal variable
    int model_index = this->EdgeTransportModelID;

    // Get grid geometry from one of the IDSs (currently ready from
    // edge_profiles IDS only!)
    // TODO: Implement IDSGridSource.
    // db._edge_profiles.get();

    // Set class shortcuts for IDS substructures
//     class IDS::edge_profiles & edge_profiles = db._edge_profiles;
//     // class IDS::edge_sources  & edge_sources = db._edge_sources;
//     // class IDS::edge_transport  & edge_transport = db._edge_transport;
//     class IDS::edge_profiles::ggd & ggd = edge_profiles.ggd(ggd_slice_index);

// #if IMAS_VERSION_DIGIT >= 3151
//     class IDS::edge_profiles::grid_ggd & grid = edge_profiles.grid_ggd(0);
//     class IDS::edge_profiles::grid_ggd::space & space = grid.space(0);
// #else
//     class IDS::edge_profiles::ggd::grid & grid = ggd.grid;
//     class IDS::edge_profiles::ggd::grid::space & space = grid.space(0);
// #endif

    // Get number of grid subsets
    int num_gridSubset = 0;

#if IMAS_VERSION_DIGIT >= 3151
    if( std::string(IDSGridSource).find("edge_profiles") != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_profiles IDS. \n");
        // db._edge_profiles.get();
        // Get number of grid subsets in the selected IDS
        // (IDSGridSource selection box)
        num_gridSubset = db._edge_profiles.
            grid_ggd(ggd_slice_index).grid_subset.extent(0);
    }
    else if( std::string(IDSGridSource).find("edge_sources")
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_sources IDS. \n");
        // db._edge_sources.get();
        // Get number of grid subsets in the selected IDS
        // (IDSGridSource selection box)
        num_gridSubset = db._edge_sources.grid_ggd(ggd_slice_index).
            grid_subset.extent(0);
    }
    else if( std::string(IDSGridSource).find("edge_transport")
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_transport IDS. \n");
        // db._edge_transport.get();
        // Get number of grid subsets in the selected IDS
        // (IDSGridSource selection box)
        num_gridSubset = db._edge_transport.grid_ggd(ggd_slice_index).
            grid_subset.extent(0);
    }

#else

    if( std::string(IDSGridSource).find("edge_profiles") != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_profiles IDS. \n");
        // db._edge_profiles.get();
        // Get number of grid subsets in the selected IDS
        // (IDSGridSource selection box)
        num_gridSubset = db._edge_profiles.
            ggd(ggd_slice_index).grid.grid_subset.extent(0);
    }
    else if( std::string(IDSGridSource).find("edge_sources")
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_sources IDS. \n");
        // db._edge_sources.get();
        // Get number of grid subsets in the selected IDS
        // (IDSGridSource selection box)
        num_gridSubset = db._edge_sources.source(source_index).
            ggd(ggd_slice_index).grid.grid_subset.extent(0);
    }
    else if( std::string(IDSGridSource).find("edge_transport")
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_transport IDS. \n");
        // db._edge_transport.get();
        // Get number of grid subsets in the selected IDS
        // (IDSGridSource selection box)
        num_gridSubset = db._edge_transport.model(model_index).
            ggd(ggd_slice_index).grid.grid_subset.extent(0);
    }
#endif

    // Get plasma state from one of the IDSs
    if( std::string(LoadIDS).find("edge_profiles")
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_profiles IDS. \n");
        // db._edge_profiles.get();
    }
    else if( std::string(LoadIDS).find( "edge_sources" )
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_sources IDS. \n");
        // db._edge_sources.get();
    }else if( std::string(LoadIDS).find( "edge_transport" )
        != std::string::npos )
    {
        vtkOutputWindowDisplayText("Reading edge_transport IDS. \n");
        // db._edge_transport.get();
    }

    // Set object to readGmtryEdge class
    readGmtryEdge gmtrye_obj;
    //
    gmtrye_obj.ggdCheck(db, ggd_slice_index);


    vtkSmartPointer<vtkMultiBlockDataSet> mainMB =
        vtkSmartPointer<vtkMultiBlockDataSet>::New();

    // Get the geometry/coordinates of all nodes/points N[R, Z]
    // forming this grid using routine 'setVtkPoints'
    vtkSmartPointer<vtkPoints> obj_0D_vtkPointsArray = gmtrye_obj.setVtkPoints(
        db,
        std::string(this->IDSGridSource),
        ggd_slice_index,
        this->EdgeSourcesSourceID,
        this->EdgeTransportModelID);

    // Object declaration for readPSEdge routines
    readPSEdge pse_obj;

    // Loop through all grid subsets and extract data for each
    for(int i = 0; i < num_gridSubset; i++)
    {
#if IMAS_VERSION_DIGIT >= 3151
        std::string gridSubset_name;
        gridSubset_name = db._edge_profiles.
            grid_ggd(ggd_slice_index).grid_subset(i).identifier.name;
        int gridSubset_index;
        gridSubset_index= db._edge_profiles.
            grid_ggd(ggd_slice_index).grid_subset(i).identifier.index;

        // Get size/number of elements forming current grid subset
        int num_gridSubset_el;
        num_gridSubset_el = db._edge_profiles.grid_ggd(ggd_slice_index).
            grid_subset(i).element.extent(0);

        // Get dimension of the objects forming this grid subset
        int gridSubset_obj_cls;
        gridSubset_obj_cls = db._edge_profiles.grid_ggd(ggd_slice_index).
            grid_subset(i).element(0).object(0).dimension;
        int gridSubset_obj_dim;
        gridSubset_obj_dim = gridSubset_obj_cls - 1;

#else

        std::string gridSubset_name;
        gridSubset_name = db._edge_profiles.
            ggd(ggd_slice_index).grid.grid_subset(i).identifier.name;
        int gridSubset_index;
        gridSubset_index= db._edge_profiles.
            ggd(ggd_slice_index).grid.grid_subset(i).identifier.index;

        // Get size/number of elements forming current grid subset
        int num_gridSubset_el;
        num_gridSubset_el = db._edge_profiles.ggd(ggd_slice_index).grid.
            grid_subset(i).element.extent(0);

        // Get dimension of the objects forming this grid subset
        int gridSubset_obj_cls;
        gridSubset_obj_cls = db._edge_profiles.ggd(ggd_slice_index).grid.
            grid_subset(i).element(0).object(0).dimension;
        int gridSubset_obj_dim;
        gridSubset_obj_dim = gridSubset_obj_cls - 1;
#endif

        // Print grid subset info
        vtkOutputWindowDisplayText(std::string("Grid subset " +
            std::to_string(gridSubset_index) + ":" + "\n").c_str());
        vtkOutputWindowDisplayText(std::string(" - Name: " + gridSubset_name +
            "\n").c_str());
        vtkOutputWindowDisplayText(std::string(" - Class: " +
            std::to_string(gridSubset_obj_cls) + "\n").c_str());
        vtkOutputWindowDisplayText(std::string(" - Dimension: " +
            std::to_string(gridSubset_obj_dim) + "\n").c_str());
        vtkOutputWindowDisplayText(std::string(
            " - Number of elements: " +
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
                db,
                gridSubsetPointsUnstructuredGrid,
                obj_0D_vtkPointsArray,
                ggd_slice_index,
                i);

            // Set data fields to vtkunstructuredGrid for selected IDS with the
            // help of 'setUnstructuredGridDataFields' routine
            pse_obj.setUnstructuredGridDataFields(
                gridSubsetPointsUnstructuredGrid,
                db,
                gridSubset_index,
                num_gridSubset_el,
                std::string(LoadIDS),
                ggd_slice_index,
                this->EdgeSourcesSourceID,
                this->EdgeTransportModelID);

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
                db,
                gridSubsetLinesUnstructuredGrid,
                obj_0D_vtkPointsArray,
                ggd_slice_index,
                i);

            // Add unstructured grid to main block
            fAddBlock2MultiBlock(mainMB, gridSubsetLinesUnstructuredGrid,
                gridSubset_name );
        }
        // ------ SET 2D CELLS -----
        else if (gridSubset_obj_cls == 3)
        {
            // Set vtk array for 2D cells
            vtkSmartPointer<vtkUnstructuredGrid> gridSubsetCellsUnstructuredGrid =
                vtkSmartPointer<vtkUnstructuredGrid>::New();

            // Set grid subset 2D geometry to vtkUnstructuredGrid
            gmtrye_obj.setGridSubset2DGeometry2UnstructuredGrid(
                db,
                gridSubsetCellsUnstructuredGrid,
                obj_0D_vtkPointsArray,
                ggd_slice_index,
                i,
                gridSubset_obj_cls);

            // Set data fields to vtkunstructuredGrid for selected IDS with the
            // help of 'setUnstructuredGridDataFields' routine
            pse_obj.setUnstructuredGridDataFields(
                gridSubsetCellsUnstructuredGrid,
                db,
                gridSubset_index,
                num_gridSubset_el,
                std::string(LoadIDS),
                ggd_slice_index,
                this->EdgeSourcesSourceID,
                this->EdgeTransportModelID);

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

