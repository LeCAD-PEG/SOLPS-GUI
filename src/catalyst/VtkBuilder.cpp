#include <vtkSmartPointer.h>
#include <vtkPoints.h>
#include <vtkVersion.h>
#include <vtkCellArray.h>
#include <vtkXMLPolyDataWriter.h>
#include <vtkDataArray.h>
#include <vtkDoubleArray.h>
#include <vtkPointData.h>
#include <vtkCellData.h>
#include "VtkBuilder.h"

void VtkBuilder::createPointsAndGrid(std::vector<double>& point_x, std::vector<double>& point_y, FileReader &obj){
	/*
	 *Create vtkPoints and vtkPolydata with point and grid data from files with geometry.
	 */
	if (grid == NULL){
		grid = vtkPolyData::New();
	}
	vtkPoints* points = vtkPoints::New();
	points->SetNumberOfPoints(point_x.size());
	for (vtkIdType id = 0; id < point_x.size(); ++id){
		points->SetPoint(id, point_x[id], point_y[id], 0);
	}
	//create 3D matrix that represents points in each cell
	const int numCellsY = obj.allData[0][1] + 2;
	const int numCellsX = obj.allData[0][0] + 2;
	const int numPtsInCell = 4;
	int gridOfPoints[38][98][4]; //...array can not be allocated at runtime - fix that...
	int pointId = 0;
	for (int j = 0; j < numCellsY; ++j){
		for (int i = 0; i < numCellsX; ++i)
		{
			gridOfPoints[j][i][0] = pointId;
			gridOfPoints[j][i][1] = pointId + numCellsY*numCellsX;
			gridOfPoints[j][i][2] = pointId + 3*numCellsY*numCellsX;
			gridOfPoints[j][i][3] = pointId + 2*numCellsY*numCellsX;
			pointId++;
		}
	}
	grid->SetPoints(points);
	points->Delete();
	//Insert cells in vtkPolyData grid
	grid->Allocate(numCellsY*numCellsX);
	for (int j = 0; j < numCellsY; ++j){
		for (int i = 0; i < numCellsX; ++i){
			vtkIdType ids[numPtsInCell];
			for (int k = 0; k < numPtsInCell; ++k){
				//ids[k] = rearrangedCells[j][i][k];
				ids[k] = gridOfPoints[j][i][k];
			}
			grid->InsertNextCell(9,numPtsInCell,ids);
		}
	}
}
void VtkBuilder::assignDataToPoints(std::vector<double>& pointData, std::string var_name){
	/*
	 *Assign Data to each point on the grid.
	 */
	if (grid == NULL){
		std::cerr << "You have to call vtkCreate::createPointsAndGrid first!\n";
	}
	vtkDoubleArray* pointDataDoubleArray = vtkDoubleArray::New();
	pointDataDoubleArray->SetNumberOfTuples(grid->GetNumberOfPoints()); // in this case number of tuples is equal to number of points
	pointDataDoubleArray->SetNumberOfComponents(1);
	pointDataDoubleArray->SetName(var_name.c_str());
	for (vtkIdType i = 0; i < grid->GetNumberOfPoints(); ++i){
		pointDataDoubleArray->SetValue(i, pointData[i]);
	}
	grid->GetPointData()->AddArray(pointDataDoubleArray);
	pointDataDoubleArray->Delete();
}
void VtkBuilder::assignDataToCells(std::vector<double>& cellData, std::string var_name){
	/*
	 *Assign Data to each cell on the grid. Based on the multiples of number of cells
	 *determines how to put data in a cell.
	 */
	if (grid == NULL){
		std::cerr << "You have to call vtkCreate::createPointsAndGrid first!\n";
	}
	int numCells = grid->GetNumberOfCells();
	if (cellData.size() == numCells){
		//1 component per cell (scalar)
		vtkDoubleArray* cellDataDoubleArray = vtkDoubleArray::New();
		cellDataDoubleArray->SetName(var_name.c_str());
		cellDataDoubleArray->SetNumberOfTuples(numCells);
		cellDataDoubleArray->SetNumberOfComponents(1);
		for (vtkIdType i = 0; i < numCells; ++i){	
			cellDataDoubleArray->InsertTuple1(i,cellData[i]);
		}
		grid->GetCellData()->AddArray(cellDataDoubleArray);
		cellDataDoubleArray->Delete();	
	} else if(cellData.size() == 2*numCells) {
		//2 components per cell (x,y)
		vtkDoubleArray* cellDataDoubleArray = vtkDoubleArray::New();
		cellDataDoubleArray->SetName(var_name.c_str());
		cellDataDoubleArray->SetNumberOfTuples(numCells);
		cellDataDoubleArray->SetNumberOfComponents(2);
		for (vtkIdType i = 0; i < numCells; ++i){	
			cellDataDoubleArray->InsertTuple2(i,cellData[i], cellData[i+numCells]);
		}
		grid->GetCellData()->AddArray(cellDataDoubleArray);
		cellDataDoubleArray->Delete();			
	} else if(cellData.size() == 3*numCells) {
		//REGION!!!

		
	} else if(cellData.size() == 4*numCells) {
		//3 components (x,y,z) and magnitude -> ignore last component (magnitude),
		//because paraview calculates it on its own.
		vtkDoubleArray* cellDataDoubleArray = vtkDoubleArray::New();
		cellDataDoubleArray->SetName(var_name.c_str());
		cellDataDoubleArray->SetNumberOfTuples(numCells);
		cellDataDoubleArray->SetNumberOfComponents(3);
		for (vtkIdType i = 0; i < numCells; ++i){	
			cellDataDoubleArray->InsertTuple3(i,cellData[i], cellData[i+numCells], cellData[i+2*numCells]/*, cellData[i+3*numCells]*/);		
		}
		grid->GetCellData()->AddArray(cellDataDoubleArray);
		cellDataDoubleArray->Delete();	
	}
}
void VtkBuilder::writeToFile(const char fileName[]){
	/*
	 *Write vtkPolyData to .vtp file.
	 */
	vtkSmartPointer<vtkXMLPolyDataWriter> writer = vtkSmartPointer<vtkXMLPolyDataWriter>::New();
  	writer->SetFileName(fileName);
	#if VTK_MAJOR_VERSION <= 5
		writer->SetInput(grid);
	#else
  		writer->SetInputData(grid);
	#endif
  	writer->Write();
}