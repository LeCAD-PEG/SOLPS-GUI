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
VERSION=${VERSION:-2.3.8}
MAIN_VERSION=${VERSION%.*}
SOURCE="motif-${VERSION}.tar.gz"
DOWNLOAD="https://sourceforge.net/projects/motif/files/Motif%20${VERSION}%20Source%20Code/${SOURCE}/download"
SRC_DIR="${BUILD_DIR}/motif-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/motif/${VERSION}

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
    ./configure --prefix=${INSTALL_DIR}
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
    make install
fi


# Generate Modulefile
if [ ! -d ${MODULE_DIR}/motif ]; then
    install -d ${MODULE_DIR}/motif
fi

cat << EOF > ${MODULE_DIR}/motif/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
puts stderr "\tIn computing, Motif refers to both a graphical user interface
(GUI) specification and the widget toolkit for building applications that
follow that specification under the X Window System on Unix and Unix-like
operating systems. "
}
module-whatis "In computing, Motif refers to both a graphical user interface
(GUI) specification and the widget toolkit for building applications that
follow that specification under the X Window System on Unix and Unix-like
operating systems. "

conflict cmake
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_PATH       ${INSTALL_DIR}/lib
prepend-path CPATH              ${INSTALL_DiR}/include
prepend-path PATH               ${INSTALL_DiR}/bin
EOF