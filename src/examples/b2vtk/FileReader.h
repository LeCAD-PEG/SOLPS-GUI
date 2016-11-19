#ifndef ARRAYS_H_INCLUDED
#define ARRAYS_H_INCLUDED

#include <string>
#include <vector>

class FileReader{
	friend class VtkBuilder;
public:
	std::vector<std::string> names;
	std::vector< std::vector<double> > allData;
	FileReader(int argc, char *argv[]);
	void findCf();
	void initializeArrays();	
	void appendDataToVector();
	void printNames();
	void printTypes();
	void printSizes();
private:
	std::vector<std::string> fileLocation;
	std::vector<int> linesWithCf;
	std::vector<std::string> types;
	std::vector<int> sizes;
	void extractDoubleFromString(std::string line, std::vector<double>& vec);
};

#endif