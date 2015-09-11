#!/bin/sh -x

PYTHON_VERSION=3.4.3
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
CMAKE_VERSION=3.3.0
CMAKE_MAINVERSION=${CMAKE_VERSION%.*}
PyQT_VERSION=5.5
PyQT_MAINVERSION=${PyQT_VERSION%.*}
QT_VERSION=4.8.6

#TCLTK_VERSION=8.6.4
#FREETYPE_VERSION=2.5.3
#GL2PS_VERSION=1.3.8
#FREEIMAGE_VERSION=3.15.0
#VTK_VERSION=6.1.0
#VTK_MAINVERSION=${VTK_VERSION%.*}
#LIBPNG_VERSION=1.2.49

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
#QT_DOWNLOAD="http://download.qt.io/official_releases/qt/${QT_MAJOR_VERSION}/${QT_VERSION}/single/qt-everywhere-opensource-src-${QT_VERSION}.tar.gz"
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

#Install pyQT5

PYTHON=${STAGING_DIR}/usr/local/bin/python${PYTHON_MAINVERSION}

PyQT_SRC="PyQt-gpl-${PyQT_VERSION}.tar.gz"
PyQT_DOWNLOAD="http://sourceforge.net/projects/pyqt/files/PyQt${PyQT_MAINVERSION}/PyQt-${PyQT_VERSION}/PyQt-gpl-${PyQT_VERSION}.tar.gz"

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
  ${PYTHON} configure.py --qmake=${STAGING_DIR}/qt/${QT_VERSION}/bin
  make -j 8
  make install DESTDIR="${STAGING_DIR}"
  touch ${PyQT_SRC_DIR}/.built
fi

exit 1

#Install cmake

CMAKE_SRC="cmake-${CMAKE_VERSION}.tar.gz"
CMAKE_DOWNLOAD="http://www.cmake.org/files/v${CMAKE_MAINVERSION}/cmake-${CMAKE_VERSION}.tar.gz"

if [ ! -f ${DOWNLOAD_DIR}/${CMAKE_SRC} ]; then 
    wget  -O ${DOWNLOAD_DIR}/${CMAKE_SRC} ${CMAKE_DOWNLOAD}
fi

