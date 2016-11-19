cmake_minimum_required(VERSION 2.8)
 
PROJECT(VtkFromB2_5)
 
find_package(VTK REQUIRED)
include(${VTK_USE_FILE})

set(HEADERS FileReader.h VtkBuilder.h)
set(SOURCES FileReader.cpp VtkBuilder.cpp main.cpp)

add_executable(VtkFromB2_5 ${SOURCES})
 
if(VTK_LIBRARIES)
  target_link_libraries(VtkFromB2_5 ${VTK_LIBRARIES})
else()
  target_link_libraries(VtkFromB2_5 vtkHybrid vtkWidgets)
endif()
