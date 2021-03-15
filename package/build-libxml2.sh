#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="libxml2"
VERSION=${VERSION:-2.9.10}
GIT_LINK="https://gitlab.gnome.org/GNOME/libxml2.git"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_gitCloneSingleBranch ${GIT_LINK} v${VERSION}

cd ${PACKAGE_SOURCE_DIR}
echo "Applying patch for 2.9.10 to work with Python 3.9..."
_applyPatchIfNecessary ${BUILDROOT}/src/patches/libxml2-patch-for-Python3.9a.patch
_applyPatchIfNecessary ${BUILDROOT}/src/patches/libxml2-patch-for-Python3.9b.patch

_log "Preparing configure."
autoreconf -i -s &> ${PACKAGE_LOG_DIR}/autoreconf.log

# _prepare_configure
_configure "--with-python=${PYTHON_INSTALL_DIR}"
_make "-j${MAKE_JOBS}"
_install
