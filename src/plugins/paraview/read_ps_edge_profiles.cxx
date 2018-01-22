/*
* This file provides C++ routines for reading the plasma state out of
* edge_profiles IDS.
*/

#include "read_ps_edge_profiles.h"
#include <UALClasses.h>
#include <vtkCellData.h>
#include <vtkDoubleArray.h>
#include <vtkSmartPointer.h>
#include <fstream>
#include <iostream>
#include <string>

using namespace std;
using namespace IdsNs;


/* Main function used to fully read plasma state from the edge_profiles IDS
* and set the data properly to specified vtkUnstructuredGrid
* @param inputVtkUnstructuredGrid   Input vtkUnstructuredGrid to fill
* @param loc_ggd            \b edge_profiles_time_slice ggd IDS data structure
* @param gridSubset_index   Grid subset index of the corresponding grid subset
*                           to the vtkUnstructuredGrid
* @param num_gridSubset_el  Number of grid subset elements forming the grid
*                           subset
*/
template< typename LQ1 >
void utilityPSEdgeProfiles::EPmain_setAllValues_GenericGridScalar(
    vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
    LQ1 loc_ggd,
    int gridSubset_index,
    int num_gridSubset_el)
{

    // Set default value
    int num_IDStarget_gridSubsets = 0;

    // Assigning values - Electrons

    // Assign values found in Electron Temperature array of structures node to
    // grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.temperature.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridScalar(
            "Electron Temperature",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.temperature(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electron Density array of structures node to
    // grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.density.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridScalar(
            "Electron Density",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.density(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electron Density_Fast array of structures node to
    // grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.density_fast.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridScalar(
            "Electron Density_Fast",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.density_fast(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electron Pressure array of structures node to
    // grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.pressure.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridScalar(
            "Electron Pressure",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.pressure(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electron Pressure_Fast_Perpendicular array of
    // structures node to grid subsets objects
    num_IDStarget_gridSubsets =
        loc_ggd.electrons.pressure_fast_perpendicular.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridScalar(
            "Electron Pressure_Fast_Perpendicular",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.pressure_fast_perpendicular(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electron Pressure_Fast_Parallel array of
    // structures  node to grid subsets objects
    num_IDStarget_gridSubsets =
        loc_ggd.electrons.pressure_fast_parallel.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridScalar(
            "Electron Pressure_Fast_Parallel",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.pressure_fast_parallel(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // In UAL 3.6.3 and older versions the .velocity IDS data structure is
    // simple structure node, while in 3.6.4 it was changed to array
    // of structures node
#if UAL__VERSION_DIGIT >= 364
    // Reading Electron velocity ( GenericGridVectorComponents data structure
    // type )
    num_IDStarget_gridSubsets = loc_ggd.electrons.velocity.extent(0);
    // Assign values found in Electron Velocity array of structures
    // node - Radial simple structure node to grid subsets objects
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridVectorComponents(
            "Electron Velocity - Radial",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.velocity(n),
            "radial",
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electron Velocity array of structures
    // node - Diamagnetic simple structure node to grid subsets objects
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridVectorComponents(
            "Electron Velocity - Diamagnetic",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.velocity(n),
            "diamagnetic",
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electron Velocity array of structures
    // node - Parallel simple structure node to grid subsets objects
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridVectorComponents(
            "Electron Velocity - Parallel",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.velocity(n),
            "parallel",
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electron Velocity array of structures
    // node - Poloidal simple structure node to grid subsets objects
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridVectorComponents(
            "Electron Velocity - Poloidal",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.velocity(n),
            "poloidal",
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electron Velocity array of structures
    // node - Toroidal simple structure node to grid subsets objects
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridVectorComponents(
            "Electron Velocity - Toroidal",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.velocity(n),
            "toroidal",
            gridSubset_index,
            num_gridSubset_el );
    }
#endif

    // Assign values found in Electron Distribution Function array of structures
    // node to grid subsets objects
    num_IDStarget_gridSubsets =
        loc_ggd.electrons.distribution_function.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        EP_Val2UnstrGrid_GenericGridScalar(
            "Electron Distribution Function",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.distribution_function(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Ion substructure to grid subsets
    // objects (2D cells)
    int num_ion_species = loc_ggd.ion.extent(0);
    for( int k = 0; k < num_ion_species; k++)
    {
        // Set ion specie label
        std::string ion_charge= loc_ggd.ion(k).label;
        std::string ion_array_label;

        // Assign values found in Ion Temperature array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel( "Temperature", k, ion_charge );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).temperature.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).temperature(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Density array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel( "Density", k, ion_charge );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).density.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).density(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Density_Fast array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel( "Density_Fast", k, ion_charge );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).density_fast.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).density_fast(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Pressure array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel( "Pressure", k, ion_charge );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).pressure.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).pressure(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Pressure - Fast Perpendicular array of
        // structures node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel(
            "Pressure - Fast Perpendicular", k, ion_charge );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).pressure_fast_perpendicular.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).pressure_fast_perpendicular(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Pressure - Fast Parallel array of
        // structures node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel(
            "Pressure - Fast Parallel", k, ion_charge );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).pressure_fast_parallel.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).pressure_fast_parallel(n),
                gridSubset_index,
                num_gridSubset_el );
        }

    // In UAL 3.6.3 and older versions the .velocity IDS data structure is
    // simple structure node, while in 3.6.4 it was changed to array
    // of structures node
#if UAL__VERSION_DIGIT >= 364
        // Reading Ion velocity ( GenericGridVectorComponents data structure
        // type )
        num_IDStarget_gridSubsets = loc_ggd.ion(k).velocity.extent(0);
        // Assign values found in Ion Velocity array of structures
        // node - Radial simple structure node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel(
            "Velocity - Radial", k, ion_charge );
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridVectorComponents(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).velocity(n),
                "radial",
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Velocity array of structures
        // node - Diamagnetic simple structure node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel(
            "Velocity - Diamagnetic", k, ion_charge );
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridVectorComponents(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).velocity(n),
                "diamagnetic",
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Velocity array of structures
        // node - Parallel simple structure node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel(
            "Velocity - Parallel", k, ion_charge );
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridVectorComponents(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).velocity(n),
                "parallel",
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Velocity array of structures
        // node - Poloidal simple structure node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel(
            "Velocity - Poloidal", k, ion_charge );
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridVectorComponents(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).velocity(n),
                "poloidal",
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Velocity array of structures
        // node - Toroidal simple structure node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel(
            "Velocity - Toroidal", k, ion_charge );
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridVectorComponents(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).velocity(n),
                "toroidal",
                gridSubset_index,
                num_gridSubset_el );
        }
#endif

        // Assign values found in Ion Energy Density Kinetic array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = EP_SetIonQuantityLabel(
            "Energy Density Kinetic", k, ion_charge );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).energy_density_kinetic.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            EP_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).energy_density_kinetic(n),
                gridSubset_index,
                num_gridSubset_el );
        }
    }
}

