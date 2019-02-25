#!/bin/sh -x
set -e


# Variables
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

# Buildroot directories
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
DOWNLOAD_DIR=${BUILDROOT}/download

# Package variables
VERSION=${VERSION:-1.8.3}
GIT="ssh://git@git.iter.org/imex/ggd.git"
SRC_DIR="${BUILD_DIR}/ggd-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/GGD/${VERSION}


# Environment dependencies
case $(hostname -f) in
    *)
        IMASDD_VERSION=${IMASDD_VERSION:-3.21.0}
        IMASUAL_VERSION=${IMASUAL_VERSION:-3.8.4}
        VERSION=${VERSION:-1.8.3}

        MDSPLUS_VERSION=${MDSPLUS_VERSION:-stable_release-7-7-8}
        MDSPLUS_INSTALL_DIR=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}

        export IMAS_VERSION=${IMASDD_VERSION}
        export UAL_VERSION=${IMASUAL_VERSION}
        IMAS_INSTALL_DIR=${STAGING_DIR}/imas/${IMASDD_VERSION}/solps

        export IMAS_PREFIX=${IMAS_INSTALL_DIR}
        export PATH=${IMAS_INSTALL_DIR}/bin:${PATH}

        export LD_LIBRARY_PATH=${IMAS_INSTALL_DIR}/lib:${LD_LIBRARY_PATH}
        export LD_LIBRARY_PATH=${MDSPLUS_INSTALL_DIR}/lib:${LD_LIBRARY_PATH}
        export PKG_CONFIG_PATH=${IMAS_INSTALL_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}
        export PKG_CONFIG_PATH=${MDSPLUS_INSTALL_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}

        export ids_path=${IMAS_INSTALL_DIR}/models/mdsplus

        export imasfortran_LIBS="-L${IMAS_INSTALL_DIR}/lib -limas-gfortran -limas"
        export imasfortran_CFLAGS="-I${IMAS_INSTALL_DIR}/include/gfortran"

        export FC=gfortran
        ;;
esac

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    git clone --branch ${VERSION} --single-branch ${GIT} ${SRC_DIR}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    ./bootstrap
    ./configure --prefix=${INSTALL_DIR} --enable-doc --enable-tests \
                --enable-modulefile \
                --with-module-prefix=${INSTALL_DIR}/include
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make #-j ${MAKE_JOBS}
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -e ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    make install
fi

# Check
if [ ! -e ${SRC_DIR}/.checked ]; then
    make check
    touch ${SRC_DIR}/.checked
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/GGD ]; then
    install -d ${MODULE_DIR}/GGD
fi

cat << EOF > ${MODULE_DIR}/GGD/${VERSION}
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

if { ![ is-loaded imas/${IMAS_VERSION}/solps ] } {
    module load imas/${IMAS_VERSION}/solps
}

prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_PATH       ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkgconfig
EOF