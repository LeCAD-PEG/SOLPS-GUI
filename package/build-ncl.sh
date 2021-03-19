
#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="ncl"
VERSION=${VERSION:-6.5.0}
DOWNLOAD_LINK="https://github.com/NCAR/ncl/archive/refs/tags/${VERSION}.tar.gz"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

cd ${PACKAGE_SOURCE_DIR}
cd config
make -f Makefile.ini
./ymake -config `pwd`

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

#define YmakeRoot ${PACKAGE_INSTALL_DIR}

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
cd ${PACKAGE_SOURCE_DIR}
./config/ymkmf

_make "Everything -j${MAKE_JOBS}"
_install
