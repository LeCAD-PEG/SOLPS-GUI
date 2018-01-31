/**
*-------------------------------------------------------------------------------
*   @file     VTK_IDS_utility.cxx
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the utility C++ file of the ParaView ReadUALEdge
*   DESCRIPTION
*   This file provides C++ utility routines for setting the IDS objects into the
*   VTK objects and other utility routines.
*-------------------------------------------------------------------------------
*/

#include "VTK_IDS_utility.h"
#include <UALClasses.h>
#include <vtkCellData.h>
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
template< typename LQ2 >
void utilityVTKIDS::VTK_IDS_Val2UnstrGrid_GenericGridScalar(
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
            VTK_IDS_setValuesArrayBase(    num_gridSubset_el,
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
void utilityVTKIDS::VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
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
                    VTK_IDS_setValuesArrayBase(    num_gridSubset_el,
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
                    VTK_IDS_setValuesArrayBase(    num_gridSubset_el,
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
                    VTK_IDS_setValuesArrayBase(    num_gridSubset_el,
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
                    VTK_IDS_setValuesArrayBase(    num_gridSubset_el,
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
                    VTK_IDS_setValuesArrayBase(    num_gridSubset_el,
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
vtkSmartPointer<vtkDoubleArray> utilityVTKIDS::VTK_IDS_setValuesArrayBase(
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
std::string utilityVTKIDS::VTK_IDS_SetIonQuantityLabel(
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

/**
*   Function used to read directory holding the IDSs and put
*   the found shot/runs into vector
*   @param userIMASShotRunDir   IMAS database directory (imasdb), containing
*                               IDS cases
*   @param user                 Owner of the IDS cases
*   @param device               IDS case device
*/
std::vector<std::string> utilityVTKIDS::findShotRun(
    std::string userIMASShotRunDir, std::string user, std::string device)
{
    DIR *pDIR = NULL;
    struct dirent *entry = NULL;
    std::string dirPath = userIMASShotRunDir;
    std::vector<std::string> availableShotRun;
    std::string d_name_str;
    int digitInStrCount = 0;
    std::string stripShot;
    std::string stripRun;

    struct stat sb;
    if(string(user) == "")
    {
        char *loginUserName = getlogin();
        user = string(loginUserName);
    }
    // Check if the directory exists
    if (stat(dirPath.c_str(), &sb) == 0 && S_ISDIR(sb.st_mode))
    {
        vtkOutputWindowDisplayText(std::string("IDS imasdb directory '" +
            device + "' from user '" + user + "' found: '" +
            userIMASShotRunDir + "' Reading available IDS shot/runs." +
            "\n\n").c_str());

        if( pDIR=opendir(dirPath.c_str()))
        {
            while(entry = readdir(pDIR))
            {
                if( strcmp(entry->d_name, ".") != 0 &&
                    strcmp(entry->d_name, "..") != 0 )
                {
                    // Read all files in directory
                    d_name_str = std::string(entry->d_name);
                    int d_name_str_len = d_name_str.length();
                    if(d_name_str.substr( d_name_str_len - 5 ) == ".tree")
                    {
                        // Work only with .tree files
                        for(int i = 0; i < d_name_str.length(); i++)
                        {
                            if(isdigit(d_name_str[i]))
                                digitInStrCount++;
                        }
                        int numExtCh = 5;   // 5 is for ".tree" == 5 characters
                        int numRunMax = 4;  // Run consists of max 4 characters
                                            // (from 0000 to 9999).
                        stripShot = d_name_str.substr(
                            d_name_str_len-numExtCh - digitInStrCount,
                            digitInStrCount-numRunMax);
                        stripRun = d_name_str.substr(
                            d_name_str_len-numExtCh - numRunMax,numRunMax);
                        // Get rid of excess zeros in Run number
                        // (example 0011->11).
                        int stripRunStartLen = stripRun.length();
                        int eraseCount = 0;
                        while(stripRun[0] == '0' &&
                              eraseCount < stripRunStartLen-1)
                        {
                            stripRun.erase(0,1);
                            eraseCount++;
                        }
                        // Set stripShot and stripRun in proper form
                        availableShotRun.push_back(stripShot);
                        availableShotRun.push_back(stripRun);
                        digitInStrCount = 0;
                    }
                }
            }
            closedir(pDIR);
        }
    }
    return availableShotRun;
}
