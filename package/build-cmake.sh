#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="cmake"
VERSION=${VERSION:-3.15.4}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="https://cmake.org/files/v${MAJOR_VERSION}/cmake-${VERSION}.tar.gz"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

_cmake_bootstrap "-- -DCMAKE_EXE_LINKER_FLAGS:STRING=-L${SSL}/lib"
_make "-j${MAKE_JOBS}"
_install
