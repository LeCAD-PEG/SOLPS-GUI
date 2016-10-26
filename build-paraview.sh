#!/bin/sh -x

PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.1.2}
QT_VERSION=${QT_VERSION:-4.8.7}
CMAKE_VERSION=3.6.1
case $(hostname) in
  *.iter.org) 
	module purge
#	module load MVAPICH2/2.2b-GCC-4.9.3-2.25
	module load GCC/4.8.3 binutils/2.25
	module load python/2.7/11 intel/12.0.2 
	export CC=gcc
	export CXX=g++
	MAKE_JOBS=${MAKE_JOBS:-8}
	;;
  *)
	;;
esac

MAKE_JOBS=${MAKE_JOBS:-4}

BUILDROOT=${PWD}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${DOWNLOAD_DIR:-${BUILDROOT}/download}
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
#STAGING_DIR=${SWITMDIR}
STAGING_QT=${STAGING_QT:-${STAGING_DIR}/qt/${QT_VERSION}}
STAGING_PARAVIEW=${STAGING_PARAVIEW:-$STAGING_DIR/paraview/$PARAVIEW_VERSION}

#Initialize directories

install -d ${BUILD_DIR}
install -d ${DOWNLOAD_DIR}
install -d ${STAGING_DIR}

set -e

# We need recent CMAKE for building ParaView 5.1
if [ $(cmake --version | sed 's/[^0-9]//g;s/^\(.\{2\}\).*/\1/' ) -ge 35 ]
 then CMAKE=cmake
 else CMAKE=${STAGING_DIR}/bin/cmake
fi

# Install cmake as needed
CMAKE_SRC_DIR="${BUILD_DIR}/cmake-${CMAKE_VERSION}"
CMAKE_INSTALL_DIR="${STAGING_DIR}"
if [ ${CMAKE} != cmake -a  ! -e  ${CMAKE_SRC_DIR}/.built ]; then
  CMAKE_SRC="cmake-${CMAKE_VERSION}.tar.gz"
  CMAKE_MAIN_VERSION=${CMAKE_VERSION%.*}
  CMAKE_SITE="https://cmake.org/files/v${CMAKE_MAIN_VERSION}"
  CMAKE_DOWNLOAD="${CMAKE_SITE}/cmake-${CMAKE_VERSION}.tar.gz"
  if [ ! -f ${DOWNLOAD_DIR}/${CMAKE_SRC} ]; then
     wget  -O ${DOWNLOAD_DIR}/${CMAKE_SRC} --no-check-certificate \
	 ${CMAKE_DOWNLOAD}
  fi
  rm -rf ${CMAKE_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${CMAKE_SRC}
  cd ${CMAKE_SRC_DIR}
  ./bootstrap --prefix=${STAGING_DIR}
  make -j ${MAKE_JOBS}
  make install
  touch ${CMAKE_SRC_DIR}/.built
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

PARAVIEW_BUILD="${BUILD_DIR}/paraview"
PARAVIEW_SOURCE_DIR="${BUILD_DIR}/ParaView-v${PARAVIEW_VERSION}"
#Download Paraview
PARAVIEW_MAJOR_VERSION=${PARAVIEW_VERSION%.*}
PARAVIEW_SOURCE="ParaView-v${PARAVIEW_VERSION}.tar.gz"
PARAVIEW_DATA="ParaViewData-v${PARAVIEW_VERSION}.tar.gz"
PARAVIEW_DOWNLOAD="http://www.paraview.org/files/v${PARAVIEW_MAJOR_VERSION}"
cd ${DOWNLOAD_DIR}
if [ ! -f ${PARAVIEW_DATA} ]; then # download examples and tutorials
    wget -O ${DOWNLOAD_DIR}/${PARAVIEW_DATA} --no-check-certificate \
        ${PARAVIEW_DOWNLOAD}/${PARAVIEW_DATA}
fi

if [ ! -f ${PARAVIEW_SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${PARAVIEW_SOURCE} --no-check-certificate \
        ${PARAVIEW_DOWNLOAD}/${PARAVIEW_SOURCE}
fi

if [ ! -d ${PARAVIEW_SOURCE_DIR} ]; then
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${PARAVIEW_SOURCE}
    tar xzf ${DOWNLOAD_DIR}/${PARAVIEW_DATA}
# See https://github.com/OpenFOAM/ThirdParty-dev/blob/master/README.org
    patch -p2 -d ${PARAVIEW_SOURCE_DIR} < \
        ${BUILDROOT}/src/patches/paraview-ui_pqExportStateWizard.patch
    patch -p1 -d ${PARAVIEW_SOURCE_DIR} < \
        ${BUILDROOT}/src/patches/paraview-vtk-storage-mkostemp.patch
fi


#Configure and build paraview
rm -rf ${PARAVIEW_BUILD}
install -d ${PARAVIEW_BUILD}
cd ${PARAVIEW_BUILD}

install -d ${STAGING_PARAVIEW}
${CMAKE} -DCMAKE_BUILD_TYPE:STRING=Release \
                -DBUILD_SHARED_LIBS:BOOL=ON  \
                -DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=ON \
                -DBUILD_TESTING:BOOL=OFF \
                -DPARAVIEW_ENABLE_PYTHON:BOOL=ON \
                -DCMAKE_Fortran_COMPILER:STRING=ifort \
                -DPARAVIEW_USE_MPI:BOOL=OFF \
                -DQT_QMAKE_EXECUTABLE:FILEPATH=${STAGING_QT}/bin/qmake \
                -DCMAKE_EXE_LINKER_FLAGS:STRING="-L${STAGING_QT}/lib" \
                -DCMAKE_INSTALL_PREFIX:PATH=${STAGING_PARAVIEW} \
		 ${PARAVIEW_SOURCE_DIR}
find .  -name link.txt -exec \
    sed -i -e "s|-lQt|-L${STAGING_QT}/lib -lQt|" \
           -e "s|-L${STAGING_QT}/lib|-L${STAGING_QT}/lib -lQtCore -lQtGui|" {} \;

LD_LIBRARY_PATH=${STAGING_QT}/lib:${LD_LIBRARY_PATH} \
make -j ${MAKE_JOBS} VERBOSE=1
make install

touch .built

