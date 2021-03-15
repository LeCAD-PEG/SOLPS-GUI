#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="sip"
VERSION=${VERSION:-4.19.25}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="https://distfiles.macports.org/py-sip/sip-${VERSION}.tar.gz"
FILENAME="${PACKAGE}_gpl-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

CONFIGURE_FLAG="--bindir=${PACKAGE_INSTALL_DIR}/bin"
CONFIGURE_FLAG="${CONFIGURE_FLAG} --sip-module=PyQt5.sip"
CONFIGURE_FLAG="${CONFIGURE_FLAG} --destdir=${PACKAGE_INSTALL_DIR}/lib"

cd ${PACKAGE_SOURCE_DIR}
_python_configure_custom "${PACKAGE_SOURCE_DIR}/configure.py" "${CONFIGURE_FLAG}"
_make "-j${MAKE_JOBS}"
_install
