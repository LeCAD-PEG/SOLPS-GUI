#ifndef __read_ps_edge_h
#define __read_ps_edge_h

/*
* This file provides C++ routines for reading the plasma state out of
* edge_profiles IDS.
*/

#include <UALClasses.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>
#include <fstream>
#include <iostream>
#include <string>

using namespace std;

class readPSEdge
{
public:
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


