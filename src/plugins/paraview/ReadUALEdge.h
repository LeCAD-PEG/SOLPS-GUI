#ifndef __ReadUALEdge_h
#define __ReadUALEdge_h

/**
*-------------------------------------------------------------------------------
*   @file     ReadUALEdge.h
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the main C++ header of the ParaView ReadUALEdge file
*   DESCRIPTION
*   ParaView ReadUALEdge plugin is a tool used to visualize and analyze data,
*   obtained by fusion simulations stored IDS database.
*   The focus of plugin development is on data stored in 'edge_profiles',
*   'edge_sources' and 'edge_transport' IDSs.
*-------------------------------------------------------------------------------
*/

#include "UALClasses.h"
#include <iostream>
#include <fstream>
#include <string>
#include "vtkSmartPointer.h"
#include "vtkStringArray.h"
#include "vtkDataArraySelection.h"
#include "vtkUnstructuredGridAlgorithm.h"
#include <vtkMultiBlockDataSetAlgorithm.h>

using namespace std;

void msgToOutputWindow( std::stringstream& msg, std::string msg_type );

class ReadUALEdge : public vtkMultiBlockDataSetAlgorithm
{
    public:

    vtkTypeMacro(ReadUALEdge, vtkMultiBlockDataSetAlgorithm);
    void PrintSelf(ostream& os, vtkIndent indent);

    static ReadUALEdge *New();

    // Get macros for ReadUALEdge ParaView plugin custom GUI widgets
    vtkGetMacro(Shot,int);
    vtkSetMacro(Shot,int);
    vtkGetMacro(Run,int);
    vtkSetMacro(Run,int);
    vtkSetStringMacro(User);
    vtkGetStringMacro(User);
    vtkSetStringMacro(Device);
    vtkGetStringMacro(Device);
    vtkSetStringMacro(LoadIDS);
    vtkGetStringMacro(LoadIDS);
    vtkGetMacro(IDSListCheckBox,int);
    vtkSetMacro(IDSListCheckBox,int);
    vtkGetMacro(EdgeSourcesSourceID,int);
    vtkSetMacro(EdgeSourcesSourceID,int);
    vtkGetMacro(EdgeTransportModelID,int);
    vtkSetMacro(EdgeTransportModelID,int);
    vtkGetMacro(GGDslice,int);
    vtkSetMacro(GGDslice,int);
    vtkSetStringMacro(IDSPlasmaStateSource);
    vtkGetStringMacro(IDSPlasmaStateSource);


protected:
    ReadUALEdge();
    ~ReadUALEdge(){}

    // Set variables to work with macros for ReadUALEdge ParaView custom plugin
    // GUI widget
    int Shot;
    int Run;
    int RefRun;
    int IDSListCheckBox;
    int EdgeSourcesSourceID;
    int EdgeTransportModelID;
    int GGDslice;
    char * User;
    char * Device;
    char * Version;
    char * LoadIDS;
    char * IDSPlasmaStateSource;
    vtkSmartPointer<vtkStringArray> stringArray;

    int RequestData(vtkInformation *, vtkInformationVector **,
                    vtkInformationVector *);

private:
    ReadUALEdge(const ReadUALEdge&);  // Not implemented.
    void operator=(const ReadUALEdge&);  // Not implemented.
};

#endif
