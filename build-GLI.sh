#!/bin/sh -x
set -e
GLI_VERSION=${GLI_VERSION:-4.5.30}


case $(hostname -f) in
    *)
esac

MAKE_JOBS=${MAKE_JOBS:-$(nproc)} # Should use all threads of a system


BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD})}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}

GLI_SOURCE="gli-${GLI_VERSION}.tar.gz"
GLI_DOWNLOAD="http://iffwww.iff.kfa-juelich.de/gli/gli-${GLI_VERSION}.tar.gz"


install -d ${BUILD_DIR}
install -d ${DOWNLOAD_DIR}
install -d ${STAGING_DIR}


if [ ! -f ${DOWNLOAD_DIR}/${GLI_SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${GLI_SOURCE} ${GLI_DOWNLOAD}
fi

GLI_SRC_DIR="${BUILD_DIR}/gli"
if [ ! -e ${GLI_SRC_DIR}/.built ]; then
    rm -rf ${GLI_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${GLI_SOURCE}
    cd gli/src
    ./configure CFLAGS="-DUSE_INTERP_RESULT"
    make # Fails if j > 1
    make install DESTDIR=${STAGING_DIR}/gli
    touch ${GLI_SRC_DIR}/.built
fi
