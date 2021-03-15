#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="flex"
VERSION=${VERSION:-2.6.3}
MAJOR_VERSION=${VERSION%.*}
VERSION_UNDERSCORE=$(tr '.' '_' <<< ${VERSION})
DOWNLOAD_LINK="https://github.com/westes/flex/archive/v${VERSION}.tar.gz"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

cd ${PACKAGE_SOURCE_DIR}
ln -sf /bin/true makeinfo
ln -sf /bin/true help2man
export PATH=${PACKAGE_SOURCE_DIR}:${PATH}

_prepare_configure
_configure
_make "-j${MAKE_JOBS}"
# Create dummy doc files
touch ${PACKAGE_SOURCE_DIR}/doc/flex.1
_install
