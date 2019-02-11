#ifndef __VTKIDSutilityTemplateClasses_h
#define __VTKIDSutilityTemplateClasses_h

/**
*-------------------------------------------------------------------------------
*   @file     VTKIDSutilityTemplateClasses.h
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

class VTKIDSutilityTemplateClasses
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

};

#endif