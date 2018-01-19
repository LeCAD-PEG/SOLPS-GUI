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

class utilityPSEdgeProfiles
{
public:
    template< typename LQ1>
    void EPmain_setAllValues_GenericGridScalar(
        vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
        LQ1 loc_quantity,
        int gridSubset_index,
        int num_gridSubset_el);

    template< typename LQ2>
    void EP_Val2UnstrGrid_GenericGridScalar(
        std::string values_array_label,
        vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
        LQ2 loc_quantity,
        int gridSubset_index,
        int num_gridSubset_el);

    template< typename LQ3>
    void EP_Val2UnstrGrid_GenericGridVectorComponents(
        std::string values_array_label,
        vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
        LQ3 loc_quantity,
        std::string component_label,
        int gridSubset_index,
        int num_gridSubset_el );

    vtkSmartPointer<vtkDoubleArray> EP_setValuesArrayBase(
        int ndarray_num_tuples,
        std::string ndarray_label);

    std::string EP_SetIonQuantityLabel(
        std::string quantity_name, int is,
        std::string ic );
};

#endif


