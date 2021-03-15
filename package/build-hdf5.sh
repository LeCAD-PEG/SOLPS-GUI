#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="hdf5"
VERSION=${VERSION:-1.10.6}
GIT_LINK="https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_gitCloneSingleBranch ${GIT_LINK} "hdf5-$(tr '.' '_' <<< ${VERSION})"

_cmake "-DHDF5_ENABLE_Z_LIB_SUPPORT:BOOL=ON"
_make "-j${MAKE_JOBS}"
_install
