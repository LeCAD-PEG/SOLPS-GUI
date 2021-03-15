#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="gli"
VERSION=${VERSION:-4.5.30}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="http://iffwww.iff.kfa-juelich.de/gli/gli-${VERSION}.tar.gz"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

_configure "" "CFLAGS=-DUSE_INTERP_RESULT"
_make "gli gligksm  cgmview libgks.so libgus.so"
_make "dist DESTDIR=${PACKAGE_INSTALL_DIR}"