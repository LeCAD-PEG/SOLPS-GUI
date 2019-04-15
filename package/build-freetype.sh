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
VERSION=${VERSION:-2.10.0}
MAIN_VERSION=${VERSION%.*}
SOURCE="freetype-${VERSION}.tar.gz"
DOWNLOAD="https://sourceforge.net/projects/freetype/files/freetype2/${VERSION}/freetype-${VERSION}.tar.gz/download"
SRC_DIR="${BUILD_DIR}/freetype-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/freetype/${VERSION}

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
if [ ! -d ${MODULE_DIR}/freetype ]; then
    install -d ${MODULE_DIR}/freetype
fi

cat << EOF > ${MODULE_DIR}/freetype/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
puts stderr "\tA free, high-quality, and portable font engine"
}
module-whatis "A free, high-quality, and portable font engine "

conflict freetype
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_PATH       ${INSTALL_DIR}/lib
prepend-path CPATH              ${INSTALL_DiR}/include
prepend-path PATH               ${INSTALL_DiR}/bin
EOF