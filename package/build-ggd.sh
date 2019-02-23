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


BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
GGD_INSTALL_DIR=${STAGING_DIR}/GGD/${GGD_VERSION}
IMAS_INSTALL_DIR=${STAGING_DIR}/imas/${IMASDD_VERSION}/solps

GGD_GIT="ssh://git@git.iter.org/imex/ggd.git"


install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${GGD_INSTALL_DIR}

GGD_SRC_DIR="${BUILD_DIR}/ggd-${GGD_VERSION}"
if [ ! -e ${GGD_SRC_DIR}/.built ]; then
    rm -rf ${GGD_SRC_DIR}
    cd ${BUILD_DIR}
    git clone --branch ${GGD_VERSION} --single-branch ${GGD_GIT} ${GGD_SRC_DIR}
    cd ${GGD_SRC_DIR}
    export IMAS_VERSION=${IMASDD_VERSION}
    export UAL_VERSION=${IMASUAL_VERSION}
    export IMAS_PREFIX=${IMAS_INSTALL_DIR}
    export PATH=${IMAS_INSTALL_DIR}/bin:${PATH}
    export LD_LIBRARY_PATH=${IMAS_INSTALL_DIR}/lib:${LD_LIBRARY_PATH}
    export LD_LIBRARY_PATH=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/lib:${LD_LIBRARY_PATH}
    export PKG_CONFIG_PATH=${IMAS_INSTALL_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}
    export ids_path=${IMAS_INSTALL_DIR}/models/mdsplus
    export imasfortran_LIBS="-L${IMAS_INSTALL_DIR}/lib -limas-gfortran -limas"
    export imasfortran_CFLAGS="-I${IMAS_INSTALL_DIR}/include/gfortran"
    ./bootstrap
    ./configure \
        --prefix=${GGD_INSTALL_DIR} \
        --enable-doc --enable-tests \
        --enable-modulefile \
        --with-module-prefix=${GGD_INSTALL_DIR}/include \
        FC=gfortran
    make
    make install
    make check
    touch ${GGD_SRC_DIR}/.built
fi

# Generate Modulefile
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/GGD ]; then
	install -d ${MODULE_DIR}/GGD
fi

cat << EOF > ${MODULE_DIR}/GGD/${GGD_VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
IMAS GGD Grid Service Library


More information
================
 - Homepage: http://imas.iter.org/
    }
}

module-whatis {Description: IMAS GGD Grid Service Library}
module-whatis {Homepage: http://imas.iter.org/}

conflict GGD

if { ![ is-loaded imas/${IMASDD_VERSION}/solps ] } {
    module load imas/${IMASDD_VERSION}/solps
}

prepend-path CPATH              ${GGD_INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${GGD_INSTALL_DIR}/lib
prepend-path LIBRARY_PATH       ${GGD_INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${GGD_INSTALL_DIR}/lib/pkgconfig
EOF