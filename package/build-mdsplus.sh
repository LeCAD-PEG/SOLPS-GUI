#!/bin/sh -x
set -e
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${BUILDROOT}/staging
MDSPLUS_VERSION=${MDSPLUS_VERSION:-stable_release-7-7-8}

MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

MDSPLUS_SOURCE="mdsplus-${MDSPLUS_VERSION}.tar.gz"
MDSPLUS_DOWNLOAD="https://github.com/MDSplus/mdsplus/archive/${MDSPLUS_VERSION}.tar.gz"

if [ ! -f ${DOWNLOAD_DIR}/${MDSPLUS_SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${MDSPLUS_SOURCE} ${MDSPLUS_DOWNLOAD}
fi

MDSPLUS_SRC_DIR="${BUILD_DIR}/mdsplus-${MDSPLUS_VERSION}"
if [ ! -e ${MDSPLUS_SRC_DIR}/.built ]; then
    rm -rf ${MDSPLUS_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${MDSPLUS_SOURCE}
    cd ${MDSPLUS_SRC_DIR}
    LD_LIBRARY_PATH=${STAGING_DIR}/lib \
    CFLAGS=-I${STAGING_DIR}/include/libxml2 \
    LDFLAGS=-lpthread \
    ./configure --prefix=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION} \
                --enable-shared --disable-doxygen-doc \
                --disable-xmltest --with-xml-prefix=${STAGING_DIR} \
                --without-labview
    make all # Errors with jobs > 1
    make install
    touch ${MDSPLUS_SRC_DIR}/.built
fi