/**
*   Function used to fill predefined (size, label...) vtkDoubleArray with
*   quantity values stored in generic_grid_scalar IDS data structure
*   and assign it to vtkUnstructuredGrid.
*   (after each full vtkDoubleArray definition process is required
*   to assign it to vtkUnstructuredGrid)
*   @param loc_quantity     \b grid_generic_scalar IDS data structure
*/
template< typename LQ2 >
void utilityPSEdgeProfiles::EP_Val2UnstrGrid_GenericGridScalar(
    std::string values_array_label,
    vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
    LQ2 loc_quantity,
    int gridSubset_index,
    int num_gridSubset_el)
{
// Skip if the node structure is empty, otherwise continue
    int quantity_gridSubset_index = loc_quantity.grid_subset_index;
    int num_values = loc_quantity.values.extent(0);
    if (gridSubset_index == quantity_gridSubset_index &&
        num_gridSubset_el == num_values)
    {

        // Define vtkDoubleArray and set its label and size
        vtkSmartPointer<vtkDoubleArray> newVtkDoubleArray =
            EP_setValuesArrayBase(    num_gridSubset_el,
                                    values_array_label);
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
void utilityPSEdgeProfiles::EP_Val2UnstrGrid_GenericGridVectorComponents(
    std::string values_array_label,
    vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
    LQ3 loc_quantity,
    std::string component_label,
    int gridSubset_index,
    int num_gridSubset_el)
{
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
                    EP_setValuesArrayBase(    num_gridSubset_el,
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
                    EP_setValuesArrayBase(    num_gridSubset_el,
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
                    EP_setValuesArrayBase(    num_gridSubset_el,
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
                    EP_setValuesArrayBase(    num_gridSubset_el,
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
                    EP_setValuesArrayBase(    num_gridSubset_el,
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
                return;
            }
        }
    }
}

/*
*   Function used to set vtkDoubleArray size and label
*/
vtkSmartPointer<vtkDoubleArray> utilityPSEdgeProfiles::EP_setValuesArrayBase(
    int ndarray_num_tuples,
    std::string ndarray_label)
{
    vtkSmartPointer<vtkDoubleArray> newDoubleArray =
        vtkSmartPointer<vtkDoubleArray>::New();
    newDoubleArray->SetNumberOfComponents(1);
    newDoubleArray->SetNumberOfTuples(ndarray_num_tuples);
    std::string set_name = ndarray_label;
    newDoubleArray->SetName(set_name.c_str());
    return newDoubleArray;
}

/*
*   Set Ion specie data field label.
*   @param   is  Ion specie index
*   @param   ic  Ion charge
*/
std::string utilityPSEdgeProfiles::EP_SetIonQuantityLabel(
    std::string quantity_name, int is,
    std::string ic )
{
    stringstream ion_species_num2str;
    ion_species_num2str << is + 1;
    std::string is_string = ion_species_num2str.str();
    std::string ion_array_label;
    if (is < 9)
    {
        ion_array_label = "Ion " + quantity_name + " 0" + is_string + ic;
    } else
    {
        ion_array_label = "Ion " + quantity_name + " " + is_string + ic;
    }
    return ion_array_label;
}


