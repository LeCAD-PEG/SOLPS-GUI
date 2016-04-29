#!/bin/sh -x

BUILDROOT="${PWD}"
BUILD_DIR="${BUILDROOT}/build"
PARAVIEW_VERSION="5.0.0"
STAGING_DIR="${BUILDROOT}/staging"
STAGING_PARAVIEW="${STAGING_DIR}/paraview/${PARAVIEW_VERSION}"
STAGING_PLUGINS="${STAGING_DIR}/paraview-plugins/${PARAVIEW_VERSION}/${DATAVERSION}"

set -e

name=Edge
install -d ${BUILD_DIR}/Plugins-ReadUAL${name}
install -d ${STAGING_PLUGINS}
cd ${BUILD_DIR}/Plugins-ReadUAL${name}
cmake -DCMAKE_BUILD_TYPE:STRING=Debug \
    -DCMAKE_INSTALL_PREFIX:PATH=${STAGING_PARAVIEW} \
    -DParaView_DIR:PATH=${STAGING_PARAVIEW} \
    ${BUILDROOT}/src/plugins/paraview 
make -j 8 VERBOSE=1 all
install -d ${STAGING_PLUGINS}
install ${BUILD_DIR}/Plugins-ReadUAL${name}/libReadUAL${name}.so \
	${STAGING_PLUGINS}




