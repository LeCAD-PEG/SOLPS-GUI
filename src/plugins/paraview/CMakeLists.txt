cmake_minimum_required(VERSION 2.8)
find_package(PkgConfig REQUIRED)

SET(GCC_COVERAGE_COMPILE_FLAGS "-fPIC -D_REENTRANT=true")

SET( CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}" )
SET( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}" )
SET( CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} ${GCC_COVERAGE_LINK_FLAGS}" )

site_name(site)

message("Building for ${site}")

if ( site MATCHES ".*iter.org" )
   pkg_search_module(BLITZ REQUIRED blitz)   
   pkg_search_module(IMASCPP REQUIRED imas-cpp)
   pkg_search_module(IMASLL REQUIRED imas-lowlevel)
   
   link_directories(${IMASCPP_LIBRARY_DIRS})
   link_directories(${IMASLL_LIBRARY_DIRS})
   link_directories($ENV{MDSPLUS_DIR}/lib)

else()

   pkg_search_module(BLITZ REQUIRED blitz)   
#   pkg_search_module(IMASCPP REQUIRED imas-cpp)
#   pkg_search_module(IMASLL REQUIRED imas-lowlevel)
   
#   link_directories(${IMASCPP_LIBRARY_DIRS})
#   link_directories(${IMASLL_LIBRARY_DIRS})
   link_directories($ENV{MDSPLUS_DIR}/lib)

#SET(IMASCPP_INCLUDE_DIRS /u/dkaljun/imas/core/imas/develop/3/ual/develop/include)
#SET(IMASLL_INCLUDE_DIRS /u/dkaljun/imas/core/imas/develop/3/ual/develop/include)

SET(IMASCPP_INCLUDE_DIRS /afs/ipp/itm/switm/imasv1/core/imas/master/3/ual/develop/include)
SET(IMASLL_INCLUDE_DIRS /afs/ipp/itm/switm/imasv1/core/imas/master/3/ual/develop/include)



#include_directories(/afs/ipp/itm/switm/ual/4.10a.4_R2.1.0/include)
include_directories(/afs/ipp/itm/switm/blitz/0.10/include)
#include_directories(/u/dkaljun/imas/core/imas/develop/3/ual/develop/include)

#link_directories(/afs/ipp/itm/switm/ual/4.10a.4_R2.1.0/lib)
#link_directories(/afs/ipp/itm/switm/mdsplus/5.2_itm_v1/lib64)
#link_directories(/afs/ipp/itm/switm/mdsplus/5.2_itm_v1/lib)
link_directories(/u/dkaljun/imas/core/imas/develop/3/ual/develop/lib)
link_directories(${BLITZ_LIBRARY_DIRS})
#link_directories(/afs/ipp/itm/switm/lib/hdf5/1.8.10)
#
endif()


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
target_include_directories(ReadUALEdge PUBLIC ${IMASCPP_INCLUDE_DIRS})
target_include_directories(ReadUALEdge PUBLIC ${IMASLL_INCLUDE_DIRS})
target_include_directories(ReadUALEdge PUBLIC ${BLITZ_INCLUDE_DIRS})
#target_include_directories(ReadUALEdge PUBLIC ${MDSPLUS_INCLUDE_DIRS})
target_link_libraries(ReadUALEdge  imas-cpp imas TreeShr TdiShr MdsShr MdsIpShr XTreeShr blitz) 

#   target_link_libraries(ReadUALEdge ${IMASCPP_LIBRARIES} ${IMASLL_LIBRARIES})

endif()




