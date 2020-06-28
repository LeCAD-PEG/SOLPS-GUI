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
VERSION=${VERSION:-4.7.4}
GIT="https://github.com/Unidata/netcdf-c"
SRC_DIR="${BUILD_DIR}/netcdf-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/netcdf/${VERSION}


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
    autoreconf -i
    CPPFLAGS="-I${H5DIR}/include -L${ODIR}/include" LDFLAGS="-L${H5DIR}/lib -L${ODIR}/lib" \
    ./configure --prefix=${INSTALL_DIR} --enable-netcdf-4 \
        --with-CURL=${ODIR} \
        --with-HDF5=${H5DIR}
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
if [ ! -d ${MODULE_DIR}/NetCDF ]; then
    install -d ${MODULE_DIR}/NetCDF
fi

cat << EOF > ${MODULE_DIR}/NetCDF/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
NetCDF (network Common Data Form) is a set of software libraries
 and machine-independent data formats that support the creation, access, and sharing of array-oriented
 scientific data.


More information
================
 - Homepage: http://www.unidata.ucar.edu/software/netcdf/
    }
}


module-whatis {Description: NetCDF (network Common Data Form) is a set of software libraries
 and machine-independent data formats that support the creation, access, and sharing of array-oriented
 scientific data.}
module-whatis {Homepage: http://www.unidata.ucar.edu/software/netcdf/}

conflict NetCDF

if { ![ is-loaded hdf5/${HDF5_VERSION} ] } {
    module load hdf5/${HDF5_VERSION}
}

if { ![ is-loaded cURL/${CURL_VERSION} ] } {
    module load cURL/${CURL_VERSION}
}

prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib64
prepend-path LIBRARY_PATH       ${INSTALL_DIR}/lib
prepend-path LIBRARY_PATH       ${INSTALL_DIR}/lib64
prepend-path PATH               ${INSTALL_DIR}/bin
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkg-config
EOF