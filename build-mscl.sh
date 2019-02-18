#!/bin/sh -x
set -e
# MSCL_VERSION=4.5.30


case $(hostname -f) in
    *)
esac

MAKE_JOBS=${MAKE_JOBS:-$(nproc)} # Should use all threads of a system


BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD})}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}

MSCL_GIT="ssh://git@git.iter.org/lib/mscl.git"


install -d ${BUILD_DIR}
install -d ${STAGING_DIR}

MSCL_SRC_DIR="${BUILD_DIR}/mscl"
if [ ! -e ${MSCL_SRC_DIR}/.built ]; then
    rm -rf ${MSCL_SRC_DIR}
    cd ${BUILD_DIR}
    git clone ${MSCL_GIT}
    cd ${MSCL_SRC_DIR}
cat <<EOT >> config/compiler.UNKNOWN.gfortran
CC       = gcc
CFLAGS   = -O3 -fPIC -fsecond-underscore

FC   = gfortran
FFLAGS   = -O3 -fPIC -fsecond-underscore
NFLAGS   = -O0 -fPIC -fsecond-underscore

CPP  = cpp
CPPFLAGS = -traditional -P

AR       = ar
EOT

    OBJECTCODE=UNKNOWN.gfortran SOLPS_LIB=${STAGING_DIR}/lib make install -j${MAKE_JOBS}
    touch .built
fi
