#ifndef __VTKIDSutility_h
#define __VTKIDSutility_h

/**
*-------------------------------------------------------------------------------
*   @file     VTKIDSutility.h
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

class VTKIDSutility
{
public:
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