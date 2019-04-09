/**
*-------------------------------------------------------------------------------
*   @file     readGmtryEdge.cxx
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the C++ file of the ParaView ReadUALEdge file for
*             handling grid geometry and grid subsets.
*   DESCRIPTION
*   This file provides C++ routines for reading the grid and grid subsets
*   geometry out of edge_profiles, edge_sources and edge_transport IDSs.
*
*-------------------------------------------------------------------------------
*/

#include "readGmtryEdge.h"
#include <UALClasses.h>
#include <vtkCellArray.h>
#include <vtkPoints.h>
#include <vtkSmartPointer.h>
#include <fstream>
#include <iostream>
#include <string>

#define PLUGIN_IMAS_VERSION_DIGIT IMAS_VERSION_DIGIT

using namespace std;
using namespace IdsNs;

template <typename IDS3>
void readGmtryEdge::ggdCheck(
    IDS3 & GG_db,
    std::string UG_LoadIDS_string,
    int GG_ggd_slice_index)
{

    // Set variables to later hold number of elements
    int num_obj_0D = 0; // Node/Point/vertice == 0D object
    int num_obj_1D = 0; // Edge    == 1D object
    int num_obj_2D = 0; // 2D Cell == 2D object

    // For edge_profiles IDS
    if (UG_LoadIDS_string.find( "edge_profiles" ) != std::string::npos)
    {
        int num_ggd_slices = GG_db._edge_profiles.ggd.extent(0);
        vtkOutputWindowDisplayText(std::string( "Number of GGD slices:" +
            std::to_string(num_ggd_slices) + "\n").c_str());

        // Checks regarding GGD slice
        if (GG_ggd_slice_index > num_ggd_slices - 1)
        {
            vtkOutputWindowDisplayWarningText("ERROR! The input GGD structure "
                "array index does not correspond to any existing GGD structure! "
                "Reverting the GGD structure array index to 0! \n\n");
            GG_ggd_slice_index = 0;
        }
        if (num_ggd_slices == 0)
        {
            vtkOutputWindowDisplayWarningText("ERROR! No filled GGD slice found! "
                "Either selected database doesn't exist or it's empty! \n\n");
            return;
        }

#if IMAS_VERSION_DIGIT >= 3151
        // Check for nodes, edges and cells data in current IDS database and
        // get number of objects for each dimension
        // objects_per_dimensions(0) holds every 0D object (nodes/vertices)
        num_obj_0D = GG_db._edge_profiles.grid_ggd(GG_ggd_slice_index).space(0).
            objects_per_dimension(0).object.extent(0);
        // objects_per_dimensions(1) holds every 1D object (edges)
        num_obj_1D = GG_db._edge_profiles.grid_ggd(GG_ggd_slice_index).space(0).
            objects_per_dimension(1).object.extent(0);
        // objects_per_dimensions(2) holds every 2D object (faces/2D cells)
        num_obj_2D = GG_db._edge_profiles.grid_ggd(GG_ggd_slice_index).space(0).
            objects_per_dimension(2).object.extent(0);
#else
        // Check for nodes, edges and cells data in current IDS database and
        // get number of objects for each dimension
        // objects_per_dimensions(0) holds every 0D object (nodes/vertices)
        num_obj_0D = GG_db._edge_profiles.ggd(GG_ggd_slice_index).grid.space(0).
            objects_per_dimension(0).object.extent(0);
        // objects_per_dimensions(1) holds every 1D object (edges)
        num_obj_1D = GG_db._edge_profiles.ggd(GG_ggd_slice_index).grid.space(0).
            objects_per_dimension(1).object.extent(0);
        // objects_per_dimensions(2) holds every 2D object (faces/2D cells)
        num_obj_2D = GG_db._edge_profiles.ggd(GG_ggd_slice_index).grid.space(0).
            objects_per_dimension(2).object.extent(0);
#endif

    }

    // TODO: ggdCheck for edge_sources and edge_transport

    vtkOutputWindowDisplayText(std::string("GGD slice: " +
        std::to_string(GG_ggd_slice_index) + "\n").c_str());
    vtkOutputWindowDisplayText(std::string( "Number of 0D objects: " +
        std::to_string(num_obj_0D) + "\n").c_str());
    vtkOutputWindowDisplayText(std::string( "Number of 1D objects: " +
        std::to_string(num_obj_1D) + "\n").c_str());
    vtkOutputWindowDisplayText(std::string( "Number of 2D objects: " +
        std::to_string(num_obj_2D) + "\n\n").c_str());
}

