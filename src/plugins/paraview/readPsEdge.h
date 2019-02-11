#ifndef __readPsEdge_h
#define __readPsEdge_h

/**
*-------------------------------------------------------------------------------
*   @file     readPsEdge.h
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the C++ header of the ParaView ReadUALEdge file for
*             handling data fields.
*   DESCRIPTION
*   This file provides C++ routines for reading the plasma state out of
*   edge_profiles IDS.
*-------------------------------------------------------------------------------
*/

#include <UALClasses.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>
#include <fstream>
#include <iostream>
#include <string>

using namespace std;

class readPsEdge
{
public:

    template <typename IDS1>
    void setUnstructuredGridDataFields(
        vtkSmartPointer<vtkUnstructuredGrid> UG,
        IDS1 & UG_db,
        int UG_gridSubset_index,
        int UG_num_gridSubset_el,
        std::string UG_LoadIDS_string,
        int UG_ggd_slice_index,
        int UG_EdgeSourcesSourceID,
        int UG_EdgeTransportModelID);

    template< typename EP1>
    void setAllDataFields_edge_profiles(
        vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
        EP1 loc_quantity,
        int gridSubset_index,
        int num_gridSubset_el);

    template< typename ES1>
    void setAllDataFields_edge_sources(
        vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
        ES1 loc_quantity,
        int gridSubset_index,
        int num_gridSubset_el);

    template< typename ET1>
    void setAllDataFields_edge_transport(
        vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
        ET1 loc_quantity,
        int gridSubset_index,
        int num_gridSubset_el);
};

#endif


