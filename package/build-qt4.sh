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
VERSION=${VERSION:-4.8.7}
SOURCE="qt-everywhere-opensource-src-${VERSION}.tar.gz"
DOWNLOAD="http://download.qt.io/archive/qt/${VERSION%.*}/${VERSION}/${SOURCE}"
SRC_DIR="${BUILD_DIR}/qt-everywhere-opensource-src-${VERSION}"
INSTALL_DIR=${INSTALL_DIR:-${STAGING_DIR}/qt/${VERSION}}

# Environment dependencies

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
    ./configure --prefix=${INSTALL_DIR}  -opensource -confirm-license \
                -no-javascript-jit -no-webkit -no-script -no-scripttools \
                -no-sql-sqlite3 -no-accessibility
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
if [ ! -d ${MODULE_DIR}/Qt4 ]; then
    install -d ${MODULE_DIR}/Qt4
fi
cat << EOF > ${MODULE_DIR}/Qt4/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##

proc ModulesHelp { } {
    puts stderr { Qt is a comprehensive cross-platform C++ application framework. - Homepage: http://qt.io/
    }
}

module-whatis {Description: Qt is a comprehensive cross-platform C++ application framework. - Homepage: http://qt.io/}
conflict Qt4
prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_DIR        ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkgconfig
prepend-path PATH               ${INSTALL_DIR}/bin
EOF

