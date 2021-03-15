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
VERSION=${VERSION:-5.15.2}
GIT=https://code.qt.io/pyside/pyside-setup.git
SRC_DIR="${BUILD_DIR}/pyside2-${VERSION}"

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
    git clone --branch ${VERSION} --recurse-submodules --single-branch ${GIT} ${SRC_DIR}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    python${PYTHON_MAINVERSION} setup.py install --qmake=${QTDIR}/bin/qmake --cmake=$(which cmake) --module-subset=Core,Gui,Widgets --skip-docs --ignore-git --parallel=${MAKE_JOBS}
fi

# # Install
# set +e
# ${PIP} uninstall -y numpy
# ${PYTHON} setup.py build install --prefix=${PYTHON_INSTALL_DIR}

# # Now install matplotlib.
# ${PIP} show matplotlib
# if [ $? -ne 0 ]; then
#     ${PIP} --trusted-host pypi.python.org install --upgrade matplotlib
# fi

# set -e