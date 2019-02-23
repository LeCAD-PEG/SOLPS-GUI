#!/bin/sh -x
set -e
OPENBLAS_VERSION=${OPENBLAS_VERSION:-0.3.5}

case $(hostname -f) in
    *)
esac

MAKE_JOBS=${MAKE_JOBS:-$(nproc)} # Should use all threads of a system


BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging} # Default install location for OpenBLAS. Requires administration rights.
OPENBLAS_INSTALL_DIR=${STAGING_DIR}/OpenBLAS/${OPENBLAS_VERSION}

OPENBLAS_SOURCE="OpenBLAS-${OPENBLAS_VERSION}.tar.gz"
OPENBLAS_DOWNLOAD="https://github.com/xianyi/OpenBLAS/archive/v${OPENBLAS_VERSION}.tar.gz"


install -d ${BUILD_DIR}
install -d ${DOWNLOAD_DIR}
install -d ${STAGING_DIR}
install -d ${OPENBLAS_INSTALL_DIR}


if [ ! -f ${DOWNLOAD_DIR}/${OPENBLAS_SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${OPENBLAS_SOURCE} ${OPENBLAS_DOWNLOAD}
fi

OPENBLAS_SRC_DIR="${BUILD_DIR}/OpenBLAS-${OPENBLAS_VERSION}"
if [ ! -e ${OPENBLAS_SRC_DIR}/.built ]; then
    rm -rf ${OPENBLAS_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${OPENBLAS_SOURCE}
    cd ${OPENBLAS_SRC_DIR}

    make -j ${MAKE_JOBS}
    make install PREFIX=${OPENBLAS_INSTALL_DIR}
    touch ${OPENBLAS_SRC_DIR}/.built
fi
# Generate Modulefile
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/OpenBLAS ]; then
	install -d ${MODULE_DIR}/OpenBLAS
fi

cat << EOF > ${MODULE_DIR}/OpenBLAS/${OPENBLAS_VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.


More information
================
 - Homepage: http://xianyi.github.com/OpenBLAS/
    }
}

module-whatis {Description: OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.}
module-whatis {Homepage: http://xianyi.github.com/OpenBLAS/}

conflict OpenBLAS

prepend-path CPATH              ${OPENBLAS_INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${OPENBLAS_INSTALL_DIR}/lib
prepend-path LIBRARY_DIR        ${OPENBLAS_INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${OPENBLAS_INSTALL_DIR}/lib/pkgconfig
EOF