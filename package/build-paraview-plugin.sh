#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="ReadUALEdge-Plugin"
VERSION=${VERSION:-1.5.0}
MAJOR_VERSION=${VERSION%.*}

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi


_copyLocalDirectory "${BUILDROOT}/src/plugins/paraview"

CMAKE_FLAGS="-DCMAKE_BUILD_TYPE:STRING=Debug"
CMAKE_FLAGS="${CMAKE_FLAGS} -DParaView_DIR:PATH=${STAGING_DIR}/paraview/${PARAVIEW_VERSION}"

_cmake "${CMAKE_FLAGS}" "IMAS_VERSION_DIGIT=$(echo "$IMAS_VERSION" | sed "s/\.//g")"
_make "-j${MAKE_JOBS} VERBOSE=1"
_install
