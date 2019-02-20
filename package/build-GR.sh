#!/bin/sh -x
set -e


case $(hostname -f) in
    *)
esac

MAKE_JOBS=${MAKE_JOBS:-$(nproc)} # Should use all threads of a system


BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}

GR_GIT="ssh://git@git.iter.org/lib/gr-software.git"


install -d ${BUILD_DIR}
install -d ${STAGING_DIR}

GR_SRC_DIR="${BUILD_DIR}/gr-software"
if [ ! -e ${GR_SRC_DIR}/.built ]; then
    rm -rf ${GR_SRC_DIR}
    cd ${BUILD_DIR}
    git clone ${GR_GIT}
    cd ${GR_SRC_DIR}
    make SOLPS_LIB=${STAGING_DIR}/lib BLDFLAG="ar cr" RANLIB=echo allf CFLAGS="-fPIC" F77=gfortran
    make install BLDFLAG="ar cr" RANLIB=echo SOLPS_LIB=${STAGING_DIR}/lib CFLAGS="-FPIC" F77=gfortran
    touch .built
fi
