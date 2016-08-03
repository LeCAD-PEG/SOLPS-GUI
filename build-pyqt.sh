#!/bin/sh -x
## Building PyQt with Python3 and Qt5
 
PYTHON_VERSION=3.5.2
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
QT_VERSION=5.7.0
PyQT_VERSION=5.7 # should be the same as Qt 
SIP_VERSION=4.18

# Site specific defaults
case $(hostname) in
  *.iter.org) # RHEL5.11 with GCC 4.2
	module purge
	module use /work/imas/opt/EasyBuild/modules/all
	module load GCC/4.8.3 binutils/2.25 python/2.7/11
	USE_QT_XCB="NO"
	BUILD_XCB="YES"
	unset CXX CC # Remove ICC to be selected by chance
        QT_EXTRA_FLAGS=${QT_EXTRA_FLAGS:-\
                        -D GLX_GLXEXT_LEGACY \
                        -D _X_INLINE=inline \
                        -D FC_WEIGHT_EXTRABLACK=215 \
                        -D FC_WEIGHT_ULTRABLACK=FC_WEIGHT_EXTRABLACK}
	;;
  g0[1234]*) # SLES 11.4 WPCD Gateway (incompatible XCB, Xlib and GL libraries)
        MAKE_JOBS=${MAKE_JOBS:-16}
	USE_QT_XCB="NO"
	BUILD_XCB="YES"
	BUILD_XLIB="YES"
        QT_EXTRA_FLAGS=${QT_EXTRA_FLAGS:--no-sql-mysql -no-opengl \
			                 -skip qtcanvas3d -skip qtquick1}
	;;
esac

MAKE_JOBS=${MAKE_JOBS:-4}    # Safe default nowadays
USE_QT_XCB=${USE_QT_XCB:-NO} # Use -qt-xcb for all except RHEL5 if possible
BUILD_XCB=${BUILD_XCB:-NO}   # YES if having problems with -qt-xcb
BUILD_XLIB=${BUILD_XLIB:-NO} # If having libX11-xcb < 1.3.2

BUILDROOT=${PWD}
BUILD_DIR=${BUILDROOT}/build
PATCH_DIR=${BUILDROOT}/src/patches
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
STAGING_QT=${STAGING_QT:-${STAGING_DIR}/qt/${QT_VERSION}}

set -e

## Initialize directories

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

## Install Python3

PYTHON_SRC="Python-${PYTHON_VERSION}.tgz"
PYTHON_SITE="https://www.python.org/ftp/python"
PYTHON_DOWNLOAD="${PYTHON_SITE}/${PYTHON_VERSION}/${PYTHON_SRC}"

if [ ! -f ${DOWNLOAD_DIR}/${PYTHON_SRC} ]; then 
    wget  -O ${DOWNLOAD_DIR}/${PYTHON_SRC} ${PYTHON_DOWNLOAD}
fi

