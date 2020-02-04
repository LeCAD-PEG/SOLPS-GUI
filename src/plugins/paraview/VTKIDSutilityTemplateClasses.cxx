/**
*-------------------------------------------------------------------------------
*   @file     VTKIDSutilityTemplateClasses.cxx
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the utility C++ file of the ParaView ReadUALEdge
*   DESCRIPTION
*   This file provides C++ utility routines for setting the IDS objects into the
*   VTK objects and other utility routines.
*-------------------------------------------------------------------------------
*/

#include "VTKIDSutilityTemplateClasses.h"
#include "VTKIDSutility.h"
#include <UALClasses.h>
#include <vtkCellData.h>
#include <vtkPointData.h>
#include <vtkDoubleArray.h>
#include <vtkSmartPointer.h>
#include <dirent.h>
#include <fstream>
#include <iostream>
#include <string>
#include <sys/stat.h>
#include <unistd.h>

using namespace std;
using namespace IdsNs;

/**
*   Fill predefined (size, label...) vtkDoubleArray with
*   quantity values stored in generic_grid_scalar IDS data structure
*   and assign it to vtkUnstructuredGrid.
*   (after each full vtkDoubleArray definition process is required
*   to assign it to vtkUnstructuredGrid)
*   @param loc_quantity     \b grid_generic_scalar IDS data structure
*/
template <typename LQ2>
void VTKIDSutilityTemplateClasses::VTK_IDS_Val2UnstrGrid_GenericGridScalar(
    std::string values_array_label,
    vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
    LQ2 & loc_quantity,
    int gridSubset_index,
    int num_gridSubset_el)
{
    // Skip if the node structure is empty, otherwise continue
    int quantity_gridSubset_index = loc_quantity.grid_subset_index;
    int num_values = loc_quantity.values.extent(0);
    if (gridSubset_index == quantity_gridSubset_index &&
        num_gridSubset_el == num_values)
    {
        VTKIDSutility util_obj;

        // Define vtkDoubleArray and set its label and size
        vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
            util_obj.VTK_IDS_setValuesArrayBase( num_gridSubset_el, values_array_label);
        // In correctly written IDS the number of grid subset
        // objects and grid subset values (scalars) is equal
        newVtkDoubleArray->
            SetNumberOfValues(num_gridSubset_el);
        for (int j = 0; j < num_gridSubset_el; j++)
        {
            newVtkDoubleArray->SetComponent(
                j,0, loc_quantity.values(j));
        }
        // Set new vtkDoubleArray, containing data field,
        // to vtkUnstructuredGrid
        inputVtkUnstructuredGrid->GetCellData()->AddArray(
            newVtkDoubleArray);

        // If the number of elements match the number of points (meaning we
        // are currently dealing with points) in
        // vtkUnstructuredGrid, set new vtkDoubleArray, containing data field,
        // to vtkUnstructuredGrid points
        if(num_gridSubset_el == inputVtkUnstructuredGrid->GetNumberOfPoints())
        {
            inputVtkUnstructuredGrid->GetPointData()->AddArray(newVtkDoubleArray);
        }
        return;
    }
}

