#!/bin/sh -x
set -e
BLITZ_VERSION=${BLITZ_VERSION:-1.0.0} # Apparently this is the same as 0.10.0
BLITZ_SOURCE="blitz-${BLITZ_VERSION}.tar.gz"
BLITZ_DOWNLOAD="https://github.com/blitzpp/blitz/archive/${BLITZ_VERSION}.tar.gz"
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
echo $BUILDROOT
exit
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}

MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

if [ ! -f ${DOWNLOAD_DIR}/${BLITZ_SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${BLITZ_SOURCE} ${BLITZ_DOWNLOAD}
fi

BLITZ_SRC_DIR="${BUILD_DIR}/blitz-${BLITZ_VERSION}"
if [ ! -e ${BLITZ_SRC_DIR}/.built ]; then
    rm -rf ${BLITZ_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${BLITZ_SOURCE}
    cd ${BLITZ_SRC_DIR}
    CXX=g++ ./configure --prefix=${STAGING_DIR} --with-pic
    make #-j ${MAKE_JOBS}
    make install
    touch ${BLITZ_SRC_DIR}/.built
fi