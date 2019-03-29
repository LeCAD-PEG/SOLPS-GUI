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
VERSION=${VERSION:-3.21.0}
GIT="ssh://git@git.iter.org/imas/data-dictionary.git"
SRC_DIR="${BUILD_DIR}/data-dictionary-${VERSION}"

# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi


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
