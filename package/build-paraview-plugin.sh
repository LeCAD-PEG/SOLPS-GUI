#!/bin/sh -x
set -e


# Variables
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

# Buildroot directories
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
DOWNLOAD_DIR=${BUILDROOT}/download

# Package variables
VERSION=${VERSION:-1.5.0}
SRC_DIR="${BUILD_DIR}/ReadUALEdge-Plugin"
INSTALL_DIR=${STAGING_DIR}/ReadUALEdge-Plugin/${VERSION}

# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source

cd ${BUILD_DIR}

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    install -d ${SRC_DIR}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    IMAS_VERSION_DIGIT=$(echo "$IMAS_VERSION" | sed "s/\.//g") \
    ${CMAKE} -DCMAKE_BUILD_TYPE:STRING=Debug \
    -DParaView_DIR:PATH=${STAGING_DIR}/ParaView/${PARAVIEW_VERSION} \
    -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR} \
    ${BUILDROOT}/src/plugins/paraview
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make -j${MAKE_JOBS} VERBOSE=1
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    make install
    # install -d ${INSTALL_DIR}
    # install ${SRC_DIR}/libReadUALEdge.so ${INSTALL_DIR}
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/paraview-plugin-edge ]; then
    install -d ${MODULE_DIR}/paraview-plugin-edge
fi

cat << EOF > ${MODULE_DIR}/paraview-plugin-edge/1.5
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
puts stderr "\tThis module sets the environment for blitz "
}
module-whatis  "ReadUAL-EDGE plugin for ParaView."

conflict paraview-plugin

if { ![ is-loaded imas/${IMAS_VERSION}/solps ] } {
    module load imas/${IMAS_VERSION}/solps
}

if { ![ is-loaded ParaView/${PARAVIEW_VERSION} ] } {
    module load ParaView/${PARAVIEW_VERSION}
}

if { ![ is-loaded MDSplus/${MDSPLUS_VERSION} ] } {
    module load MDSplus/${MDSPLUS_VERSION}
}

prepend-path PV_PLUGIN_PATH          ${INSTALL_DIR}
EOF