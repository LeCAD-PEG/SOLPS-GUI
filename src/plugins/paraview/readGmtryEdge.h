#ifndef __readGmtryEdge_h
#define __readGmtryEdge_h

/**
*-------------------------------------------------------------------------------
*   @file     readGmtryEdge.h
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the C++ file of the ParaView ReadUALEdge file for
*             handling grid geometry and grid subsets.
*   DESCRIPTION
*   This file provides C++ routines for reading the grid and grid subsets
*   geometry out of edge_profiles, edge_sources and edge_transport IDSs.
*-------------------------------------------------------------------------------
*/

#include <UALClasses.h>
#include <vtkSmartPointer.h>
#include <vtkCellArray.h>
#include <vtkPoints.h>
#include <vtkUnstructuredGrid.h>
#include <fstream>
#include <iostream>
#include <string>

using namespace std;

class readGmtryEdge
{
public:

    template <typename IDS3>
    void ggdCheck(
        IDS3 & GG_db,
        std::string UG_LoadIDS_string,
        int GG_ggd_slice_index);

    template <typename IDS4>
    void setGridSubset0DGeometry2UnstructuredGrid(
        IDS4 & GS_db,
        vtkSmartPointer<vtkUnstructuredGrid> unstructuredGrid,
        vtkSmartPointer<vtkPoints> vtk_grid_points,
        int GS_ggd_slice_index,
        int GS_gridSubset_index);

    template <typename IDS5>
    void setGridSubset1DGeometry2UnstructuredGrid(
        IDS5 & GS_db,
        vtkSmartPointer<vtkUnstructuredGrid> unstructuredGrid,
        vtkSmartPointer<vtkPoints> vtk_grid_points,
        int GS_ggd_slice_index,
        int GS_gridSubset_index);

    template <typename IDS6>
    void setGridSubset2DGeometry2UnstructuredGrid(
        IDS6 & GS_db,
        vtkSmartPointer<vtkUnstructuredGrid> unstructuredGrid,
        vtkSmartPointer<vtkPoints> vtk_grid_points,
        int GS_ggd_slice_index,
        int GS_gridSubset_index,
        int GS_gridSubset_obj_cls);

    template <typename IDS2>
    vtkSmartPointer<vtkPoints> setVtkPoints(
        IDS2 & PNT_db,
        std::string PNT_IDSGridSource_string,
        int PNT_ggd_slice_index,
        int PNT_EdgeSourcesSourceID,
        int PNT_EdgeTransportModelID);

    template <typename V1, typename V2, typename V3>
    vtkSmartPointer<vtkCellArray> setVTKCellArray(
        V1 const& el_data_type,
        V2& loc_gridSubset,
        V3& grid);
};

#endif