#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="ggd"
VERSION=${VERSION:-1.9.1}
GIT_LINK="ssh://git@git.iter.org/imex/ggd.git"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_gitCloneSingleBranch ${GIT_LINK} ${VERSION}

cd ${PACKAGE_SOURCE_DIR}
./bootstrap

CONFIGURE_FLAG="--enable-doc --enable-tests --enable-modulefile"
CONFIGURE_FLAG="${CONFIGURE_FLAG} --with-module-prefix=${PACKAGE_INSTALL_DIR}/include"

_configure "${CONFIGURE_FLAG}"
_make
_install
