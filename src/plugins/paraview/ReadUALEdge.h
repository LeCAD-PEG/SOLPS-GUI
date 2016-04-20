#ifndef __ReadUALEdge_h
#define __ReadUALEdge_h

#include "UALClasses.h"
#include <iostream>
#include <fstream>
#include "vtkSmartPointer.h"
#include "vtkStringArray.h"
#include "vtkDataArraySelection.h"
#include "vtkUnstructuredGridAlgorithm.h"
#include <vtkMultiBlockDataSetAlgorithm.h>
using namespace std; 

 
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

  vtkGetMacro(RefRun,int);
  vtkSetMacro(RefRun,int);

  vtkGetMacro(CPOLoad,int);
  vtkSetMacro(CPOLoad,int);
 
  vtkGetMacro(FieldLoadStatus,int);
  vtkSetMacro(FieldLoadStatus,int);  
 
  vtkSetStringMacro(User);
  vtkGetStringMacro(User);
  
  vtkSetStringMacro(Tokamak);
  vtkGetStringMacro(Tokamak);
 
  virtual vtkDataArraySelection *  GetCPOListSelection();
  int GetCPOListArrayStatus(char *name);
  void SetCPOListArrayStatus(const char * name, int status);
  int GetNumberOfCPOListArrays();
  const char * GetCPOListArrayName(int index);
  
  
  virtual vtkDataArraySelection *  GetFieldListSelection();
  int GetFieldListArrayStatus(char *name);
  void SetFieldListArrayStatus(const char * name, int status);
  int GetNumberOfFieldListArrays();
  const char * GetFieldListArrayName(int index);

 
protected:
  ReadUALEdge();
  ~ReadUALEdge(){}

  int Shot;
  int BOX_TEST; //DP_13_7_2015
  int Run;
  int RefRun;
  int CPOLoad;
  int FieldLoadStatus;
  char * User;
  char * Tokamak;
  char * Version;
  vtkSmartPointer<vtkDataArraySelection> trial; 
  vtkSmartPointer<vtkDataArraySelection> fields;  


  int RequestData(vtkInformation *, vtkInformationVector **,
                  vtkInformationVector *);

private:
  ReadUALEdge(const ReadUALEdge&);  // Not implemented.
  void operator=(const ReadUALEdge&);  // Not implemented.
 
};
 
#endif