CMAKE_SRC_DIR="${BUILD_DIR}/cmake-${CMAKE_VERSION}"
CMAKE_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${CMAKE_SRC_DIR}/.built ]; then
  rm -rf ${CMAKE_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${CMAKE_SRC}
  cd ${CMAKE_SRC_DIR}
  ./bootstrap 
  make -j 8
  make install DESTDIR="${STAGING_DIR}"
  touch ${CMAKE_SRC_DIR}/.built
fi

CMAKE=${STAGING_DIR}/usr/local/bin/cmake


#Install libpng

LIBPNG_SRC="libpng-${LIBPNG_VERSION}.tar.gz"
LIBPNG_DOWNLOAD="http://sourceforge.net/projects/libpng/files/libpng12/older-releases/${LIBPNG_VERSION}/libpng-${LIBPNG_VERSION}.tar.gz/download"

if [ ! -f ${DOWNLOAD_DIR}/${LIBPNG_SRC} ]; then 
    wget  -O ${DOWNLOAD_DIR}/${LIBPNG_SRC} ${LIBPNG_DOWNLOAD}
fi

LIBPNG_SRC_DIR="${BUILD_DIR}/libpng-${LIBPNG_VERSION}"
LIBPNG_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${LIBPNG_SRC_DIR}/.built ]; then
  rm -rf ${LIBPNG_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${LIBPNG_SRC}
  cd ${LIBPNG_SRC_DIR}
  ./configure  --prefix=${LIBPNG_INSTALL_DIR} 
  make -j 8
  make install
  touch ${LIBPNG_SRC_DIR}/.built
  fi




# Install Tcl and Tk build

TCL_SRC="tcl${TCLTK_VERSION}-src.tar.gz"
TK_SRC="tk${TCLTK_VERSION}-src.tar.gz"
TCL_DOWNLOAD="http://prdownloads.sourceforge.net/tcl/${TCL_SRC}"
TK_DOWNLOAD="http://prdownloads.sourceforge.net/tcl/${TK_SRC}"

if [ ! -f ${DOWNLOAD_DIR}/${TCL_SRC} ]; then 
    wget -P ${DOWNLOAD_DIR} ${TCL_DOWNLOAD}
    wget -P ${DOWNLOAD_DIR} ${TK_DOWNLOAD}
fi

TCL_SRC_DIR="${BUILD_DIR}/tcl${TCLTK_VERSION}"
TCL_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${TCL_SRC_DIR}/.built ]; then
  rm -rf ${TCL_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${TCL_SRC}
  cd ${TCL_SRC_DIR}/unix
  ./configure --enable-gcc  --enable-shared --enable-threads --prefix=${TCL_INSTALL_DIR}
  make -j 8
  make install
  touch ${TCL_SRC_DIR}/.built
fi


TK_SRC_DIR="${BUILD_DIR}/tk${TCLTK_VERSION}"
TK_INSTALL_DIR="${STAGING_DIR}"
TCL_LIB_DIR="${TCL_INSTALL_DIR}/lib"

if [ ! -e   ${TK_SRC_DIR}/.built ]; then
  rm -rf ${TK_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${TK_SRC}
  cd ${TK_SRC_DIR}/unix
  ./configure --enable-gcc  --enable-shared --enable-threads --with-tcl=${TCL_LIB_DIR} \
      --prefix=${TK_INSTALL_DIR}
  make -j 8
  make install
  touch ${TK_SRC_DIR}/.built
fi

# Install FreeType

FREETYPE_SRC="freetype-${FREETYPE_VERSION}.tar.bz2"
FREETYPE_DOWNLOAD="http://downloads.sourceforge.net/project/freetype/freetype2/${FREETYPE_VERSION}/${FREETYPE_SRC}"

if [ ! -f ${DOWNLOAD_DIR}/${FREETYPE_SRC} ]; then 
    wget -P ${DOWNLOAD_DIR} "${FREETYPE_DOWNLOAD}"
fi

FREETYPE_SRC_DIR="${BUILD_DIR}/freetype-${FREETYPE_VERSION}"
FREETYPE_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${FREETYPE_SRC_DIR}/.built ]; then
  rm -rf ${FREETYPE_SRC_DIR}
  cd ${BUILD_DIR}
  tar xjf ${DOWNLOAD_DIR}/${FREETYPE_SRC}
  cd ${FREETYPE_SRC_DIR}
  ./configure --with-png=${LIBPNG_SRC_DIR} --prefix=${FREETYPE_INSTALL_DIR} 
  make -j 8
  make install
  touch ${FREETYPE_SRC_DIR}/.built
fi

#Install TBB

TBB_SRC="tbb43_20150611oss_lin.tgz"
TBB_DOWNLOAD="https://www.threadingbuildingblocks.org/sites/default/files/software_releases/linux/${TBB_SRC}"

if [ ! -f ${DOWNLOAD_DIR}/${TBB_SRC} ]; then 
    wget -P ${DOWNLOAD_DIR} ${TBB_DOWNLOAD}
fi

TBB_SRC_DIR="${BUILD_DIR}/tbb43_20150611oss"
TBB_INSTALL_DIR="${TBB_SRC_DIR}"

if [ ! -e   ${TBB_SRC_DIR}/.built ]; then
  rm -rf ${TBB_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${TBB_SRC}
  touch ${TBB_SRC_DIR}/.built
fi

#Install gl2ps

GL2PS_SRC="gl2ps-${GL2PS_VERSION}.tgz"
GL2PS_DOWNLOAD="http://geuz.org/gl2ps/src/${GL2PS_SRC}"

if [ ! -f ${DOWNLOAD_DIR}/${GL2PS_SRC} ]; then 
    wget -P ${DOWNLOAD_DIR} ${GL2PS_DOWNLOAD}
fi

GL2PS_SRC_DIR="${BUILD_DIR}/gl2ps-${GL2PS_VERSION}-source"
GL2PS_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${GL2PS_SRC_DIR}/.built ]; then
  rm -rf ${GL2PS_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${GL2PS_SRC}
  cd ${GL2PS_SRC_DIR}
  ${CMAKE} -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=${GL2PS_INSTALL_DIR} .
  make -j 8
  make install
  touch ${GL2PS_SRC_DIR}/.built
fi

#Install FreeImage
FREEIMAGE_VERSION2=$(echo "${FREEIMAGE_VERSION}" | tr -d . )
FREEIMAGE_SRC=FreeImage${FREEIMAGE_VERSION2}.zip
FREEIMAGE_DOWNLOAD=http://sourceforge.net/projects/freeimage/files/Source%20Distribution/${FREEIMAGE_VERSION}/${FREEIMAGE_SRC}/download

if [ ! -f ${DOWNLOAD_DIR}/${FREEIMAGE_SRC} ]; then 
    wget  -O ${DOWNLOAD_DIR}/${FREEIMAGE_SRC} ${FREEIMAGE_DOWNLOAD}
fi

FREEIMAGE_SRC_DIR="${BUILD_DIR}/FreeImage"
FREEIMAGE_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${FREEIMAGE_SRC_DIR}/.built ]; then
  rm -rf ${FREEIMAGE_SRC_DIR}
  cd ${BUILD_DIR}
  unzip ${DOWNLOAD_DIR}/${FREEIMAGE_SRC}
  
#  patch -p3 -d ${FREEIMAGE_SRC_DIR} < \
#        ${BUILDROOT}/src/patch/ImathMatrix.patch
  sed -i -e  's/-o root -g root//' ${FREEIMAGE_SRC_DIR}/Makefile.gnu
  sed -i -e '/ldconfig/d' ${FREEIMAGE_SRC_DIR}/Makefile.gnu
  
  cd ${FREEIMAGE_SRC_DIR}
  
  make -j 8
  make install DESTDIR="${STAGING_DIR}"
  make clean
  touch ${FREEIMAGE_SRC_DIR}/.built
fi

#Install VTK

VTK_SRC="VTK-${VTK_VERSION}.tar.gz"
VTK_DOWNLOAD="http://www.vtk.org/files/release/${VTK_MAINVERSION}/VTK-${VTK_VERSION}.tar.gz"

if [ ! -f ${DOWNLOAD_DIR}/${VTK_SRC} ]; then 
    wget -P ${DOWNLOAD_DIR} ${VTK_DOWNLOAD}
fi

VTK_SRC_DIR="${BUILD_DIR}/VTK-${VTK_VERSION}"
VTK_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${VTK_SRC_DIR}/.built ]; then
  rm -rf ${VTK_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${VTK_SRC}
  install -d ${VTK_SRC_DIR}/build
  cd ${VTK_SRC_DIR}/build
  ${CMAKE} -DCMAKE_BUILD_TYPE:STRING=Release \
      -DCMAKE_INSTALL_PREFIX:STRING=${VTK_INSTALL_DIR} \
      -DBUILD_EXAMPLES:BOOL=OFF .. 
  make -j 8
  make install
  touch ${VTK_SRC_DIR}/.built
fi


