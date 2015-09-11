#!/bin/sh -x

PYTHON_VERSION=3.4.3
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
CMAKE_VERSION=3.3.0
CMAKE_MAINVERSION=${CMAKE_VERSION%.*}
PyQT_VERSION=4.11.4
PyQT_MAINVERSION=${PyQT_VERSION%.*}
QT_VERSION=4.8.6
SIP_VERSION=4.16.9

BUILDROOT=${PWD}
BUILD_DIR=${BUILDROOT}/build
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
  ./configure 
  make -j 8
  make altinstall DESTDIR="${STAGING_DIR}"
  touch ${PYTHON_SRC_DIR}/.built
fi

#Install QT

QT_MAJOR_VERSION=${QT_VERSION%.*}
QT_TAR="qt-everywhere-opensource-src-${QT_VERSION}.tar.gz"
QT_DOWNLOAD="http://ftp.fau.de/qtproject/official_releases/qt/${QT_MAJOR_VERSION}/${QT_VERSION}/${QT_TAR}"
QT_SOURCE_DIR="${BUILD_DIR}/qt-everywhere-opensource-src-${QT_VERSION}"

#Download tar and unpack
if [ ! -f ${DOWNLOAD_DIR}/${QT_TAR} ]; then
  wget -P ${DOWNLOAD_DIR} ${QT_DOWNLOAD}
fi

if [ ! -e   ${QT_SOURCE_DIR}/.built ]; then
  #Building QT
  rm -rf ${QT_SOURCE_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${QT_TAR} 
  
  cd ${QT_SOURCE_DIR}
  echo 'yes' | ./configure --prefix=${STAGING_QT} -opensource
  make -j 8
  make install 
  touch ${QT_SOURCE_DIR}/.built
fi

#Instal sip

PYTHON=${STAGING_DIR}/usr/local/bin/python${PYTHON_MAINVERSION}

SIP_SRC="sip-${SIP_VERSION}.tar.gz"
SIP_DOWNLOAD="http://sourceforge.net/projects/pyqt/files/sip/sip-${SIP_VERSION}/sip-${SIP_VERSION}.tar.gz"

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
  make -j 8
  make install 
  touch ${SIP_SRC_DIR}/.built
fi

#Install pyQT

PYTHON=${STAGING_DIR}/usr/local/bin/python${PYTHON_MAINVERSION}

PyQT_SRC="PyQt-gpl-${PyQT_VERSION}.tar.gz"
PyQT_DOWNLOAD="http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-${PyQT_VERSION}/PyQt-x11-gpl-${PyQT_VERSION}.tar.gz/download"

if [ ! -f ${DOWNLOAD_DIR}/${PyQT_SRC} ]; then 
    wget  -O ${DOWNLOAD_DIR}/${PyQT_SRC} ${PyQT_DOWNLOAD}
fi

PyQT_SRC_DIR="${BUILD_DIR}/PyQt-x11-gpl-${PyQT_VERSION}"
PyQT_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${PyQT_SRC_DIR}/.built ]; then
  rm -rf ${PyQT_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${PyQT_SRC}
  cd ${PyQT_SRC_DIR}
  echo 'yes' | ${PYTHON} configure.py --qmake=${STAGING_DIR}/qt/${QT_VERSION}/bin/qmake 
  make -j 8
  make install DESTDIR="${STAGING_DIR}"
  touch ${PyQT_SRC_DIR}/.built
fi

