#!/bin/bash -e 

PACKAGE=pyqt5
VERSION=${VERSION:-5.15.2}
DOWNLOAD_LINK=https://distfiles.macports.org/py-pyqt5/PyQt5-${VERSION}.tar.gz
FILENAME=${PACKAGE}_gpl-${VERSION}.tar.gz

source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

_prerequisites python sip qt5

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

SIP_INSTALL_DIR=$(${PACKAGE_DIR}/sip.sh --prefix)
QTDIR=$(${PACKAGE_DIR}/qt5.sh --prefix)
PYTHON_VERSION=$(${PACKAGE_DIR}/python.sh --version)
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}

CONFIGURE_FLAG="--verbose --confirm-license"
CONFIGURE_FLAG+=" --qmake=${QTDIR}/bin/qmake"
CONFIGURE_FLAG+=" --sip=${SIP_INSTALL_DIR}/bin/sip"
CONFIGURE_FLAG+=" --destdir=${PACKAGE_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages"

eval $(${PACKAGE_DIR}/python.sh --env)
eval $(${PACKAGE_DIR}/qt5.sh --env --pkg)

cd ${PACKAGE_SOURCE_DIR}
_python_configure_custom "${PACKAGE_SOURCE_DIR}/configure.py" "${CONFIGURE_FLAG}"
_make "-j${MAKE_JOBS}"
_install
