#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="gnuplot"
VERSION=${VERSION:-5.2.8}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="http://sourceforge.net/projects/gnuplot/files/gnuplot/${VERSION}/gnuplot-${VERSION}.tar.gz/download"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

cd ${PACKAGE_SOURCE_DIR}
libtoolize

CONFIGURE_FLAG="--without-cairo --with-qt=qt5 --without-libcerf"
CONFIGURE_FLAG="${CONFIGURE_FLAG} --disable-wxwidgets"
CONFIGURE_FLAG="${CONFIGURE_FLAG} --with-texdir=${PACKAGE_INSTALL_DIR}/share/tex"

_configure "${CONFIGURE_FLAG}" "CXXFLAGS=-std=c++11"
_make "-j${MAKE_JOBS}"
_install