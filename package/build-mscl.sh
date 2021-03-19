#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="mscl"
VERSION=${VERSION:-1.1.1}
GIT_LINK="ssh://git@git.iter.org/lib/mscl.git"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_gitCloneSingleBranch ${GIT_LINK} ${VERSION}
cd ${PACKAGE_SOURCE_DIR}

cat <<EOF > ${PACKAGE_SOURCE_DIR}/config/compiler.UNKNOWN.gfortran
CC       = gcc
CFLAGS   = -O3 -fPIC -fsecond-underscore

FC   = gfortran
FFLAGS   = -O3 -fPIC -fsecond-underscore
NFLAGS   = -O0 -fPIC -fsecond-underscore

CPP  = cpp
CPPFLAGS = -traditional -P

AR       = ar
EOF

PRE_FLAGS="OBJECTCODE=UNKNOWN.gfortran SOLPS_LIB=${PACKAGE_INSTALL_DIR}/lib"

cd ${PACKAGE_SOURCE_DIR}
_make "-j${MAKE_JOBS}" "${PRE_FLAGS}"
_install "" "${PRE_FLAGS}"
