#!/bin/bash -x
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
VERSION=${VERSION:-1.10.5}
GIT="https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git"
DOWNLOAD="${BUILD_DIR}/hdf5"
SRC_DIR="${BUILD_DIR}/hdf5-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/hdf5/${VERSION}


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
if [ ! -d ${DOWNLOAD} ]; then
    git clone --branch "hdf5-$(tr '.' '_' <<< ${VERSION})" --single-branch ${GIT} ${DOWNLOAD}
fi

install -d ${SRC_DIR}
cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    cmake -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR} ${DOWNLOAD}
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
if [ ! -d ${MODULE_DIR}/hdf5 ]; then
    install -d ${MODULE_DIR}/hdf5
fi

cat << EOF > ${MODULE_DIR}/hdf5/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
Hierarchical Data Format (HDF) is a set of file formats (HDF4, HDF5) designed
to store and organize large amounts of data. Originally developed at the
National Center for Supercomputing Applications, it is supported by The HDF
Group, a non-profit corporation whose mission is to ensure continued
development of HDF5 technologies and the continued accessibility of data
stored in HDF.


More information
================
 - Homepage: https://www.hdfgroup.org
    }
}

module-whatis {Description:
Hierarchical Data Format (HDF) is a set of file formats (HDF4, HDF5) designed
to store and organize large amounts of data. Originally developed at the
National Center for Supercomputing Applications, it is supported by The HDF
Group, a non-profit corporation whose mission is to ensure continued
development of HDF5 technologies and the continued accessibility of data
stored in HDF.
}
module-whatis {Homepage: https://www.hdfgroup.org}

conflict hdf5
prepend-path CPATH              ${INSTALL_DIR}/inclue
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_PATH       ${INSTALL_DIR}/lib
prepend-path PATH               ${INSTALL_DIR}/bin
EOF