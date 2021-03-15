#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="gr"
VERSION=${VERSION:-0.0.94}
GIT_LINK="ssh://git@git.iter.org/lib/gr-software.git"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_gitCloneSingleBranch ${GIT_LINK} ${VERSION}

cd ${PACKAGE_SOURCE_DIR}

PRE_FLAGS="SOLPS_LIB=${PACKAGE_INSTALL_DIR}/lib"
# PRE_FLAGS="${PRE_FLAGS} BLDFLAG=\"ar cr\""
PRE_FLAGS="${PRE_FLAGS} RANLIB=echo CFLAGS=-fPIC"
PRE_FLAGS="${PRE_FLAGS} F77=gfortran FFLAGS=-std=legacy"
export BLDFLAG="ar cr"
install -d ${PACKAGE_INSTALL_DIR}/lib
_make "libgr.a" "${PRE_FLAGS}"
cp libgr.a ${PACKAGE_INSTALL_DIR}/lib
