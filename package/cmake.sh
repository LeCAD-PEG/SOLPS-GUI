#!/bin/bash -e
PACKAGE=cmake
VERSION=${VERSION:-3.22.2}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="https://cmake.org/files/v${MAJOR_VERSION}/cmake-${VERSION}.tar.gz"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

_cmake_bootstrap "-- -DCMAKE_EXE_LINKER_FLAGS:STRING=-L${SSL}/lib"
_make "-j${MAKE_JOBS}"
_install
