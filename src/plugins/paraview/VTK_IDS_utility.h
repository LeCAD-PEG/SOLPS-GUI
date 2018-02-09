#ifndef __VTK_IDS_utility_h
#define __VTK_IDS_utility_h

/**
*-------------------------------------------------------------------------------
*   @file     VTK_IDS_utility.h
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the utility C++ header of the ParaView ReadUALEdge
*   DESCRIPTION
*   This file provides C++ utility routines for setting the IDS objects into the
*   VTK objects and other utility routines.
*-------------------------------------------------------------------------------
*/

#include <UALClasses.h>
#include <vtkDoubleArray.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>
#include <fstream>
#include <iostream>
#include <string>

using namespace std;

class utilityVTKIDS
{
public:
    template< typename LQ2>
    void VTK_IDS_Val2UnstrGrid_GenericGridScalar(
        std::string values_array_label,
        vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
        LQ2 & loc_quantity,
        int gridSubset_index,
        int num_gridSubset_el);

    template< typename LQ3>
    void VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
        std::string values_array_label,
        vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
        LQ3 loc_quantity,
        std::string component_label,
        int gridSubset_index,
        int num_gridSubset_el );

    vtkSmartPointer<vtkDoubleArray> VTK_IDS_setValuesArrayBase(
        int ndarray_num_tuples,
        std::string ndarray_label);

    std::string VTK_IDS_SetIonQuantityLabel(
        std::string quantity_name, int is,
        std::string ic );

    std::vector<std::string> findShotRun(
        std::string userIMASShotRunDir, std::string user, std::string device);

};

#endif