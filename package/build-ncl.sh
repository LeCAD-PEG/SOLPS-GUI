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
VERSION=${VERSION:-6.5.0}
GIT="https://github.com/NCAR/ncl.git"
SRC_DIR="${BUILD_DIR}/ncl-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/ncl/${VERSION}


# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi

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
    cd config
    make -f Makefile.ini
    ./ymake -config `pwd`
    # Manually edit the configuration file, avoiding using the interactive
    # session.
    # Grep the makefile for SYSTEM_INCLUDE
    SYSTEM=$(sed -n 's/SYSTEM_INCLUDE\s*=\s*"\([a-zA-Z]*\)"/\1/p' Makefile)

    # Default parameters should be ok
         # 'CCompiler': '$CC'),
         # 'FCompiler': '$F90'),
         # 'CcOptions': '-ansi $CFLAGS'),
         # 'FcOptions': '$FFLAGS'),
         # 'COptimizeFlag': '$CFLAGS'),
         # 'FOptimizeFlag': '$FFLAGS'),
         # 'ExtraSysLibraries': '$LDFLAGS'),
         # 'CtoFLibraries': -lgfortran -lm
    case ${OS} in
        CentOS)
            LIB_DIRS="-L/usr/lib -L/usr/lib64"
            ;;
        *)
            LIB_DIRS="-L/usr/lib -L/usr/lib/x86_64"
            ;;
    esac
    cat << EOF > Site.local
/*
 *  This file was created by the SOLPS-GUI build script.
 */

#ifdef FirstSite

#endif /* FirstSite */


#ifdef SecondSite

#define YmakeRoot ${INSTALL_DIR}

#define NetCDFlib -lnetcdf

#define LibSearch ${LIB_DIRS}
#define IncSearch -I/usr/include -I/usr/local/include



#define BuildRasterHDF 0
#define HDFlib
#define BuildHDF4 0
#define BuildNetCDF4 0
#define NetCDF4lib
#define BuildUdunits 0
#define UdUnitslib
#define BuildHDFEOS 0
#define HDFEOSlib
#define BuildHDFEOS5 0
#define HDFEOS5lib
#define BuildHDF5 0
#define HDF5lib
#define BuildGRIB2 0
#define GRIB2lib
#define BuildEEMD 0
#define EEMDlib


#endif /* SecondSite */
EOF
    cd ${SRC_DIR}
    ./config/ymkmf
    touch ${SRC_DIR}/.configured
fi


# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make Everything -j${MAKE_JOBS}
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}/lib
    make install
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/ncl ]; then
    install -d ${MODULE_DIR}/ncl
fi

cat << EOF > ${MODULE_DIR}/ncl/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
NCL is an interpreted language designed specifically for scientific data
analysis and visualization.


More information
================
 - Homepage: Homepage: http://www.ncl.ucar.edu
    }
}

module-whatis {Description:
NCL is an interpreted language designed specifically for scientific data
analysis and visualization.
}
module-whatis {Homepage: http://www.ncl.ucar.edu}

conflict ncl

if { ![ is-loaded freetype/${FREETYPE_VERSION} ] } {
    module load freetype/${FREETYPE_VERSION}
}

prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_PATH       ${INSTALL_DIR}/lib
prepend-path CPATH              ${INSTALL_DiR}/include
prepend-path PATH               ${INSTALL_DiR}/bin

EOF