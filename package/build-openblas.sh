#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="openblas"
VERSION=${VERSION:-0.3.13}
DOWNLOAD_LINK="https://github.com/xianyi/OpenBLAS/archive/v${VERSION}.tar.gz"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

cd ${PACKAGE_SOURCE_DIR}
# Since OpenBLAS make has no configure and CMake is still not as stable
# we have to manually go into the source directory and compile it.
_make "" "DYNAMIC_ARCH=1"
_install "PREFIX=${PACKAGE_INSTALL_DIR}"