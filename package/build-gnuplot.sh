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
VERSION=${VERSION:-5.2.7}
SOURCE="gnuplot-${VERSION}.tar.gz"
DOWNLOAD="http://sourceforge.net/projects/gnuplot/files/gnuplot/${VERSION}/${SOURCE}/download"
SRC_DIR="${BUILD_DIR}/gnuplot-${VERSION}"
INSTALL_DIR="${STAGING_DIR}/gnuplot/${VERSION}"


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
    wget -O ${DOWNLOAD_DIR}/${SOURCE} ${DOWNLOAD} --no-check-certificate
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
    libtoolize
    CXXFLAGS=" -std=c++11" \
    ./configure --without-cairo --prefix=${INSTALL_DIR} \
        --with-qt=qt5 --without-libcerf --disable-wxwidgets \
        --with-texdir=${INSTALL_DIR}/share/tex
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make -j${MAKE_JOBS}
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    make install
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/gnuplot ]; then
    install -d ${MODULE_DIR}/gnuplot
fi

cat << EOF > ${MODULE_DIR}/gnuplot/${VERSION}-qt-${QT_VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
Portable interactive, function plotting utility


More information
================
 - Homepage: http://gnuplot.sourceforge.net/
    }
}

module-whatis {Description: Portable interactive, function plotting utility}
module-whatis {Homepage: http://gnuplot.sourceforge.net/}

conflict gnuplot

if { ![ is-loaded Qt5/${QT_VERSION} ] } {
    module load Qt5/${QT_VERSION}
}

prepend-path PATH               ${INSTALL_DIR}/bin
EOF