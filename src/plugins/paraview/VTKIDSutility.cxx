/**
*-------------------------------------------------------------------------------
*   @file     VTKIDSutility.cxx
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the utility C++ file of the ParaView ReadUALEdge
*   DESCRIPTION
*   This file provides C++ utility routines for setting the IDS objects into the
*   VTK objects and other utility routines.
*-------------------------------------------------------------------------------
*/

#include "VTKIDSutility.h"
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

/*
*   Function used to set vtkDoubleArray size and label
*/
vtkSmartPointer<vtkDoubleArray> VTKIDSutility::VTK_IDS_setValuesArrayBase(
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
std::string VTKIDSutility::VTK_IDS_SetIonQuantityLabel(
    std::string quantity_name, int is,
    std::string ic )
{
    stringstream ion_species_num2str;
    ion_species_num2str << is + 1;
    std::string is_string = ion_species_num2str.str();
    std::string ion_array_label;
    if (is < 9)
    {
        ion_array_label = "Ion " + quantity_name + " 0" + is_string + " " + ic;
    } else
    {
        ion_array_label = "Ion " + quantity_name + " " + is_string + " " + ic;
    }
    return ion_array_label;
}

/**
*   Function used to read directory holding the IDSs and put
*   the found shot/runs into vector
*   @param userIMASShotRunDir   IMAS database directory (imasdb), containing
*                               IDS cases
*   @param user                 Owner of the IDS cases
*   @param database             IDS case database
*/
std::vector<std::string> VTKIDSutility::findShotRun(
    std::string userIMASShotRunDir, std::string user, std::string database)
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
            database + "' from user '" + user + "' found: '" +
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
