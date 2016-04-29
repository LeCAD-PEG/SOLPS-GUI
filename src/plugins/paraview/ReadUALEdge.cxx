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

#define IMAS

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
  this->Tokamak = NULL;
  this->Version = NULL;
  this->SetNumberOfInputPorts(0);
  this->SetNumberOfOutputPorts(1);
  this->trial=vtkSmartPointer<vtkDataArraySelection>::New();
  this->DebugOff();
  this->trial->DisableAllArrays();
  this->fields=vtkSmartPointer<vtkDataArraySelection>::New();
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
#ifdef IMAS
  std::clog << "TEST" << std::endl;
  using namespace IdsNs;
  IDS db(this->Shot,this->Run,this->Shot,this->RefRun);
  //IDS db(16151,1000,16151,1000);
  //db.openEnv(this->User, this->Tokamak, this->Version);
  db.open();
  std::clog << "User: "<<this->User<<" Tokamak:"<<this->Tokamak<< std::endl;
  //IDS::edge_profiles edge;
  db._edge_profiles.get();
  //edge.get();
  
  #if 0
  // Example: Printing IMAS/IDS database data to .txt file
  //db._edge_profiles.getSlice(time, INTERPOLATION);
  db._edge_profiles.getSlice(1,1);
  ofstream myfile;
  myfile.open ("log_edge_profiles.txt");
  myfile << db._edge_profiles;
  myfile.close();
  //std::cout << db._edge_profiles << std::endl;
  #endif
  
  int num_slices = db._edge_profiles.ggd.extent(0);
  std::clog << "slices:" << num_slices << std::endl;
  if (num_slices == 0)
    return 0;
  
  class IDS::edge_profiles & edge = db._edge_profiles;
  class IDS::edge_profiles::ggd & ggd = edge.ggd(0);
  class IDS::edge_profiles::ggd::grid & grid = ggd.grid;
  class IDS::edge_profiles::ggd::grid::space & space = grid.space(0);
  class IDS::edge_profiles::ggd::grid::space::objects_per_dimension & objects_per_dimension = space.objects_per_dimension(0);
  class IDS::edge_profiles::ggd::grid::space::objects_per_dimension::object & nodes = objects_per_dimension.object(0);
  class IDS::edge_profiles::ggd::grid::space::objects_per_dimension::object & edges = objects_per_dimension.object(1);
  class IDS::edge_profiles::ggd::grid::space::objects_per_dimension::object & cells = objects_per_dimension.object(2);
  
  int num_nodes = nodes.nodes.extent(0);
  int num_geo = nodes.geometry.extent(0);
  int num_edges = edges.boundary(0).neighbours.extent(0)/2;
  int num_cells = cells.boundary(0).neighbours.extent(0)/4;
  
  std::clog << "num_nodes: " << num_nodes << std::endl;
  std::clog << "num_geo: " << num_geo << std::endl;
  std::clog << "num_edges: " << num_edges << std::endl;
  std::clog << "num_cells: " << num_cells << std::endl;
  
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  
  double all_cells[num_cells][4]; 
  for (int i = 0; i < num_cells; ++i) {
  int node_idx[4]; // Resulting node indices for a cell
  int free_edge[3]; // list of edges that are free to search for node
  int last_idx; // last node index 
  int edge_idx = cells.boundary(0).neighbours(i*4) - 1;
  free_edge[0] = cells.boundary(0).neighbours((i*4)+1) - 1;
  free_edge[1] = cells.boundary(0).neighbours((i*4)+2) - 1;
  free_edge[2] = cells.boundary(0).neighbours((i*4)+3) - 1;
  
  node_idx[0] = edges.boundary(0).neighbours(edge_idx*2) - 1;
  node_idx[last_idx=1] = edges.boundary(0).neighbours((edge_idx*2)+1) - 1;
    for(int loop_count = 0; last_idx < 3 && loop_count < 4; ++loop_count){
      for(int j = 0; j < 3 ; ++j) { // free_edge
	edge_idx = free_edge[j];
	if(edge_idx < 0)
	  continue;
	int node1 =  edges.boundary(0).neighbours(edge_idx*2) - 1;
	int node2 =  edges.boundary(0).neighbours((edge_idx*2)+1) - 1;

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
  
  for(int i=0; i < num_nodes; i++)
  {
   points->InsertNextPoint(nodes.geometry(i*2), nodes.geometry((i*2)+1), 0.0); 
  }
  
  vtkSmartPointer<vtkQuad> Quad =  vtkSmartPointer<vtkQuad>::New();
  vtkSmartPointer<vtkCellArray> cellArray = vtkSmartPointer<vtkCellArray>::New();
  
  //ELECTRON DENSITY and ELECTRON TEMPERATURE creating array + cells assembly
  vtkSmartPointer<vtkDoubleArray> electronDensityArray = vtkSmartPointer<vtkDoubleArray>::New();
  electronDensityArray->SetNumberOfComponents(1);
  electronDensityArray->SetNumberOfTuples(num_cells);
  electronDensityArray->SetName("Electron density"); 
  
  vtkSmartPointer<vtkDoubleArray> electronTemperatureArray = vtkSmartPointer<vtkDoubleArray>::New();
  electronTemperatureArray->SetNumberOfComponents(1);
  electronTemperatureArray->SetNumberOfTuples(num_cells);
  electronTemperatureArray->SetName("Electron temperature"); 
  
  for(int i = 0; i < num_cells; i++)
  {
    Quad->GetPointIds()->SetId(0,all_cells[i][0]);
    Quad->GetPointIds()->SetId(1,all_cells[i][1]);
    Quad->GetPointIds()->SetId(2,all_cells[i][2]);
    Quad->GetPointIds()->SetId(3,all_cells[i][3]);
    cellArray->InsertNextCell(Quad);
    
    electronDensityArray->SetComponent(i, 0, ggd.electrons.density(0).values(i)); 
    electronTemperatureArray->SetComponent(i, 0, ggd.electrons.temperature(0).values(i));
  }
  
  vtkSmartPointer<vtkUnstructuredGrid> ug = vtkSmartPointer<vtkUnstructuredGrid>::New();
  
  ug->SetPoints(points);
  ug->SetCells(VTK_QUAD, cellArray);
  
  ug->GetCellData()->AddArray(electronDensityArray);
  ug->GetCellData()->AddArray(electronTemperatureArray);
  
  //ION DENSITY and ION TEMPERATURE creating array and allocatin scalars
  int num_ion_species = ggd.ion.extent(0);
  std::clog << "num_ion_species: " << num_ion_species << std::endl;
  int num_ni_species = num_ion_species;
  int num_ti_species = 1; //In database there are currently 2 ion density arrays but only one ion temperature array.
  int size = num_cells; //Later, when the code will work with subgrids, the "size" variable will hold the size (number of cells) of the subgrid.
  for(int k = 0; k < num_ni_species; k++)
  {
    
    vtkSmartPointer<vtkDoubleArray> ionDensityArray = vtkSmartPointer<vtkDoubleArray>::New();
    ionDensityArray->SetNumberOfComponents(1);
    ionDensityArray->SetNumberOfTuples(size);
    std::string set_name = "Ion Density ";
    set_name = set_name + SSTR(k+1);
    ionDensityArray->SetName(set_name.c_str());
    for(int j = 0; j < size; j++)
    {
      ionDensityArray->SetComponent(j, 0, ggd.ion(k).density(0).values(j)); // .density(i) -> i stands for subset. 
									    //Subgrid "0" is the main grid / the main subset. i = 0;
    }
    ug->GetCellData()->AddArray(ionDensityArray);
  }
  for(int k = 0; k < num_ti_species; k++)
  {
    
    vtkSmartPointer<vtkDoubleArray> ionTemperatureArray = vtkSmartPointer<vtkDoubleArray>::New();
    ionTemperatureArray->SetNumberOfComponents(1);
    ionTemperatureArray->SetNumberOfTuples(size);
    std::string set_name = "Ion Temperature ";
    set_name = set_name + SSTR(k+1);
    ionTemperatureArray->SetName(set_name.c_str());
    for(int j = 0; j < size; j++)
    {
      ionTemperatureArray->SetComponent(j, 0, ggd.ion(k).temperature(0).values(j)); 
    }
    ug->GetCellData()->AddArray(ionTemperatureArray);
    
  }

  vtkSmartPointer<vtkMultiBlockDataSet> MainMB = vtkSmartPointer<vtkMultiBlockDataSet>::New();
  MainMB->SetBlock(0, ug);
  MainMB->GetMetaData((unsigned int) 0)->Set(vtkCompositeDataSet::NAME(), "Cells");
  output->ShallowCopy(MainMB);
  
  db.close();
  
  
#else
  ItmNs::Itm itm(this->Shot,this->Run,this->Shot,this->RefRun);

  if (!this->Version)
    this->Version = strdup("4.10a");
  itm.openEnv(this->User, this->Tokamak, this->Version); //Open the database
  std::clog << "User: "<<this->User<<" Tokamak:"<<this->Tokamak<< std::endl;
  
  itm._edgeArray.get();
  
  int num_slices = itm._edgeArray.extent(0);
  if (num_slices == 0)
    return 0;

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
  vtkSmartPointer<vtkQuad> subgridQuad2 =  vtkSmartPointer<vtkQuad>::New();
  
  vtkSmartPointer<vtkCellArray> cellArray = vtkSmartPointer<vtkCellArray>::New();
  vtkSmartPointer<vtkQuad> quad =  vtkSmartPointer<vtkQuad>::New();

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
 
  // Reading Scalars
  class ItmNs::Itm::edge::fluid::ne & ne = edge.fluid.ne;
  class ItmNs::Itm::edge::fluid::ne::value & ne_value = ne.value(0);
  class ItmNs::Itm::edge::fluid::te & te = edge.fluid.te;
  class ItmNs::Itm::edge::fluid::te::value & te_value = te.value(0);
  
  // Checking contents under po (electric potential)
  class ItmNs::Itm::edge::fluid::po & po = edge.fluid.po;
  std::clog << std::left << setw(42) << "po.value(0).extent(0): __________________" << edge.fluid.po.value.extent(0) << std::endl;
  std::clog << std::left << setw(42) << "po.value(0).scalar.extent(0): __________" << edge.fluid.po.value(0).scalar.extent(0) << std::endl;
  
  double electronDensityScalars[num_cells];
  double electronTemperatureScalars[num_cells];
  double electricPotentialScalars[num_cells];
  
  std::clog << "Getting scalars" << std::endl;
  
  // Getting Electron Density and Electron Temperature CELL scalars
  for (int j = 0; j < num_cells; ++j)
    {
      electronDensityScalars[j] = ne_value.scalar(j);
      electronTemperatureScalars[j] = te_value.scalar(j);
      electricPotentialScalars[j] = po.value(0).scalar(j);
    }
  std::clog << "ne_value.subgrid: " << ne_value.subgrid << std::endl;
  
  // Getting for Ion Density CELL Scalars
  int num_ni_species = edge.fluid.ni.extent(0);
  std::clog << "edge.fluid.ni.extent(0): " << num_ni_species << std::endl; //
  double ionDensityScalars[num_cells][num_ni_species]; 
  
  std::clog << "Number of Ion Density species:" << num_ni_species << std::endl;
  for (int k = 0 ; k < num_ni_species ; ++k)
  {
    int num_ni_values = edge.fluid.ni(k).value.extent(0); // =/= num_cells
    class ItmNs::Itm::edge::fluid::ni::value & ni_value = edge.fluid.ni(k).value(0);
    for (int j = 0; j < num_cells; ++j)
    {
      ionDensityScalars[j][k] = ni_value.scalar(j);
    }	
  }
  
  // Getting Ion Temperature CELL Scalars
  int num_ti_species = edge.fluid.ti.extent(0);
  double ionTemperatureScalars[num_cells][num_ti_species];
  std::clog << "Number of Ion Temperature species:" << num_ti_species << std::endl;
  for (int k = 0 ; k < num_ti_species ; ++k)
  {
    int num_ti_values = edge.fluid.ti(k).value(0).scalar.extent(0);
    class ItmNs::Itm::edge::fluid::ti::value & ti_value = edge.fluid.ti(k).value(0);
    for (int j = 0; j < num_cells; ++j)
    {
      ionTemperatureScalars[j][k] = ti_value.scalar(j);
    }	
  }
  
  vtkSmartPointer<vtkMultiBlockDataSet> mainMB = vtkSmartPointer<vtkMultiBlockDataSet>::New();
  
  int num_subgrids = grid.subgrids.extent(0);
  std::string subgridName[num_subgrids];
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
    }else{
      for(int j = 0; j < ind_num; j++)
      {
	jIndex = grid.subgrids(i).list(0).ind(j,0) - 1;
	index_array[j] = jIndex;
      }
    } 
    
    int size = (sizeof(index_array)/sizeof(*index_array));
    
    vtkSmartPointer<vtkCellArray> subgridCellArray = vtkSmartPointer<vtkCellArray>::New();
    
    //ELECTRON TEMPERATURE creating array
    vtkSmartPointer<vtkDoubleArray> electronTemperatureArray = vtkSmartPointer<vtkDoubleArray>::New();
    electronTemperatureArray->SetNumberOfComponents(1);
    electronTemperatureArray->SetNumberOfTuples(size);
    electronTemperatureArray->SetName("Electron Temperature"); 
    
    //ELECTRON DENSITY creating array
    vtkSmartPointer<vtkDoubleArray> electronDensityArray = vtkSmartPointer<vtkDoubleArray>::New();
    electronDensityArray->SetNumberOfComponents(1);
    electronDensityArray->SetNumberOfTuples(size);
    electronDensityArray->SetName("Electron Density"); 
    
    //ELECTRIC POTENTIAL creating array
    vtkSmartPointer<vtkDoubleArray> electricPotentialArray = vtkSmartPointer<vtkDoubleArray>::New();
    electricPotentialArray->SetNumberOfComponents(1);
    electricPotentialArray->SetNumberOfTuples(size);
    electricPotentialArray->SetName("Electric Potential"); 
    
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
	vtkSmartPointer<vtkDoubleArray> ionDensityArray = vtkSmartPointer<vtkDoubleArray>::New();
	ionDensityArray->SetNumberOfComponents(1);
	ionDensityArray->SetNumberOfTuples(size);
	std::string set_name = "Ion Density ";
	set_name = set_name + SSTR(k+1);
	ionDensityArray->SetName(set_name.c_str());
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
	vtkSmartPointer<vtkDoubleArray> ionTemperatureArray = vtkSmartPointer<vtkDoubleArray>::New();
	ionTemperatureArray->SetNumberOfComponents(1);
	ionTemperatureArray->SetNumberOfTuples(size);
	std::string set_name = "Ion Temperature ";
	set_name = set_name + SSTR(k+1);
	ionTemperatureArray->SetName(set_name.c_str());
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
      
      
    }else if(subgrid_class == 1) //LINES
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
	electronDensityArray->SetComponent(j, 0, electronDensityScalars[index_array[j]]);
	electronTemperatureArray->SetComponent(j, 0, electronTemperatureScalars[index_array[j]]);
	electricPotentialArray->SetComponent(j, 0, electricPotentialScalars[index_array[j]]);
      }
      vtkSmartPointer<vtkUnstructuredGrid> ug = vtkSmartPointer<vtkUnstructuredGrid>::New();
      
      ug->SetPoints(points);
      ug->SetCells(VTK_QUAD, subgridCellArray);
      
      //Setting Electron Density and Electron Temperature to UnstructuredGrid
      ug->GetCellData()->AddArray(electronTemperatureArray);
      ug->GetCellData()->AddArray(electronDensityArray);
      ug->GetCellData()->AddArray(electricPotentialArray);
      
      #if 1
      //ION DENSITY 
      for(int k = 0; k < num_ni_species; k++)
	{
	  vtkSmartPointer<vtkDoubleArray> ionDensityArray = vtkSmartPointer<vtkDoubleArray>::New();
	  ionDensityArray->SetNumberOfComponents(1);
	  ionDensityArray->SetNumberOfTuples(size);
	  std::string set_name = "Ion Density ";
	  set_name = set_name + SSTR(k+1);
	  ionDensityArray->SetName(set_name.c_str());
	  for(int j =0; j < size; j++)
	  {
	    ionDensityArray->SetComponent(j, 0, ionDensityScalars[index_array[j]][k]);
	  }
	  ug->GetCellData()->AddArray(ionDensityArray);
	}
      #endif
      
      #if 1
      //ION TEMPERATURE 
      for(int k = 0; k < num_ti_species; k++)
	{
	  vtkSmartPointer<vtkDoubleArray> ionTemperatureArray = vtkSmartPointer<vtkDoubleArray>::New();
	  ionTemperatureArray->SetNumberOfComponents(1);
	  ionTemperatureArray->SetNumberOfTuples(size);
	  std::string set_name = "Ion Temperature ";
	  set_name = set_name + SSTR(k+1);
	  ionTemperatureArray->SetName(set_name.c_str());
	  
	  for(int j =0; j < size; j++)
	  {
	    ionTemperatureArray->SetComponent(j, 0, ionTemperatureScalars[index_array[j]][k]);
	  }
	  ug->GetCellData()->AddArray(ionTemperatureArray);
	}
      #endif
      
      //Getting all subgrids to main multiblockdataset block
      int num_blocks = mainMB->GetNumberOfBlocks();
      mainMB->SetBlock(num_blocks, ug);
      mainMB->GetMetaData((unsigned int) num_blocks)->Set(vtkCompositeDataSet::NAME(), subgridName[i].c_str());
    }
  } 
  output->ShallowCopy(mainMB);
