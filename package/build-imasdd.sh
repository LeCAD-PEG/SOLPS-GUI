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
VERSION=${VERSION:-3.20.0}
GIT="ssh://git@git.iter.org/imas/data-dictionary.git"
SRC_DIR="${BUILD_DIR}/data-dictionary-${VERSION}"


# Environment dependencies
case $(hostname -f) in
    *)
        PYTHON_VERSION=${PYTHON_VERSION:-3.6.8}
        PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
        SAXON_VERSION=${SAXON_VERSION:-HE9-8-0-12J}

        export PATH=${STAGING_DIR}/Python/${PYTHON_VERSION}/bin:${PATH}
        export PYTHONPATH=${STAGING_DIR}/Python/${PYTHON_VERSION}/lib/python${PYTHON_MAINVERSION}/site-packages
        export LD_LIBRARY_PATH=${STAGING_DIR}/Python/${PYTHON_VERSION}/lib:${LD_LIBRARY_PATH}
        export CLASSPATH=${STAGING_DIR}/saxon/${SAXON_VERSION}/saxon9he.jar
        ;;
esac

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    git clone --branch ${VERSION} --single-branch ${GIT} ${SRC_DIR}
fi

cd ${SRC_DIR}

# Configure

# Build

# Install
if [ ! -e ${SRC_DIR}/.installed ]; then
    make install
    touch ${SRC_DIR}/.installed
fi


# Generate Modulefile
