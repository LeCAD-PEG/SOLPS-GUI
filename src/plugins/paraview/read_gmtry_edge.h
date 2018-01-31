#ifndef __read_gmtry_edge_h
#define __read_gmtry_edge_h

/**
*-------------------------------------------------------------------------------
*   @file     read_gmtry_edge.h
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
        int GG_ggd_slice_index);

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