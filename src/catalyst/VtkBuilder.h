#ifndef VTKBUILDER_H_INCLUDED
#define VTKBUILDER_H_INCLUDED

#include <vector>
#include <vtkPolyData.h>
#include "FileReader.h"

class VtkBuilder{
public:
	void createPointsAndGrid(std::vector<double>& point_x, std::vector<double>& point_y, FileReader &obj);
	void assignDataToPoints(std::vector<double>& pointData, std::string var_name);
	void assignDataToCells(std::vector<double>& cellData, std::string var_name);
	void writeToFile(const char fileName[]);
private:
	vtkPolyData* grid = NULL;
};

#endif