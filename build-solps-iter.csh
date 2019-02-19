#!/usr/bin/tcsh

# Installation of solps-iter code, to be used with other build scripts in the
# SOLPS-GUI repository as they build and install required packages for
# solps-iter.


if !($?BUILDROOT) then
    setenv BUILDROOT "${PWD}"
endif

if !($?SOLPS_VERSION) then
    set SOLPS_VERSION=3.0.7
endif

# Expecting all the other packages are built in the same directory, inside
# staging directory.
set STAGING_DIR=${BUILDROOT}/staging
# No need for download and build dir. We will git clone the whole solps-iter
# into staging dir.

set SOLPS_GIT="ssh://git@git.iter.org/bnd/solps-iter.git"
set SOLPS_SRC_DIR=${STAGING_DIR}/solps-iter/${SOLPS_VERSION}

if !($?IMASDD_VERSION) then
    setenv IMAS_VERSION 3.21.0
else
    setenv IMAS_VERSION "${IMASDD_VERSION}"
endif

if !($?IMASUAL_VERSION) then
    setenv UAL_VERSION 3.8.4
else
    setenv UAL_VERSION ${IMASUAL_VERSION}
endif

if !($?GGD_VERSION) then
    setenv GGD_VERSION 1.8.3
endif

if !($?MDSPLUS_VERSION) then
    setenv MDSPLUS_VERSION stable_release-7-7-8
endif

setenv IMAS_PREFIX ${STAGING_DIR}/access-layer/${UAL_VERSION}
if !($?PATH) then
    setenv PATH ${STAGING_DIR}/bin
else
    setenv PATH ${STAGING_DIR}/bin:${PATH}
endif

setenv PATH ${STAGING_DIR}/access-layer/${UAL_VERSION}/bin:${PATH}

if !($?PKG_CONFIG_PATH) then
    setenv PKG_CONFIG_PATH ${STAGING_DIR}/access-layer/${UAL_VERSION}/lib/pkgconfig
else
    setenv PKG_CONFIG_PATH ${STAGING_DIR}/access-layer/${UAL_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}
endif

# System PKG_CONFIG_PATH
setenv PKG_CONFIG_PATH /usr/lib/pkgconfig:${PKG_CONFIG_PATH}
# Debian
setenv PKG_CONFIG_PATH /usr/lib/x86_64-linux-gnu/pkgconfig:${PKG_CONFIG_PATH}
# CentOS
setenv PKG_CONFIG_PATH /usr/lib64/pkgconfig

setenv PKG_CONFIG_PATH ${STAGING_DIR}/ggd/${GGD_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}
setenv PKG_CONFIG_PATH ${SOLPS_SRC_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}

if !($?LD_LIBRARY_PATH) then
    setenv LD_LIBRARY_PATH ${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/lib
else
    setenv LD_LIBRARY_PATH ${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/lib:${LD_LIBRARY_PATH}
endif

setenv LD_LIBRARY_PATH ${STAGING_DIR}/lib:${LD_LIBRARY_PATH}

# System LD_LIBRARY_PATH
set GCC_VERSION="`gcc -dumpversion`"
# Debian
setenv LD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu:/usr/lib/gcc/x86_64-linux-gnu/${GCC_VERSION}:${LD_LIBRARY_PATH}
# CentOS
setenv LD_LIBRARY_PATH /usr/lib64/:/usr/lib/gcc/x86_64-redhat-linux/${GCC_VERSION}:${LD_LIBRARY_PATH}

# setenv PKG_CONFIG_PATH ${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}

setenv CPATH /usr/include:/usr/include/x86_64-linux-gnu:/usr/include/freetype:/usr/include/cairo


# solps-iter/SETUP/config.*.gfortran packages locations
setenv MSCL_ROOT ${STAGING_DIR}
setenv GR_ROOT ${STAGING_DIR}
setenv GLI_HOME ${STAGING_DIR}/gli
setenv NCARG_ROOT /usr/lib/x86_64-linux-gnu/ncarg
setenv MDSPLUS_DIR ${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}
setenv MPDIR /usr/lib/x86_64-linux-gnu/openmpi
setenv OPENBLAS_ROOT ${STAGING_DIR}

if (! -e ${SOLPS_SRC_DIR}/.git) then
    git clone --branch feature/config-LECAD ${SOLPS_GIT} --single-branch ${SOLPS_SRC_DIR}
    cd ${SOLPS_SRC_DIR}
    git pull
    git submodule update --init
endif

cd ${SOLPS_SRC_DIR}
source ${SOLPS_SRC_DIR}/setup.csh gfortran
make solps solps_openmp solps_mpi