#endif // IMAS
  return 1;
}

void  ReadUALEdge::PrintSelf(ostream& os, vtkIndent indent)
{
  this->Superclass::PrintSelf(os,indent);
}

vtkDataArraySelection * ReadUALEdge::GetCPOListSelection(){
  vtkDebugMacro(<<"GetCPOListSelection");
  return this->trial.GetPointer();
}

int ReadUALEdge::GetCPOListArrayStatus(char *name){
  vtkDebugMacro(<<"GetCPOListArrayStatus");
  return this->trial->GetArraySetting(name);
}

void ReadUALEdge::SetCPOListArrayStatus(const char * name, int status){
  vtkDebugMacro(<<"SetCPOListArrayStatus");
  if (status){
    this->trial->EnableArray(name);
  }
  else{
    this->trial->DisableArray(name);
  }
}

int ReadUALEdge::GetNumberOfCPOListArrays(){
  vtkDebugMacro(<<"GetNumberOfCPOListArrays");
  return this->trial->GetNumberOfArrays();
}

const char * ReadUALEdge::GetCPOListArrayName(int index){
  vtkDebugMacro(<<"GetCPOListArrayName");
  return this->trial->GetArrayName(index);
}

vtkDataArraySelection * ReadUALEdge::GetFieldListSelection(){
  vtkDebugMacro(<<"GetFieldListSelection");
  return this->fields.GetPointer();
}


int ReadUALEdge::GetFieldListArrayStatus(char *name){
  vtkDebugMacro(<<"GetFieldListArrayStatus");
  return this->fields->GetArraySetting(name);
}

void ReadUALEdge::SetFieldListArrayStatus(const char * name, int status){
  vtkDebugMacro(<<"SetFieldListArrayStatus");
	if (status){
      this->fields->EnableArray(name);
	}
	else{
		this->fields->DisableArray(name);
	}
}

int ReadUALEdge::GetNumberOfFieldListArrays(){
  vtkDebugMacro(<<"GetNumberOfFieldListArrays");
  return this->fields->GetNumberOfArrays();
}

const char * ReadUALEdge::GetFieldListArrayName(int index){
  vtkDebugMacro(<<"GetFieldListArrayName");
  return this->fields->GetArrayName(index);
}