PYTHON_SRC_DIR="${BUILD_DIR}/Python-${PYTHON_VERSION}"
PYTHON_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${PYTHON_SRC_DIR}/.built ]; then
  rm -rf ${PYTHON_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${PYTHON_SRC}
  cd ${PYTHON_SRC_DIR}
  # LDFLAGS for OpenSSL static build see the following
  # http://stackoverflow.com/questions/7307857/libssl-static-lib-compiling-issue-with-fpic
  LDFLAGS="-Wl,-Bsymbolic,-rpath=${STAGING_DIR}/lib" \
  ./configure --prefix=${STAGING_DIR} --enable-shared
  LD_PRELOAD=/usr/lib64/libgssapi_krb5.so:/usr/lib64/libz.so \
  make -j ${MAKE_JOBS}
  LD_PRELOAD=/usr/lib64/libgssapi_krb5.so:/usr/lib64/libz.so \
  make install
  PYTHONPATH= LD_PRELOAD=/usr/lib64/libgssapi_krb5.so:/usr/lib64/libz.so \
  ${STAGING_DIR}/bin/pip3 --trusted-host pypi.python.org install --upgrade sphinx
  touch ${PYTHON_SRC_DIR}/.built
fi

XCB_FLAGS="-xcb -no-xcb-xlib" # XCB is mandatory for Linux 
if [ "${USE_QT_XCB}" = "YES" ]; then # build QT with QT-provided XCB libs
  XCB_FLAGS="${XCB_FLAGS} -qt-xcb"
fi

PYTHON="${STAGING_DIR}/bin/python${PYTHON_MAINVERSION}"

## Build XCB Xlib and libXML for Qt5 locally instead of Qt provided XCB libs.
# For Qt5.x build problems on RHEL5 see
# https://forum.qt.io/topic/37757/howto-building-qt-5-2-1-including-webkit-on-rhel5-linux-centos-5-7
# See http://kate-editor.org/2014/12/22/qt-5-4-on-red-hat-enterprise-5/

URLS="http://xmlsoft.org/sources/libxml2-2.9.3.tar.gz"

if [ "${BUILD_XCB}" = "YES" ]; then
  URLS="${URLS} \
  http://xorg.freedesktop.org/archive/individual/proto/xproto-7.0.28.tar.gz\
  http://xcb.freedesktop.org/dist/xcb-proto-1.11.tar.gz \
  http://xcb.freedesktop.org/dist/libpthread-stubs-0.3.tar.gz \
  http://xcb.freedesktop.org/dist/libxcb-1.11.1.tar.gz \
  http://xcb.freedesktop.org/dist/xcb-util-0.4.0.tar.gz \
  http://xcb.freedesktop.org/dist/xcb-util-image-0.4.0.tar.gz \
  http://xcb.freedesktop.org/dist/xcb-util-keysyms-0.4.0.tar.gz \
  http://xcb.freedesktop.org/dist/xcb-util-wm-0.4.1.tar.gz \
  http://xcb.freedesktop.org/dist/xcb-util-renderutil-0.3.9.tar.gz \
  http://xcb.freedesktop.org/dist/xcb-util-cursor-0.1.2.tar.gz"
  XCB_INCLUDES="-I${STAGING_DIR}/include -I${STAGING_DIR}/include/libxml2"
  XCB_LIBS="-L${STAGING_DIR}/lib"
  XCB_FLAGS="${XCB_FLAGS} ${XCB_INCLUDES} ${XCB_LIBS}"
fi

if [ "${BUILD_XLIB}" = "YES" ] ; then 
  URLS="${URLS} http://www.x.org/releases/X11R7.7/src/lib/libX11-1.5.0.tar.gz"
fi

install -d  ${BUILD_DIR}/libs
cd ${BUILD_DIR}/libs
for url in ${URLS}; do
  file=${url##*/}
  test -f ${DOWNLOAD_DIR}/${file} || wget -O ${DOWNLOAD_DIR}/${file} ${url}
  pkgdir=${file%.*.*}
  test -e ${pkgdir}/.built && continue
  rm -rf ${pkgdir}
  tar xf ${DOWNLOAD_DIR}/${file}
  cd ${pkgdir}
  if [ "${pkgdir%%-*}" = "libxml2" ]; then configopt="--without-python"
  else configopt=
  fi
  PKG_CONFIG_PATH=${STAGING_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH} \
  PYTHON=${PYTHON} ./configure --prefix=${STAGING_DIR} ${configopt}
  make -j ${MAKE_JOBS}
  make install
  touch .built
  cd ..
done

## Install QT

QT_MAJOR_VERSION=${QT_VERSION%.*}
QT_TAR="qt-everywhere-opensource-src-${QT_VERSION}.tar.gz"
QT_SITE="http://download.qt.io/official_releases/qt"
#QT_SITE="http://download.qt.io/development_releases/qt/"
QT_DOWNLOAD="${QT_SITE}/${QT_MAJOR_VERSION}/${QT_VERSION}/single/${QT_TAR}"

QT_SOURCE_DIR="${BUILD_DIR}/qt-everywhere-opensource-src-${QT_VERSION}"

if [ ! -f ${DOWNLOAD_DIR}/${QT_TAR} ]; then
  wget -P ${DOWNLOAD_DIR} ${QT_DOWNLOAD}
fi


if [ ! -e ${QT_SOURCE_DIR}/.configured ]; then # Configuring Qt
  rm -rf ${QT_SOURCE_DIR} ${STAGING_QT} 
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${QT_TAR} 
  cd ${QT_SOURCE_DIR}
  sed -i.orig -e 's/-Wno-error=return-type//' \
      qtlocation/src/3rdparty/poly2tri/poly2tri.pro
  patch -p 1 -d ${QT_SOURCE_DIR} < ${PATCH_DIR}/qt5-openssl.patch
  patch -p 1 -d ${QT_SOURCE_DIR} < ${PATCH_DIR}/qt5-no-offscreen.patch
  patch -p 1 -d ${QT_SOURCE_DIR} < ${PATCH_DIR}/qt5-qfbvthandler.patch
  patch -p 1 -d ${QT_SOURCE_DIR}<${PATCH_DIR}/qglxintegration-glx-context.patch
  patch -p 1 -d ${QT_SOURCE_DIR} < ${PATCH_DIR}/qt5-qxcbconnection.patch
  patch -p 1 -d ${QT_SOURCE_DIR} < ${PATCH_DIR}/qt5-qbenchmarkperfevents.patch
  #patch -p 1 -d ${QT_SOURCE_DIR} < ${PATCH_DIR}/qsimd.cpp-gcc4.2.patch
  sed -i -e '/auto/d' qtdeclarative/tests/tests.pro \
                      qtmultimedia/tests/tests.pro \
                      qtgraphicaleffects/tests/tests.pro
  PKG_CONFIG_PATH=${STAGING_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH} \
    ./configure -v --prefix=${STAGING_QT} -opensource -confirm-license \
      -shared -no-audio-backend \
      -skip qtgamepad \
      -skip qtwebchannel \
      -skip qtwebengine \
      -skip qtwebsockets \
      -skip qtwebview \
      -skip qt3d ${XCB_FLAGS} ${QT_EXTRA_FLAGS} \
      -qt-xkbcommon -xkb-config-root /usr/share/X11/xkb
  touch ${QT_SOURCE_DIR}/.configured
fi

if [ ! -e ${QT_SOURCE_DIR}/.built ]; then  ## Building Qt and docs
  cd ${QT_SOURCE_DIR}
  make -j ${MAKE_JOBS}
  make install
  # Building Qt documentation
  PATH="${STAGING_QT}/bin:${PATH}" make -C qttools/src sub-qdoc
  PATH="${STAGING_QT}/bin:${PATH}" make -C qtbase/src html_docs
  PATH="${STAGING_QT}/bin:${PATH}" make qmake_all
  PATH="${STAGING_QT}/bin:${PATH}" make -j ${MAKE_JOBS} docs install_docs
  touch ${QT_SOURCE_DIR}/.built
fi # building Qt

## Install sip

SIP_SRC="sip-${SIP_VERSION}.tar.gz"
SIP_SITE="http://sourceforge.net/projects/pyqt/files/sip"
SIP_DOWNLOAD="${SIP_SITE}/sip-${SIP_VERSION}/${SIP_SRC}/download"

if [ ! -f ${DOWNLOAD_DIR}/${SIP_SRC} ]; then 
    wget -O ${DOWNLOAD_DIR}/${SIP_SRC} --no-check-certificate \
          ${SIP_DOWNLOAD}
fi

SIP_SRC_DIR="${BUILD_DIR}/sip-${SIP_VERSION}"
SIP_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${SIP_SRC_DIR}/.built ]; then
  rm -rf ${SIP_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${SIP_SRC}
  cd ${SIP_SRC_DIR}
  ${PYTHON} configure.py
  make -j ${MAKE_JOBS}
  make install 
  touch ${SIP_SRC_DIR}/.built
fi

## Install PyQT

PyQT_SRC="PyQt5_gpl-${PyQT_VERSION}.tar.gz"
PyQT_SITE="http://sourceforge.net/projects/pyqt/files/PyQt5"
#PyQT_SITE="https://www.riverbankcomputing.com/static/Downloads/PyQt5}"
PyQT_DOWNLOAD="${PyQT_SITE}/PyQt-${PyQT_VERSION}/${PyQT_SRC}/download"


if [ ! -f ${DOWNLOAD_DIR}/${PyQT_SRC} ]; then 
    wget  -O ${DOWNLOAD_DIR}/${PyQT_SRC} --no-check-certificate \
        ${PyQT_DOWNLOAD}
fi

PyQT_SRC_DIR="${BUILD_DIR}/PyQt5_gpl-${PyQT_VERSION}"
PyQT_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${PyQT_SRC_DIR}/.built ]; then
  rm -rf ${PyQT_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${PyQT_SRC}
  cd ${PyQT_SRC_DIR}
  ${PYTHON} configure.py --confirm-license --verbose \
      --qmake=${STAGING_DIR}/qt/${QT_VERSION}/bin/qmake \
      --sip=${STAGING_DIR}/bin/sip
  make -j ${MAKE_JOBS}
  make install 
  touch ${PyQT_SRC_DIR}/.built
fi
