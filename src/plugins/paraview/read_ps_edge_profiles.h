#ifndef __read_ps_edge_profiles_h
#define __read_ps_edge_profiles_h

/*
* This file provides C++ routines for reading the plasma state out of
* edge_profiles IDS.
*/

#include <UALClasses.h>
#include <vtkDoubleArray.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>
#include <fstream>
#include <iostream>
#include <string>

using namespace std;

class readPSEdgeProfiles
{
public:
    template< typename LQ1>
    void EP_SetAllDataFields(
        vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
        LQ1 loc_quantity,
        int gridSubset_index,
        int num_gridSubset_el);
};

#endif


