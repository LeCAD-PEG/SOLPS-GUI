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
VERSION=${VERSION:-stable_release-7-96-8}
SOURCE="mdsplus-${VERSION}.tar.gz"
DOWNLOAD="https://github.com/MDSplus/mdsplus/archive/${VERSION}.tar.gz"
INSTALL_DIR=${STAGING_DIR}/mdsplus/${VERSION}
SRC_DIR=${BUILD_DIR}/mdsplus-${VERSION}

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
    CFLAGS=-I${LIBXML2_INSTALL_DIR}/include/libxml2 \
    LDFLAGS=-lpthread \
    ./configure --prefix=${INSTALL_DIR} \
                --enable-shared --disable-doxygen-doc \
                --disable-xmltest \
                --with-xml-prefix=${LIBXML2_INSTALL_DIR} \
                --without-labview
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make all # Errors with jobs > 1
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    make install
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/MDSplus ]; then
    install -d ${MODULE_DIR}/MDSplus
fi

cat << EOF > ${MODULE_DIR}/MDSplus/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
MDSplus is a set of software tools for data acquisition and storage and a methodology
 for management of complex scientific data.


More information
================
 - Homepage: http://mdsplus.org/
    }
}

module-whatis {Description: MDSplus is a set of software tools for data acquisition and storage and a methodology
 for management of complex scientific data.}
module-whatis {Homepage: http://mdsplus.org/}

conflict MDSplus

if { ![ is-loaded libxml2/${LIBXML2_VERSION} ] } {
    module load libxml2/${LIBXML2_VERSION}
}

prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_DIR        ${INSTALL_DIR}/lib
prepend-path PATH               ${INSTALL_DIR}/bin
setenv       MDS_PATH           ${INSTALL_DIR}/tdi
prepend-path IDS_PATH           ${INSTALL_DIR}/idl
EOF