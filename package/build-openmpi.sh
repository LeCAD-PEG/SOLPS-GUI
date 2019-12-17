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
VERSION=${VERSION:-4.0.0}
GIT="https://github.com/open-mpi/ompi.git"
SRC_DIR="${BUILD_DIR}/openmpi-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/openmpi/${VERSION}


# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi


# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    git clone --branch v${VERSION} --single-branch ${GIT} ${SRC_DIR}
fi
install -d ${SRC_DIR}
cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    if [ ! -e ${SRC_DIR}/configure ]; then
        ./autogen.pl
    fi
    ./configure --prefix=${INSTALL_DIR}
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make -j${MAKE_JOBS}
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    make install
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/OpenMPI ]; then
    install -d ${MODULE_DIR}/OpenMPI
fi

cat << EOF > ${MODULE_DIR}/OpenMPI/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
The Open MPI Project is an open source Message Passing Interface implementation
that is developed and maintained by a consortium of academic, research, and
industry partners. Open MPI is therefore able to combine the expertise,
technologies, and resources from all across the High Performance Computing
community in order to build the best MPI library available. Open MPI offers
advantages for system and software vendors, application developers and
computer science researchers.


More information
================
 - Homepage: https://www.open-mpi.org/
    }
}


module-whatis {Description: The Open MPI Project is an open source Message Passing Interface implementation
that is developed and maintained by a consortium of academic, research, and
industry partners. Open MPI is therefore able to combine the expertise,
technologies, and resources from all across the High Performance Computing
community in order to build the best MPI library available. Open MPI offers
advantages for system and software vendors, application developers and
computer science researchers. }
module-whatis {Homepage: https://www.open-mpi.org/}

conflict OpenMPI
prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_PATH       ${INSTALL_DIR}/lib
prepend-path PATH               ${INSTALL_DIR}/bin
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkg-config
EOF