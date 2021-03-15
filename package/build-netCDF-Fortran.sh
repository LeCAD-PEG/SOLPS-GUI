#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="netcdf-fortran"
VERSION=${VERSION:-4.5.3}
DOWNLOAD_LINK="https://github.com/Unidata/netcdf-fortran/archive/v${VERSION}.zip"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"
if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}


cd ${PACKAGE_SOURCE_DIR}

#ODIR is CURLDIR for some reason... forgot why it has to be set like that
PRE_FLAGS="CPPFLAGS=\"-I${NCDIR}/include -L${ODIR}/include\" LDFLAGS=\"-L${NCDIR}/lib -L\${ODIR}/lib\""
CMAKE_FLAGS="-DCMAKE_PREFIX_PATH=\"${ODIR} ${NCDIR}\""
CMAKE_FLAGS="${CMAKE_FLAGS} -DnetCDF_LIBRARY_DIR=\"${NCDIR}/lib/libnetcdf.so\""
CMAKE_FLAGS="${CMAKE_FLAGS} -DnetCDF_INCLUDE_DIR=\"${NCDIR}/include\""

_cmake ${CMAKE_FLAGS} ${PRE_FLAGS}
_make "-j1"
_install
