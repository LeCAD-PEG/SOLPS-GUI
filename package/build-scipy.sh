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
VERSION=${VERSION:-1.2.1}
SOURCE="scipy-${VERSION}.tar.gz"
DOWNLOAD="https://github.com/scipy/scipy/releases/download/v${VERSION}/scipy-${VERSION}.tar.gz"
SRC_DIR="${BUILD_DIR}/scipy-${VERSION}"


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
    cat <<EOF > site.cfg
[openblas]
libraries = openblas
library_dirs = ${OPENBLAS_INSTALL_DIR}/lib
include_dirs = ${OPENBLAS_INSTALL_DIR}/include
runtime_library_dirs = ${OPENBLAS_INSTALL_DIR}/lib
EOF
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    python3 setup.py build
    touch ${SRC_DIR}/.built
fi

# Install
set +e
pip3 show scipy
if [ $? -ne 0 ]; then
    install -d ${INSTALL_DIR}
    python3 setup.py build install --prefix=${PYTHON_INSTALL_DIR}
fi
set -e