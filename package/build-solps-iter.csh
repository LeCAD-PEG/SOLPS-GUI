#!/usr/bin/tcsh

# Installation of solps-iter code, to be used with other build scripts in the
# SOLPS-GUI repository as they build and install required packages for
# solps-iter.


if !($?BUILDROOT) then
    # Hack for getting the BUILDROOT directory when executing the script.
    set tmp_builddir = `dirname $0`
    set abs_tmp_builddir = `cd ${tmp_builddir}/.. && pwd`
    setenv BUILDROOT "${abs_tmp_builddir}"
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

if !($?MSCL_VERSION) then
    setenv MSCL_VERSION 1.1.1
endif

if !($?GR_VERSION) then
    setenv GR_VERSION 0.0.94
endif

if !($?GLI_VERSION) then
    setenv GLI_VERSION 4.5.30
endif

if !($?MDSPLUS_VERSION) then
    setenv MDSPLUS_VERSION stable_release-7-7-8
endif

if !($?OPENBLAS_VERSION) then
    setenv OPENBLAS_VERSION 0.3.5
endif

setenv IMAS_PREFIX ${STAGING_DIR}/imas/${IMAS_VERSION}/solps
if !($?PATH) then
    setenv PATH ${STAGING_DIR}/bin
else
    setenv PATH ${STAGING_DIR}/bin:${PATH}
endif

setenv PATH ${STAGING_DIR}/imas/${IMAS_VERSION}/solps/bin:${PATH}

if !($?PKG_CONFIG_PATH) then
    setenv PKG_CONFIG_PATH ${STAGING_DIR}/imas/${IMAS_VERSION}/solps/lib/pkgconfig
else
    setenv PKG_CONFIG_PATH ${STAGING_DIR}/imas/${IMAS_VERSION}/solps/lib/pkgconfig:${PKG_CONFIG_PATH}
endif

# System PKG_CONFIG_PATH
setenv PKG_CONFIG_PATH /usr/lib/pkgconfig:${PKG_CONFIG_PATH}
# Debian
setenv PKG_CONFIG_PATH /usr/lib/x86_64-linux-gnu/pkgconfig:${PKG_CONFIG_PATH}
# CentOS
setenv PKG_CONFIG_PATH /usr/lib64/pkgconfig:${PKG_CONFIG_PATH}

setenv PKG_CONFIG_PATH ${STAGING_DIR}/GGD/${GGD_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}

setenv PKG_CONFIG_PATH ${SOLPS_SRC_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}

setenv PKG_CONFIG_PATH ${STAGING_DIR}/mscl/${MSCL_VERSION}/pkgconfig:${PKG_CONFIG_PATH}

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
setenv NCDIR /usr
setenv MSCL_ROOT ${STAGING_DIR}/mscl/${MSCL_VERSION}
setenv GR_ROOT ${STAGING_DIR}/GR/${GR_VERSION}
setenv GLI_HOME ${STAGING_DIR}/GLI/${GLI_VERSION}
setenv MDSPLUS_DIR ${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}

if ( -f /etc/redhat-release ) then
    setenv NCARG_ROOT /usr/lib64/ncarg
    # setenv MPDIR /usr/lib64/openmpi
    module load mpi/openmpi-x86_64
else
    setenv NCARG_ROOT /usr/lib/x86_64-linux-gnu/ncarg
    setenv MPDIR /usr/lib/x86_64-linux-gnu/openmpi
endif

setenv OPENBLAS_ROOT ${STAGING_DIR}/OpenBLAS/${OPENBLAS_VERSION}/lib

if (! -e ${SOLPS_SRC_DIR}/.git) then
    git clone --branch feature/config-LECAD ${SOLPS_GIT} --single-branch ${SOLPS_SRC_DIR}
    cd ${SOLPS_SRC_DIR}
    git pull
    git submodule update --init
endif

cd ${SOLPS_SRC_DIR}
source ${SOLPS_SRC_DIR}/setup.csh gfortran
# make solps solps_openmp solps_mpi # Problem with manual, maybe because it is being called three times?
make carre divgeo b25eirene uinp triang amds sonnet-light b25eirene_openmp b25eirene_mpi uinp_mpi amds_mpi manual