/**
*   Set grid subset geometry of class 1 (contains only 0D objects - vertices) to
*   vtkUnstructuredGrid.
*   @param GS_db                        Base type of IDS data structure
*                                       (IdsNs::IDS)
*   @param unstructuredGrid             vtkUnstructuredGrid to hold grid subset
*                                       geometry
*   @param vtk_grid_points              vtkPoints object, containing the required
*                                       0D objects (points) of the full grid
*   @param GS_ggd_slice_index           Array index of the ggd(:) array of
*                                       structures node
*   @param GS_gridSubset_index          Index of the grid subset which
*                                       geometry data is to be set to
*                                       vtkUnstructuredGrid
*/
template <typename IDS4>
void readGmtryEdge::setGridSubset0DGeometry2UnstructuredGrid(
    IDS4 & GS_db,
    vtkSmartPointer<vtkUnstructuredGrid> unstructuredGrid,
    vtkSmartPointer<vtkPoints> vtk_grid_points,
    int GS_ggd_slice_index,
    int GS_gridSubset_index)
{
    // Set vtkVertex vtk data type
    vtkSmartPointer<vtkVertex> gridSubsetVertex =
        vtkSmartPointer<vtkVertex>::New();

    // Set vtkCellArray for nodes/points
    vtkSmartPointer<vtkCellArray> gridSubsetVertices =
        vtkSmartPointer<vtkCellArray>::New();

#if IMAS_VERSION_DIGIT >= 3151
    gridSubsetVertices = setVTKCellArray(gridSubsetVertex,
        GS_db._edge_profiles.grid_ggd(GS_ggd_slice_index).
            grid_subset(GS_gridSubset_index),
        GS_db._edge_profiles.grid_ggd(GS_ggd_slice_index));
#else
    gridSubsetVertices = setVTKCellArray(gridSubsetVertex,
        GS_db._edge_profiles.ggd(GS_ggd_slice_index).grid.
            grid_subset(GS_gridSubset_index),
        GS_db._edge_profiles.ggd(GS_ggd_slice_index).grid);
#endif

    // Assign vtkCellArray to vtkUnstructuredGrid
    unstructuredGrid->SetPoints(vtk_grid_points);
    unstructuredGrid->SetCells(
        VTK_VERTEX, gridSubsetVertices);
}

/**
*   Set grid subset geometry of class 2 (contains only 1D objects - edges) to
*   vtkUnstructuredGrid.
*   @param GS_db                        Base type of IDS data structure
*                                       (IdsNs::IDS)
*   @param unstructuredGrid             vtkUnstructuredGrid to hold grid subset
*                                       geometry
*   @param vtk_grid_points              vtkPoints object, containing the required
*                                       0D objects (points) of the full grid
*   @param GS_ggd_slice_index           Array index of the ggd(:) array of
*                                       structures node
*   @param GS_gridSubset_index          Index of the grid subset which
*                                       geometry data is to be set to
*                                       vtkUnstructuredGrid
*/
template <typename IDS5>
void readGmtryEdge::setGridSubset1DGeometry2UnstructuredGrid(
    IDS5 & GS_db,
    vtkSmartPointer<vtkUnstructuredGrid> unstructuredGrid,
    vtkSmartPointer<vtkPoints> vtk_grid_points,
    int GS_ggd_slice_index,
    int GS_gridSubset_index)
{
    // Set vtkCellArray for edges
    vtkSmartPointer<vtkCellArray> gridSubsetLinesArray =
        vtkSmartPointer<vtkCellArray>::New();
    vtkSmartPointer<vtkLine> gridSubsetLine =
        vtkSmartPointer<vtkLine>::New();

#if IMAS_VERSION_DIGIT >= 3151
    gridSubsetLinesArray = setVTKCellArray(gridSubsetLine,
        GS_db._edge_profiles.grid_ggd(GS_ggd_slice_index).
            grid_subset(GS_gridSubset_index),
        GS_db._edge_profiles.grid_ggd(GS_ggd_slice_index));
#else
    gridSubsetLinesArray = setVTKCellArray(gridSubsetLine,
        GS_db._edge_profiles.ggd(GS_ggd_slice_index).grid.
            grid_subset(GS_gridSubset_index),
        GS_db._edge_profiles.ggd(GS_ggd_slice_index).grid);
#endif
    // Assign vtkCellArray to vtkUnstructuredGrid
    unstructuredGrid->SetPoints(vtk_grid_points);
    unstructuredGrid->SetCells(
        VTK_LINE, gridSubsetLinesArray);
}

