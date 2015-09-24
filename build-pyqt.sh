#!/bin/sh -x

MAKE_JOBS=${MAKE_JOBS:-4}
PYTHON_VERSION=3.4.3
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
CMAKE_VERSION=3.3.0
CMAKE_MAINVERSION=${CMAKE_VERSION%.*}
PyQT_VERSION=5.5
PyQT_MAINVERSION=${PyQT_VERSION%.*}
QT_VERSION=5.5.0
SIP_VERSION=4.16.9

# For Qt5.x build problems on RHEL5 see
# https://forum.qt.io/topic/37757/howto-building-qt-5-2-1-including-webkit-on-rhel5-linux-centos-5-7

BUILDROOT=${PWD}
BUILD_DIR=${BUILDROOT}/build
PATCH_DIR=${BUILDROOT}/src/patches
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${BUILDROOT}/staging
STAGING_QT=${STAGING_DIR}/qt/${QT_VERSION}

set -e

#Initialize directories

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}


#Install python

PYTHON_SRC="Python-${PYTHON_VERSION}.tgz"
PYTHON_DOWNLOAD="https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz"

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
  ./configure --prefix=${STAGING_DIR} --enable-shared
  make -j ${MAKE_JOBS}
  make install
  #make altinstall DESTDIR="${STAGING_DIR}"
  touch ${PYTHON_SRC_DIR}/.built
fi

#Build xcb for Qt5 on RHEL5. See http://doc.qt.io/qt-5/linux-requirements.html
# and http://kate-editor.org/2014/12/22/qt-5-4-on-red-hat-enterprise-5/
if ! test -d /usr/include/xcb ; then
install -d  ${BUILD_DIR}/xcb
cd ${BUILD_DIR}/xcb
for url in \
http://xmlsoft.org/sources/libxml2-2.9.2.tar.gz \
http://xorg.freedesktop.org/archive/individual/proto/xproto-7.0.28.tar.gz \
http://xcb.freedesktop.org/dist/xcb-proto-1.11.tar.gz \
http://xcb.freedesktop.org/dist/libpthread-stubs-0.3.tar.gz \
http://xcb.freedesktop.org/dist/libxcb-1.11.1.tar.gz \
http://xcb.freedesktop.org/dist/xcb-util-0.4.0.tar.gz \
http://xcb.freedesktop.org/dist/xcb-util-image-0.4.0.tar.gz \
http://xcb.freedesktop.org/dist/xcb-util-keysyms-0.4.0.tar.gz \
http://xcb.freedesktop.org/dist/xcb-util-wm-0.4.1.tar.gz \
http://xcb.freedesktop.org/dist/xcb-util-renderutil-0.3.9.tar.gz \
http://xcb.freedesktop.org/dist/xcb-util-cursor-0.1.2.tar.gz \
; do
   file=${url##*/}
   test -f ${file} || wget ${url}
   pkgdir=${file%.*.*}
   test -e ${pkgdir}/.built && continue
   rm -rf ${pkgdir}
   tar xf ${file}
   cd ${pkgdir}
   if [ "${pkgdir%%-*}" = "libxml2"]; then configopt="--without-python"
   else configopt=
   fi
   PKG_CONFIG_PATH=${STAGING_DIR}/lib/pkgconfig \
       ./configure --prefix=${STAGING_DIR} ${configopt} 
   make
   make install
   touch .built
   cd ..
done
cd ${BUILDROOT}
fi

LD_LIBRARY_PATH="${STAGING_DIR}/lib:${LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH

#Install QT

QT_MAJOR_VERSION=${QT_VERSION%.*}
QT_TAR="qt-everywhere-opensource-src-${QT_VERSION}.tar.gz"
QT_DOWNLOAD="http://download.qt.io/official_releases/qt/${QT_MAJOR_VERSION}/${QT_VERSION}/single/${QT_TAR}"
#QT_DOWNLOAD="http://download.qt.io/development_releases/qt/${QT_MAJOR_VERSION}/${QT_VERSION}/single/${QT_TAR}"
QT_SOURCE_DIR="${BUILD_DIR}/qt-everywhere-opensource-src-${QT_VERSION}"

#Download tar and unpack
if [ ! -f ${DOWNLOAD_DIR}/${QT_TAR} ]; then
  wget -P ${DOWNLOAD_DIR} ${QT_DOWNLOAD}
fi

if [ ! -e   ${QT_SOURCE_DIR}/.built ]; then
  #Building QT
  rm -rf ${QT_SOURCE_DIR} ${STAGING_QT} 
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${QT_TAR} 
  
  cd ${QT_SOURCE_DIR}
  sed -i.orig -e 's/-Wno-error=return-type//' \
    qtlocation/src/3rdparty/poly2tri/poly2tri.pro
  patch -p 1 -d ${QT_SOURCE_DIR} < ${PATCH_DIR}/qt5-openssl.patch
  patch -p 1 -d ${QT_SOURCE_DIR} < ${PATCH_DIR}/qt5-no-offscreen.patch
#  patch -p 1 -d ${QT_SOURCE_DIR} < ${PATCH_DIR}/qt5-fontconfig-ultrablack.patch
  patch -p 1 -d ${QT_SOURCE_DIR} < ${PATCH_DIR}/qt5-forkfd.patch
  patch -p 1 -d ${QT_SOURCE_DIR} < ${PATCH_DIR}/qt5-qfbvthandler.patch
  PKG_CONFIG_PATH=${STAGING_DIR}/lib/pkgconfig \
    ./configure -v --prefix=${STAGING_QT} -opensource -confirm-license \
      -shared -no-audio-backend -skip qtwebkit -skip qtwebkit-examples \
      -skip qt3d -xcb -xcb-xlib \
      -qt-xkbcommon -xkb-config-root /usr/share/X11/xkb \
      -D GLX_GLXEXT_LEGACY \
      -D _X_INLINE=inline \
      -D FC_WEIGHT_EXTRABLACK=215 \
      -D FC_WEIGHT_ULTRABLACK=FC_WEIGHT_EXTRABLACK \
      -I${STAGING_DIR}/include -I${STAGING_DIR}/include/libxml2 \
      -L${STAGING_DIR}/lib
  make -j ${MAKE_JOBS}
  make install
  PATH="${STAGING_QT}/bin:${PATH}" make qmake_all docs install_docs 
  touch ${QT_SOURCE_DIR}/.built
fi

#Install sip

PYTHON=${STAGING_DIR}/bin/python${PYTHON_MAINVERSION}

SIP_SRC="sip-${SIP_VERSION}.tar.gz"
SIP_DOWNLOAD="http://sourceforge.net/projects/pyqt/files/sip/sip-${SIP_VERSION}/${SIP_SRC}"

if [ ! -f ${DOWNLOAD_DIR}/${SIP_SRC} ]; then 
    wget  -O ${DOWNLOAD_DIR}/${SIP_SRC} ${SIP_DOWNLOAD}
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

#Install PyQT

PYTHON=${STAGING_DIR}/bin/python${PYTHON_MAINVERSION}

PyQT_SRC="PyQt-gpl-${PyQT_VERSION}.tar.gz"
PyQT_DOWNLOAD="http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-${PyQT_VERSION}/${PyQT_SRC}/download"

if [ ! -f ${DOWNLOAD_DIR}/${PyQT_SRC} ]; then 
    wget  -O ${DOWNLOAD_DIR}/${PyQT_SRC} ${PyQT_DOWNLOAD}
fi

PyQT_SRC_DIR="${BUILD_DIR}/PyQt-gpl-${PyQT_VERSION}"
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

