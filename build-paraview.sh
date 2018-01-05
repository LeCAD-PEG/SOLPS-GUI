#!/bin/sh -x

PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.4.1}
CMAKE_VERSION=3.10.1

case $(hostname -f) in
  *.iter.org)
	module purge
	module load GCC/4.8.3 binutils/2.25 intel/12.0.2
	module load Python/2.7.3-goolf-1.5.16
	module load OpenSSL/1.0.2g-GCC-4.8.3
	#module load Python/2.7.9-gompi-1.5.16-bare
	#module load imas/3.10.1/ual/3.6.0 blitz/0.10 binutils/2.25
        #module load OpenSSL/1.0.2g-GCC-4.8.3
        #module load Python/2.7.9-goolf-1.5.16 # overwrite Anaconda
	#module load libpng/1.6.12-goolf-1.5.16 # needed for Qt4.8.7
	#module load freetype/2.6.2-goolf-1.5.16
	#module load fontconfig/2.11.94-goolf-1.5.16
	export CC=gcc
	export CXX=g++
        CMAKE_EXTRA_FLAGS=${CMAKE_EXTRA_FLAGS:-\
          -DCMAKE_EXE_LINKER_FLAGS:STRING=-L${EBROOTOPENSSL}/lib}
	#PARAVIEW_EXTRA_FLAGS=${PARAVIEW_EXTRA_FLAGS:-\
        #          -DPARAVIEW_ENABLE_PYTHON:BOOL=OFF}
	MAKE_JOBS=${MAKE_JOBS:-8}
	;;
  *.marconi.cineca.it) # EU-IM Gateway with CentOS7.2
	. /etc/profile.d.gw/modules.sh
	module purge
	module load cineca imasenv cmake/3.5.2 
	module switch itm-python/2.7
	module unload matlab
	QT_VERSION=${QT_VERSION:-4.8.7}
	module load itm-qt/${QT_VERSION}
	STAGING_QT=${QTDIR}
	MAKE_JOBS=${MAKE_JOBS:-36}
	export CXXFLAGS=-fpermissive
	PARAVIEW_EXTRA_FLAGS=${PARAVIEW_EXTRA_FLAGS:-\
                        -DPARAVIEW_USE_MPI:BOOL=ON}
	;;
  *)
	;;
esac

QT_VERSION=${QT_VERSION:-4.8.7}
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

# We need recent CMAKE for building ParaView 5.x
CMAKE_TEST=$(hash cmake 2> /dev/null && cmake --version \
             | sed -e 's/[^0-9]//g;s/^\(.\{2\}\).*/\1/')
if [ "${CMAKE_TEST}0" -ge 350 ]
 then CMAKE=cmake
 else CMAKE=${STAGING_DIR}/cmake/${CMAKE_VERSION}/bin/cmake
fi

set -e

# Install cmake as needed
CMAKE_SRC_DIR="${BUILD_DIR}/cmake-${CMAKE_VERSION}"
CMAKE_INSTALL_DIR="${STAGING_DIR}"/cmake/${CMAKE_VERSION}
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
  ./bootstrap --prefix=${STAGING_DIR} -- ${CMAKE_EXTRA_FLAGS}
  make -j ${MAKE_JOBS} VERBOSE=1
  make install
  touch ${CMAKE_SRC_DIR}/.built
fi

#Install QT if needed
if ! test -x ${STAGING_QT}/bin/qmake ; then
    QT_MAJOR_VERSION=${QT_VERSION%.*}
    QT_TAR="qt-everywhere-opensource-src-${QT_VERSION}.tar.gz"
    QT_SITE="http://download.qt.io/official_releases/qt"
    QT_DOWNLOAD="${QT_SITE}/${QT_MAJOR_VERSION}/${QT_VERSION}/${QT_TAR}"
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
	./configure --prefix=${STAGING_QT}  -opensource -confirm-license \
	    -no-javascript-jit -no-webkit -no-script -no-scripttools \
	    -no-sql-sqlite3 -no-accessibility
	make -j ${MAKE_JOBS}
	make install
	touch ${QT_SOURCE_DIR}/.built
    fi
fi

