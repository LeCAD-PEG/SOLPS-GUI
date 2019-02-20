#!/bin/sh -x
set -e
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${BUILDROOT}/staging
LIBXML2_VERSION=${LIBXML2_VERSION:-2.9.1}

MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

LIBXML2_SRC="libxml2-${LIBXML2_VERSION}.tar.gz"
LIBXML2_SITE="ftp://xmlsoft.org/libxml2" # Using FTP site, to avoid using
                                         # autoconf tools on the github release
LIBXML2_DOWNLOAD="${LIBXML2_SITE}/libxml2-${LIBXML2_VERSION}.tar.gz"

if [ ! -f ${DOWNLOAD_DIR}/${LIBXML2_SRC} ]; then
    wget  -O ${DOWNLOAD_DIR}/${LIBXML2_SRC} ${LIBXML2_DOWNLOAD}
fi

LIBXML2_SRC_DIR="${BUILD_DIR}/libxml2-${LIBXML2_VERSION}"
if [ ! -e ${LIBXML2_SRC_DIR}/.built ]; then
    rm -rf ${LIBXML2_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${LIBXML2_SRC}
    cd ${LIBXML2_SRC_DIR}
    PATH=${STAGING_DIR}/bin:${PATH} \
    PYTHONPATH=${STAGING_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages \
    LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} \
    ./configure --with-python=${STAGING_DIR} \
      --prefix=${STAGING_DIR} LDFLAGS=-L${STAGING_DIR}/lib
    make -j${MAKE_JOBS}
    make install
    # Not sure if python bindings needed
    # cd python
    # CFLAGS=-I${LIBXML2_SRC_DIR}/include ${STAGING_DIR}/bin/python3 setup.py build
    # CFLAGS=-I${LIBXML2_SRC_DIR}/include ${STAGING_DIR}/bin/python3 setup.py install
    touch .built
fi