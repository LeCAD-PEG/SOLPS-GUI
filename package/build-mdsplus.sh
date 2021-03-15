#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="mdsplus"
VERSION=${VERSION:-7.96.8}
DOWNLOAD_LINK="https://github.com/MDSplus/mdsplus/archive/stable_release-$(tr '.' '-' <<< ${VERSION}).tar.gz"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

cd ${PACKAGE_SOURCE_DIR}

PRE_FLAGS="CFLAGS=-I${LIBXML2_INSTALL_DIR}/include/libxml2 LDFLAGS=-lpthread"
CONFIGURE_FLAG="--enable-shared --disable-doxygen-doc"
CONFIGURE_FLAG="${CONFIGURE_FLAG} --disable-xmltest"
CONFIGURE_FLAG="${CONFIGURE_FLAG} --with-xml-prefix=${LIBXML2_INSTALL_DIR}"
CONFIGURE_FLAG="${CONFIGURE_FLAG} --without-labview"
_configure "${CONFIGURE_FLAG}" "${PRE_FLAGS}"
_applyPatchIfNecessary ${BUILDROOT}/src/patches/mdsplus-mitdevices-do-NOT-clear-LD_LIBRARY_PATH.patch ${PACKAGE_BUILD_DIR}
_make "all"
_install