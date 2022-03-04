#!/bin/bash -e

PACKAGE=gnuplot
VERSION=${VERSION:-5.2.8}
FILENAME=${PACKAGE}-${VERSION}.tar.gz
DOWNLOAD_LINK=http://sourceforge.net/projects/gnuplot/files/gnuplot/${VERSION}/${FILENAME}/download


source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

_prerequisites qt5

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

eval $(${PACKAGE_DIR}/qt5.sh --env --pkg)

cd ${PACKAGE_SOURCE_DIR}
libtoolize

CONFIGURE_FLAG="--without-cairo --with-qt=qt5 --without-libcerf"
CONFIGURE_FLAG+=" --disable-wxwidgets"
CONFIGURE_FLAG+=" --with-texdir=${PACKAGE_INSTALL_DIR}/share/tex"

_configure "${CONFIGURE_FLAG}" "CXXFLAGS=-std=c++11"
_make "-j${MAKE_JOBS}"
_install
