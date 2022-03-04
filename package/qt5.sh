#!/bin/bash -e

PACKAGE=qt5
VERSION=${VERSION:-5.15.2}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK=https://download.qt.io/official_releases/qt/${MAJOR_VERSION}/${VERSION}/single/qt-everywhere-src-${VERSION}.tar.xz
FILENAME=qt-everywhere-src-${VERSION}.tar.xz

source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

_prerequisites python sip

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

CONFIGURE_FLAG="-v -release -opensource -confirm-license"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -nomake tests -nomake examples"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -no-rpath"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -no-separate-debug-info"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -xcb"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -qt-libpng -no-eglfs -dbus-runtime"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -skip qtwebengine"

CONFIGURE_FLAG="${CONFIGURE_FLAG} -skip qtwayland"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -skip qtgamepad"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -skip qtwebchannel"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -skip qtwebsockets"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -skip qtwebview"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -skip qtdeclarative"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -skip qtpurchasing"

CONFIGURE_FLAG="${CONFIGURE_FLAG} -qt-harfbuzz"
CONFIGURE_FLAG="${CONFIGURE_FLAG} -no-openssl"
# qmake fails if the following variables are set... https://bugreports.qt.io/browse/QTBUG-78729
unset CPLUS_INCLUDE_PATH
unset CPATH

${PACKAGE_DIR}/python.sh
${PACKAGE_DIR}/sip.sh

eval $(${PACKAGE_DIR}/python.sh --env)
eval $(${PACKAGE_DIR}/sip.sh --env)

_configure "${CONFIGURE_FLAG}"
_make "-j${MAKE_JOBS}"
_install

# TODO: also install documentation, but that requires LLVM...
