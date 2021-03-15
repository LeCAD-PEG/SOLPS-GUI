#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="imas"
DD_VERSION=${IMASDD_VERSION}
VERSION=${VERSION:-4.8.7}
UAL_VERSION=${VERSION}
GIT_LINK="ssh://git@git.iter.org/imas/access-layer.git"

# Installation path is imas/IMASDD_VERSION/solps
VERSION="${IMASDD_VERSION}/solps"
if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_gitCloneSingleBranch ${GIT_LINK} ${UAL_VERSION}

# Patch sources
cd ${PACKAGE_SOURCE_DIR}
_applyPatchIfNecessary ${BUILDROOT}/src/patches/imas-comment-documentation-installation.patch
ln -sf ${SOURCE_DIR}/imasdd-${IMASDD_VERSION} xml

# Have to export variables because for some reason IMAS Makefile can't handle
# them when supplied via env
export IMAS_IFORT='no'
export IMAS_PYTHON='yes' IMAS_PYTHON2='no' IMAS_PYTHON3='yes'
export IMAS_CPP='yes' IMAS_FORTRAN='yes'
export IMAS_JAVA='no'
export IMAS_MATLAB='no'
export IMAS_UDA='no'
export IMAS_MEX='no'
export IMAS_MDSPLUS='yes'
export IMAS_PREFIX=${PACKAGE_INSTALL_DIR}
_make "-j${MAKE_JOBS}"
_install "IMAS_INSTALL_DIR=${PACKAGE_INSTALL_DIR}"

# Post install fixes

# Disable the fail on error
set +e
if ! grep -Fxq "Version: - ${IMAS_VERSION}-${UAL_VERSION}" ${PACKAGE_INSTALL_DIR}/lib/pkgconfig/imas-gfortran.pc
then
    sed -i -e "s/Version: -/Version: - ${IMAS_VERSION}-${UAL_VERSION}/g" ${PACKAGE_INSTALL_DIR}/lib/pkgconfig/imas-gfortran.pc
fi
# Enable the fail on error
set -e

A=$(echo "imas_${IMAS_VERSION}_ual_${UAL_VERSION}"|tr . _)
B=$(uname -m) # Get system bitness
# Link imas as imas, so you can simply say import imas in python!
ln -sf $A ${PACKAGE_INSTALL_DIR}/python/lib.linux-${B}-${PYTHON_MAINVERSION}/imas
