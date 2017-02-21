#!/bin/bash -x
## Building PyQt with Python2 and Qt4
## Minimum GCC supported version for building Qt5 is 4.7
 
PYTHON_VERSION=2.7.13
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
QT_VERSION=${QT_VERSION:-4.8.7}
PyQT_VERSION=4.12 # should be the same as Qt 
SIP_VERSION=4.19

# Site specific defaults
case $(hostname -f) in
  *.iter.org) # RHEL5.11 with GCC 4.2
	module purge
	# module load GCC/4.8.3 binutils/2.25 python/2.7/11 #gperf
        module load imas/3.7.2/ual/3.3.14
	USE_QT_XCB="NO"
	BUILD_XCB="YES"
	unset CXX CC # Remove ICC to be selected by chance
        QT_EXTRA_FLAGS=${QT_EXTRA_FLAGS:-\
                        -D GLX_GLXEXT_LEGACY \
                        -D _X_INLINE=inline \
                        -D FC_WEIGHT_EXTRABLACK=215 \
                        -D FC_WEIGHT_ULTRABLACK=FC_WEIGHT_EXTRABLACK}
	;;
  # SLES 11.4 WPCD Gateway (incompatible XCB, Xlib and GL libraries)
  g0[1234].itm.rzg.mpg.de \
  | tok*.bc.rzg.mpg.de) # IPP MPG 
        MAKE_JOBS=${MAKE_JOBS:-16}
	USE_QT_XCB="NO"
	BUILD_XCB="YES"
	BUILD_XLIB="YES"
        QT_EXTRA_FLAGS=${QT_EXTRA_FLAGS:--no-sql-mysql -no-opengl \
			                 -skip qtcanvas3d  -skip qtpurchasing \
					 -skip qtvirtualkeyboard}
	;;

  *.marconi.cineca.it) # CentOS 7, 
        MAKE_JOBS=${MAKE_JOBS:-16}
	. /etc/profile.d.gw/modules.sh
	# module unload itm-gcc/6.1.0 itm-python/2.7
	module switch itm-python/2.7.13.b1
	module unload itm-gcc/6.1.0 gcc/6.1.0
	USE_QT_XCB="NO"
	BUILD_XCB="NO"
	BUILD_XLIB="NO"
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

## Install Python2

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
  if pkg-config --exists libssl; then
    ssl=$(pkg-config --variable=prefix libssl)
    sed -i -e "s,#SSL=.*,SSL=${ssl}," -e "/^#.*ssl/s/#//" \
	-e '/ssl/s|-lcrypto|-lcrypto -Wl,-rpath,$(SSL)/lib|' Modules/Setup.dist
  fi
  ./configure --prefix=${STAGING_DIR} --enable-shared
  make -j ${MAKE_JOBS}
  make install
  LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} PYTHONPATH= \
#  ${STAGING_DIR}/bin/pip --trusted-host pypi.python.org install --upgrade \
#      pip sphinx sphinx_rtd_theme matplotlib mock nose
  # The following Python modules are preferred by IMAS
  if [ -n "${IMAS_PREFIX}" ]; then
    LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} PYTHONPATH= \
    ${STAGING_DIR}/bin/pip --trusted-host pypi.python.org install --upgrade \
      Cython mpi4py scipy luigi tornado deap decorator liac-arff ecdsa \
      netaddr paramiko paycheck # netifaces 
  fi
  touch ${PYTHON_SRC_DIR}/.built
fi


#Install QT
QT_MAJOR_VERSION=${QT_VERSION%.*}
QT_TAR="qt-everywhere-opensource-src-${QT_VERSION}.tar.gz"
QT_DOWNLOAD="http://download.qt.io/official_releases/qt/${QT_MAJOR_VERSION}/${QT_VERSION}/${QT_TAR}"
QT_SOURCE_DIR="${BUILD_DIR}/qt-everywhere-opensource-src-${QT_VERSION}"

#Download tar and unpack
if [ ! -f ${DOWNLOAD_DIR}/${QT_TAR} ]; then
  cd ${DOWNLOAD_DIR}
  wget ${QT_DOWNLOAD}
fi

if [ ! -e   ${QT_SOURCE_DIR}/.built ]; then
  #Building QT
  rm -rf ${QT_SOURCE_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${QT_TAR} 
  
  cd ${QT_SOURCE_DIR}
  ./configure --prefix=${STAGING_QT} -no-webkit -opensource -confirm-license
  make -j ${MAKE_JOBS}
  make install 
  touch ${QT_SOURCE_DIR}/.built
fi

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
PYTHON=${STAGING_DIR}/bin/python2.7


if [ ! -e   ${SIP_SRC_DIR}/.built ]; then
  rm -rf ${SIP_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${SIP_SRC}
  cd ${SIP_SRC_DIR}
  LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} PYTHONPATH= \
  ${PYTHON} configure.py
  make -j ${MAKE_JOBS}
  make install 
  touch ${SIP_SRC_DIR}/.built
fi

## Install PyQT

PyQT_SRC="PyQt4_gpl_x11-${PyQT_VERSION}.tar.gz"
PyQT_SITE="http://sourceforge.net/projects/pyqt/files/PyQt4"
PyQT_DOWNLOAD="${PyQT_SITE}/PyQt-${PyQT_VERSION}/${PyQT_SRC}/download"


if [ ! -f ${DOWNLOAD_DIR}/${PyQT_SRC} ]; then 
    wget  -O ${DOWNLOAD_DIR}/${PyQT_SRC} --no-check-certificate \
        ${PyQT_DOWNLOAD}
fi

PyQT_SRC_DIR="${BUILD_DIR}/PyQt4_gpl_x11-${PyQT_VERSION}"
PyQT_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${PyQT_SRC_DIR}/.built ]; then
  rm -rf ${PyQT_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${PyQT_SRC}
  cd ${PyQT_SRC_DIR}
  LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} PYTHONPATH= \
  ${PYTHON} configure.py --confirm-license --verbose \
      --qmake=${STAGING_DIR}/qt/${QT_VERSION}/bin/qmake \
      --sip=${STAGING_DIR}/bin/sip
  make -j ${MAKE_JOBS}
  make install 
  touch ${PyQT_SRC_DIR}/.built
fi
