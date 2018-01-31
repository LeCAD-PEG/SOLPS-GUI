/**
*-------------------------------------------------------------------------------
*   @file     read_gmtry_edge.cxx
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the C++ file of the ParaView ReadUALEdge file for
*             handling grid geometry and grid subsets.
*   DESCRIPTION
*   This file provides C++ routines for reading the grid and grid subsets
*   geometry out of edge_profiles, edge_sources and edge_transport IDSs.
*
*-------------------------------------------------------------------------------
*/

#include "read_gmtry_edge.h"
// #include "VTK_IDS_utility.h"
// #include "VTK_IDS_utility.cxx"
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

#if IMAS_VERSION_DIGIT >= 3151
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
        num_obj_0D = PNT_db._edge_profiles.grid_ggd(PNT_grid_ggd_slice_index).
            space(0).objects_per_dimension(0).object.extent(0);

        for(int i = 0; i < num_obj_0D; ++i)
        {
            pointsArray->InsertNextPoint(
                PNT_db._edge_profiles.grid_ggd(PNT_grid_ggd_slice_index).
                    space(0).objects_per_dimension(0).object(i).geometry(0),
                PNT_db._edge_profiles.grid_ggd(PNT_grid_ggd_slice_index).
                    space(0).objects_per_dimension(0).object(i).geometry(1),
                0.0);
        }
    // For "edge_sources" selection in "Load IDS" text box
    }else if( PNT_IDSGridSource_string.find( "edge_sources" ) !=
        std::string::npos )
    {
        // Get number of 0D objects / points
        num_obj_0D = PNT_db._edge_sources.source(PNT_EdgeSourcesSourceID).
            grid_ggd(PNT_grid_ggd_slice_index).
            space(0).objects_per_dimension(0).object.extent(0);

        for(int i = 0; i < num_obj_0D; ++i)
        {
            pointsArray->InsertNextPoint(
                PNT_db._edge_sources.source(PNT_EdgeSourcesSourceID).
                    grid_ggd(PNT_grid_ggd_slice_index).
                    space(0).objects_per_dimension(0).object(i).geometry(0),
                PNT_db._edge_sources.source(PNT_EdgeSourcesSourceID).
                    grid_ggd(PNT_grid_ggd_slice_index).
                    space(0).objects_per_dimension(0).object(i).geometry(1),
                0.0);
        }

    // For "edge_transport" selection in "Load IDS" text box
    }else if( PNT_IDSGridSource_string.find( "edge_transport" ) !=
        std::string::npos )
    {
        // Get number of 0D objects / points
        num_obj_0D = PNT_db._edge_transport.model(PNT_EdgeTransportModelID).
            grid_ggd(PNT_grid_ggd_slice_index).
            space(0).objects_per_dimension(0).object.extent(0);

        for(int i = 0; i < num_obj_0D; ++i)
        {
            pointsArray->InsertNextPoint(
                PNT_db._edge_transport.model(PNT_EdgeTransportModelID).
                    grid_ggd(PNT_grid_ggd_slice_index).
                    space(0).objects_per_dimension(0).object(i).geometry(0),
                PNT_db._edge_transport.model(PNT_EdgeTransportModelID).
                    grid_ggd(PNT_grid_ggd_slice_index).
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