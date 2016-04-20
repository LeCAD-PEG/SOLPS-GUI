cmake_minimum_required(VERSION 2.8)

SET(GCC_COVERAGE_COMPILE_FLAGS "-D_REENTRANT=true -lUALCPPInterface -lblitz -lUALLowLevel")
SET(GCC_COVERAGE_LINK_FLAGS    "-D_REENTRANT=true -lUALCPPInterface -lblitz -lUALLowLevel")

SET( CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}" )
SET( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}" )
SET( CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} ${GCC_COVERAGE_LINK_FLAGS}" )

include_directories(/afs/ipp/itm/switm/ual/4.10a.4_R2.1.0/include)
include_directories(/afs/ipp/itm/switm/blitz/0.10/include)


link_directories(/afs/ipp/itm/switm/ual/4.10a.4_R2.1.0/lib)
link_directories(/afs/ipp/itm/switm/blitz/0.10/lib)

FIND_PACKAGE(ParaView REQUIRED)
INCLUDE(${PARAVIEW_USE_FILE})

if (PARAVIEW_BUILD_QT_GUI)
  qt4_wrap_cpp(moc_srcs
    pqFieldListPropertyWidgetDecorator.h
    pqFieldPropertyWidgetDecorator.h
    pqMyPropertyWidgetDecorator.h)
   
  set (outifaces0)
  set (outsrcs0)
  add_paraview_property_widget_decorator(outifaces0 outsrcs0
    TYPE "field_list_decorator"
    CLASS_NAME pqFieldListPropertyWidgetDecorator)


  set (outifaces1)
  set (outsrcs1)
  add_paraview_property_widget_decorator(outifaces1 outsrcs1
    TYPE "field_decorator"
    CLASS_NAME pqFieldPropertyWidgetDecorator)


  set (outifaces2)
  set (outsrcs2)
  add_paraview_property_widget_decorator(outifaces2 outsrcs2
    TYPE "my_decorator"
    CLASS_NAME pqMyPropertyWidgetDecorator)

   #Now, create the plugin.
  add_paraview_plugin(ReadUALEdge "1.0"
                      SERVER_MANAGER_XML ReadUALEdge.xml
                      GUI_INTERFACES ${outifaces0} 
				     ${outifaces2} 
                                     ${outifaces1}
                      SERVER_MANAGER_SOURCES ReadUALEdge.cxx
                      SOURCES  ${outsrcs0}
                               ${outsrcs2}
                               ${outsrcs1}
                               ${moc_srcs}
			       pqFieldPropertyWidgetDecorator.cxx
                               pqMyPropertyWidgetDecorator.cxx
			       pqFieldListPropertyWidgetDecorator.cxx)
endif()




