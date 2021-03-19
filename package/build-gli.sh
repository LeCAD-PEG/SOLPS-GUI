#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="gli"
VERSION=${VERSION:-4.5.30}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="http://iffwww.iff.kfa-juelich.de/gli/gli-${VERSION}.tar.gz"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

cd ${PACKAGE_SOURCE_DIR}/src
export CPATH="-I/usr/include/tirpc:${CPATH}"
PRE_FLAGS="F77=gfortran CFLAGS=-DUSE_INTERP_RESULT LIBS=-ltirpc"
_configure_custom "${PACKAGE_SOURCE_DIR}/src/configure" "" "${PRE_FLAGS}"
_make
mkdir -p ${STAGING_DIR}/${PACKAGE}
_install "DESTDIR=${PACKAGE_INSTALL_DIR}"