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
VERSION=${VERSION:-0.3.8}
SOURCE="OpenBLAS-${VERSION}.tar.gz"
DOWNLOAD="https://github.com/xianyi/OpenBLAS/archive/v${VERSION}.tar.gz"
SRC_DIR="${BUILD_DIR}/OpenBLAS-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/OpenBLAS/${VERSION}

# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source
if [ ! -f ${DOWNLOAD_DIR}/${SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${SOURCE} ${DOWNLOAD}
fi

cd ${BUILD_DIR}

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    tar xzf ${DOWNLOAD_DIR}/${SOURCE}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    touch ${SRC_DIR}/.configured
fi
# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    # Support multiple architectures with dynamic arch.
    DYNAMIC_ARCH=${DYNAMIC_ARCH:-1}
    DYNAMIC_ARCH=${DYNAMIC_ARCH} make -j${MAKE_JOBS}
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    make install PREFIX=${INSTALL_DIR}
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/OpenBLAS ]; then
    install -d ${MODULE_DIR}/OpenBLAS
fi

cat << EOF > ${MODULE_DIR}/OpenBLAS/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.


More information
================
 - Homepage: http://xianyi.github.com/OpenBLAS/
    }
}

module-whatis {Description: OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.}
module-whatis {Homepage: http://xianyi.github.com/OpenBLAS/}

conflict OpenBLAS

prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_DIR        ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkgconfig
EOF
