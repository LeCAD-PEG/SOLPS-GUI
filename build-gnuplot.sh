#!/bin/sh -x
source setupenv.sh
MAKE_JOBS=${MAKE_JOBS:-4}
GNUPLOT_VERSION=${GNUPLOT_VERSION:-5.2.1}
QT_VERSION=${QT_VERSION:-5.9.1}

BUILDROOT=${PWD}
BUILD_DIR=${BUILDROOT}/build
PATCH_DIR=${BUILDROOT}/src/patches
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
STAGING_QT=${STAGING_QT:-${STAGING_DIR}/qt/${QT_VERSION}}

case $(hostname -f) in
  *.iter.org)
        module purge
	#module load GCC
        module load imas binutils
        module unload Anaconda2
        qmake --version && sip -V
        QT_VERSION=5.6.2 PyQT_VERSION=5.6.2 SIP_VERSION=4.18
        STAGING_QT=${EBROOTANACONDA3}/pkgs/qt-5.6.2-3
        QT_LIBS=$(pkg-config --libs Qt5Network Qt5Svg Qt5PrintSupport\
                  Qt5Widgets Qt5Gui Qt5Core)
        QT_LIBS="-Wl,-rpath=${EBROOTANACONDA3}/lib ${QT_LIBS}"
        export QT_LIBS="-L${EBROOTANACONDA3}/lib -liconv ${QT_LIBS}"
        GNUPLOT_INSTALL_DIR=${GNUPLOT_INSTALL_DIR:-${STAGING_DIR}}
	MAKE_JOBS=${MAKE_JOBS:-4}
	;;

  *)
	;;
esac

set -e

#Initialize directories

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

LD_LIBRARY_PATH="${STAGING_DIR}/lib:${LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
PKG_CONFIG_PATH="${STAGING_DIR}/qt/${QT_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}"
export PKG_CONFIG_PATH

GNUPLOT_SRC="gnuplot-${GNUPLOT_VERSION}.tar.gz"
GNUPLOT_SITE="http://sourceforge.net/projects/gnuplot/files/gnuplot"
GNUPLOT_DOWNLOAD="${GNUPLOT_SITE}/${GNUPLOT_VERSION}/${GNUPLOT_SRC}/download"

if [ ! -f ${DOWNLOAD_DIR}/${GNUPLOT_SRC} ]; then
    wget  -O ${DOWNLOAD_DIR}/${GNUPLOT_SRC} ${GNUPLOT_DOWNLOAD} \
        --no-check-certificate
fi

GNUPLOT_SRC_DIR=${BUILD_DIR}/gnuplot-${GNUPLOT_VERSION}
GNUPLOT_INSTALL_DIR=${GNUPLOT_INSTALL_DIR:-${STAGING_DIR}}

if [ ! -e   ${GNUPLOT_SRC_DIR}/.built ]; then
  rm -rf ${GNUPLOT_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${GNUPLOT_SRC}
  cd ${GNUPLOT_SRC_DIR}
  libtoolize
  export CXXFLAGS=" -std=c++11"
  ./configure --without-cairo --prefix=${GNUPLOT_INSTALL_DIR} \
      --with-qt=qt5 --without-libcerf
  make -j ${MAKE_JOBS}
  make install
  touch ${GNUPLOT_SRC_DIR}/.built
fi

