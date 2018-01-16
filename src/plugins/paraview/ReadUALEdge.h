#ifndef __ReadUALEdge_h
#define __ReadUALEdge_h

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

std::vector<std::string> findShotRun(
    std::string userIMASShotRunDir, std::string user);

class ReadUALEdge : public vtkMultiBlockDataSetAlgorithm
{
    public:

    vtkTypeMacro(ReadUALEdge, vtkMultiBlockDataSetAlgorithm);
    void PrintSelf(ostream& os, vtkIndent indent);

    static ReadUALEdge *New();

    vtkGetMacro(Shot,int);
    vtkSetMacro(Shot,int);

    vtkGetMacro(Run,int);
    vtkSetMacro(Run,int);

    vtkGetMacro(IDSListCheckBox,int);
    vtkSetMacro(IDSListCheckBox,int);

    vtkSetStringMacro(User);
    vtkGetStringMacro(User);

    vtkSetStringMacro(Device);
    vtkGetStringMacro(Device);

    vtkSetStringMacro(LoadIDS);
    vtkGetStringMacro(LoadIDS);

protected:
    ReadUALEdge();
    ~ReadUALEdge(){}

    int Shot;
    int Run;
    int RefRun;
    int IDSListCheckBox;
    char * User;
    char * Device;
    char * Version;
    char * LoadIDS;
    vtkSmartPointer<vtkStringArray> stringArray;

    int RequestData(vtkInformation *, vtkInformationVector **,
                    vtkInformationVector *);

private:
    ReadUALEdge(const ReadUALEdge&);  // Not implemented.
    void operator=(const ReadUALEdge&);  // Not implemented.
};

#endif
