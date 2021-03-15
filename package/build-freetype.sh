#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="freetype"
VERSION=${VERSION:-2.10.0}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="https://sourceforge.net/projects/freetype/files/freetype2/${VERSION}/freetype-${VERSION}.tar.gz/download"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

_configure
_make "-j${MAKE_JOBS}"
_install
