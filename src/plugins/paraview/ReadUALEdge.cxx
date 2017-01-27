#include <iostream>
#include <fstream>
#include <string>
#include "vtkVersion.h"
#include "vtkSmartPointer.h"
#include "vtkTable.h"
#include "vtkFloatArray.h"
#include "vtkIntArray.h"
#include "vtkCellArray.h"
#include "vtkPointData.h"
#include "ReadUALEdge.h"
#include "vtkUnstructuredGrid.h"
#include "vtkMultiBlockDataSet.h"
#include "vtkObjectFactory.h"
#include "vtkInformationVector.h"
#include "vtkInformation.h"
#include "vtkDataObject.h"
#include "vtkDoubleArray.h"
#include "vtkCellData.h"
#include "vtkPoints.h"
#include "vtkPolyData.h"
#include "vtkQuad.h"
#include "UALClasses.h"
#include <vtkLine.h>
#include <vtkVertex.h>
#include <vtkStringArray.h>
#include <dirent.h>
#include <vector> 
#include <sys/stat.h>
#include <unistd.h>

#define IMAS_IDS

// From itmggd/c/src/constants/itm_grid_coordinates.h
#define COORDTYPE_X              1  // X [m]
#define COORDTYPE_Y              2  // Y [m]
#define COORDTYPE_R              4  // Major radius R [m]
#define COORDTYPE_Z              5  // Vertical height Z [m]
#define COORDTYPE_PHI            6  // Toroidal angle phi [rad]
#define COORDTYPE_PSI            7  // Radial flux coordinate psi
#define COORDTYPE_THETA          8  // Poloidal angle theta [rad]

#define SSTR( x ) dynamic_cast< std::ostringstream & >(                 \
                ( std::ostringstream() << std::dec << x ) ).str()

vtkStandardNewMacro(ReadUALEdge);

ReadUALEdge::ReadUALEdge() 
{
  this->User = NULL;
  this->Device = NULL;
  this->Version = NULL;
  this->RefRun = 0;
  this->SetNumberOfInputPorts(0);
  this->SetNumberOfOutputPorts(1);
  this->DebugOff();
	this->stringArray=vtkSmartPointer<vtkStringArray>::New();
}

