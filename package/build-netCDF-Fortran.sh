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
VERSION=${VERSION:-4.5.3}
GIT="https://github.com/Unidata/netcdf-fortran.git"
SRC_DIR="${BUILD_DIR}/netcdf-fortran-${VERSION}"
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
    install -d ${BUILD_DIR}/NetCDF-Fortran-${VERSION}
    cd ${BUILD_DIR}/NetCDF-Fortran-${VERSION}
    CPPFLAGS="-I${NCDIR}/include -L${ODIR}/include" LDFLAGS="-L${NCDIR}/lib -L\${ODIR}/lib" \
    cmake -DCMAKE_INSTALL_PREFIX=${STAGING_DIR}/netcdf/${NETCDF_VERSION} \
          -DCMAKE_PREFIX_PATH="${ODIR} ${NCDIR}" \
          -DnetCDF_LIBRARY_DIR="${NCDIR}/lib/libnetcdf.so" \
          \ # -DNETCDF_C_LIBRARY="${NCDIR}/lib/libnetcdf.so" \
          -DnetCDF_INCLUDE_DIR="${NCDIR}/include" \
          \ # -DNETCDF_C_INCLUDE="${NCDIR}/include/netcdf.h" \
          ${SRC_DIR}
    # ./configure --prefix=${INSTALL_DIR} \
    #      --with-pic  FCFLAGS="-fPIC -O2 -march=native" FC="gfortran"\
    #     --with-CURL=${ODIR} \
    #     --with-HDF5=${H5DIR}
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make -j1 # Fails >1
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -e ${INSTALL_DIR} ]; then
    make install
fi

# Do not create module file. It is created with build-netcdf.sh