#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="netcdf"
VERSION=${VERSION:-4.7.4}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="https://github.com/Unidata/netcdf-c/archive/v${VERSION}.tar.gz"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

# PRE_FLAGS="CPPFLAGS=\"-I${H5DIR}/include\\\ -L${ODIR}/include\" LDFLAGS=\"-L${H5DIR}/lib\\\ -L${ODIR}/lib\""
CONFIGURE_FLAGS="--enable-netcdf-4"
# --with-CURL=${ODIR} --with-HDF5=${H5DIR}"

export CPPFLAGS="-I${H5DIR}/include -I${ODIR}/include"
export LDFLAGS="-L${H5DIR}/lib -L${ODIR}/lib"
_configure "${CONFIGURE_FLAGS}"
_make "-j${MAKE_JOBS}"
_install