#!/bin/sh -x
set -e
OPENBLAS_VERSION=${OPENBLAS_VERSION:-0.3.5}

case $(hostname -f) in
    *)
esac

MAKE_JOBS=${MAKE_JOBS:-$(nproc)} # Should use all threads of a system


BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging} # Default install location for OpenBLAS. Requires administration rights.

OPENBLAS_SOURCE="OpenBLAS-${OPENBLAS_VERSION}.tar.gz"
OPENBLAS_DOWNLOAD="https://github.com/xianyi/OpenBLAS/archive/v${OPENBLAS_VERSION}.tar.gz"


install -d ${BUILD_DIR}
install -d ${DOWNLOAD_DIR}
install -d ${STAGING_DIR}


if [ ! -f ${DOWNLOAD_DIR}/${OPENBLAS_SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${OPENBLAS_SOURCE} ${OPENBLAS_DOWNLOAD}
fi

OPENBLAS_SRC_DIR="${BUILD_DIR}/OpenBLAS-${OPENBLAS_VERSION}"
if [ ! -e ${OPENBLAS_SRC_DIR}/.built ]; then
    rm -rf ${OPENBLAS_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${OPENBLAS_SOURCE}
    cd ${OPENBLAS_SRC_DIR}

    make -j ${MAKE_JOBS}
    make install PREFIX=${STAGING_DIR}
    touch ${OPENBLAS_SRC_DIR}/.built
fi