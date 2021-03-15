#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="curl"
VERSION=${VERSION:-7.64.1}
MAJOR_VERSION=${VERSION%.*}
VERSION_UNDERSCORE=$(tr '.' '_' <<< ${VERSION})
DOWNLOAD_LINK="https://github.com/curl/curl/releases/download/curl-${VERSION_UNDERSCORE}/curl-${VERSION}.tar.bz2"
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
