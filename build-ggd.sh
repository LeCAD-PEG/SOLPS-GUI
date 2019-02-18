#!/bin/sh -x
set -e
IMASDD_VERSION=${IMASDD_VERSION:-3.21.0}
IMASUAL_VERSION=${IMASUAL_VERSION:-3.8.4}
GGD_VERSION=${GGD_VERSION:-1.8.3}
MDSPLUS_VERSION=${MDSPLUS_VERSION:-stable_release-7-7-8}

case $(hostname -f) in
    *)
esac

MAKE_JOBS=${MAKE_JOBS:-$(nproc)} # Should use all threads of a system


BUILDROOT=$(cd ${0%/*} && echo ${PWD})
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}

GGD_GIT="ssh://git@git.iter.org/imex/ggd.git"


install -d ${BUILD_DIR}
install -d ${STAGING_DIR}

GGD_SRC_DIR="${BUILD_DIR}/ggd-${GGD_VERSION}"
if [ ! -e ${GGD_SRC_DIR}/.built ]; then
    rm -rf ${GGD_SRC_DIR}
    cd ${BUILD_DIR}
    git clone --branch ${GGD_VERSION} --single-branch ${GGD_GIT} ${GGD_SRC_DIR}
    cd ${GGD_SRC_DIR}
    export IMAS_VERSION=${IMASDD_VERSION}
    export UAL_VERSION=${IMASUAL_VERSION}
    export IMAS_PREFIX=${STAGING_DIR}/access-layer/${IMASUAL_VERSION}
    export PATH=${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/bin:${PATH}
    export LD_LIBRARY_PATH=${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/lib:${LD_LIBRARY_PATH}
    export LD_LIBRARY_PATH=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/lib:${LD_LIBRARY_PATH}
    export PKG_CONFIG_PATH=${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}
    export ids_path=${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/models/mdsplus
    export imasfortran_LIBS="-L${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/lib -limas-gfortran -limas"
    export imasfortran_CFLAGS="-I${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/include/gfortran"
    ./bootstrap
    ./configure \
        --prefix=${STAGING_DIR}/ggd/${GGD_VERSION} \
        --enable-doc --enable-tests \
        FC=gfortran
    make
    make install
    make check
    touch ${GGD_SRC_DIR}/.built
fi
