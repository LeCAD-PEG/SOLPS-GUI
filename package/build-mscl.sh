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
VERSION=${VERSION:-1.1.1}
GIT="ssh://git@git.iter.org/lib/mscl.git"
SRC_DIR="${BUILD_DIR}/mscl-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/mscl/${VERSION}

# Environment dependencies

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    git clone --branch ${VERSION} --single-branch ${GIT} ${SRC_DIR}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    cat <<EOF > ${SRC_DIR}/config/compiler.UNKNOWN.gfortran
CC       = gcc
CFLAGS   = -O3 -fPIC -fsecond-underscore

FC   = gfortran
FFLAGS   = -O3 -fPIC -fsecond-underscore
NFLAGS   = -O0 -fPIC -fsecond-underscore

CPP  = cpp
CPPFLAGS = -traditional -P

AR       = ar
EOF
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    OBJECTCODE=UNKNOWN.gfortran SOLPS_LIB=${INSTALL_DIR}/lib \
    make -j${MAKE_JOBS}
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    OBJECTCODE=UNKNOWN.gfortran SOLPS_LIB=${INSTALL_DIR}/lib \
    make install
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/mscl ]; then
    install -d ${MODULE_DIR}/mscl
fi

cat << EOF > ${MODULE_DIR}/mscl/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
Standard library used within SOLPS distribution.


More information
================
 - Homepage: https://git.iter.org/projects/LIB/repos/mscl
    }
}

module-whatis {Description: Standard library used within SOLPS distribution.}
module-whatis {Homepage: https://git.iter.org/projects/LIB/repos/mscl}

conflict MSCL

prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_DIR        ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkgconfig

EOF