#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="qt5"
VERSION=${VERSION:-5.15.2}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="https://download.qt.io/official_releases/qt/${MAJOR_VERSION}/${VERSION}/single/qt-everywhere-opensource-src-${VERSION}.tar.xz"
FILENAME="qt-everywhere-src-${VERSION}.tar.xz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

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

_configure "${CONFIGURE_FLAG}"
_make "-j${MAKE_JOBS}"
_install

# TODO: also install documentation, but that requires LLVM...