/**
*   Set grid subset geometry of class 3 (contains only 2D objects - 2D cells) to
*   vtkUnstructuredGrid.
*   @param GS_db                        Base type of IDS data structure
*                                       (IdsNs::IDS)
*   @param unstructuredGrid             vtkUnstructuredGrid to hold grid subset
*                                       geometry
*   @param vtk_grid_points              vtkPoints object, containing the required
*                                       0D objects (points) of the full grid
*   @param GS_ggd_slice_index           Array index of the ggd(:) array of
*                                       structures node
*   @param GS_gridSubset_index          Index of the grid subset which
*                                       geometry data is to be set to
*                                       vtkUnstructuredGrid
*/
template <typename IDS6>
void readGmtryEdge::setGridSubset2DGeometry2UnstructuredGrid(
    IDS6 & GS_db,
    vtkSmartPointer<vtkUnstructuredGrid> unstructuredGrid,
    vtkSmartPointer<vtkPoints> vtk_grid_points,
    int GS_ggd_slice_index,
    int GS_gridSubset_index,
    int GS_gridSubset_obj_cls)
{
    vtkSmartPointer<vtkQuad> gridSubsetQuad =
        vtkSmartPointer<vtkQuad>::New();
    vtkSmartPointer<vtkTriangle> gridSubsetTriangle =
        vtkSmartPointer<vtkTriangle>::New();
    vtkSmartPointer<vtkCellArray> gridSubsetCellArray =
        vtkSmartPointer<vtkCellArray>::New();

#if IMAS_VERSION_DIGIT >= 3151
    // Get number of nodes of the first 2D cell in order to find out
    // whether they are triangles or quad (all other 2D cells of the
    // same grid should be of the same type for now)
    int num_obj_nodes_first = GS_db._edge_profiles.grid_ggd(GS_ggd_slice_index).
        space(0).objects_per_dimension(GS_gridSubset_obj_cls - 1).object(0).
        nodes.extent(0);

    // Cells-Triangles
    if (num_obj_nodes_first == 3)
    {
        gridSubsetCellArray = setVTKCellArray(gridSubsetTriangle,
            GS_db._edge_profiles.grid_ggd(GS_ggd_slice_index).
                grid_subset(GS_gridSubset_index),
            GS_db._edge_profiles.grid_ggd(GS_ggd_slice_index));

        // Assign vtkCellArray to vtkUnstructuredGrid
        unstructuredGrid->SetPoints(vtk_grid_points);
        unstructuredGrid->SetCells(VTK_TRIANGLE, gridSubsetCellArray);
    }
    // Cells-Quad
    else if (num_obj_nodes_first == 4)
    {
        gridSubsetCellArray = setVTKCellArray(gridSubsetQuad,
            GS_db._edge_profiles.grid_ggd(GS_ggd_slice_index).
                grid_subset(GS_gridSubset_index),
            GS_db._edge_profiles.grid_ggd(GS_ggd_slice_index));

        // Assign vtkCellArray to vtkUnstructuredGrid
        unstructuredGrid->SetPoints(vtk_grid_points);
        unstructuredGrid->SetCells(VTK_QUAD, gridSubsetCellArray);
    }
}

#else

    // Get number of nodes of the first 2D cell in order to find out
    // whether they are triangles or quad (all other 2D cells of the
    // same grid should be of the same type for now)
    int num_obj_nodes_first = GS_db._edge_profiles.ggd(GS_ggd_slice_index).grid.
        space(0).objects_per_dimension(GS_gridSubset_obj_cls - 1).object(0).
        nodes.extent(0);

    // Cells-Triangles
    if (num_obj_nodes_first == 3)
    {
        gridSubsetCellArray = setVTKCellArray(gridSubsetTriangle,
            GS_db._edge_profiles.ggd(GS_ggd_slice_index).grid.
                grid_subset(GS_gridSubset_index),
            GS_db._edge_profiles.ggd(GS_ggd_slice_index).grid);
        // Assign vtkCellArray to vtkUnstructuredGrid
        unstructuredGrid->SetPoints(vtk_grid_points);
        unstructuredGrid->SetCells(VTK_TRIANGLE, gridSubsetCellArray);
    }
    // Cells-Quad
    else if (num_obj_nodes_first == 4)
    {
        gridSubsetCellArray = setVTKCellArray(gridSubsetQuad,
            GS_db._edge_profiles.ggd(GS_ggd_slice_index).grid.
                grid_subset(GS_gridSubset_index),
            GS_db._edge_profiles.ggd(GS_ggd_slice_index).grid);

        // Assign vtkCellArray to vtkUnstructuredGrid
        unstructuredGrid->SetPoints(vtk_grid_points);
        unstructuredGrid->SetCells(VTK_QUAD, gridSubsetCellArray);
    }
}
#endif