std::vector<std::string> findShotRun(std::string userIMASShotRunDir, std::string user){
  // Function for reading directory with shot/run-s and inserting the found shot/runs into vector for later use
  DIR *pDIR = NULL;
  struct dirent *entry = NULL;
  std::string dirPath = userIMASShotRunDir;
  std::vector<std::string> availableShotRun; 
  std::string d_name_str;
  int digitInStrCount = 0;
  std::string stripShot;
  std::string stripRun;

  struct stat sb;
  if(string(user)=="")
    {
      char *loginUserName = getlogin();
      user = string(loginUserName);
    }
  
  // Checking if the directory exists
  if (stat(dirPath.c_str(), &sb) == 0 && S_ISDIR(sb.st_mode))
    {
      std::clog <<"IDS directory from user " << user << " found. Reading available IDS shot/runs." << std::endl;
      if( pDIR=opendir(dirPath.c_str()))
	{
	  while(entry = readdir(pDIR))
	    {
	      if( strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0 )
		// Reading all files in directory
		{
		  d_name_str = std::string(entry->d_name);
		  int d_name_str_len = d_name_str.length();
		  
		  if(d_name_str.substr( d_name_str_len - 5 ) == ".tree")
		    // We want to work only with .tree files.
		    {
		      for(int i = 0; i < d_name_str.length(); i++)
			{
			  if(isdigit(d_name_str[i])) digitInStrCount++;       
			}
		      int numExtCh = 5;   // 5 is for ".tree" == 5 characters.
		      int numRunMax = 4;  // Run consists of max 4 characters (from 0000 to 9999).
		      stripShot = d_name_str.substr(d_name_str_len-numExtCh-digitInStrCount,digitInStrCount-numRunMax);
		      stripRun = d_name_str.substr(d_name_str_len-numExtCh-numRunMax,numRunMax);
		      // In case of numbers in the front of Run we want to get rid of them (example 0011->11).
		      int stripRunStartLen = stripRun.length(); 
		      int eraseCount = 0;
		      while(stripRun[0] == '0' && eraseCount < stripRunStartLen-1)
			{
			  stripRun.erase(0,1);
			  eraseCount++;
			}
		      // Now stripShot and stripRun are in wanted form.
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

vtkSmartPointer<vtkDoubleArray> fCreateNewDoubleArray(int ndarray_num_tuples, std::string ndarray_name, int ndarray_id = -1)
//Function for creating vtk double arrays
{
  vtkSmartPointer<vtkDoubleArray> newDoubleArray = vtkSmartPointer<vtkDoubleArray>::New();
  newDoubleArray->SetNumberOfComponents(1);
  newDoubleArray->SetNumberOfTuples(ndarray_num_tuples);
  std::string set_name = ndarray_name;
  if (ndarray_id != -1)
    {
      set_name = set_name + SSTR(ndarray_id+1);
    }   
  newDoubleArray->SetName(set_name.c_str()); 
  return newDoubleArray;
}

int ReadUALEdge::RequestData(
			     vtkInformation *vtkNotUsed(request),
			     vtkInformationVector **vtkNotUsed(inputVector),
			     vtkInformationVector *outputVector)
{
  // get the info object
  vtkInformation *outInfo = outputVector->GetInformationObject(0);
  // get the output
  vtkMultiBlockDataSet *output = vtkMultiBlockDataSet::SafeDownCast(
		     outInfo->Get(vtkMultiBlockDataSet::DATA_OBJECT()));

  std::clog << "Shot:" << this->Shot << " Run:" << this->Run << std::endl;

#ifdef IMAS_IDS
  using namespace IdsNs;
  std::clog << "Reading IDS" << std::endl;
  IDS db(this->Shot, this->Run, this->Shot, this->RefRun);
  if (!this->Version)
    this->Version = strdup("3");
  db.openEnv(this->User, this->Device, this->Version);
  std::clog << "User: "<<this->User<<" Device:"<<this->Device<< std::endl;
  db._edge_profiles.get();
#if 0
  // Example: Printing IMAS/IDS database data to .txt file
  //db._edge_profiles.getSlice(time, INTERPOLATION);
  db._edge_profiles.getSlice(1,1);
  ofstream myfile;
  myfile.open ("log_ids_edge_profiles.txt");
  myfile << db._edge_profiles;
  myfile.close();
  //std::cout << db._edge_profiles << std::endl;
#endif
  
  int num_slices = db._edge_profiles.ggd.extent(0);
  std::clog << "slices:" << num_slices << std::endl;
  if (num_slices == 0) 
    {
      std::clog << "ERROR! Either selected database doesn't exist or it's empty!" << std::endl;
      vtkErrorMacro(<<"ERROR! Either selected database doesn't exist or it's empty!");
      return 0;
    }
  
  class IDS::edge_profiles & edge = db._edge_profiles;
  class IDS::edge_profiles::ggd & ggd = edge.ggd(0);
  class IDS::edge_profiles::ggd::grid & grid = ggd.grid;
  class IDS::edge_profiles::ggd::grid::space & space = grid.space(0);
  class IDS::edge_profiles::ggd::grid::space::objects_per_dimension & dim_nodes = space.objects_per_dimension(0);
  class IDS::edge_profiles::ggd::grid::space::objects_per_dimension & dim_edges = space.objects_per_dimension(1);
  class IDS::edge_profiles::ggd::grid::space::objects_per_dimension & dim_cells = space.objects_per_dimension(2);
  
  // Checking, if we have nodes, edges and cells data in current IDS database
  int num_nodes_nodes = 0;
  int num_nodes_geo = 0;
  int num_edges_nodes = 0;
  int num_cells_nodes = 0;
  
  if (dim_nodes.object.extent(0) > 0){
    num_nodes_nodes = dim_nodes.object(0).nodes.extent(0);
    num_nodes_geo = dim_nodes.object(0).geometry.extent(0);
  }
  if (dim_edges.object.extent(0) > 0){
    num_edges_nodes = dim_nodes.object(0).nodes.extent(0)/2;
  }
  if (dim_cells.object.extent(0) > 0){
    num_cells_nodes = dim_cells.object(0).nodes.extent(0)/4;
  }
  
//   std::clog << "dim_nodes.object.extent(0): " << dim_nodes.object.extent(0) << std::endl;
//   std::clog << "dim_edges.object.extent(0): " << dim_edges.object.extent(0) << std::endl;
//   std::clog << "dim_cells.object.extent(0): " << dim_cells.object.extent(0) << std::endl;  
  
  std::clog << "num_nodes_geo: " << num_nodes_geo << std::endl;
  std::clog << "num_nodes_nodes: " << num_nodes_nodes << std::endl;
  std::clog << "num_edges_nodes: " << num_edges_nodes << std::endl;
  std::clog << "num_cells_nodes: " << num_cells_nodes << std::endl;

  //vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  vtkSmartPointer<vtkQuad> Quad =  vtkSmartPointer<vtkQuad>::New();
  vtkSmartPointer<vtkCellArray> cellArray = vtkSmartPointer<vtkCellArray>::New();
  vtkSmartPointer<vtkMultiBlockDataSet> mainMB = vtkSmartPointer<vtkMultiBlockDataSet>::New();
  
  vtkSmartPointer<vtkPoints> points_global = vtkSmartPointer<vtkPoints>::New();
  
  for(int i=0; i < num_nodes_nodes; ++i){
    points_global->InsertNextPoint(dim_nodes.object(0).geometry(i), dim_nodes.object(0).geometry(num_nodes_nodes+i), 0.0);
  }
  
  int num_subgrids = grid.grid_subset.extent(0);

  for(int i = 0; i < num_subgrids; i++){
    int subgrid_class = grid.grid_subset(i).element(0).object(0).dimension; // 0 -> nodes; 1 -> edges; 2 -> faces/cells
    int subgrid_space = grid.grid_subset(i).element(0).object(0).space;
    int subgrid_class_object_id = grid.grid_subset(i).element(0).object(0).index;  
    std::string subgrid_name = grid.grid_subset(i).identifier.name;
    int subgrid_base_id = grid.grid_subset(i).identifier.index; 
    
    //getting sizes of subgrids (we need that now, because vtkDoubleArrays, which take size as one of parameters, must be defined insite this loop, not later!)
    int size = 0;
    if (subgrid_class -1 == 0){
      size = dim_nodes.object(subgrid_class_object_id-1).nodes.extent(0);
    } else if (subgrid_class - 1 == 1){
      size = dim_edges.object(subgrid_class_object_id-1).nodes.extent(0)/2;
    } else if (subgrid_class -1 == 2){
      size = dim_cells.object(subgrid_class_object_id-1).nodes.extent(0)/4;
    }

    //std::clog << i << "  " << subgrid_base_id << "  " <<  subgrid_class_object_id << "  " <<  subgrid_name << "  " <<  subgrid_class << std::endl;
    vtkSmartPointer<vtkCellArray> subgridCellArray = vtkSmartPointer<vtkCellArray>::New();
    
    //ELECTRON TEMPERATURE creating array
    vtkSmartPointer<vtkDoubleArray> electronTemperatureArray = fCreateNewDoubleArray(size, "Electron Temperature");
      
    //ELECTRON DENSITY creating array
    vtkSmartPointer<vtkDoubleArray> electronDensityArray = fCreateNewDoubleArray(size, "Electron Density");
    //
    if (subgrid_class - 1 == 0){ // ------POINTS/NODES-----
      //class IDS::edge_profiles::ggd::grid::space::objects_per_dimension::object & object_nodes = dim_nodes.object(subgrid_class_object_id-1);
      vtkSmartPointer<vtkUnstructuredGrid> subgridPointsUnstructuredGrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
      
      //int size = dim_nodes.object(subgrid_class_object_id-1).nodes.extent(0);
      //std::clog << "subgrid " << subgrid_base_id << " class 0 size: "<< size << std::endl;

      //////////Setting points
      vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
      vtkSmartPointer<vtkCellArray> subgridVertices = vtkSmartPointer<vtkCellArray>::New();
      vtkSmartPointer<vtkVertex> subgridVertex = vtkSmartPointer<vtkVertex>::New();
      for (int j = 0; j < size; j++){
	points->InsertNextPoint(dim_nodes.object(subgrid_class_object_id-1).geometry(j), dim_nodes.object(subgrid_class_object_id-1).geometry(size+j), 0.0);
	subgridVertex->GetPointIds()->SetId(0, j);
	subgridVertices->InsertNextCell(subgridVertex);
      }
      subgridPointsUnstructuredGrid->SetPoints(points);
      subgridPointsUnstructuredGrid->SetCells(VTK_VERTEX, subgridVertices);
      
      //ELECTRON TEMPERATURE creating array
      //vtkSmartPointer<vtkDoubleArray> electronTemperatureArray = fCreateNewDoubleArray(size, "Electron Temperature ");
      int te_subgrids_num = ggd.electrons.temperature.extent(0); 
    
      //ELECTRON DENSITY creating array
      //vtkSmartPointer<vtkDoubleArray> electronDensityArray = fCreateNewDoubleArray(size, "Electron Density ");
      int ne_subgrids_num = ggd.electrons.density.extent(0);

      // Getting vertex colored by reading scalars from electron temperature subgrids (nodes)
      for (int n = 0; n < te_subgrids_num; n++){
	int te_subgrid_base_id = ggd.electrons.temperature(n).grid_subset_index;
	
	if (subgrid_base_id == te_subgrid_base_id && size == ggd.electrons.temperature(n).values.extent(0)){ //If database was written correctly, then the size of subgrid geometry(nodes) and subgrid values (scalars) are of the same size
	  electronTemperatureArray->SetNumberOfValues(size);
	  
	  for (int j = 0; j < size; j++){
	    //std::clog << "j: " << j << " x: " << dim_nodes.object(subgrid_class_object_id-1).geometry(j) << " y: " << dim_nodes.object(subgrid_class_object_id-1).geometry(size+j) << std::endl;
	    electronTemperatureArray->SetComponent(j,0, ggd.electrons.temperature(n).values(j));
	  }
	  subgridPointsUnstructuredGrid->GetCellData()->AddArray(electronTemperatureArray);
	  break;
	}
      }
    
    
      // Getting vertex colored by reading scalars from electron density subgrids (nodes)
      for (int n = 0; n < ne_subgrids_num; n++){
	int ne_subgrid_base_id = ggd.electrons.density(n).grid_subset_index;
	
	if (subgrid_base_id == ne_subgrid_base_id && size == ggd.electrons.density(n).values.extent(0)){ //If database was written correctly, then the size of subgrid geometry(nodes) and subgrid values (scalars) are of the same size
	  electronDensityArray->SetNumberOfValues(size);
	  for (int j = 0; j < size; j++){
	    electronDensityArray->SetComponent(j,0, ggd.electrons.density(n).values(j));
	  }
	  subgridPointsUnstructuredGrid->GetCellData()->AddArray(electronDensityArray);
	  break;
	}
      }
      
      // Getting vertex colored by reading scalars from ion temperature subgrids (nodes)
      int ti_species_num = ggd.ion.extent(0); //CHANGE TO ion_species_num and combine ion density and ion temperature into single ion_species_num loop
      
      for( int k = 0; k < ti_species_num; k++){
	vtkSmartPointer<vtkDoubleArray> ionTemperatureArray = fCreateNewDoubleArray(size, "Ion Temperature");
	int ti_subgrids_num = ggd.ion(k).temperature.extent(0);
	
	for (int n = 0; n < ti_subgrids_num; n++){
	  int ti_subgrid_base_id = ggd.ion(k).temperature(n).grid_subset_index;
	  
	  if (subgrid_base_id == ti_subgrid_base_id && size == ggd.ion(k).temperature(n).values.extent(0)){ //If database was written correctly, then the size of subgrid geometry(nodes) and subgrid values (scalars) are of the same size
	    ionTemperatureArray->SetNumberOfValues(size);
	    
	    for (int j = 0; j < size; j++){
	      ionTemperatureArray->SetComponent(j,0, ggd.ion(k).temperature(n).values(j));
	    }
	    subgridPointsUnstructuredGrid->GetCellData()->AddArray(ionTemperatureArray);
	    break;
	  }
	}
      }
      
      // Getting vertex colored by reading scalars from ion density subgrids (nodes)
      int ni_species_num = ggd.ion.extent(0);
      
      for( int k = 0; k < ni_species_num; k++){
	std::string ion_charge= ggd.ion(k).label;
	stringstream ni_species_num2str;
	ni_species_num2str << k+1;
	string ni_species_num_str = ni_species_num2str.str();
	
	std::string ni_array_string;
	if (k < 9){
	  ni_array_string = "Ion Density 0" + ni_species_num_str + ion_charge;
	} else {
	  ni_array_string = "Ion Density " + ni_species_num_str + ion_charge;
	}
	vtkSmartPointer<vtkDoubleArray> ionDensityArray = fCreateNewDoubleArray(size, ni_array_string);
	int ni_subgrids_num = ggd.ion(k).density.extent(0);
	
	for (int n = 0; n < ni_subgrids_num; n++){
	  int ni_subgrid_base_id = ggd.ion(k).density(n).grid_subset_index;
	  
	  if (subgrid_base_id == ni_subgrid_base_id && size == ggd.ion(k).density(n).values.extent(0)){ //If database was written correctly, then the size of subgrid geometry(nodes) and subgrid values (scalars) are of the same size
	    ionDensityArray->SetNumberOfValues(size);
	    
	    for (int j = 0; j < size; j++){
	      ionDensityArray->SetComponent(j,0, ggd.ion(k).density(n).values(j));
	    }
	    subgridPointsUnstructuredGrid->GetCellData()->AddArray(ionDensityArray);
	    break;
	  }
	}
      }
      
      //Getting all subgrids to main block
      //std::clog << "i: " << i << " subgrid_base_id: " << subgrid_base_id << std::endl;
      
      int num_blocks = mainMB->GetNumberOfBlocks();
      //std::clog << "num_blocks:" << num_blocks << std::endl;
      mainMB->SetBlock(num_blocks, subgridPointsUnstructuredGrid);
      mainMB->GetMetaData((unsigned int) num_blocks)->Set(vtkCompositeDataSet::NAME(), subgrid_name.c_str()); 
      //}
#if 1
    } else if (subgrid_class -1 == 1){  //------LINES-----
      //vtkSmartPointer<vtkPoints> subgridLinesPoints = vtkSmartPointer<vtkPoints>::New();
      vtkSmartPointer<vtkUnstructuredGrid> subgridLinesUnstructuredGrid =vtkSmartPointer<vtkUnstructuredGrid>::New();
      vtkSmartPointer<vtkCellArray> subgridLinesArray = vtkSmartPointer<vtkCellArray>::New();
      
      //int size = dim_edges.object(subgrid_class_object_id-1).nodes.extent(0)/2;
      //std::clog << "subgrid " << subgrid_base_id << "  class 1 size: "<< size << std::endl;
      
      for(int j = 0; j < size; j++)
	{
	  vtkSmartPointer<vtkLine> subgridLine = vtkSmartPointer<vtkLine>::New();
	  
	  int line_ind_0 = dim_edges.object(subgrid_class_object_id-1).nodes(j)-1;
	  int line_ind_1 = dim_edges.object(subgrid_class_object_id-1).nodes(size+j)-1;
	  
	  /*
	    if (j < 100){
	    std::clog << line_ind_0 << "  " << line_ind_1 << std::endl;
	    }
	  */
	  subgridLine ->GetPointIds()->SetId(0, line_ind_0);
	  subgridLine ->GetPointIds()->SetId(1, line_ind_1);
	  subgridLinesArray->InsertNextCell(subgridLine);
	}
      
      subgridLinesUnstructuredGrid->SetPoints(points_global);
      subgridLinesUnstructuredGrid->SetCells(VTK_LINE, subgridLinesArray);
      
      //Getting all subgrids to main block
      int num_blocks = mainMB->GetNumberOfBlocks();
      //std::clog << "num_blocks:" << num_blocks << std::endl;
      mainMB->SetBlock(num_blocks, subgridLinesUnstructuredGrid);
      mainMB->GetMetaData((unsigned int) num_blocks)->Set(vtkCompositeDataSet::NAME(), subgrid_name.c_str()); 
      
    } else if (subgrid_class -1 == 2){ //-----CELLS------
      vtkSmartPointer<vtkUnstructuredGrid> subgridCellsUnstructuredGrid =vtkSmartPointer<vtkUnstructuredGrid>::New();
      vtkSmartPointer<vtkQuad> subgridQuad =  vtkSmartPointer<vtkQuad>::New();
      vtkSmartPointer<vtkCellArray> subgridCellArray = vtkSmartPointer<vtkCellArray>::New();
      
      //int size = dim_cells.object(subgrid_class_object_id-1).nodes.extent(0)/4;
      //std::clog << "subgrid " << subgrid_base_id << "  class 2 size: "<< size << std::endl;

      for(int j = 0; j < size; j++)
      {
	int cell_ind_0 = dim_cells.object(subgrid_class_object_id-1).nodes(j)-1;
	int cell_ind_1 = dim_cells.object(subgrid_class_object_id-1).nodes(size+j)-1;
	int cell_ind_2 = dim_cells.object(subgrid_class_object_id-1).nodes(2*size+j)-1;
	int cell_ind_3 = dim_cells.object(subgrid_class_object_id-1).nodes(3*size+j)-1;
#if 0
        if(j < 300){
	  std::clog << j << ": " << cell_ind_0 << " " << cell_ind_1 << " " << cell_ind_2 << " " << cell_ind_3 << std::endl;
        }
#endif
	
	subgridQuad->GetPointIds()->SetId(0,cell_ind_0);
	subgridQuad->GetPointIds()->SetId(1,cell_ind_1);
	subgridQuad->GetPointIds()->SetId(2,cell_ind_2);
	subgridQuad->GetPointIds()->SetId(3,cell_ind_3);
	subgridCellArray->InsertNextCell(subgridQuad);
	
      }
      int te_subgrids_num = ggd.electrons.temperature.extent(0);
      int ne_subgrids_num = ggd.electrons.density.extent(0);
      //std::clog << "subgrid_class_object_id: " << subgrid_class_object_id << std::endl;
      for (int n = 0; n < te_subgrids_num; n++){ //te_subgrids_num == ne_subgrids_num, thats why we can include also electron density in the next coming loops
	int te_subgrid_base_id = ggd.electrons.density(n).grid_subset_index;
	if (subgrid_base_id == te_subgrid_base_id && size == ggd.electrons.temperature(n).values.extent(0)){ //If database was written correctly, then the size of subgrid geometry(nodes) and subgrid values (scalars) are of the same size
	  for(int j = 0; j < size; j++){
	    //ELECTRON DENSITY and ELECTRON TEMPERATURE
	    electronTemperatureArray->SetComponent(j, 0, ggd.electrons.temperature(n).values(j));
	    electronDensityArray->SetComponent(j, 0, ggd.electrons.density(n).values(j));
	  }
	  break;
	}
      }
      
      subgridCellsUnstructuredGrid->SetPoints(points_global);
      subgridCellsUnstructuredGrid->SetCells(VTK_QUAD, subgridCellArray);
      //Setting Electron Density and Electron Temperature to UnstructuredGrid
      subgridCellsUnstructuredGrid->GetCellData()->AddArray(electronTemperatureArray);
      subgridCellsUnstructuredGrid->GetCellData()->AddArray(electronDensityArray);
      
      //ION DENSITY AND ION TEMPERATURE
      int ion_species_num = ggd.ion.extent(0);
      for(int k = 0; k < ion_species_num; k++){
	std::string ion_charge  = ggd.ion(k).label;
	stringstream ni_species_num2str;
	ni_species_num2str << k+1;
	string ni_species_num_str = ni_species_num2str.str();
	
	std::string ni_array_string;
	if (k < 9){
	  ni_array_string = "Ion Density 0" + ni_species_num_str + ion_charge;
	} else {
	  ni_array_string = "Ion Density " + ni_species_num_str + ion_charge;
	}
	vtkSmartPointer<vtkDoubleArray> ionDensityArray = fCreateNewDoubleArray(size, ni_array_string);
	
	vtkSmartPointer<vtkDoubleArray> ionTemperatureArray = fCreateNewDoubleArray(size, "Ion Temperature");
	int ni_subgrids_num = ggd.ion(k).density.extent(0);
	int ti_subgrids_num = ggd.ion(k).temperature.extent(0);
	
	for(int n = 0; n < ni_subgrids_num; n++){
	  int ni_subgrid_base_id = ggd.ion(k).density(n).grid_subset_index;
	  if (subgrid_base_id == ni_subgrid_base_id && size == ggd.ion(k).density(n).values.extent(0)){
	    for (int j = 0; j < size; j++){
	      //std::clog << j << std::endl;
	      ionDensityArray->SetComponent(j, 0, ggd.ion(k).density(n).values(j));
	    }
	    subgridCellsUnstructuredGrid->GetCellData()->AddArray(ionDensityArray);
	    break;
	  }
	}
	
	//std::clog << "ti_subgrids_num" << ti_subgrids_num << std::endl;
	for (int n = 0; n < ti_subgrids_num; n++){
	  int ti_subgrid_base_id = ggd.ion(k).temperature(n).grid_subset_index;
	  
	  if (subgrid_base_id == ti_subgrid_base_id && size == ggd.ion(k).temperature(n).values.extent(0)){
	    for (int j = 0; j < size; j++){
	      //std::clog << j << " " << ggd.ion(k).temperature(n).values(j) << std::endl;
	      ionTemperatureArray->SetComponent(j, 0, ggd.ion(k).temperature(n).values(j));
	    }
	    subgridCellsUnstructuredGrid->GetCellData()->AddArray(ionTemperatureArray);
	    break;
	  }
	}
      }
      int num_blocks = mainMB->GetNumberOfBlocks();
      mainMB->SetBlock(num_blocks, subgridCellsUnstructuredGrid);
      mainMB->GetMetaData((unsigned int) num_blocks)->Set(vtkCompositeDataSet::NAME(), subgrid_name.c_str());
    }
#endif
  }
  
  output->ShallowCopy(mainMB);
  db.close();
  
#else  // CPO
  ItmNs::Itm itm(this->Shot,this->Run,this->Shot,this->RefRun);

  if (!this->Version)
    this->Version = strdup("4.10a");
  itm.openEnv(this->User, this->Device, this->Version); //Open the database
  std::clog << "User: "<<this->User<<" Device:"<<this->Device<< std::endl;
  
  itm._edgeArray.get();
  
  int num_slices = itm._edgeArray.extent(0);
  if (num_slices == 0) 
    {
      std::clog << "ERROR! Either selected database doesn't exist or it's empty!" << std::endl;
      return 0;
    }
  
  class ItmNs::Itm::edge & edge = itm._edgeArray[0];
  class ItmNs::Itm::edge::grid & grid = edge.grid;  
  class ItmNs::Itm::edge::grid::spaces & space = grid.spaces(0);
  class ItmNs::Itm::edge::grid::spaces::objects & nodes = space.objects(0);
  class ItmNs::Itm::edge::grid::spaces::objects & edges = space.objects(1); 
  class ItmNs::Itm::edge::grid::spaces::objects & cells = space.objects(2); 
  
  std::clog << "grid id: " << grid.id << std::endl;
  
  int num_spaces = grid.spaces.extent(0);
  std::clog << "num_spaces: " << num_spaces << std::endl;
  grid.spaces.extent(0);
  
  int num_coordtypes =  space.coordtype.extent(0);
  
  if (num_spaces != 1 && num_coordtypes != 2) {
    std::clog << "Unhandled space configuration!" << std::endl;
    return 0;
  }
  
  // Assure we are reading SOLPS grid
  assert(space.coordtype(0,0) == COORDTYPE_R);
  assert(space.coordtype(1,0) == COORDTYPE_Z);
  // assert(space.objects.extent(0) == 1);

  int num_objects = space.objects.extent(0);
  std::clog << "num_objects: " << num_objects << std::endl;
  
  int num_nodes = nodes.geo.extent(0);
  std::clog << "num_nodes: " << num_nodes << std::endl;
  
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  
  for(int i=0; i < num_nodes; ++i){
    points->InsertNextPoint(nodes.geo(i, 0), nodes.geo(i, 1), 0.0);
  }
  
  // 2D cells in GGD are defined by edges. Edges have indices to nodes.
  
  int num_edges = edges.boundary.extent(0);   
  int num_cells = cells.boundary.extent(0);
  
  std::clog << "num_cells :" << num_cells << std::endl;
  
  vtkSmartPointer<vtkQuad> subgridQuad =  vtkSmartPointer<vtkQuad>::New();
  vtkSmartPointer<vtkCellArray> cellArray = vtkSmartPointer<vtkCellArray>::New();
  vtkSmartPointer<vtkMultiBlockDataSet> mainMB = vtkSmartPointer<vtkMultiBlockDataSet>::New();
  
  double all_cells[num_cells][4]; 
  for (int i = 0; i < num_cells; ++i) {
    int node_idx[4]; // Resulting node indices for a cell
    int free_edge[3]; // list of edges that are free to search for node
    int last_idx; // last node index 
    int edge_idx = cells.boundary(i, 0) - 1;
    free_edge[0] = cells.boundary(i, 1) - 1;
    free_edge[1] = cells.boundary(i, 2) - 1;
    free_edge[2] = cells.boundary(i, 3) - 1;
    
    node_idx[0] = edges.boundary(edge_idx, 0) - 1;
    node_idx[last_idx=1] = edges.boundary(edge_idx, 1) - 1;
    
    for(int loop_count = 0; last_idx < 3 && loop_count < 4; ++loop_count){
      for(int j = 0; j < 3 ; ++j) { // free_edge
	edge_idx = free_edge[j];
	if(edge_idx < 0)
	  continue;
	int node1 =  edges.boundary(edge_idx, 0) - 1;
	int node2 =  edges.boundary(edge_idx, 1) - 1;
	
	if (node_idx[last_idx] == node1) {
	  free_edge[j] = -1;
	  node_idx[++last_idx] = node2;
	  break;
	}
	if (node_idx[last_idx] == node2) {
	  free_edge[j] = -1;
	  node_idx[++last_idx] = node1;
	  break;
	}
      }
      assert(loop_count < 3);
    }
    all_cells[i][0] = node_idx[0];
    all_cells[i][1] = node_idx[1];
    all_cells[i][2] = node_idx[2];
    all_cells[i][3] = node_idx[3];
  } 
  
  // Checking contents under po (electric potential)
  class ItmNs::Itm::edge::fluid::po & po = edge.fluid.po;
  std::clog << std::left << setw(35) << "po.value(0).extent(0): _______" << edge.fluid.po.value.extent(0) << std::endl;
  std::clog << std::left << setw(35) << "po.value(0).scalar.extent(0): ___" << edge.fluid.po.value(0).scalar.extent(0) << std::endl;
  
  //std::clog << "ne_value.subgrid: " << ne_value.subgrid << std::endl;
  int num_ni_species = edge.fluid.ni.extent(0);
  std::clog << "Number of Ion Density species:" << num_ni_species << std::endl;
  int num_ti_species = edge.fluid.ti.extent(0);
  std::clog << "Number of Ion Temperature species:" << num_ti_species << std::endl;
  
  int num_subgrids = grid.subgrids.extent(0);
  std:: subgridName[num_subgrids];
  std::clog << "num_subgrids: "<< num_subgrids << std::endl; 
  std::clog << "Setting scalars" << std::endl;
  for(int i = 0; i < num_subgrids; i++) 
    {  
      int subgrid_class = grid.subgrids(i).list(0).cls(0);
      int ind_num = grid.subgrids(i).list(0).ind.extent(0);
      subgridName[i] = grid.subgrids(i).id;
      int indset_found = grid.subgrids(i).list(0).indset.extent(0); // grid.subgrids(i).list(0).indset contains range for certain subgrid. 
      // If indset is not found then also there is no range for that subgrid.
      std::clog << std::left << "Subgrid id number: " << setw(2) << i+1 << " Subgrid name: " << setw(18) << subgridName[i] << " Subgrid class: " << setw(1) << subgrid_class << " ";
      
      int range0 = 0;
      int range1 = 0;
      int range_found;
      int start_index;
      int end_index;
      int jIndex = 0;
      int array_size;
      
      if(indset_found > 0)
	{
	  int range_size = grid.subgrids(i).list(0).indset(0).range.extent(0);
	  if(range_size > 1)
	    {
	      range_found = 1;
	      range0 = grid.subgrids(i).list(0).indset(0).range(0) - 1;
	      range1 = grid.subgrids(i).list(0).indset(0).range(1);
	      start_index = range0;
	      end_index = range1;
	      std::clog << std::left << " range: " << setw(4) << range0+1 << " - " << setw(4) << range1;
	      array_size = end_index - start_index;
	    }else{
	    std::clog << "Range is either EMPTY or it doesn't exist" << std::endl;
	  }
	}else
	{
	  range_found = 0;
	  start_index = grid.subgrids(i).list(0).ind(0,0) - 1;
	  end_index = grid.subgrids(i).list(0).ind(ind_num-1,0) - 1;
	  std::clog << std::left << setw(19) << "range: not found";
	  array_size = ind_num;
	}
      
      int index_array[array_size];
      std::clog << "  index_Array size: " << sizeof(index_array)/sizeof(*index_array) << std::endl;
      
      if(range_found == 1)
	{
	  for(int j = start_index; j < end_index; j++)
	    {
	      index_array[j-start_index] = j;
	    }
	} else {
	for(int j = 0; j < ind_num; j++)
	  {
	    jIndex = grid.subgrids(i).list(0).ind(j,0) - 1; 
	    index_array[j] = jIndex;
	  }
      } 
      
      int size = (sizeof(index_array)/sizeof(*index_array));
      
      vtkSmartPointer<vtkCellArray> subgridCellArray = vtkSmartPointer<vtkCellArray>::New();
      
      //ELECTRON TEMPERATURE creating array
      vtkSmartPointer<vtkDoubleArray> electronTemperatureArray = fCreateNewDoubleArray(size, "Electron Temperature");
      
      //ELECTRON DENSITY creating array
      vtkSmartPointer<vtkDoubleArray> electronDensityArray = fCreateNewDoubleArray(size, "Electron Density");
      
      //ELECTRIC POTENTIAL creating array
      vtkSmartPointer<vtkDoubleArray> electricPotentialArray = fCreateNewDoubleArray(size, "Electric Potential");
      
      if(subgrid_class == 0) // POINTS/NODES
	{
	  vtkSmartPointer<vtkUnstructuredGrid> subgridPointsUnstructuredGrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
	  // Getting vertex colored by reading scalars from electron density subgrids (nodes) 
	  int ne_subgrid_num = edge.fluid.ne.value.extent(0);
	  for(int n = 0; n < ne_subgrid_num; n++)
	    {
	      int ne_subgrid_ind = edge.fluid.ne.value(n).subgrid; 
	      if(i+1 == edge.fluid.ne.value(n).subgrid) // +1 because in GGD index starts with 1 and not with 0 as in C++
		{
		  vtkSmartPointer<vtkCellArray> subgridVertices = vtkSmartPointer<vtkCellArray>::New();
		  vtkSmartPointer<vtkVertex> subgridVertex = vtkSmartPointer<vtkVertex>::New();
		  
		  electronDensityArray->SetNumberOfValues(size);
		  for(int j = 0; j < size; j++)
		    {
		      points->InsertNextPoint(nodes.geo(index_array[j], 0), nodes.geo(index_array[j], 1), 0.0);
		      subgridVertex->GetPointIds()->SetId(0, j);
		      subgridVertices->InsertNextCell(subgridVertex);
		      electronDensityArray->SetComponent(j, 0, edge.fluid.ne.value(n).scalar(j)); 
		    }
		  
		  // To add new array Electron Density (Cells) as unstructuredGrid
		  subgridPointsUnstructuredGrid->SetPoints(points);
		  subgridPointsUnstructuredGrid->SetCells(VTK_VERTEX, subgridVertices);
		  subgridPointsUnstructuredGrid->GetCellData()->AddArray(electronDensityArray);
		}
	    }
	  
	  // Getting vertex colored by reading scalars from electron temperature subgrids (nodes) 
	  int te_subgrid_num = edge.fluid.te.value.extent(0);
	  for(int n = 0; n < te_subgrid_num; n++)
	    {
	      int te_subgrid_ind = edge.fluid.te.value(n).subgrid; 
	      if(i+1 == edge.fluid.te.value(n).subgrid) // +1 because in GGD index starts with 1 and not with 0 as in C++
		{
		  vtkSmartPointer<vtkCellArray> subgridVertices = vtkSmartPointer<vtkCellArray>::New();
		  vtkSmartPointer<vtkVertex> subgridVertex = vtkSmartPointer<vtkVertex>::New();
		  electronTemperatureArray->SetNumberOfValues(size);
		  for(int j = 0; j < size; j++)
		    {
		      points->InsertNextPoint(nodes.geo(index_array[j], 0), nodes.geo(index_array[j], 1), 0.0);
		      subgridVertex->GetPointIds()->SetId(0, j);
		      subgridVertices->InsertNextCell(subgridVertex);
		      electronTemperatureArray->SetComponent(j, 0, edge.fluid.te.value(n).scalar(j)); 
		    }
		  
		  // To add new array Electron Temperature (Cells) as unstructuredGrid
		  subgridPointsUnstructuredGrid->SetPoints(points);
		  subgridPointsUnstructuredGrid->SetCells(VTK_VERTEX, subgridVertices);
		  subgridPointsUnstructuredGrid->GetCellData()->AddArray(electronTemperatureArray);
		}
	    }
	  
	  // Getting vertex colored by reading scalars from ion density subgrids (nodes) 
	  for(int k = 0; k < num_ni_species; k++)
	    {
	      std::string ion_charge = edge.species(k).label;
	      stringstream ni_species_num2str;
	      ni_species_num2str << k+1;
	      string ni_species_num_str = ni_species_num2str.str();
	      std::string ni_array_string;
	      if (k < 9){
		ni_array_string = "Ion Density 0" + ni_species_num_str + ion_charge;
	      }else{
		ni_array_string = "Ion Density " + ni_species_num_str + ion_charge;
	      }
	      vtkSmartPointer<vtkDoubleArray> ionDensityArray = fCreateNewDoubleArray(size, ni_array_string);
	      int ni_subgrid_num = edge.fluid.ni(k).value.extent(0);
	      for(int n = 0; n < ni_subgrid_num; n++)
		{
		  int ni_subgrid_ind = edge.fluid.ni(k).value(n).subgrid; 
		  if(i+1 == edge.fluid.ni(k).value(n).subgrid) // +1 because in GGD index starts with 1 and not with 0 as in C++
		    {
		      
		      vtkSmartPointer<vtkCellArray> subgridVertices = vtkSmartPointer<vtkCellArray>::New();
		      vtkSmartPointer<vtkVertex> subgridVertex = vtkSmartPointer<vtkVertex>::New();
		      
		      ionDensityArray->SetNumberOfValues(size);
		      for(int j = 0; j < size; j++)
			{
			  points->InsertNextPoint(nodes.geo(index_array[j], 0), nodes.geo(index_array[j], 1), 0.0);
			  subgridVertex->GetPointIds()->SetId(0, j);
			  subgridVertices->InsertNextCell(subgridVertex);
			  ionDensityArray->SetComponent(j, 0, edge.fluid.ni(k).value(n).scalar(j)); 
			}
		      
		      // To add new array Electron Density (Cells) as unstructuredGrid
		      subgridPointsUnstructuredGrid->SetPoints(points);
		      subgridPointsUnstructuredGrid->SetCells(VTK_VERTEX, subgridVertices);
		      subgridPointsUnstructuredGrid->GetCellData()->AddArray(ionDensityArray);
		    }
		}
	    }
	  
	  // Getting vertex colored by reading scalars from ion Temperature subgrids (nodes) 
	  for(int k = 0; k < num_ti_species; k++)
	    {
	      vtkSmartPointer<vtkDoubleArray> ionTemperatureArray = fCreateNewDoubleArray(size, "Ion Temperature");
	      int ti_subgrid_num = edge.fluid.ti(k).value.extent(0);
	      for(int n = 0; n < ti_subgrid_num; n++)
		{
		  int ti_subgrid_ind = edge.fluid.ti(k).value(n).subgrid; 
		  if(i+1 == edge.fluid.ti(k).value(n).subgrid) // +1 because in GGD index starts with 1 and not with 0 as in C++
		    {
		      vtkSmartPointer<vtkCellArray> subgridVertices = vtkSmartPointer<vtkCellArray>::New();
		      vtkSmartPointer<vtkVertex> subgridVertex = vtkSmartPointer<vtkVertex>::New();
		      
		      ionTemperatureArray->SetNumberOfValues(size);
		      for(int j = 0; j < size; j++)
			{
			  points->InsertNextPoint(nodes.geo(index_array[j], 0), nodes.geo(index_array[j], 1), 0.0);
			  subgridVertex->GetPointIds()->SetId(0, j);
			  subgridVertices->InsertNextCell(subgridVertex);
			  ionTemperatureArray->SetComponent(j, 0, edge.fluid.ti(k).value(n).scalar(j)); 
			}
		      
		      // To add new array Electron Temperature (Cells) as unstructuredGrid
		      subgridPointsUnstructuredGrid->SetPoints(points);
		      subgridPointsUnstructuredGrid->SetCells(VTK_VERTEX, subgridVertices);
		      subgridPointsUnstructuredGrid->GetCellData()->AddArray(ionTemperatureArray);
		    }
		}
	    }
	  
	  // Getting vertex colored by reading scalars from electric potential subgrids (nodes): There is no data for electric potential nodes.
	  int num_blocks = mainMB->GetNumberOfBlocks();
	  mainMB->SetBlock(num_blocks, subgridPointsUnstructuredGrid);
	  mainMB->GetMetaData((unsigned int) num_blocks)->Set(vtkCompositeDataSet::NAME(), subgridName[i].c_str());
	  
	} 
      else if(subgrid_class == 1) //LINES
	{
	  vtkSmartPointer<vtkUnstructuredGrid> subgridLinesUnstructuredGrid =vtkSmartPointer<vtkUnstructuredGrid>::New();
	  vtkSmartPointer<vtkCellArray> subgridLinesArray = vtkSmartPointer<vtkCellArray>::New();
	  for(int j = 0; j < size; j++)
	    {
	      vtkSmartPointer<vtkLine> subgridLine = vtkSmartPointer<vtkLine>::New();
	      
	      int line_ind_0 = edges.boundary(index_array[j],0) -1;
	      int line_ind_1 = edges.boundary(index_array[j],1) -1;
	      
	      subgridLine ->GetPointIds()->SetId(0, line_ind_0);
	      subgridLine ->GetPointIds()->SetId(1, line_ind_1);
	      subgridLinesArray->InsertNextCell(subgridLine);
	    }
	  subgridLinesUnstructuredGrid->SetPoints(points);
	  subgridLinesUnstructuredGrid->SetCells(VTK_LINE, subgridLinesArray);
	  
	  //Getting all subgrids to main block
	  int num_blocks = mainMB->GetNumberOfBlocks();
	  mainMB->SetBlock(num_blocks, subgridLinesUnstructuredGrid);
	  mainMB->GetMetaData((unsigned int) num_blocks)->Set(vtkCompositeDataSet::NAME(), subgridName[i].c_str());
	}
      else if(subgrid_class == 2) //CELLS
	{
	  for(int j = 0; j < size; j++)
	    {
	      subgridQuad->GetPointIds()->SetId(0,all_cells[index_array[j]][0]);
	      subgridQuad->GetPointIds()->SetId(1,all_cells[index_array[j]][1]);
	      subgridQuad->GetPointIds()->SetId(2,all_cells[index_array[j]][2]);
	      subgridQuad->GetPointIds()->SetId(3,all_cells[index_array[j]][3]);
	      subgridCellArray->InsertNextCell(subgridQuad);
	      
	      //ELECTRON DENSITY and ELECTRON TEMPERATURE
	      electronDensityArray->SetComponent(j, 0, edge.fluid.ne.value(0).scalar(index_array[j]));
	      electronTemperatureArray->SetComponent(j, 0, edge.fluid.te.value(0).scalar(index_array[j]));
	      electricPotentialArray->SetComponent(j, 0, edge.fluid.po.value(0).scalar(index_array[j]));
	    }
	  vtkSmartPointer<vtkUnstructuredGrid> subgridCellsUnstructuredGrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
	  
	  subgridCellsUnstructuredGrid->SetPoints(points);
	  subgridCellsUnstructuredGrid->SetCells(VTK_QUAD, subgridCellArray);
	  
	  //Setting Electron Density and Electron Temperature to UnstructuredGrid
	  subgridCellsUnstructuredGrid->GetCellData()->AddArray(electronTemperatureArray);
	  subgridCellsUnstructuredGrid->GetCellData()->AddArray(electronDensityArray);
	  subgridCellsUnstructuredGrid->GetCellData()->AddArray(electricPotentialArray);
	  
	  //ION DENSITY 
	  for(int k = 0; k < num_ni_species; k++)
	    {
	      std::string ion_charge = edge.species(k).label;	
	      stringstream ni_species_num2str;
	      ni_species_num2str << k+1;
	      string ni_species_num_str = ni_species_num2str.str();
	      std::string ni_array_string;
	      if (k < 9){
		ni_array_string = "Ion Density 0" + ni_species_num_str + ion_charge;
	      } else {
		ni_array_string = "Ion Density " + ni_species_num_str + ion_charge;
	      }
	      vtkSmartPointer<vtkDoubleArray> ionDensityArray = fCreateNewDoubleArray(size, ni_array_string);
	      for(int j =0; j < size; j++)
		{
		  ionDensityArray->SetComponent(j, 0, edge.fluid.ni(k).value(0).scalar(index_array[j]));
		}
	      subgridCellsUnstructuredGrid->GetCellData()->AddArray(ionDensityArray);
	    }
	  
	  //ION TEMPERATURE 
	  for(int k = 0; k < num_ti_species; k++)
	    {
	      vtkSmartPointer<vtkDoubleArray> ionTemperatureArray = fCreateNewDoubleArray(size, "Ion Temperature");
	      for(int j =0; j < size; j++)
		{
		  ionTemperatureArray->SetComponent(j, 0, edge.fluid.ti(k).value(0).scalar(index_array[j]));
		}
	      subgridCellsUnstructuredGrid->GetCellData()->AddArray(ionTemperatureArray);
	    }
	  
	  //Getting all subgrids to main multiblockdataset block
	  int num_blocks = mainMB->GetNumberOfBlocks();
	  mainMB->SetBlock(num_blocks, subgridCellsUnstructuredGrid);
	  mainMB->GetMetaData((unsigned int) num_blocks)->Set(vtkCompositeDataSet::NAME(), subgridName[i].c_str());
	}
    } 
  output->ShallowCopy(mainMB);
  itm.close();
#endif // IMAS_IDS
  return 1;
}

void  ReadUALEdge::PrintSelf(ostream& os, vtkIndent indent)
{
  this->Superclass::PrintSelf(os, indent);
}

