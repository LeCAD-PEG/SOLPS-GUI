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
SRC_DIR="${BUILD_DIR}/Plugins-ReadUALEdge"
INSTALL_DIR=${STAGING_DIR}/ReadUALEdge-Plugin/${VERSION}

# Environment dependencies
case $(hostname -f) in
  *.iter.org)
        module purge
    module load IMAS/3.21.0-3.8.6
        module load OpenSSL/1.0.2g-GCC-4.8.3
    module unload Python/2.7.14-intel-2018a
    module load Python/3.6.4-intel-2018a
    # BUILDING PLUGIN FOR ITER PARAVIEW (available as a module)
    #module load ParaView/5.4.1-intel-2018a-mpi
    #export PARAVIEW_PREFIX=${EBROOTPARAVIEW}
    #export CMAKE_PREFIX_PATH=${EBROOTPARAVIEW}/lib/cmake/paraview-5.4
    export CC=gcc -E
    export CXX=g++
    MAKE_JOBS=${MAKE_JOBS:-4}
    ;;

  *.marconi.cineca.it) # EU-IM Gateway with CentOS7.2
    . /etc/profile.d.gw/modules.sh
    module purge
    module load cineca imasenv/3.20.0 #cmake/3.12.0
    module switch itm-python/2.7
    module unload matlab
    QT_VERSION=4.8.7
    module load itm-qt/${QT_VERSION}
    MAKE_JOBS=${MAKE_JOBS:-36}
    ;;

  *)
    PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.4.1}
    PARAVIEW_MAINVERSION=${PARAVIEW_VERSION%.*}
    QT_VERSION=${QT_VERSION:-4.8.7}
    IMASUAL_VERSION=${IMASUAL_VERSION:-3.8.4}
    IMASDD_VERSION=${IMASDD_VERSION:-3.21.0}
    MDSPLUS_VERSION=${MDSPLUS_VERSION:-stable_release-7-7-8}
    BLITZ_VERSION=${BLITZ_VERSION:-1.0.0}
    CMAKE_VERSION=${CMAKE_VERSION:-3.10.1}
    CMAKE=${STAGING_DIR}/cmake/${CMAKE_VERSION}/bin/cmake

    export IMAS_VERSION=${IMASDD_VERSION}

    export PKG_CONFIG_PATH=${STAGING_DIR}/imas/${IMAS_VERSION}/solps/lib/pkgconfig:${PKG_CONFIG_PATH}
    export PKG_CONFIG_PATH=${STAGING_DIR}/blitz/${BLITZ_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}
    export PKG_CONFIG_PATH=${STAGING_DIR}/qt/${QT_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}

    # export LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH}
    # export LD_LIBRARY_PATH=${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/lib:${LD_LIBRARY_PATH}
    # export LD_LIBRARY_PATH=${STAGING_DIR}/qt/${QT_VERSION}/lib:${LD_LIBRARY_PATH}
    # export LD_LIBRARY_PATH=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/lib:${LD_LIBRARY_PATH}

    export PATH=${STAGING_DIR}/paraview/${PARAVIEW_VERSION}/bin:${PATH}
    export PATH=${STAGING_DIR}/qt/${QT_VERSION}/bin:${PATH}

    export MDSPLUS_DIR=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}
    ;;
esac

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
    install -d ${INSTALL_DIR}
    install ${SRC_DIR}/libReadUALEdge.so ${INSTALL_DIR}
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