PARAVIEW_BUILD="${BUILD_DIR}/paraview"
PARAVIEW_SOURCE_DIR="${BUILD_DIR}/ParaView-v${PARAVIEW_VERSION}"
#Download Paraview
PARAVIEW_MAJOR_VERSION=${PARAVIEW_VERSION%.*}
PARAVIEW_SOURCE="ParaView-v${PARAVIEW_VERSION}.tar.gz"
PARAVIEW_DATA="ParaViewData-v${PARAVIEW_VERSION}.tar.gz"
PARAVIEW_DOWNLOAD="http://www.paraview.org/files/v${PARAVIEW_MAJOR_VERSION}"
cd ${DOWNLOAD_DIR}

if [ ! -f ${PARAVIEW_SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${PARAVIEW_SOURCE} --no-check-certificate \
        ${PARAVIEW_DOWNLOAD}/${PARAVIEW_SOURCE}
fi

if [ ! -d ${PARAVIEW_SOURCE_DIR} ]; then
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${PARAVIEW_SOURCE}
    # Ignore git describe tags as we are building ParaView from tar.gz
    sed -i -e "/^determine_version/d" ${PARAVIEW_SOURCE_DIR}/CMakeLists.txt
fi


#Configure and build ParaView
if [ ! -e   ${PARAVIEW_BUILD}/.built ]; then
    rm -rf ${PARAVIEW_BUILD}
    install -d ${PARAVIEW_BUILD}
    cd ${PARAVIEW_BUILD}

    if [ ${QT_VERSION%%.*} = 5 ]
	then VTK_RENDERING_BACKEND=OpenGL2
	else VTK_RENDERING_BACKEND=OpenGL
    fi

    install -d ${STAGING_PARAVIEW}
    ${CMAKE} -DCMAKE_BUILD_TYPE:STRING=Release \
	-DVTK_RENDERING_BACKEND:STRING=${VTK_RENDERING_BACKEND} \
	-DPARAVIEW_QT_VERSION:STRING=${QT_VERSION%%.*} \
	-DVTK_QT_VERSION:STRING=${QT_VERSION%%.*} \
        -DBUILD_SHARED_LIBS:BOOL=ON  \
        -DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=ON \
        -DBUILD_TESTING:BOOL=OFF \
        -DPARAVIEW_ENABLE_PYTHON:BOOL=ON \
        -DCMAKE_Fortran_COMPILER:STRING=ifort \
        -DQT_QMAKE_EXECUTABLE:FILEPATH=${STAGING_QT}/bin/qmake \
        -DCMAKE_EXE_LINKER_FLAGS:STRING="-L${STAGING_QT}/lib -Wl,-rpath -Wl,${STAGING_QT/lib}" \
        -DCMAKE_INSTALL_PREFIX:PATH=${STAGING_PARAVIEW} \
	${PARAVIEW_EXTRA_FLAGS} ${PARAVIEW_SOURCE_DIR}
    find .  -name link.txt -exec \
	sed -i -e "s|-lQt|-L${STAGING_QT}/lib -lQt|" \
        -e "s|-L${STAGING_QT}/lib|-L${STAGING_QT}/lib -lQtCore -lQtGui|" {} \;

    LD_LIBRARY_PATH=${STAGING_QT}/lib:${LD_LIBRARY_PATH} \
	make -j ${MAKE_JOBS} VERBOSE=0
    make install
    touch .built
fi

PARAVIEW_DOC_VERSION=${PARAVIEW_DOC_VERSION:-${PARAVIEW_MAJOR_VERSION}.0}
STAGING_DOC=${STAGING_PARAVIEW}/share/paraview-${PARAVIEW_MAJOR_VERSION}/doc
install -d ${STAGING_DOC}
for file in ParaViewGettingStarted-${PARAVIEW_DOC_VERSION%-*}.pdf \
    ParaViewTutorial.pdf  ParaViewGuide-${PARAVIEW_DOC_VERSION%-*}.pdf \
    ParaViewCatalystGuide-${PARAVIEW_DOC_VERSION%-*}.pdf  ; do
    if [ ! -f ${DOWNLOAD_DIR}/${file} ]; then
         wget -O ${DOWNLOAD_DIR}/${file} --no-check-certificate \
             ${PARAVIEW_DOWNLOAD}/${file}
    fi
    noParaView=${file#ParaView}
    noVersion=${noParaView%-*}
    noPdf=${noVersion%.pdf}
    target=${noPdf}.pdf
    install -m 444 ${DOWNLOAD_DIR}/${file} ${STAGING_DOC}/${target}
done




