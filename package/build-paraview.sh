#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="paraview"
VERSION=${VERSION:-5.8.1}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="http://www.paraview.org/files/v${VERSION%.*}/ParaView-v${VERSION}.tar.xz"
FILENAME="${PACKAGE}-${VERSION}.tar.xz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

PYTHON3_PATH=$(which python3)
IFS='.' read -r -a ver_arr <<< "${VERSION}"
FORTRAN_COMPILER_FOR_CATALYST=${FORTRAN_COMPILER_FOR_CATALYST:-ifort}

CMAKE_FLAGS="-DCMAKE_BUILD_TYPE:STRING=Release"
CMAKE_FLAGS="${CMAKE_FLAGS} -DPARAVIEW_BUILD_SHARED_LIBS:BOOL=ON"
CMAKE_FLAGS="${CMAKE_FLAGS} -DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=ON"
CMAKE_FLAGS="${CMAKE_FLAGS} -DBUILD_TESTING:BOOL=OFF"
CMAKE_FLAGS="${CMAKE_FLAGS} -DUSE_SYSTEM_PYTHON:BOOL=OFF"

if [ "$((ver_arr[0]))" -eq "5" ]; then # Version major check for 5
    if [ "$((ver_arr[1]))" -ge "8" ]; then # Minor version check for 8
        CMAKE_FLAGS="${CMAKE_FLAGS} -DPARAVIEW_USE_PYTHON:BOOL=ON"
        CMAKE_FLAGS="${CMAKE_FLAGS} -DPARAVIEW_PYTHON_VERSION=3"
        CMAKE_FLAGS="${CMAKE_FLAGS} -DPython3_INCLUDE_DIR:STRING=${PYTHON_INSTALL_DIR}/include/python${PYTHON_MAINVERSION}"
        CMAKE_FLAGS="${CMAKE_FLAGS} -DPython3_LIBRARY:STRING=${PYTHON_INSTALL_DIR}/lib/libpython${PYTHON_MAINVERSION}.so"
    else # Lower versions than 8
        CMAKE_FLAGS="${CMAKE_FLAGS} -DPARAVIEW_PYTHON_LIBRARY:FILEPATH=${STAGING_DIR}/python/${PYTHON_VERSION}/lib/libpython3.so"
        CMAKE_FLAGS="${CMAKE_FLAGS} -DPYTHON_EXECUTABLE:FILEPATH=${PYTHON3_PATH}"
        CMAKE_FLAGS="${CMAKE_FLAGS} -DPARAVIEW_ENABLE_PYTHON:BOOL=ON"
    fi
fi

CMAKE_FLAGS="${CMAKE_FLAGS} -DCMAKE_Fortran_COMPILER:STRING=${FORTRAN_COMPILER_FOR_CATALYST}"
CMAKE_FLAGS="${CMAKE_FLAGS} -DQT_QMAKE_EXECUTABLE:FILEPATH=${STAGING_DIR}/qt/${QT_VERSION}/bin/qmake"
CMAKE_FLAGS="${CMAKE_FLAGS} -DCMAKE_VERBOSE_MAKEFILE:BOOL=OFF"
CMAKE_FLAGS="${CMAKE_FLAGS} ${PARAVIEW_EXTRA_FLAGS}"

_cmake "${CMAKE_FLAGS}"
_make "-j${MAKE_JOBS} --silent"
_install

# Post Installation
DOC_VERSION=${DOC_VERSION:-${VERSION%.*}.0}
INSTALL_DOC_DIR=${PACKAGE_INSTALL_DIR}/share/paraview-${VERSION%.*}/doc
install -d ${INSTALL_DOC_DIR}
for file in ParaViewGettingStarted-${DOC_VERSION%-*}.pdf \
    ParaViewTutorial-${DOC_VERSION%-*}.pdf  ParaViewGuide-${DOC_VERSION%-*}.pdf \
    ParaViewCatalystGuide-${DOC_VERSION%-*}.pdf  ; do
    if [ ! -f ${DOWNLOAD_DIR}/${file} ]; then
         wget -O ${DOWNLOAD_DIR}/${file} --no-check-certificate \
             http://www.paraview.org/files/v${VERSION%.*}/${file}
    fi
    noParaView=${file#ParaView}
    noVersion=${noParaView%-*}
    noPdf=${noVersion%.pdf}
    target=${noPdf}.pdf
    install -m 444 ${DOWNLOAD_DIR}/${file} ${INSTALL_DOC_DIR}/${target}
done