#if IMAS_VERSION_DIGIT >= 3151
/**
*   Function used to get the geometry/coordinates of all 0D objects/points
*   P[R, Z] forming this grid and set it to vtkPoints
*   @param PNT_db                       Base type of IDS data structure
*                                       (IdsNs::IDS)
*   @param PNT_IDSGridSource_string     String containing name of the IDS of
*                                       which grid geometry points
*                                       added to vtkPoints
*   @param PNT_ggd_slice_index          Array index of the ggd(:) array of
*                                       structures node
*   @param PNT_EdgeSourcesSourceID      Array index of the source(:) array of
*                                       structures node (relevant only to
*                                       edge_sources IDS)
*   @param PNT_EdgeTransportModelID     Array index of the model(:) array of
*                                       structures node (relevant only to
*                                       edge_transport IDS)
*/
template <typename IDS2>
vtkSmartPointer<vtkPoints> readGmtryEdge::setVtkPoints(
    IDS2 & PNT_db,
    std::string PNT_IDSGridSource_string,
    int PNT_ggd_slice_index,
    int PNT_EdgeSourcesSourceID,
    int PNT_EdgeTransportModelID)
{
    int num_obj_0D = 0;
    vtkSmartPointer<vtkPoints> pointsArray = vtkSmartPointer<vtkPoints>::New();
    // For "edge_profiles" selection in "IDSGridSource" text box
    if( PNT_IDSGridSource_string.find( "edge_profiles" ) != std::string::npos)
    {
        // Get number of 0D objects / points
        num_obj_0D = PNT_db._edge_profiles.grid_ggd(PNT_ggd_slice_index).
            space(0).objects_per_dimension(0).object.extent(0);

        for(int i = 0; i < num_obj_0D; ++i)
        {
            pointsArray->InsertNextPoint(
                PNT_db._edge_profiles.grid_ggd(PNT_ggd_slice_index).
                    space(0).objects_per_dimension(0).object(i).geometry(0),
                PNT_db._edge_profiles.grid_ggd(PNT_ggd_slice_index).
                    space(0).objects_per_dimension(0).object(i).geometry(1),
                0.0);
        }
    // For "edge_sources" selection in "Load IDS" text box
    }else if( PNT_IDSGridSource_string.find( "edge_sources" ) !=
        std::string::npos )
    {
        // Get number of 0D objects / points
        num_obj_0D = PNT_db._edge_sources.grid_ggd(PNT_ggd_slice_index).
            space(0).objects_per_dimension(0).object.extent(0);

        for(int i = 0; i < num_obj_0D; ++i)
        {
            pointsArray->InsertNextPoint(
                PNT_db._edge_sources.grid_ggd(PNT_ggd_slice_index).
                    space(0).objects_per_dimension(0).object(i).geometry(0),
                PNT_db._edge_sources.grid_ggd(PNT_ggd_slice_index).
                    space(0).objects_per_dimension(0).object(i).geometry(1),
                0.0);
        }

    // For "edge_transport" selection in "Load IDS" text box
    }else if( PNT_IDSGridSource_string.find( "edge_transport" ) !=
        std::string::npos )
    {
        // Get number of 0D objects / points
        num_obj_0D = PNT_db._edge_transport.grid_ggd(PNT_ggd_slice_index).
            space(0).objects_per_dimension(0).object.extent(0);

        for(int i = 0; i < num_obj_0D; ++i)
        {
            pointsArray->InsertNextPoint(
                PNT_db._edge_transport.grid_ggd(PNT_ggd_slice_index).
                    space(0).objects_per_dimension(0).object(i).geometry(0),
                PNT_db._edge_transport.grid_ggd(PNT_ggd_slice_index).
                    space(0).objects_per_dimension(0).object(i).geometry(1),
                0.0);
        }
    }
    return pointsArray;
}
#else
/**
*   Function used to get the geometry/coordinates of all 0D objects/points
*   P[R, Z] forming this grid
*   @param  PNT_db                      Base type of IDS data structure
*                                       (IdsNs::IDS)
*   @param  PNT_IDSGridSource_string    String containing name of the IDS of
*                                       which grid geometry points
*                                       added to vtkPoints
*   @param PNT_ggd_slice_index          Array index of the ggd(:) array of
*                                       structures node
*   @param PNT_EdgeSourcesSourceID      Array index of the source(:) array of
*                                       structures node (relevant only to
*                                       edge_sources IDS)
*   @param PNT_EdgeTransportModelID     Array index of the model(:) array of
*                                       structures node (relevant only to
*                                       edge_transport IDS)
*/
template <typename IDS2>
vtkSmartPointer<vtkPoints> readGmtryEdge::setVtkPoints(
    IDS2 & PNT_db,
    std::string PNT_IDSGridSource_string = "edge_profiles",
    int PNT_ggd_slice_index = 0,
    int PNT_EdgeSourcesSourceID = 0,
    int PNT_EdgeTransportModelID = 0)
{

    int num_obj_0D = 0;
    vtkSmartPointer<vtkPoints> pointsArray = vtkSmartPointer<vtkPoints>::New();
    // For "edge_profiles" selection in "IDSGridSource" text box
    if( PNT_IDSGridSource_string.find( "edge_profiles" ) != std::string::npos)
    {
        // Get number of 0D objects / points
        num_obj_0D = PNT_db._edge_profiles.ggd(PNT_ggd_slice_index).grid.
            space(0).objects_per_dimension(0).object.extent(0);

        for(int i = 0; i < num_obj_0D; ++i)
        {
            pointsArray->InsertNextPoint(
                PNT_db._edge_profiles.ggd(PNT_ggd_slice_index).grid.
                    space(0).objects_per_dimension(0).object(i).geometry(0),
                PNT_db._edge_profiles.ggd(PNT_ggd_slice_index).grid.
                    space(0).objects_per_dimension(0).object(i).geometry(1),
                0.0);
        }
    // For "edge_sources" selection in "Load IDS" text box
    }else if( PNT_IDSGridSource_string.find( "edge_sources" ) !=
        std::string::npos )
    {
        // Get number of 0D objects / points
        num_obj_0D = PNT_db._edge_sources.source(PNT_EdgeSourcesSourceID).
            ggd(PNT_ggd_slice_index).grid.
            space(0).objects_per_dimension(0).object.extent(0);

        for(int i = 0; i < num_obj_0D; ++i)
        {
            pointsArray->InsertNextPoint(
                PNT_db._edge_sources.source(PNT_EdgeSourcesSourceID).
                    ggd(PNT_ggd_slice_index).grid.
                    space(0).objects_per_dimension(0).object(i).geometry(0),
                PNT_db._edge_sources.source(PNT_EdgeSourcesSourceID).
                    ggd(PNT_ggd_slice_index).grid.
                    space(0).objects_per_dimension(0).object(i).geometry(1),
                0.0);
        }

    // For "edge_transport" selection in "Load IDS" text box
    }else if( PNT_IDSGridSource_string.find( "edge_transport" ) !=
        std::string::npos )
    {
        // Get number of 0D objects / points
        num_obj_0D = PNT_db._edge_transport.model(PNT_EdgeTransportModelID).
            ggd(PNT_ggd_slice_index).grid.
            space(0).objects_per_dimension(0).object.extent(0);

        for(int i = 0; i < num_obj_0D; ++i)
        {
            pointsArray->InsertNextPoint(
                PNT_db._edge_transport.model(PNT_EdgeTransportModelID).
                    ggd(PNT_ggd_slice_index).grid.
                    space(0).objects_per_dimension(0).object(i).geometry(0),
                PNT_db._edge_transport.model(PNT_EdgeTransportModelID).
                    ggd(PNT_ggd_slice_index).grid.
                    space(0).objects_per_dimension(0).object(i).geometry(1),
                0.0);
        }
    }
    return pointsArray;
}
#endif

/**
*   Function used to fill predefined (size, label...) vtkCellArray.
*   @param  el_data_type    VTK data type (vtkVertex etc.)
*   @param  loc_gridSubset  Type of edge_profiles IDS data structure, designed
*                           for handling grid subset data
*   @param  grid            Type of edge_profiles IDS data structure, designed
*                           for handling full grid data
*/
template <typename V1, typename V2, typename V3>
vtkSmartPointer<vtkCellArray> readGmtryEdge::setVTKCellArray(
    V1 const& el_data_type,
    V2& loc_gridSubset,
    V3& grid)
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