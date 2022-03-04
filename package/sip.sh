#!/bin/bash -e

PACKAGE=sip
VERSION=${VERSION:-4.19.25}
DOWNLOAD_LINK=https://distfiles.macports.org/py-sip/sip-${VERSION}.tar.gz
FILENAME=${PACKAGE}_gpl-${VERSION}.tar.gz

source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

_prerequisites python

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

CONFIGURE_FLAG="--bindir=${PACKAGE_INSTALL_DIR}/bin"
CONFIGURE_FLAG="${CONFIGURE_FLAG} --sip-module=PyQt5.sip"
CONFIGURE_FLAG="${CONFIGURE_FLAG} --destdir=${PACKAGE_INSTALL_DIR}/lib"


eval $(${PACKAGE_DIR}/python.sh --env)

cd ${PACKAGE_SOURCE_DIR}
_python_configure_custom "${PACKAGE_SOURCE_DIR}/configure.py" "${CONFIGURE_FLAG}"
_make "-j${MAKE_JOBS}"
_install
