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
VERSION=${VERSION:-3.6.9}
MAINVERSION=${VERSION%.*}
SOURCE="Python-${VERSION}.tgz"
DOWNLOAD="https://www.python.org/ftp/python/${VERSION}/${SOURCE}"
SRC_DIR="${BUILD_DIR}/Python-${VERSION}"
INSTALL_DIR="${STAGING_DIR}/Python/${VERSION}"

# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi


# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}
## Install Python3

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
    if pkg-config --exists libssl; then
        ssl=$(pkg-config --variable=prefix libssl)
        sed -i -e "s,#SSL=.*,SSL=${ssl}," -e "/^#.*ssl/s/#//" \
        -e '/ssl/s|-lcrypto |-lcrypto -Wl,-rpath,$(SSL)/lib|' Modules/Setup.dist
    fi
    ./configure --prefix=${INSTALL_DIR} --enable-shared # --enable-optimizations
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

    ln -sf python3 ${INSTALL_DIR}/bin/python
    pip3 --trusted-host pypi.python.org install --upgrade \
        pip sphinx sphinx_rtd_theme mock nose Cython wheel setuptools

    # The following Python modules are preferred by IMAS

    # pip3 --trusted-host pypi.python.org install --upgrade \
    #     Cython luigi tornado deap decorator liac-arff ecdsa \
    #     netaddr paramiko virtualenv setuptools \
    #     wheel pyvtk
fi

MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/Python ]; then
	install -d ${MODULE_DIR}/Python
fi

cat << EOF > ${MODULE_DIR}/Python/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
Python is a programming language that lets you work more quickly and integrate your systems
 more effectively.


More information
================
 - Homepage: http://python.org/


    }
}

if { ![ is-loaded OpenBLAS/${OPENBLAS_VERSION} ] } {
    module load OpenBLAS/${OPENBLAS_VERSION}
}

module-whatis {Description: Python is a programming language that lets you work more quickly and integrate your systems
 more effectively.}
module-whatis {Homepage: http://python.org/}

conflict Python
prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib/python${MAINVERSION}/site-packages
prepend-path LIBRARY_DIR        ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkgconfig
prepend-path PATH               ${INSTALL_DIR}/bin
EOF
