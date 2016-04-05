#include <iostream>
#include "FileReader.h"
#include "VtkBuilder.h"

int main(int argc, char *argv[]){
	if (argc < 2){
		std::cout << "Pass paths to files with data as argument!\n";
		return 1;
	}
	FileReader reader(argc, argv);
	reader.findCf();
	reader.initializeArrays();
	reader.appendDataToVector();
	VtkBuilder mesh;
	int indexCrx = 0;
	int indexCry = 0;
	for (int i = 0; i < reader.names.size(); ++i)
	{
		if (reader.names[i] == "crx") indexCrx = i;
		if (reader.names[i] == "cry") indexCry = i;
	}
	mesh.createPointsAndGrid(reader.allData[indexCrx], reader.allData[indexCry], reader);
	for (int i = 0; i < reader.allData.size(); ++i)	{
		mesh.assignDataToCells(reader.allData[i],reader.names[i]);
	}
	mesh.writeToFile("ParaviewFile.vtp");
}
/*
TO-DO:
	- class FileReader:
		- all data is saved under type double - change that (you have to handle char, int, double)
	- class VtkBuilder:
		- repair hard-coded array sizes
		- figure out what to do with data that can not be processed automatically
*/