/**
*   Function used to fill predefined (size, label...) vtkDoubleArray with
*   quantity values stored in generic_grid_vector_components IDS data structure
*   and assign it to vtkUnstructuredGrid.
*   (after each full vtkDoubleArray definition process is required
*   to assign it to vtkUnstructuredGrid)
*   @param loc_quantity     \b grid_generic_vector_components IDS data structure
*/
template <typename LQ3>
void VTKIDSutilityTemplateClasses::VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
    std::string values_array_label,
    vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
    LQ3 loc_quantity,
    std::string component_label,
    int gridSubset_index,
    int num_gridSubset_el)
{
    VTKIDSutility util_obj;

    int quantity_gridSubset_index = loc_quantity.grid_subset_index;
    // Set component_label_ID integer to be used in switch statement
    // (as C++ cannot directly use strings in switch statements)
    int component_label_ID = 0;
    if ( component_label == "radial") component_label_ID = 1;
    if ( component_label == "diamagnetic") component_label_ID = 2;
    if ( component_label == "parallel") component_label_ID = 3;
    if ( component_label == "poloidal") component_label_ID = 4;
    if ( component_label == "toroidal") component_label_ID = 5;

    // Read defined component and set it to vtkDoubleArray
    switch( component_label_ID )
    {
        case 1:
        {
            int num_values = loc_quantity.radial.extent(0);
            if (gridSubset_index == quantity_gridSubset_index &&
                num_gridSubset_el == num_values)
            {
                // Define vtkDoubleArray and set its label and size
                vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
                    util_obj.VTK_IDS_setValuesArrayBase(    num_gridSubset_el,
                                            values_array_label);
                // In correctly written IDS the number of grid subset
                // objects and grid subset values (scalars) is equal
                newVtkDoubleArray->
                    SetNumberOfValues(num_gridSubset_el);
                for (int j = 0; j < num_gridSubset_el; j++)
                {
                    newVtkDoubleArray->SetComponent(
                        j,0, loc_quantity.radial(j));
                }
                // Set new vtkDoubleArray, containing data field,
                // to vtkUnstructuredGrid
                inputVtkUnstructuredGrid->GetCellData()->AddArray(
                    newVtkDoubleArray);
                // If the number of elements match the number of points
                // (meaning we are currently dealing with points) in
                // vtkUnstructuredGrid, set new vtkDoubleArray, containing
                // data field, to vtkUnstructuredGrid points
                if(num_gridSubset_el == inputVtkUnstructuredGrid->
                    GetNumberOfPoints())
                {
                    inputVtkUnstructuredGrid->GetPointData()->
                        AddArray(newVtkDoubleArray);
                }
                return;
            }
        }
        case 2:
        {
            int num_values = loc_quantity.diamagnetic.extent(0);
            if (gridSubset_index == quantity_gridSubset_index &&
                num_gridSubset_el == num_values)
            {
                // Define vtkDoubleArray and set its label and size
                vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
                    util_obj.VTK_IDS_setValuesArrayBase(    num_gridSubset_el,
                                            values_array_label);
                // In correctly written IDS the number of grid subset
                // objects and grid subset values (scalars) is equal
                newVtkDoubleArray->
                    SetNumberOfValues(num_gridSubset_el);
                for (int j = 0; j < num_gridSubset_el; j++)
                {
                    newVtkDoubleArray->SetComponent(
                        j,0, loc_quantity.diamagnetic(j));
                }
                // Set new vtkDoubleArray, containing data field,
                // to vtkUnstructuredGrid
                inputVtkUnstructuredGrid->GetCellData()->AddArray(
                    newVtkDoubleArray);
                // If the number of elements match the number of points
                // (meaning we are currently dealing with points) in
                // vtkUnstructuredGrid, set new vtkDoubleArray, containing
                // data field, to vtkUnstructuredGrid points
                if(num_gridSubset_el == inputVtkUnstructuredGrid->
                    GetNumberOfPoints())
                {
                    inputVtkUnstructuredGrid->GetPointData()->
                        AddArray(newVtkDoubleArray);
                }
                return;
            }
        }
        case 3:
        {
            int num_values = loc_quantity.parallel.extent(0);
            if (gridSubset_index == quantity_gridSubset_index &&
                num_gridSubset_el == num_values)
            {
                // Define vtkDoubleArray and set its label and size
                vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
                    util_obj.VTK_IDS_setValuesArrayBase(    num_gridSubset_el,
                                            values_array_label);
                // In correctly written IDS the number of grid subset
                // objects and grid subset values (scalars) is equal
                newVtkDoubleArray->
                    SetNumberOfValues(num_gridSubset_el);
                for (int j = 0; j < num_gridSubset_el; j++)
                {
                    newVtkDoubleArray->SetComponent(
                        j,0, loc_quantity.parallel(j));
                }
                // Set new vtkDoubleArray, containing data field,
                // to vtkUnstructuredGrid
                inputVtkUnstructuredGrid->GetCellData()->AddArray(
                    newVtkDoubleArray);
                // If the number of elements match the number of points
                // (meaning we are currently dealing with points) in
                // vtkUnstructuredGrid, set new vtkDoubleArray, containing
                // data field, to vtkUnstructuredGrid points
                if(num_gridSubset_el == inputVtkUnstructuredGrid->
                    GetNumberOfPoints())
                {
                    inputVtkUnstructuredGrid->GetPointData()->
                        AddArray(newVtkDoubleArray);
                }
                return;
            }
        }
        case 4:
        {
            int num_values = loc_quantity.poloidal.extent(0);
            if (gridSubset_index == quantity_gridSubset_index &&
                num_gridSubset_el == num_values)
            {
                // Define vtkDoubleArray and set its label and size
                vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
                    util_obj.VTK_IDS_setValuesArrayBase(    num_gridSubset_el,
                                            values_array_label);
                // In correctly written IDS the number of grid subset
                // objects and grid subset values (scalars) is equal
                newVtkDoubleArray->
                    SetNumberOfValues(num_gridSubset_el);
                for (int j = 0; j < num_gridSubset_el; j++)
                {
                    newVtkDoubleArray->SetComponent(
                        j,0, loc_quantity.poloidal(j));
                }
                // Set new vtkDoubleArray, containing data field,
                // to vtkUnstructuredGrid
                inputVtkUnstructuredGrid->GetCellData()->AddArray(
                    newVtkDoubleArray);
                // If the number of elements match the number of points
                // (meaning we are currently dealing with points) in
                // vtkUnstructuredGrid, set new vtkDoubleArray, containing
                // data field, to vtkUnstructuredGrid points
                if(num_gridSubset_el == inputVtkUnstructuredGrid->
                    GetNumberOfPoints())
                {
                    inputVtkUnstructuredGrid->GetPointData()->
                        AddArray(newVtkDoubleArray);
                }
                return;
            }
        }
        case 5:
        {
            int num_values = loc_quantity.toroidal.extent(0);
            if (gridSubset_index == quantity_gridSubset_index &&
                num_gridSubset_el == num_values)
            {
                // Define vtkDoubleArray and set its label and size
                vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
                    util_obj.VTK_IDS_setValuesArrayBase(    num_gridSubset_el,
                                            values_array_label);
                // In correctly written IDS the number of grid subset
                // objects and grid subset values (scalars) is equal
                newVtkDoubleArray->
                    SetNumberOfValues(num_gridSubset_el);
                for (int j = 0; j < num_gridSubset_el; j++)
                {
                    newVtkDoubleArray->SetComponent(
                        j,0, loc_quantity.toroidal(j));
                }
                // Set new vtkDoubleArray, containing data field,
                // to vtkUnstructuredGrid
                inputVtkUnstructuredGrid->GetCellData()->AddArray(
                    newVtkDoubleArray);
                // If the number of elements match the number of points
                // (meaning we are currently dealing with points) in
                // vtkUnstructuredGrid, set new vtkDoubleArray, containing
                // data field, to vtkUnstructuredGrid points
                if(num_gridSubset_el == inputVtkUnstructuredGrid->
                    GetNumberOfPoints())
                {
                    inputVtkUnstructuredGrid->GetPointData()->
                        AddArray(newVtkDoubleArray);
                }
                return;
            }
        }
    }
}