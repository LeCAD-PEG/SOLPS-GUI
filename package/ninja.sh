#!/bin/bash -e

PACKAGE=ninja
VERSION=${VERSION:-1.10.2}
FILENAME=v${VERSION}.tar.gz
DOWNLOAD_LINK=https://github.com/ninja-build/ninja/archive/${FILENAME}

source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

_prerequisites cmake

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

_cmake 
_cmake_build  "--parallel ${MAKE_JOBS}"
_cmake_install
