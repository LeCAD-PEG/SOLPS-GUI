#include <iostream>
#include <sstream>
#include <cstdlib>
#include <fstream>
#include "FileReader.h"

FileReader::FileReader(int argc, char *argv[]){
	if (argv == NULL){
		std::cout << "Enter path(s) to file.\n";
	}else{
		for (int i = 1; i < argc; ++i){
			fileLocation.push_back(argv[i]);
		}
	}
}
void FileReader::printNames(){
	std::cout << "Names are: \n";
	for (int i = 0; i < names.size(); ++i){
		std::cout << names[i] << "\n";
	}
	std::cout << "\n";
}
void FileReader::printTypes(){
	std::cout << "Types are: \n";
	for (int i = 0; i < types.size(); ++i){
		std::cout << types[i] << "\n";
	}
	std::cout << "\n";
}
void FileReader::printSizes(){
	std::cout << "Sizes are: \n";
	for (int i = 0; i < sizes.size(); ++i){
		std::cout << sizes[i] << "\n";
	}
	std::cout << "\n";
}		
void FileReader::appendDataToVector(){
	/*
	 *Take "std::vector< std::vector<double> > allData" and 
	 *save all data of each variable into a vector.
	 */
	std::string line;
	allData.resize(names.size());
	int cfIndex = 0;
	for (int fileIndex = 0; fileIndex < fileLocation.size(); ++fileIndex){
		std::ifstream ist(fileLocation[fileIndex].c_str());
		if (!ist){
			std::cerr << "Can not open input file " << fileLocation[fileIndex];
		}
		int lineNumber = 1;
		while(std::getline(ist,line)){
			//Save data from file when in line with data
			if (cfIndex == linesWithCf.size()-1 && lineNumber >= linesWithCf[cfIndex]+1){
				//We are reading data from last "cf*" in file
				extractDoubleFromString(line,allData[cfIndex]);
			}
			else{
				if (lineNumber >= linesWithCf[cfIndex]+1 && lineNumber < linesWithCf[cfIndex+1] ){
					extractDoubleFromString(line,allData[cfIndex]);
				}
			}
			if (lineNumber == linesWithCf[cfIndex+1]-1) {
				cfIndex++;}
			lineNumber++;
		}
	}
}
void FileReader::extractDoubleFromString(std::string line, std::vector<double>& vec){
	/*
	 *Extracts doubles from a stringstream - given a string of numbers
	 *it extracts out vector of numbers.
	 */
	std::stringstream iss(line);
	std::vector<std::string> allwords;
	std::string word;
	while(iss >> word){
		allwords.push_back(word);
	}
	for (int i = 0; i < allwords.size(); ++i){
		double tempNumber = atof(allwords[i].c_str());
		vec.push_back(tempNumber);
	}
}
void FileReader::findCf(){
	/*
	 *Finds lines with "*cf:" and saves those line numbers into a std::vector.
	 */
	for (int fileIndex = 0; fileIndex < fileLocation.size(); ++fileIndex){
		std::ifstream ist(fileLocation[fileIndex].c_str());
		if (!ist){
			std::cerr << "Can not open input file " << fileLocation[fileIndex];
		}
		std::string firstWordInLine;
		int lineNumber = 1;
		while(ist >> firstWordInLine){
			if (firstWordInLine.compare("*cf:") == 0){
				linesWithCf.push_back(lineNumber);
			}
			ist.ignore(200, '\n');
			lineNumber++;
		}
	}
}
void FileReader::initializeArrays(){
	/*
	 *loop through every line of a file and process every line that contains "*cf:".
	 *Save type, size and name of a variable.
	 */
	int chIndex = 0;
	for (int fileIndex = 0; fileIndex < fileLocation.size(); ++fileIndex){
		std::ifstream ist(fileLocation[fileIndex].c_str());
		if (!ist){
			std::cerr << "Can not open input file " << fileLocation[fileIndex];
		}
		std::string line;
		int lineNumber = 1;
		while(std::getline(ist,line)){
			if (lineNumber == linesWithCf[chIndex]){
				std::stringstream iss(line);
				std::vector<std::string> allwords;
				std::string word, word2, word3, word4;
				while(iss >> word >> word2 >> word3 >> word4){
					types.push_back(word2);
					sizes.push_back(atoi(word3.c_str()));
					names.push_back(word4);
				}
				chIndex++;
			}
			lineNumber++;
		}
	}
}