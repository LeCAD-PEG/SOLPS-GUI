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
VERSION=${VERSION:-4.5.30}
SOURCE="gli-${VERSION}.tar.gz"
DOWNLOAD="http://iffwww.iff.kfa-juelich.de/gli/gli-${VERSION}.tar.gz"
SRC_DIR="${BUILD_DIR}/gli"
INSTALL_DIR=${STAGING_DIR}/GLI/${VERSION}

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
    cd ${SRC_DIR}/src
    ./configure CFLAGS="-DUSE_INTERP_RESULT"
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make # Fails if j > 1
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    make install DESTDIR=${INSTALL_DIR}
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/GLI ]; then
    install -d ${MODULE_DIR}/GLI
fi

cat << EOF > ${MODULE_DIR}/GLI/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
Graphics Language Interpreter


More information
================
 - Homepage: http://iffwww.iff.kfa-juelich.de/gli/
    }
}
module-whatis {Description: Graphics Language Interpreter}
module-whatis {Homepage: http://iffwww.iff.kfa-juelich.de/gli/}

conflict GLI
prepend-path PATH               ${INSTALL_DIR}
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}
setenv       GLI_HOME ${INSTALL_DIR}
EOF
