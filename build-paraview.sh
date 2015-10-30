#!/bin/sh -x

PARAVIEW_VERSION=4.4.0
QT_VERSION=4.8.7

case $(hostname) in
  *.iter.org) 
	module use /work/imas/etc/modulefiles \
	    /work/imas/opt/EasyBuild/modules/all
	module load goolf binutils cmake python/2.7/10
	PYTHON_LIBRARY=/work/imas/opt/python/2.7/10/lib/libpython2.7.a
	PYTHON_INCLUDE_DIR=/work/imas/opt/python/2.7/10/include/python2.7
	unset CC CXX # we don't want ICC 11.1 to be selected
	MAKE_JOBS=${MAKE_JOBS:-4}
  which gcc
	;;
  *)
	MAKE_JOBS=${MAKE_JOBS:-8}
	;;
esac


BUILDROOT=${PWD}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${BUILDROOT}/staging
#STAGING_DIR=/work/imas/project
STAGING_QT=${STAGING_DIR}/qt/${QT_VERSION}
STAGING_PARAVIEW=${STAGING_DIR}/paraview/${PARAVIEW_VERSION}

#Initialize directories

install -d ${BUILD_DIR}
install -d ${DOWNLOAD_DIR}
install -d ${STAGING_DIR}

set -e

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
PARAVIEW_SOURCE_DIR="${BUILD_DIR}/ParaView-v${PARAVIEW_VERSION}-source"
#Download Paraview
PARAVIEW_MAJOR_VERSION=${PARAVIEW_VERSION%.*}
PARAVIEW_SOURCE="ParaView-v${PARAVIEW_VERSION}-source.tar.gz"
PARAVIEW_DOWNLOAD="download.php?submit=Download&version=v${PARAVIEW_MAJOR_VERSION}&type=source&os=all&downloadFile=ParaView-v${PARAVIEW_VERSION}-source.tar.gz"

cd ${DOWNLOAD_DIR}
if [ ! -f ${PARAVIEW_SOURCE} ]; then
    curl -vO http://www.paraview.org/paraview-downloads/${PARAVIEW_DOWNLOAD} 
    mv ${PARAVIEW_DOWNLOAD} ${PARAVIEW_SOURCE}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${PARAVIEW_SOURCE}
# See https://github.com/OpenFOAM/ThirdParty-dev/blob/master/README.org
    patch -p2 -d ${PARAVIEW_SOURCE_DIR} < \
        ${BUILDROOT}/src/patches/paraview-ui_pqExportStateWizard.patch
fi

#Configure and build paraview
rm -rf ${PARAVIEW_BUILD}
install -d ${PARAVIEW_BUILD}
cd ${PARAVIEW_BUILD}
install -d ${STAGING_PARAVIEW}
cmake -DCMAKE_BUILD_TYPE:STRING=Release \
                -DBUILD_SHARED_LIBS:BOOL=ON  \
                -DVTK_USE_RPATH:BOOL=OFF \
                -DVTK_USE_TK:BOOL=OFF \
                -DPARAVIEW_INSTALL_DEVELOPMENT:BOOL=ON \
                -DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=ON \
                -DBUILD_TESTING:BOOL=OFF \
                -DPARAVIEW_ENABLE_PYTHON:BOOL=ON \
                -DPYTHON_LIBRARY:FILEPATH=${PYTHON_LIBRARY} \
                -DPYTHON_INCLUDE_DIR:PATH=${PYTHON_INCLUDE_DIR} \
                -DPARAVIEW_INSTALL_THIRD_PARTY_LIBRARIES:BOOL=OFF \
                -DPARAVIEW_USE_MPI:BOOL=OFF \
                -DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=ON \
                -DQT_QMAKE_EXECUTABLE:FILEPATH=${STAGING_QT}/bin/qmake \
                -DCMAKE_EXE_LINKER_FLAGS:String="-L${STAGING_QT}/lib" \
                -DCMAKE_INSTALL_PREFIX:PATH=${STAGING_PARAVIEW} \
                -DPQWIDGETS_DISABLE_QTWEBKIT:BOOL=ON \
		-DVTK_QT_USE_WEBKIT:BOOL=OFF  ${PARAVIEW_SOURCE_DIR}
make -j ${MAKE_JOBS}
make install
