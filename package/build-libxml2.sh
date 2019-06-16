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
VERSION=${VERSION:-2.9.1}
GIT="https://gitlab.gnome.org/GNOME/libxml2.git"
SRC_DIR="${BUILD_DIR}/libxml2-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/libxml2/${VERSION}

# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi


# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    git clone --branch v${VERSION} --single-branch ${GIT} ${SRC_DIR}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    autoreconf -i
    ./configure --with-python=${PYTHON_INSTALL_DIR} \
                --prefix=${INSTALL_DIR}
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
if [ ! -d ${MODULE_DIR}/libxml2 ]; then
    install -d ${MODULE_DIR}/libxml2
fi

cat << EOF > ${MODULE_DIR}/libxml2/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
puts stderr "\tThis module sets the environment for libxml2 v${VERSION}"
}

module-whatis "Libxml2 is the XML C parser and toolkit developed for the Gnome project (but usable outside of the Gnome platform). (v${VERSION}"

conflict libxml2

if { ![ is-loaded Python/${PYTHON_VERSION} ] } {
    module load Python/${PYTHON_VERSION}
}

prepend-path PATH                   ${INSTALL_DIR}/bin
prepend-path CPATH                  ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH        ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH        ${INSTALL_DIR}/lib/pkgconfig
EOF